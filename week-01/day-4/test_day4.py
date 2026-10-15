"""Week 1, Day 4 - the library's version, and tracing the graph.

Run me:  pytest week-01/day-4 -v
"""

import json

import pytest
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage

from models import ScriptedModel, call, say


class Recording(BaseCallbackHandler):
    def __init__(self):
        self.model_calls = []

    def on_chat_model_start(self, serialized, messages, **kwargs):
        self.model_calls.append(kwargs.get("metadata") or {})


@pytest.fixture
def prebuilt(load):
    return load("prebuilt.py")


@pytest.fixture
def desk(load):
    return load("desk_graph.py")


def script():
    return [call("add_note", {"title": "dentist", "body": "Tue"}), say("Saved it.")]


class TestThePrebuiltAgent:
    def test_same_answer_same_notes(self, prebuilt, desk, notes_file, tmp_path, monkeypatch):
        mine = desk.ask(desk.build_graph(ScriptedModel(script())), "save dentist")
        my_notes = json.loads(notes_file.read_text())

        theirs_file = tmp_path / "theirs.json"
        monkeypatch.setenv("NOTES_FILE", str(theirs_file))
        agent = prebuilt.build_prebuilt(ScriptedModel(script()))
        theirs = agent.invoke({"messages": [HumanMessage("save dentist")]})["messages"][-1].content

        assert mine == theirs == "Saved it."
        assert json.loads(theirs_file.read_text()) == my_notes

    def test_it_sends_the_same_system_prompt(self, prebuilt, desk):
        model = ScriptedModel(say("Hi."))
        prebuilt.build_prebuilt(model).invoke({"messages": [HumanMessage("hi")]})
        assert model.last_request["messages"][0].content == desk.SYSTEM


class TestTracing:
    def test_config(self, prebuilt):
        handler = Recording()
        assert prebuilt.config_for("alice", "s1", [handler], limit=7) == {
            "callbacks": [handler], "recursion_limit": 7,
            "metadata": {"langfuse_user_id": "alice", "langfuse_session_id": "s1"}}

    def test_every_model_call_carries_the_user_and_session(self, prebuilt, desk, notes_file):
        handler = Recording()
        desk.ask(desk.build_graph(ScriptedModel(script())), "save dentist",
                 config=prebuilt.config_for("alice", "s1", [handler]))
        assert len(handler.model_calls) == 2
        for metadata in handler.model_calls:
            assert metadata.get("langfuse_user_id") == "alice"
            assert metadata.get("langfuse_session_id") == "s1"


@pytest.mark.parametrize("name,headings", [
    ("COMPARE.md", ["What is the same", "What is different",
                    "What the graph's trace shows that mine did not",
                    "What mine showed that the graph's does not"]),
    ("READING.md", ["Where is the loop?", "What decides whether the tools run again?",
                    "What does it do that my graph does not?",
                    "What would I change to stop before a tool runs?"]),
])
def test_written(source, name, headings):
    text = source(name)
    assert "<!--" not in text, f"Delete the instructions comment in {name}."
    for heading in headings:
        assert f"## {heading}" in text, f"{name} has no '{heading}' section."
        part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(part.split()) >= 30, f"{name} '{heading}' is {len(part.split())} words."
