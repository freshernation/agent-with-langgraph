# Day 3 - tools over the shop, and tools that read the state.
#
# The `shop` package is given (read shop/__init__.py first). Helpdesk is always
# talking to ONE customer, and which one is not the model's decision.
#
#   from typing import Annotated, TypedDict
#   from langchain_core.tools import tool
#   from langgraph.prebuilt import InjectedState, ToolNode, tools_condition
#   import shop
#
#   SYSTEM   Helpdesk's instructions, 25 words or more: use the tools, never
#            guess a status, date or amount, only this customer's orders.
#
#   class HelpState(TypedDict, total=False)
#       messages   list of messages, reduced by add_messages
#       customer   str - the customer's id, set by your code, never by the model
#
#   describe(order) -> str
#       "A1002 placed 2026-09-28: shipped, $34.00"
#
#   Three tools. Each takes `state: Annotated[dict, InjectedState]` - LangGraph
#   fills it in from the graph's state, and the model never sees it in the schema.
#
#   my_orders()                 every order of state["customer"], newest first,
#                               one describe() per line; or
#                               "This customer has no orders."
#   order_details(order_id)     "<describe>. Items: 1 x Kettle at $39.00. Refunded so far: $0.00."
#                               (items joined with ", ")
#   tracking(order_id)          "A1002 is shipped, tracking number TRK-5544."
#                               or "A1004 is processing and has not been sent yet."
#
#   For an order that does not exist OR belongs to someone else, both
#   order_details and tracking say exactly:
#       "<order_id> is not one of this customer's orders."
#   (The same words for both, so the model cannot learn which orders exist.)
#
#   TOOLS = [my_orders, order_details, tracking]
#
#   call_model(state, model) -> {"messages": [reply]}   as in week 1, with SYSTEM
#
#   build_lookup(model) -> compiled graph
#       START -> "model" -> tools_condition -> "tools" (a ToolNode(TOOLS)) -> "model"
#       You wrote your own tool node in week 1. Now use the library's: it is the
#       one that knows how to fill in InjectedState.
