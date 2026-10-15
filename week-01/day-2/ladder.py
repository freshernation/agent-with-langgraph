# Day 2 - a graph with no model in it.
#
# Your week 1 chatbot from Agent From Zero, as a LangGraph graph. Same replies:
#
#   hello          Hi! I am Desk.
#   help           I know: hello, help, count, quit.
#   count          You have sent 3 messages.        (including this one)
#   (nothing)      Say something.                   (does NOT count)
#   anything else  I don't know "pizza" yet.        (the tidied text)
#   quit           Bye! We exchanged 5 messages.    (including this one)
#
#   from typing import TypedDict
#   from langgraph.graph import StateGraph, START, END
#
#   class Turn(TypedDict, total=False)
#       text: str        what the person typed
#       command: str     text with spaces trimmed and lowercased
#       sent: int        messages counted so far, including this one
#       reply: str       what Desk says
#       path: list[str]  the names of the nodes this turn went through, in order
#
#   tidy(state) -> dict
#       sets command, adds 1 to sent (0 if missing) unless command is empty,
#       and appends "tidy" to path. A node returns ONLY the keys it changes.
#
#   route(state) -> str
#       "empty" for an empty command, the command itself if it is one of
#       hello / help / count / quit, otherwise "unknown"
#
#   build_graph() -> a compiled graph
#       START -> tidy -> (route) -> one of six answer nodes, named
#       hello, help, count, quit, empty, unknown -> END
#       Each answer node sets reply and appends its own name to path.
#
#   chat(graph, lines) -> list[str]
#       invoke the graph once per line, starting each turn from
#       {"text": line, "sent": <sent so far>, "path": []}; collect the replies;
#       stop after quit. The count lives OUTSIDE the graph, in this loop -
#       remember that on week 3 day 1.
