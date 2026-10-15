"""Helpdesk on all twenty labelled tickets, with your real model - given.

    python3 run_tickets.py            # the triage report
    python3 run_tickets.py --replies  # and every reply

About forty model calls for the report, more with replies. Traced to Langfuse
in session "tickets" if your keys are set.
"""

import os
import sys

from dotenv import find_dotenv, load_dotenv

import shop
from helpdesk import build_helpdesk
from models import connect
from triage_report import triage_report

load_dotenv(find_dotenv(usecwd=True))


def main():
    model = connect()
    config = {}
    if os.environ.get("LANGFUSE_PUBLIC_KEY"):
        from langfuse.langchain import CallbackHandler
        config = {"callbacks": [CallbackHandler()],
                  "metadata": {"langfuse_session_id": "tickets"}}
    report = triage_report(model.with_config(config) if config else model, shop.TICKETS)
    print(f"{report['right']}/{report['total']} right ({report['accuracy']:.0%})")
    print("wrong kind: ", report["wrong_kind"])
    print("wrong order:", report["wrong_order"])
    if "--replies" in sys.argv:
        graph = build_helpdesk(model)
        for ticket in shop.TICKETS:
            run = dict(config, metadata={**config.get("metadata", {}), "langfuse_user_id": ticket["customer"]})
            reply = graph.invoke({"customer": ticket["customer"], "ticket": ticket["text"]}, run)["reply"]
            print(f"\n{ticket['id']} [{ticket['kind']}] {ticket['text']}\n  -> {reply}")
    if config:
        from langfuse import get_client
        get_client().flush()


if __name__ == "__main__":
    main()
