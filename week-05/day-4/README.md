# Day 4 — Cost, latency, and breaking it

> **By the end of today** you know what a ticket costs and how long it takes, and you
> have broken Helpdesk on purpose and written up what happened.

---

## Read first

- [ ] Langfuse — [Token and cost tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking) · 10 min
- [ ] Google SRE — [Postmortem culture](https://sre.google/sre-book/postmortem-culture/) · 20 min

---

## What you need to know

### A ticket is the unit

A trace is one turn; a ticket is a session of turns. Customers care what a ticket
takes; you pay for what a ticket costs. Summarise both, and find the costliest.

### The 95th percentile

Nine fast tickets and one slow one average out fine. The 95th percentile does not.
That one customer is the one who writes in.

### Break it on purpose

Pick one: an invalid model key; kill the server while a refund is waiting; or the
longest ticket allowed, twenty times. Watch from the client and in Langfuse. Put it
right. Then write it up — blameless, with a timeline, and with what you changed.

---

## Exercises

```bash
pytest week-05/day-4 -v
python3 week-05/day-4/fetch_costs.py
```

Write `costs.py`, then break Helpdesk and write `INCIDENT.md`.

---

## Predict-then-run

Before `fetch_costs.py`: which kind of ticket is your costliest, and why?

---

## Before you close the laptop

Commit, push, fill in the signal log.
