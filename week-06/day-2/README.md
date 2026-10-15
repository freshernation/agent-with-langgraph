# Days 2 and 3 — Build it, test it, measure it

> **By the end of Wednesday** your agent runs, has at least five offline tests of its
> own, a labelled eval set of ten or more, and a report of how it scored.

---

## What you need to know

### It lives in `project/`

`graph.py` with `build_graph(model, checkpointer=None)`, your tests beside it, and
`evals.py`. Today's tests check the shape and run **your** tests; what the agent does
is yours.

### Tests first, offline

Every test uses `ScriptedModel`. Test the behaviour you would be most embarrassed to get
wrong — usually the one that needs a person.

### Trace it into its own sessions

When you run it for real, give each run a session named `project/<something>`, so
`check_traces.py week-06` can find them and your portfolio can show them.

### Evaluate, then fix one thing

On Wednesday run your evals with a real model, find what fails, fix one thing — in
code if you can, not only in the prompt — and run them again. `EVAL_REPORT.md` is that
story, with the numbers.

---

## Exercises

```bash
pytest week-06/day-2 -v      # Tuesday: the agent and its tests
pytest week-06/day-3 -v      # Wednesday: the evals and the report
python3 check_traces.py week-06
```

---

## Before you close the laptop

Commit, push, fill in the signal log.
