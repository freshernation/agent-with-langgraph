# Day 4 — One customer, many tickets

> **By the end of today** each ticket is one session in Langfuse, named the same as
> its saved thread, and you can pull up one customer's week.

---

## Read first

- [ ] Langfuse — [Sessions](https://langfuse.com/docs/observability/features/sessions) · 5 min
- [ ] Langfuse — [Users](https://langfuse.com/docs/observability/features/users) · 5 min

---

## What you need to know

### One config, three jobs

The thread for the checkpointer, the callbacks for tracing, the user and session for
Langfuse. Make the thread id and the session id the **same string**, and you can always
get from a row in Langfuse to the saved thread and back.

### Reading traces back

Langfuse has an API. `fetch_customer.py` asks it for one customer's traces; your
`customer_story` turns them into one line per ticket. When a customer says "you have
answered me badly all week", this is where you start.

---

## Exercises

```bash
pytest week-03/day-4 -v
python3 week-03/day-4/fetch_customer.py c1
```

Write `sessions.py`, then `ONE_CUSTOMER.md`.

---

## Predict-then-run

Before you fetch: how many sessions does c1 have, and which cost most?

---

## Before you close the laptop

Commit, push, fill in the signal log.
