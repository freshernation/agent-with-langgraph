"""Check your judge against a person's labels, with your real model - given.

    python3 run_judge.py

Twelve replies a person marked good or bad. About twelve model calls.
"""

import json
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from judge import agreement, judge, trustworthy
from models import connect

load_dotenv(find_dotenv(usecwd=True))


def main():
    model = connect()
    labels = json.loads(Path(__file__).with_name("labels.json").read_text())
    judged = []
    for label in labels:
        verdict = judge(model, label["ticket"], label["reply"], label["facts"])
        judged.append(None if verdict is None else verdict.good)
        mark = "?" if verdict is None else ("ok " if verdict.good == label["good"] else "XX ")
        print(mark, label["reply"][:60], "-", verdict.reason if verdict else "could not decide")
    report = agreement(judged, [label["good"] for label in labels])
    print(report)
    print("trust it" if trustworthy(report) else "do not trust it yet")


if __name__ == "__main__":
    main()
