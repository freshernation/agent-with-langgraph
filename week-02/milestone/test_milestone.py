"""Week 2 milestone - Helpdesk, version one.

Run me:  pytest week-02/milestone -v
"""

import pytest

import shop
from models import ScriptedModel, call, say

TICKETS = [
    {"id": "X1", "kind": "where", "order": "A1002", "text": "where is A1002"},
    {"id": "X2", "kind": "refund", "order": "A1001", "text": "refund A1001"},
    {"id": "X3", "kind": "other", "order": None, "text": "password?"},
]


def form(**fields):
    return call("Triage", fields)


@pytest.fixture
def report(load):
    return load("triage_report.py")


class TestTheReport:
    def test_all_right(self, report):
        model = ScriptedModel([form(kind="where", order_id="A1002"), form(kind="refund", order_id="A1001"),
                               form(kind="other")])
        assert report.triage_report(model, TICKETS) == {
            "total": 3, "right": 3, "accuracy": 1.0, "wrong_kind": [], "wrong_order": []}

    def test_wrong_kind_and_wrong_order(self, report):
        model = ScriptedModel([form(kind="change", order_id="A1002"), form(kind="refund", order_id="A1005"),
                               form(kind="other")])
        result = report.triage_report(model, TICKETS)
        assert result["right"] == 1 and result["accuracy"] == 0.33
        assert result["wrong_kind"] == ["X1"] and result["wrong_order"] == ["X2"]

    def test_a_guessed_order_is_wrong(self, report):
        model = ScriptedModel([form(kind="other", order_id="A1001")])
        assert report.triage_report(model, [TICKETS[2]])["wrong_order"] == ["X3"], (
            "The ticket names no order and the model filled one in. That is a guess."
        )

    def test_nothing(self, report):
        assert report.triage_report(ScriptedModel(), [])["accuracy"] == 0.0


class TestHelpdesk:
    def test_end_to_end(self, load):
        helpdesk = load("helpdesk.py")
        model = ScriptedModel([form(kind="where", order_id="A1008"), call("tracking", {"order_id": "A1008"}),
                               say("Shipped, TRK-5560."), say("Your bottles are on the way (TRK-5560).")])
        assert helpdesk.answer(helpdesk.build_helpdesk(model), "c4", shop.TICKETS[13]["text"]) == (
            "Your bottles are on the way (TRK-5560).")


class TestTheWriteUp:
    def test_written(self, source):
        text = source("GRAPH.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("Why these nodes", "Why this state", "What I kept out of the state",
                        "What the triage report says"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
