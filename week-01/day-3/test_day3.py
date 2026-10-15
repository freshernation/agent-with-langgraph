"""Week 1, Day 3 - Desk as a graph.

Run me:  pytest week-01/day-3 -v
"""

import json

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from models import ScriptedModel, call, calls, say


@pytest.fixture
def desk(load):
    return load("desk_graph.py")


def titles(notes_file):
    return [note["title"] for note in json.loads(notes_file.read_text())]


class TestTheTools:
    def test_four_described_tools(self, desk):
        assert [each.name for each in desk.TOOLS] == ["add_note", "list_titles", "find_notes", "calculate"]
        for each in desk.TOOLS:
            assert len(each.description.split()) >= 8, f"{each.name}'s description is too short."

    def test_the_schema_is_the_hints(self, desk):
        assert set(desk.add_note.args) == {"title", "body"}
        assert desk.add_note.invoke({"title": "x"}) == "Saved 'x'."


class TestTheNodes:
    def test_call_model_returns_only_the_new_message(self, desk):
        model = ScriptedModel(say("Hi."))
        out = desk.call_model({"messages": [HumanMessage("hi")]}, model)
        assert len(out["messages"]) == 1 and out["messages"][0].content == "Hi."

    def test_call_model_sends_the_system_prompt_and_tools(self, desk):
        model = ScriptedModel(say("Hi."))
        desk.call_model({"messages": [HumanMessage("hi")]}, model)
        sent = model.last_request
        assert sent["messages"][0].content == desk.SYSTEM
        assert len(sent["tools"]) == 4

    def test_run_tools(self, desk, notes_file):
        state = {"messages": [calls([("add_note", {"title": "a"}), ("list_titles", {})])]}
        out = desk.run_tools(state)["messages"]
        assert [m.content for m in out] == ["Saved 'a'.", "1. a"]
        assert [m.tool_call_id for m in out] == ["call_1", "call_2"]

    def test_unknown_tool(self, desk):
        out = desk.run_tools({"messages": [call("delete_note", {"title": "a"})]})["messages"]
        assert out[0].content == "Error: there is no tool called delete_note."

    def test_bad_arguments_do_not_crash(self, desk):
        out = desk.run_tools({"messages": [call("add_note", {})]})["messages"]
        assert out[0].content.startswith("Error:")

    def test_route(self, desk):
        assert desk.route({"messages": [call("list_titles")]}) == "tools"
        assert desk.route({"messages": [say("done")]}) == "__end__"


class TestTheGraph:
    def test_shape(self, desk):
        drawn = desk.build_graph(ScriptedModel()).get_graph()
        assert set(drawn.nodes) == {"__start__", "model", "tools", "__end__"}

    def test_a_turn_with_a_tool(self, desk, notes_file):
        model = ScriptedModel([call("add_note", {"title": "dentist", "body": "Tue"}), say("Saved it.")])
        assert desk.ask(desk.build_graph(model), "save dentist") == "Saved it."
        assert titles(notes_file) == ["dentist"]
        assert model.call_count == 2

    def test_the_tool_result_goes_back_to_the_model(self, desk, notes_file):
        model = ScriptedModel([call("calculate", {"expression": "6*7"}), say("42")])
        desk.ask(desk.build_graph(model), "6 times 7?")
        sent = model.last_request["messages"]
        assert sent[-1].content == "42" and sent[-2].tool_calls, (
            "The second model call must see its own tool call and the result."
        )

    def test_no_tool(self, desk):
        assert desk.ask(desk.build_graph(ScriptedModel(say("Hello."))), "hi") == "Hello."

    def test_a_model_that_never_stops(self, desk, notes_file):
        model = ScriptedModel(call("list_titles"))
        assert desk.ask(desk.build_graph(model), "loop", limit=6) == desk.STOPPED
