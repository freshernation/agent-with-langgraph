"""The course's LangChain models - one way to get a chat model for any provider.

    from models import connect

    model = connect()                       # whichever provider .env names
    reply = model.invoke("Hello")           # an AIMessage

Three providers, chosen by AGENT_PROVIDER in .env, exactly as in the llm package:

    fake     ScriptedModel - no key, no network, no cost. The default, and every test
    claude   ChatAnthropic   (needs ANTHROPIC_API_KEY; AGENT_CLAUDE_MODEL to change model)
    openai   ChatOpenAI      (needs OPENAI_API_KEY; AGENT_OPENAI_MODEL to change model)

The llm package beside this one is the hand-written model layer from Agent From
Zero, kept for week 1's comparison. From week 1 day 3 on, everything uses this one.
"""

import os

from models.scripted import ScriptedModel, call, calls, say

__all__ = ["connect", "ScriptedModel", "say", "call", "calls"]

PROVIDERS = ("fake", "claude", "openai")
CLAUDE_DEFAULT = "claude-opus-5-5"
OPENAI_DEFAULT = "gpt-5-mini"

# Claude thinks before it answers, out of max_tokens; a small limit can be spent
# before the answer starts. Generous, but not the library's 128k default.
MAX_TOKENS = 16000


def connect(provider=None):
    """Return a LangChain chat model. With no argument, reads AGENT_PROVIDER (default: fake)."""
    _load_env_file()
    provider = (provider or os.environ.get("AGENT_PROVIDER") or "fake").strip().lower()
    if provider == "fake":
        return ScriptedModel()
    if provider == "claude":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=os.environ.get("AGENT_CLAUDE_MODEL") or CLAUDE_DEFAULT,
                             max_tokens=MAX_TOKENS)
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.environ.get("AGENT_OPENAI_MODEL") or OPENAI_DEFAULT,
                          max_completion_tokens=MAX_TOKENS)
    raise ValueError(f"Unknown provider {provider!r}. Set AGENT_PROVIDER to one of: "
                     + ", ".join(PROVIDERS))


def _load_env_file():
    try:
        from dotenv import find_dotenv, load_dotenv
    except ImportError:
        return
    load_dotenv(find_dotenv(usecwd=True))
