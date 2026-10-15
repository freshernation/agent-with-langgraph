"""Week 3 milestone - Project 1: Helpdesk survives a restart, asks before a
refund, and can be rewound.

Run me:  pytest week-03/milestone -v
"""

import pytest

import shop
from models import ScriptedModel, call, say


def form(**fields):
    return call("Triage", fields)


ASK = call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "stopped working"})
REFUND_START = [form(kind="refund", order_id="A1001"), ASK]


@pytest.fixture
def parts(load):
    return load("helpdesk.py"), load("durable.py")


def build(parts, path, script):
    helpdesk, durable = parts
    return helpdesk.build_helpdesk(ScriptedModel(script), checkpointer=durable.open_checkpointer(path))


class TestARefund:
    def test_stops_and_waits(self, parts, load, tmp_path):
        helpdesk, durable = parts
        graph = build(parts, str(tmp_path / "c.db"), REFUND_START)
        config = durable.config_for("c1", "T02")
        assert helpdesk.answer(graph, "c1", "Kettle broke, refund A1001", config) is None
        assert load("refunds.py").pending(graph, config)[0]["order_id"] == "A1001"
        assert shop.refunds() == []

    def test_approved(self, parts, tmp_path):
        helpdesk, durable = parts
        graph = build(parts, str(tmp_path / "c.db"), REFUND_START + [say("Refunded $39."), say("We've refunded $39.00.")])
        config = durable.config_for("c1", "T02")
        helpdesk.answer(graph, "c1", "Kettle broke, refund A1001", config)
        assert helpdesk.decide(graph, config, "approve") == "We've refunded $39.00."
        assert shop.refunds()[0]["amount"] == 39.0

    def test_rejected(self, parts, tmp_path):
        helpdesk, durable = parts
        graph = build(parts, str(tmp_path / "c.db"), REFUND_START + [say("Not approved."), say("Sorry - not this time.")])
        config = durable.config_for("c1", "T02")
        helpdesk.answer(graph, "c1", "Kettle broke, refund A1001", config)
        helpdesk.decide(graph, config, "reject", note="Out of warranty.")
        assert shop.refunds() == []

    def test_the_draft_is_told_what_happened(self, parts, tmp_path):
        helpdesk, durable = parts
        model = ScriptedModel(REFUND_START + [say("Refunded $20."), say("ok")])
        helpdesk_graph = helpdesk.build_helpdesk(model, checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")))
        config = durable.config_for("c1", "T02")
        helpdesk.answer(helpdesk_graph, "c1", "refund A1001", config)
        helpdesk.decide(helpdesk_graph, config, "edit", amount=20.0)
        assert shop.refunds()[0]["amount"] == 20.0
        assert model.last_request["messages"][0].content == helpdesk.DRAFT
        assert len(helpdesk.DRAFT.split()) >= 40


class TestARestart:
    def test_while_waiting_for_a_person(self, parts, tmp_path):
        helpdesk, durable = parts
        path = str(tmp_path / "c.db")
        config = durable.config_for("c1", "T02")
        helpdesk.answer(build(parts, path, REFUND_START), "c1", "refund A1001", config)
        later = build(parts, path, [say("Refunded."), say("Done - $39.00 back to you.")])
        assert helpdesk.decide(later, config, "approve") == "Done - $39.00 back to you."
        assert len(shop.refunds()) == 1

    def test_in_the_middle_of_a_lookup(self, parts, tmp_path):
        helpdesk, durable = parts
        path = str(tmp_path / "c.db")
        config = durable.config_for("c1", "T01")
        crashing = build(parts, path, [form(kind="where", order_id="A1002"), RuntimeError("killed")])
        with pytest.raises(RuntimeError):
            helpdesk.answer(crashing, "c1", "Where is A1002?", config)
        later = build(parts, path, [say("Shipped."), say("On its way.")])
        assert durable.resume(later, config) == "On its way."


class TestRewind:
    def test_fix_a_wrong_triage(self, parts, load, tmp_path):
        helpdesk, durable = parts
        graph = build(parts, str(tmp_path / "c.db"),
                      [form(kind="other"), say("Shipped."), say("On its way.")])
        config = durable.config_for("c1", "T01")
        assert helpdesk.answer(graph, "c1", "Where is A1002?", config) == helpdesk.HANDOFF
        right = load("classify.py").Triage(kind="where", order_id="A1002")
        assert load("timetravel.py").fix_triage(graph, config, right) == "On its way."


class TestTheWriteUp:
    def test_written(self, source):
        text = source("APPROVAL.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("What a person sees", "What happens on yes, no and edit", "What runs twice",
                        "What happens on a restart"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
