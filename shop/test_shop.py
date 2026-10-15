"""The shop works, offline, on a throwaway file."""

import pytest

import shop


@pytest.fixture(autouse=True)
def fresh(tmp_path, monkeypatch):
    monkeypatch.setenv("SHOP_FILE", str(tmp_path / "shop.json"))


def test_customers_and_orders():
    assert shop.find_customer(" Asha@Example.com")["id"] == "c1"
    assert shop.find_customer("nobody@example.com") is None
    assert shop.get_order("a1001")["total"] == 39.0
    assert [order["id"] for order in shop.orders_for("c1")] == ["A1002", "A1001"]


def test_a_refund_is_recorded():
    assert shop.refund("A1001", 39.0, "broken") == "Refunded $39.00 on A1001."
    assert shop.get_order("A1001")["refunded"] == 39.0
    assert shop.refunds() == [{"order": "A1001", "amount": 39.0, "reason": "broken"}]


def test_refund_rules():
    assert shop.refund("A9999", 1, "x") == "There is no order A9999."
    assert "processing" in shop.refund("A1004", 10, "x")
    assert shop.refund("A1001", 0, "x") == "A refund must be more than zero."
    shop.refund("A1001", 30, "x")
    assert shop.refund("A1001", 10, "x") == "A1001 can be refunded at most $9.00."


def test_the_starting_data_is_not_changed():
    shop.refund("A1001", 39.0, "broken")
    from shop.data import ORDERS
    assert ORDERS["A1001"]["refunded"] == 0.0


def test_every_ticket_is_labelled():
    kinds = {ticket["kind"] for ticket in shop.TICKETS}
    assert kinds == {"refund", "where", "change", "other"}
    for ticket in shop.TICKETS:
        assert ticket["order"] is None or shop.get_order(ticket["order"]) is not None
