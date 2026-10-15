# Day 3 — The loop is an edge

> **By the end of today** Desk runs as a graph: a model node, a tool node you wrote,
> and the conditional edge between them that is the agent loop.

---

## Read first

- [ ] LangGraph — [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) · 20 min
- [ ] Anthropic — [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), the section on agents · 10 min

---

## What you need to know

### Your loop, drawn

```
START -> model -> (tool calls?) -> tools -> model -> ... -> END
```

The `while` loop you wrote is now an edge from `tools` back to `model`. The `if` that
decided whether to stop is `route`.

### `MessagesState` appends

Its `messages` key has a **reducer** that adds what a node returns to what is already
there. So `call_model` returns one message, not the list. Return the whole list and
every message doubles — try it once on purpose.

### Tools from functions

`@tool` turns a function into a tool: its name is the tool's name, its docstring the
description, its type hints the schema. Desk's own functions in `desk.kit` do the
work, unchanged.

### `recursion_limit` is your step limit

It counts graph steps, not model calls. When it is reached, LangGraph raises; `ask`
turns that into an honest answer.

---

## Exercises

```bash
pytest week-01/day-3 -v
```

Write `desk_graph.py`.

---

## Predict-then-run

A model that always asks for `list_titles`, and `limit=6`. How many times is the model
called before it stops? Count it from `model.call_count`.

---

## Before you close the laptop

Commit, push, fill in the signal log.
