#!/usr/bin/env python3
"""Federal Register documents backfill (discovery sweep #58/#73: looks like a panel,
is a snapshot). FED_FEDERAL_REGISTER_DOCUMENTS is currently the API's most-recent
5,000 documents -- a ~9.5-week window (2026-04-10 .. 2026-06-16). That makes the
"track federal rulemaking over time" promise a lie: there's no time to track.

This SNAPSHOT-REPLACES the table with the full requested window
(2023-01-01 .. 2026-06-16, ~3.5 years, ~84k documents) by paginating the public
JSON API. The API caps deep paging (max 2,000 pages / search_after cursor), so we
window by MONTH and follow `next_page_url` (cursor pagination) within each month --
no window exceeds a few thousand docs, far under any page cap.

Source: https://www.federalregister.gov/api/v1/documents.json
  per_page=1000 + fields[] (all 29 landing columns) + conditions[publication_date][gte/lte]

The document objects carry nested JSON (agencies[], agency_names[], president{},
images{}, docket_ids[], ...). We flatten each field to the existing landing column:
scalars as-is, arrays/objects serialized to a JSON string (matching how the current
snapshot stores AGENCIES). Meta cols stamped via the shared ingest module.

Idempotent: snapshot-replace. The first write_pandas uses overwrite=True (truncate +
reload), subsequent batches append. Re-running fully rebuilds the table.

    python3 scripts/federal_register_backfill.py                       # preview (counts, no load)
    python3 scripts/federal_register_backfill.py --run                 # full 2023-01-01..2026-06-16
    python3 scripts/federal_register_backfill.py --start 2024-01-01 --end 2024-12-31 --run

BUDGET: ~84k small text rows on RIPPLE_WH (X-Small). Trivial credits/storage. The
HTTP fetch (a few hundred paginated calls) is the slow part, not Snowflake.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

TABLE = "FED_FEDERAL_REGISTER_DOCUMENTS"
SID = "fed_federal_register_documents"
API = "https://www.federalregister.gov/api/v1/documents.json"
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
PER_PAGE = 1000
DEFAULT_GTE = "2023-01-01"
DEFAULT_LTE = "2026-06-16"
SCRATCH = Path("c:/Code/Ripple_v6/.scratch/"
               "e8eac5fb-de36-4362-9440-da24a904b9b4/scratchpad")

# Landing column  <-  API field. (snake_case API field name)
# Order matches DESCRIBE TABLE so the frame lines up before write_pandas.
COLMAP = {
    "DOCUMENT_NUMBER": "document_number",
    "TITLE": "title",
    "TYPE": "type",
    "ABSTRACT": "abstract",
    "ACTION": "action",
    "AGENCIES": "agencies",
    "AGENCY_NAMES": "agency_names",
    "PUBLICATION_DATE": "publication_date",
    "EFFECTIVE_ON": "effective_on",
    "CITATION": "citation",
    "START_PAGE": "start_page",
    "END_PAGE": "end_page",
    "HTML_URL": "html_url",
    "PDF_URL": "pdf_url",
    "FULL_TEXT_XML_URL": "full_text_xml_url",
    "BODY_HTML_URL": "body_html_url",
    "JSON_URL": "json_url",
    "DOCKET_IDS": "docket_ids",
    "REGULATION_ID_NUMBERS": "regulation_id_numbers",
    "CFR_REFERENCES": "cfr_references",
    "SIGNIFICANT": "significant",
    "EXECUTIVE_ORDER_NOTES": "executive_order_notes",
    "COMMENTS_CLOSE_ON": "comments_close_on",
    "SUBTYPE": "subtype",
    "PRESIDENT": "president",
    "EXCERPTS": "excerpts",
    "IMAGES": "images",
    "PAGE_LENGTH": "page_length",
    "RAW_TEXT_URL": "raw_text_url",
}
DATA_COLS = list(COLMAP.keys())
META_COLS = [ingest.META_INGESTED_AT, ingest.META_SOURCE_RUN_ID, ingest.META_SRC_SHA256]
TABLE_COLS = DATA_COLS + META_COLS
API_FIELDS = list(COLMAP.values())


def _flatten(v):
    """One API field value -> one landing TEXT cell.

    Scalars (str/int/float/bool) pass through as text. Nested arrays/objects
    (agencies[], president{}, images{}, docket_ids[], ...) are JSON-serialized so
    the cell mirrors how the current snapshot stores AGENCIES (a JSON string).
    None -> None (lands as SQL NULL). Empty list/dict -> "[]" / "{}" to match
    the live API surface.
    """
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    return str(v)


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(UA)
    return s


def _months(gte: str, lte: str) -> list[tuple[str, str]]:
    """Split [gte, lte] into per-calendar-month [start, end] windows (inclusive)."""
    a = _dt.date.fromisoformat(gte)
    b = _dt.date.fromisoformat(lte)
    out: list[tuple[str, str]] = []
    cur = _dt.date(a.year, a.month, 1)
    while cur <= b:
        if cur.month == 12:
            nxt = _dt.date(cur.year + 1, 1, 1)
        else:
            nxt = _dt.date(cur.year, cur.month + 1, 1)
        win_start = max(cur, a)
        win_end = min(nxt - _dt.timedelta(days=1), b)
        out.append((win_start.isoformat(), win_end.isoformat()))
        cur = nxt
    return out


def _fetch_window(sess: requests.Session, gte: str, lte: str) -> list[dict]:
    """All documents in [gte, lte], following cursor pagination (next_page_url)."""
    params = {
        "per_page": PER_PAGE,
        "fields[]": API_FIELDS,
        "conditions[publication_date][gte]": gte,
        "conditions[publication_date][lte]": lte,
    }
    url = API
    out: list[dict] = []
    first = True
    while url:
        for attempt in range(5):
            try:
                r = sess.get(url, params=params if first else None, timeout=120)
                if r.status_code == 200:
                    break
                if r.status_code in (429, 500, 502, 503, 504):
                    time.sleep(2 * (attempt + 1))
                    continue
                r.raise_for_status()
            except requests.RequestException:
                if attempt == 4:
                    raise
                time.sleep(2 * (attempt + 1))
        first = False
        data = r.json()
        out.extend(data.get("results", []) or [])
        url = data.get("next_page_url")
        # be polite to a .gov endpoint
        time.sleep(0.15)
    return out


def _window_count(sess: requests.Session, gte: str, lte: str) -> int:
    r = sess.get(API, params={
        "per_page": 1,
        "conditions[publication_date][gte]": gte,
        "conditions[publication_date][lte]": lte,
    }, timeout=60)
    r.raise_for_status()
    return int(r.json().get("count") or 0)


def _to_frame(records: list[dict]) -> pd.DataFrame:
    rows = []
    for rec in records:
        row = {col: _flatten(rec.get(api_field)) for col, api_field in COLMAP.items()}
        rows.append(row)
    df = pd.DataFrame(rows, columns=DATA_COLS)
    # everything lands as TEXT; force object dtype so write_pandas doesn't infer numerics
    return df.astype(object)


def main() -> int:
    ap = argparse.ArgumentParser(description="Federal Register full-window backfill (snapshot-replace).")
    ap.add_argument("--start", default=DEFAULT_GTE, help="publication_date gte (YYYY-MM-DD)")
    ap.add_argument("--end", default=DEFAULT_LTE, help="publication_date lte (YYYY-MM-DD)")
    ap.add_argument("--run", action="store_true", help="actually fetch + snapshot-replace (else preview)")
    args = ap.parse_args()

    gte, lte = args.start, args.end
    windows = _months(gte, lte)
    sess = _session()

    # ---- PREVIEW: total count via month windows (count is exact when < 10k) ----
    print(f"Federal Register backfill  {gte} .. {lte}   ({len(windows)} monthly windows)")
    total = 0
    for (a, b) in windows:
        n = _window_count(sess, a, b)
        total += n
    print(f"PREVIEW: ~{total:,} documents in window "
          f"(API per_page={PER_PAGE}, cursor pagination, snapshot-replace {TABLE}).")
    if total > 25_000_000:
        print("!! Window exceeds 25M rows -- bound it tighter (--start/--end).")
        return 2
    if not args.run:
        print("\nPREVIEW only. Add --run to fetch all windows and SNAPSHOT-REPLACE the table.")
        return 0

    # ---- RUN: fetch all windows, flatten, snapshot-replace ----
    run_id = uuid.uuid4().hex[:16]
    started = ingest._utcnow()
    conn = snow.connect()
    appended = 0
    first_write = True
    sha = hashlib.sha256()
    try:
        for i, (a, b) in enumerate(windows, 1):
            recs = _fetch_window(sess, a, b)
            if not recs:
                print(f"  [{i}/{len(windows)}] {a}..{b}  0 docs", flush=True)
                continue
            df = _to_frame(recs)
            # stable provenance hash over the document numbers + dates in this window
            sha.update(("|".join(sorted(
                (str(x) for x in df["DOCUMENT_NUMBER"].tolist()))) + a + b).encode("utf-8"))
            df[ingest.META_INGESTED_AT] = int(started.timestamp() * 1_000_000)  # epoch micros (INTEGER col)
            df[ingest.META_SOURCE_RUN_ID] = run_id
            df[ingest.META_SRC_SHA256] = ""  # set after full hash known; placeholder keeps schema
            df = df[TABLE_COLS]
            ok, _c, n, _ = write_pandas(
                conn, df, table_name=TABLE,
                database=settings.raw_database, schema=settings.raw_schema,
                auto_create_table=False, overwrite=first_write, quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write_pandas failed in window {a}..{b} after {appended:,} rows")
            appended += len(df)
            first_write = False
            print(f"  [{i}/{len(windows)}] {a}..{b}  {len(df):>5,} docs  (cumulative {appended:,})",
                  flush=True)

        full_sha = sha.hexdigest()
        # stamp the real provenance hash now that the full window is hashed
        cur = conn.cursor()
        cur.execute(f"UPDATE LIBRARY_RAW.LANDING.{TABLE} SET {ingest.META_SRC_SHA256} = %s "
                    f"WHERE {ingest.META_SOURCE_RUN_ID} = %s", (full_sha, run_id))
        cur.close()

        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", appended, 0, full_sha,
                        f"{API}?gte={gte}&lte={lte}", started, ended,
                        f"Federal Register backfill {gte}..{lte}: snapshot-replaced "
                        f"{appended:,} documents across {len(windows)} monthly windows.")

        # ---- confirm the unlock ----
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*), MIN(PUBLICATION_DATE), MAX(PUBLICATION_DATE), "
                    f"COUNT(DISTINCT PUBLICATION_DATE), "
                    f"COUNT(DISTINCT LEFT(PUBLICATION_DATE,4)) "
                    f"FROM LIBRARY_RAW.LANDING.{TABLE}")
        cnt, mn, mx, ndates, nyears = cur.fetchone()
        cur.close()
        print(f"\nDONE: {appended:,} loaded. {TABLE} now = {cnt:,} rows, "
              f"{mn} .. {mx}, {ndates:,} distinct dates across {nyears} years.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
