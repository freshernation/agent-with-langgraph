"""Week 7 milestone - Project 3: the interview.

Run me:  pytest week-07/milestone -v

The interview itself is Friday. This checks you rehearsed it.
"""

import re


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_two_rehearsals(source):
    text = source("INTERVIEW.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading in ("Rehearsal 1", "Rehearsal 2"):
        part = section(text, heading)
        assert "SIGNAL" in part and "role: interviewer" in part, f"Paste the interviewer's SIGNAL block under {heading}."
        assert re.search(r"design: \d/5", part) and re.search(r"debug: \d/5", part)


def test_what_changes(source):
    part = section(source("INTERVIEW.md"), "What I will do differently on Friday")
    assert len(part.split()) >= 40
