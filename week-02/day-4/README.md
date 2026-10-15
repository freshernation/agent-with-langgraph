# Day 4 — Routing

> **By the end of today** a ticket is classified, routed, looked up and drafted — and
> a dropped connection or a provider outage does not stop it.

---

## Read first

- [ ] LangGraph — [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents), "Routing" · 15 min
- [ ] LangGraph — [Use the graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api), "Add retry policies" · 10 min

---

## What you need to know

### A workflow with an agent inside

Classify and draft are single model calls in fixed places. Lookup is the week 1 loop.
Most real agents look like this: a fixed shape, with a loop only where the number of
steps genuinely varies.

### Draft from facts only

The drafting call gets the ticket, the kind and what lookup found — and no tools.
It cannot look anything up, so it cannot invent a lookup.

### Retries are for blips

`RetryPolicy` on a node runs it again when it raises. By default it retries a dropped
connection and not a bug — but check what your provider's errors inherit from before
you trust that with a 400.

### A backup model

`with_fallbacks` tries a second model when the first raises. Bind the tools to **each**
model first: a model with fallbacks has no `bind_tools` of its own.

---

## Exercises

```bash
pytest week-02/day-4 -v
```

Copy `classify.py` and `tools.py`, then write `helpdesk.py`.

---

## Predict-then-run

A password ticket. Predict how many model calls Helpdesk makes, then count them.

---

## Before you close the laptop

Commit, push, fill in the signal log.
