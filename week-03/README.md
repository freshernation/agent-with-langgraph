# Week 3 — Memory and a human

> **Destination**
> Helpdesk survives being killed in the middle of a ticket, stops and waits for a
> person before it refunds anyone, and can be taken back to before a mistake and run
> again — and you can follow one customer's tickets in Langfuse.

**Project 1.** Everything this week is one idea: a graph that saves where it was.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Save every step of every ticket, and carry on after a crash |
| Tue | `day-2/` | Stop for a person before a refund, and resume on their decision |
| Wed | `day-3/` | Read a thread's history, replay from a step, and fork with a fix |
| Thu | `day-4/` | Follow one customer across their tickets in Langfuse |
| Fri | `milestone/` | **Project 1** — Helpdesk that refunds only with approval, through a restart |

---

## The rule from this week on

**Nothing before an `interrupt()` may change anything.** When the graph resumes, the
node runs again from its first line. A refund above the interrupt is a refund paid
twice.

---

## Before Monday

Nothing new. You will run `run_desk.py` on Friday with a real model — check your key
works.

---

## Outside-view question

> *A bank cheque over a limit needs a second signature. Who signs, what do they see,
> and what happens if they say no?*
