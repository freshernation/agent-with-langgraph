# Day 1 — Save every step

> **By the end of today** every step of every ticket is saved, a second message on a
> ticket sees the first, and a crash in the middle of a ticket loses nothing.

---

## Read first

- [ ] LangGraph — [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), up to "Memory store" · 20 min

---

## What you need to know

### A checkpointer saves the state after every step

Compile with one and every super-step is written down — the whole state, the nodes due
next — under a **thread**. Invoke again on the same thread and the graph starts from
what was saved.

### One thread per ticket

`thread_id` is yours to choose. A ticket is a good unit: everything said about it, by
the customer and by Helpdesk, lives in one thread. In week 1 your `chat` loop carried
the count between invokes; now the checkpointer carries everything.

### A crash is just a stop

If a node raises, the last completed step is already saved. A new process, a new
connection to the same file, and `invoke(None, config)` carries on — the finished
steps are not run again.

---

## Exercises

```bash
pytest week-03/day-1 -v
```

Copy your week 2 files (with two small changes to `helpdesk.py`), then write
`durable.py`.

---

## Predict-then-run

After a crash in the lookup's second model call, which node is due next? Write it
down, then call `where_it_stopped`.

---

## Before you close the laptop

Commit, push, fill in the signal log.
