"""Week 7, Day 3 - your agent, evaluated.

Run me:  pytest week-07/day-3 -v
"""

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).parent.parent / "project"


@pytest.fixture
def evals():
    sys.path.insert(0, str(PROJECT))
    try:
        spec = importlib.util.spec_from_file_location("project_evals", PROJECT / "evals.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        yield module
    finally:
        sys.path.remove(str(PROJECT))


class TestTheEvals:
    def test_a_dataset(self, evals):
        items = getattr(evals, "DATASET", [])
        assert len(items) >= 10, f"{len(items)} items. Label at least ten."
        assert len({item["id"] for item in items}) == len(items), "Item ids repeat."
        for item in items:
            assert "input" in item and "expected_output" in item

    def test_evaluators(self, evals):
        evaluators = getattr(evals, "EVALUATORS", [])
        assert len(evaluators) >= 2
        for evaluator in evaluators:
            parameters = inspect.signature(evaluator).parameters
            assert {"input", "output", "expected_output"} <= set(parameters)

    def test_a_task(self, evals):
        assert callable(getattr(evals, "make_task", None))


class TestTheReport:
    def test_written(self, source):
        text = source("EVAL_REPORT.md")
        assert "<!--" not in text, "Delete the instructions comment."
        for heading in ("What I measured", "The numbers", "What failed, and why", "What I changed"):
            assert f"## {heading}" in text, f"No '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 30, f"'{heading}' is {len(part.split())} words."
        assert any(ch.isdigit() for ch in text.split("## The numbers", 1)[1].split("\n## ")[0])
