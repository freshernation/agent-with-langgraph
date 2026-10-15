"""Week 5, Day 2 - a streaming server.

Run me:  pytest week-05/day-2 -v
"""

import json

import pytest
from fastapi.testclient import TestClient

import shop
from models import ScriptedModel, call, say


def form(**fields):
    return call("Triage", fields)


WHERE = [form(kind="where", order_id="A1002"), call("tracking", {"order_id": "A1002"}),
         say("Shipped, TRK-5544."), say("Your mugs are on the way.")]
REFUND = [form(kind="refund", order_id="A1001"),
          call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "broken"}),
          say("Refunded."), say("We have refunded you.")]


@pytest.fixture
def server(load):
    return load("server.py")


def client(server, tmp_path, script):
    return TestClient(server.create_app(ScriptedModel(script), str(tmp_path / "h.db")))


def parse(text):
    events = []
    for block in text.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


class TestSse:
    def test_one_event(self, server):
        assert server.sse("token", "hi\nthere") == 'event: token\ndata: "hi\\nthere"\n\n'


class TestMessages:
    def test_streams_a_ticket(self, server, tmp_path):
        with client(server, tmp_path, WHERE) as http:
            response = http.post("/tickets/T01/messages", json={"customer": "c1", "text": "where is A1002"})
            assert response.headers["content-type"].startswith("text/event-stream")
            events = parse(response.text)
            assert events[0] == ("step", "classify")
            assert "".join(data for kind, data in events if kind == "token") == "Your mugs are on the way."
            assert events[-1] == ("done", "Your mugs are on the way.")

    def test_rejects_an_empty_message(self, server, tmp_path):
        with client(server, tmp_path, []) as http:
            assert http.post("/tickets/T01/messages", json={"customer": "c1", "text": ""}).status_code == 422

    def test_health(self, server, tmp_path):
        with client(server, tmp_path, []) as http:
            assert http.get("/health").json() == {"status": "ok"}


class TestStatus:
    def test_a_finished_ticket(self, server, tmp_path):
        with client(server, tmp_path, WHERE) as http:
            http.post("/tickets/T01/messages", json={"customer": "c1", "text": "where is A1002"})
            assert http.get("/tickets/T01", params={"customer": "c1"}).json() == {
                "next": [], "reply": "Your mugs are on the way.", "waiting": []}

    def test_no_such_ticket(self, server, tmp_path):
        with client(server, tmp_path, []) as http:
            assert http.get("/tickets/T99", params={"customer": "c1"}).status_code == 404

    def test_someone_elses_ticket_is_not_found(self, server, tmp_path):
        with client(server, tmp_path, WHERE) as http:
            http.post("/tickets/T01/messages", json={"customer": "c1", "text": "where is A1002"})
            assert http.get("/tickets/T01", params={"customer": "c2"}).status_code == 404


class TestDecisions:
    def test_waits_then_approves(self, server, tmp_path):
        with client(server, tmp_path, REFUND) as http:
            events = parse(http.post("/tickets/T02/messages", json={"customer": "c1", "text": "refund A1001"}).text)
            assert events[-1][0] == "waiting" and events[-1][1]["order_id"] == "A1001"
            assert http.get("/tickets/T02", params={"customer": "c1"}).json()["waiting"][0]["amount"] == 39.0
            done = parse(http.post("/tickets/T02/decision", json={"customer": "c1", "action": "approve"}).text)
            assert done[-1] == ("done", "We have refunded you.")
            assert shop.refunds()[0]["order"] == "A1001"

    def test_nothing_waiting(self, server, tmp_path):
        with client(server, tmp_path, WHERE) as http:
            http.post("/tickets/T01/messages", json={"customer": "c1", "text": "where is A1002"})
            assert http.post("/tickets/T01/decision", json={"customer": "c1", "action": "approve"}).status_code == 409

    def test_an_edit_needs_an_amount(self, server, tmp_path):
        with client(server, tmp_path, REFUND) as http:
            http.post("/tickets/T02/messages", json={"customer": "c1", "text": "refund A1001"})
            assert http.post("/tickets/T02/decision", json={"customer": "c1", "action": "edit"}).status_code == 422
            assert http.post("/tickets/T02/decision", json={"customer": "c1", "action": "maybe"}).status_code == 422


class TestTheComparison:
    def test_written(self, source):
        text = source("API.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("How theirs does it", "What theirs has that mine does not",
                        "What mine does that theirs does not", "Which I would ship, and why"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 30, f"'{heading}' is {len(part.split())} words."
