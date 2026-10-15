# Week 3 Milestone — Project 1: Helpdesk, durable and supervised

> Helpdesk refunds only with a person's approval, survives a restart at any point,
> and can be rewound.

---

## The files

| File | Where it comes from |
|---|---|
| `classify.py`, `tools.py`, `durable.py`, `refunds.py`, `timetravel.py`, `sessions.py` | **copy from this week's days** |
| `helpdesk.py` | day 1's, with refunds, a new draft prompt, and `decide` |
| `run_desk.py` | given — Helpdesk in your terminal, with you approving refunds |
| `APPROVAL.md` | new |

## Run it

```bash
cd week-03/milestone
python3 run_desk.py c1 T02
```

Ask for a refund on A1001. Approve it. Then do it again on another ticket and press
Ctrl-C at the approval prompt; start it again with the same arguments.

## `APPROVAL.md`

| Section | What goes in it |
|---|---|
| What a person sees | and what they do not |
| What happens on yes, no and edit | where the money moves, and where it does not |
| What runs twice | and why that is safe |
| What happens on a restart | what was saved, what runs again |

---

## Check it

```bash
pytest week-03/milestone -v
```

## Friday

The defence starts with your instructor pressing Ctrl-C.
