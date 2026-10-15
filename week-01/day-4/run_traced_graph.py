"""Run one traced turn of the graph Desk, beside yesterday's hand-written one - given.

    python3 run_traced_graph.py "Save a note called dentist: Tuesday 3pm"

Needs your Langfuse keys and, for a fair comparison, a real model in .env. The
trace lands in session "compare" for user "me" - run day 1's run_traced.py
with the same task and compare the two.
"""

import sys

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client
from langfuse.langchain import CallbackHandler

from desk_graph import ask, build_graph
from models import connect
from prebuilt import config_for

load_dotenv(find_dotenv(usecwd=True))


def main():
    task = sys.argv[1] if len(sys.argv) > 1 else "What notes do I have?"
    config = config_for("me", "compare", [CallbackHandler()])
    print("Desk:", ask(build_graph(connect()), task, config=config))
    get_client().flush()
    print("Sent. In Langfuse, open Sessions and find 'compare'.")


if __name__ == "__main__":
    main()
