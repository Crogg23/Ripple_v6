"""Export LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX -> outputs/portal_index.json.

SETUP: loads library-onboarding/.env (override=True) and connects with
snowflake-connector-python using SNOWFLAKE_PAT (passed as the password, the
project's standard PAT auth).

Run modes:
    python export_portal_index.py --discover   # STEP 1 only: print real schema
    python export_portal_index.py              # STEP 1 + STEP 2/3 export

Nothing about the table's columns is hardcoded blindly -- Step 1 discovers the
real names live; the extract in Step 2 uses exactly those.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# --- SETUP: source library-onboarding/.env every time ----------------------
ENV_PATH = Path(__file__).resolve().parent.parent / "library-onboarding" / ".env"
load_dotenv(ENV_PATH, override=True)

import snowflake.connector

FQN = "LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX"
OUT = Path(__file__).resolve().parent.parent / "outputs" / "portal_index.json"


def connect():
    pat = os.environ.get("SNOWFLAKE_PAT", "").strip()
    if not pat:
        sys.exit(f"FATAL: no SNOWFLAKE_PAT after loading {ENV_PATH}")
    print(f"[setup] loaded {ENV_PATH}  (PAT present, len={len(pat)})")
    return snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "ONEAFDA-UMB20733"),
        user=os.environ.get("SNOWFLAKE_USER", "CROGG23"),
        password=pat,  # PAT works as a password replacement
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "RIPPLE_WH"),
        role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    )


def discover(cur):
    """STEP 1 -- print the real schema. No guessing."""
    print("=" * 78)
    print(f"SHOW COLUMNS IN TABLE {FQN}")
    print("=" * 78)
    cur.execute(f"SHOW COLUMNS IN TABLE {FQN}")
    desc = [d[0] for d in cur.description]
    idx = {n: i for i, n in enumerate(desc)}
    ci = idx.get("column_name", 2)
    di = idx.get("data_type", 3)
    rows = cur.fetchall()
    print(f"{'COLUMN_NAME':<34} DATA_TYPE")
    print(f"{'-'*33:<34} {'-'*30}")
    for r in rows:
        print(f"{str(r[ci]):<34} {r[di]}")
    print(f"\n({len(rows)} columns)\n")

    print("=" * 78)
    print(f"SELECT * FROM {FQN} LIMIT 1   (one row, values truncated; arrays parsed)")
    print("=" * 78)
    cur.execute(f"SELECT * FROM {FQN} LIMIT 1")
    cols = [d[0] for d in cur.description]
    row = cur.fetchone()
    if row is None:
        print("(table is empty)")
        return cols
    for name, val in zip(cols, row):
        s = "" if val is None else str(val)
        extra = ""
        if isinstance(val, str) and val[:1] in "[{":
            try:
                j = json.loads(val)
                if isinstance(j, list):
                    extra = f"   <JSON array · len={len(j)} · e.g. {j[:3]}>"
                elif isinstance(j, dict):
                    extra = f"   <JSON object · keys={list(j.keys())[:8]}>"
            except Exception:
                pass
        if len(s) > 200:
            s = s[:200] + f" ...[{len(str(val))} chars total]"
        print(f"{name:<34} = {s}{extra}")
    print()
    return cols


# --- value coercion --------------------------------------------------------
def as_int(v):
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None


def as_list(v):
    """ARRAY columns arrive from the connector as JSON text (or None) -- return
    a real Python list so the output JSON has true arrays, not strings."""
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
            return parsed if isinstance(parsed, list) else []
        except Exception:
            return []
    return []


def extract(cur, dump_all=False):
    """STEP 2 -- pull the needed columns using the REAL names confirmed in
    STEP 1. Default = fingerprinted datasets only (those carrying a COLUMN_NAMES
    array, which also have JOIN_KEYS + TOP_TIER); --all includes bare stubs."""
    where = "" if dump_all else "WHERE COLUMN_NAMES IS NOT NULL"
    sql = (
        "SELECT DATASET_TITLE, PORTAL_NAME, ROW_COUNT, TOP_TIER, SOURCE_URL, "
        f"COLUMN_NAMES, JOIN_KEYS FROM {FQN} {where} ORDER BY DATASET_UID"
    )
    print("STEP 2 -- pull:")
    print("  " + sql)
    cur.execute(sql)
    out = []
    for title, portal, rc, tier, url, cols, joins in cur:
        out.append({
            "title": title,
            "portal": portal,
            "row_count": as_int(rc),
            "confidence_tier": tier,
            "url": url,
            "columns": as_list(cols),
            "join_keys": as_list(joins),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--discover", action="store_true", help="STEP 1 only: print schema")
    ap.add_argument("--all", action="store_true",
                    help="export ALL 338k rows incl. untagged stubs (default: fingerprinted only)")
    args = ap.parse_args()

    conn = connect()
    cur = conn.cursor()
    try:
        discover(cur)  # STEP 1 -- discover real schema, every run
        if args.discover:
            print("[discover] done -- run without --discover to export.")
            return
        rows = extract(cur, dump_all=args.all)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        size_mb = OUT.stat().st_size / 1e6
        print()
        print("STEP 3 -- wrote %s objects -> %s  (%.1f MB)" % (f"{len(rows):,}", OUT, size_mb))
        print("filter: %s" % ("ALL rows" if args.all else "fingerprinted only (COLUMN_NAMES not null)"))
        print("first 2 objects:")
        print(json.dumps(rows[:2], ensure_ascii=False, indent=2))
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
