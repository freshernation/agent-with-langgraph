# What this course does not teach

Every item below is real, and every one is out.

| Out | Why, and when to pick it up |
|---|---|
| **Multi-agent systems** — supervisors, swarms, handoffs | Only after one agent with good tools has measurably failed. Zero to Agent Engineer week 11 builds a team by hand |
| **Subgraphs** | One graph is enough to learn how LangGraph thinks. Subgraphs are the first thing to read afterwards |
| **Retrieval** — embeddings, vector stores | Retrieval Under Test is a whole course on it |
| **MCP** | Agent In Production, week 7 |
| **A public deployment, CI, alerts** | Agent In Production, weeks 5 and 6. Here the server runs on your machine |
| **LangSmith tracing and evals** | One tracing tool, properly — and the open-source one. Studio is used with LangSmith tracing off |
| **The hosted LangGraph Platform** | A paid plan. `langgraph dev` shows you its API for free |
| **LangChain beyond what LangGraph needs** — chains as a subject, its agent zoo, its retrievers | You use LangChain's models, messages and tools. The rest is another library |
| **Fine-tuning, front ends, Kubernetes** | Not what this course is about |

---

## Why

Each of these is learnable in about a week once you can build, trace and evaluate one
agent in a graph — and none of them teaches you to. Most of them add another layer
over the part you most need to understand.

People who know why something was cut stop worrying that they are missing it.

---

## The one that will be argued about

**No multi-agent.** Every framework's front page shows a team of agents, and it is
what most students think they are buying. A team is several prompts, several loops and
a handoff that loses information — and it is the answer only when one agent with good
tools has been measured and has failed. You will know how to measure that by week 4.

---

## What to add afterwards, in order

1. **Subgraphs**, then one multi-agent pattern — after you have a single agent's eval
   failing for a reason a second agent would fix.
2. **Running it for other people** — Agent In Production, if you have not taken it.
3. **Retrieval** as a tool in your graph — and episodes recalled by embeddings instead
   of word overlap.
4. **A second tracing tool**, to find out which of your habits were about the first.
