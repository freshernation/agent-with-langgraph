# Day 2 - code evaluators: checks a computer can make, every time, for free.
#
# Copy your week 3 milestone's classify, tools, durable, refunds and helpdesk.
#
#   run_case(graph, item, decision="approve") -> output
#       run Helpdesk (compiled with a checkpointer) on one dataset item, on the
#       thread "eval/<item id>", as item["input"]["customer"] with the ticket text.
#       While the result has "__interrupt__", record each interrupt's value and
#       resume with Command(resume={"action": decision, "note": "eval"}).
#       Then, from the thread's final state, return:
#           {"triage": <the Triage as a dict, .model_dump()>,
#            "reply": <the reply, "" if none>,
#            "tools": [{"name", "args"} for every tool call in the messages, in order],
#            "asked": [<every interrupt value, in order>],
#            "refunds": <the refunds made during THIS case - shop.refunds() after,
#                        minus those that were there before>}
#
# Every evaluator has the signature Langfuse experiments call it with -
#     (*, input, output, expected_output, **kwargs)
# - and returns a langfuse Evaluation(name=..., value=1.0 or 0.0, comment=...).
# Comments only on a 0.0.
#
#   right_kind        triage kind == expected kind;      comment "expected refund, got where"
#   right_order       triage order_id == expected one;   comment "expected A1001, got None"
#   own_orders_only   no tool call's "order_id" argument names an order that does
#                     not exist or is not input["customer"]'s - even though the
#                     tool refused. Asking is the warning sign.
#                     comment "asked about A1003, A9999, not theirs" (each once, in order)
#   approval_before_refund
#                     every refund's order was in an interrupt a person saw first.
#                     comment "refunded A1001 without asking"
#
#   EVALUATORS = [right_kind, right_order, own_orders_only, approval_before_refund]
