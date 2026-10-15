# Week 5 — Ship it

> **Destination**
> Helpdesk behind an HTTP server that streams the reply as it is written, on a
> checkpointer that survives a restart and can be Postgres with one setting, in a
> container — and you have broken it on purpose and written up what happened.

**Project 2.** This week it stops being a script you run and becomes a service a
front end could talk to.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Stream a graph with `async`: the steps, the reply's words, the questions for a person |
| Tue | `day-2/` | Serve Helpdesk over HTTP with server-sent events, and compare with LangGraph's own server |
| Wed | `day-3/` | Choose the checkpointer by a setting, and run it all in a container |
| Thu | `day-4/` | Read cost and latency from Langfuse, break the service, write the incident |
| Fri | `milestone/` | **Project 2** — streaming, durable, traced, in a container |

---

## The rule from this week on

**The customer sees only the reply.** Not the classifier's form, not a tool's raw
result, not the lookup's working. Stream the draft's words and nothing else.

---

## Before Monday

Docker running on your machine (`SETUP.md` step 7).

---

## Outside-view question

> *A kitchen's pass is where plates wait to go out. What happens there when the
> kitchen is overwhelmed?*
