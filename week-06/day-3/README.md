# Day 3 — What happened last time

> **By the end of today** every finished ticket leaves a one-line record, and a new
> ticket is told about the earlier ones that matter to it.

---

## Read first

- [ ] Sumers et al. — [Cognitive architectures for language agents](https://arxiv.org/abs/2309.02427), section 4.1 on memory · 20 min

---

## What you need to know

### An episode is a record, not a transcript

Not the whole conversation — one line: what was asked, what happened, which order. A
model writes it, as a form, at the end of the ticket. Plain facts, never an opinion
about the customer: whatever it writes follows them around.

### Recall by relevance, by hand

A customer with forty tickets does not need all forty in the prompt. Rank them by the
words they share with the new ticket, newest first on a tie, and keep the top three.
That is retrieval, written in twenty lines — and you can see exactly why something was
recalled.

### The store could do this for you

`InMemoryStore(index=...)` ranks by embeddings. Better at synonyms, worse at explaining
itself, and one more model to pay for. Measure before you switch.

---

## Exercises

```bash
pytest week-06/day-3 -v
```

Copy `tools.py` and `facts.py`, then write `episodes.py`.

---

## Predict-then-run

"My new kettle is broken too." Which of three earlier tickets is recalled? Write it
down, then run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
