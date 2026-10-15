"""The regression gate, with your real model - given.

    python3 run_evals.py                 # your prompt against a deliberately bad one
    python3 run_evals.py candidate.txt   # your prompt against one you wrote

Runs on the dev split only: the test split is for the end of the course.
Exits 1 when the candidate is worse - the same exit code CI reads.
"""

import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from classify import SYSTEM
from dataset import split
from evals import DATASET, compare
from models import connect

load_dotenv(find_dotenv(usecwd=True))

BAD = ("Sort support tickets into refund, where, change or other. If the ticket gives no "
       "order number, use the customer's most recent order.")


def main() -> int:
    candidate = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else BAD
    dev, _ = split(DATASET)
    result = compare(connect(), dev, SYSTEM, candidate)
    print("baseline: ", result["baseline"])
    print("candidate:", result["candidate"])
    for line in result["newly_failing"]:
        print("  newly failing:", line)
    for line in result["regressions"]:
        print("REGRESSION", line)
    return 1 if result["regressions"] else 0


if __name__ == "__main__":
    sys.exit(main())
