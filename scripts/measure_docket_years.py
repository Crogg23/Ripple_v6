#!/usr/bin/env python3
"""Measure the year span of every table the docket names, in one connection.

Running coverage_probe once per table costs a fresh Snowflake login each time,
which dominates the run: 147 logins is over half an hour of nothing but
handshakes. This opens one connection and reuses it.

Read only. Rows append to LIBRARY_META.REGISTRY.SOURCE_COVERAGE_YEARS, one per
table per year, and readers take the newest run per table.
"""
from __future__ import annotations

import csv
import datetime as _dt
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))
sys.path.insert(0, str(REPO / "scripts"))
try:
    from dotenv import load_dotenv
    load_dotenv(REPO / "library-onboarding" / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from build_freshness_ledger import recency_inner  # noqa: E402

_s = importlib.util.spec_from_file_location("cp", REPO / "scripts" / "coverage_probe.py")
cp = importlib.util.module_from_spec(_s)
_s.loader.exec_module(cp)

# Load stamps say when a row arrived, not what year it is about.
AUDIT = re.compile(r"INGEST|LOADED|LOAD_TS|ETL_|DBT_|SNAPSHOT_DATE|CREATED_AT"
                   r"|UPDATED_AT|_SRC|SOURCE_RUN", re.I)
DATEY = re.compile(r"(^|_)(DATE|DT|YEAR|YR|FY|CYCLE|PERIOD|FILED|MONTH|QUARTER|TIME"
                   r"|BEGIN|END|START|EFF|EXPIR|ISSUE|REPORT|ACTION|TRANSACT|CERT"
                   r"|DECISION|OPEN|CLOSE)($|_)", re.I)
DATE_TYPES = ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ")


def docket_tables() -> set[str]:
    out = set()
    for r in csv.DictReader((REPO / "docket" / "docket.csv").open()):
        for t in (r.get("tables") or "").split("|"):
            if t.strip():
                out.add(t.strip().upper())
    return out


def pick_columns(conn, tables: set[str]) -> dict[str, str]:
    """One date column per table. Typed dates win, then date-shaped names."""
    cur = conn.cursor()
    cols: dict[str, list[tuple[str, str]]] = {}
    for db in ("LIBRARY_RAW", "LIBRARY_MARTS"):
        cur.execute(f"""SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
                        FROM {db}.INFORMATION_SCHEMA.COLUMNS""")
        for sch, t, col, dt in cur.fetchall():
            cols.setdefault(f"{db}.{sch}.{t}", []).append((col, (dt or "").upper()))
    cur.close()
    picks = {}
    for t in sorted(tables):
        cand = [(c, d) for c, d in cols.get(t, []) if not AUDIT.search(c)]
        typed = [c for c in cand if c[1] in DATE_TYPES]
        named = [c for c in cand if DATEY.search(c[0])]
        got = (typed or named)
        if got:
            picks[t] = got[0][0]
    return picks


def main() -> int:
    tables = docket_tables()
    conn = snow.connect()
    try:
        picks = pick_columns(conn, tables)
        print(f"{len(tables)} docket tables, {len(picks)} with a date column\n")
        snow.execute(conn, cp.CREATE_SQL)
        cur = conn.cursor()
        done = {r[0] for r in cur.execute(
            "SELECT DISTINCT SOURCE_ID FROM " + cp.COVERAGE_TABLE).fetchall()}
        cur.close()

        measured = skipped = failed = 0
        for i, (t, col) in enumerate(sorted(picks.items()), 1):
            if t in done:
                skipped += 1
                continue
            m = {"source_id": t, "landing_fqn": t, "recency_col": col,
                 "recency_kind": "mixed"}
            try:
                rows = cp.measure_one(conn, m, True)
            except Exception as exc:
                print(f"[{i}/{len(picks)}] {t.split('.')[-1][:44]}: "
                      f"{str(exc).splitlines()[-1][:60]}")
                failed += 1
                continue
            if rows:
                cp.save(conn, rows)
                measured += 1
            else:
                failed += 1
        print(f"\nmeasured {measured}, already had {skipped}, no result {failed}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
