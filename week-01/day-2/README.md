# Day 2 — A graph with no model in it

> **By the end of today** you can build a LangGraph graph from typed state, nodes and
> edges, and route between nodes — with no model anywhere, so you can see the
> framework on its own.

---

## Read first

- [ ] LangGraph — [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api), up to "Send" · 20 min
- [ ] Python — [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict) · 5 min

---

## What you need to know

### Three ideas

- **State** — a typed dict that every node can read.
- **Nodes** — functions that take the state and return **only the keys they
  changed**. LangGraph merges them in.
- **Edges** — what runs next. A conditional edge calls a function that returns the
  name of the next node.

### Your week 1 chatbot, again

In Agent From Zero you wrote it as an `if` ladder inside a `while` loop. Today the
ladder becomes a `route` function and six answer nodes. The loop is not in the graph:
one invoke is one message, and `chat` carries the count from one invoke to the next.
On week 3 day 1 a checkpointer will carry it for you.

### See it

`build_graph().get_graph().draw_mermaid()` prints your graph as a diagram. Paste it
into any Mermaid viewer. It should look like your drawing.

---

## Exercises

```bash
pytest week-01/day-2 -v
```

Write `ladder.py`.

---

## Predict-then-run

What does `graph.invoke({"text": "  "})` return — every key? Write it down, then run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
