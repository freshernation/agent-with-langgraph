# Week 1 — Friday defence

Forty minutes. It starts with a drawing.

---

## Phase 0 — Draw it (5 min)

Before they open the code: *"Draw your Desk graph. Every node, every edge, and what
is in the state after each step of a turn that adds one note."* Then compare the
drawing to `get_graph().draw_mermaid()`.

## Phase 1 — Explain (10 min)

1. *"Where is the loop?"* — the edge from tools back to model. Then: *"where was it
   in the hand-written Desk?"*
2. *"`call_model` returns one message, but the state ends up with all of them. Why?"*
   — `MessagesState`'s reducer appends. This is the best question of the week.
3. *"What does `recursion_limit` count, and what did your hand-written Desk count
   instead?"*
4. *"Your parity check found a difference. Which, and why?"*
5. *"Where do the user and session in Langfuse come from?"*

## Phase 2 — Mutate (10 min)

- *"A tool call for a tool that does not exist. What does your graph do? What does
  `create_agent` do?"* Make them find out, not guess.
- *"Add the repeat guard back."* Where does it go — a node, the route, the tool node?
  Each works; the defence is in the reason.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `call_model` returns the whole message list plus the reply | Every message doubles. Do they see the reducer? |
| Medium | `route` returns `"tool"` | A clear error at compile time — can they read it? |
| Medium | the `@tool` docstring removed | Fails loudly; ask why a description is required |
| Nasty | `tools -> END` instead of `tools -> model` | The tool runs, the answer is the tool's raw output, and nothing errors |

The **Nasty** one: the graph "works", and the model never sees its tool result.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Draw** | Drawing matches the graph, state right at every step | Shape right, state vague | Cannot draw it |
| **Explain** | Explains the reducer unprompted | Gets there with a hint | Recites |
| **Mutate** | Finds out by running, and argues where the guard goes | Gets it working | Guesses |
| **Debug** | Suspects the edge | Finds it | Guesses |

---

## Instructor: framing week 2

> **Next week, a new agent.** Helpdesk answers customers about their orders. Before it
> can do anything, you decide what it remembers — the state — and that decision shapes
> everything after it.
