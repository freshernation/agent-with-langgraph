# Day 2 — Refunds need a human

> **By the end of today** Helpdesk can ask for a refund, stops and waits — for hours,
> through a restart — for a person to approve, reject or change it, and only then
> does anything happen.

---

## Read first

- [ ] LangGraph — [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) · 20 min

---

## What you need to know

### `interrupt()` stops the graph

Called inside a node — or a tool — it saves the thread and returns control to your
code, with a value saying what needs deciding. `Command(resume=decision)` carries on,
and `interrupt()` returns the decision.

### The node runs again from the top

When the graph resumes, the interrupted node starts again from its first line. Code
above the interrupt runs twice. So: checks above it, changes below it. Always.

### Do not wake a person for nothing

An order that is not theirs, or not delivered, is refused before the interrupt. A
person's time is the most expensive thing in this system.

### Approve, reject, edit

Three decisions. Edit is the one people forget: the person agrees to a refund, but not
that amount.

---

## Exercises

```bash
pytest week-03/day-2 -v
```

Copy your day 1 files, then write `refunds.py`.

---

## Predict-then-run

Put a `print("checking")` at the top of `request_refund`. Approve a refund. Predict
how many times it prints.

---

## Before you close the laptop

Commit, push, fill in the signal log.
