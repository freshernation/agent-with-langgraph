# Week 1 milestone - does the graph behave like the loop you wrote?
#
# Copy desk_graph.py from day 3 and traced.py from day 1 into this folder.
#
# A script is what the model will say, turn by turn, written once for both:
#     ("say", "Saved it.")                                  a plain answer
#     ("tools", [("add_note", {"title": "x"}), ...])         tool calls in one turn
# A LIST of steps is played in order. A single step (a tuple, not a list) is
# repeated for ever.
#
#   to_hand(steps)   an llm.FakeModel playing that script     (llm.say, llm.use_many)
#   to_graph(steps)  a models.ScriptedModel playing it        (models.say, models.calls)
#
#   run_hand(steps, task) -> {"answer": ..., "titles": [...]}
#       Desk's own run_agent from desk.agent, with desk_graph's SYSTEM, and only
#       the four tools the graph has - the matching entries of desk.kit's
#       SCHEMAS and TOOLS. titles: the notes file's titles afterwards, in order
#       ([] if there is no file). The file is os.environ["NOTES_FILE"], or notes.json.
#
#   run_graph(steps, task, limit=10) -> {"answer": ..., "titles": [...]}
#       desk_graph's build_graph, invoked with the task and recursion_limit=limit.
#       If it hits the limit, the answer is desk_graph's STOPPED.
#
#   differences(hand, graph) -> list[str]
#       the keys, of "answer" then "titles", whose values differ.
#
# The tests run each on a fresh notes file. One script is meant to differ - find
# out why, and write it into FRAMEWORK.md.
