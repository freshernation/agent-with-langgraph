# Week 4 — Friday defence

Forty minutes. **Defend one eval: what it catches, and what it misses.**

---

## Phase 0 — The gate (5 min)

They run `run_evals.py` with their real model. It must exit 1 on the bad prompt and
name the tickets that newly fail.

## Phase 1 — Explain (10 min)

1. *"Why does the split use a hash, not `random`?"*
2. *"`own_orders_only` fails when the tool refused anyway. Why count it?"*
3. *"Your judge agrees 90% of the time. Is that good?"* — not without kappa; ask them to
   compute it on a judge that says "good" to everything.
4. *"Which is worse in a judge, a false pass or a false fail — for Helpdesk?"*
5. *"The prompt store is down. What does Helpdesk use?"*

## Phase 2 — Choose one eval and defend it (10 min)

They pick one evaluator. You propose three runs: one it should catch, one it should
miss, and one that is fine but it fails. Ask them to predict each before you run it.
Use the editor's red-team list from `ai/editor.md` if they have one.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `split` uses `random.random()` | The dev set changes every run — can they see why that matters? |
| Medium | `gate` compares `>` the wrong way | Improvements fail, regressions pass |
| Medium | `agreement` counts undecided as agreement | A judge that never answers looks perfect |
| Nasty | `run_case` resumes with `"approve"` and `approval_before_refund` checks only that refunds exist | Every refund looks approved, including ones nobody saw |

The **Nasty** one: an eval that can never fail is worse than none, because it looks
like a guarantee.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Gate** | Exits 1, names the tickets | Exits 1 | Passes the bad prompt |
| **Explain** | Explains kappa with the always-yes judge | Knows what it is | Quotes agreement alone |
| **One eval** | Predicts all three runs | Two | Believes it catches everything |
| **Debug** | Suspects the eval that cannot fail | Finds it | Guesses |

---

## Instructor: framing week 5

> **Next week Helpdesk leaves your terminal.** It goes behind an HTTP server that
> streams the reply as it is written, on a checkpointer that survives a restart, in a
> container — and you break it on purpose and write up what happened.
