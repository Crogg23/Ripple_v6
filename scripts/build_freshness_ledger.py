#!/usr/bin/env python3
"""Build the DATA-FRESHNESS LEDGER — the keystone of the platform foundation (Phase 0).

THE BUG THIS KILLS: the system tracks when a source was LOADED, never whether the DATA is current.
NOAA AIS (58M rows) was loaded recently so every load-stamp reads "fresh" — but every vessel ping is
dated Jan 2024, ~2.5 years stale, and nothing knew. This ledger measures DATA recency per source and
never lets a load-stamp lie again.

HOW IT WORKS
  For each of the ~102 real sources we know (scripts/freshness_mapping.json):
    1. measure DATA_THROUGH = MAX(parsed data-about column) live — NOT a load-stamp
       (_INGESTED_AT/_SOURCE_RUN_ID/_SRC_SHA256/_LOADED_AT/SRC_SHA256 are NEVER eligible)
    2. compare to CADENCE_BUCKET (how often it SHOULD update) vs today
    3. derive FRESHNESS_STATE: fresh | due | overdue | stale | dead | unknown

  The recency column is parsed with a universal best-effort expression that tolerates every shape a
  TEXT landing column throws (ISO date, timestamp, YYYYMMDD, YYYYMM, bare year) — year-grain is
  encoded as YYYY-12-31 so a 2025-latest annual source reads fresh in mid-2026 while 2024-latest reads
  stale. Anything unparseable → DATA_THROUGH NULL → 'unknown' (never false-fresh).

  --apply also creates V_SOURCE_FRESHNESS, which RE-DERIVES the state live against CURRENT_DATE — so a
  source silently drifts fresh -> due -> overdue -> stale as days pass with no rebuild. Re-run this
  builder only to refresh DATA_THROUGH after a source is re-loaded (Phase 3's heartbeat will).

USAGE
    python scripts/build_freshness_ledger.py            # PREVIEW (read-only): the freshness picture
    python scripts/build_freshness_ledger.py --rotting  # preview, stale/overdue only
    python scripts/build_freshness_ledger.py --apply     # Chris runs this: create + populate the ledger
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass
import snow  # noqa: E402

MAPPING = Path(__file__).resolve().parent / "freshness_mapping.json"

# grace windows in DAYS per cadence: (fresh<=, due<=, overdue<=, else stale).
GRACE = {
    "daily":     (3, 5, 7),
    "real_time": (4, 10, 30),   # the Library's "real-time" sources are batch file feeds, not streams
    "weekly":    (11, 17, 21),
    "monthly":   (40, 55, 75),
    "quarterly": (100, 125, 150),
    "annual":    (400, 425, 450),
    "irregular": (270, 455, 730),  # generous — irregular feeds legitimately go quiet for months
}
STATE_ORDER = {"dead": 0, "stale": 1, "overdue": 2, "due": 3, "unknown": 4, "fresh": 5}


def col_ref(col: str) -> str | None:
    """A valid SQL TEXT reference for a recency column, or None if the mapping value
    isn't a usable column. Landing columns are TEXT; a few sources land a VARIANT
    ``RECORD`` blob, so a ``base:path`` mapping is a VARIANT extract cast back to text.
    Prose / derived expressions (spaces, not an identifier) return None -> recency unmeasured."""
    col = (col or "").strip()
    if re.match(r"^[A-Za-z_][A-Za-z0-9_$]*$", col):                       # plain identifier
        return '"' + col + '"'
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_$]*):([A-Za-z0-9_$.\[\]:]+)$", col)
    if m:                                                                 # VARIANT path RECORD:field
        return f'"{m.group(1)}":{m.group(2)}::STRING'
    return None                                                          # prose / derived / unusable


def recency_expr(col: str, kind: str) -> str | None:
    """Parse a TEXT column to a DATE, driven by the per-source RECENCY_KIND the measurement agents found.
    Returns None when ``col`` is not a usable column reference (caller then records recency as unmeasured).

    EPOCH TRAP: TRY_TO_DATE/TRY_TO_TIMESTAMP read a BARE NUMBER as seconds-since-epoch, so a year '2023'
    or a 'YYYYMMDD' like '20240108' silently parses to 1970. Every branch here is therefore guarded:
    date/timestamp parses require a separator (- / :); numeric shapes are matched by exact pattern; bare
    years must look like 19xx/20xx and not exceed next year. A wrong guess yields NULL, never a false date.
    """
    c = col_ref(col)
    if c is None:
        return None
    t = f"TRIM({c})"
    sep = f"({t} LIKE '%-%' OR {t} LIKE '%/%' OR {t} LIKE '%:%')"
    dt = f"IFF({sep},TRY_TO_DATE(NULLIF({t},'')),NULL)"                                   # separated date
    ts = f"IFF({sep},TRY_TO_TIMESTAMP(NULLIF({t},''))::DATE,NULL)"                        # timestamp
    ymd8 = f"IFF(REGEXP_LIKE({t},'^[0-9]{{8}}$'),TRY_TO_DATE({t},'YYYYMMDD'),NULL)"       # yyyymmdd
    ymd6 = f"IFF(REGEXP_LIKE({t},'^[0-9]{{6}}$'),TRY_TO_DATE({t}||'01','YYYYMMDD'),NULL)" # yyyymm -> 1st
    ymd14 = f"IFF(REGEXP_LIKE({t},'^[0-9]{{14}}$'),TRY_TO_DATE(SUBSTR({t},1,8),'YYYYMMDD'),NULL)"  # YYYYMMDDHHMMSS (wayback)
    yr = (f"IFF(REGEXP_LIKE({t},'^(19|20)[0-9]{{2}}') "
          f"AND TO_NUMBER(SUBSTR({t},1,4))<=YEAR(CURRENT_DATE())+1,"
          f"DATE_FROM_PARTS(TO_NUMBER(SUBSTR({t},1,4)),12,31),NULL)")                     # year -> Dec 31
    if kind == "date":
        inner = dt
    elif kind == "timestamp":
        inner = ts
    elif kind == "yyyymmdd_text":
        inner = f"COALESCE({ymd14},{ymd8},{ymd6})"
    elif kind in ("year_text", "year_int"):
        inner = yr
    else:  # 'mixed' / fallback — every branch guarded, so still epoch-safe
        inner = f"COALESCE({dt},{ts},{ymd14},{ymd8},{ymd6},{yr})"
    return f"MAX({inner})"


def freshness_state(cadence: str, data_through: date | None, row_count: int | None) -> tuple[str, int | None]:
    """Mirror of the V_SOURCE_FRESHNESS CASE logic, in Python. Returns (state, data_age_days)."""
    if not row_count:
        return "dead", None
    if cadence == "static":
        return "fresh", None
    if data_through is None:
        return "unknown", None
    if cadence not in GRACE:
        return "unknown", None
    age = (date.today() - data_through).days
    f, d, o = GRACE[cadence]
    if age <= f:
        return "fresh", age
    if age <= d:
        return "due", age
    if age <= o:
        return "overdue", age
    return "stale", age


def measure(conn, mapping: list[dict]) -> list[dict]:
    cur = conn.cursor()
    rows = []
    for m in mapping:
        sid = m["source_id"]
        fqn = m.get("landing_fqn") or f"LIBRARY_RAW.LANDING.{sid.upper()}"
        col = m.get("recency_col")
        note = m.get("note", "")
        data_through = None
        row_count = None
        # one default, used for BOTH the SQL expr and the recorded row so they can never diverge:
        # col present -> 'mixed' (matches recency_expr's own fallback); col absent -> 'none' (no recency measure)
        kind = m.get("recency_kind", "mixed" if col else "none")
        # Row count on its OWN query: a recency-parse failure must never blow away the
        # count and mislabel a live source as 'dead' (freshness_state -> dead when not row_count).
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM {fqn}")
            row_count = int(cur.fetchone()[0])
        except Exception as exc:  # table missing / unreadable
            note = (note + " | " if note else "") + f"COUNT ERROR: {str(exc)[:120]}"
        # Recency: best-effort and DECOUPLED. Only when the table has rows and the mapping
        # points at a usable column; a failure here leaves row_count intact (state -> unknown, not dead).
        sel = recency_expr(col, kind) if col else None
        if col and sel is None:
            note = (note + " | " if note else "") + f"recency_col {col!r} not a usable column; recency unmeasured"
        elif sel is not None and row_count:
            try:
                cur.execute(f"SELECT {sel} AS data_through FROM {fqn}")
                data_through = cur.fetchone()[0]  # snowflake returns a datetime.date or None
                # sanity clamp: a date far in the future (or absurdly old) is a parse artifact, not data
                if data_through is not None and (
                    data_through > date.today() + timedelta(days=550) or data_through.year < 1900
                ):
                    note = (note + " | " if note else "") + f"dropped suspect parse {data_through.isoformat()}"
                    data_through = None
            except Exception as exc:  # column gone / parse blew up — recency only, count survives
                note = (note + " | " if note else "") + f"RECENCY ERROR: {str(exc)[:120]}"
        state, age = freshness_state(m.get("cadence_bucket", "unknown"), data_through, row_count)
        rows.append({
            "source_id": sid,
            "landing_fqn": fqn,
            "recency_col": col,
            "recency_kind": kind,
            "data_through": data_through.isoformat() if data_through else None,
            "row_count": row_count,
            "cadence_bucket": m.get("cadence_bucket", "unknown"),
            "freshness_state": state,
            "age_days": age,
            "note": note,
        })
    cur.close()
    return rows


# --------------------------------------------------------------------------- preview
def preview(rows: list[dict], rotting_only: bool) -> None:
    by_state: dict[str, int] = {}
    for r in rows:
        by_state[r["freshness_state"]] = by_state.get(r["freshness_state"], 0) + 1

    print("=" * 78)
    print(f"  DATA-FRESHNESS LEDGER — preview  ({len(rows)} sources, as of {date.today().isoformat()})")
    print("=" * 78)
    order = ["fresh", "due", "overdue", "stale", "dead", "unknown"]
    print("  " + "   ".join(f"{s}={by_state.get(s,0)}" for s in order))
    rotten = sum(by_state.get(s, 0) for s in ("overdue", "stale"))
    print(f"  --> {by_state.get('fresh',0)} genuinely fresh · {rotten} past grace (overdue+stale) · "
          f"{by_state.get('dead',0)} dead · {by_state.get('unknown',0)} unmeasurable")
    print("-" * 78)

    shown = [r for r in rows if (not rotting_only or r["freshness_state"] in ("overdue", "stale"))]
    shown.sort(key=lambda r: (STATE_ORDER.get(r["freshness_state"], 9),
                              -(r["age_days"] or 0)))
    print(f"  {'SOURCE_ID':<34}{'THROUGH':<12}{'CADENCE':<11}{'STATE':<9}AGE")
    for r in shown:
        age = f"{r['age_days']/365:.1f}y" if r["age_days"] else ""
        through = r["data_through"] or "—"
        print(f"  {r['source_id']:<34}{through:<12}{r['cadence_bucket']:<11}{r['freshness_state']:<9}{age}")
    if not rotting_only:
        print("-" * 78)
        print("  PREVIEW only — nothing written. Re-run with --apply to create the ledger (Chris, ACCOUNTADMIN).")


# --------------------------------------------------------------------------- apply
TABLE_DDL = """
CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.SOURCE_FRESHNESS (
    SOURCE_ID         VARCHAR        NOT NULL,
    LANDING_FQN       VARCHAR,
    RECENCY_COL       VARCHAR,
    RECENCY_KIND      VARCHAR,
    DATA_THROUGH_ISO  DATE,
    ROW_COUNT         NUMBER(38,0),
    CADENCE_BUCKET    VARCHAR,
    FRESHNESS_STATE   VARCHAR,
    LAST_MEASURED_AT  TIMESTAMP_NTZ  DEFAULT CURRENT_TIMESTAMP(),
    NOTE              VARCHAR,
    CONSTRAINT PK_SOURCE_FRESHNESS PRIMARY KEY (SOURCE_ID)
)
COMMENT = 'Data-freshness ledger: how current each source DATA is (not when it was loaded). Built by scripts/build_freshness_ledger.py.'
"""

VIEW_DDL = """
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS AS
WITH last_run AS (
    SELECT SOURCE_ID, RUN_ID AS LAST_RUN_ID, STATUS AS LAST_RUN_STATUS,
           COALESCE(ENDED_AT, STARTED_AT, _LOADED_AT) AS LAST_RUN_AT, ROW_COUNT AS LAST_RUN_ROWS
    FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
    QUALIFY ROW_NUMBER() OVER (PARTITION BY SOURCE_ID
            ORDER BY COALESCE(ENDED_AT, STARTED_AT, _LOADED_AT) DESC NULLS LAST) = 1
),
base AS (
    SELECT f.*, DATEDIFF('day', f.DATA_THROUGH_ISO, CURRENT_DATE()) AS DATA_AGE_DAYS
    FROM LIBRARY_META.REGISTRY.SOURCE_FRESHNESS f
)
SELECT b.SOURCE_ID, b.LANDING_FQN, b.RECENCY_COL, b.RECENCY_KIND, b.DATA_THROUGH_ISO,
       b.ROW_COUNT, b.CADENCE_BUCKET, b.DATA_AGE_DAYS,
       CASE
         WHEN COALESCE(b.ROW_COUNT,0)=0 THEN 'dead'
         WHEN b.CADENCE_BUCKET='static' THEN 'fresh'
         WHEN b.DATA_THROUGH_ISO IS NULL THEN COALESCE(b.FRESHNESS_STATE,'unknown')
         WHEN b.CADENCE_BUCKET='unknown' THEN 'unknown'
         WHEN b.CADENCE_BUCKET='daily'     THEN CASE WHEN b.DATA_AGE_DAYS<=3   THEN 'fresh' WHEN b.DATA_AGE_DAYS<=5   THEN 'due' WHEN b.DATA_AGE_DAYS<=7   THEN 'overdue' ELSE 'stale' END
         WHEN b.CADENCE_BUCKET='real_time' THEN CASE WHEN b.DATA_AGE_DAYS<=4   THEN 'fresh' WHEN b.DATA_AGE_DAYS<=10  THEN 'due' WHEN b.DATA_AGE_DAYS<=30  THEN 'overdue' ELSE 'stale' END
         WHEN b.CADENCE_BUCKET='weekly'    THEN CASE WHEN b.DATA_AGE_DAYS<=11  THEN 'fresh' WHEN b.DATA_AGE_DAYS<=17  THEN 'due' WHEN b.DATA_AGE_DAYS<=21  THEN 'overdue' ELSE 'stale' END
         WHEN b.CADENCE_BUCKET='monthly'   THEN CASE WHEN b.DATA_AGE_DAYS<=40  THEN 'fresh' WHEN b.DATA_AGE_DAYS<=55  THEN 'due' WHEN b.DATA_AGE_DAYS<=75  THEN 'overdue' ELSE 'stale' END
         WHEN b.CADENCE_BUCKET='quarterly' THEN CASE WHEN b.DATA_AGE_DAYS<=100 THEN 'fresh' WHEN b.DATA_AGE_DAYS<=125 THEN 'due' WHEN b.DATA_AGE_DAYS<=150 THEN 'overdue' ELSE 'stale' END
         WHEN b.CADENCE_BUCKET='annual'    THEN CASE WHEN b.DATA_AGE_DAYS<=400 THEN 'fresh' WHEN b.DATA_AGE_DAYS<=425 THEN 'due' WHEN b.DATA_AGE_DAYS<=450 THEN 'overdue' ELSE 'stale' END
         WHEN b.CADENCE_BUCKET='irregular' THEN CASE WHEN b.DATA_AGE_DAYS<=270 THEN 'fresh' WHEN b.DATA_AGE_DAYS<=455 THEN 'due' WHEN b.DATA_AGE_DAYS<=730 THEN 'overdue' ELSE 'stale' END
         ELSE 'unknown'
       END AS FRESHNESS_STATE,
       b.FRESHNESS_STATE AS FRESHNESS_STATE_AT_MEASURE, b.LAST_MEASURED_AT,
       lr.LAST_RUN_ID, lr.LAST_RUN_AT, lr.LAST_RUN_STATUS, lr.LAST_RUN_ROWS,
       DATEDIFF('day', b.DATA_THROUGH_ISO, lr.LAST_RUN_AT) AS LOAD_MINUS_DATA_DAYS,
       b.NOTE
