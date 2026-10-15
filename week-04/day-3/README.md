# Day 3 — A judge, checked against people

> **By the end of today** a model judges whether a reply is good — and you know how
> often it agrees with a person, corrected for luck, before you let it count.

---

## Read first

- [ ] Langfuse — [LLM-as-a-judge](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge) · 15 min
- [ ] Wikipedia — [Cohen's kappa](https://en.wikipedia.org/wiki/Cohen%27s_kappa), the definition and the first example · 10 min

---

## What you need to know

### Some things need judgement

"Does this reply promise something the facts do not show?" A computer cannot check
that. A model can — sometimes. So the judge is a second model with a rubric, filling
in a `Verdict`.

### A judge is a classifier, so measure it

`labels.json` has twelve replies a person marked good or bad. Run the judge on them
and compare. **Agreement alone lies**: when most replies are good, a judge that says
"good" to everything agrees most of the time and knows nothing. Kappa subtracts the
agreement you would get by luck.

### False passes are the dangerous ones

A judge that fails a good reply wastes your time. One that passes a bad reply hides it.
For Helpdesk, `trustworthy` allows no false passes.

### "Could not decide" is its own answer

Not good, not bad. Leave it out of agreement — and do not trust a judge that leaves
things undecided.

---

## Exercises

```bash
pytest week-04/day-3 -v
python3 week-04/day-3/run_judge.py
```

Write `judge.py`.

---

## Predict-then-run

Before `run_judge.py`: which of the twelve will your judge get wrong?

---

## Before you close the laptop

Commit, push, fill in the signal log.
