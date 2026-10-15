# Day 2 - refunds need a human.
#
# Copy your week-03/day-1 files into this folder.
#
#   from langgraph.types import interrupt, Command
#
#   REFUND_RULE   one or two sentences added to tools.SYSTEM: when to ask for a
#                 refund, and that a person approves every one.
#
#   @tool request_refund(order_id, amount: float, reason, state: InjectedState) -> str
#       description: what it does AND that it only happens if a person approves.
#       In this order:
#         1. not one of this customer's orders -> "<order_id> is not one of this customer's orders."
#         2. not delivered -> "Only delivered orders can be refunded; <id> is <status>."
#            (no point waking a person for something that cannot be done)
#         3. decision = interrupt({"customer", "order_id", "amount", "reason"})
#            The graph STOPS here and saves itself. When a person decides, the
#            graph resumes - and this tool runs again FROM THE TOP, with
#            interrupt() returning the decision. So nothing above this line may
#            change anything.
#         4. decision["action"]:
#              "approve" -> shop.refund(order id, amount, reason)
#              "edit"    -> shop.refund(order id, decision["amount"], reason)
#              "reject"  -> "A person did not approve this refund. <note>"
#                           (decision.get("note", ""), and no trailing space if empty)
#
#   REFUND_TOOLS = tools.TOOLS + [request_refund]
#
#   call_model(state, model)          as tools.call_model, with REFUND_TOOLS and
#                                     SYSTEM + REFUND_RULE
#   build_refund_desk(model, checkpointer)
#       the day 3 lookup loop (model, ToolNode, tools_condition) over REFUND_TOOLS,
#       compiled with the checkpointer. No checkpointer, no stopping.
#
#   pending(graph, config) -> list[dict]
#       what the thread is waiting for a person to decide: the value of each
#       interrupt in graph.get_state(config).interrupts
#
#   decide(graph, config, action, amount=None, note="") -> str
#       resume with Command(resume={"action": action, "note": note}) - plus
#       "amount" when one is given - and return the last message's content.
