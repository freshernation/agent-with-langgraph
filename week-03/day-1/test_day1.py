"""Week 3, Day 1 - checkpointers and threads.

Run me:  pytest week-03/day-1 -v

"A restart" here is what it is in real life: the graph and its connection are
thrown away, and a new one is opened on the same file.
"""

import pytest

from models import ScriptedModel, call, say


@pytest.fixture
def durable(load):
    return load("durable.py")


@pytest.fixture
def helpdesk(load):
    return load("helpdesk.py")


def form(**fields):
    return call("Triage", fields)


class TestThreads:
    def test_config(self, durable):
        assert durable.config_for("c1", "T01") == {"configurable": {"thread_id": "c1/T01"}}

    def test_a_finished_thread_has_nothing_next(self, durable, helpdesk, tmp_path):
        graph = helpdesk.build_helpdesk(ScriptedModel([form(kind="other")]),
                                        checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")))
        config = durable.config_for("c1", "T11")
        helpdesk.answer(graph, "c1", "How do I reset my password?", config)
        assert durable.where_it_stopped(graph, config) == ()

    def test_a_second_message_sees_the_first(self, durable, helpdesk, tmp_path):
        model = ScriptedModel([form(kind="where", order_id="A1002"), say("Shipped."), say("It's on its way."),
                               form(kind="where", order_id="A1002"), say("Still shipped."), say("Still coming.")])
        graph = helpdesk.build_helpdesk(model, checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")))
        config = durable.config_for("c1", "T01")
        helpdesk.answer(graph, "c1", "Where is A1002?", config)
        helpdesk.answer(graph, "c1", "Any news?", config)
        lines = durable.conversation(graph, config)
        assert lines[0] == "human: Where is A1002?" and "human: Any news?" in lines
        lookup_saw = [m.content for m in model.requests[4]["messages"]]
        assert "Where is A1002?" in lookup_saw, "The second turn's lookup must see the first turn."

    def test_threads_do_not_mix(self, durable, helpdesk, tmp_path):
        model = ScriptedModel([form(kind="other"), form(kind="other")])
        graph = helpdesk.build_helpdesk(model, checkpointer=durable.open_checkpointer(str(tmp_path / "c.db")))
        helpdesk.answer(graph, "c1", "first ticket", durable.config_for("c1", "T1"))
        helpdesk.answer(graph, "c1", "second ticket", durable.config_for("c1", "T2"))
        assert durable.conversation(graph, durable.config_for("c1", "T2")) == ["human: second ticket"]


class TestARestart:
    def test_it_carries_on_where_it_stopped(self, durable, helpdesk, tmp_path):
        path = str(tmp_path / "c.db")
        config = durable.config_for("c1", "T01")
        crashing = ScriptedModel([form(kind="where", order_id="A1002"),
                                  call("tracking", {"order_id": "A1002"}), RuntimeError("process killed")])
        graph = helpdesk.build_helpdesk(crashing, checkpointer=durable.open_checkpointer(path))
        with pytest.raises(RuntimeError):
            helpdesk.answer(graph, "c1", "Where is A1002?", config)

        fresh = ScriptedModel([say("A1002 has shipped, TRK-5544."), say("Your mugs are on the way.")])
        restarted = helpdesk.build_helpdesk(fresh, checkpointer=durable.open_checkpointer(path))
        assert durable.where_it_stopped(restarted, config) == ("lookup",)
        assert durable.resume(restarted, config) == "Your mugs are on the way."
        assert fresh.call_count == 2, (
            "After the restart only the unfinished work should run. Classifying again, "
            "or calling the tool again, means the checkpoint was not used."
        )
