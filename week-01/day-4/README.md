# Day 4 — The library's version

> **By the end of today** your graph is traced through Langfuse's LangChain handler,
> you have opened it in Studio, and you can point at the lines in `create_agent` that
> are the loop you wrote yesterday.

---

## Read first

- [ ] Langfuse — [LangChain and LangGraph integration](https://langfuse.com/integrations/frameworks/langchain) · 15 min
- [ ] LangGraph — [Run a local server](https://docs.langchain.com/oss/python/langgraph/local-server) · 10 min
- [ ] LangChain — [Agents](https://docs.langchain.com/oss/python/langchain/agents), up to "Middleware" · 15 min

---

## What you need to know

### Tracing without a recorder

A LangChain **callback** is told when every model, tool and node starts and ends.
Langfuse's `CallbackHandler` is one: pass it in the config, and the whole graph is
traced. Two metadata keys give it the user and the session.

### Studio

`langgraph dev` serves your graph locally with an API; Studio is a web page that
draws it and lets you run it step by step. It asks you to sign in to LangSmith to show
the page — keep `LANGSMITH_TRACING=false`, so nothing is sent there.

```bash
cd week-01/day-4 && langgraph dev
```

### `create_agent`

The library's ready-made agent. Build Desk with it — one line — and check it behaves
like yours. Then **read its source**. Reading a library's code to find out what a
function really does is a skill this course expects of you from now on.

---

## Exercises

```bash
pytest week-01/day-4 -v
```

Copy `desk_graph.py`, write `prebuilt.py`, then `COMPARE.md` and `READING.md`.

---

## Predict-then-run

Run `run_traced_graph.py` and day 1's `run_traced.py` with the same task. Before you
open Langfuse: which trace has more observations, and by roughly how many?

---

## Before you close the laptop

Commit, push, fill in the signal log.
