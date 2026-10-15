"""Run one traced Desk turn against your Langfuse project - given.

    python3 run_traced.py "Save a note called dentist: Tuesday 3pm"

Needs LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY in .env. Works with the
fake model (AGENT_PROVIDER=fake), which is free and still makes a real trace.
Then find the trace in Langfuse, filtered by user 'me'.
"""

import sys

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client, propagate_attributes

from llm import connect
from traced import run_traced

load_dotenv(find_dotenv(usecwd=True))


def main():
    client = get_client()
    task = sys.argv[1] if len(sys.argv) > 1 else "What notes do I have?"
    answer = run_traced(connect(), task, user="me", session="day-1", client=client,
                        propagate=propagate_attributes)
    print("Desk:", answer)
    client.flush()
    print("Sent. In Langfuse, open Tracing and filter by user 'me'; the newest is this one.")


if __name__ == "__main__":
    main()
