# Day 1 — When two nodes write the same key

> **By the end of today** you can choose a reducer for every key in a state, and say
> what goes wrong without one.

---

## Read first

- [ ] LangGraph — [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), the section on state and reducers · 15 min

---

## What you need to know

### A reducer is how a write is combined

A node returns `{"notes": ["order checked"]}`. What happens to the notes already
there? With no reducer, the new value **replaces** the old. With `operator.add`, the
lists **join**. With a function you write, whatever you decide.

### Parallel nodes make it matter

Three nodes running in the same step, all writing `notes`. Without a reducer there is
no right answer — so LangGraph raises `InvalidUpdateError` rather than guess. With one,
every write is kept.

### `add_messages` is a reducer too

It is why `call_model` returned one message in week 1. It appends — unless the new
message has the **same id** as an old one, and then it replaces it. That is how you
edit a message already in the state.

### Type nodes loosely

LangGraph reads a node's type hint as the state it expects. Type the argument as
`dict` when one function serves two graphs.

---

## Exercises

```bash
pytest week-02/day-1 -v
```

Write `reducers.py`.

---

## Predict-then-run

Change `tags` to `operator.add`. Predict `result["tags"]` before you run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
