# Week 5 — Project 2 defence

Fifty minutes. **Live: `docker compose up`, then curl.**

---

## Phase 0 — Run it (10 min)

They start it with compose and send a refund ticket with `curl -N`. The words stream.
It stops for approval. **You run `docker compose restart api`.** They approve with
curl. One refund.

## Phase 1 — Explain (10 min)

1. *"Why does only the draft's text reach the customer, and where is that decided?"*
2. *"Why is the checkpointer async here and not on week 3?"*
3. *"What changes to move this to Postgres?"* — one setting, plus `setup()`. Then:
   *"why would you?"* — more than one server process.
4. *"The customer id comes from the request body. What is wrong with that?"*
5. *"What is your p95, and which node is it spent in?"*

## Phase 2 — The incident (10 min)

Read `INCIDENT.md` aloud. Is it blameless? Is there a timeline with times? What did
they change, and did they break it again to prove the change worked?

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `tokens` without the node filter | The classifier's form streams to the customer |
| Medium | the Dockerfile copies the code before `pip install` | Every change rebuilds everything |
| Medium | `serde` left off the async saver | A warning on every read — can they find what it means? |
| Nasty | the decision route does not check that something is waiting | A stray approve starts a new run with `None` as its input |

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Run it** | Streams, survives the restart, one refund | Works with a nudge | Does not start |
| **Explain** | Knows where every byte the customer sees comes from | Most | Cannot say |
| **Incident** | Blameless, timed, change re-tested | Clear, not re-tested | A story |
| **Debug** | Suspects the unchecked decision | Finds it | Guesses |

Project 2 passes with **3 or more in every phase**.

---

## Instructor: framing week 6

> **Next week Helpdesk remembers.** Facts about a customer that outlive a ticket, what
> happened last time, and house rules only staff may write — and how it forgets.
