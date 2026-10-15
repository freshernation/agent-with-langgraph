# Day 1 — Streaming

> **By the end of today** you can watch a graph run step by step, and stream just the
> words of the reply as the model writes them.

---

## Read first

- [ ] LangGraph — [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming), up to "Stream custom data" · 20 min
- [ ] Python — [Coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html), the first two sections · 15 min

---

## What you need to know

### Why `async`

A server handles many customers at once. While one ticket waits on the model, `async`
lets the server get on with another. `await` marks the places it may switch.

### Three stream modes

- `values` — the whole state after every step
- `updates` — what each node changed, as it finishes
- `messages` — every piece of every message, as it is produced

Ask for two at once and each item says which mode it came from.

### Filter by node

`messages` streams everything: the classifier's form, the lookup's working, tool
results. The customer should see the draft's words only. Every chunk's metadata says
which node produced it — filter on that.

### An interrupt is an event too

A refund waiting for a person arrives as an update called `__interrupt__`. The stream
ends; the thread waits.

---

## Exercises

```bash
pytest week-05/day-1 -v
```

Copy your week 3 milestone files, then write `streaming.py`.

---

## Predict-then-run

Stream a refund ticket with `stream_mode="values"` and print how many times the whole
state arrives. Predict first.

---

## Before you close the laptop

Commit, push, fill in the signal log.
