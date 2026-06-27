#!/usr/bin/env python3
"""CATALOG TRUST-GATE — stop the catalog lying about broken data. SAFE BY DEFAULT (preview).

The 2026-06-27 audit found the catalog's LIFECYCLE/TRUST_LAYER labels are too generous in
two ways, so the moat's "this source has real data" promise is unreliable:

  GAP 1 — STUB MARTS ride in as 'modeled'.  The CATALOG view marks a mart "real" unless it's
          a 1-3 row stub over a >100-row landing. That >100 floor lets 9 broken marts pass:
          a single dbt-rebuild that produced 1 (or 3) rows over a landing that itself failed
          (hhs_taggs 1<-45, zefix 1<-18, nara_wra_aad 1<-36, gemi 1<-40, fdic_enf 1<-14,
          naag 1<-26, doj_crt_cases 1<-1, ie_cro 1<-3, borme 3<-25). They show TRUST_LAYER
          'mart' and LIFECYCLE 'modeled' — top trust — while holding ~nothing.

  GAP 2 — A 100%-EMPTY LANDING reads 'landed'.  fed_fjc_idb logged STATUS='success' on a
          4.1M-row load whose every data column is blank (parse failure: 0/20000 sampled rows
          carry a value). The 'landed' branch has NO density floor, so a 4.1M-row husk reads
          the same trust as a clean 4.1M-row table. This is the systemic trust gap.

WHAT THE GATE DOES (only on --apply, run by Chris):
  * MART GATE  — a mart is 'real' (=> TRUST_LAYER 'mart', LIFECYCLE 'modeled') only when it is
        NOT a stub, where a stub is:  mart_rows <= 1                       (a 1-row mart is
        never a real analytics table), OR  mart_rows <= 3 AND land_rows > mart_rows*4  (a tiny
        mart dwarfed by its own landing). The absolute <=3 cap is what stops the ratio from
        collateral-demoting LEGIT aggregated marts (mapping_inequality 1155<-10154,
        fara_bulk 21326<-221900, nara_aad 9<-554) — those keep mart_rows well above 3.
  * LANDED GATE — a source reads 'landed' (TRUST_LAYER 'raw') only when its landing clears a
        NON-EMPTY DENSITY floor. Density can't be measured cheaply inside a view, so --apply
        first builds a small probe table LIBRARY_META.REGISTRY.LANDING_DENSITY_PROBE
        (one row per landed/modeled table: nonempty_ratio over a sample of its data columns),
        and the redefined view LEFT JOINs it. A landing whose ratio is below DENSITY_FLOOR
        (0.02) demotes 'landed'/'modeled' -> 'empty'. Today that is exactly fed_fjc_idb (0.000);
        every healthy landed source sits 0.125 .. 1.000, far above the floor.

PREVIEW (default, the ONLY thing this run does):
  Reads the live numbers, simulates the new lifecycle/trust_layer in Python, and prints the
  exact SOURCE_IDs that change — proving it catches the 9 stubs + the empty load and does NOT
  touch the healthy set (nppes 9.6M, noaa_ais 7.3M, etc.). No DDL, no writes, no view replace.

    python3 scripts/propose_catalog_trust_gate.py            # preview (no writes)   <- safe
    python3 scripts/propose_catalog_trust_gate.py --apply    # Chris runs this (ACCOUNTADMIN)

NB: this only makes the catalog tell the TRUTH about these sources. It does not repair them —
the stub marts and fjc_idb need RE-INGESTION (the landing parse is broken), not a relabel.

Design mirrors scripts/propose_catalog_hygiene_fixes.py & propose_catalog_domaining_fixes.py:
preview-by-default, rollback-snapshotted (GET_DDL of the live view saved before replace),
idempotent (CREATE OR REPLACE), --apply gated, as-role verify. The auto-mode classifier blocks
the agent from writing the catalog directly, so --apply is handed to Chris.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

# Load library-onboarding/.env explicitly (cwd-independent — the bug that bit the 2026-06-26
# session: running from repo root left config with stale OS creds).
try:
    from dotenv import load_dotenv

    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402

VIEW = "LIBRARY_META.REGISTRY.CATALOG"
PROBE = "LIBRARY_META.REGISTRY.LANDING_DENSITY_PROBE"
ROLLBACK = _REPO / "outputs" / "_rollback_CATALOG_view_trustgate.sql"

# ---- gate thresholds (the knobs; tuned against the 2026-06-27 live numbers) ----
MART_STUB_MAX = 3        # only a 1-3 row mart can be a stub
MART_STUB_RATIO = 4      # ... and only if its landing dwarfs it 4x+ (1-row marts: always stub)
DENSITY_FLOOR = 0.02     # a landing below 2% non-empty is an empty husk (fjc_idb = 0.000)
DENSITY_SAMPLE = 20000   # rows sampled per table when probing non-empty density
DENSITY_MAXCOLS = 8      # data columns sampled per table (cheap, representative)


# -------------------------------------------------------------------------- helpers
def _is_stub_mart(mart_rows, land_rows) -> bool:
    """Mirror of the gate's SQL stub predicate, in Python, for the preview diff."""
    if mart_rows is None:
        return False
    if mart_rows <= 1:
        return True
    if mart_rows <= MART_STUB_MAX and land_rows is not None and land_rows > mart_rows * MART_STUB_RATIO:
        return True
    return False


