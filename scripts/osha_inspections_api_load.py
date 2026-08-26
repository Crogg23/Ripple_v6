"""Re-pull OSHA workplace inspections from the DOL v4 API into LANDING.

The July 2026 sweep found the OSHA inspections table was destroyed by a load
that logged success, and the old enforcedata.dol.gov bulk ZIPs are gone
(the URLs now serve a Drupal page). The DOL API works with the key in
library-onboarding/.env, pages at 5,000 rows, and supports keyset pagination
on activity_nr — verified live 2026-08-22.

Keyset pagination (activity_nr > last), NOT offset — offset paging on
multi-million-row endpoints has been capped before (FDIC, 2M).

Checkpointed: progress lands in data/osha_inspections/checkpoint.json and
each page batch appends to Snowflake as it goes, so a kill resumes where it
left off. All values land as TEXT (byte-faithful landing; NaN never written —
values pass through _as_text).

    python scripts/osha_inspections_api_load.py            # preview (2 pages)
    python scripts/osha_inspections_api_load.py --run      # full pull, resumable
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

TABLE = "FED_DOL_OSHA_INSPECTIONS"
BASE = "https://apiprod.dol.gov/v4/get/osha/inspection/json"
PAGE = 5000
UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
CKPT = _REPO / "data" / "osha_inspections" / "checkpoint.json"


def _as_text(v):
    """NaN/None -> None, everything else -> str. Never let pandas NaN reach Snowflake."""
    if v is None:
        return None
    if isinstance(v, float) and v != v:
        return None
    s = str(v)
    return None if s == "" else s


def fetch_page(key: str, after: int) -> list[dict]:
    fo = urllib.parse.quote(json.dumps(
        {"field": "activity_nr", "operator": "gt", "value": after}))
    url = (f"{BASE}?limit={PAGE}&sort_by=activity_nr&sort=asc"
           f"&filter_object={fo}&X-API-KEY={key}")
    # The DOL quota window is long — sustained 429s for 7+ minutes observed
    # 2026-08-22 — so be very patient: up to ~4h of backoff before giving up.
    for attempt in range(30):
        try:
            r = requests.get(url, timeout=180, headers=UA)
            r.raise_for_status()
            return r.json().get("data", [])
        except Exception as e:
            wait = min(600, 60 * (attempt + 1))
            print(f"  page after={after} attempt {attempt+1} failed "
                  f"({str(e)[:80]}); retry in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"page after={after}: 30 straight failures")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--pages", type=int, default=None,
                    help="stop after N pages (default: run to exhaustion)")
    args = ap.parse_args()

    key = os.environ.get("DOL_API_KEY", "")
    if not key:
        print("DOL_API_KEY not set"); return 1

    preview_pages = 2 if not args.run else args.pages

    CKPT.parent.mkdir(parents=True, exist_ok=True)
    # start at 1, not 0 — the API 500s on filter value 0 (verified 2026-08-22);
    # first real activity_nr is 18 so nothing is skipped
    state = {"last_activity_nr": 1, "rows_loaded": 0, "table_created": False}
    if CKPT.exists():
        state = json.loads(CKPT.read_text())
        print(f"Resuming from activity_nr={state['last_activity_nr']:,} "
              f"({state['rows_loaded']:,} rows already loaded)", flush=True)

    conn = snow.connect() if args.run else None
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    from snowflake.connector.pandas_tools import write_pandas

    # Reconcile against the warehouse before trusting the checkpoint file.
    # 2026-08-25 finding: a run that crashes between write_pandas succeeding
    # and CKPT.write_text() running leaves the checkpoint behind what's
    # actually landed -- the next --run then re-fetches and re-appends a
    # block of already-loaded pages (415,000 duplicate rows caught live this
    # session). Snowflake is ground truth for what's landed; the checkpoint
    # is only a resume hint.
    if args.run and state.get("table_created"):
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT MAX(TRY_TO_NUMBER(ACTIVITY_NR)), COUNT(*) FROM "
                f"{bulk.LANDING_DB}.{bulk.LANDING_SCHEMA}.{TABLE}")
            live_max, live_count = cur.fetchone()
            if live_max is not None and int(live_max) > state["last_activity_nr"]:
                print(f"Checkpoint said last_activity_nr={state['last_activity_nr']:,} but "
                      f"the warehouse already has rows up to {int(live_max):,} "
                      f"({live_count:,} total) -- trusting the warehouse, not the stale "
                      f"checkpoint.", flush=True)
                state["last_activity_nr"] = int(live_max)
                state["rows_loaded"] = int(live_count)
        except Exception as e:
            print(f"Warehouse reconciliation check failed ({e}); "
                  f"trusting checkpoint file as-is.", flush=True)

    pages = 0
    while True:
        rows = fetch_page(key, state["last_activity_nr"])
        if not rows:
            print("Exhausted — no more rows.", flush=True)
            break
        df = pd.DataFrame(rows)
        df = df.map(_as_text)
        df.columns = [bulk.sf_col(c) for c in df.columns]
        df[bulk.META_INGESTED_AT] = started
        df[bulk.META_SOURCE_RUN_ID] = run_id
        df[bulk.META_SRC_SHA256] = None

        last = max(int(r["activity_nr"]) for r in rows)
        pages += 1

        if args.run:
            # Create the table EXPLICITLY, every column VARCHAR. auto_create_table
            # types columns off the first page's values, and a column that is
            # all-null on page 1 lands as NUMBER — page 2's "X" then kills the
            # append (hit live 2026-08-22). Landing is byte-faithful TEXT anyway.
            if not state["table_created"]:
                data_cols = [c for c in df.columns
                             if c not in (bulk.META_INGESTED_AT,
                                          bulk.META_SOURCE_RUN_ID,
                                          bulk.META_SRC_SHA256)]
                ddl_cols = ", ".join(f"{c} VARCHAR" for c in data_cols)
                conn.cursor().execute(
                    f"create or replace table {bulk.LANDING_DB}.{bulk.LANDING_SCHEMA}.{TABLE} "
                    f"({ddl_cols}, {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                    f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR)")
                state["table_cols"] = list(df.columns)
            # keep column order/set stable across pages; a NEW api column should
            # fail loudly, not silently shift
            missing = [c for c in state.get("table_cols", list(df.columns))
                       if c not in df.columns]
            for c in missing:
                df[c] = None
            extra = [c for c in df.columns if c not in state.get("table_cols", list(df.columns))]
            if extra:
                raise RuntimeError(f"API added new columns mid-pull: {extra}")
            df = df[state.get("table_cols", list(df.columns))]
            ok, _c, _n, _ = write_pandas(
                conn, df, table_name=TABLE,
                database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                auto_create_table=False,
                overwrite=False, quote_identifiers=False,
            )
            if not ok:
                raise RuntimeError(f"write_pandas failed at after="
                                   f"{state['last_activity_nr']}")
            state["table_created"] = True
            state["rows_loaded"] += len(df)
            state["last_activity_nr"] = last
            CKPT.write_text(json.dumps(state))
        else:
            print(df.iloc[0].to_dict() if pages == 1 else "", flush=True)
            state["last_activity_nr"] = last

        print(f"page {pages}: {len(df):,} rows, up to activity_nr={last:,} "
              f"(total {state['rows_loaded']:,})", flush=True)
        time.sleep(5)  # the API rate-limits (429s observed); stay polite

        if preview_pages and pages >= preview_pages:
            print(f"Stopping after {pages} pages "
                  f"({'preview' if not args.run else '--pages cap'}).", flush=True)
            break
        if len(rows) < PAGE:
            print("Short page — done.", flush=True)
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
