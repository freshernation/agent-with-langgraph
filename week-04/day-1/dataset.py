# Day 1 - an eval set, from labelled tickets and from real traces.
#
# An item is the shape Langfuse datasets use:
#   {"id": "T01",
#    "input": {"customer": "c1", "text": "<the ticket>"},
#    "expected_output": {"kind": "where", "order_id": "A1002"},
#    "metadata": {"source": "labelled"}}
#
#   KINDS = ("refund", "where", "change", "other")
#
#   from_ticket(ticket) -> item
#       one of shop.TICKETS, as an item, with metadata {"source": "labelled"}
#
#   from_trace(trace, kind, order_id) -> item
#       a real Helpdesk trace a person has just labelled. trace is a dict with
#       "id" and "input" - and Helpdesk's input is {"customer": ..., "ticket": ...}.
#       id: the trace's id. metadata {"source": "trace", "source_trace_id": <id>}.
#
#   in_test(item_id, test_share) -> bool
#       sha256 of the id as a number, mod 100, is below test_share * 100.
#       The same item always lands on the same side - this week, next week, on
#       anyone's machine.
#
#   split(items, test_share=0.3) -> (dev, test)
#       two lists, each in the original order. You tune prompts on dev. You look
#       at test when you are done, and never tune on it.
#
#   problems(items, least=3) -> list[str]
#       what is wrong with the set, in this order:
#         "<id> appears twice"                 (for each repeat)
#         "<id> has an unknown kind: <kind>"
#       and then, for each of KINDS in order with fewer than `least` items:
#         "only <n> examples of <kind>"
