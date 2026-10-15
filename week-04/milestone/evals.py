# Week 4 milestone - an eval suite that fails a bad prompt change.
#
# Copy dataset, evaluators, judge, experiment and classify from this week's days.
#
#   DATASET = [from_ticket(t) for t in shop.TICKETS]
#
#   compare(model, items, baseline_system, candidate_system,
#           evaluators=(right_kind, right_order), tolerance=0.0) -> dict
#       run the classifier over the items twice with run_local - once with each
#       prompt - and return
#           {"baseline": <its means>, "candidate": <its means>,
#            "regressions": gate(baseline means, candidate means, tolerance),
#            "newly_failing": newly_failing(baseline run, candidate run)}
#
#   newly_failing(baseline, candidate) -> list[str]
#       the two full run_local results. For every item and score that went DOWN
#       from baseline to candidate, in the candidate's order:
#           "T05 right_order: expected None, got A1005"
#       (the candidate's comment for that score; just "T05 right_order" if none)
#       A mean tells you that it got worse. This tells you where.
