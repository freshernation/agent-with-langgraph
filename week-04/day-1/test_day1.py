"""Week 4, Day 1 - an eval set.

Run me:  pytest week-04/day-1 -v
"""

import pytest

import shop


@pytest.fixture
def dataset(load):
    return load("dataset.py")


class TestItems:
    def test_from_ticket(self, dataset):
        assert dataset.from_ticket(shop.TICKETS[0]) == {
            "id": "T01", "input": {"customer": "c1", "text": shop.TICKETS[0]["text"]},
            "expected_output": {"kind": "where", "order_id": "A1002"}, "metadata": {"source": "labelled"}}

    def test_from_trace(self, dataset):
        trace = {"id": "tr-9", "input": {"customer": "c4", "ticket": "zip broke, A1007"}}
        assert dataset.from_trace(trace, "refund", "A1007") == {
            "id": "tr-9", "input": {"customer": "c4", "text": "zip broke, A1007"},
            "expected_output": {"kind": "refund", "order_id": "A1007"},
            "metadata": {"source": "trace", "source_trace_id": "tr-9"}}


class TestSplit:
    def test_always_the_same_side(self, dataset):
        assert dataset.in_test("T01", 0.3) == dataset.in_test("T01", 0.3)

    def test_roughly_the_share(self, dataset):
        items = [{"id": f"x{n}"} for n in range(1000)]
        dev, test = dataset.split(items, 0.3)
        assert len(dev) + len(test) == 1000
        assert 250 < len(test) < 350

    def test_order_kept(self, dataset):
        items = [dataset.from_ticket(t) for t in shop.TICKETS]
        dev, test = dataset.split(items)
        assert [i["id"] for i in dev] == [i["id"] for i in items if i in dev]

    def test_nothing_in_test(self, dataset):
        assert dataset.split([{"id": "a"}], 0.0) == ([{"id": "a"}], [])


def item(id, kind):
    return {"id": id, "input": {}, "expected_output": {"kind": kind, "order_id": None}, "metadata": {}}


class TestProblems:
    def test_the_labelled_tickets(self, dataset):
        assert dataset.problems([dataset.from_ticket(t) for t in shop.TICKETS]) == []

    def test_repeats_unknowns_and_thin_kinds(self, dataset):
        items = [item("a", "refund"), item("a", "refund"), item("b", "banana")] + \
                [item(f"w{n}", "where") for n in range(3)] + [item(f"o{n}", "other") for n in range(3)]
        assert dataset.problems(items) == [
            "a appears twice", "b has an unknown kind: banana",
            "only 2 examples of refund", "only 0 examples of change"]
