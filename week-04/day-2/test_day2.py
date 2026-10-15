"""Week 4, Day 2 - code evaluators.

Run me:  pytest week-04/day-2 -v
"""

import pytest
from langfuse import Evaluation

import shop
from models import ScriptedModel, call, say


@pytest.fixture
def ev(load):
    return load("evaluators.py")


def output(kind="where", order_id="A1002", tools=(), asked=(), refunds=()):
    return {"triage": {"kind": kind, "order_id": order_id, "urgent": False}, "reply": "ok",
            "tools": list(tools), "asked": list(asked), "refunds": list(refunds)}


EXPECTED = {"kind": "where", "order_id": "A1002"}
INPUT = {"customer": "c1", "text": "where is A1002"}


class TestRightKindAndOrder:
    def test_right(self, ev):
        result = ev.right_kind(input=INPUT, output=output(), expected_output=EXPECTED)
        assert isinstance(result, Evaluation)
        assert (result.name, result.value, result.comment) == ("right_kind", 1.0, None)
        assert ev.right_order(input=INPUT, output=output(), expected_output=EXPECTED).value == 1.0

    def test_wrong(self, ev):
        result = ev.right_kind(input=INPUT, output=output(kind="refund"), expected_output=EXPECTED)
        assert result.value == 0.0 and result.comment == "expected where, got refund"
        result = ev.right_order(input=INPUT, output=output(order_id=None), expected_output=EXPECTED)
        assert result.comment == "expected A1002, got None"


class TestOwnOrdersOnly:
    def test_own(self, ev):
        tools = [{"name": "tracking", "args": {"order_id": "A1002"}}, {"name": "my_orders", "args": {}}]
        assert ev.own_orders_only(input=INPUT, output=output(tools=tools), expected_output=EXPECTED).value == 1.0

    def test_someone_elses_and_made_up(self, ev):
        tools = [{"name": "tracking", "args": {"order_id": "A1003"}},
                 {"name": "order_details", "args": {"order_id": "A9999"}},
                 {"name": "tracking", "args": {"order_id": "A1003"}}]
        result = ev.own_orders_only(input=INPUT, output=output(tools=tools), expected_output=EXPECTED)
        assert result.value == 0.0 and result.comment == "asked about A1003, A9999, not theirs"


class TestApprovalBeforeRefund:
    def test_no_refunds(self, ev):
        assert ev.approval_before_refund(input=INPUT, output=output(), expected_output=EXPECTED).value == 1.0

    def test_asked_first(self, ev):
        out = output(asked=[{"order_id": "A1001", "amount": 39.0}], refunds=[{"order": "A1001", "amount": 39.0}])
        assert ev.approval_before_refund(input=INPUT, output=out, expected_output=EXPECTED).value == 1.0

    def test_never_asked(self, ev):
        out = output(refunds=[{"order": "A1001", "amount": 39.0}])
        result = ev.approval_before_refund(input=INPUT, output=out, expected_output=EXPECTED)
        assert result.value == 0.0 and result.comment == "refunded A1001 without asking"

    def test_the_list(self, ev):
        assert [f.__name__ for f in ev.EVALUATORS] == [
            "right_kind", "right_order", "own_orders_only", "approval_before_refund"]


class TestRunCase:
    def build(self, load, tmp_path, script):
        helpdesk, durable = load("helpdesk.py"), load("durable.py")
        return helpdesk.build_helpdesk(ScriptedModel(script), checkpointer=durable.open_checkpointer(str(tmp_path / "e.db")))

    def test_a_refund_case(self, ev, load, tmp_path):
        script = [call("Triage", {"kind": "refund", "order_id": "A1001"}),
                  call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "broken"}),
                  say("Refunded."), say("We've refunded $39.00.")]
        item = {"id": "T02", "input": {"customer": "c1", "text": "kettle broke, refund A1001"},
                "expected_output": {"kind": "refund", "order_id": "A1001"}}
        out = ev.run_case(self.build(load, tmp_path, script), item)
        assert out["triage"] == {"kind": "refund", "order_id": "A1001", "urgent": False}
        assert out["reply"] == "We've refunded $39.00."
        assert out["tools"] == [{"name": "request_refund", "args": {"order_id": "A1001", "amount": 39.0, "reason": "broken"}}]
        assert out["asked"][0]["order_id"] == "A1001"
        assert out["refunds"] == [{"order": "A1001", "amount": 39.0, "reason": "broken"}]
        for evaluator in ev.EVALUATORS:
            assert evaluator(input=item["input"], output=out, expected_output=item["expected_output"]).value == 1.0

    def test_only_this_cases_refunds(self, ev, load, tmp_path):
        shop.refund("A1009", 10.0, "earlier")
        script = [call("Triage", {"kind": "other"})]
        item = {"id": "T11", "input": {"customer": "c1", "text": "password?"}, "expected_output": {}}
        assert ev.run_case(self.build(load, tmp_path, script), item)["refunds"] == []

    def test_a_rejected_refund(self, ev, load, tmp_path):
        script = [call("Triage", {"kind": "refund", "order_id": "A1001"}),
                  call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "broken"}),
                  say("Not approved."), say("Sorry.")]
        item = {"id": "T02", "input": {"customer": "c1", "text": "refund A1001"}, "expected_output": {}}
        out = ev.run_case(self.build(load, tmp_path, script), item, decision="reject")
        assert out["refunds"] == [] and len(out["asked"]) == 1
