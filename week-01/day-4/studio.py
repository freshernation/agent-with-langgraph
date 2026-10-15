"""The graph Studio opens - given. See langgraph.json beside it.

    cd week-01/day-4 && langgraph dev

Uses whichever model .env names. Studio asks you to sign in to LangSmith to show
the page; keep LANGSMITH_TRACING=false so no trace is sent there.
"""

from desk_graph import build_graph
from models import connect

graph = build_graph(connect())
