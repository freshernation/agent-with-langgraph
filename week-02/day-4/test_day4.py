"""Week 2, Day 4 - routing, retries and a fallback.

Run me:  pytest week-02/day-4 -v
"""

import pytest

import shop
from models import ScriptedModel, call, say


@pytest.fixture
def helpdesk(load):
    return load("helpdesk.py")


def form(**fields):
    return call("Triage", fields)


def where_script():
    return [form(kind="where", order_id="A1002"),
            call("tracking", {"order_id": "A1002"}),
            say("A1002 has shipped, tracking TRK-5544."),
            say("Your mugs are on their way - the tracking number is TRK-5544.")]


class TestTheShape:
    def test_nodes(self, helpdesk):
        nodes = set(helpdesk.build_helpdesk(ScriptedModel()).get_graph().nodes)
        assert nodes == {"__start__", "classify", "lookup", "tools", "draft", "handoff", "__end__"}


class TestTheRoutes:
    def test_where(self, helpdesk):
        model = ScriptedModel(where_script())
        reply = helpdesk.answer(helpdesk.build_helpdesk(model), "c1", "Where are my mugs, A1002?")
        assert reply == "Your mugs are on their way - the tracking number is TRK-5544."
        assert model.call_count == 4

    def test_other_goes_to_a_person(self, helpdesk):
        model = ScriptedModel([form(kind="other")])
        reply = helpdesk.answer(helpdesk.build_helpdesk(model), "c1", "How do I reset my password?")
        assert reply == helpdesk.HANDOFF
        assert model.call_count == 1, "A ticket for a person should not cost three model calls."

    def test_a_refund_is_only_drafted(self, helpdesk):
        model = ScriptedModel([form(kind="refund", order_id="A1001"),
                               call("order_details", {"order_id": "A1001"}), say("Kettle, $39."),
                               say("A person will review your refund within one working day.")])
        helpdesk.answer(helpdesk.build_helpdesk(model), "c1", "Kettle broke, refund A1001")
        assert shop.refunds() == []


class TestWhatEachNodeIsGiven:
    def test_lookup_is_told_the_triage(self, helpdesk):
        model = ScriptedModel(where_script())
        helpdesk.answer(helpdesk.build_helpdesk(model), "c1", "Where are my mugs, A1002?")
        system = model.requests[1]["messages"][0].content
        assert system.endswith("This ticket is about: where, order A1002.")

    def test_draft_is_given_the_facts(self, helpdesk):
        model = ScriptedModel(where_script())
        helpdesk.answer(helpdesk.build_helpdesk(model), "c1", "Where are my mugs, A1002?")
        sent = model.last_request["messages"]
        assert sent[0].content == helpdesk.DRAFT
        assert sent[1].content == ("Ticket: Where are my mugs, A1002?\nKind: where\n"
                                   "What we found: A1002 has shipped, tracking TRK-5544.")
        assert len(helpdesk.DRAFT.split()) >= 40


class TestWhenTheModelFails:
    def test_a_dropped_connection_is_retried(self, helpdesk):
        script = where_script()
        script.insert(1, ConnectionError("blip"))
        model = ScriptedModel(script)
        reply = helpdesk.answer(helpdesk.build_helpdesk(model), "c1", "Where are my mugs, A1002?")
        assert reply.startswith("Your mugs")

    def test_the_backup_answers(self, helpdesk):
        primary = ScriptedModel([form(kind="where", order_id="A1002"), RuntimeError("down"), RuntimeError("down")])
        backup = ScriptedModel([say("A1002 has shipped."), say("From the backup: it's on its way.")])
        reply = helpdesk.answer(helpdesk.build_helpdesk(primary, backup), "c1", "Where is A1002?")
        assert reply == "From the backup: it's on its way."
        assert backup.call_count == 2
