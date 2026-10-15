"""One customer's tickets, as Langfuse saw them - given.

    python3 fetch_customer.py c1

Needs your Langfuse keys. Reads the customer's last 100 traces and prints one
line per session (ticket), using your customer_story().
"""

import sys

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client

from sessions import customer_story

load_dotenv(find_dotenv(usecwd=True))


def fetch(customer: str) -> list[dict]:
    found = get_client().api.trace.list(user_id=customer, limit=100)
    return [{"id": trace.id, "timestamp": trace.timestamp.isoformat(), "session_id": trace.session_id,
             "total_cost": trace.total_cost, "latency": trace.latency} for trace in found.data]


def main():
    customer = sys.argv[1] if len(sys.argv) > 1 else "c1"
    for session in customer_story(fetch(customer)):
        print(f"{session['session']:20} {session['traces']:3} traces  ${session['cost']:.4f}  "
              f"{session['first'][:16]} -> {session['last'][:16]}")


if __name__ == "__main__":
    main()
