"""Week 4, Day 3 - a judge, checked against people.

Run me:  pytest week-04/day-3 -v
"""

import pytest

from models import ScriptedModel, call, say


@pytest.fixture
def jd(load):
    return load("judge.py")


def verdict(good, reason="because"):
    return call("Verdict", {"good": good, "reason": reason})


class TestJudge:
    def test_a_verdict(self, jd):
        model = ScriptedModel([verdict(True, "Answers with the tracking number.")])
        result = jd.judge(model, "Where is A1002?", "On its way, TRK-5544.", "A1002 is shipped, TRK-5544.")
        assert result == jd.Verdict(good=True, reason="Answers with the tracking number.")
        sent = model.last_request["messages"]
        assert sent[0].content == jd.RUBRIC and len(jd.RUBRIC.split()) >= 50
        assert sent[1].content == "Ticket: Where is A1002?\nFacts: A1002 is shipped, TRK-5544.\nReply: On its way, TRK-5544."

    def test_retries_then_gives_up(self, jd):
        assert jd.judge(ScriptedModel([say("hm"), verdict(False)]), "t", "r", "f").good is False
        assert jd.judge(ScriptedModel([say("hm"), say("hm")]), "t", "r", "f") is None


class TestAgreement:
    def test_perfect(self, jd):
        report = jd.agreement([True, False, True, False], [True, False, True, False])
        assert report == {"items": 4, "judged": 4, "agree": 4, "agreement": 1.0,
                          "false_pass": 0, "false_fail": 0, "kappa": 1.0}

    def test_kappa_corrects_for_luck(self, jd):
        human = [True] * 9 + [False]
        report = jd.agreement([True] * 10, human)
        assert report["agreement"] == 0.9
        assert report["kappa"] == 0.0, (
            "A judge that says 'good' to everything agrees 90% of the time here, "
            "and knows nothing. Kappa says so."
        )
        assert report["false_pass"] == 1

    def test_a_worked_example(self, jd):
        judged = [True, True, False, False, True, None]
        human = [True, False, False, True, True, True]
        report = jd.agreement(judged, human)
        assert report["judged"] == 5 and report["agree"] == 3 and report["agreement"] == 0.6
        assert report["false_pass"] == 1 and report["false_fail"] == 1
        assert report["kappa"] == 0.17

    def test_nothing_judged(self, jd):
        assert jd.agreement([None], [True])["kappa"] == 0.0


class TestTrust:
    def test_trusted(self, jd):
        assert jd.trustworthy(jd.agreement([True, False, True, False], [True, False, True, False]))

    def test_a_false_pass_is_not_trusted(self, jd):
        report = jd.agreement([True, True, False, False, True, True, False, False, True, True],
                              [True, True, False, False, True, True, False, False, True, False])
        assert report["kappa"] >= 0.6 and not jd.trustworthy(report)

    def test_undecided_is_not_trusted(self, jd):
        assert not jd.trustworthy(jd.agreement([True, False, None], [True, False, True]))


class TestAsAnEvaluator:
    def test_judge_good(self, jd):
        model = ScriptedModel([verdict(False, "Promises a date it was not given.")])
        evaluate = jd.judge_evaluator(model)
        out = {"reply": "Tomorrow!", "tools": [{"name": "tracking", "args": {"order_id": "A1002"}}]}
        result = evaluate(input={"customer": "c1", "text": "where?"}, output=out, expected_output={})
        assert (result.name, result.value, result.comment) == ("judge_good", 0.0, "Promises a date it was not given.")
        assert "tracking" in model.last_request["messages"][1].content

    def test_undecided(self, jd):
        result = jd.judge_evaluator(ScriptedModel([say("?"), say("?")]))(
            input={"text": "t"}, output={"reply": "r", "tools": []}, expected_output={})
        assert result.value == 0.0 and result.comment == "the judge could not decide"
