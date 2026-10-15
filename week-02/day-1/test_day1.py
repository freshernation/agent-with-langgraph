"""Week 2, Day 1 - reducers.

Run me:  pytest week-02/day-1 -v
"""

from typing import get_type_hints

import pytest
from langchain_core.messages import AIMessage, HumanMessage


@pytest.fixture
def reducers(load):
    return load("reducers.py")


class TestKeepUnique:
    def test_merges_in_order(self, reducers):
        assert reducers.keep_unique(["a", "b"], ["b", "c"]) == ["a", "b", "c"]

    def test_does_not_change_the_old_list(self, reducers):
        old = ["a"]
        reducers.keep_unique(old, ["b"])
        assert old == ["a"]


class TestTheState:
    def test_every_key_has_the_right_reducer(self, reducers):
        hints = get_type_hints(reducers.Ticket, include_extras=True)
        assert hints["notes"].__metadata__[0].__name__ == "add"
        assert hints["attempts"].__metadata__[0].__name__ == "add"
        assert hints["tags"].__metadata__[0] is reducers.keep_unique
        from langgraph.graph import add_messages
        assert hints["messages"].__metadata__[0] is add_messages
        assert not hasattr(hints["status"], "__metadata__"), "status has no reducer: last write wins."


class TestInParallel:
    def test_every_write_is_kept(self, reducers):
        result = reducers.build_checks().invoke({"notes": [], "attempts": 0, "tags": []})
        assert sorted(result["notes"]) == ["customer checked", "history checked", "order checked"]
        assert result["attempts"] == 3
        assert sorted(result["tags"]) == ["has-order", "known-customer"]
        assert result["status"] == "ready"

    def test_the_graph_is_parallel(self, reducers):
        edges = {(edge.source, edge.target) for edge in reducers.build_checks().get_graph().edges}
        for name in ("order", "customer", "history"):
            assert ("__start__", name) in edges and (name, "decide") in edges

    def test_without_reducers_it_breaks(self, reducers):
        assert reducers.broken() == "InvalidUpdateError", (
            "Three nodes wrote 'notes' in the same step and nothing said how to "
            "combine them. LangGraph refuses rather than guess."
        )


class TestAddMessages:
    def test_a_message_with_the_same_id_is_replaced(self, reducers):
        graph_state = reducers.build_checks().invoke({
            "messages": [HumanMessage("hi", id="m1")], "notes": [], "attempts": 0, "tags": []})
        assert len(graph_state["messages"]) == 1
        from langgraph.graph import add_messages
        merged = add_messages([AIMessage("draft", id="r1")], [AIMessage("final", id="r1")])
        assert [m.content for m in merged] == ["final"], (
            "add_messages appends - unless the id matches, and then it replaces. "
            "That is how you edit a message already in the state."
        )
