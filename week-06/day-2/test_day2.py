"""Week 6, Day 2 - facts go stale.

Run me:  pytest week-06/day-2 -v
"""

import pytest
from langchain_core.messages import HumanMessage

from models import ScriptedModel, call, say


@pytest.fixture
def stale(load):
    return load("stale.py")


@pytest.fixture
def store(load, tmp_path):
    return load("facts.py").open_store(str(tmp_path / "m.db"))


class TestUpdate:
    def test_new_unchanged_updated(self, stale, store):
        assert stale.update_fact(store, "c1", "Address", "Bristol", "2026-09-01") == "new"
        assert stale.update_fact(store, "c1", "address", "Bristol", "2026-09-20") == "unchanged"
        assert stale.update_fact(store, "c1", "address", "Leeds", "2026-10-15") == "updated"
        assert stale.history(store, "c1", "address") == [
            {"fact": "Bristol", "since": "2026-09-01", "until": "2026-10-15"},
            {"fact": "Leeds", "since": "2026-10-15", "until": None}]

    def test_no_history(self, stale, store):
        assert stale.history(store, "c1", "address") == []


class TestForget:
    def test_one_topic(self, stale, store):
        stale.update_fact(store, "c1", "address", "Leeds", "2026-10-15")
        assert stale.forget(store, "c1", "address") == 1
        assert stale.forget(store, "c1", "address") == 0

    def test_everything(self, stale, store):
        for topic in ("address", "contact", "size"):
            stale.update_fact(store, "c1", topic, "x", "2026-10-15")
        stale.update_fact(store, "c2", "address", "York", "2026-10-15")
        assert stale.forget(store, "c1") == 3
        assert stale.facts_for_prompt(store, "c1") == ""
        assert stale.facts_for_prompt(store, "c2") != "", "Forgetting one customer must not touch another."

    def test_forget_me_through_a_graph(self, stale, store, load):
        facts = load("facts.py")
        stale.update_fact(store, "c1", "address", "Leeds", "2026-10-15")
        tools = facts.MEMORY_TOOLS + [stale.forget_me]
        from langgraph.graph import START, StateGraph
        from langgraph.prebuilt import ToolNode
        model = ScriptedModel([call("forget_me")])
        graph = StateGraph(load("tools.py").HelpState)
        graph.add_node("model", lambda s: {"messages": [model.invoke(s["messages"])]})
        graph.add_node("tools", ToolNode(tools))
        graph.add_edge(START, "model")
        graph.add_edge("model", "tools")
        result = graph.compile(store=store).invoke({"messages": [HumanMessage("forget me")], "customer": "c1"})
        assert result["messages"][-1].content == "Forgotten 1 facts."


class TestForThePrompt:
    def test_newest_first_and_capped(self, stale, store):
        stale.update_fact(store, "c1", "address", "Leeds", "2026-10-15")
        stale.update_fact(store, "c1", "contact", "email", "2026-08-01")
        stale.update_fact(store, "c1", "size", "medium", "2026-09-10")
        assert stale.facts_for_prompt(store, "c1", limit=2) == (
            f"{stale.HEADER}\n- address: Leeds (since 2026-10-15)\n- size: medium (since 2026-09-10)")

    def test_a_fact_from_day_1_has_no_since(self, stale, store, load):
        store.put(load("facts.py").namespace("c1"), "contact", {"fact": "phone"})
        assert stale.facts_for_prompt(store, "c1").endswith("- contact: phone")

    def test_nothing(self, stale, store):
        assert stale.facts_for_prompt(store, "c9") == ""
