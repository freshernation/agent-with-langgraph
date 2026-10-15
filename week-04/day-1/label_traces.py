"""Label your own Helpdesk traces, and send the eval set to Langfuse - given.

    python3 label_traces.py            # label recent traces into labelled.json
    python3 label_traces.py --push     # tickets + labelled.json -> Langfuse dataset "helpdesk"

Labelling shows you each trace's ticket and asks what it really was. Each label
is also sent to Langfuse as a human score on that trace, named "human-kind".
"""

import json
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client

import shop
from dataset import from_ticket, from_trace, problems

load_dotenv(find_dotenv(usecwd=True))
LABELLED = Path("labelled.json")


def label():
    client = get_client()
    done = json.loads(LABELLED.read_text()) if LABELLED.exists() else []
    seen = {item["id"] for item in done}
    for trace in client.api.trace.list(limit=30).data:
        if trace.id in seen or not isinstance(trace.input, dict) or "ticket" not in trace.input:
            continue
        print(f"\n{trace.input['ticket']}")
        kind = input("  kind (refund/where/change/other, blank to skip): ").strip()
        if not kind:
            continue
        order = input("  order id (blank for none): ").strip() or None
        done.append(from_trace({"id": trace.id, "input": trace.input}, kind, order))
        client.create_score(trace_id=trace.id, name="human-kind", value=kind, data_type="CATEGORICAL")
    LABELLED.write_text(json.dumps(done, indent=2))
    client.flush()
    print(f"\n{len(done)} labelled traces in {LABELLED}")


def push():
    items = [from_ticket(ticket) for ticket in shop.TICKETS]
    if LABELLED.exists():
        items += json.loads(LABELLED.read_text())
    for problem in problems(items):
        print("warning:", problem)
    client = get_client()
    client.create_dataset(name="helpdesk", description="Helpdesk tickets, labelled by a person")
    for item in items:
        client.create_dataset_item(dataset_name="helpdesk", input=item["input"],
                                   expected_output=item["expected_output"], metadata=item["metadata"],
                                   source_trace_id=item["metadata"].get("source_trace_id"))
    client.flush()
    print(f"{len(items)} items in dataset 'helpdesk'")


if __name__ == "__main__":
    push() if "--push" in sys.argv else label()
