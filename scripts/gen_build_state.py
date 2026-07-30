#!/usr/bin/env python3
"""Generate build-state.md from LIBRARY_META.BUILD. Deterministic. Zero LLM.

Move 3 of RIPPLE_GOVERN_THYSELF (2026-07-12). build-state.md stops being a
1,600-line hand-typed diary and becomes a printout of the build registry.
If every AI company vanished tomorrow, this still runs.

    python3 scripts/gen_build_state.py            # render to stdout
    python3 scripts/gen_build_state.py --write    # overwrite build-state.md
    python3 scripts/gen_build_state.py --check    # CI lock: regenerate + diff;
                                                  # exit 1 if build-state.md was
                                                  # hand-edited (banner ignored)

Reads only LIBRARY_META.BUILD.* + REGISTRY.V_STATE — runs fine on the READER lane.
FIRST --write: diff against the hand-typed file is printed to
outputs/build_state_DIVERGENCE_<date>.diff — the list of everything the diary
believed that the registry doesn't. Keep it.
"""
from __future__ import annotations

import argparse
import difflib
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))

TARGET = REPO / "build-state.md"

BANNER = """<!-- GENERATED FILE. DO NOT EDIT BY HAND.
     Source: LIBRARY_META.BUILD  |  Generated: {ts}
     To change anything here, change the row and regenerate:
     python3 scripts/gen_build_state.py --write -->
"""


def fetch(cur, sql):
    cur.execute(sql)
    return cur.fetchall()


def render(conn) -> str:
    cur = conn.cursor()
    build_state = fetch(cur, "SELECT METRIC, VALUE FROM LIBRARY_META.BUILD.V_BUILD_STATE ORDER BY 1")
    v_state = fetch(cur, "SELECT METRIC, VALUE FROM LIBRARY_META.REGISTRY.V_STATE ORDER BY METRIC")
    defects = fetch(cur, """
        SELECT SEVERITY, TITLE, AREA, STATUS, LAST_VERDICT,
               TO_VARCHAR(LAST_VERIFIED_AT, 'YYYY-MM-DD'), NOTES
        FROM LIBRARY_META.BUILD.DEFECTS WHERE STATUS='open'
        ORDER BY DECODE(SEVERITY,'blocker',0,'high',1,'medium',2,'low',3), AREA, TITLE""")
    closed = fetch(cur, """
        SELECT TITLE, TO_VARCHAR(CLOSED_AT,'YYYY-MM-DD'), CLOSED_BY
        FROM LIBRARY_META.BUILD.DEFECTS WHERE STATUS IN ('closed','fixed','wontfix','superseded')
        ORDER BY CLOSED_AT DESC NULLS LAST LIMIT 15""")
    actions = fetch(cur, """
        SELECT ACTION_ID, SEQ, SCRIPT_PATH, STATUS, REQUIRES_HUMAN, REVERSIBLE, DEPENDS_ON, DESCRIPTION
        FROM LIBRARY_META.BUILD.PENDING_ACTIONS
        WHERE STATUS IN ('pending','previewed') ORDER BY SEQ""")
    applied = fetch(cur, """
        SELECT ACTION_ID, SCRIPT_PATH, TO_VARCHAR(APPLIED_AT,'YYYY-MM-DD'), APPLIED_BY
        FROM LIBRARY_META.BUILD.PENDING_ACTIONS WHERE STATUS='applied'
        ORDER BY APPLIED_AT DESC NULLS LAST""")
    parked = fetch(cur, """
        SELECT HEAT, TITLE, NOTE, STATUS, SUPERSEDED_BY FROM LIBRARY_META.BUILD.PARKED
        ORDER BY DECODE(STATUS,'parked',0,1), DECODE(HEAT,'hot',0,1), TITLE""")
    policy = fetch(cur, """
        SELECT POLICY_KEY, STATEMENT, TO_VARCHAR(DECIDED_AT,'YYYY-MM-DD')
        FROM LIBRARY_META.BUILD.POLICY
        WHERE STATUS='active'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY POLICY_KEY ORDER BY RECORDED_AT DESC) = 1
        ORDER BY POLICY_KEY""")

    L = []
    L.append("# Build State")
    L.append("")
    L.append("**This file is a printout, not a diary.** Canonical truth: "
             "`SELECT * FROM LIBRARY_META.BUILD.V_BUILD_STATE;` (build) and "
             "`LIBRARY_META.REGISTRY.V_STATE` (data). Numbers below were live at generation.")
    L.append("")

    L.append("## BUILD STATE (V_BUILD_STATE)")
    for m, v in build_state:
        L.append(f"- {m}: **{v}**")
    L.append("")

    L.append("## DATA STATE (V_STATE)")
    for m, v in v_state:
        L.append(f"- {m}: {v}")
    L.append("")

    L.append("## OPEN DEFECTS")
    L.append("")
    L.append("| sev | area | defect | last verdict | verified |")
    L.append("|---|---|---|---|---|")
    for sev, title, area, _status, verdict, ver_at, _notes in defects:
        L.append(f"| {sev} | {area} | {title} | {verdict or 'never verified'} | {ver_at or '-'} |")
    L.append("")
    L.append("Re-verify: `python3 scripts/verify_defects.py` — 'clear' is a recommendation; "
             "a human closes.")
    L.append("")

    if closed:
        L.append("## RECENTLY CLOSED")
        for title, at, by in closed:
            L.append(f"- {title} — closed {at or '?'} by {by or '?'}")
        L.append("")

    L.append("## PENDING ACTIONS (dependency order)")
    L.append("")
    L.append("| id | seq | action | flags | depends on |")
    L.append("|---|---|---|---|---|")
    for aid, seq, path, _status, human, reversible, deps, _desc in actions:
        flags = " ".join(f for f in [
            "HUMAN" if human else "", "IRREVERSIBLE" if not reversible else ""] if f) or "-"
        L.append(f"| {aid} | {seq} | `{path}` | {flags} | {deps or '-'} |")
    L.append("")
    if applied:
        L.append("Applied: " + "; ".join(
            f"{aid} ({at or '?'} by {by or '?'})" for aid, _p, at, by in applied))
        L.append("")

    L.append("## PARKED IDEAS")
    for heat, title, note, status, superseded in parked:
        if status == "parked":
            L.append(f"- [IDEA — {heat.upper()}] {title}" + (f" | WHY: {note}" if note else ""))
        else:
            L.append(f"- [{status.upper()}] {title}"
                     + (f" | superseded by: {superseded}" if superseded else ""))
    L.append("")

    L.append("## STANDING POLICY")
    for key, stmt, decided in policy:
        L.append(f"- **{key}** ({decided or '?'}): {stmt}")
    L.append("")

    nxt = next(((aid, path) for aid, _s, path, _st, _h, _r, _d, _de in actions), None)
    L.append("## NEXT ACTION")
    L.append(f"{nxt[0]}: `{nxt[1]}`" if nxt else "Queue drained.")
    L.append("")
    return "\n".join(L)


