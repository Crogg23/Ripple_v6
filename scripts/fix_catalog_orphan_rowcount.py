"""Fix the orphan-schema double-count in LIBRARY_META.REGISTRY.CATALOG.MART_ROW_COUNT
(2026-08-18 census-grid ROW_DISAGREE follow-up).

THE BUG: the `marts` CTE sums ROW_COUNT across EVERY schema in LIBRARY_MARTS with no
exclusion beyond INFORMATION_SCHEMA itself:

    FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
    WHERE POSITION('__' IN TABLE_NAME) > 0 AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
    GROUP BY 1

Three schemas are debris from the 2026-07-01 / 2026-07-31 mart cleanups that relocated
or superseded a batch of models but never dropped their old physical tables:
_RESTORE_20260701 (12 tables), _RESTORE_20260731 (28 tables), UNCATEGORIZED (2 tables)
-- 42 orphan tables, ~342M phantom rows, confirmed live this session. Any live mart whose
table name shares the same SOURCE_ID suffix as an orphan gets that orphan's rows silently
summed into MART_ROW_COUNT (most land near exactly 2x live). Confirmed 16 currently-live
marts hit this. A second, worse effect: 19 SOURCE_IDs exist ONLY as orphan-schema tables
(no live mart at all) -- those currently read LIFECYCLE='modeled' with a phantom row count
lifted from a table that's actually retired/deleted (e.g. int_gleif_rr, whose live table
was dropped in the 2026-08-11 GLEIF repair). This fix corrects both: it will also flip
those 19 SOURCE_IDs off 'modeled' onto whatever their landing status actually is.

FIX: exclude the two known orphan schema patterns from the `marts` CTE's WHERE clause.
Scoped to the exact 3 schemas confirmed orphaned this session (not "any underscore-
prefixed schema") to avoid silently excluding some future legitimate schema.

CRITICAL: the rebuild uses COPY GRANTS (see scripts/fix_catalog_lifecycle.py D04 note --
a plain CREATE OR REPLACE VIEW strips every grant, which is exactly how the read-only
role lost SELECT on CATALOG before).

    python scripts/fix_catalog_orphan_rowcount.py            # PREVIEW: diff MART_ROW_COUNT / LIFECYCLE / _REAL_MART
    python scripts/fix_catalog_orphan_rowcount.py --apply     # rebuild the view (COPY GRANTS) + verify

Idempotent: re-running --apply on the already-fixed view is a drift-abort (the anchor
won't match), so it fails safe rather than double-patching. Rollback DDL is snapshotted
every run to outputs/.
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

ORPHAN_SCHEMAS = ("_RESTORE_20260701", "_RESTORE_20260731", "UNCATEGORIZED")

_MARTS_WHERE_RE = re.compile(
    r"(FROM LIBRARY_MARTS\.INFORMATION_SCHEMA\.TABLES\s*\n\s*"
    r"WHERE POSITION\('__' IN TABLE_NAME\) > 0 AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA')"
    r"(\s*\n\s*GROUP BY 1\s*\n\),)"
)


def _marts_where_new(m: re.Match) -> str:
    excl = " AND ".join(f"TABLE_SCHEMA <> '{s}'" for s in ORPHAN_SCHEMAS)
    return (
        f"{m.group(1)}\n"
        f"      -- 2026-08-18 fix: exclude orphan backup/uncategorized schemas left behind by the\n"
        f"      -- 2026-07-01/07-31 mart cleanups (42 leftover tables, ~342M phantom rows) so their\n"
        f"      -- row counts stop getting silently summed into a live mart with the same SOURCE_ID suffix.\n"
        f"      AND {excl}"
        f"{m.group(2)}"
    )


def _sub_once(rx: re.Pattern, repl, s: str, label: str) -> str:
    out, n = rx.subn(repl, s)
    if n != 1:
        raise SystemExit(
            f"DRIFT ABORT: transform '{label}' matched {n} times (expected 1). "
            f"The live CATALOG view is not the shape this script was written for -- "
            f"re-pull GET_DDL and re-derive the transform before applying."
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

    fixed_body = _sub_once(_MARTS_WHERE_RE, _marts_where_new, body, "orphan-schema-exclude")

    qhead = header.replace("create or replace view CATALOG(",
                           f"create or replace view {VIEW}(", 1)
    apply_full = f"{qhead}\n) COPY GRANTS as\n{fixed_body}"
    rollback_full = f"{qhead}\n) COPY GRANTS as\n{body}"
    return apply_full, fixed_body, rollback_full


def _snapshot(cur, query: str) -> dict:
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    si = cols.index("SOURCE_ID")
    idx = {c: i for i, c in enumerate(cols)}
    out = {}
    for r in cur.fetchall():
        out[r[si]] = {
            "MART_ROW_COUNT": r[idx["MART_ROW_COUNT"]],
            "LIFECYCLE": r[idx["LIFECYCLE"]],
            "_REAL_MART": r[idx["_REAL_MART"]],
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Fix CATALOG orphan-schema MART_ROW_COUNT double-count")
    ap.add_argument("--apply", action="store_true", help="rebuild the view (default: preview)")
    args = ap.parse_args()

    from ripple.common import connect
    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT GET_DDL('VIEW','{VIEW}')")
    raw = cur.fetchone()[0]
    apply_full, preview_body, rollback_full = _transform(raw)

    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    roll = REPO / "outputs" / f"_rollback_CATALOG_view_orphan_rowcount_{ts}.sql"
    roll.write_text(rollback_full + ";\n")
    print(f"  rollback DDL snapshotted -> {roll}")

    old = _snapshot(cur, f"SELECT SOURCE_ID, MART_ROW_COUNT, LIFECYCLE, _REAL_MART FROM {VIEW}")
    new = _snapshot(cur, f"SELECT SOURCE_ID, MART_ROW_COUNT, LIFECYCLE, _REAL_MART FROM ({preview_body})")

    row_movers = {sid: (old[sid]["MART_ROW_COUNT"], new[sid]["MART_ROW_COUNT"])
                  for sid in new if old.get(sid, {}).get("MART_ROW_COUNT") != new[sid]["MART_ROW_COUNT"]}
    lifecycle_movers = {sid: (old.get(sid, {}).get("LIFECYCLE"), new[sid]["LIFECYCLE"])
                         for sid in new if old.get(sid, {}).get("LIFECYCLE") != new[sid]["LIFECYCLE"]}

    print(f"\n  MART_ROW_COUNT changes: {len(row_movers)} source(s)")
    for sid, (o, n) in sorted(row_movers.items()):
        print(f"    {sid:<48} {str(o):>14} -> {str(n):>14}")

    print(f"\n  LIFECYCLE changes: {len(lifecycle_movers)} source(s)")
    from collections import Counter
    trans = Counter(f"{o} -> {n}" for o, n in lifecycle_movers.values())
    for t, c in trans.most_common():
        print(f"    {c:>4}  {t}")
    if len(lifecycle_movers) <= 40:
        for sid, (o, n) in sorted(lifecycle_movers.items()):
            print(f"    {sid:<48} {str(o):<10} -> {n}")

    if not args.apply:
        print("\n  PREVIEW only -- nothing changed. Re-run with --apply to rebuild the view.")
        conn.close()
        return 0

    # --- APPLY ---
    print(f"\n  applying (CREATE OR REPLACE VIEW {VIEW} ... COPY GRANTS) ...")
    cur.execute(apply_full)
    print("  view rebuilt.")

    cur.execute(f"SHOW GRANTS ON VIEW {VIEW}")
    grants = cur.fetchall()
    readers = [g for g in grants if "RIPPLE_READER" in str(g)]
    print(f"  grants on view: {len(grants)}; RIPPLE_READER SELECT preserved: {bool(readers)}")
    if not readers:
        print("  [!] RIPPLE_READER lost its grant -- COPY GRANTS may not have carried it; "
              "re-run scripts/apply_read_lane.py --apply to restore.")

    live = _snapshot(cur, f"SELECT SOURCE_ID, MART_ROW_COUNT, LIFECYCLE, _REAL_MART FROM {VIEW}")
    confirmed_rows = sum(1 for sid, (_o, n) in row_movers.items()
                          if live.get(sid, {}).get("MART_ROW_COUNT") == n)
    confirmed_life = sum(1 for sid, (_o, n) in lifecycle_movers.items()
                          if live.get(sid, {}).get("LIFECYCLE") == n)
    print(f"  post-apply: {confirmed_rows}/{len(row_movers)} row-count fixes confirmed live, "
          f"{confirmed_life}/{len(lifecycle_movers)} lifecycle moves confirmed live.")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
