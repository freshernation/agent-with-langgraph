"""Week 2, Day 2 - structured output.

Run me:  pytest week-02/day-2 -v
"""

import pytest
from pydantic import ValidationError

from models import ScriptedModel, call, say


@pytest.fixture
def classify(load):
    return load("classify.py")


def form(**fields):
    return call("Triage", fields)


class TestTriage:
    def test_a_good_form(self, classify):
        assert classify.Triage(kind="refund", order_id="A1001").urgent is False

    def test_kind_is_one_of_four(self, classify):
        with pytest.raises(ValidationError):
            classify.Triage(kind="banana")

    def test_order_id_looks_like_an_order(self, classify):
        with pytest.raises(ValidationError):
            classify.Triage(kind="where", order_id="order 12")
        assert classify.Triage(kind="where").order_id is None


class TestClassify:
    def test_fills_the_form(self, classify):
        model = ScriptedModel([form(kind="where", order_id="A1002", urgent=False)])
        assert classify.classify(model, "Where is A1002?") == classify.Triage(kind="where", order_id="A1002")

    def test_sends_the_instructions_and_the_ticket(self, classify):
        model = ScriptedModel([form(kind="other")])
        classify.classify(model, "How do I reset my password?")
        sent = model.last_request["messages"]
        assert sent[0].content == classify.SYSTEM and sent[1].content == "How do I reset my password?"
        assert len(classify.SYSTEM.split()) >= 40
        assert model.last_request["tools"][0]["function"]["name"] == "Triage"

    def test_a_bad_form_is_tried_again(self, classify):
        model = ScriptedModel([form(kind="banana"), form(kind="refund", order_id="A1001")])
        assert classify.classify(model, "money back for A1001").kind == "refund"
        assert model.call_count == 2

    def test_words_instead_of_a_form_are_tried_again(self, classify):
        model = ScriptedModel([say("This looks like a refund."), form(kind="refund")])
        assert classify.classify(model, "money back").kind == "refund"

    def test_gives_up_to_a_person(self, classify):
        model = ScriptedModel([say("hmm"), form(kind="banana")])
        assert classify.classify(model, "???") == classify.FALLBACK
        assert classify.FALLBACK.kind == "other"

    def test_more_retries(self, classify):
        model = ScriptedModel([say("a"), say("b"), say("c"), form(kind="where")])
        assert classify.classify(model, "where", retries=3).kind == "where"
