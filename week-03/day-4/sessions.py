# Day 4 - one customer, many tickets, in Langfuse.
#
# Copy your week-03/day-1 files into this folder.
#
#   run_config(customer, ticket_id, callbacks) -> dict
#       one config that does three jobs at once:
#           {"configurable": {"thread_id": "<customer>/<ticket_id>"},      the checkpointer's thread
#            "callbacks": callbacks,                                        Langfuse's handler
#            "metadata": {"langfuse_user_id": customer,                    who
#                         "langfuse_session_id": "<customer>/<ticket_id>"}} which conversation
#       The thread and the session are the SAME string, so a ticket in your
#       database and a session in Langfuse can always be matched.
#
#   customer_story(traces) -> list[dict]
#       traces are one customer's traces as fetch_customer.py gets them:
#           {"id", "timestamp" (ISO text), "session_id" (or None), "total_cost" (or None), "latency"}
#       Group them by session, in order of each session's first trace:
#           {"session": <id, or "(no session)">, "traces": n,
#            "cost": total to 6 places (None counts as 0), "first": <timestamp>, "last": <timestamp>}
