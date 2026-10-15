# Week 3 — Project 1 defence

Fifty minutes. **Live, in the terminal.**

---

## Phase 0 — Kill it (10 min)

They run `run_desk.py` with a real model and send a refund ticket. When the approval
prompt appears, **you press Ctrl-C**. They start it again with the same arguments.
It must ask the same question, and one approval must make one refund.

## Phase 1 — Explain (10 min)

1. *"What is in `desk.db` right now, and how much of it would you need to rebuild
   this ticket?"*
2. *"Point at the line that runs twice when the graph resumes."* — the top of
   `request_refund`. Then: *"what would happen if the refund came first?"*
3. *"Why are an order that is not theirs and an undelivered order refused before the
   interrupt?"*
4. *"After `fix_triage`, where is the old handoff?"* — still in the history; a fork adds.
5. *"How do you get from a session in Langfuse to the saved thread?"* — the same string.

## Phase 2 — Mutate (10 min)

- *"Refunds under five dollars need no approval."* Where does that go — and does
  anything still run twice?
- *"The person wants to see the ticket text, not just the reason."* What changes in the
  interrupt's value, and is anything sensitive now shown?

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | the graph compiled without the checkpointer | `interrupt` fails at once — can they read why? |
| Medium | `config_for` uses only the customer as thread id | Two tickets share one conversation |
| Medium | `answer` returns `result["reply"]` while waiting | The customer is shown the previous ticket's reply |
| Nasty | `shop.refund` moved above `interrupt()` | Approve once, refunded twice; reject, refunded anyway |

The **Nasty** one is the lesson of the week.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Kill it** | Same question after restart, one refund | Resumes with a nudge | Starts over or refunds twice |
| **Explain** | Points at the line that runs twice unprompted | With a hint | Cannot say what is saved |
| **Mutate** | Names every line, sees what runs twice | Gets there | Cannot place it |
| **Debug** | Suspects the order of lines | Finds it | Guesses |

Project 1 passes with **3 or more in every phase**.

---

## Instructor: framing week 4

> **Next week you find out whether Helpdesk is any good.** Not by reading replies —
> by building an eval set from the traces you have been collecting, and a gate that
> fails a bad prompt change before anyone sees it.
