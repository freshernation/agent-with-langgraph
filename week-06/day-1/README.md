# Day 1 — Facts that outlive a ticket

> **By the end of today** a fact Helpdesk learns in one ticket is there in the next,
> for that customer only — and a card number is never stored.

---

## Read first

- [ ] LangGraph — [Memory](https://docs.langchain.com/oss/python/langgraph/memory), short-term and long-term · 20 min

---

## What you need to know

### A checkpoint is one ticket; a store is everything

The checkpointer saves a thread. A new ticket is a new thread and starts empty. The
**store** is keyed by a namespace and a key, and every thread can read it. So
`("customers", "c1", "facts")` is where c1's facts live, whichever ticket they arrive in.

### Tools reach the store through the runtime

A tool that takes `runtime: ToolRuntime` gets `runtime.store` and `runtime.state` —
filled in by LangGraph, invisible to the model. The customer comes from the state, so
the model can never write to someone else's memory.

### Refuse before storing

A card number in memory is a card number in every future prompt, every trace and every
backup. The tool refuses any long run of digits before anything is written.

### The connection manages nothing

`SqliteStore` runs its own transactions, so its connection is opened with
`isolation_level=None`. Get this wrong and the first write fails.

---

## Exercises

```bash
pytest week-06/day-1 -v
```

Copy `tools.py`, then write `facts.py`.

---

## Predict-then-run

Remember a fact in thread T1, then open thread T2 for the same customer. Predict what
`graph.get_state(T2).values` holds, and what `known_facts` says.

---

## Before you close the laptop

Commit, push, fill in the signal log.
