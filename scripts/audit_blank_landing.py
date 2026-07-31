"""Find landing tables that loaded "successfully" but captured NO DATA.

THE FAILURE THIS CATCHES
------------------------
FED_FJC_IDB had 4,126,450 rows. Every column, on every row, was the empty string.
The loader logged success (the row count matched the source), the registry recorded
4.1M rows, and dbt_project.yml carried a comment saying the source had been
"re-ingested (4.1M rows)" -- all true, and all meaningless. Nobody had looked at a
value. The staging model's dedup then correctly collapsed all 4.1M rows to ONE
(every surrogate key was identical, because every input was ''), which is what
finally made it visible: a 1-row mart under a 4.1M-row source.

WHY THE USUAL CHECK MISSES IT
-----------------------------
`COUNT(col)` counts empty strings. A fully-blank column reads as 100% populated.
This is the same class of false-confidence reading CLAUDE.md already documents for
NPPES EIN and NOAA_AIS imo_number, and the reason the house rule is: never trust
COUNT(col) alone -- always pair it with COUNT(DISTINCT col) and a value sample.

WHAT THIS DOES
--------------
For each landing table, on a bounded SAMPLE (not a full scan), computes
COUNT(DISTINCT col) over the non-metadata columns and flags the table when every
column collapses to <= 1 distinct value. That signature -- "many rows, no
variation" -- is corruption, not a small table.

    python scripts/audit_blank_landing.py                 # audit everything
    python scripts/audit_blank_landing.py --min-rows 1000 # only tables worth caring about
    python scripts/audit_blank_landing.py --limit 50      # first N tables (smoke test)
    python scripts/audit_blank_landing.py --json out.json

Read-only. Runs one lightweight query per table and never writes to the warehouse.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from connect import db  # noqa: E402

LANDING_DB = "LIBRARY_RAW"
LANDING_SCHEMA = "LANDING"

# Loader bookkeeping columns -- constant BY DESIGN within one run, so including them
# would mask a genuinely blank table (and flag a healthy single-run one).
META_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_LOADED_AT", "_FILE_NAME", "_BATCH_ID"}

# TWO STAGES, and the second one is not optional.
#
# SCREEN_COLS: a cheap first pass over the leading columns. Fast enough to sweep 1,455
# tables, but it CANNOT convict on its own -- FED_DHS_OHSS is a 475-column ragged union
# whose first 12 columns are blank while 460 of the rest carry real data. Screening
# alone called it dead. It is not.
#
# So anything the screen flags goes to _confirm(), which re-probes EVERY column. Only a
# table with no variation in ANY column is reported. The screen finds suspects; the
# confirm pass is what's allowed to convict.
SCREEN_COLS = 12
SAMPLE_ROWS = 10_000


# A loader that fetched an error page / JS shell instead of a data file writes the
# PAGE into the table, and the parser turns the markup into column names. Found live
# on FED_FFIEC_CALL_REPORTS: its first column is DOCTYPE_HTML, holding
# '<html lang="en">', while RSSD_ID / INSTITUTION_NAME / TOTAL_ASSETS are all blank.
#
# ONLY DOCTYPE. The first version of this set also had HTML, HEAD, BODY, STYLE, META,
# DIV, SPAN, TYPE -- and immediately produced THREE false positives out of four hits:
# 'DIV' is a real column in a Tucson property-assessment extract (division), 'STYLE'
# is a real column in an Allegheny County GIS streets layer. Those are ordinary words.
# A column named DOCTYPE_HTML is not -- no real dataset has one.
#
# Even so, a markup column only NOMINATES. The verdict needs the corroborating
# evidence: the table's actual data columns must also be blank. A page that landed in
# a table always brings both signatures; a dataset that merely uses one of these words
# as a column name brings neither.
_MARKUP_COLS = {"DOCTYPE_HTML", "DOCTYPE"}


def markup_columns(cols: list[str]) -> list[str]:
    return [c for c in cols if c.upper().replace(" ", "_") in _MARKUP_COLS]


def landing_tables(conn, min_rows: int) -> list[tuple[str, int]]:
    rows = db.dicts(conn, f"""
        SELECT TABLE_NAME, COALESCE(ROW_COUNT, 0) AS ROW_COUNT
        FROM {LANDING_DB}.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{LANDING_SCHEMA}' AND TABLE_TYPE = 'BASE TABLE'
          AND COALESCE(ROW_COUNT, 0) >= {int(min_rows)}
        ORDER BY ROW_COUNT DESC""")
    return [(r["TABLE_NAME"], int(r["ROW_COUNT"])) for r in rows]


def table_columns(conn, table: str) -> list[str]:
    rows = db.dicts(conn, f"""
        SELECT COLUMN_NAME FROM {LANDING_DB}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{LANDING_SCHEMA}' AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION""", (table,))
    return [r["COLUMN_NAME"] for r in rows if r["COLUMN_NAME"].upper() not in META_COLS]


