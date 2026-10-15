# Day 2 — A form the model must fill in

> **By the end of today** a model sorts a ticket into a typed form you can check, and
> your code copes — honestly — when it will not.

---

## Read first

- [ ] LangChain — [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output) · 15 min
- [ ] Pydantic — [Fields](https://docs.pydantic.dev/latest/concepts/fields/), up to "Validation" · 10 min

---

## What you need to know

### A schema is a contract

`Triage` says exactly what the answer must be: one of four kinds, an order id that
looks like one or nothing, a yes or no. `with_structured_output(Triage)` hands the
model the schema as a tool it must call, and turns the call back into a `Triage`.

### Two ways it fails

The model fills the form in wrong — a kind of "banana", an order id of "order 12" —
and Pydantic raises. Or it answers in words and fills in nothing, and you get `None`.
Both happen with real models; both are tested.

### Then what?

Try again, a set number of times. Then a **fallback**: a ticket nobody could classify
goes to a person. Never invent a classification to keep the pipeline moving.

### Never guess an order id

The pattern on `order_id` refuses nonsense, but it cannot refuse a real-looking guess.
The instructions say: copy it from the ticket, or leave it empty. Your milestone
measures whether the model listened.

---

## Exercises

```bash
pytest week-02/day-2 -v
```

Write `classify.py`.

---

## Predict-then-run

With a real model, classify T13 — the ticket with an instruction inside it. Predict
the kind, then run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
