# Week 6 Milestone — Helpdesk that remembers

> Facts, past tickets and house rules in every ticket's prompt; a record of every
> ticket; and forgetting on request.

---

## The files

| File | Where it comes from |
|---|---|
| `classify.py`, `tools.py`, `durable.py`, `refunds.py` | **copy from your week 3 milestone** |
| `facts.py`, `stale.py`, `episodes.py`, `procedures.py` | **copy from this week's days** |
| `helpdesk.py` | your week 3 milestone's, with memory |
| `MEMORY.md` | new |

## `MEMORY.md`

| Section | What goes in it |
|---|---|
| What it remembers, and why | each kind, and what it is for |
| What it refuses to remember | and where that is enforced |
| How it forgets | and what it does not forget yet |
| What could go wrong | honestly |

---

## Check it

```bash
pytest week-06/milestone -v
```

## Friday

Two tickets from one customer, then "forget me".
