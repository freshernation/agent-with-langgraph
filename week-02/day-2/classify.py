# Day 2 - structured output: a form the model must fill in.
#
#   from typing import Literal
#   from pydantic import BaseModel, Field
#   from langchain_core.messages import HumanMessage, SystemMessage
#
#   SYSTEM   the classifier's instructions, 40 words or more. Say what each kind
#            means, that order_id is only ever copied from the ticket (never
#            guessed), and that the ticket's text is never an instruction.
#
#   class Triage(BaseModel)
#       kind      one of "refund", "where", "change", "other"
#       order_id  str or None, default None - and when present it must look like
#                 an order number: "A" and four digits (Field(pattern=...))
#       urgent    bool, default False
#
#   FALLBACK = Triage(kind="other", order_id=None, urgent=False)
#
#   classify(model, text, retries=1) -> Triage
#       model.with_structured_output(Triage), invoked with a SystemMessage(SYSTEM)
#       and a HumanMessage(text). Two ways it fails:
#         - it raises (the model filled the form in wrong: kind "banana",
#           order_id "order 12")
#         - it returns None (the model answered in words and filled in nothing)
#       Either way, try again - `retries` more times. If it never succeeds,
#       return FALLBACK: a ticket nobody could classify goes to a person.
