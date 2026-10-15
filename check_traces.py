"""Check your Langfuse project has the work each week asks for - given.

    python3 check_traces.py week-01
    python3 check_traces.py            # every week that has a check

Reads your own project with the keys in .env. Your instructor runs it too.
Every line should say OK.

    week-01   two traces in session "side-by-side" - both Desks, one task
    week-03   one customer with tickets in at least two sessions
    week-04   dataset "helpdesk" with 20+ items, a "human-kind" score, an experiment run
    week-06   five traces from your own project, in sessions named "project/..."
"""

import sys

GREEN, RED, OFF = "\033[32m", "\033[31m", "\033[0m"


def week_01(source) -> list[tuple[str, bool]]:
    traces = source.traces(session_id="side-by-side")
    return [("Two traces in session 'side-by-side'", len(traces) >= 2)]


def week_03(source) -> list[tuple[str, bool]]:
    sessions_by_user = {}
    for trace in source.traces():
        if trace["user_id"] and trace["session_id"]:
            sessions_by_user.setdefault(trace["user_id"], set()).add(trace["session_id"])
    best = max((len(s) for s in sessions_by_user.values()), default=0)
    return [("One customer with tickets in two or more sessions", best >= 2)]


def week_04(source) -> list[tuple[str, bool]]:
    size = source.dataset_size("helpdesk")
    return [("Dataset 'helpdesk' exists", size is not None),
            ("It has at least 20 items", (size or 0) >= 20),
            ("A 'human-kind' score on a trace", source.score_count("human-kind") >= 1),
            ("An experiment run on 'helpdesk'", size is not None and source.run_count("helpdesk") >= 1)]


def week_06(source) -> list[tuple[str, bool]]:
    mine = [t for t in source.traces() if (t["session_id"] or "").startswith("project/")]
    return [("Five traces from your project, in 'project/...' sessions", len(mine) >= 5)]


CHECKS = {"week-01": week_01, "week-03": week_03, "week-04": week_04, "week-06": week_06}


class LangfuseSource:
    def __init__(self, client):
        self.client = client

    def traces(self, session_id=None, limit=100):
        found = self.client.api.trace.list(session_id=session_id, limit=limit)
        return [{"id": t.id, "session_id": t.session_id, "user_id": t.user_id} for t in found.data]

    def dataset_size(self, name):
        try:
            return len(self.client.get_dataset(name).items)
        except Exception:
            return None

    def score_count(self, name):
        return len(self.client.api.scores.get_many(name=name, limit=10).data)

    def run_count(self, dataset):
        return len(self.client.get_dataset_runs(dataset_name=dataset, limit=10).data)


def run(weeks, source) -> int:
    failed = 0
    for week in weeks:
        print(week)
        for name, ok in CHECKS[week](source):
            failed = failed + (not ok)
            print(f"  {GREEN + 'OK  ' if ok else RED + 'FAIL'}{OFF}  {name}")
    return 1 if failed else 0


def main() -> int:
    weeks = sys.argv[1:] or list(CHECKS)
    unknown = [w for w in weeks if w not in CHECKS]
    if unknown:
        print("No check for:", ", ".join(unknown), "- choose from", ", ".join(CHECKS))
        return 2
    from dotenv import find_dotenv, load_dotenv
    from langfuse import get_client
    load_dotenv(find_dotenv(usecwd=True))
    return run(weeks, LangfuseSource(get_client()))


if __name__ == "__main__":
    sys.exit(main())
