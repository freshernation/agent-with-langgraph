"""check_traces.py's checks, against a pretend Langfuse project."""

import check_traces


class Source:
    def __init__(self, traces=(), datasets=None, scores=None, runs=None):
        self._traces = list(traces)
        self.datasets, self.scores, self.runs = datasets or {}, scores or {}, runs or {}

    def traces(self, session_id=None, limit=100):
        return [t for t in self._traces if session_id is None or t["session_id"] == session_id]

    def dataset_size(self, name):
        return self.datasets.get(name)

    def score_count(self, name):
        return self.scores.get(name, 0)

    def run_count(self, dataset):
        return self.runs.get(dataset, 0)


def trace(session=None, user=None):
    return {"id": "x", "session_id": session, "user_id": user}


def passed(results):
    return all(ok for _, ok in results)


def test_week_01():
    assert passed(check_traces.week_01(Source([trace("side-by-side"), trace("side-by-side")])))
    assert not passed(check_traces.week_01(Source([trace("side-by-side")])))


def test_week_03():
    assert passed(check_traces.week_03(Source([trace("c1/T1", "c1"), trace("c1/T2", "c1")])))
    assert not passed(check_traces.week_03(Source([trace("c1/T1", "c1"), trace("c2/T2", "c2")])))


def test_week_04():
    full = Source(datasets={"helpdesk": 24}, scores={"human-kind": 3}, runs={"helpdesk": 1})
    assert passed(check_traces.week_04(full))
    thin = Source(datasets={"helpdesk": 12}, scores={"human-kind": 3}, runs={"helpdesk": 1})
    assert not passed(check_traces.week_04(thin))
    assert not passed(check_traces.week_04(Source()))


def test_week_07():
    assert passed(check_traces.week_07(Source([trace(f"project/{n}") for n in range(5)])))
    assert not passed(check_traces.week_07(Source([trace("c1/T1")] * 9)))


def test_run_reports_failure(capsys):
    assert check_traces.run(["week-01"], Source()) == 1
    assert "FAIL" in capsys.readouterr().out
