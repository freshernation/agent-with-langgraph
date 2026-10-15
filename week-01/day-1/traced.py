# Day 1 - your hand-written Desk, traced in Langfuse.
#
# You will not change Desk. You will stand things in front of it, the way a
# Recorder stands in front of a model, so that every call is written down.
#
# `client` is a Langfuse client (from langfuse import get_client). The one
# method you need:
#
#     with client.start_as_current_observation(as_type=..., name=..., input=...) as obs:
#         ...
#         obs.update(output=..., usage_details=...)
#
# Anything started inside a `with` block is nested under it. That nesting IS
# the trace.
#
#   class TracedModel(model, client)
#       .chat(messages, system=None, tools=None, max_tokens=None)
#           inside an observation with as_type="generation", name="model",
#           model=<the model's .name, or None if it has none>, input=messages:
#           call the real model, then update the observation with
#               output        the reply's text, or its tool_calls if the text is empty
#               usage_details {"input": <tokens in>, "output": <tokens out>}
#           and return the reply unchanged.
#
#   traced(function, name, client) -> function
#       a tool that runs inside an observation with as_type="tool", name=name,
#       input=<the arguments as a dict>, and records its result as the output.
#
#   traced_tools(tools, client) -> dict
#       every tool in a dispatch table, traced.
#
#   run_traced(model, task, user, session, client, propagate) -> str
#       one Desk turn as one trace:
#       an observation with as_type="agent", name="desk", input=task; inside it,
#       `with propagate(user_id=user, session_id=session):` around
#       run_agent(TracedModel(...), task, SCHEMAS, traced_tools(TOOLS, ...),
#       system=SYSTEM); then the root's output is the answer. Return the answer.
#
#       (propagate is langfuse.propagate_attributes - passed in so the tests
#        can watch it. SCHEMAS and TOOLS come from desk.kit, SYSTEM from desk.app.)
