"""Week 3, Day 3 - history, replay and forking.

Run me:  pytest week-03/day-3 -v
"""

import pytest

from models import ScriptedModel, call, say


def form(**fields):
    return call("Triage", fields)


@pytest.fixture
def tt(load):
    return load("timetravel.py")


@pytest.fixture
def parts(load):
    return load("helpdesk.py"), load("durable.py"), load("classify.py")


def build(parts, path, script):
    helpdesk, durable, _ = parts
    return helpdesk.build_helpdesk(ScriptedModel(script), checkpointer=durable.open_checkpointer(path))


WHERE = [form(kind="where", order_id="A1002"), call("tracking", {"order_id": "A1002"}),
         say("Shipped, TRK-5544."), say("First draft.")]


class TestHistory:
    def test_newest_first(self, tt, parts, tmp_path):
        helpdesk, durable, _ = parts
        graph = build(parts, str(tmp_path / "c.db"), WHERE)
        config = durable.config_for("c1", "T01")
        helpdesk.answer(graph, "c1", "Where is A1002?", config)
        steps = tt.history(graph, config)
        assert steps[0]["next"] == () and steps[-1]["next"] == ("__start__",)
        assert [s["step"] for s in steps] == sorted([s["step"] for s in steps], reverse=True)
        assert all(s["checkpoint_id"] for s in steps)

    def test_checkpoint_before(self, tt, parts, tmp_path):
        helpdesk, durable, _ = parts
        graph = build(parts, str(tmp_path / "c.db"), WHERE)
        config = durable.config_for("c1", "T01")
        helpdesk.answer(graph, "c1", "Where is A1002?", config)
        assert graph.get_state(tt.checkpoint_before(graph, config, "draft")).next == ("draft",)
        assert tt.checkpoint_before(graph, config, "handoff") is None


class TestReplay:
    def test_runs_again_from_there(self, tt, parts, tmp_path):
        helpdesk, durable, _ = parts
        graph = build(parts, str(tmp_path / "c.db"), WHERE + [say("Second draft.")])
        config = durable.config_for("c1", "T01")
        helpdesk.answer(graph, "c1", "Where is A1002?", config)
        assert tt.replay(graph, tt.checkpoint_before(graph, config, "draft")) == "Second draft."
        assert graph.get_state(config).values["reply"] == "Second draft.", (
            "After a replay, the thread's latest state is the new branch."
        )


class TestFork:
    def test_fix_a_wrong_triage(self, tt, parts, tmp_path):
        helpdesk, durable, classify = parts
        script = [form(kind="other"), call("tracking", {"order_id": "A1002"}),
                  say("Shipped, TRK-5544."), say("Your mugs are on the way.")]
        graph = build(parts, str(tmp_path / "c.db"), script)
        config = durable.config_for("c1", "T01")
        assert helpdesk.answer(graph, "c1", "Where is A1002?", config) == helpdesk.HANDOFF

        right = classify.Triage(kind="where", order_id="A1002")
        assert tt.fix_triage(graph, config, right) == "Your mugs are on the way."
        assert graph.get_state(config).values["triage"] == right
        assert any(step["next"] == ("handoff",) for step in tt.history(graph, config)), (
            "The old branch is still in the history. A fork adds; it does not erase."
        )

    def test_nothing_to_fix(self, tt, parts, tmp_path):
        helpdesk, durable, classify = parts
        graph = build(parts, str(tmp_path / "c.db"), [])
        with pytest.raises(ValueError):
            tt.fix_triage(graph, durable.config_for("c1", "never"), classify.Triage(kind="where"))
