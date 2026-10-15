"""Both Desks, one task, one Langfuse session - given.

    python3 run_side_by_side.py "Save a note called dentist: Tuesday 3pm"

Needs your Langfuse keys and a real model in .env. Both traces land in session
"side-by-side" for user "me", one after the other.
"""

import sys

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client, propagate_attributes
from langfuse.langchain import CallbackHandler

import llm
import models
from desk_graph import ask, build_graph
from traced import run_traced

load_dotenv(find_dotenv(usecwd=True))


def main():
    task = sys.argv[1] if len(sys.argv) > 1 else "What notes do I have?"
    client = get_client()
    print("By hand:", run_traced(llm.connect(), task, "me", "side-by-side", client,
                                 propagate_attributes))
    config = {"callbacks": [CallbackHandler()],
              "metadata": {"langfuse_user_id": "me", "langfuse_session_id": "side-by-side"}}
    print("Graph:  ", ask(build_graph(models.connect()), task, config=config))
    client.flush()
    print("Sent. In Langfuse, open Sessions and find 'side-by-side'.")


if __name__ == "__main__":
    main()
