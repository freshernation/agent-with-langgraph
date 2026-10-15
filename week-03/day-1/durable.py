# Day 1 - a graph that remembers where it was.
#
# Copy classify.py and tools.py from your week 2 milestone, and helpdesk.py
# with the two changes its stub describes.
#
#   import sqlite3
#   from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
#   from langgraph.checkpoint.sqlite import SqliteSaver
#
#   SAFE_TYPES = [("classify", "Triage")]
#
#   serializer() -> JsonPlusSerializer
#       JsonPlusSerializer(allowed_msgpack_modules=SAFE_TYPES). A checkpoint is
#       data read back from disk; LangGraph will only rebuild Python objects of
#       types you have named. Triage is the one class Helpdesk keeps in its state.
#
#   open_checkpointer(path) -> SqliteSaver
#       a SqliteSaver over sqlite3.connect(path, check_same_thread=False), with
#       serde=serializer(). Every step of every run is saved in that file.
#
#   config_for(customer, ticket_id) -> dict
#       {"configurable": {"thread_id": "<customer>/<ticket_id>"}}
#       One thread per ticket. Everything said about that ticket, by anyone,
#       lives in it.
#
#   where_it_stopped(graph, config) -> tuple
#       the names of the nodes that would run next on that thread
#       (graph.get_state(config).next). () means it finished.
#
#   resume(graph, config) -> str
#       carry on from where the thread stopped: invoke with None as the input,
#       and return the reply.
#
#   conversation(graph, config) -> list[str]
#       the thread's messages as "<type>: <content>" lines, e.g. "human: Where is A1002?"