FROM base b LEFT JOIN last_run lr ON lr.SOURCE_ID = b.SOURCE_ID
"""


def apply(conn, rows: list[dict]) -> int:
    cur = conn.cursor()
    cur.execute(TABLE_DDL)
    cur.execute(VIEW_DDL)
    cur.execute("DELETE FROM LIBRARY_META.REGISTRY.SOURCE_FRESHNESS")
    # Direct bind into the DATE column: data_through is an ISO string or None, and the
    # connector's server-side binding turns TRY_TO_DATE(%s) into TRY_CAST(NULL AS DATE)
    # for the None rows — a compilation error (hit live 2026-07-02). Snowflake coerces
    # an ISO string to DATE on insert; None binds as plain NULL.
    cur.executemany(
        "INSERT INTO LIBRARY_META.REGISTRY.SOURCE_FRESHNESS "
        "(SOURCE_ID, LANDING_FQN, RECENCY_COL, RECENCY_KIND, DATA_THROUGH_ISO, ROW_COUNT, "
        " CADENCE_BUCKET, FRESHNESS_STATE, NOTE) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [(r["source_id"], r["landing_fqn"], r["recency_col"], r["recency_kind"], r["data_through"],
          r["row_count"], r["cadence_bucket"], r["freshness_state"], r["note"][:4000]) for r in rows],
    )
    cur.close()
    print(f"APPLIED — SOURCE_FRESHNESS ({len(rows)} rows) + V_SOURCE_FRESHNESS live in LIBRARY_META.REGISTRY.")
    print("  Query it:  SELECT FRESHNESS_STATE, COUNT(*) FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS GROUP BY 1;")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the data-freshness ledger (preview by default)")
    ap.add_argument("--apply", action="store_true", help="create + populate the ledger (Chris, ACCOUNTADMIN)")
    ap.add_argument("--rotting", action="store_true", help="preview only overdue/stale sources")
    args = ap.parse_args(argv)

    mapping = json.loads(MAPPING.read_text())
    conn = snow.connect()
    try:
        rows = measure(conn, mapping)
        if args.apply:
            preview(rows, rotting_only=False)
            return apply(conn, rows)
        preview(rows, rotting_only=args.rotting)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
