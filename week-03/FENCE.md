# Week 3 — Concept fence

## Allowed

**Everything from weeks 1 and 2**, plus:

- `SqliteSaver`, threads and `thread_id`
- `get_state`, `.next`, `.values`, `.interrupts`, `get_state_history`, checkpoint ids
- `interrupt()`, `Command(resume=...)`
- `invoke(None, config)` to resume or replay
- `update_state(..., as_node=...)` to fork
- Langfuse sessions and users through metadata; reading traces back with the API

## Not yet

Datasets, scores, a judge (week 4) · `async`, streaming, a server (week 5) · the
Postgres checkpointer (week 5) · the long-term store · `interrupt_before` on compile —
read about it, use `interrupt()` inside the node

---

## Why `interrupt()` inside the tool

You could stop before the whole tools node with `interrupt_before`. Then every tool —
`tracking` too — waits for a person. Putting the interrupt inside `request_refund`
stops only for the one action that moves money, and only after the checks that make
the request worth a person's time.
