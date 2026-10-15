# Project 1 - start from your week-03/day-1/helpdesk.py. Four changes:
#
#   1. Helpdesk can refund - with a person's approval. lookup and the ToolNode
#      use refunds.REFUND_TOOLS, and lookup's system message is
#      tools.SYSTEM + refunds.REFUND_RULE + " This ticket is about: ...".
#
#   2. DRAFT, 40 words or more, now says: claim a refund was made only if the
#      facts say so, with the amount; if a person did not approve it, say so
#      kindly with their reason.
#
#   3. answer(graph, customer, ticket, config=None) -> str | None
#      None when the run stopped to wait for a person (the result has
#      "__interrupt__") - NOT the reply left over from an earlier turn.
#
#   4. decide(graph, config, action, amount=None, note="") -> str | None
#      resume with Command(resume={"action", "note", and "amount" if given});
#      the reply, or None if it stopped again.
