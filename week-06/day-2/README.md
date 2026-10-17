# Day 2 — Facts go stale

> **By the end of today** a changed fact replaces the old one without losing it, the
> prompt carries only the freshest few, and a customer can ask to be forgotten.

---

## Read first

- [ ] Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), the section on memory · 15 min
- [ ] ICO — [Right to erasure](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/), the first section · 10 min

---

## What you need to know

### Replace, but keep the history

"Moving to Leeds" replaces "lives in Bristol" — but the old address is not wrong, it is
old. Keep it, dated, in the fact's history. The prompt only ever shows the current one.

### Five facts, not fifty

Everything in the prompt is paid for on every model call, and the model attends less to
each thing as the list grows. Newest first, capped.

### Forgetting is a feature

A customer may ask you to forget them, and in many places the law says you must. Delete
their facts — only theirs — and say how many.

---

## Exercises

```bash
pytest week-06/day-2 -v
```

Copy `tools.py` and `facts.py`, then write `stale.py`.

---

## Predict-then-run

Update the same topic three times. Predict the length of its history, then check.

---

## Before you close the laptop

Commit, push, fill in the signal log.
