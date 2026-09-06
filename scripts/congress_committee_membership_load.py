#!/usr/bin/env python3
"""Load congressional committee membership BY CONGRESS, 113th to current.

Two @unitedstates/congress-legislators files: committee-membership-current.yaml
(committee_code -> [members]) + committees-current.yaml (committee/subcommittee
names). Flattened to one row per (congress, committee_code, bioguide), keyed on
bioguide so it joins straight to POLITICS__MEMBER_CROSSWALK.

WHERE THE HISTORY ACTUALLY COMES FROM, measured 2026-09-06:

  committees-historical.yaml holds NO membership. It is a list of committees that
  once existed -- name, thomas_id, and the congresses each sat in. There are no
  people in it. Reading it would have produced a committee list, not a roster,
  and questions 78 and 84 need the roster.

  The membership history lives in the git history of the CURRENT file. That file
  has 210 commits reaching back to 2012-11-09. Fetching it at a past commit gives
  the roster as it stood that day. The member schema is stable across the whole
  range: bioguide, name, party, rank, title are present in 2013 and today.

  So: one snapshot per congress, taken from inside that congress's term.

TRAP, hit live: the LAST commit in a term is not the roster. The file is EMPTIED
on the way out to make room for the incoming congress. Commit ee290b5d, dated
2021-01-01, has zero committees and zero seats, while the same file six days
earlier had 222 committees and 3,847 seats. So this walks a term's commits
newest-first and takes the first one carrying at least SEAT_FLOOR seats. About
3,800 seats per congress, roughly 27,000 rows for the seven.

WHAT THIS IS NOT: a day-by-day roster. A member who joined and left a committee
inside one congress shows only as of the snapshot. Say "roster as of the end of
the 117th", never "was on the committee in 2021".
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

import pandas as pd
import requests
import yaml

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

from land_frame import land  # noqa: E402

REPO = "unitedstates/congress-legislators"
GH = f"https://raw.githubusercontent.com/{REPO}"
API = f"https://api.github.com/repos/{REPO}"
MEMBERSHIP = "committee-membership-current.yaml"
COMMITTEES = "committees-current.yaml"
SID = "fed_congress_committee_membership"

FIRST_CONGRESS = 113   # earliest with a usable snapshot; the file starts 2012-11
LAST_CONGRESS = 119
# A real roster runs about 3,800 seats. Anything under this is the emptied-out
# file at a term boundary, not a congress with few committees.
SEAT_FLOOR = 2000


def _term(n: int) -> tuple[dt.date, dt.date]:
    """A congress runs Jan 3 of an odd year to Jan 3 two years later."""
    start = dt.date(2013 + 2 * (n - 113), 1, 3)
    return start, dt.date(start.year + 2, 1, 3)


def _seat_count(sha: str) -> int:
    y = _yaml_at(sha, MEMBERSHIP)
    return sum(len(v or []) for v in (y or {}).values()) if y else 0


def snapshots(want: list[int] | None = None) -> dict[int, tuple[str, str]]:
    """congress -> (commit sha, commit date). Newest commit in the term that still
    carries a real roster wins. See the emptied-file trap in the module docstring."""
    commits = []
    page = 1
    while True:
        r = requests.get(f"{API}/commits",
                         params={"path": MEMBERSHIP, "per_page": 100, "page": page},
                         timeout=120)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        commits += batch
        page += 1
    dated = sorted((c["sha"], c["commit"]["committer"]["date"]) for c in commits)
    dated.sort(key=lambda x: x[1])
    print(f"  {len(dated):,} commits touch {MEMBERSHIP}", flush=True)

    picked: dict[int, tuple[str, str]] = {}
    for n in (want or range(FIRST_CONGRESS, LAST_CONGRESS + 1)):
        a, b = _term(n)
        inside = [(sha, when) for sha, when in dated
                  if a <= dt.date.fromisoformat(when[:10]) < b]
        for sha, when in reversed(inside):
            seats = _seat_count(sha)
            if seats >= SEAT_FLOOR:
                picked[n] = (sha, when)
                break
            print(f"    congress {n}: skipping {when[:10]}, only {seats} seats", flush=True)
    return picked


def _yaml_at(sha: str, path: str):
    r = requests.get(f"{GH}/{sha}/{path}", timeout=120)
    r.raise_for_status()
    return yaml.safe_load(r.content)


def flatten(congress: int, sha: str, when: str) -> pd.DataFrame:
    mem = _yaml_at(sha, MEMBERSHIP)
    coms = _yaml_at(sha, COMMITTEES)
    cname = {}
    for c in coms or []:
        tid = c.get("thomas_id")
        if tid:
            cname[tid] = c.get("name", "")
        for sc in c.get("subcommittees", []) or []:
            cname[(tid or "") + sc.get("thomas_id", "")] = f"{c.get('name','')} -- {sc.get('name','')}"
    rows = []
    for code, members in (mem or {}).items():
        for m in (members or []):
            rows.append({
                "CONGRESS": str(congress),
                "SNAPSHOT_DATE": when[:10],
                "SNAPSHOT_SHA": sha,
                "COMMITTEE_CODE": code,
                "COMMITTEE_NAME": cname.get(code, ""),
                "IS_SUBCOMMITTEE": str(len(code) > 4),
                "BIOGUIDE": m.get("bioguide", ""),
                "MEMBER_NAME": m.get("name", ""),
                "PARTY": m.get("party", ""),
                "RANK": str(m.get("rank", "")),
                "TITLE": m.get("title", ""),  # Chair / Ranking Member / Vice Chair / ''
            })
    df = pd.DataFrame(rows)
    print(f"  congress {congress} @ {when[:10]}: {len(df):,} seats, "
          f"{df['COMMITTEE_CODE'].nunique()} committees/subcommittees", flush=True)
    return df


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Load congressional committee membership by congress, 113th to current.")
    ap.add_argument("--congresses", default="",
                    help=f"comma-separated congress numbers (default {FIRST_CONGRESS}-{LAST_CONGRESS})")
    ap.add_argument("--dry-run", action="store_true",
                    help="build the frame and print the shape, land nothing")
    args = ap.parse_args()

    print("=== Congressional committee membership by congress ===", flush=True)
    want = ([int(x) for x in args.congresses.split(",") if x.strip()]
            if args.congresses else list(range(FIRST_CONGRESS, LAST_CONGRESS + 1)))
    picked = snapshots(want)
    missing = [n for n in want if n not in picked]
    if missing:
        raise RuntimeError(f"no snapshot commit found for congress {missing}")

    df = pd.concat([flatten(n, *picked[n]) for n in want], ignore_index=True)
    print(f"\n  total {len(df):,} seats across {df.CONGRESS.nunique()} congresses, "
          f"{df.BIOGUIDE.nunique():,} distinct members", flush=True)

    if args.dry_run:
        print("DRY RUN: nothing landed", flush=True)
        return 0

    result = land(df, SID, f"{GH}/main/{MEMBERSHIP}",
         "Congressional committee + subcommittee membership, 113th-119th; one row = "
         "one member-seat as of that congress's snapshot date.")
    if result.get("status") != "success":
        raise RuntimeError(f"QUALITY GATE FAILED for {SID}: {result}")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