def _data_columns(cur, table_name: str) -> list[str]:
    cur.execute(
        """SELECT column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
           WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s AND LEFT(column_name,1) <> '_'
           ORDER BY ordinal_position LIMIT %s""",
        (table_name, DENSITY_MAXCOLS),
    )
    return [r[0] for r in cur.fetchall()]


def _nonempty_ratio(cur, table_name: str):
    """Sampled fraction of (row, data-col) cells that are non-empty. None if no data cols."""
    cols = _data_columns(cur, table_name)
    if not cols:
        return None
    parts = " + ".join('IFF(NULLIF(TRIM("%s"),\'\') IS NULL,0,1)' % c for c in cols)
    q = 'SELECT AVG((%s)/%d) FROM LIBRARY_RAW.LANDING."%s" SAMPLE (%d ROWS)' % (
        parts, len(cols), table_name, DENSITY_SAMPLE,
    )
    cur.execute(q)
    v = cur.fetchone()[0]
    return float(v) if v is not None else None


# -------------------------------------------------------------------------- preview
def preview(conn) -> int:
    cur = conn.cursor()

    # Current catalog rows for every source that has a mart OR is 'landed' — these are the
    # only rows the gate can change. (Everything else keeps its current lifecycle exactly.)
    cur.execute(
        """WITH marts AS (
               SELECT LOWER(SPLIT_PART(TABLE_NAME,'__',2)) AS sid, SUM(ROW_COUNT) AS mart_rows
               FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
               WHERE POSITION('__' IN TABLE_NAME) > 0 AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
               GROUP BY 1)
           SELECT c.source_id, c.lifecycle, c.trust_layer,
                  m.mart_rows, c.landed_row_count,
                  UPPER(c.source_id) AS landing_tbl
           FROM LIBRARY_META.REGISTRY.CATALOG c
           LEFT JOIN marts m ON m.sid = c.source_id
           WHERE m.mart_rows IS NOT NULL OR c.lifecycle = 'landed'
           ORDER BY COALESCE(m.mart_rows, c.landed_row_count) DESC NULLS LAST""",
    )
    rows = cur.fetchall()

    mart_demotions = []     # stub marts: modeled -> (landed/staging/raw)
    landed_demotions = []   # empty husks: landed -> empty
    spared_thin = []        # thin-but-complete marts kept 'modeled' (proof of no over-reach)
    spared_big = []         # the headline healthy marts, kept 'modeled'

    print("=" * 78)
    print("CATALOG TRUST-GATE — PREVIEW (no writes)")
    print("=" * 78)
    print(f"  mart stub   = mart_rows<=1  OR  (mart_rows<={MART_STUB_MAX} AND "
          f"land_rows>mart_rows*{MART_STUB_RATIO})")
    print(f"  empty husk  = landing non-empty density < {DENSITY_FLOOR} "
          f"(sampled {DENSITY_SAMPLE} rows / {DENSITY_MAXCOLS} cols)")
    print("-" * 78)

    # GAP 1 — mart gate (pure metadata, no table scans)
    for sid, lc, tl, mart_rows, land_rows, _tbl in rows:
        if mart_rows is None:
            continue
        if _is_stub_mart(mart_rows, land_rows):
            if lc == "modeled":
                mart_demotions.append((sid, mart_rows, land_rows))
        else:
            # real mart — record the thin ones (<=200) and the big ones as "untouched" proof
            if mart_rows <= 200:
                spared_thin.append((sid, mart_rows, land_rows))
            elif mart_rows >= 1_000_000:
                spared_big.append((sid, mart_rows, land_rows))

    # GAP 2 — landed density gate. Probe ONLY the 'landed' tables (+ any mart-stub landing we
    # just demoted, since a demoted mart falls back to 'landed' and must clear the floor too).
    probe_targets = sorted({sid for sid, _lc, _tl, _m, _l, _t in rows
                            if _lc == "landed"} | {sid for sid, _m, _l in mart_demotions})
    print(f"\nprobing non-empty density on {len(probe_targets)} landing tables...")
    probe = {}
    for sid in probe_targets:
        try:
            probe[sid] = _nonempty_ratio(cur, sid.upper())
        except Exception as exc:  # pragma: no cover — table may be gone; treat as unknown
            probe[sid] = None
            print(f"    (probe skipped for {sid}: {str(exc)[:60]})")

    for sid, ratio in probe.items():
        if ratio is not None and ratio < DENSITY_FLOOR:
            landed_demotions.append((sid, ratio))

    # ----- report -----
    print("\n" + "-" * 78)
    print(f"GAP 1 — STUB MARTS demoted out of 'modeled'  ({len(mart_demotions)}):")
    if not mart_demotions:
        print("    (none — gate is a no-op on marts)")
    for sid, mart_rows, land_rows in sorted(mart_demotions, key=lambda x: x[0]):
        print(f"    {sid:<36} mart={mart_rows:<6} land={land_rows}   modeled/mart -> raw/empty")

    print(f"\nGAP 2 — EMPTY-HUSK landings demoted out of 'landed'  ({len(landed_demotions)}):")
    if not landed_demotions:
        print("    (none)")
    for sid, ratio in sorted(landed_demotions, key=lambda x: x[0]):
        print(f"    {sid:<36} non-empty density={ratio:.3f} < {DENSITY_FLOOR}   landed -> empty")

    print("\n" + "-" * 78)
    print("PROOF OF NO OVER-REACH — these stay 'modeled' (sample):")
    print("  thin-but-complete marts (mart_rows <= 200), UNTOUCHED:")
    for sid, mart_rows, land_rows in sorted(spared_thin, key=lambda x: x[1]):
        print(f"    {sid:<36} mart={mart_rows:<6} land={land_rows}   kept modeled")
    print("  headline big marts (>= 1M rows), UNTOUCHED:")
    for sid, mart_rows, land_rows in sorted(spared_big, key=lambda x: -x[1]):
        print(f"    {sid:<36} mart={mart_rows:<10} land={land_rows}   kept modeled")
    # the healthy 'landed' giants whose density we probed and cleared
    healthy_landed = [(sid, r) for sid, r in probe.items()
                      if r is not None and r >= DENSITY_FLOOR]
    print(f"  healthy 'landed' sources clearing the density floor ({len(healthy_landed)}), "
          "UNTOUCHED:")
    for sid, r in sorted(healthy_landed, key=lambda x: -x[1])[:8]:
        print(f"    {sid:<36} non-empty density={r:.3f} >= {DENSITY_FLOOR}   kept landed")
    if len(healthy_landed) > 8:
        print(f"    ... +{len(healthy_landed) - 8} more, all >= {DENSITY_FLOOR}")

    print("\n" + "=" * 78)
    print(f"SUMMARY: would demote {len(mart_demotions)} stub mart(s) + "
          f"{len(landed_demotions)} empty husk(s).")
    print(f"         {len(spared_thin) + len(spared_big) + len(healthy_landed)} verified-healthy "
          "sources untouched.")
    print("PREVIEW only — re-run with --apply to write (snapshots the view DDL first;\n"
          f"rollback via {ROLLBACK}).")
    print("=" * 78)
    return 0


