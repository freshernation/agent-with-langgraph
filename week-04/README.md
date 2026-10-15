# Week 4 — Measure it

> **Destination**
> An eval set built from labelled tickets and your own traces, code evaluators that
> check what a computer can check, a model judge you have tested against people, and
> a gate that fails a bad prompt change before anyone sees it.

Three weeks of building. This week you find out whether any of it is good.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Build an eval set from labelled tickets and real traces, and split it once |
| Tue | `day-2/` | Write evaluators for the route, the order, the tools, and approval before refunds |
| Wed | `day-3/` | Use a model as a judge — after measuring how often it agrees with a person |
| Thu | `day-4/` | Keep prompts in Langfuse, run experiments, and gate a change on the result |
| Fri | `milestone/` | An eval suite that fails a deliberately bad prompt |

---

## The rule from this week on

**No prompt change without a run.** Every change to a prompt goes through the gate on
the dev split. The test split is touched once, at the end of the course.

---

## Before Monday

Run `run_tickets.py` from your week 2 milestone and `run_desk.py` from week 3 a few
times with a real model, so you have traces of your own to label.

---

## Outside-view question

> *A restaurant inspector does not eat every dish. How do they decide the kitchen is
> safe?*
