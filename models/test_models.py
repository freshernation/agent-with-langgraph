"""The course's LangChain model layer works offline."""

import pytest
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel

from models import ScriptedModel, call, connect, say


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def test_in_order():
    model = ScriptedModel([say("one"), say("two")])
    assert model.invoke("x").content == "one"
    assert model.invoke("x").content == "two"
    with pytest.raises(AssertionError):
        model.invoke("x")


def test_repeats_a_single_reply():
    model = ScriptedModel(say("same"))
    assert [model.invoke("x").content for _ in range(3)] == ["same"] * 3


def test_echoes_when_unscripted():
    assert "hello" in ScriptedModel().invoke([HumanMessage("hello")]).content


def test_tool_calls_and_records_tools():
    model = ScriptedModel([call("add", {"a": 1, "b": 2})])
    reply = model.bind_tools([add]).invoke("1+2")
    assert reply.tool_calls[0]["name"] == "add" and reply.tool_calls[0]["args"] == {"a": 1, "b": 2}
    assert model.last_request["tools"][0]["function"]["name"] == "add"
    assert model.call_count == 1


def test_usage():
    assert ScriptedModel(say("x", input=5, output=7)).invoke("x").usage_metadata["output_tokens"] == 7


def test_errors():
    model = ScriptedModel([RuntimeError("down")])
    with pytest.raises(RuntimeError):
        model.invoke("x")


def test_structured_output():
    class Kind(BaseModel):
        kind: str
    model = ScriptedModel([call("Kind", {"kind": "refund"})])
    assert model.with_structured_output(Kind).invoke("x") == Kind(kind="refund")


def test_connect_defaults_to_scripted(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "fake")
    assert isinstance(connect(), ScriptedModel)


def test_connect_refuses_nonsense():
    with pytest.raises(ValueError):
        connect("nonsense")
