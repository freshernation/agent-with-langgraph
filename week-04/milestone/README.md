# Week 4 Milestone — An eval suite that says no

> A prompt change that makes Helpdesk worse is caught, by name, before anyone sees it.

---

## The files

| File | Where it comes from |
|---|---|
| `dataset.py`, `evaluators.py`, `judge.py`, `experiment.py`, `classify.py` | **copy from this week's days** |
| `evals.py` | new |
| `run_evals.py` | given |
| `EVALS.md` | new |

## Run it

```bash
cd week-04/milestone
python3 run_evals.py            # your prompt against a deliberately bad one: exits 1
python3 run_evals.py mine.txt   # against a prompt you wrote
```

## `EVALS.md`

| Section | What goes in it |
|---|---|
| What the suite checks | each evaluator, and the dataset |
| What it misses | honestly |
| The judge, and whether I trust it | your kappa and false passes |
| The bad change it caught | which tickets, and how you knew |

---

## Check it

```bash
pytest week-04/milestone -v
```

## Friday

You defend one eval: what it catches, and what it misses.
