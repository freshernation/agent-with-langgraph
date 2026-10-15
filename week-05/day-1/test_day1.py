"""Week 5, Day 1 - async and streaming.

Run me:  pytest week-05/day-1 -v
"""

import asyncio

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from models import ScriptedModel, call, say


def form(**fields):
    return call("Triage", fields)


WHERE = [form(kind="where", order_id="A1002"), call("tracking", {"order_id": "A1002"}),
         say("Shipped, TRK-5544."), say("Your mugs are on the way.")]
REFUND = [form(kind="refund", order_id="A1001"),
          call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "broken"}),
          say("Refunded."), say("We have refunded you.")]
CONFIG = {"configurable": {"thread_id": "c1/T1"}}
INPUT = {"customer": "c1", "ticket": "where is A1002"}


@pytest.fixture
def streaming(load):
    return load("streaming.py")


@pytest.fixture
def helpdesk(load):
    return load("helpdesk.py")


def graph(helpdesk, script):
    return helpdesk.build_helpdesk(ScriptedModel(script), checkpointer=InMemorySaver())


async def collect(agen):
    return [item async for item in agen]


class TestUpdates:
    def test_the_nodes_in_order(self, streaming, helpdesk):
        names = asyncio.run(streaming.updates(graph(helpdesk, WHERE), INPUT, CONFIG))
        assert names == ["classify", "lookup", "tools", "lookup", "draft"]

    def test_an_interrupt_shows(self, streaming, helpdesk):
        names = asyncio.run(streaming.updates(graph(helpdesk, REFUND), INPUT, CONFIG))
        assert names[-1] == "__interrupt__"


class TestTokens:
    def test_only_the_reply(self, streaming, helpdesk):
        pieces = asyncio.run(streaming.tokens(graph(helpdesk, WHERE), INPUT, CONFIG))
        assert pieces == ["Your ", "mugs ", "are ", "on ", "the ", "way."], (
            "Only the draft node's words reach the customer - not the lookup's working."
        )


class TestEvents:
    def test_steps_tokens_done(self, streaming, helpdesk):
        events = asyncio.run(collect(streaming.events(graph(helpdesk, WHERE), INPUT, CONFIG)))
        assert events[0] == {"type": "step", "data": "classify"}
        assert [e["data"] for e in events if e["type"] == "token"] == ["Your ", "mugs ", "are ", "on ", "the ", "way."]
        assert events[-1] == {"type": "done", "data": "Your mugs are on the way."}
        tokens_at = [i for i, e in enumerate(events) if e["type"] == "token"]
        draft_step = events.index({"type": "step", "data": "draft"})
        assert max(tokens_at) < draft_step, "The words must arrive while the draft is being written, not after."

    def test_waiting_and_then_done(self, streaming, helpdesk):
        g = graph(helpdesk, REFUND)
        first = asyncio.run(collect(streaming.events(g, {"customer": "c1", "ticket": "refund A1001"}, CONFIG)))
        assert first[-1] == {"type": "waiting", "data": {"customer": "c1", "order_id": "A1001",
                                                           "amount": 39.0, "reason": "broken"}}
        assert all(e["type"] != "done" for e in first)
        second = asyncio.run(collect(streaming.events(g, Command(resume={"action": "approve"}), CONFIG)))
        assert second[-1] == {"type": "done", "data": "We have refunded you."}
