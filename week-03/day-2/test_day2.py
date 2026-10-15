"""Week 3, Day 2 - interrupt and resume.

Run me:  pytest week-03/day-2 -v
"""

import pytest
from langchain_core.messages import HumanMessage

import shop
from models import ScriptedModel, call, say


@pytest.fixture
def refunds(load):
    return load("refunds.py")


@pytest.fixture
def durable(load):
    return load("durable.py")


ASK = call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "stopped working"})


def start(refunds, durable, path, script, customer="c1"):
    graph = refunds.build_refund_desk(ScriptedModel(script), durable.open_checkpointer(path))
    config = durable.config_for(customer, "T02")
    result = graph.invoke({"messages": [HumanMessage("My kettle broke, refund A1001")],
                           "customer": customer}, config)
    return graph, config, result


class TestTheTool:
    def test_hides_the_state(self, refunds):
        assert set(refunds.request_refund.tool_call_schema.model_json_schema()["properties"]) == {
            "order_id", "amount", "reason"}
        assert "approve" in refunds.request_refund.description

    def test_someone_elses_order_never_reaches_a_person(self, refunds, durable, tmp_path):
        script = [call("request_refund", {"order_id": "A1003", "amount": 5.0, "reason": "x"}), say("Sorry.")]
        graph, config, _ = start(refunds, durable, str(tmp_path / "c.db"), script)
        assert refunds.pending(graph, config) == []
        assert graph.get_state(config).values["messages"][-2].content == "A1003 is not one of this customer's orders."

    def test_an_undelivered_order_never_reaches_a_person(self, refunds, durable, tmp_path):
        script = [call("request_refund", {"order_id": "A1002", "amount": 5.0, "reason": "x"}), say("Sorry.")]
        graph, config, _ = start(refunds, durable, str(tmp_path / "c.db"), script)
        assert refunds.pending(graph, config) == []


class TestItStops:
    def test_waits_for_a_person(self, refunds, durable, tmp_path):
        graph, config, result = start(refunds, durable, str(tmp_path / "c.db"), [ASK])
        assert refunds.pending(graph, config) == [
            {"customer": "c1", "order_id": "A1001", "amount": 39.0, "reason": "stopped working"}]
        assert durable.where_it_stopped(graph, config) == ("tools",)
        assert shop.refunds() == [], "Nothing may be refunded before a person says yes."


class TestTheDecision:
    def test_approve(self, refunds, durable, tmp_path):
        graph, config, _ = start(refunds, durable, str(tmp_path / "c.db"), [ASK, say("Done - refunded.")])
        assert refunds.decide(graph, config, "approve") == "Done - refunded."
        assert shop.refunds() == [{"order": "A1001", "amount": 39.0, "reason": "stopped working"}]

    def test_reject(self, refunds, durable, tmp_path):
        graph, config, _ = start(refunds, durable, str(tmp_path / "c.db"), [ASK, say("Sorry, no.")])
        refunds.decide(graph, config, "reject", note="Out of warranty.")
        assert shop.refunds() == []
        tool_result = graph.get_state(config).values["messages"][-2].content
        assert tool_result == "A person did not approve this refund. Out of warranty."

    def test_edit(self, refunds, durable, tmp_path):
        graph, config, _ = start(refunds, durable, str(tmp_path / "c.db"), [ASK, say("Part refunded.")])
        refunds.decide(graph, config, "edit", amount=20.0)
        assert shop.refunds()[0]["amount"] == 20.0

    def test_the_person_can_decide_after_a_restart(self, refunds, durable, tmp_path):
        path = str(tmp_path / "c.db")
        _, config, _ = start(refunds, durable, path, [ASK])
        later = refunds.build_refund_desk(ScriptedModel([say("Refunded.")]), durable.open_checkpointer(path))
        assert refunds.decide(later, config, "approve") == "Refunded."
        assert len(shop.refunds()) == 1, "Approved once, refunded once - even though the tool ran twice."
