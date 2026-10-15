# Day 4 - what Helpdesk costs, and how long it takes.
#
# A trace here is a dict, as fetch_costs.py gets it from Langfuse:
#   {"id", "timestamp", "session_id" (or None), "latency" (seconds, or None),
#    "total_cost" (dollars, or None)}
# None counts as 0. A ticket is a session; a trace with no session is its own ticket
# (use its id).
#
#   percentile(values, p) -> float
#       nearest rank: sorted, the value at position ceil(p/100 * n), counting
#       from 1 and never below 1. 0.0 for none.
#
#   summarise(traces) -> dict
#       {"traces": n, "tickets": <how many tickets>,
#        "p50_seconds", "p95_seconds": percentiles of latency, to 2 places,
#        "cost_per_trace", "cost_per_ticket": means, to 6 places,
#        "costliest_ticket": <the ticket id with the highest total cost>}
#       No traces: zeros, and None for the costliest ticket.
#
#   slowest(traces, n) -> list[str]
#       the ids of the n slowest traces, slowest first; ties by id.
