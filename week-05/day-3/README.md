# Day 3 — Durable, and in a container

> **By the end of today** the checkpointer is chosen by `DATABASE_URL` — SQLite or
> Postgres — and Helpdesk runs in a container with its data on a volume.

---

## Read first

- [ ] LangGraph — [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), the checkpointer libraries · 10 min
- [ ] Docker — [Building best practices](https://docs.docker.com/build/building/best-practices/) · 15 min

---

## What you need to know

### A setting, not a code change

`sqlite:///helpdesk.db` on your laptop; `postgresql://...` when there is more than one
server process. The code that builds the graph does not change. Import the Postgres
saver only on that branch, so nobody using SQLite needs the driver.

### When SQLite stops being enough

One process writing one file is SQLite's sweet spot. Two server processes, or two
machines, need a database that is shared: Postgres. `compose.yaml` has it under a
profile — the deep track.

### The container

Requirements before code, so a code change does not reinstall everything. A user that
is not root. The data on a named volume, so `docker compose down` and `up` keep every
ticket. Secrets from the environment, never written in the file.

---

## Exercises

```bash
pytest week-05/day-3 -v
```

Copy `durable.py`, write `checkpoints.py`, the `Dockerfile`, `compose.yaml` and
`.dockerignore`.

---

## Predict-then-run

Deep track: `docker compose --profile postgres up`, point `DATABASE_URL` at it, and
send a refund ticket. Predict which tables appear in Postgres.

---

## Before you close the laptop

Commit, push, fill in the signal log.
