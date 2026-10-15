# Day 2 — A streaming server

> **By the end of today** Helpdesk is an HTTP service: a ticket's reply streams to the
> client word by word, and a person approves refunds with a request.

---

## Read first

- [ ] FastAPI — [Custom response](https://fastapi.tiangolo.com/advanced/custom-response/), "StreamingResponse" · 10 min
- [ ] MDN — [Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) · 15 min

---

## What you need to know

### Server-sent events

A response that stays open and sends `event:` and `data:` lines as things happen.
Browsers understand it natively; `curl -N` shows it. Each event's data is JSON, so a
newline in a token cannot break the stream.

### A lifespan holds the checkpointer

The server opens its checkpointer once, at start-up, and closes it at shutdown. A
lifespan is where that goes; the graph lives on `app.state`.

### Three routes, one thread per ticket

Send a message, read a ticket's status, decide a refund. The decision route refuses
when nothing is waiting, and an edit with no amount — before the graph is touched.

### LangGraph has a server too

`langgraph dev` serves any graph with a generic API. Compare it with yours in `API.md`:
what it gives you for free, and what only your own routes can say.

---

## Exercises

```bash
pytest week-05/day-2 -v
```

Copy your files, then write `server.py` and `API.md`.

---

## Predict-then-run

Approve a ticket that is not waiting. Predict the status code, then send it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
