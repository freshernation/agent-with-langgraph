# Day 1 — See your own agent

> **By the end of today** your hand-written Desk sends a trace of every turn to
> Langfuse, and you can read one: what ran, in what order, how long it took, what it
> cost.

---

## Read first

- [ ] Langfuse — [Observability overview](https://langfuse.com/docs/observability/overview) · 15 min
- [ ] Langfuse — [Sessions](https://langfuse.com/docs/observability/features/sessions) · 5 min

---

## What you need to know

### A trace is a tree

One turn is one **trace**. Inside it are **observations**, nested: the turn itself,
and inside it each model call (a **generation**, with tokens and cost) and each tool
call. In Langfuse's Python SDK, anything started inside a `with` block is nested under
it. That is the whole trick.

### Stand in front, change nothing

`TracedModel` looks like a model to Desk and passes every call through, writing it
down on the way. Traced tools do the same. Desk itself does not change by one line —
the same idea as a recorder, and the same idea LangChain's callbacks use on Thursday.

### Users and sessions

`propagate_attributes(user_id=..., session_id=...)` stamps every observation inside
it with who and which conversation. That is how you will find one customer's day in
week 3.

### The tests do not need Langfuse

They hand your code a fake client that writes the trace down. `run_traced.py` uses
the real one — run it, and look.

---

## Exercises

```bash
pytest week-01/day-1 -v
```

Write `traced.py`. Then run `run_traced.py` twice and write `READING_A_TRACE.md`.

---

## Predict-then-run

Before you open the trace of a two-tool turn: how many generations, how many tool
observations, and which generation used more input tokens?

---

## Before you close the laptop

Commit, push, fill in the signal log.
