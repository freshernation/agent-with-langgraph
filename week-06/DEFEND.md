# Week 6 — Project 3: the mock interview

Sixty minutes. You are the interviewer. **Fair, senior, not easily impressed.**

---

## Part 1 — System design (25 min)

At a whiteboard: *"Design your agent as if starting again."* The state first, then the
nodes, where a person comes in, what is checkpointed. Then change the requirements
twice:

- *"Ten times the traffic."* — looking for what actually breaks: the checkpointer's
  database, the model's rate limit, cost — not "add Kubernetes".
- *"A regulator needs every decision explained."* — looking for traces, the
  checkpoint history, and what is missing from both.

Push on every choice: *"why a node and not a tool?"*, *"what is in the state that
nobody reads?"*

## Part 2 — Debug a trace (20 min)

Describe a trace from **their** agent that went wrong, in words: the spans in order,
inputs, outputs, durations, tokens. Pick one real cause: a reducer that drops
messages, a route that loops, a tool given the wrong argument, an approval skipped on
a resumed thread. Answer only what they ask. Score where they look first.

## Part 3 — Judgement (15 min)

1. *"Half the time. What do you cut?"*
2. *"Which of your evals do you trust least, and why?"*
3. *"What would you do differently with LangGraph if you started again?"*

---

## Scoring

| Part | 5 | 3 | 1 |
|---|---|---|---|
| **Design** | State first, every choice reasoned, both changes handled | Sound shape, thin reasons | Cannot redraw their own agent |
| **Debug** | Starts at the decision that went wrong, finds it fast | Finds it by reading everything | Guesses |
| **Judgement** | Cuts decisively, distrusts the right eval | Reasonable | "It depends" |

Project 3 passes with **3 or more in every part**. Tell them the result and the one
thing that would have made it a 5.
