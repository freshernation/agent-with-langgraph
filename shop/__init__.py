"""Helpdesk's world - customers, orders, tickets and refunds - given, complete.

    find_customer(email)            a customer dict, or None
    get_order(order_id)             an order dict, or None
    orders_for(customer_id)         that customer's orders, newest first
    refund(order_id, amount, reason) -> str
                                    records a refund and says so, or says why not
    refunds()                       every refund so far, oldest first
    CUSTOMERS, TICKETS              the starting data (shop/data.py)

Nothing real is charged. Refunds, and what they change, are written to the file
named by SHOP_FILE (shop.json in the current folder if it is not set). No file
means the starting data. Every test gets a fresh one.

Every function returns a plain string or plain dicts, so a tool can hand its
result straight to the model.
"""

import copy
import json
import os
from pathlib import Path

from shop.data import CUSTOMERS, ORDERS, TICKETS

__all__ = ["find_customer", "get_order", "orders_for", "refund", "refunds",
           "CUSTOMERS", "TICKETS"]


def _path() -> Path:
    return Path(os.environ.get("SHOP_FILE", "shop.json"))


def _load() -> dict:
    path = _path()
    if path.exists():
        return json.loads(path.read_text())
    return {"orders": copy.deepcopy(ORDERS), "refunds": []}


def _save(state: dict) -> None:
    _path().write_text(json.dumps(state, indent=2))


def find_customer(email: str) -> dict | None:
    for customer in CUSTOMERS.values():
        if customer["email"] == email.strip().lower():
            return dict(customer)
    return None


def get_order(order_id: str) -> dict | None:
    order = _load()["orders"].get(order_id.strip().upper())
    return copy.deepcopy(order) if order else None


def orders_for(customer_id: str) -> list[dict]:
    mine = [order for order in _load()["orders"].values() if order["customer"] == customer_id]
    return sorted(mine, key=lambda order: order["placed"], reverse=True)


def refund(order_id: str, amount: float, reason: str) -> str:
    state = _load()
    order = state["orders"].get(order_id.strip().upper())
    if order is None:
        return f"There is no order {order_id}."
    if order["status"] != "delivered":
        return f"Only delivered orders can be refunded; {order['id']} is {order['status']}."
    if amount <= 0:
        return "A refund must be more than zero."
    left = round(order["total"] - order["refunded"], 2)
    if amount > left:
        return f"{order['id']} can be refunded at most ${left:.2f}."
    order["refunded"] = round(order["refunded"] + amount, 2)
    state["refunds"].append({"order": order["id"], "amount": round(amount, 2), "reason": reason})
    _save(state)
    return f"Refunded ${amount:.2f} on {order['id']}."


def refunds() -> list[dict]:
    return _load()["refunds"]
