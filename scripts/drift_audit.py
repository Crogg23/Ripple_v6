"""
drift_audit — how often the rules got broken lately. Heuristic, free, no model calls.

Reads recent Claude Code transcripts for this project and counts, per session:
  dense        assistant messages with a paragraph over 4 lines and no blank line
  unverified   "done / works / fixed / verified" with no "skeptic" / "not verified" / "test" nearby
  reminders    assistant text repeating Chris's own to-do phrasing ("you need to", "don't forget")
  reader_flags times the Stop-hook reader fired
  corrections  Chris messages that read as corrections ("no,", "wrong", "I said", "stop", "again")
Output is a table. A rule that breaks every session is a hook problem, not a wording problem.

  python scripts/drift_audit.py --days 7
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import time

PROJ = os.path.expanduser("~/.claude/projects/c--Code-Ripple-v6")

DONE = re.compile(r"\b(done|works|fixed|verified|solved|all set|you'?re good)\b", re.I)
OK = re.compile(r"(skeptic|not verified|looks done|test(s|ed)? pass|\d+/\d+ pass)", re.I)
REMIND = re.compile(r"\b(you need to|don'?t forget|remember to|you should (also )?(publish|commit))\b", re.I)
CORR = re.compile(r"^\s*(no[,. ]|wrong|stop|again|i said|that'?s not|you lost me|contract\b|hard to read|dense)", re.I)


def texts(msg) -> list[str]:
    c = msg.get("message", {}).get("content")
    if isinstance(c, str):
        return [c]
    if isinstance(c, list):
        return [b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"]
    return []


def dense(t: str) -> bool:
    for para in t.split("\n\n"):
        lines = [l for l in para.split("\n") if l.strip()]
        if len(lines) > 4 and not any(l.startswith(("|", "-", "*", "#")) for l in lines):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    cutoff = time.time() - a.days * 86400
    files = [f for f in glob.glob(os.path.join(PROJ, "*.jsonl")) if os.path.getmtime(f) >= cutoff]
    if not files:
        print(f"no transcripts modified in the last {a.days} days under {PROJ}")
        return 1
    print(f"| session | msgs | dense | unverified | reminders | reader_flags | corrections |")
    print(f"|---|---|---|---|---|---|---|")
    tot = [0] * 6
    for f in sorted(files, key=os.path.getmtime):
        n = d = u = r = rf = c = 0
        with open(f, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                try:
                    m = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                role = m.get("type") or m.get("message", {}).get("role")
                for t in texts(m):
                    if role == "assistant":
                        n += 1
                        if len(t) > 300 and dense(t):
                            d += 1
                        if DONE.search(t) and not OK.search(t):
                            u += 1
                        if REMIND.search(t):
                            r += 1
                        if "reader flagged" in t.lower():
                            rf += 1
                    elif role == "user" and CORR.search(t[:60]):
                        c += 1
        sid = os.path.basename(f)[:8]
        print(f"| {sid} | {n} | {d} | {u} | {r} | {rf} | {c} |")
        for i, v in enumerate((n, d, u, r, rf, c)):
            tot[i] += v
    print(f"| **total** | {tot[0]} | {tot[1]} | {tot[2]} | {tot[3]} | {tot[4]} | {tot[5]} |")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
