# Day 4 - routing: classify, branch, look up, draft.
#
# Copy classify.py (day 2) and tools.py (day 3) into this folder.
#
#        START -> classify --other--> handoff -> END
#                    |
#                  (else)
#                    v
#                  lookup <-> tools          (the week 1 loop, with the shop's tools)
#                    |
#                    v
#                  draft -> END
#
#   DRAFT     the drafting instructions, 40 words or more: only the facts given,
#             no promised dates or amounts, and for a refund, say a PERSON will
#             review it within one working day - Helpdesk cannot refund (yet).
#   HANDOFF = ("Thanks for getting in touch. I've passed this to a person on our team, who will "
#              "reply within one working day.")
#   RETRY = RetryPolicy(max_attempts=3)          (from langgraph.types)
#
#   class Help(TypedDict, total=False)
#       messages (add_messages), customer: str, ticket: str, triage: Triage, reply: str
#
#   with_backup(runnable, backup_runnable)
#       runnable.with_fallbacks([backup_runnable]), or runnable alone if there is no backup
#
#   classify_node(state, model)
#       {"triage": classify(model, state["ticket"]), "messages": [HumanMessage(ticket)]}
#   after_classify(state) -> "handoff" for kind "other", otherwise "lookup"
#
#   lookup(state, model, backup)
#       like week 1's call_model, but the system message is tools.SYSTEM plus
#       " This ticket is about: <kind>" and ", order <id>" if there is one, then ".".
#       Bind the tools to EACH model before adding the fallback - a model with
#       fallbacks has no bind_tools of its own.
#   after_lookup(state) -> "tools" if the last message asks for any, otherwise "draft"
#
#   draft(state, model, backup)
#       one model call (with the backup) with SystemMessage(DRAFT) and a
#       HumanMessage of three lines:
#           Ticket: <ticket>
#           Kind: <kind>
#           What we found: <the last message's content>
#       returns {"reply": <its content>}
#   handoff(state) -> {"reply": HANDOFF}
#
#   build_helpdesk(model, backup=None) -> compiled graph
#       the nodes above, plus "tools" = ToolNode(TOOLS). lookup and draft get
#       retry_policy=RETRY: a dropped connection is tried again; a bug is not.
#
#   answer(graph, customer, ticket) -> str     invoke, return the reply
