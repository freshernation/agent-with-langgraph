# Day 4 - experiments, prompts in Langfuse, and a gate.
#
# Copy dataset.py (day 1), and classify.py (week 3) with its one new argument.
# Copy evaluators.py (day 2) too.
#
#   classify_task(model, system) -> task
#       a task in Langfuse's experiment shape, task(*, item, **kwargs), returning
#       {"triage": classify(model, item["input"]["text"], system=system).model_dump()}
#
#   run_local(items, task, evaluators) -> dict
#       what client.run_experiment does, on your machine, with no network:
#       for each item, output = task(item=item); call every evaluator with
#       input=, output=, expected_output=, metadata=item.get("metadata").
#           {"per_item": [{"id", "output", "scores": {name: value},
#                          "comments": {name: comment - only those with one}}],
#            "means": {name: mean of its values to 3 places}}
#
#   gate(baseline, candidate, tolerance=0.0) -> list[str]
#       baseline and candidate are "means" dicts. For each name in baseline, in
#       order:  "<name>: missing"               if the candidate has no score for it
#               "<name>: 0.95 -> 0.80"          if candidate < baseline - tolerance
#       [] means the change may ship.
#
#   load_prompt(client, name, fallback) -> str
#       the text of the prompt labelled "production" in Langfuse:
#       client.get_prompt(name, label="production", fallback=fallback).prompt.
#       If client is None, or anything goes wrong, the fallback. Helpdesk must
#       never stop because the prompt store is unreachable.