def probe(conn, table: str, cols: list[str], *, sample: bool = True) -> dict:
    """-> {col: n_distinct}. COUNT(DISTINCT) treats '' as a value, which is the
    point: a blank column shows n_distinct == 1, not 0 (an all-NULL column shows 0).

    sample=True bounds the scan to SAMPLE_ROWS for the cheap screen. sample=False
    scans the whole table -- used only by _confirm on the handful of screen hits, so
    the full-width cost is paid a few times, not 1,455 times.
    """
    sel = ", ".join(f'COUNT(DISTINCT "{c}") AS "D{i}"' for i, c in enumerate(cols))
    src = (f"(SELECT * FROM {LANDING_DB}.{LANDING_SCHEMA}.\"{table}\" LIMIT {SAMPLE_ROWS})"
           if sample else f'{LANDING_DB}.{LANDING_SCHEMA}."{table}"')
    row = db.dicts(conn, f"SELECT {sel} FROM {src}")[0]
    return {c: int(row[f"D{i}"] or 0) for i, c in enumerate(cols)}


def _confirm(conn, table: str, cols: list[str]) -> tuple[bool, dict]:
    """Re-probe EVERY column, full table. -> (is_really_dead, distincts).

    This exists because the screen was wrong. Twice: once on FED_FDA_FAERS_REAC
    (all-NULL legacy columns read as damage) and once on FED_DHS_OHSS (blank leading
    columns on a 475-column ragged union). Both were healthy tables. A tool that
    cries wolf about data corruption is worse than no tool -- it trains you to ignore it.
    """
    dist = probe(conn, table, cols, sample=False)
    varying = [c for c, v in dist.items() if v > 1]
    constant = [c for c, v in dist.items() if v == 1]
    return (not varying and bool(constant)), dist


def sample_values(conn, table: str, cols: list[str]) -> dict:
    probe_cols = cols[:5]
    sel = ", ".join(f'"{c}"' for c in probe_cols)
    rows = db.dicts(conn, f'SELECT {sel} FROM {LANDING_DB}.{LANDING_SCHEMA}."{table}" LIMIT 1')
    return rows[0] if rows else {}


