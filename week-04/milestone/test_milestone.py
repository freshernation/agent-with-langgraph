"""Week 4 milestone - an eval suite that fails a bad prompt change.

Run me:  pytest week-04/milestone -v

The model here obeys the classifier prompt's one rule that matters: with "never
guess" in it, it copies the order id from the ticket; without, it guesses the
customer's most recent order. So the gate can be tested with no key.
"""

import re

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

import shop


class PromptSensitive(BaseChatModel):
    @property
    def _llm_type(self):
        return "prompt-sensitive"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        system, text = messages[0].content, messages[1].content
        ticket = next(t for t in shop.TICKETS if t["text"] == text)
        found = re.search(r"A\d{4}", text)
        if found:
            order = found.group(0)
        elif "never guess" in system.lower():
            order = None
        else:
            order = shop.orders_for(ticket["customer"])[0]["id"]
        call = {"name": "Triage", "args": {"kind": ticket["kind"], "order_id": order}, "id": "c", "type": "tool_call"}
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="", tool_calls=[call]))])


GOOD = "Sort tickets. Never guess an order id."
BAD = "Sort tickets. If none is given, use the most recent order."


@pytest.fixture
def evals(load):
    return load("evals.py")


class TestTheDataset:
    def test_every_ticket(self, evals):
        assert len(evals.DATASET) == 20 and evals.DATASET[0]["id"] == "T01"


class TestTheGate:
    def test_the_same_prompt_passes(self, evals):
        result = evals.compare(PromptSensitive(), evals.DATASET, GOOD, GOOD)
        assert result["regressions"] == [] and result["newly_failing"] == []
        assert result["baseline"] == {"right_kind": 1.0, "right_order": 1.0}

    def test_a_bad_prompt_fails(self, evals):
        result = evals.compare(PromptSensitive(), evals.DATASET, GOOD, BAD)
        assert result["regressions"] == ["right_order: 1.00 -> 0.60"]
        assert "T05 right_order: expected None, got A1006" in result["newly_failing"]

    def test_a_tolerance_lets_it_through(self, evals):
        assert evals.compare(PromptSensitive(), evals.DATASET, GOOD, BAD, tolerance=0.5)["regressions"] == []


class TestNewlyFailing:
    def test_only_what_went_down(self, evals):
        base = {"per_item": [{"id": "a", "scores": {"k": 1.0}, "comments": {}},
                             {"id": "b", "scores": {"k": 0.0}, "comments": {"k": "x"}}]}
        cand = {"per_item": [{"id": "a", "scores": {"k": 0.0}, "comments": {}},
                             {"id": "b", "scores": {"k": 1.0}, "comments": {}}]}
        assert evals.newly_failing(base, cand) == ["a k"]


class TestTheWriteUp:
    def test_written(self, source):
        text = source("EVALS.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("What the suite checks", "What it misses", "The judge, and whether I trust it",
                        "The bad change it caught"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
