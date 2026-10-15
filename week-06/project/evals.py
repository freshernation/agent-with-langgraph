# Your evals.
#
#   DATASET     at least ten items, each {"id", "input", "expected_output"},
#               ids all different - real examples, labelled by you
#   EVALUATORS  at least two evaluators with the week 4 signature,
#               (*, input, output, expected_output, **kwargs) -> Evaluation
#   make_task(model) -> task(*, item, **kwargs) -> output
#               runs your graph on one item
