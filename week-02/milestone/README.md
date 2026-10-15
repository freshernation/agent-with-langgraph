# Week 2 Milestone — Helpdesk, version one

> Helpdesk answers a ticket end to end, and you know how often it sorts tickets
> right.

---

## The files

| File | Where it comes from |
|---|---|
| `classify.py`, `tools.py`, `helpdesk.py` | **copy from this week's days** |
| `triage_report.py` | new |
| `run_tickets.py` | given |
| `GRAPH.md` | new |

## `triage_report.py`

Classify every labelled ticket and count how many match the person's label — kind
and order both. Run it on the twenty in `shop.TICKETS` with your real model:

```bash
python3 week-02/milestone/run_tickets.py
```

## `GRAPH.md`

| Section | What goes in it |
|---|---|
| Why these nodes | each node, and what would break without it |
| Why this state | each key, and who reads it |
| What I kept out of the state | and why |
| What the triage report says | your numbers, and the tickets it got wrong |

---

## Check it

```bash
pytest week-02/milestone -v
```

## Friday

The defence starts with your state, key by key.
