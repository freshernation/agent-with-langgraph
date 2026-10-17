# Day 4 - procedures: what Helpdesk has learned to do, and who may teach it.
#
# Copy tools.py and day 1's facts.py into this folder.
#
# A procedure is a house rule - "offer the tracking link before saying sorry" -
# shared by EVERY customer's tickets. That makes it the most dangerous memory
# there is: if a customer can write one, one ticket rewrites how Helpdesk treats
# everyone. So only staff write procedures, and a rule the model proposes waits
# for staff to approve it.
#
#   NAMESPACE = ("helpdesk", "procedures")
#   HEADER = "House rules from staff:"
#   PROPOSE   instructions, 30 words or more: turn a staff member's refusal note
#             into one short, imperative rule about the situation, not the customer.
#
#   class Proposal(BaseModel):  rule: str
#
#   add_procedure(store, role, text) -> str
#       role other than "staff": store nothing, "Only staff can add procedures."
#       empty text: "A procedure needs some text."
#       otherwise put {"rule": <text, stripped>} under the key "p001", "p002", ...
#       (one more than how many there are) and return "Saved."
#
#   procedures_for_prompt(store) -> str
#       "" for none; otherwise HEADER and "- <rule>" per procedure, in key order
#
#   propose(model, note, retries=1) -> Proposal | None     structured output, as before
#
#   class Learning(TypedDict, total=False):  note: str   rule: str   saved: bool
#
#   build_learning(model, store, checkpointer) -> compiled graph
#       START -> propose -> ask_staff -> save -> END
#       propose     rule = propose(...).rule, or "" if nothing was proposed
#       ask_staff   no rule: saved False. Otherwise interrupt({"proposed": rule,
#                   "from_note": note}); saved is True only if the decision is
#                   "approve"
#       save        if saved, add_procedure(store, "staff", rule) - nothing above
#                   the interrupt writes anything (week 3's rule)
