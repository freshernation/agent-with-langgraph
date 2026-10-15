# Sources

Chosen by the librarian rule: an official source for how the thing works, an
engineering account from people who build with it for why, and nothing that is a
vendor selling the answer without saying so. Three or four a week, not ten.

Need something that is not here? `ai/librarian.md`.

---

## The ones worth reading twice

| Read | Why |
|---|---|
| [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | When a graph, when an agent, and when neither |
| [LangGraph — Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) | The framework's own account of how to design a graph |
| [Langfuse — Observability overview](https://langfuse.com/docs/observability/overview) | Traces, observations and sessions, in one page |

---

## Week 1 — You already wrote this

| Read | Why |
|---|---|
| [Langfuse — Observability overview](https://langfuse.com/docs/observability/overview) | Traces, observations, generations |
| [LangGraph — Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) | State, nodes, edges, in the library's words |
| [LangGraph — Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) | How to design a graph before writing one |
| [Langfuse — LangChain and LangGraph integration](https://langfuse.com/integrations/frameworks/langchain) | Tracing a graph with one callback |

**Ignore for now:** LCEL, LangChain's chains, LangSmith.

## Week 2 — State

| Read | Why |
|---|---|
| [LangGraph — Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) | State and reducers |
| [LangChain — Structured output](https://docs.langchain.com/oss/python/langchain/structured-output) | A form the model must fill in |
| [LangChain — Tools](https://docs.langchain.com/oss/python/langchain/tools) | Tools that read the state, which the model never sees |
| [LangGraph — Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | Routing, and when a fixed shape beats an agent |

**Ignore for now:** `Send` and map-reduce, subgraphs, LangChain's output parsers.

## Week 3 — Memory and a human

| Read | Why |
|---|---|
| [LangGraph — Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Checkpointers, threads, and what is saved |
| [LangGraph — Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Stopping for a person, and the rule about code that runs twice |
| [LangGraph — Time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel) | Replay and fork |
| [Langfuse — Sessions](https://langfuse.com/docs/observability/features/sessions) | One conversation, many traces |

**Ignore for now:** the long-term store, `interrupt_before` on compile, Postgres.

## Weeks 4 to 6

Chosen when each week is published.
