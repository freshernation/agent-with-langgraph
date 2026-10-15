# Week 2 — Friday defence

Forty minutes. It starts with the state.

---

## Phase 0 — The state (5 min)

*"Read me your `Help` state, key by key. For each one: who writes it, who reads it."*
Any key nobody reads is a finding.

## Phase 1 — Explain (10 min)

1. *"Three nodes write `notes` in the same step. What happens with no reducer, and
   why does LangGraph refuse instead of picking one?"*
2. *"The model answered in words instead of filling the form. What does your code
   do, and what does the customer see?"*
3. *"Where does `customer` come from, and could a ticket change it?"* — the best
   question of the week. The answer is the injected state.
4. *"Why does `order_details` say the same thing for 'not yours' and 'does not
   exist'?"*
5. *"A 400 from the provider — does your retry policy retry it?"* Make them check
   what the default retries.

## Phase 2 — Mutate (10 min)

- *"Add a fifth kind: complaint, which goes straight to a person."* Which lines change
  — the form, the route, the report?
- *"The backup model is cheaper and worse. Use it only for drafting."* Where does that
  change go?

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `order_id` pattern removed | T05 gets a guessed order and nothing complains |
| Medium | `customer` passed as a tool argument instead of injected | The model can read anyone's orders. Ask them to prove it with a ticket |
| Medium | `with_fallbacks` before `bind_tools` | Fails at once — can they read why? |
| Nasty | `after_classify` sends `other` to lookup | Every password question costs three model calls and gets a made-up answer |

The **Nasty** one: nothing errors, and every reply still reads well.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **State** | Every key justified by a reader | Most | Cannot say who reads what |
| **Explain** | Explains the injected customer unprompted | With a hint | Recites |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the route | Finds it | Guesses |

---

## Instructor: framing week 3

> **Next week Helpdesk can refund — but only after a person says yes.** To stop and
> wait for a person, a graph has to save exactly where it was. That is a checkpointer,
> and once you have one you can also go back in time.
