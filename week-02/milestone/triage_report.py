# Week 2 milestone - how often does the classifier get a ticket right?
#
#   triage_report(model, tickets) -> dict
#       classify every ticket's text (classify.py). A ticket is right when BOTH
#       the kind and the order_id match the person's label ("kind", "order").
#       {"total": n, "right": k, "accuracy": k/n to 2 places (0.0 for none),
#        "wrong_kind": [ids, in order], "wrong_order": [ids, in order]}
#
# shop.TICKETS are twenty tickets a person labelled. run_tickets.py runs this,
# and Helpdesk, over all of them with your real model. Week 4 turns it into an
# eval suite.
