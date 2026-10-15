"""Week 1 milestone - Desk as a graph, behaving like the loop you wrote.

Run me:  pytest week-01/milestone -v
"""

import pytest

SCRIPTS = {
    "no tool": [("say", "Hello.")],
    "one tool": [("tools", [("add_note", {"title": "dentist", "body": "Tue"})]), ("say", "Saved it.")],
    "two tools in one turn": [("tools", [("add_note", {"title": "a"}), ("add_note", {"title": "b"})]),
                              ("say", "Saved both.")],
    "a sum": [("tools", [("calculate", {"expression": "6*7"})]), ("say", "42")],
}


@pytest.fixture
def parity(load):
    return load("parity.py")


def fresh(monkeypatch, tmp_path, name):
    monkeypatch.setenv("NOTES_FILE", str(tmp_path / f"{name}.json"))


class TestTheScripts:
    def test_both_models_play_the_same_script(self, parity):
        steps = SCRIPTS["one tool"]
        hand = parity.to_hand(steps).chat([{"role": "user", "content": "x"}])
        graph = parity.to_graph(steps).invoke("x")
        assert hand["tool_calls"][0]["name"] == graph.tool_calls[0]["name"] == "add_note"

    def test_a_single_step_repeats(self, parity):
        model = parity.to_graph(("say", "again"))
        assert [model.invoke("x").content for _ in range(3)] == ["again"] * 3


class TestParity:
    @pytest.mark.parametrize("name", SCRIPTS)
    def test_same_behaviour(self, parity, monkeypatch, tmp_path, name):
        fresh(monkeypatch, tmp_path, "hand")
        hand = parity.run_hand(SCRIPTS[name], "do it")
        fresh(monkeypatch, tmp_path, "graph")
        graph = parity.run_graph(SCRIPTS[name], "do it")
        assert parity.differences(hand, graph) == [], f"{name}: {hand} vs {graph}"

    def test_the_one_that_differs(self, parity, monkeypatch, tmp_path):
        loop = ("tools", [("list_titles", {})])
        fresh(monkeypatch, tmp_path, "hand")
        hand = parity.run_hand(loop, "loop")
        fresh(monkeypatch, tmp_path, "graph")
        graph = parity.run_graph(loop, "loop")
        assert parity.differences(hand, graph) == ["answer"], (
            "A model that asks for the same tool for ever. Your hand-written Desk "
            "has a guard for this; the graph does not."
        )
        assert "repeat" in hand["answer"].lower()


class TestTheWriteUp:
    def test_written(self, source):
        text = source("FRAMEWORK.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("What the framework bought", "What it took away", "What I would still write by hand"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."
