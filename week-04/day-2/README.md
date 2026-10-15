# Day 2 — Code evaluators

> **By the end of today** four evaluators check every case for free: the right kind,
> the right order, no prying into other customers' orders, and no refund without a
> person.

---

## Read first

- [ ] Hamel Husain — [Your AI product needs evals](https://hamel.dev/blog/posts/evals/) · 20 min

---

## What you need to know

### Check what a computer can check

Was it classified right? Was the order id right? Did any tool call ask about an order
that is not this customer's? Did any refund happen without a person seeing it first?
None of these needs a model to judge. They are exact, instant and free.

### The shape Langfuse calls

Every evaluator takes `input`, `output` and `expected_output` by keyword and returns an
`Evaluation`. The same function runs in your tests, in `run_local` on Thursday, and in
Langfuse's experiments — unchanged.

### Run a case like a customer would

`run_case` runs Helpdesk on one item, approves (or rejects) every refund it asks for,
and collects what happened: the triage, the reply, every tool call, every question to a
person, every refund. Evaluators read that, not the graph.

### Comment the failures

A 0 with "expected where, got refund" is something you can act on. A 0 alone is not.

---

## Exercises

```bash
pytest week-04/day-2 -v
```

Copy your week 3 milestone files, then write `evaluators.py`.

---

## Predict-then-run

Run T13 — the ticket with an instruction in it — through `run_case` with a real model.
Which evaluators fail?

---

## Before you close the laptop

Commit, push, fill in the signal log.
