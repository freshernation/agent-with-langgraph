"""Week 5 milestone - Project 2: Helpdesk over HTTP, streaming, durable.

Run me:  pytest week-05/milestone -v
Then:    docker compose -f week-05/milestone/compose.yaml up --build
"""

import json

import pytest
from fastapi.testclient import TestClient
from langchain_core.callbacks import BaseCallbackHandler

import shop
from models import ScriptedModel, call, say


def form(**fields):
    return call("Triage", fields)


WHERE = [form(kind="where", order_id="A1002"), call("tracking", {"order_id": "A1002"}),
         say("Shipped, TRK-5544."), say("Your mugs are on the way.")]
REFUND_START = [form(kind="refund", order_id="A1001"),
                call("request_refund", {"order_id": "A1001", "amount": 39.0, "reason": "broken"})]


class Recording(BaseCallbackHandler):
    def __init__(self):
        self.metadata = []

    def on_chat_model_start(self, serialized, messages, **kwargs):
        self.metadata.append(kwargs.get("metadata") or {})


@pytest.fixture
def app(load):
    return load("app.py")


def parse(text):
    events = []
    for block in text.strip().split("\n\n"):
        fields = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((fields["event"], json.loads(fields["data"])))
    return events


def url(tmp_path):
    return f"sqlite:///{tmp_path / 'h.db'}"


class TestOverHttp:
    def test_a_ticket_streams(self, app, tmp_path):
        with TestClient(app.create_app(ScriptedModel(WHERE), url(tmp_path))) as http:
            events = parse(http.post("/tickets/T01/messages", json={"customer": "c1", "text": "where is A1002"}).text)
            assert events[-1] == ("done", "Your mugs are on the way.")

    def test_every_model_call_is_traced_to_the_ticket(self, app, tmp_path):
        handler = Recording()
        with TestClient(app.create_app(ScriptedModel(WHERE), url(tmp_path), [handler])) as http:
            http.post("/tickets/T01/messages", json={"customer": "c1", "text": "where is A1002"})
        assert len(handler.metadata) == 4
        assert all(m.get("langfuse_session_id") == "c1/T01" and m.get("langfuse_user_id") == "c1"
                   for m in handler.metadata)


class TestARefundThroughARestart:
    def test_decided_after_the_server_restarts(self, app, tmp_path):
        with TestClient(app.create_app(ScriptedModel(REFUND_START), url(tmp_path))) as http:
            events = parse(http.post("/tickets/T02/messages", json={"customer": "c1", "text": "refund A1001"}).text)
            assert events[-1][0] == "waiting"

        later = ScriptedModel([say("Refunded."), say("We've refunded $39.00.")])
        with TestClient(app.create_app(later, url(tmp_path))) as http:
            assert http.get("/tickets/T02", params={"customer": "c1"}).json()["waiting"][0]["order_id"] == "A1001"
            done = parse(http.post("/tickets/T02/decision", json={"customer": "c1", "action": "approve"}).text)
            assert done[-1] == ("done", "We've refunded $39.00.")
        assert len(shop.refunds()) == 1

    def test_no_new_message_while_waiting(self, app, tmp_path):
        with TestClient(app.create_app(ScriptedModel(REFUND_START), url(tmp_path))) as http:
            http.post("/tickets/T02/messages", json={"customer": "c1", "text": "refund A1001"})
            again = http.post("/tickets/T02/messages", json={"customer": "c1", "text": "hello??"})
            assert again.status_code == 409, (
                "A second message while a refund waits starts a second turn on top of the "
                "first. Refuse it until a person decides."
            )


class TestFromTheEnvironment:
    def test_uses_database_url(self, app, tmp_path, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", url(tmp_path))
        monkeypatch.setenv("AGENT_PROVIDER", "fake")
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        with TestClient(app.from_environment()) as http:
            assert http.get("/health").json() == {"status": "ok"}
        assert (tmp_path / "h.db").exists()


def lines(source, name):
    return "\n".join(l for l in source(name).splitlines() if l.strip() and not l.strip().startswith("#"))


class TestTheContainer:
    def test_the_files(self, source):
        assert "--factory" in lines(source, "Dockerfile") and "app:from_environment" in lines(source, "Dockerfile")
        assert "week-05/milestone/Dockerfile" in lines(source, "compose.yaml")
        assert ".env" in lines(source, ".dockerignore")


class TestTheIncident:
    def test_written(self, source):
        text = source("INCIDENT.md")
        assert "<!--" not in text, "Copy your incident write-up from day 4."
        for heading in ("What customers saw", "Timeline", "Why it happened", "How I found out", "What I changed"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
