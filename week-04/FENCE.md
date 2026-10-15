# Week 4 — Concept fence

## Allowed

**Everything from weeks 1 to 3**, plus:

- `hashlib.sha256` for a stable split
- Langfuse: datasets and dataset items, scores, `Evaluation`, `run_experiment`,
  prompts with labels and a fallback
- Agreement, false passes and false fails, Cohen's kappa
- A model judge with structured output

## Not yet

`async` and streaming (week 5) · a server (week 5) · running evals in CI — Agent In
Production does that · generating test cases with a model · LangSmith evals

---

## Why only code evaluators gate

The four code evaluators are exact and free, so a drop in any of them is a fact. A
judge's verdict is an opinion with an error rate — this week you measure that rate.
It is a warning until you trust it, and the gate stays on facts.
