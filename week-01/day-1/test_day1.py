"""Week 1, Day 1 - the hand-written Desk, traced.

Run me:  pytest week-01/day-1 -v

The tests use a fake Langfuse client that writes the trace down instead of
sending it, so you can see exactly what your code would send.
"""

import contextlib
import json

import pytest

from llm import FakeModel, say, use


class Observation:
    def __init__(self, recorder, parent, **fields):
        self.recorder, self.parent, self.fields = recorder, parent, fields
        self.children = []
        self.updates = {}

    def update(self, **fields):
        self.updates.update(fields)

    def __enter__(self):
        self.recorder.stack.append(self)
        return self

    def __exit__(self, *exc):
        self.recorder.stack.pop()
        return False


class FakeLangfuse:
    def __init__(self):
        self.stack, self.roots, self.propagated = [], [], []

    def start_as_current_observation(self, **fields):
        parent = self.stack[-1] if self.stack else None
        observation = Observation(self, parent, **fields)
        (parent.children if parent else self.roots).append(observation)
        return observation

    @contextlib.contextmanager
    def propagate(self, **attributes):
        self.propagated.append(attributes)
        yield


@pytest.fixture
def traced(load):
    return load("traced.py")


@pytest.fixture
def client():
    return FakeLangfuse()


class TestTracedModel:
    def test_records_a_generation(self, traced, client):
        model = traced.TracedModel(FakeModel(say("Hi.", input=12, output=3)), client)
        reply = model.chat([{"role": "user", "content": "hello"}])
        assert reply["text"] == "Hi."
        generation = client.roots[0]
        assert generation.fields["as_type"] == "generation" and generation.fields["name"] == "model"
        assert generation.fields["input"] == [{"role": "user", "content": "hello"}]
        assert generation.updates["output"] == "Hi."
        assert generation.updates["usage_details"] == {"input": 12, "output": 3}

    def test_a_tool_call_is_the_output(self, traced, client):
        model = traced.TracedModel(FakeModel(use("list_titles")), client)
        model.chat([{"role": "user", "content": "list"}])
        assert client.roots[0].updates["output"][0]["name"] == "list_titles"

    def test_passes_everything_on(self, traced, client):
        fake = FakeModel(say("ok"))
        traced.TracedModel(fake, client).chat([{"role": "user", "content": "x"}], system="Be brief.")
        assert fake.last_request["system"] == "Be brief."


class TestTracedTools:
    def test_one_tool(self, traced, client):
        tool = traced.traced(lambda title: f"Saved '{title}'.", "add_note", client)
        assert tool(title="dentist") == "Saved 'dentist'."
        observation = client.roots[0]
        assert observation.fields == {"as_type": "tool", "name": "add_note", "input": {"title": "dentist"}}
        assert observation.updates["output"] == "Saved 'dentist'."

    def test_a_table(self, traced, client):
        table = traced.traced_tools({"a": lambda: "A", "b": lambda: "B"}, client)
        assert sorted(table) == ["a", "b"] and table["b"]() == "B"


class TestOneTurn:
    def test_one_trace_nested(self, traced, client, notes_file):
        model = FakeModel([use("add_note", {"title": "dentist", "body": "Tuesday"}), say("Saved.")])
        answer = traced.run_traced(model, "save dentist", "alice", "s1", client, client.propagate)
        assert answer == "Saved."
        assert len(client.roots) == 1, "One turn is one trace: everything must sit under one root."
        root = client.roots[0]
        assert root.fields["as_type"] == "agent" and root.fields["name"] == "desk"
        assert root.fields["input"] == "save dentist" and root.updates["output"] == "Saved."
        kinds = [(child.fields["as_type"], child.fields["name"]) for child in root.children]
        assert kinds == [("generation", "model"), ("tool", "add_note"), ("generation", "model")]

    def test_user_and_session(self, traced, client, notes_file):
        traced.run_traced(FakeModel(say("Hi.")), "hi", "alice", "s1", client, client.propagate)
        assert client.propagated == [{"user_id": "alice", "session_id": "s1"}]

    def test_desk_really_ran(self, traced, client, notes_file):
        model = FakeModel([use("add_note", {"title": "dentist"}), say("Saved.")])
        traced.run_traced(model, "save dentist", "alice", "s1", client, client.propagate)
        assert [note["title"] for note in json.loads(notes_file.read_text())] == ["dentist"]


class TestReadingATrace:
    def test_written(self, source):
        text = source("READING_A_TRACE.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("The shape", "Where the time went", "Where the tokens went", "What I could not see"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 30, f"'{heading}' is {len(part.split())} words."
