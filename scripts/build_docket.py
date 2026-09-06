#!/usr/bin/env python3
"""Build the docket: one canonical list of every idea, plus views.

WHY THIS EXISTS
The ideas lived in four date-stamped CSVs from 2026-09-05 that all held the same
150 rows with different columns. A date in the filename means the list forks
every time someone regenerates it, and the four copies had already drifted:
one used `#`, one used `id`, and `where_it_stands` held 89 distinct strings for what is
really six states. Picking what to investigate next meant reading four files and
guessing which was current.

THE SHAPE
`docket/docket.csv` is the one file anyone edits. No date in the name,
so git history is the versioning. Every other view is generated from it and
should never be hand-edited.

    docket/docket.csv        the canonical list, edit this
    docket/DOCKET.md         the readable board, grouped by state
    docket/docket_open.csv   only what is still worth picking up

WHERE_IT_STANDS is one of seven fixed phrases. Free text is where a list
goes to die, so these never vary:

    open        nobody has run it
    partial     started, not finished
    confirmed   ran, the number held up
    modest      ran, the signal is thin but real
    dead        ran, the leg is missing or the answer is no
    merged      folded into another entry

NEEDS names the data hole standing in the way, so the docket and the
backfill plan point at each other instead of drifting apart.

PROBE points at the report directory that ran it, discovered by matching the
leading id on folders under reports/.

USAGE
    python scripts/build_docket.py            # rebuild the views
    python scripts/build_docket.py --import   # first build, from the 2026-09-05 CSVs
"""
from __future__ import annotations

import argparse
import csv
import glob
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCKET_CSV = REPO / "docket" / "docket.csv"
PAGE = REPO / "docket" / "DOCKET.md"
OPEN_CSV = REPO / "docket" / "docket_open.csv"

FIELDS = ["id", "title", "question", "why_it_matters", "where_it_stands", "needs",
          "tables", "rows", "time_window", "effort", "watch_out", "probe"]

# Every label says what it means. No word here needs a glossary.
STANDS = ["not started", "part done", "found something", "found a little",
          "nothing there", "missing a piece", "same as another"]
STANDS_LABEL = {
    "not started": "Not started",
    "part done": "Part done",
    "found something": "Found something",
    "found a little": "Found a little",
    "nothing there": "Ran it, nothing there",
    "missing a piece": "Can't answer yet, a piece is missing",
    "same as another": "Same as another entry",
}
OPEN_STATES = ("not started", "part done")

# 89 free-text status strings map onto the six. Order matters: the first
# pattern that matches wins, so the traps come first. Two traps in particular:
# "Not checked yet" contains "checked", and "No pattern found" means it RAN and
# the answer was no, which is dead, not open.
NORMALISE = [
    (r"^not checked|^too early", "not started"),
    (r"^merged", "same as another"),
    (r"^partially checked|^setup works|^confirmed the setup works|^found \d+ so far"
     r"|only a few months|needs a real run", "part done"),
    # a piece is missing is not the same as there is nothing there
    (r"isn.t loaded|isn.t usable|not in a usable|don.t exist|is empty"
     r"|only has \d+ records|data isn.t|can.t currently tell|not loaded"
     r"|no full list|aren.t usable|doesn.t line up|don.t line up|no overlap"
     r"|records aren.t|ownership records", "missing a piece"),
    (r"^dead end", "nothing there"),
    (r"no difference|no pattern|no relationship|no real effect|no real pattern"
     r"|none found|came back clean|no clear pattern|turned out|false alarm"
     r"|opposite of expected|not on prescriptions", "nothing there"),
    (r"modest|weak|real but small|small group|small number|unclear|one state"
     r"|cuts both ways", "found a little"),
    (r"^confirmed|^checked", "found something"),
]


def read_where_it_stands(raw: str) -> str:
    s = (raw or "").strip().lower()
    for pat, out in NORMALISE:
        if re.search(pat, s):
            return out
    return "open"


def find_probes() -> dict[str, str]:
    """Map an id to the report directory that ran it, by its leading number."""
    out: dict[str, str] = {}
    for d in glob.glob(str(REPO / "reports" / "*" / "*") + "/"):
        m = re.match(r"(E?\d+)_", os.path.basename(d.rstrip("/")))
        if m:
            out.setdefault(m.group(1), str(Path(d.rstrip("/")).relative_to(REPO)))
    return out


