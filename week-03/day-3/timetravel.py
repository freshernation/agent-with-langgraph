# Day 3 - go back to before the bad step, change it, run again.
#
# Copy your week-03/day-1 files into this folder. Every function here works on a
# Helpdesk compiled WITH a checkpointer.
#
#   history(graph, config) -> list[dict]
#       every checkpoint of the thread, newest first (graph.get_state_history):
#           {"step": <metadata["step"]>, "next": <the nodes due next>,
#            "checkpoint_id": <config["configurable"]["checkpoint_id"]>}
#
#   checkpoint_before(graph, config, node) -> dict | None
#       the config of the most recent checkpoint at which `node` was due next,
#       or None if it never was
#
#   replay(graph, checkpoint) -> str
#       invoke with None from that checkpoint's config: everything after it runs
#       again - the model is called again - and the result is a new branch.
#       Return the reply.
#
#   fix_triage(graph, config, triage) -> str
#       the classifier got it wrong. Find the checkpoint just after classify
#       (the newest one whose next is ("lookup",) or ("handoff",)), write the
#       right triage into it with graph.update_state(..., as_node="classify") -
#       as if classify had said it - and run on from there. Return the new reply.
#       Raise ValueError if the thread was never classified.
#       as_node matters: it makes LangGraph take the edge that leaves classify
#       again, with the corrected triage.
