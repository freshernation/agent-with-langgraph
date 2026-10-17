"""Week 7, Day 4 - the portfolio page.

Run me:  pytest week-07/day-4 -v
"""

import re
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestThePage:
    def test_finished(self, source):
        text = source("PORTFOLIO.md")
        assert "<!--" not in text and "<Your agent" not in text

    @pytest.mark.parametrize("heading", ["What it does", "How I know it works", "What I would do next"])
    def test_sections(self, source, heading):
        text = source("PORTFOLIO.md")
        assert f"## {heading}" in text, f"No '{heading}' section."
        assert len(section(text, heading).split()) >= 40, f"'{heading}' is too short."

    def test_the_graph(self, source):
        assert "```" in section(source("PORTFOLIO.md"), "The graph")

    def test_screenshots_exist(self, source):
        images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", section(source("PORTFOLIO.md"), "Traces"))
        assert len(images) >= 2, "Link at least two screenshots: a trace and an eval run."
        for image in images:
            assert (HERE / image).exists(), f"{image} is linked but not in the folder."
