# Day 3 — Go back in time

> **By the end of today** you can list every step a ticket went through, run it again
> from any of them, and fork it with a correction — without losing what happened.

---

## Read first

- [ ] LangGraph — [Time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel) · 15 min

---

## What you need to know

### The history is every checkpoint

`get_state_history` lists them, newest first: what was due next, the step number, the
checkpoint id. Each one is a config you can start from.

### Replay

`invoke(None, <a checkpoint's config>)` runs everything after that point again. The
model is called again and may say something different. The result is a new branch;
the thread's latest state is the new branch's end.

### Fork with a fix

The classifier sent a "where is my order" ticket to a person. Take the checkpoint just
after classify, write the right triage into it **as if classify had said it**
(`as_node="classify"`), and run on. The edge out of classify is taken again, with the
correction.

### Nothing is erased

The old branch is still in the history. That is the point: you can always show what
happened and what you changed.

---

## Exercises

```bash
pytest week-03/day-3 -v
```

Copy your day 1 files, then write `timetravel.py`. Try the same fork in Studio.

---

## Predict-then-run

After `fix_triage`, how many checkpoints in the history have `next == ("handoff",)`?

---

## Before you close the laptop

Commit, push, fill in the signal log.
