"""Helpdesk in your terminal, with you as the person who approves refunds - given.

    python3 run_desk.py c1 T02

One customer, one ticket thread, saved in desk.db. Stop it with Ctrl-C at any
point and start it again with the same arguments: it carries on. Traced to
Langfuse if your keys are set.
"""

import os
import sys

from dotenv import find_dotenv, load_dotenv

from durable import open_checkpointer, where_it_stopped
from helpdesk import answer, build_helpdesk, decide
from models import connect
from refunds import pending
from sessions import run_config

load_dotenv(find_dotenv(usecwd=True))


def approve_in_terminal(graph, config):
    while pending(graph, config):
        ask = pending(graph, config)[0]
        print(f"\n  REFUND REQUEST: ${ask['amount']:.2f} on {ask['order_id']} for {ask['customer']}"
              f" - {ask['reason']}")
        choice = input("  approve / reject / edit? ").strip().lower()
        if choice == "edit":
            reply = decide(graph, config, "edit", amount=float(input("  amount: ")))
        elif choice == "approve":
            reply = decide(graph, config, "approve")
        else:
            reply = decide(graph, config, "reject", note=input("  reason for the customer: "))
        if reply:
            print(f"Helpdesk: {reply}")


def main():
    customer = sys.argv[1] if len(sys.argv) > 1 else "c1"
    ticket = sys.argv[2] if len(sys.argv) > 2 else "T01"
    callbacks = []
    if os.environ.get("LANGFUSE_PUBLIC_KEY"):
        from langfuse.langchain import CallbackHandler
        callbacks = [CallbackHandler()]
    config = run_config(customer, ticket, callbacks)
    graph = build_helpdesk(connect(), checkpointer=open_checkpointer("desk.db"))
    if where_it_stopped(graph, config):
        print("(carrying on where this ticket stopped)")
        approve_in_terminal(graph, config)
    while True:
        text = input(f"{customer}: ").strip()
        if text in ("", "quit"):
            break
        reply = answer(graph, customer, text, config)
        if reply:
            print(f"Helpdesk: {reply}")
        approve_in_terminal(graph, config)


if __name__ == "__main__":
    main()
