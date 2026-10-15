"""Week 5, Day 4 - cost and latency, and an incident.

Run me:  pytest week-05/day-4 -v
"""

import pytest


@pytest.fixture
def costs(load):
    return load("costs.py")


def trace(id, session, latency, cost):
    return {"id": id, "timestamp": "2026-10-15T09:00:00", "session_id": session,
            "latency": latency, "total_cost": cost}


TRACES = [trace("a", "c1/T1", 2.0, 0.010), trace("b", "c1/T1", 9.0, 0.030),
          trace("c", "c2/T3", 3.0, 0.005), trace("d", None, 1.0, None)]


class TestPercentile:
    def test_nearest_rank(self, costs):
        assert costs.percentile([1, 2, 3, 4], 50) == 2
        assert costs.percentile([4, 3, 2, 1], 95) == 4
        assert costs.percentile([], 50) == 0.0


class TestSummarise:
    def test_numbers(self, costs):
        assert costs.summarise(TRACES) == {
            "traces": 4, "tickets": 3, "p50_seconds": 2.0, "p95_seconds": 9.0,
            "cost_per_trace": 0.01125, "cost_per_ticket": 0.015, "costliest_ticket": "c1/T1"}

    def test_nothing(self, costs):
        assert costs.summarise([])["costliest_ticket"] is None


class TestSlowest:
    def test_order(self, costs):
        assert costs.slowest(TRACES, 2) == ["b", "c"]

    def test_ties_by_id(self, costs):
        assert costs.slowest([trace("z", None, 1.0, 0), trace("y", None, 1.0, 0)], 2) == ["y", "z"]


class TestTheIncident:
    def test_written(self, source):
        text = source("INCIDENT.md")
        assert "<!--" not in text, "Delete the instructions comment."
        assert "<one line" not in text, "Give the incident a title."
        for heading in ("What customers saw", "Timeline", "Why it happened", "How I found out", "What I changed"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
