"""Week 2, Day 3 - tools over the shop, and tools that read the state.

Run me:  pytest week-02/day-3 -v
"""

import pytest
from langchain_core.messages import HumanMessage

import shop
from models import ScriptedModel, call, say


@pytest.fixture
def tools(load):
    return load("tools.py")


def run(tools, model, customer="c1", text="help"):
    return tools.build_lookup(model).invoke({"messages": [HumanMessage(text)], "customer": customer})


class TestDescribe:
    def test_one_line(self, tools):
        assert tools.describe(shop.get_order("A1002")) == "A1002 placed 2026-09-28: shipped, $34.00"


class TestTheSchemas:
    def test_the_model_cannot_choose_the_customer(self, tools):
        model = ScriptedModel(say("ok"))
        run(tools, model)
        for schema in model.last_request["tools"]:
            assert "state" not in schema["function"]["parameters"].get("properties", {}), (
                f"{schema['function']['name']} shows the state to the model. Then the model "
                "- or a ticket that talks it round - can pick whose orders to read."
            )

    def test_names(self, tools):
        assert [each.name for each in tools.TOOLS] == ["my_orders", "order_details", "tracking"]


class TestThroughTheGraph:
    def test_my_orders(self, tools):
        result = run(tools, ScriptedModel([call("my_orders"), say("You have two orders.")]))
        assert result["messages"][-2].content == (
            "A1002 placed 2026-09-28: shipped, $34.00\nA1001 placed 2026-09-02: delivered, $39.00")
        assert result["messages"][-1].content == "You have two orders."

    def test_details(self, tools):
        result = run(tools, ScriptedModel([call("order_details", {"order_id": "A1001"}), say("ok")]))
        assert result["messages"][-2].content == (
            "A1001 placed 2026-09-02: delivered, $39.00. Items: 1 x Kettle at $39.00. "
            "Refunded so far: $0.00.")

    def test_tracking(self, tools):
        result = run(tools, ScriptedModel([call("tracking", {"order_id": "A1002"}), say("ok")]))
        assert result["messages"][-2].content == "A1002 is shipped, tracking number TRK-5544."

    def test_not_sent_yet(self, tools):
        result = run(tools, ScriptedModel([call("tracking", {"order_id": "A1004"}), say("ok")]), customer="c2")
        assert result["messages"][-2].content == "A1004 is processing and has not been sent yet."

    @pytest.mark.parametrize("tool", ["order_details", "tracking"])
    def test_someone_elses_order(self, tools, tool):
        result = run(tools, ScriptedModel([call(tool, {"order_id": "A1003"}), say("ok")]), customer="c1")
        assert result["messages"][-2].content == "A1003 is not one of this customer's orders."

    def test_an_order_that_does_not_exist_reads_the_same(self, tools):
        result = run(tools, ScriptedModel([call("tracking", {"order_id": "A9999"}), say("ok")]))
        assert result["messages"][-2].content == "A9999 is not one of this customer's orders."

    def test_no_orders(self, tools):
        result = run(tools, ScriptedModel([call("my_orders"), say("ok")]), customer="c9")
        assert result["messages"][-2].content == "This customer has no orders."
