"""A scripted LangChain chat model, for tests. No key, no network, no cost.

    ScriptedModel([reply_1, reply_2])   hands those back in order
    ScriptedModel(reply)                hands the same one back every time
    ScriptedModel()                     repeats the last human message back

    say("Hello.")                                   a plain answer
    call("add_note", {"title": "x"})                one tool call
    calls([("a", {}), ("b", {"x": 1})])             several tool calls in one turn

Put an exception in the script to make that call fail. After a run,
model.requests holds what each call was sent, and model.call_count how many.
"""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import PrivateAttr


def _usage(input: int, output: int) -> dict:
    return {"input_tokens": input, "output_tokens": output, "total_tokens": input + output}


def say(text: str, input: int = 10, output: int = 20) -> AIMessage:
    return AIMessage(content=text, usage_metadata=_usage(input, output))


def call(name: str, args: dict | None = None, id: str = "call_1", text: str = "",
         input: int = 10, output: int = 20) -> AIMessage:
    return calls([(name, args or {})], text=text, input=input, output=output, first_id=id)


def calls(pairs: list, text: str = "", input: int = 10, output: int = 20,
          first_id: str = "call_1") -> AIMessage:
    tool_calls = []
    for number, (name, args) in enumerate(pairs):
        call_id = first_id if number == 0 else f"call_{number + 1}"
        tool_calls.append({"name": name, "args": dict(args), "id": call_id, "type": "tool_call"})
    return AIMessage(content=text, tool_calls=tool_calls, usage_metadata=_usage(input, output))


class ScriptedModel(BaseChatModel):
    _script: list = PrivateAttr(default_factory=list)
    _repeat: bool = PrivateAttr(default=False)
    _unscripted: bool = PrivateAttr(default=True)
    _position: int = PrivateAttr(default=0)
    _requests: list = PrivateAttr(default_factory=list)

    def __init__(self, script: Any = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._unscripted = script is None
        self._repeat = script is not None and not isinstance(script, list)
        if script is None:
            self._script = []
        elif self._repeat:
            self._script = [script]
        else:
            self._script = list(script)

    @property
    def _llm_type(self) -> str:
        return "scripted"

    @property
    def requests(self) -> list:
        return self._requests

    @property
    def call_count(self) -> int:
        return len(self._requests)

    @property
    def last_request(self) -> dict:
        return self._requests[-1]

    def bind_tools(self, tools, **kwargs):
        return self.bind(tools=[convert_to_openai_tool(tool) for tool in tools], **kwargs)

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        self._requests.append({"messages": list(messages), "tools": kwargs.get("tools")})
        if self._unscripted:
            said = ""
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    said = message.content if isinstance(message.content, str) else str(message.content)
                    break
            reply = say(f"(scripted model) You said: {said}")
        elif self._repeat:
            reply = self._script[0]
        else:
            if self._position >= len(self._script):
                raise AssertionError(
                    f"The code called the model {self._position + 1} times but only "
                    f"{len(self._script)} replies were scripted. It should have stopped by now.")
            reply = self._script[self._position]
            self._position += 1
        if isinstance(reply, Exception):
            raise reply
        return ChatResult(generations=[ChatGeneration(message=reply.model_copy(deep=True))])
