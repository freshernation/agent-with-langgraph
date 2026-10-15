"""Week 1, Day 2 - a graph with no model in it.

Run me:  pytest week-01/day-2 -v
"""

import pytest


@pytest.fixture
def ladder(load):
    return load("ladder.py")


@pytest.fixture
def graph(ladder):
    return ladder.build_graph()


class TestTidy:
    def test_trims_and_counts(self, ladder):
        assert ladder.tidy({"text": "  HELP ", "sent": 2, "path": []}) == {
            "command": "help", "sent": 3, "path": ["tidy"]}

    def test_empty_does_not_count(self, ladder):
        assert ladder.tidy({"text": "   ", "sent": 2, "path": []})["sent"] == 2

    def test_returns_only_what_it_changes(self, ladder):
        assert "text" not in ladder.tidy({"text": "hi", "sent": 0, "path": []}), (
            "A node returns the keys it changed. LangGraph merges them into the state."
        )


class TestRoute:
    @pytest.mark.parametrize("command,node", [
        ("hello", "hello"), ("help", "help"), ("count", "count"), ("quit", "quit"),
        ("", "empty"), ("pizza", "unknown"),
    ])
    def test_routes(self, ladder, command, node):
        assert ladder.route({"command": command}) == node


class TestTheGraph:
    def test_its_nodes(self, graph):
        nodes = set(graph.get_graph().nodes) - {"__start__", "__end__"}
        assert nodes == {"tidy", "hello", "help", "count", "quit", "empty", "unknown"}

    def test_one_turn(self, graph):
        result = graph.invoke({"text": "hello", "sent": 0, "path": []})
        assert result["reply"] == "Hi! I am Desk."
        assert result["path"] == ["tidy", "hello"]

    def test_unknown_uses_the_tidied_text(self, graph):
        assert graph.invoke({"text": " Pizza ", "sent": 0, "path": []})["reply"] == 'I don\'t know "pizza" yet.'


class TestChat:
    def test_the_worked_example(self, ladder, graph):
        assert ladder.chat(graph, ["hello", "pizza", "", "count", "quit"]) == [
            "Hi! I am Desk.", 'I don\'t know "pizza" yet.', "Say something.",
            "You have sent 3 messages.", "Bye! We exchanged 4 messages."]

    def test_stops_at_quit(self, ladder, graph):
        assert len(ladder.chat(graph, ["quit", "hello"])) == 1
