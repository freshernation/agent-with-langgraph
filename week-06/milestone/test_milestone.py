"""Week 6 milestone - Helpdesk that remembers.

Run me:  pytest week-06/milestone -v
"""

import pytest

from models import ScriptedModel, call, say


def form(**fields):
    return call("Triage", fields)


def episode(asked, outcome, order=None):
    return call("Episode", {"asked": asked, "outcome": outcome, "order_id": order})


@pytest.fixture
def parts(load):
    return load("helpdesk.py"), load("durable.py"), load("facts.py"), load("procedures.py")


def run(parts, tmp_path, script, customer, thread, text):
    helpdesk, durable, facts, _ = parts
    graph = helpdesk.build_helpdesk(ScriptedModel(script), checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")),
                                    store=facts.open_store(str(tmp_path / "m.db")))
    reply = helpdesk.answer(graph, customer, text, durable.config_for(customer, thread))
    return graph, reply


FIRST = [form(kind="refund", order_id="A1001"),
         call("remember_fact", {"topic": "contact", "fact": "prefers email"}),
         say("Noted the contact preference."),
         say("A person will review your kettle refund."),
         episode("Refund on a broken kettle", "Sent for approval", "A1001")]


class TestAcrossTickets:
    def test_the_second_ticket_knows_the_first(self, parts, tmp_path):
        run(parts, tmp_path, FIRST, "c1", "T1", "My kettle broke, refund A1001")
        model = ScriptedModel([form(kind="refund", order_id="A1001"), say("Seen before."), say("Sorry again."),
                               episode("Kettle again", "Apologised")])
        helpdesk, durable, facts, _ = parts
        graph = helpdesk.build_helpdesk(model, checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")),
                                        store=facts.open_store(str(tmp_path / "m.db")))
        helpdesk.answer(graph, "c1", "The kettle is broken again", durable.config_for("c1", "T2"))
        brief = model.requests[1]["messages"][0].content
        assert "- contact: prefers email" in brief, "A fact from ticket T1 must reach ticket T2's lookup."
        assert "c1/T1: Refund on a broken kettle; Sent for approval" in brief

    def test_each_ticket_is_recorded(self, parts, tmp_path):
        graph, _ = run(parts, tmp_path, FIRST, "c1", "T1", "My kettle broke, refund A1001")
        items = parts[2].open_store(str(tmp_path / "m.db")).search(("customers", "c1", "episodes"))
        assert [item.key for item in items] == ["c1/T1"]

    def test_another_customer_sees_none_of_it(self, parts, tmp_path):
        run(parts, tmp_path, FIRST, "c1", "T1", "My kettle broke, refund A1001")
        model = ScriptedModel([form(kind="where", order_id="A1003"), say("Delivered."), say("It was delivered."),
                               episode("Lamp", "Delivered")])
        helpdesk, durable, facts, _ = parts
        graph = helpdesk.build_helpdesk(model, checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")),
                                        store=facts.open_store(str(tmp_path / "m.db")))
        helpdesk.answer(graph, "c2", "Where is my lamp A1003, kettle aside", durable.config_for("c2", "T3"))
        brief = model.requests[1]["messages"][0].content
        assert "prefers email" not in brief and "c1/T1" not in brief


class TestHouseRules:
    def test_staff_rules_reach_every_ticket(self, parts, tmp_path):
        helpdesk, durable, facts, procedures = parts
        store = facts.open_store(str(tmp_path / "m.db"))
        procedures.add_procedure(store, "staff", "Offer the tracking number before apologising.")
        model = ScriptedModel([form(kind="where", order_id="A1002"), say("Shipped."), say("On its way."),
                               episode("Mugs", "Shipped")])
        graph = helpdesk.build_helpdesk(model, store=store)
        helpdesk.answer(graph, "c1", "Where are my mugs?")
        assert "- Offer the tracking number before apologising." in model.requests[1]["messages"][0].content


class TestForgetting:
    def test_forget_me(self, parts, tmp_path):
        run(parts, tmp_path, FIRST, "c1", "T1", "My kettle broke, refund A1001")
        helpdesk, durable, facts, _ = parts
        store = facts.open_store(str(tmp_path / "m.db"))
        graph = helpdesk.build_helpdesk(ScriptedModel([form(kind="change"), call("forget_me"), say("Done."),
                                                       say("We've forgotten what we knew."), episode("Forget me", "Done")]),
                                        store=store)
        helpdesk.answer(graph, "c1", "Please forget everything about me")
        assert store.search(facts.namespace("c1")) == []


class TestWithoutAStore:
    def test_still_works(self, parts):
        helpdesk = parts[0]
        graph = helpdesk.build_helpdesk(ScriptedModel([form(kind="where", order_id="A1002"), say("Shipped."),
                                                       say("On its way.")]))
        assert helpdesk.answer(graph, "c1", "Where are my mugs?") == "On its way."


class TestTheWriteUp:
    def test_written(self, source):
        text = source("MEMORY.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("What it remembers, and why", "What it refuses to remember", "How it forgets",
                        "What could go wrong"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