def strip_banner(text: str) -> str:
    lines = text.splitlines()
    out, skipping = [], False
    for ln in lines:
        if ln.startswith("<!-- GENERATED FILE"):
            skipping = True
        if not skipping:
            out.append(ln)
        if skipping and ln.rstrip().endswith("-->"):
            skipping = False
    return "\n".join(out).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Render build-state.md from LIBRARY_META.BUILD.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true", help="overwrite build-state.md")
    g.add_argument("--check", action="store_true",
                   help="exit 1 if build-state.md differs from a fresh render (banner ignored)")
    args = ap.parse_args()

    import snow  # noqa: E402
    conn = snow.connect()
    try:
        body = render(conn)
    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    full = BANNER.format(ts=ts) + "\n" + body

    if args.check:
        current = TARGET.read_text() if TARGET.exists() else ""
        if strip_banner(current) != body.strip() + "\n":
            print("DRIFT: build-state.md does not match the registry. Someone hand-edited it, "
                  "or rows changed without a regenerate. Run: "
                  "python3 scripts/gen_build_state.py --write")
            for ln in list(difflib.unified_diff(
                    strip_banner(current).splitlines(), body.splitlines(),
                    "build-state.md", "regenerated", lineterm=""))[:60]:
                print(ln)
            return 1
        print("build-state.md matches the registry.")
        return 0

    if args.write:
        old = TARGET.read_text() if TARGET.exists() else ""
        if old and "GENERATED FILE" not in old:
            # the payoff moment: what the hand-typed diary believed that the registry doesn't
            diff_path = REPO / "outputs" / f"build_state_DIVERGENCE_{ts[:10]}.diff"
            diff = "\n".join(difflib.unified_diff(
                old.splitlines(), full.splitlines(),
                "build-state.md (hand-typed)", "build-state.md (generated)", lineterm=""))
            diff_path.write_text(diff + "\n")
            print(f"hand-typed diary diffed to {diff_path} — keep it.")
        TARGET.write_text(full)
        print(f"wrote {TARGET} ({len(full.splitlines())} lines, was "
              f"{len(old.splitlines()) if old else 0})")
        return 0

    print(full)
    return 0


if __name__ == "__main__":
    sys.exit(main())
