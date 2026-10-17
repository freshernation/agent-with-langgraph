"""Week 6, Day 3 - episodes.

Run me:  pytest week-06/day-3 -v
"""

import pytest

from models import ScriptedModel, call, say


@pytest.fixture
def ep(load):
    return load("episodes.py")


@pytest.fixture
def store(load, tmp_path):
    return load("facts.py").open_store(str(tmp_path / "m.db"))


class TestSummarise:
    def test_a_record(self, ep):
        model = ScriptedModel([call("Episode", {"asked": "Refund on a kettle", "outcome": "Refunded $39.00",
                                                "order_id": "A1001"})])
        episode = ep.summarise(model, "Kettle broke, refund A1001", "We've refunded $39.00.")
        assert episode == ep.Episode(asked="Refund on a kettle", outcome="Refunded $39.00", order_id="A1001")
        sent = model.last_request["messages"]
        assert sent[0].content == ep.SUMMARY and len(ep.SUMMARY.split()) >= 30
        assert sent[1].content == "Ticket: Kettle broke, refund A1001\nReply: We've refunded $39.00."

    def test_gives_up(self, ep):
        assert ep.summarise(ScriptedModel([say("?"), say("?")]), "t", "r") is None


class TestWords:
    def test_words(self, ep):
        assert ep.words("Refund my kettle, A1001!") == {"refund", "kettle", "a1001"}
        assert "the" not in ep.words("the kettle and the mug") and "asked" in ep.STOP


def record(ep, store, ticket, asked, outcome, when, order=None, customer="c1"):
    ep.record_episode(store, customer, ticket, ep.Episode(asked=asked, outcome=outcome, order_id=order), when)


class TestRecallByRelevance:
    def test_the_relevant_one_first(self, ep, store):
        record(ep, store, "T02", "Refund on a kettle", "Refunded $39.00", "2026-10-01", "A1001")
        record(ep, store, "T05", "Where are my mugs", "Shipped, TRK-5544", "2026-10-05", "A1002")
        record(ep, store, "T09", "Password reset", "Sent to a person", "2026-10-09")
        found = ep.relevant_episodes(store, "c1", "My new kettle is broken too")
        assert [e["ticket"] for e in found] == ["T02"]
        assert found[0] == {"ticket": "T02", "asked": "Refund on a kettle", "outcome": "Refunded $39.00",
                            "when": "2026-10-01"}

    def test_ties_go_to_the_newest(self, ep, store):
        record(ep, store, "T1", "kettle refund", "done", "2026-09-01")
        record(ep, store, "T2", "kettle question", "answered", "2026-10-01")
        assert [e["ticket"] for e in ep.relevant_episodes(store, "c1", "kettle")] == ["T2", "T1"]

    def test_more_overlap_wins(self, ep, store):
        record(ep, store, "T1", "kettle", "done", "2026-10-09")
        record(ep, store, "T2", "kettle refund A1001", "refunded", "2026-09-01", "A1001")
        assert ep.relevant_episodes(store, "c1", "refund for kettle A1001")[0]["ticket"] == "T2"

    def test_an_order_number_matches(self, ep, store):
        record(ep, store, "T5", "Where is it", "Shipped", "2026-10-05", "A1002")
        assert ep.relevant_episodes(store, "c1", "Any news on A1002?")[0]["ticket"] == "T5"

    def test_only_this_customer(self, ep, store):
        record(ep, store, "T1", "kettle refund", "done", "2026-10-01", customer="c2")
        assert ep.relevant_episodes(store, "c1", "kettle") == []

    def test_limit(self, ep, store):
        for n in range(5):
            record(ep, store, f"T{n}", "kettle", "done", f"2026-10-0{n + 1}")
        assert len(ep.relevant_episodes(store, "c1", "kettle", limit=2)) == 2


class TestForThePrompt:
    def test_lines(self, ep):
        text = ep.episodes_for_prompt([{"ticket": "T02", "asked": "Refund on a kettle",
                                        "outcome": "Refunded $39.00", "when": "2026-10-01"}])
        assert text == f"{ep.HEADER}\n- 2026-10-01 T02: Refund on a kettle; Refunded $39.00"

    def test_nothing(self, ep):
        assert ep.episodes_for_prompt([]) == ""
