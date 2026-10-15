# Day 3 - a model as a judge, and checking it before you trust it.
#
#   RUBRIC   the judge's instructions, 50 words or more. A reply is good only if
#            it answers what was asked, every fact in it appears in the facts it
#            is given, it promises no refund the facts do not show, and it is
#            polite. Ask for the reason in one sentence.
#
#   class Verdict(BaseModel):  good: bool   reason: str
#
#   judge(model, ticket, reply, facts, retries=1) -> Verdict | None
#       structured output, as on week 2 day 2: SystemMessage(RUBRIC) and a
#       HumanMessage of three lines:
#           Ticket: <ticket>
#           Facts: <facts>
#           Reply: <reply>
#       Retry on an exception or None; after that, None - "could not decide" is
#       not the same as "good" or "bad".
#
#   agreement(judged, human) -> dict
#       judged: the judge's verdicts as True / False / None; human: a person's,
#       True / False, same order. Leave out the items the judge could not decide.
#           {"items": <all>, "judged": <decided>, "agree": <how many matched>,
#            "agreement": agree / judged to 2 places,
#            "false_pass": judge True where the person said False,
#            "false_fail": judge False where the person said True,
#            "kappa": Cohen's kappa to 2 places}
#       Cohen's kappa: agreement corrected for luck.
#           observed = agree / judged
#           chance   = P(judge yes) * P(person yes) + P(judge no) * P(person no)
#           kappa    = (observed - chance) / (1 - chance)
#       If chance is 1, kappa is 1.0 when observed is 1, else 0.0. Nothing judged:
#       agreement and kappa are 0.0.
#
#   trustworthy(report, min_kappa=0.6, max_false_pass=0) -> bool
#       every item decided, kappa at least min_kappa, and false passes at most
#       max_false_pass. A judge that passes bad replies is worse than none.
#
#   judge_evaluator(model) -> an evaluator named judge_good
#       with the day 2 signature. Facts: the output's tool calls, each as str(),
#       joined with " | ". Evaluation(name="judge_good", value 1.0 or 0.0,
#       comment=<the reason>) - or value 0.0, comment "the judge could not decide".
