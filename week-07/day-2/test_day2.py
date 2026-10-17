"""Week 7, Days 2 and 3 - your agent, built and tested.

Run me:  pytest week-07/day-2 -v

Your code lives in week-07/project/. These tests check its shape and run YOUR
tests; what it does is up to you.
"""

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

from langgraph.graph.state import CompiledStateGraph

from models import ScriptedModel

PROJECT = Path(__file__).parent.parent / "project"
ROOT = Path(__file__).parents[2]


def load_graph_module():
    sys.path.insert(0, str(PROJECT))
    try:
        spec = importlib.util.spec_from_file_location("project_graph", PROJECT / "graph.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(PROJECT))


def test_build_graph():
    module = load_graph_module()
    assert hasattr(module, "build_graph"), "project/graph.py needs build_graph(model, checkpointer=None)."
    graph = module.build_graph(ScriptedModel())
    assert isinstance(graph, CompiledStateGraph)
    nodes = set(graph.get_graph().nodes) - {"__start__", "__end__"}
    assert len(nodes) >= 3, f"Only {len(nodes)} nodes of your own: {sorted(nodes)}."


def test_at_least_five_tests_of_your_own():
    count = 0
    for path in PROJECT.glob("test_*.py"):
        tree = ast.parse(path.read_text())
        count += sum(1 for node in ast.walk(tree)
                     if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    assert count >= 5, f"{count} tests in week-07/project. Write at least five."


def test_your_tests_are_offline():
    with_tests = [path for path in PROJECT.glob("test_*.py")
                  if any(isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
                         for node in ast.walk(ast.parse(path.read_text())))]
    assert with_tests, "No test functions in week-07/project yet."
    for path in with_tests:
        assert "ScriptedModel(" in path.read_text(), f"{path.name} does not use ScriptedModel."


def test_your_tests_pass():
    result = subprocess.run([sys.executable, "-m", "pytest", str(PROJECT), "-q", "-p", "no:cacheprovider"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout[-2000:]