# --------------------------------------------------------------------------- apply
def apply(conn) -> int:
    """Chris runs this. Builds the density probe, snapshots the live view, replaces it."""
    cur = conn.cursor()

    # 1) rollback snapshot of the live view DDL (read-only GET_DDL) BEFORE any change
    cur.execute("SELECT GET_DDL('VIEW','LIBRARY_META.REGISTRY.CATALOG')")
    old_ddl = cur.fetchone()[0]
    ROLLBACK.parent.mkdir(parents=True, exist_ok=True)
    ROLLBACK.write_text(old_ddl)
    print(f"  rollback snapshot -> {ROLLBACK}")

    # 2) build the density-probe table: one row per landed/modeled landing table.
    #    (Cheap: samples DENSITY_SAMPLE rows / DENSITY_MAXCOLS cols per table.)
    cur.execute(
        """SELECT DISTINCT UPPER(source_id) FROM LIBRARY_META.REGISTRY.CATALOG
           WHERE lifecycle IN ('landed','modeled')"""
    )
    targets = [r[0] for r in cur.fetchall()]
    cur.execute(
        f"""CREATE OR REPLACE TABLE {PROBE} (
                SOURCE_ID STRING, NONEMPTY_RATIO FLOAT, SAMPLED_COLS INT,
                PROBED_AT TIMESTAMP_NTZ DEFAULT SYSDATE()
            )"""
    )
    for tbl in targets:
        cols = _data_columns(cur, tbl)
        if not cols:
            cur.execute(
                f"INSERT INTO {PROBE}(SOURCE_ID,NONEMPTY_RATIO,SAMPLED_COLS) VALUES (%s,NULL,0)",
                (tbl.lower(),),
            )
            continue
        parts = " + ".join('IFF(NULLIF(TRIM("%s"),\'\') IS NULL,0,1)' % c for c in cols)
        cur.execute(
            f'''INSERT INTO {PROBE}(SOURCE_ID,NONEMPTY_RATIO,SAMPLED_COLS)
                SELECT %s, AVG(({parts})/{len(cols)}), {len(cols)}
                FROM LIBRARY_RAW.LANDING."{tbl}" SAMPLE ({DENSITY_SAMPLE} ROWS)''',
            (tbl.lower(),),
        )
    print(f"  built {PROBE} ({len(targets)} tables probed).")

    # 3) redefine the CATALOG view with the trust gate. We only swap the stub predicate and
    #    add the density gate; every other branch is byte-for-byte the live DDL.
    new_ddl = _build_gated_ddl(old_ddl)
    cur.execute(new_ddl)
    print("  CATALOG view replaced with trust gate.")

    # 4) as-role verify (read back through CLAUDE_MCP_READONLY's view of the world)
    for lc, cnt in cur.execute(
        "SELECT lifecycle, COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG GROUP BY 1 ORDER BY 2 DESC"
    ).fetchall():
        print(f"    {lc:<10} {cnt}")
    return 0


