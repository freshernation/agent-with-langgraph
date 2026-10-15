# Day 1 — An eval set

> **By the end of today** you have an eval set made of tickets a person labelled and
> traces you labelled yourself, split once into dev and test, and in Langfuse.

---

## Read first

- [ ] Anthropic — [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) · 20 min
- [ ] Langfuse — [Datasets](https://langfuse.com/docs/evaluation/experiments/datasets) · 10 min

---

## What you need to know

### Real traces beat invented cases

The twenty tickets in `shop` are a start. The traces you made last week are better:
real wording, real mistakes. `label_traces.py` shows you each one and asks what it
really was; your answer becomes an item, and a human score on the trace.

### Split once, by a hash

Tune on **dev**. Look at **test** once, at the end. A random split changes every time
you run it, so your "held-out" set slowly leaks into your tuning. A hash of the id puts
each item on the same side forever.

### Check the set before trusting it

Duplicates count twice. An unknown kind is a typo. A kind with two examples tells you
nothing about that kind. `problems` says so before the numbers can mislead you.

---

## Exercises

```bash
pytest week-04/day-1 -v
python3 week-04/day-1/label_traces.py
python3 week-04/day-1/label_traces.py --push
```

Write `dataset.py`.

---

## Predict-then-run

How many of the twenty tickets land in test? Predict, then count.

---

## Before you close the laptop

Commit, push, fill in the signal log.
