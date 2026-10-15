# Day 1 - reducers: what happens when two nodes write the same key.
#
#   import operator
#   from typing import Annotated, TypedDict
#   from langchain_core.messages import AnyMessage
#   from langgraph.graph import StateGraph, START, END, add_messages
#   from langgraph.errors import InvalidUpdateError
#
#   keep_unique(old, new) -> list[str]
#       a reducer: old, then each item of new that is not already there, in order.
#       keep_unique(["a", "b"], ["b", "c"]) == ["a", "b", "c"]
#
#   class Ticket(TypedDict, total=False)
#       messages   list of messages, reduced by add_messages
#       notes      list of str, reduced by operator.add (lists join)
#       attempts   int, reduced by operator.add (numbers add)
#       tags       list of str, reduced by keep_unique
#       status     str, NO reducer: the last write wins
#
#   build_checks() -> compiled graph
#       three nodes run IN PARALLEL from START - "order", "customer", "history" -
#       each returning one note "<name> checked", attempts 1 and one tag:
#           order -> "has-order", customer -> "known-customer", history -> "has-order"
#       then all three -> "decide", which sets status to "ready" if there are
#       exactly three notes, otherwise "incomplete"; decide -> END.
#       (Parallel: an edge from START to each of the three.)
#
#   broken() -> str
#       build the SAME graph over a state with the same keys but NO reducers,
#       invoke it, and return the name of the exception class it raises
#       (catch InvalidUpdateError) - or "no error" if it does not.
#       Write it so the two graphs share one function that builds them - and
#       type the nodes' argument as plain `dict`: LangGraph reads a node's type
#       hint as the state it expects, and Ticket would clash with the other state.