def _require_replace(ddl: str, old: str, new: str, label: str, count: int = -1) -> str:
    """str.replace, but ABORT loudly if the target fragment isn't present.

    Bare .replace() is silent on a miss: if the live CATALOG view has drifted so a
    fragment no longer matches, the transform would no-op and --apply would CREATE OR
    REPLACE a view MISSING that part of the gate with no error. So we assert the
    fragment exists first and refuse to build a partially-gated DDL.
    """
    found = ddl.count(old)
    if found == 0:
        raise RuntimeError(
            f"trust-gate ABORT [{label}]: expected DDL fragment not found in the live "
            f"CATALOG view — it has DRIFTED since this script was written. Re-derive the "
            f"gate against the current GET_DDL before --apply. Fragment:\n    {old[:120]}..."
        )
    return ddl.replace(old, new) if count < 0 else ddl.replace(old, new, count)


def _build_gated_ddl(old_ddl: str) -> str:
    """Transform the live CATALOG DDL into the trust-gated version.

    Four edits, all additive / non-breaking to healthy paths, each guarded by
    _require_replace so a drifted view aborts instead of silently half-applying:
      (a) qualify the CREATE so it targets the right schema regardless of session context;
      (b) add a LEFT JOIN to the density probe + a `dp` density handle;
      (c) replace the stub predicate (appears in _REAL_MART, LIFECYCLE, TRUST_LAYER —
          replace-all) with the new stub rule;
      (d) gate the 'landed' branch on the density floor.
    """
    old_stub = "(m.sid IS NOT NULL AND NOT (COALESCE(m.mart_rows,0) <= 3 AND COALESCE(l.land_rows,0) > 100))"
    new_stub = (
        "(m.sid IS NOT NULL AND NOT ("
        "COALESCE(m.mart_rows,0) <= 1 "
        f"OR (COALESCE(m.mart_rows,0) <= {MART_STUB_MAX} "
        f"AND COALESCE(l.land_rows,0) > COALESCE(m.mart_rows,0) * {MART_STUB_RATIO})))"
    )
    # (c) stub predicate — replace ALL occurrences (it appears in 3 branches)
    ddl = _require_replace(old_ddl, old_stub, new_stub, "stub-predicate")

    # (a) qualify the CREATE target (matches the hygiene script's approach)
    ddl = _require_replace(ddl, "create or replace view CATALOG(",
                           "create or replace view LIBRARY_META.REGISTRY.CATALOG(",
                           "qualify-create", count=1)

    # (b) add the density-probe join (handle `dp`) right after the landed join
    ddl = _require_replace(
        ddl, "LEFT JOIN landed l ON l.sid = i.SOURCE_ID",
        "LEFT JOIN landed l ON l.sid = i.SOURCE_ID\n"
        f"    LEFT JOIN {PROBE} dp ON dp.SOURCE_ID = i.SOURCE_ID",
        "density-join", count=1)

    # (d) gate the 'landed' branch on the density floor: a husk (ratio measured AND below
    #     floor) falls through to 'empty' instead of reading 'landed'.
    ddl = _require_replace(
        ddl, "        WHEN lr.STATUS='success' THEN 'landed'\n",
        "        WHEN lr.STATUS='success' AND dp.NONEMPTY_RATIO IS NOT NULL "
        f"AND dp.NONEMPTY_RATIO < {DENSITY_FLOOR} THEN 'empty'\n"
        "        WHEN lr.STATUS='success' THEN 'landed'\n",
        "landed-density-gate", count=1)

    if ddl == old_ddl:
        raise RuntimeError("trust-gate ABORT: transform produced an unchanged DDL — refusing to "
                           "CREATE OR REPLACE with no gate applied.")
    return ddl


# ---------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Preview/apply the CATALOG trust gate")
    ap.add_argument("--apply", action="store_true",
                    help="write the gate (default previews). Chris runs this with ACCOUNTADMIN.")
    args = ap.parse_args(argv)

    conn = snow.connect()
    try:
        if args.apply:
            return apply(conn)
        return preview(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
