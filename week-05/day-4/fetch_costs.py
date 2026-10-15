"""Helpdesk's cost and latency, from your Langfuse project - given.

    python3 fetch_costs.py            # the last 100 traces
    python3 fetch_costs.py 500        # more
"""

import sys

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client

from costs import slowest, summarise

load_dotenv(find_dotenv(usecwd=True))


def fetch(limit: int) -> list[dict]:
    client, traces, page = get_client(), [], 1
    while len(traces) < limit:
        found = client.api.trace.list(limit=min(100, limit - len(traces)), page=page)
        if not found.data:
            break
        traces += [{"id": t.id, "timestamp": t.timestamp.isoformat(), "session_id": t.session_id,
                    "latency": t.latency, "total_cost": t.total_cost} for t in found.data]
        page = page + 1
    return traces


def main():
    traces = fetch(int(sys.argv[1]) if len(sys.argv) > 1 else 100)
    for name, value in summarise(traces).items():
        print(f"{name:18} {value}")
    print("slowest:", slowest(traces, 5))


if __name__ == "__main__":
    main()
