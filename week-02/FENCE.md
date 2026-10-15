# Week 2 — Concept fence

## Allowed

**Everything from week 1**, plus:

- `Annotated`, `operator.add`, a reducer function you write, `add_messages`
- Parallel nodes; `InvalidUpdateError`
- Pydantic `BaseModel`, `Field`, `Literal`, `ValidationError`
- `with_structured_output`
- `InjectedState`, `ToolNode`, `tools_condition`
- `RetryPolicy`, `with_fallbacks`

## Not yet

Checkpointers, threads, `interrupt`, `Command` (week 3) · a refund tool (week 3) ·
datasets, scores, a judge (week 4) · `async` and streaming (week 5) · `Send` and
map-reduce · subgraphs

---

## Why no refund tool yet

A tool that moves money needs a person to say yes first, and a graph can only stop
and wait for a person once it can save where it was. That is next week. Until then
Helpdesk drafts — "a person will review your refund" — and nothing more.
