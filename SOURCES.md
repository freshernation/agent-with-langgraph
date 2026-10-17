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

**Ignore for now:** `interrupt_before` on compile, Postgres. The long-term store is week 6.

## Week 4 — Measure it

| Read | Why |
|---|---|
| [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | What to grade, and how |
| [Hamel Husain — Your AI product needs evals](https://hamel.dev/blog/posts/evals/) | An engineer's account of building them for real |
| [Langfuse — LLM-as-a-judge](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge) | A judge, and its limits |
| [Langfuse — Experiments via the SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk) | Running a dataset with your evaluators |

**Ignore for now:** generated test cases, evaluation leaderboards, LangSmith evals.

## Week 5 — Ship it

| Read | Why |
|---|---|
| [LangGraph — Streaming](https://docs.langchain.com/oss/python/langgraph/streaming) | The stream modes, and filtering by node |
| [MDN — Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) | The format your stream speaks |
| [Docker — Building best practices](https://docs.docker.com/build/building/best-practices/) | The build cache, and not running as root |
| [Google SRE — Postmortem culture](https://sre.google/sre-book/postmortem-culture/) | Writing an incident without blame |

**Ignore for now:** WebSockets, Kubernetes, the hosted LangGraph Platform.

## Week 6 — Memory that lasts

| Read | Why |
|---|---|
| [LangGraph — Memory](https://docs.langchain.com/oss/python/langgraph/memory) | Short-term and long-term, and the store |
| [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | What deserves a place in the prompt |
| [Sumers et al. — Cognitive architectures for language agents](https://arxiv.org/abs/2309.02427) | Where "facts, episodes, procedures" comes from |
| [ICO — Right to erasure](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/) | Why forgetting is a feature |

**Ignore for now:** memory frameworks, vector databases for memory, shared memory between agents.

## Week 7 — Your agent, and the interview

No new reading. Reread what your own project needs, and `ai/interviewer.md`.