def import_legacy() -> list[dict]:
    """One-time: fold the four 2026-09-05 CSVs into the canonical shape."""
    src = REPO / "reports" / "hunch_master_spreadsheet_2026-09-05.csv"
    if not src.exists():
        sys.exit(f"cannot import, missing {src}")
    probes = find_probes()
    out = []
    for r in csv.DictReader(src.open()):
        raw = (r.get("where_it_stands") or "").strip()
        out.append({
            "id": r["#"],
            "title": (r.get("who's involved") or "").strip(),
            "question": (r.get("the plain question") or "").strip(),
            "why_it_matters": (r.get("why it matters") or "").strip(),
            "where_it_stands": read_where_it_stands(raw),
            "needs": "",
            "tables": (r.get("exact warehouse tables") or "").strip(),
            "rows": (r.get("total rows") or "").strip(),
            "time_window": (r.get("time window") or "").strip(),
            "effort": (r.get("effort to check") or "").strip(),
            # the original free text is the finding, so it is kept, not thrown away
            "watch_out": (r.get("watch out for") or "").strip() or raw,
            "probe": probes.get(r["#"], ""),
        })
    return out


def load() -> list[dict]:
    with DOCKET_CSV.open() as fh:
        return list(csv.DictReader(fh))


def save(rows: list[dict]) -> None:
    DOCKET_CSV.parent.mkdir(exist_ok=True)
    with DOCKET_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def refresh_probes(rows: list[dict]) -> int:
    probes = find_probes()
    n = 0
    for r in rows:
        found = probes.get(r["id"], "")
        if found and r.get("probe") != found:
            r["probe"] = found
            n += 1
    return n


def _effort(row: dict) -> str:
    """quick, medium or skip. Anything else is treated as medium."""
    e = (row.get("effort") or "").split("—")[0].strip().lower()
    return e if e in ("quick", "medium", "skip") else "medium"


def _size(row: dict) -> tuple[int, int]:
    """How big a job it looks: how many tables, then how many rows.

    Not a promise. Two tables and a hundred thousand rows is a morning; six
    tables and forty million is not. It is the only ordering the sheet supports
    without someone re-timing all 150 by hand.
    """
    tables = len([t for t in (row.get("tables") or "").split("|") if t.strip()])
    digits = re.sub(r"[^0-9]", "", row.get("rows") or "")
    return (tables or 99, int(digits) if digits else 10 ** 12)


def _startable(rows: list[dict]) -> list[dict]:
    """Only entries that actually ask something.

    Two rows carry a note where the question should be, e.g. "Nothing to
    compare yet, program just started". Those are fine in the sheet and wrong
    at the top of the page, where every line has to be pickable.
    """
    return [r for r in rows if (r.get("question") or "").strip().endswith("?")]


def _line(r: dict) -> str:
    q = (r.get("question") or "").replace("|", ";").strip()
    why = (r.get("why_it_matters") or "").replace("|", ";").strip()
    return f"| {r['id']} | {q} | {why} |"


