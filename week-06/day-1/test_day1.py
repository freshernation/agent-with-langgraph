"""Week 6, Day 1 - facts that outlive a ticket.

Run me:  pytest week-06/day-1 -v
"""

import pytest
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from models import ScriptedModel, call, say


@pytest.fixture
def facts(load):
    return load("facts.py")


def ticket(facts, store, script, customer="c1", thread="T1", text="hi"):
    graph = facts.build_memory_desk(ScriptedModel(script), store, InMemorySaver())
    return graph.invoke({"messages": [HumanMessage(text)], "customer": customer},
                        {"configurable": {"thread_id": f"{customer}/{thread}"}})


class TestTheStore:
    def test_survives_reopening(self, facts, tmp_path):
        path = str(tmp_path / "m.db")
        facts.open_store(path).put(facts.namespace("c1"), "address", {"fact": "Leeds"})
        assert facts.open_store(path).get(facts.namespace("c1"), "address").value == {"fact": "Leeds"}

    def test_namespace(self, facts):
        assert facts.namespace("c4") == ("customers", "c4", "facts")


class TestRemember:
    def test_the_schema_hides_the_runtime(self, facts):
        assert set(facts.remember_fact.tool_call_schema.model_json_schema()["properties"]) == {"topic", "fact"}
        assert facts.known_facts.tool_call_schema.model_json_schema().get("properties", {}) == {}

    def test_one_ticket_remembers_another_reads(self, facts, tmp_path):
        store = facts.open_store(str(tmp_path / "m.db"))
        first = ticket(facts, store, [call("remember_fact", {"topic": " Address ", "fact": "moving to Leeds"}),
                                      say("Noted.")], thread="T1")
        assert first["messages"][-2].content == "Remembered: address."
        second = ticket(facts, store, [call("known_facts"), say("You are moving to Leeds.")], thread="T2")
        assert second["messages"][-2].content == "address: moving to Leeds", (
            "A new ticket is a new thread. The checkpoint starts empty; the store does not."
        )

    def test_another_customer_knows_nothing(self, facts, tmp_path):
        store = facts.open_store(str(tmp_path / "m.db"))
        ticket(facts, store, [call("remember_fact", {"topic": "address", "fact": "Leeds"}), say("ok")])
        other = ticket(facts, store, [call("known_facts"), say("ok")], customer="c2")
        assert other["messages"][-2].content == "Nothing remembered about this customer yet."

    def test_a_topic_again_replaces(self, facts, tmp_path):
        store = facts.open_store(str(tmp_path / "m.db"))
        ticket(facts, store, [call("remember_fact", {"topic": "contact", "fact": "email"}), say("ok")])
        ticket(facts, store, [call("remember_fact", {"topic": "contact", "fact": "phone"}), say("ok")], thread="T2")
        assert store.get(facts.namespace("c1"), "contact").value == {"fact": "phone"}

    @pytest.mark.parametrize("fact", ["card 4111 1111 1111 1111", "account 12-34-56-78-90-12"])
    def test_never_a_card_number(self, facts, tmp_path, fact):
        store = facts.open_store(str(tmp_path / "m.db"))
        result = ticket(facts, store, [call("remember_fact", {"topic": "payment", "fact": fact}), say("ok")])
        assert result["messages"][-2].content == "I do not store card or account numbers."
        assert store.get(facts.namespace("c1"), "payment") is None


class TestThePrompt:
    def test_the_rule_is_sent(self, facts, tmp_path):
        model = ScriptedModel(say("Hi."))
        graph = facts.build_memory_desk(model, facts.open_store(str(tmp_path / "m.db")))
        graph.invoke({"messages": [HumanMessage("hi")], "customer": "c1"})
        system = model.last_request["messages"][0].content
        assert system.endswith(facts.MEMORY_RULE) and len(facts.MEMORY_RULE.split()) >= 30
        assert "instruction" in facts.MEMORY_RULE
