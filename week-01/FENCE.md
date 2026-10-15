# Week 1 — Concept fence

## Allowed

**Everything from Agent From Zero**, plus:

- `TypedDict`, type hints on functions, `total=False`
- Decorators — using one (`@tool`), not writing one
- `functools.partial`
- LangGraph: `StateGraph`, `START`, `END`, `add_node`, `add_edge`,
  `add_conditional_edges`, `compile`, `invoke`, `MessagesState`, `recursion_limit`,
  `GraphRecursionError`
- LangChain: `HumanMessage`, `SystemMessage`, `ToolMessage`, `AIMessage.tool_calls`,
  `@tool`, `bind_tools`, `create_agent`
- Langfuse: `start_as_current_observation`, `propagate_attributes`, the LangChain
  `CallbackHandler`, `langfuse_user_id` and `langfuse_session_id` metadata
- `langgraph dev` and Studio, with LangSmith tracing off

## Not yet

Reducers you write yourself (week 2) · structured output (week 2) · checkpointers,
threads, `interrupt` (week 3) · datasets and scores (week 4) · `async` and streaming
(week 5) · `ToolNode` and `tools_condition` — read about, not used · LCEL pipes

---

## Why your own tool node

`ToolNode` exists and does more than yours. You write your own first because it is
twenty lines, because you can see exactly what happens when a tool fails, and because
in week 3 you will put a human approval step inside it. Use the library's once you
could have written it.