def audit(conn, *, min_rows: int, limit: int | None) -> dict:
    tables = landing_tables(conn, min_rows)
    if limit:
        tables = tables[:limit]
    dead, suspect, ok, errors = [], [], 0, []
    scraped: list[dict] = []

    for i, (table, n_rows) in enumerate(tables, 1):
        try:
            cols = table_columns(conn, table)
            if not cols:
                continue
            markup = markup_columns(cols)
            if markup:
                # NOMINATION, not verdict -- corroborate against the real columns.
                # A saved page leaves the genuine data columns empty; a dataset that
                # merely uses one of these words as a column name does not.
                real_cols = [c for c in cols if c not in markup]
                blank, full = _confirm(conn, table, real_cols) if real_cols else (True, {})
                if blank:
                    scraped.append({"table": table, "rows": n_rows,
                                    "markup_columns": markup, "distincts": full})
                else:
                    live = sum(1 for v in full.values() if v > 1)
                    print(f"    (markup column on {table}; but {live}/{len(real_cols)} "
                          f"real columns carry data -- CLEARED, not a scraped page)",
                          flush=True)
                    ok += 1
                continue
            dist = probe(conn, table, cols[:SCREEN_COLS])
            if not dist:
                continue
            # An ALL-NULL column has 0 distinct and is NORMAL -- legacy/optional fields
            # are empty all the time (FAERS carries a dead 'ISR' column, and treating
            # that as damage produced a false positive on a 20.6M-row table that turned
            # out to be perfectly healthy). The blank-load signature is specifically
            # EXACTLY ONE distinct value -- the empty string, repeated forever. So judge
            # only on constant-valued columns, and ignore the all-NULL ones entirely.
            constant = [c for c, v in dist.items() if v == 1]
            varying = [c for c, v in dist.items() if v > 1]
            if not varying and constant:
                # SCREEN HIT ONLY -- not a verdict. Re-probe every column, full table,
                # before reporting. This is what separates FED_NIH_REPORTER (really
                # dead: 0 of 46 columns vary) from FED_DHS_OHSS (healthy: 460 of 474
                # vary, it just has blank leading columns).
                really_dead, full = _confirm(conn, table, cols)
                if really_dead:
                    dead.append({"table": table, "rows": n_rows, "n_cols": len(cols),
                                 "distincts": full,
                                 "sample_row": sample_values(conn, table, cols)})
                else:
                    live = sum(1 for v in full.values() if v > 1)
                    print(f"    (screen flagged {table}; full-width check CLEARED it "
                          f"-- {live}/{len(cols)} columns carry data)", flush=True)
                    ok += 1
            elif len(varying) == 1 and len(constant) >= 3:
                # One surviving column against several frozen ones: possible
                # partial-parse damage (the whole line landing in column 1).
                # Confirm this the same way as everything else -- the first version
                # reported this bucket straight off the screen, and 2 of its 3
                # entries (FED_USGS_MINERALS, FED_DHS_HIFLD) turned out healthy once
                # every column was checked. A "suspect" list that's mostly wrong is
                # noise a human learns to skip.
                _dead, full = _confirm(conn, table, cols)
                still_odd = [c for c, v in full.items() if v > 1]
                if len(still_odd) <= 1:
                    suspect.append({"table": table, "rows": n_rows, "distincts": full})
                else:
                    print(f"    (screen flagged {table} as suspect; full-width check "
                          f"CLEARED it -- {len(still_odd)}/{len(cols)} columns carry data)",
                          flush=True)
                    ok += 1
            else:
                ok += 1
        except Exception as exc:  # noqa: BLE001 - one bad table must not kill the sweep
            errors.append({"table": table, "error": str(exc)[:160]})
        if i % 50 == 0:
            print(f"  ... {i}/{len(tables)} scanned "
                  f"({len(dead)} dead, {len(suspect)} suspect)", flush=True)

    return {"scanned": len(tables), "healthy": ok, "dead": dead, "scraped": scraped,
            "suspect": suspect, "errors": errors}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="find landing tables that loaded nothing")
    ap.add_argument("--min-rows", type=int, default=1,
                    help="skip tables smaller than this (a 3-row table is legitimately low-variance)")
    ap.add_argument("--limit", type=int, default=None, help="only the first N tables")
    ap.add_argument("--json", dest="json_out", default=None, help="write the full report here")
    a = ap.parse_args(argv)

    conn = db.connect()
    print(f"auditing {LANDING_DB}.{LANDING_SCHEMA} (min_rows={a.min_rows}) ...", flush=True)
    rep = audit(conn, min_rows=a.min_rows, limit=a.limit)

    print(f"\nscanned {rep['scanned']} tables: {rep['healthy']} healthy, "
          f"{len(rep['dead'])} DEAD, {len(rep['scraped'])} scraped-page, "
          f"{len(rep['suspect'])} suspect, {len(rep['errors'])} errored")

    if rep["dead"]:
        print("\nDEAD -- rows landed, no data in them (every probed column constant):")
        for d in sorted(rep["dead"], key=lambda x: -x["rows"]):
            print(f"  {d['rows']:>14,}  {d['table']}  ({d['n_cols']} cols)")
    if rep["scraped"]:
        print("\nSCRAPED PAGE -- the table's columns are HTML, so a web page landed"
              " instead of a data file:")
        for s in sorted(rep["scraped"], key=lambda x: -x["rows"]):
            print(f"  {s['rows']:>14,}  {s['table']}  (markup cols: {', '.join(s['markup_columns'][:4])})")
    if rep["suspect"]:
        print("\nSUSPECT -- all but one column constant:")
        for s in sorted(rep["suspect"], key=lambda x: -x["rows"])[:25]:
            print(f"  {s['rows']:>14,}  {s['table']}")
    if rep["errors"]:
        print(f"\n{len(rep['errors'])} table(s) could not be probed; first few:")
        for e in rep["errors"][:5]:
            print(f"  {e['table']}: {e['error']}")

    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rep, indent=2, default=str), encoding="utf-8")
        print(f"\nfull report -> {a.json_out}")

    # Exit non-zero when dead tables exist so this can gate a pipeline later.
    return 1 if (rep["dead"] or rep["scraped"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
