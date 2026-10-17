"""Week 7, Day 1 - the problem, on paper.

Run me:  pytest week-07/day-1 -v
"""

import pytest

HEADINGS = ["The problem", "Who it is for", "What goes wrong if it is wrong", "The cut list",
            "The graph", "The one eval that proves it works"]


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestTheProblem:
    def test_finished(self, source):
        text = source("PROBLEM.md")
        assert "<!--" not in text, "Delete the instructions comment."
        assert "<a name>" not in text, "Name your agent."

    @pytest.mark.parametrize("heading", [h for h in HEADINGS if h != "The graph"])
    def test_sections(self, source, heading):
        text = source("PROBLEM.md")
        assert f"## {heading}" in text, f"No '{heading}' section."
        assert len(section(text, heading).split()) >= 30, f"'{heading}' is too short."

    def test_the_graph_is_drawn(self, source):
        assert "```" in section(source("PROBLEM.md"), "The graph"), "Draw the graph in a code block."