def write_views(rows: list[dict]) -> None:
    openish = [r for r in rows if r["where_it_stands"] in OPEN_STATES]
    with OPEN_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in sorted(openish, key=lambda x: (_effort(x), x["id"])):
            w.writerow({k: r.get(k, "") for k in FIELDS})

    waiting = [r for r in openish if r.get("needs")]
    ready = sorted((r for r in openish if not r.get("needs")), key=_size)
    small = ready[:12]
    bigger = ready[12:]
    done = [r for r in rows if r["where_it_stands"] in ("found something", "found a little")]
    stopped = [r for r in rows if r["where_it_stands"] in ("nothing there", "same as another")]
    stuck = [r for r in rows if r["where_it_stands"] == "missing a piece"]

    HEAD = "| # | the question | why it matters |\n|---|---|---|"
    L = ["# What to look into next", "",
         "Pick a line. Every one is a question the data could answer.", "",
         f"**{len(openish)} still open.** {len(ready)} could run today, "
         f"{len(waiting)} are waiting on missing data.", "",
         f"{len(done)} already answered. {len(stopped)} ran and came back empty. "
         f"{len(stuck)} are stuck on a missing piece.", "",
         "---", ""]

    L += ["## Start here", "",
          "The five smallest jobs with nothing missing.",
          "Fewest tables, fewest rows, so the answer comes back fast.", "",
          "| # | the question | why it matters | size |", "|---|---|---|---|"]
    for r in _startable(small)[:5]:
        t, _ = _size(r)
        q = (r.get("question") or "").replace("|", ";").strip()
        why = (r.get("why_it_matters") or "").replace("|", ";").strip()
        tw = "1 table" if t == 1 else f"{t} tables"
        L.append(f"| {r['id']} | {q} | {why} | {tw}, {r.get('rows') or '?'} rows |")
    L += ["", "---", ""]

    L += [f"## Small — {len(small)}", "",
          "Few tables, not much data. Good for a short sitting.", "", HEAD]
    for r in small:
        L.append(_line(r))
    L += [""]

    L += [f"## Bigger — {len(bigger)}", "",
          "The data is there. It is just more of it.", "",
          "<details><summary>open the list</summary>", "", HEAD]
    for r in bigger:
        L.append(_line(r))
    L += ["", "</details>", ""]

    L += [f"## Waiting on data — {len(waiting)}", "",
          "The question is fine. Something is missing from the warehouse.",
          "The last column says what.", "",
          "| # | the question | what it needs |", "|---|---|---|"]
    for r in waiting:
        q = (r.get("question") or "").replace("|", ";")
        L.append(f"| {r['id']} | {q} | {r['needs']} |")
    L += [""]

    L += [f"## Already answered — {len(done)}", "",
          "Ran, and something real came back.", "",
          "<details><summary>open the list</summary>", "",
          "| # | the question | what came back |", "|---|---|---|"]
    for r in done:
        q = (r.get("question") or "").replace("|", ";")
        w = (r.get("watch_out") or "").replace("|", ";")
        L.append(f"| {r['id']} | {q} | {w} |")
    L += ["", "</details>", ""]

    L += [f"## Stuck on a missing piece — {len(stuck)}", "",
          "The question is good. Something the warehouse holds is unusable.",
          "The last column says what.", "",
          "| # | the question | what is missing |", "|---|---|---|"]
    for r in stuck:
        q = (r.get("question") or "").replace("|", ";")
        w = (r.get("watch_out") or "").replace("|", ";")
        L.append(f"| {r['id']} | {q} | {w} |")
    L += [""]

    L += [f"## Ran it, nothing there — {len(stopped)}", "",
          "Someone checked and there was no pattern.",
          "Kept so nobody spends a day rediscovering it.", "",
          "<details><summary>open the list</summary>", "",
          "| # | the question | what came back |", "|---|---|---|"]
    for r in stopped:
        q = (r.get("question") or "").replace("|", ";")
        w = (r.get("watch_out") or "").replace("|", ";")
        L.append(f"| {r['id']} | {q} | {w} |")
    L += ["", "</details>", "",
          "---", "",
          "The full spreadsheet, with tables and row counts, is",
          "`docket/docket.csv`. This page is built from it.", ""]

    PAGE.write_text("\n".join(L))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--import", dest="do_import", action="store_true",
                    help="first build, from the 2026-09-05 CSVs")
    ap.add_argument("--force", action="store_true",
                    help="with --import, replace an existing docket")
    args = ap.parse_args()

    if args.do_import:
        if DOCKET_CSV.exists() and not args.force:
            sys.exit(f"{CATALOG} already exists; pass --force to replace it")
        rows = import_legacy()
        save(rows)
        print(f"imported {len(rows)} entries")
    else:
        rows = load()
        moved = refresh_probes(rows)
        save(rows)
        if moved:
            print(f"linked {moved} entries to a probe report")

    write_views(rows)
    counts = {s: sum(1 for r in rows if r["where_it_stands"] == s) for s in STANDS}
    print(f"{len(rows)} entries: " + ", ".join(f"{counts[s]} {s}" for s in STANDS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
