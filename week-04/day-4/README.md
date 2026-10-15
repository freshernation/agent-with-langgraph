# Day 4 — Experiments and a gate

> **By the end of today** a prompt lives in Langfuse with a label, an experiment
> compares two prompts on the same items, and a gate says whether the new one may
> ship.

---

## Read first

- [ ] Langfuse — [Prompt management](https://langfuse.com/docs/prompt-management/overview) · 15 min
- [ ] Langfuse — [Experiments via the SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk) · 15 min

---

## What you need to know

### An experiment is the same items, a different setting

Same dataset, same evaluators, one thing changed — here, the classifier's prompt.
`run_local` does on your machine what `run_experiment` does in Langfuse, so you can
test the harness with no network and then run it for real.

### A gate turns numbers into yes or no

For every score the baseline had: is the candidate's lower, by more than the
tolerance? Then it does not ship. A score that disappeared is a regression too.

### Prompts with labels

In Langfuse a prompt has versions, and a label — `production` — says which one is live.
Changing the label changes the prompt without a deploy. So `load_prompt` asks for the
production one, and **falls back to the prompt in your code** if Langfuse cannot be
reached. Helpdesk must never stop because a prompt store is down.

---

## Exercises

```bash
pytest week-04/day-4 -v
python3 week-04/day-4/push_prompt.py --push --experiment
```

Copy `dataset.py`, `evaluators.py` and `classify.py` (with one new argument), then
write `experiment.py`.

---

## Predict-then-run

Edit the production prompt in Langfuse to remove "never guess". Predict which tickets
newly fail, then run the experiment again.

---

## Before you close the laptop

Commit, push, fill in the signal log.
