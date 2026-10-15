"""Week 3, Day 4 - sessions and users.

Run me:  pytest week-03/day-4 -v
"""

import pytest
from langchain_core.callbacks import BaseCallbackHandler

from models import ScriptedModel, call, say


class Recording(BaseCallbackHandler):
    def __init__(self):
        self.metadata = []

    def on_chat_model_start(self, serialized, messages, **kwargs):
        self.metadata.append(kwargs.get("metadata") or {})


@pytest.fixture
def sessions(load):
    return load("sessions.py")


class TestRunConfig:
    def test_one_config_three_jobs(self, sessions):
        handler = Recording()
        assert sessions.run_config("c1", "T01", [handler]) == {
            "configurable": {"thread_id": "c1/T01"}, "callbacks": [handler],
            "metadata": {"langfuse_user_id": "c1", "langfuse_session_id": "c1/T01"}}

    def test_every_model_call_is_stamped(self, sessions, load, tmp_path):
        helpdesk, durable = load("helpdesk.py"), load("durable.py")
        handler = Recording()
        model = ScriptedModel([call("Triage", {"kind": "where", "order_id": "A1002"}), say("Shipped."), say("On its way.")])
        graph = helpdesk.build_helpdesk(model, checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")))
        helpdesk.answer(graph, "c1", "Where is A1002?", sessions.run_config("c1", "T01", [handler]))
        assert len(handler.metadata) == 3
        assert all(m.get("langfuse_session_id") == "c1/T01" for m in handler.metadata)
        assert graph.get_state(durable.config_for("c1", "T01")).next == (), (
            "The same config must also reach the checkpointer's thread."
        )


def trace(id, session, when, cost):
    return {"id": id, "timestamp": when, "session_id": session, "total_cost": cost, "latency": 1.0}


class TestCustomerStory:
    def test_grouped_by_session_in_order(self, sessions):
        traces = [trace("3", "c1/T02", "2026-10-02T09:00", 0.01),
                  trace("1", "c1/T01", "2026-10-01T09:00", 0.02),
                  trace("2", "c1/T01", "2026-10-01T09:05", 0.03)]
        assert sessions.customer_story(traces) == [
            {"session": "c1/T01", "traces": 2, "cost": 0.05, "first": "2026-10-01T09:00", "last": "2026-10-01T09:05"},
            {"session": "c1/T02", "traces": 1, "cost": 0.01, "first": "2026-10-02T09:00", "last": "2026-10-02T09:00"}]

    def test_missing_session_and_cost(self, sessions):
        story = sessions.customer_story([trace("1", None, "2026-10-01T09:00", None)])
        assert story == [{"session": "(no session)", "traces": 1, "cost": 0.0,
                          "first": "2026-10-01T09:00", "last": "2026-10-01T09:00"}]


class TestTheWriteUp:
    def test_written(self, source):
        text = source("ONE_CUSTOMER.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("What I could find", "What it cost", "What I could not find"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 30, f"'{heading}' is {len(part.split())} words."
