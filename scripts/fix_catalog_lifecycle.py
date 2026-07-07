"""Fix two lifecycle misclassifications in LIBRARY_META.REGISTRY.CATALOG (D13 + D14).

The CATALOG view derives LIFECYCLE (scouted/queued/sampled/landed/modeled/empty/failed/stale)
from run status + landing rows + message heuristics. Two branches misfire:

  D14  the `LOWER(MESSAGE) LIKE '% sample%'` heuristic (meant to catch a bounded/capped LOAD)
       also matches a source whose DESCRIPTION contains the word "sample". FED_FHFA_NMDB has a
       clean success run of 19,054,246 rows but its message ends "...drawn from the NMDB 5%
       national sample", so the 3rd-largest table in the Library reads 'sampled' and is excluded
       from every landed/modeled front-door query. FIX: the message-word 'sample'/'proof slice'
       signals only count when the landing is actually small (<= 200,000 rows; the largest
       round-number cap is 100,000). A 19M-row load is never a bounded sample. The round-number
       and 'bulk portal load' signals are untouched.

  D13  the lifecycle CASE handles STATUS in (success, failed, empty) but has NO branch for any
       other status. FED_CMS_OPEN_PAYMENTS_2022 has 13,250,000 landing rows but its only runs are
       STATUS='error' ("I/O operation on closed file"), so it falls through every branch to
       'scouted' -- reading as "never attempted" when a load was attempted and errored. FIX: any
       non-standard run status (e.g. 'error') reads 'failed' (data-first: a load happened), not
       'scouted'. This does NOT promote it into the reading room -- the data is from failed streams
       and still needs a real reload (scripts/reconcile_op2022.py) -- it just stops the lie.

CRITICAL: the rebuild uses COPY GRANTS. A plain CREATE OR REPLACE VIEW strips every grant on the
view (this is exactly why the read-only role lost SELECT on CATALOG -- audit D04). COPY GRANTS
preserves them, including the RIPPLE_READER SELECT just applied.

    python3 scripts/fix_catalog_lifecycle.py            # PREVIEW: snapshot DDL + show every source whose lifecycle changes
    python3 scripts/fix_catalog_lifecycle.py --apply     # rebuild the view (COPY GRANTS) + verify

Idempotent: re-running --apply on the already-fixed view is a drift-abort (the anchors won't match),
so it fails safe rather than double-patching. Rollback DDL is snapshotted every run to outputs/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

VIEW = "LIBRARY_META.REGISTRY.CATALOG"

# --- the three body transforms (whitespace-tolerant; each MUST match exactly once) ---

_SAMPLED_RE = re.compile(
    r"WHEN lr\.STATUS='success' AND \(\s*"
    r"LOWER\(lr\.MESSAGE\) LIKE '%proof slice%'\s*"
    r"OR LOWER\(lr\.MESSAGE\) LIKE 'bulk portal load%of % rows\.'\s*"
    r"OR LOWER\(lr\.MESSAGE\) LIKE '% sample%'\s*"
    r"OR lr\.run_rows IN \(500,1000,2000,5000,10000,25000,50000,100000\)\s*"
    r"\) THEN 'sampled'"
)
_SAMPLED_NEW = (
    "WHEN lr.STATUS='success' AND (\n"
    "                 LOWER(lr.MESSAGE) LIKE 'bulk portal load%of % rows.'\n"
    "              OR lr.run_rows IN (500,1000,2000,5000,10000,25000,50000,100000)\n"
    "              OR ((LOWER(lr.MESSAGE) LIKE '%proof slice%' OR LOWER(lr.MESSAGE) LIKE '% sample%')\n"
    "                   AND COALESCE(l.land_rows, lr.run_rows, 0) <= 200000)  -- D14: 'sample' in a source DESCRIPTION (NMDB 5% national sample, 19M rows) is not a bounded LOAD sample\n"
    "             ) THEN 'sampled'"
)

_ISSAMPLE_RE = re.compile(
    r"\(lr\.STATUS='success' AND \(\s*"
    r"LOWER\(lr\.MESSAGE\) LIKE '%proof slice%' OR LOWER\(lr\.MESSAGE\) LIKE '% sample%'\s*"
    r"OR lr\.run_rows IN \(500,1000,2000,5000,10000,25000,50000,100000\)\)\) AS IS_SAMPLE"
)
_ISSAMPLE_NEW = (
    "(lr.STATUS='success' AND (\n"
    "         lr.run_rows IN (500,1000,2000,5000,10000,25000,50000,100000)\n"
    "      OR ((LOWER(lr.MESSAGE) LIKE '%proof slice%' OR LOWER(lr.MESSAGE) LIKE '% sample%')\n"
    "           AND COALESCE(l.land_rows, lr.run_rows, 0) <= 200000))) AS IS_SAMPLE"
)

_ERROR_RE = re.compile(
    r"(WHEN lr\.STATUS='empty' THEN 'empty'\s*\n)(\s*WHEN r\.INCLUDE='Y' THEN 'queued')"
)
_ERROR_NEW = (
    r"\1        WHEN lr.STATUS IS NOT NULL THEN 'failed'  -- D13: a run status other than "
    r"success/failed/empty (e.g. 'error') = a load was ATTEMPTED; 'failed', not 'scouted'\n\2"
)


def _sub_once(rx: re.Pattern, repl: str, s: str, label: str) -> str:
    out, n = rx.subn(repl, s)
    if n != 1:
        raise SystemExit(
            f"DRIFT ABORT: transform '{label}' matched {n} times (expected 1). "
            f"The live CATALOG view is not the shape this script was written for -- "
            f"re-pull GET_DDL and re-derive the transforms before applying."
        )
    return out


def _transform(raw_ddl: str) -> tuple[str, str, str]:
    """Return (apply_full_ddl, preview_body, rollback_full_ddl)."""
    header, sep, body = raw_ddl.partition("\n) as\n")
    if not sep:
        raise SystemExit("DRIFT ABORT: could not find the column-list terminator '\\n) as\\n'.")
    if "create or replace view CATALOG(" not in header:
        raise SystemExit("DRIFT ABORT: unexpected view header.")
    body = body.rstrip().rstrip(";")

    fixed_body = _sub_once(_SAMPLED_RE, _SAMPLED_NEW, body, "D14-sampled")
    fixed_body = _sub_once(_ISSAMPLE_RE, _ISSAMPLE_NEW, fixed_body, "D14-is_sample")
    fixed_body = _sub_once(_ERROR_RE, _ERROR_NEW, fixed_body, "D13-error-branch")

    qhead = header.replace("create or replace view CATALOG(",
                           f"create or replace view {VIEW}(", 1)
    apply_full = f"{qhead}\n) COPY GRANTS as\n{fixed_body}"
    # rollback = the ORIGINAL body, also qualified + COPY GRANTS so it's directly runnable
    rollback_full = f"{qhead}\n) COPY GRANTS as\n{body}"
    return apply_full, fixed_body, rollback_full


def _lifecycle_map(cur, query: str) -> dict:
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    si, li = cols.index("SOURCE_ID"), cols.index("LIFECYCLE")
    return {r[si]: r[li] for r in cur.fetchall()}


def main() -> int:
    ap = argparse.ArgumentParser(description="Fix CATALOG lifecycle D13/D14")
    ap.add_argument("--apply", action="store_true", help="rebuild the view (default: preview)")
    args = ap.parse_args()

    from ripple.common import connect
    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT GET_DDL('VIEW','{VIEW}')")
    raw = cur.fetchone()[0]
    apply_full, preview_body, rollback_full = _transform(raw)

    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    roll = REPO / "outputs" / f"_rollback_CATALOG_view_lifecycle_{ts}.sql"
    roll.write_text(rollback_full + ";\n")
    print(f"  rollback DDL snapshotted -> {roll}")

    # Preview: run the fixed body as a plain SELECT and diff LIFECYCLE vs the live view.
    old = _lifecycle_map(cur, f"SELECT SOURCE_ID, LIFECYCLE FROM {VIEW}")
    new = _lifecycle_map(cur, preview_body)
    movers = {sid: (old.get(sid), new[sid]) for sid in new if old.get(sid) != new[sid]}

    print(f"\n  lifecycle changes: {len(movers)} source(s) move")
    from collections import Counter
    trans = Counter(f"{o} -> {n}" for o, n in movers.values())
    for t, c in trans.most_common():
        print(f"    {c:>4}  {t}")

    # Spotlight the two the fix targets.
    for sid in ("fed_fhfa_nmdb", "fed_cms_open_payments_2022"):
        print(f"    [{sid}]  {old.get(sid)} -> {new.get(sid)}")

    if len(movers) <= 60:
        print("\n  every mover:")
        for sid, (o, n) in sorted(movers.items(), key=lambda kv: (kv[1][1], kv[0])):
            print(f"    {o or 'MISSING':<9} -> {n:<9}  {sid}")

    if not args.apply:
        print("\n  PREVIEW only -- nothing changed. Re-run with --apply to rebuild the view.")
        conn.close()
        return 0

    # --- APPLY ---
    print(f"\n  applying (CREATE OR REPLACE VIEW {VIEW} ... COPY GRANTS) ...")
    cur.execute(apply_full)
    print("  view rebuilt.")

    # Verify: grants preserved (COPY GRANTS) + lifecycle now matches the preview.
    cur.execute(f"SHOW GRANTS ON VIEW {VIEW}")
    grants = cur.fetchall()
    readers = [g for g in grants if "RIPPLE_READER" in str(g)]
    print(f"  grants on view: {len(grants)}; RIPPLE_READER SELECT preserved: {bool(readers)}")
    if not readers:
        print("  [!] RIPPLE_READER lost its grant -- COPY GRANTS may not have carried it; "
              "re-run scripts/apply_read_lane.py --apply to restore.")
    live = _lifecycle_map(cur, f"SELECT SOURCE_ID, LIFECYCLE FROM {VIEW}")
    confirmed = sum(1 for sid, (_o, n) in movers.items() if live.get(sid) == n)
    print(f"  post-apply: {confirmed}/{len(movers)} moves confirmed live.")
    print(f"  NMDB={live.get('fed_fhfa_nmdb')}  OP2022={live.get('fed_cms_open_payments_2022')}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
