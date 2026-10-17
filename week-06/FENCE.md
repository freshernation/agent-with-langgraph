# Week 6 — Concept fence

## Allowed

**Everything from weeks 1 to 5**, plus:

- LangGraph's store: `SqliteStore`, `InMemoryStore`, namespaces, `put`, `get`,
  `search`, `delete`, `setup()`
- `compile(store=...)`; `ToolRuntime` in a tool; `Runtime` and `RunnableConfig` in a node
- Ranking by word overlap, by hand

## Not yet

Embeddings and the store's semantic index — read about, not graded · memory shared
between different agents · deleting old episodes on a schedule · encrypting memory

---

## Why recall by word overlap

The store can rank by embeddings, and in production you might let it. But an embedding
is another model, another key and another bill, and it hides why something was
recalled. Word overlap, by hand, shows you exactly what "relevant" means — and the
week 4 evals can tell you when it is not good enough.
