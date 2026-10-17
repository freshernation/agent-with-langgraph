# Agent With LangGraph

Seven weeks from the loop you wrote to a graph you can defend in an interview.

You wrote an AI agent by hand: the loop, its tools, a gate in front of anything
dangerous, memory and evals. This course rebuilds it in **LangGraph**, so the
framework is a translation of something you already understand — then uses it to build
what is hard to build by hand: typed state, an agent that survives a restart, a human
approval step, rewinding to an earlier step, memory that lasts. Every run is traced and evaluated in
**Langfuse**. In the last week you build an agent for a problem you chose, and defend
it in a mock interview.

---

## Who this is for

You have finished **Agent From Zero**, or you can do what its final project asks:
build an agent with tools and evals, with no framework, and explain every line.

You do not need to know type hints, decorators or `async` yet. Each arrives in the
week that needs it. Before week 1 you run a short baseline interview so that you, and
your instructor, know which to watch.

---

## The rules

**1. The twenty-minute rule.** Stuck for twenty minutes: open the tutor. Still stuck:
bring it to the live hour. Log every stuck moment in `logs/stuck-log.md`.

**2. You may not commit a line you could not have written and cannot explain on
Friday.**

**3. Nothing counts until the tests pass and it is pushed.**

**4. Draw the graph before you write it.** Nodes, edges, and what the state holds at
each step — on paper first.

---

## The seven weeks

| Week | | Milestone |
|---|---|---|
| 1 | You already wrote this | Desk as a graph, behaving like the one you wrote; both traced side by side |
| 2 | State | Helpdesk classifies a support ticket, looks up the order and drafts a reply |
| 3 | Memory and a human | **Project 1** — survives a restart mid-ticket, stops for approval before a refund, can be rewound |
| 4 | Measure it | An eval suite built from real traces that fails a bad prompt change |
| 5 | Ship it | **Project 2** — streaming over HTTP on a durable checkpointer, with an incident write-up |
| 6 | Memory that lasts | Helpdesk remembers facts, past tickets and house rules — and forgets on request |
| 7 | Your agent, and the interview | **Project 3** — an agent for a problem you chose, a portfolio page, a mock interview |

Every test runs offline against a scripted model — no key, no cost. A Langfuse
account is needed from day 1 and a real model key from week 1 day 4.

---

## How a week works

| | |
|---|---|
| **Monday to Thursday** | One live hour, then the day's folder: read, build, make the tests pass |
| **Friday** | No new content. Ship the milestone, then defend it |

Each day folder has a `README.md`, the files to write, and a test file that fails until
you have written them. Run the day's tests with `pytest week-NN/day-N -v`.

---

## What is in the repo

| Path | What it is |
|---|---|
| `desk/`, `llm/` | Desk, the agent you wrote by hand, and its model layer — for week 1's comparison |
| `models/` | The LangChain model layer: Claude, OpenAI, or the scripted model every test uses |
| `week-01/` … | One folder per week |
| `ai/` | The AI roles. Read `ai/README.md` first |
| `logs/` | Your baseline, your stuck log and your signal log |
| `shop/` | Helpdesk's world: customers, orders, labelled tickets, refunds |
| `check_traces.py` | Checks your Langfuse project has each week's work |
| `SETUP.md` | Day zero |
| `CUT_LIST.md` | What this course does not teach, and why |
| `SOURCES.md` | What to read, and what to ignore |

Start with `SETUP.md`.
