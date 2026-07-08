#!/usr/bin/env python3
"""Retire the exact-duplicate FED_IRS_EO_BMF landing table (evidence.dev cleanup).

THE PROBLEM
-----------
LIBRARY_RAW.LANDING.FED_IRS_EO_BMF is a DOUBLED load that is fully contained in
LIBRARY_RAW.LANDING.FED_IRS_BMF:

  * FED_IRS_EO_BMF     = 3,949,660 rows / 1,974,830 distinct EIN  (ratio EXACTLY 2.00 --
                         every EIN appears exactly twice, under ONE _SOURCE_RUN_ID stamp)
  * FED_IRS_BMF        = 1,974,830 rows / 1,974,830 distinct EIN  (clean 1-row-per-EIN)
  * every EIN in EO_BMF is already present in BMF (0 missing)

So EO_BMF is redundant: BMF is the same universe of orgs, de-duplicated. Both read
'landed' in CATALOG, which double-counts the IRS EO universe in the front door and in
the connection graph (EO_BMF carries 140 CONNECT edges -- every one of which BMF
already carries to the same 132 partners, so EO_BMF adds zero unique connectivity).

WHAT THIS DOES  (all reversible; snapshots rollback DDL to outputs/ first)
--------------------------------------------------------------------------
RE-PROVES the duplication LIVE before touching anything. Four hard checks + guards;
if ANY fails it ABORTS (it might be a genuine EO subset, not a dup):
  (1) rowcount / distinct-EIN ratio == 2.00 exactly
  (2) EO distinct-EIN == BMF distinct-EIN
  (3) 0 EINs in EO_BMF missing from BMF
  (4) EO_BMF carries a single _SOURCE_RUN_ID stamp
  guards: BMF is one-row-per-EIN and non-empty; every EO EIN appears exactly twice.

Only if all pass, --apply QUARANTINES (never hard-deletes):
  1. CREATE SCHEMA IF NOT EXISTS LIBRARY_RAW.RETIRED
  2. ALTER TABLE ...LANDING.FED_IRS_EO_BMF RENAME TO ...RETIRED.FED_IRS_EO_BMF
     (instant, zero-copy, fully reversible -- data is preserved, just moved out of the
     LANDING schema the CATALOG scans, so it stops reading 'landed')
  3. de-catalog: INGEST_RUNS success -> 'empty' (terminal, never re-tried, never re-lands
     the dup) with a RETIRED_DUP message; SOURCE_REGISTRY INCLUDE 'Y' -> 'N' + NOTES stamp
  Net: CATALOG lifecycle fed_irs_eo_bmf  'landed' -> 'empty', trust_layer 'raw' -> 'none'.

  --prune-edges (opt-in, with --apply): ALSO back up + delete the 140 now-dangling
  CONNECT_EDGES rows referencing FED_IRS_EO_BMF. Verified safe -- BMF carries identical
  reach (140 edges, same 132 partners). Backed up to a table in the CONNECT schema and
  a re-INSERT rollback, so it un-does cleanly. Without this flag the edges are left as-is
  and the preview tells you to prune them or rebuild the graph (`connect all`).

GRANTS: this script does NO `CREATE OR REPLACE VIEW/TABLE` on any read-granted object
(the CATALOG view is untouched). ALTER ... RENAME moves the table WITH its grants, and
row UPDATEs don't touch DDL -- so there is no D04 grant-strip risk and no COPY GRANTS
needed. The edge-backup table is brand new (no grants to preserve).

    python3 scripts/dedup_irs_eo_bmf.py                     # PREVIEW: 4 proofs + exact DDL + rollback path
    python3 scripts/dedup_irs_eo_bmf.py --apply             # quarantine + de-catalog
    python3 scripts/dedup_irs_eo_bmf.py --apply --prune-edges  # + delete the 140 redundant edges

Idempotent: re-running once retired detects the moved table + INCLUDE='N' and exits clean.
Classifier-gated -> Chris runs --apply; the agent only ever runs PREVIEW.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

# --- targets -------------------------------------------------------------------
DUP_SID = "fed_irs_eo_bmf"           # the doubled dup to retire
DUP_TBL = "FED_IRS_EO_BMF"
KEEP_SID = "fed_irs_bmf"             # the clean keeper it is contained in
KEEP_TBL = "FED_IRS_BMF"

RAW_DB = "LIBRARY_RAW"
LANDING = f"{RAW_DB}.LANDING"
RETIRED = f"{RAW_DB}.RETIRED"
DUP_LANDING_FQN = f"{LANDING}.{DUP_TBL}"
DUP_RETIRED_FQN = f"{RETIRED}.{DUP_TBL}"
KEEP_LANDING_FQN = f"{LANDING}.{KEEP_TBL}"

INGEST_RUNS = "LIBRARY_META.INGEST_LOGS.INGEST_RUNS"
REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"
CATALOG = "LIBRARY_META.REGISTRY.CATALOG"
EDGES = 'LIBRARY_META."CONNECT".CONNECT_EDGES'
EDGE_BACKUP = 'LIBRARY_META."CONNECT".ZZ_RETIRED_EDGES_FED_IRS_EO_BMF'

TS = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
ROLLBACK = REPO / "outputs" / f"_rollback_dedup_irs_eo_bmf_{TS}.sql"

RETIRE_MSG = (
    f"[RETIRED_DUP {dt.date.today()}] Not literally empty: this was an EXACT-DUPLICATE "
    f"doubled load (3,949,660 rows = every EIN twice) fully contained in {KEEP_TBL} "
    f"(1,974,830 rows, 1-row-per-EIN). Table quarantined to {DUP_RETIRED_FQN}; run "
    f"demoted success->empty so it stops reading 'landed'. Reversible via "
    f"outputs/_rollback_dedup_irs_eo_bmf_*.sql."
)
NOTE_STAMP = (
    f" || [RETIRED {dt.date.today()} as exact-duplicate of {KEEP_SID}: doubled load "
    f"(2x every EIN), fully contained in {KEEP_TBL}. Table moved to {RETIRED} schema, "
    f"INCLUDE set N. Use {KEEP_SID} instead.]"
)


def _scalar(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchone()[0]


def _table_exists(cur, schema: str, table: str) -> bool:
    return _scalar(
        cur,
        f"SELECT COUNT(*) FROM {RAW_DB}.INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
        (schema.split(".")[-1], table),
    ) > 0


def _already_retired(cur) -> bool:
    """True if a prior --apply already moved the table + demoted the registry."""
    landing_gone = not _table_exists(cur, "LANDING", DUP_TBL)
    retired_present = _table_exists(cur, "RETIRED", DUP_TBL)
    include = _scalar(
        cur, f"SELECT MAX(INCLUDE) FROM {REGISTRY} WHERE SOURCE_ID=%s", (DUP_SID,)
    )
    return landing_gone and retired_present and include == "N"


def _prove(cur) -> dict:
    """Re-prove the duplication live. Returns the measured numbers (all 4 checks)."""
    eo_rows = _scalar(cur, f"SELECT COUNT(*) FROM {DUP_LANDING_FQN}")
    eo_ein = _scalar(cur, f"SELECT COUNT(DISTINCT EIN) FROM {DUP_LANDING_FQN}")
    keep_rows = _scalar(cur, f"SELECT COUNT(*) FROM {KEEP_LANDING_FQN}")
    keep_ein = _scalar(cur, f"SELECT COUNT(DISTINCT EIN) FROM {KEEP_LANDING_FQN}")
    missing = _scalar(
        cur,
        f"SELECT COUNT(*) FROM (SELECT DISTINCT EIN FROM {DUP_LANDING_FQN}) e "
        f"LEFT JOIN (SELECT DISTINCT EIN FROM {KEEP_LANDING_FQN}) b ON e.EIN=b.EIN "
        "WHERE b.EIN IS NULL",
    )
    stamps = _scalar(cur, f"SELECT COUNT(DISTINCT _SOURCE_RUN_ID) FROM {DUP_LANDING_FQN}")
    min_occ = _scalar(
        cur, f"SELECT MIN(c) FROM (SELECT EIN, COUNT(*) c FROM {DUP_LANDING_FQN} GROUP BY EIN)"
    )
    max_occ = _scalar(
        cur, f"SELECT MAX(c) FROM (SELECT EIN, COUNT(*) c FROM {DUP_LANDING_FQN} GROUP BY EIN)"
    )
    ratio = (eo_rows / eo_ein) if eo_ein else None
    return dict(eo_rows=eo_rows, eo_ein=eo_ein, keep_rows=keep_rows, keep_ein=keep_ein,
                missing=missing, stamps=stamps, min_occ=min_occ, max_occ=max_occ, ratio=ratio)


def _check(p: dict) -> list[str]:
    """Return a list of failure reasons; empty list == all proofs pass."""
    fails = []
    if p["ratio"] != 2.0:
        fails.append(f"[1] rowcount/distinct-EIN ratio is {p['ratio']}, not 2.00")
    if p["eo_ein"] != p["keep_ein"]:
        fails.append(f"[2] EO distinct-EIN {p['eo_ein']:,} != BMF distinct-EIN {p['keep_ein']:,}")
    if p["missing"] != 0:
        fails.append(f"[3] {p['missing']:,} EO EIN(s) missing from BMF (not fully contained)")
    if p["stamps"] != 1:
        fails.append(f"[4] EO carries {p['stamps']} run stamps, not a single doubled load")
    if not (p["min_occ"] == 2 and p["max_occ"] == 2):
        fails.append(f"guard: EO EIN occurrences span {p['min_occ']}..{p['max_occ']}, not exactly 2")
    if p["keep_rows"] != p["keep_ein"]:
        fails.append(f"guard: BMF not 1-row-per-EIN ({p['keep_rows']:,} rows vs {p['keep_ein']:,} EIN)")
    if p["keep_ein"] == 0:
        fails.append("guard: BMF is empty -- cannot prove containment")
    return fails


def _run_row(cur):
    """The single success run row for the dup (RUN_ID, STATUS, ROW_COUNT, MESSAGE)."""
    cur.execute(
        f"SELECT RUN_ID, STATUS, ROW_COUNT, MESSAGE FROM {INGEST_RUNS} "
        "WHERE SOURCE_ID=%s ORDER BY STARTED_AT", (DUP_SID,))
    return cur.fetchall()


def _write_rollback(cur, prune_edges: bool):
    ROLLBACK.parent.mkdir(parents=True, exist_ok=True)
    runs = _run_row(cur)
    cur.execute(f"SELECT INCLUDE, NOTES FROM {REGISTRY} WHERE SOURCE_ID=%s", (DUP_SID,))
    reg_row = cur.fetchall()
    inc = reg_row[0][0] if reg_row else None
    with open(ROLLBACK, "w", encoding="utf-8") as f:
        f.write(f"-- Rollback for dedup_irs_eo_bmf ({TS}) -- restores the pre-retirement state.\n")
        f.write(f"-- INGEST_RUNS rows before demote: {runs}\n")
        f.write(f"-- SOURCE_REGISTRY INCLUDE before: {inc}\n\n")
        f.write("-- 1. move the table back into LANDING\n")
        f.write(f"ALTER TABLE {DUP_RETIRED_FQN} RENAME TO {DUP_LANDING_FQN};\n\n")
        f.write("-- 2. restore the ingest run to success (row count 3,949,660)\n")
        f.write(f"UPDATE {INGEST_RUNS} SET STATUS='success', ROW_COUNT=3949660\n")
        f.write(f"  WHERE SOURCE_ID='{DUP_SID}' AND STATUS='empty';\n\n")
        f.write("-- 3. restore the registry include flag\n")
        f.write(f"UPDATE {REGISTRY} SET INCLUDE='Y' WHERE SOURCE_ID='{DUP_SID}';\n")
        f.write("--    (NOTES was appended to; trim the [RETIRED ...] suffix by hand if desired)\n")
        if prune_edges:
            f.write("\n-- 4. restore the 140 CONNECT edges from the backup table\n")
            f.write(f"INSERT INTO {EDGES} SELECT * FROM {EDGE_BACKUP};\n")
    print(f"  rollback DDL snapshotted -> {ROLLBACK}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Retire exact-duplicate FED_IRS_EO_BMF.")
    ap.add_argument("--apply", action="store_true", help="perform the retirement (else preview)")
    ap.add_argument("--prune-edges", action="store_true",
                    help="with --apply: also back up + delete the 140 redundant CONNECT edges")
    args = ap.parse_args()

    mode = "APPLY" if args.apply else "PREVIEW (reads only, no writes)"
    print("=" * 78)
    print(f"DEDUP / RETIRE {DUP_TBL}  --  {mode}")
    print("=" * 78)

    from connect import db
    conn = db.connect()
    cur = conn.cursor()
    try:
        # --- idempotency: already retired? ---
        if _already_retired(cur):
            print(f"\n  ALREADY RETIRED: {DUP_LANDING_FQN} is gone, {DUP_RETIRED_FQN} present, "
                  "registry INCLUDE=N.")
            cur.execute(f"SELECT lifecycle, trust_layer FROM {CATALOG} WHERE source_id=%s", (DUP_SID,))
            print(f"  CATALOG now: {cur.fetchone()}  (expected ('empty','none'))")
            print("  Nothing to do.")
            return 0

        if not _table_exists(cur, "LANDING", DUP_TBL):
            print(f"\n  ABORT: {DUP_LANDING_FQN} does not exist and it is not in a retired state. "
                  "Inspect manually before proceeding.")
            return 2

        # --- RE-PROVE the duplication live ---
        p = _prove(cur)
        print("\n  PROOFS (re-measured live):")
        print(f"    [1] {DUP_TBL}: {p['eo_rows']:,} rows / {p['eo_ein']:,} distinct EIN "
              f"= ratio {p['ratio']:.4f}   (need 2.00)")
        print(f"    [2] distinct EIN  EO {p['eo_ein']:,}  ==  BMF {p['keep_ein']:,}   "
              f"({'MATCH' if p['eo_ein']==p['keep_ein'] else 'MISMATCH'})")
        print(f"    [3] EO EINs missing from BMF: {p['missing']:,}   (need 0)")
        print(f"    [4] distinct _SOURCE_RUN_ID in EO: {p['stamps']}   (need 1)")
        print(f"    guard: every EO EIN occurs {p['min_occ']}..{p['max_occ']}x (need 2..2); "
              f"BMF {p['keep_rows']:,} rows / {p['keep_ein']:,} EIN (1-row-per-EIN: "
              f"{p['keep_rows']==p['keep_ein']})")

        fails = _check(p)
        if fails:
            print("\n  ABORT -- duplication NOT proven; this may be a genuine EO subset, not a dup:")
            for fr in fails:
                print(f"    FAIL {fr}")
            return 2
        print("\n  ALL 4 PROOFS PASS -- EO_BMF is a doubled load fully contained in BMF. Safe to retire.")

        # --- dangling-edge advisory (always shown) ---
        eo_edges = _scalar(cur, f"SELECT COUNT(*) FROM {EDGES} WHERE A=%s OR B=%s", (DUP_TBL, DUP_TBL))
        keep_edges = _scalar(cur, f"SELECT COUNT(*) FROM {EDGES} WHERE A=%s OR B=%s", (KEEP_TBL, KEEP_TBL))
        print(f"\n  CONNECT graph: {DUP_TBL} carries {eo_edges} edges; {KEEP_TBL} carries "
              f"{keep_edges} to the same partners (EO adds ZERO unique reach).")
        if not args.prune_edges:
            print(f"    -> retiring the table leaves those {eo_edges} edges dangling. Re-run with "
                  "--prune-edges to remove them (safe), or rebuild later with `connect all`.")

        # --- show the exact DDL the apply path would run ---
        runs = _run_row(cur)
        print("\n  INGEST_RUNS for the dup (before):")
        for r in runs:
            print("    ", (r[0], r[1], f"{r[2]:,}" if isinstance(r[2], int) else r[2], str(r[3])[:50]))
        print("\n  DDL --apply would run:")
        print(f"    CREATE SCHEMA IF NOT EXISTS {RETIRED};")
        print(f"    ALTER TABLE {DUP_LANDING_FQN} RENAME TO {DUP_RETIRED_FQN};")
        print(f"    UPDATE {INGEST_RUNS} SET STATUS='empty', MESSAGE=<retired_dup> "
              f"WHERE SOURCE_ID='{DUP_SID}' AND STATUS='success';")
        print(f"    UPDATE {REGISTRY} SET INCLUDE='N', NOTES=NOTES||<stamp> "
              f"WHERE SOURCE_ID='{DUP_SID}';")
        if args.prune_edges:
            print(f"    CREATE OR REPLACE TABLE {EDGE_BACKUP} AS "
                  f"SELECT * FROM {EDGES} WHERE A='{DUP_TBL}' OR B='{DUP_TBL}';  -- {eo_edges} rows")
            print(f"    DELETE FROM {EDGES} WHERE A='{DUP_TBL}' OR B='{DUP_TBL}';")

        if not args.apply:
            print("\n  PREVIEW only -- nothing changed. Re-run with --apply (Chris runs this).")
            return 0

        # ============================ APPLY ============================
        _write_rollback(cur, args.prune_edges)

        if _table_exists(cur, "RETIRED", DUP_TBL):
            print(f"  ABORT: {DUP_RETIRED_FQN} already exists (partial prior run?). "
                  "Resolve manually before re-applying.")
            return 2

        print("\n  applying ...")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {RETIRED} "
                    "COMMENT='Quarantine for retired/duplicate landing tables (not scanned by CATALOG).'")
        cur.execute(f"ALTER TABLE {DUP_LANDING_FQN} RENAME TO {DUP_RETIRED_FQN}")
        print(f"    table moved -> {DUP_RETIRED_FQN}")

        cur.execute(
            f"UPDATE {INGEST_RUNS} SET STATUS='empty', "
            "MESSAGE = LEFT(COALESCE(MESSAGE,'') || ' || ' || %s, 4000) "
            "WHERE SOURCE_ID=%s AND STATUS='success'",
            (RETIRE_MSG, DUP_SID))
        print(f"    INGEST_RUNS demoted success->empty ({cur.rowcount} row)")

        cur.execute(
            f"UPDATE {REGISTRY} SET INCLUDE='N', NOTES=LEFT(COALESCE(NOTES,'') || %s, 16000) "
            "WHERE SOURCE_ID=%s", (NOTE_STAMP, DUP_SID))
        print(f"    SOURCE_REGISTRY INCLUDE Y->N + NOTES stamped ({cur.rowcount} row)")

        if args.prune_edges:
            cur.execute(f"CREATE OR REPLACE TABLE {EDGE_BACKUP} AS "
                        f"SELECT * FROM {EDGES} WHERE A=%s OR B=%s", (DUP_TBL, DUP_TBL))
            n_back = _scalar(cur, f"SELECT COUNT(*) FROM {EDGE_BACKUP}")
            cur.execute(f"DELETE FROM {EDGES} WHERE A=%s OR B=%s", (DUP_TBL, DUP_TBL))
            print(f"    CONNECT edges: {n_back} backed up -> {EDGE_BACKUP}, {cur.rowcount} deleted")

        conn.commit()

        # --- verify ---
        print("\n  verify:")
        print(f"    LANDING table exists: {_table_exists(cur, 'LANDING', DUP_TBL)} (want False)")
        print(f"    RETIRED table exists: {_table_exists(cur, 'RETIRED', DUP_TBL)} (want True)")
        cur.execute(f"SELECT lifecycle, trust_layer FROM {CATALOG} WHERE source_id=%s", (DUP_SID,))
        print(f"    CATALOG {DUP_SID}: {cur.fetchone()} (want ('empty','none'))")
        cur.execute(f"SELECT lifecycle, trust_layer FROM {CATALOG} WHERE source_id=%s", (KEEP_SID,))
        print(f"    CATALOG {KEEP_SID} (keeper, untouched): {cur.fetchone()}")
        if args.prune_edges:
            print(f"    EO edges remaining: "
                  f"{_scalar(cur, f'SELECT COUNT(*) FROM {EDGES} WHERE A=%s OR B=%s', (DUP_TBL, DUP_TBL))} (want 0)")
        print("\n  DONE.")
        return 0
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
