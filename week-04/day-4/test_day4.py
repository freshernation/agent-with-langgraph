"""Week 4, Day 4 - experiments and a gate.

Run me:  pytest week-04/day-4 -v
"""

import pytest

import shop
from models import ScriptedModel, call


@pytest.fixture
def ex(load):
    return load("experiment.py")


@pytest.fixture
def ev(load):
    return load("evaluators.py")


@pytest.fixture
def items(load):
    dataset = load("dataset.py")
    return [dataset.from_ticket(t) for t in shop.TICKETS[:3]]


def triage(kind, order_id=None):
    return call("Triage", {"kind": kind, "order_id": order_id})


class TestClassifyTask:
    def test_uses_the_prompt_it_is_given(self, ex, items):
        model = ScriptedModel([triage("where", "A1002")])
        out = ex.classify_task(model, "A DIFFERENT PROMPT")(item=items[0])
        assert out == {"triage": {"kind": "where", "order_id": "A1002", "urgent": False}}
        assert model.last_request["messages"][0].content == "A DIFFERENT PROMPT"


class TestRunLocal:
    def test_scores_and_means(self, ex, ev, items):
        model = ScriptedModel([triage("where", "A1002"), triage("refund", "A1001"), triage("refund")])
        result = ex.run_local(items, ex.classify_task(model, "p"), [ev.right_kind, ev.right_order])
        assert [r["id"] for r in result["per_item"]] == ["T01", "T02", "T03"]
        assert result["per_item"][2]["scores"] == {"right_kind": 0.0, "right_order": 1.0}
        assert result["per_item"][2]["comments"] == {"right_kind": "expected change, got refund"}
        assert result["per_item"][0]["comments"] == {}
        assert result["means"] == {"right_kind": 0.667, "right_order": 1.0}


class TestGate:
    def test_passes(self, ex):
        assert ex.gate({"right_kind": 0.9}, {"right_kind": 0.95}) == []

    def test_a_regression(self, ex):
        assert ex.gate({"right_kind": 0.9, "right_order": 0.95}, {"right_kind": 0.9, "right_order": 0.8}) == [
            "right_order: 0.95 -> 0.80"]

    def test_tolerance(self, ex):
        assert ex.gate({"right_kind": 0.9}, {"right_kind": 0.88}, tolerance=0.05) == []

    def test_a_missing_score_is_a_regression(self, ex):
        assert ex.gate({"right_kind": 0.9, "judge_good": 0.8}, {"right_kind": 0.9}) == ["judge_good: missing"]


class FakePrompts:
    def __init__(self, text=None, fail=False):
        self.text, self.fail, self.asked = text, fail, []

    def get_prompt(self, name, label=None, fallback=None):
        self.asked.append((name, label, fallback))
        if self.fail:
            raise ConnectionError("unreachable")

        class Prompt:
            prompt = self.text if self.text is not None else fallback
        return Prompt()


class TestLoadPrompt:
    def test_from_langfuse(self, ex):
        client = FakePrompts("Prompt v7")
        assert ex.load_prompt(client, "helpdesk-classify", "local") == "Prompt v7"
        assert client.asked == [("helpdesk-classify", "production", "local")]

    def test_unreachable(self, ex):
        assert ex.load_prompt(FakePrompts(fail=True), "x", "local") == "local"

    def test_no_client(self, ex):
        assert ex.load_prompt(None, "x", "local") == "local"
