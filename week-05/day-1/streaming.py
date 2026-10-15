# Day 1 - async, and the stream modes.
#
# Copy your week 3 milestone's classify, tools, durable, refunds and helpdesk.
# Every function here is `async def`, and reads the graph with `async for`.
#
#   async updates(graph, input, config) -> list[str]
#       graph.astream(input, config, stream_mode="updates") yields one dict per
#       step, keyed by the node that ran. Return the node names, in order.
#       (An interrupt shows up as a key too: "__interrupt__".)
#
#   async tokens(graph, input, config, node="draft") -> list[str]
#       stream_mode="messages" yields (chunk, metadata) for every piece of every
#       message as it is produced. Return the non-empty chunk contents whose
#       metadata["langgraph_node"] is `node` - only the reply the customer reads,
#       not the classifier's form or the lookup's working.
#
#   async events(graph, input, config, node="draft")      an async generator
#       stream_mode=["updates", "messages"] at once - each item is then
#       (mode, data). Yield, as they happen:
#           {"type": "step", "data": <node name>}            for each update
#           {"type": "waiting", "data": <interrupt value>}   for each interrupt
#           {"type": "token", "data": <text>}                as updates/tokens above
#       and when the stream ends, if the thread has nothing next
#       (await graph.aget_state(config)), one last
#           {"type": "done", "data": <the reply, "" if none>}
#       A thread waiting for a person gets no "done".
