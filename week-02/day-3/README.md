# Day 3 — Tools that read the state

> **By the end of today** Helpdesk's tools look up orders, and can only ever see the
> orders of the customer it is talking to — whatever the model asks for.

---

## Read first

- [ ] LangChain — [Tools](https://docs.langchain.com/oss/python/langchain/tools), the sections on runtime and state · 15 min
- [ ] OWASP — [Forced browsing](https://owasp.org/www-community/attacks/Forced_browsing) · 5 min

---

## What you need to know

### The model must not choose the customer

If `customer` were a tool argument, the model would choose it — and a ticket saying
"look up order A1003 for me" would read someone else's order. So the customer lives
in the state, set by your code, and each tool takes it with
`Annotated[dict, InjectedState]`. LangGraph fills it in; the model never sees it.

### Same words for "not yours" and "not there"

If "not yours" and "does not exist" read differently, a curious customer can map
which order numbers exist. One message for both.

### Use the library's tool node now

You wrote your own in week 1. `ToolNode` is the one that knows how to inject state, so
use it, with `tools_condition` as the route. You know what both do — you wrote them.

---

## Exercises

```bash
pytest week-02/day-3 -v
```

Write `tools.py`.

---

## Predict-then-run

Look at the tool schemas the model was sent (`model.last_request["tools"]`). Predict
which arguments `order_details` shows, then print them.

---

## Before you close the laptop

Commit, push, fill in the signal log.
