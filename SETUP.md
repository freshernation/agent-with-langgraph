# Day zero

About an hour. Do it before week 1, not on Monday morning.

---

## 1. Python 3.12 or newer

```bash
python3 --version
```

If that prints 3.12 or higher, skip ahead. Otherwise install it from
[python.org](https://www.python.org/downloads/) or, on macOS, `brew install python@3.12`.

## 2. Your own repository

Make your own copy of this repository on GitHub (**Use this template**), then clone
your copy:

```bash
git clone https://github.com/YOUR-USERNAME/agent-with-langgraph.git
cd agent-with-langgraph
```

You push to your copy every day.

## 3. The environment

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

## 4. Check it

```bash
python3 check_setup.py
pytest -q
```

Every line of `check_setup.py` should say OK except two — Langfuse (step 6) and your
baseline (step 5).

## 5. Your baseline interview

Open a fresh chat with any capable AI. Paste the whole of `ai/advisor.md`. Answer its
questions honestly; it will ask you to do small things rather than rate yourself. At
the end it prints a `BASELINE` block. Paste it into `logs/baseline.md`, replacing the
bracketed lines, and push.

Your instructor reads every baseline before Monday.

## 6. Langfuse, and a model key

**Before week 1 day 1:** a free [Langfuse Cloud](https://cloud.langfuse.com) account on
the Hobby plan, with one project of your own. Put its keys in `.env` as
`LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`. The Hobby plan keeps traces for a
limited time, so save the screenshots and reports your portfolio needs in the week
you make them.

**Before week 1 day 4:** a key for Claude or OpenAI in `.env`, and `AGENT_PROVIDER` set
to `claude` or `openai`. Until then the scripted model is all you need.

Keep `LANGSMITH_TRACING=false` in `.env`. Studio (week 1 day 4) asks you to sign in to
LangSmith; that is all it is for. Langfuse is the only place traces go.

## 7. Before week 5: Docker

Week 5 runs Helpdesk in containers on your machine. You need Docker running. If it
will not run on your machine, tell your instructor in week 3, not in week 5.
