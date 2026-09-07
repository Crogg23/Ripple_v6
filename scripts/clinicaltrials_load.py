"""Crawl every study on ClinicalTrials.gov through the v2 API and land it.

Target: LIBRARY_RAW.LANDING.FED_CLINICALTRIALS_FULL, a NEW table. The old
FED_CLINICALTRIALS (500 rows, one API page, 2026-06) is never touched.

Shape: the same 35 data columns the old table carries, all VARCHAR, so the
existing staging model can be re-pointed with a one-line source change. JSON
blocks (LOCATIONS, INTERVENTIONS, RESPONSIBLE_PARTY, ...) land as json text,
exactly as before. Plus three meta columns: _INGESTED_AT (ISO text, NOT the
epoch-micros NUMBER the old table carries -- see traps 2026-09-02),
_SOURCE_RUN_ID, _SRC_SHA256 (sha256 of the page body the row came from).

API: https://clinicaltrials.gov/api/v2/studies?pageSize=1000&pageToken=...
     ~600K studies on 2026-09-07, so ~600 pages. No key needed.

Usage:
    python scripts/clinicaltrials_load.py          # dry run: first page + total
    python scripts/clinicaltrials_load.py --run    # land everything, resumable

Resume: logs/clinicaltrials_checkpoint.json holds the next pageToken and the
run id. A page token is an exact cursor, so a restart continues where the last
flushed page ended. Not airtight: the checkpoint is written AFTER the flush, so
a crash between COPY commit and checkpoint write re-lands up to FLUSH_PAGES
pages, and the auth-expiry retry re-sends a whole batch. Nothing enforces
uniqueness on NCT_ID. After any resumed run, count distinct NCT_ID. Delete the checkpoint to start over
(the table is appended to, so a fresh start on a non-empty table doubles rows;
the script refuses that unless --append-anyway).

Pattern: scripts/senate_lda_load.py (stream pages, flush a buffer, checkpoint,
reconnect on auth expiry).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import uuid
from datetime import datetime, timezone
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

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
USER_AGENT = "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"
HEADERS = {"User-Agent": USER_AGENT, "Accept": "application/json"}
PAGE_SIZE = 1000
REQUEST_DELAY = 0.25        # seconds between pages; the API has no published cap
TABLE = "FED_CLINICALTRIALS_FULL"
CHECKPOINT_FILE = _REPO / "logs" / "clinicaltrials_checkpoint.json"
FLUSH_PAGES = 10            # 10 pages = 10,000 rows per write_pandas call
PROGRESS_EVERY = 50         # pages

# The 35 data columns of LIBRARY_RAW.LANDING.FED_CLINICALTRIALS, in its order.
COLUMNS = [
    "NCT_ID", "BRIEF_TITLE", "OFFICIAL_TITLE", "OVERALL_STATUS", "PHASE",
    "STUDY_TYPE", "START_DATE", "COMPLETION_DATE", "PRIMARY_COMPLETION_DATE",
    "ENROLLMENT", "LEAD_SPONSOR_NAME", "LEAD_SPONSOR_CLASS", "COLLABORATORS",
    "CONDITIONS", "INTERVENTIONS", "PRIMARY_OUTCOMES", "SECONDARY_OUTCOMES",
    "ELIGIBILITY_CRITERIA", "GENDER", "MINIMUM_AGE", "MAXIMUM_AGE", "LOCATIONS",
    "RESULTS_FIRST_POSTED_DATE", "HAS_RESULTS", "WHY_STOPPED", "RESPONSIBLE_PARTY",
    "KEYWORDS", "REFERENCES", "ORG_STUDY_ID", "SECONDARY_IDS", "OVERSIGHT_HAS_DMC",
    "IS_FDA_REGULATED_DRUG", "IS_FDA_REGULATED_DEVICE", "LAST_UPDATE_POSTED_DATE",
    "FIRST_POSTED_DATE",
]
META = ["_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"]


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------
def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {}


def save_checkpoint(cp: dict) -> None:
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(json.dumps(cp, indent=2))


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
def fetch_page(page_token: str | None, count_total: bool = False) -> tuple[dict, bytes]:
    """One page of studies. Returns (parsed json, raw body bytes for hashing).
    Retries 429, 5xx and network drops; a 600-page crawl must survive those."""
    params = {"pageSize": PAGE_SIZE, "format": "json"}
    if page_token:
        params["pageToken"] = page_token
    if count_total:
        params["countTotal"] = "true"
    for attempt in range(8):
        time.sleep(REQUEST_DELAY)
        try:
            r = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=120)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as exc:
            wait = min(300, 15 * (attempt + 1))
            print(f"    network error ({str(exc)[:60]}), retry in {wait}s...", flush=True)
            time.sleep(wait)
            continue
        if r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 30))
            print(f"    429 throttled, waiting {retry_after}s...", flush=True)
            time.sleep(retry_after + 1)
            continue
        if r.status_code >= 500:
            wait = min(300, 15 * (attempt + 1))
            print(f"    HTTP {r.status_code}, retry in {wait}s...", flush=True)
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json(), r.content
    raise RuntimeError(f"Failed after 8 retries at pageToken={page_token!r}")


# ---------------------------------------------------------------------------
# Flatten one study to the 35-column shape
# ---------------------------------------------------------------------------
def _j(v):
    """JSON text for lists/dicts, matching how the old table stored them."""
    if v is None:
        return None
    return json.dumps(v, ensure_ascii=False)


def _b(v):
    """Booleans landed as the strings 'True' / 'False' in the old table."""
    if v is None:
        return None
    return "True" if v else "False"


def _date(struct):
    return (struct or {}).get("date")


def flatten_study(study: dict) -> dict:
    p = study.get("protocolSection") or {}
    ident = p.get("identificationModule") or {}
    status = p.get("statusModule") or {}
    spons = p.get("sponsorCollaboratorsModule") or {}
    design = p.get("designModule") or {}
    cond = p.get("conditionsModule") or {}
    arms = p.get("armsInterventionsModule") or {}
    outc = p.get("outcomesModule") or {}
    elig = p.get("eligibilityModule") or {}
    locs = p.get("contactsLocationsModule") or {}
    refs = p.get("referencesModule") or {}
    over = p.get("oversightModule") or {}
    lead = spons.get("leadSponsor") or {}
    enroll = design.get("enrollmentInfo") or {}
    return {
        "NCT_ID": ident.get("nctId"),
        "BRIEF_TITLE": ident.get("briefTitle"),
        "OFFICIAL_TITLE": ident.get("officialTitle"),
        "OVERALL_STATUS": status.get("overallStatus"),
        "PHASE": _j(design.get("phases")),
        "STUDY_TYPE": design.get("studyType"),
        "START_DATE": _date(status.get("startDateStruct")),
        "COMPLETION_DATE": _date(status.get("completionDateStruct")),
        "PRIMARY_COMPLETION_DATE": _date(status.get("primaryCompletionDateStruct")),
        "ENROLLMENT": (str(enroll["count"]) if enroll.get("count") is not None else None),
        "LEAD_SPONSOR_NAME": lead.get("name"),
        "LEAD_SPONSOR_CLASS": lead.get("class"),
        "COLLABORATORS": _j(spons.get("collaborators") or []),
        "CONDITIONS": _j(cond.get("conditions") or []),
        "INTERVENTIONS": _j(arms.get("interventions") or []),
        "PRIMARY_OUTCOMES": _j(outc.get("primaryOutcomes") or []),
        "SECONDARY_OUTCOMES": _j(outc.get("secondaryOutcomes") or []),
        "ELIGIBILITY_CRITERIA": elig.get("eligibilityCriteria"),
        "GENDER": elig.get("sex"),
        "MINIMUM_AGE": elig.get("minimumAge"),
        "MAXIMUM_AGE": elig.get("maximumAge"),
        "LOCATIONS": _j(locs.get("locations") or []),
        "RESULTS_FIRST_POSTED_DATE": _date(status.get("resultsFirstPostDateStruct")),
        "HAS_RESULTS": _b(study.get("hasResults")),
        "WHY_STOPPED": status.get("whyStopped"),
        "RESPONSIBLE_PARTY": _j(spons.get("responsibleParty")),
        "KEYWORDS": _j(cond.get("keywords") or []),
        "REFERENCES": _j(refs.get("references") or []),
        "ORG_STUDY_ID": (ident.get("orgStudyIdInfo") or {}).get("id"),
        "SECONDARY_IDS": _j(ident.get("secondaryIdInfos") or []),
        "OVERSIGHT_HAS_DMC": _b(over.get("oversightHasDmc")),
        "IS_FDA_REGULATED_DRUG": _b(over.get("isFdaRegulatedDrug")),
        "IS_FDA_REGULATED_DEVICE": _b(over.get("isFdaRegulatedDevice")),
        "LAST_UPDATE_POSTED_DATE": _date(status.get("lastUpdatePostDateStruct")),
        "FIRST_POSTED_DATE": _date(status.get("studyFirstPostDateStruct")),
    }


# ---------------------------------------------------------------------------
# Snowflake
# ---------------------------------------------------------------------------
_conn = None


def get_conn():
    """Health-checked connection; a crawl this long outlives an auth token."""
    global _conn
    if _conn is not None:
        try:
            _conn.cursor().execute("select 1")
            return _conn
        except Exception:
            try:
                _conn.close()
            except Exception:
                pass
            _conn = None
            print("    (snowflake session expired -- reconnecting)", flush=True)
    _conn = snow.connect()
    return _conn


def _reset_conn():
    global _conn
    try:
        if _conn is not None:
            _conn.close()
    except Exception:
        pass
    _conn = None


def ensure_table(conn) -> None:
    cols_sql = ", ".join(f'"{c}" VARCHAR' for c in COLUMNS + META)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{TABLE}" ({cols_sql})')
    cur.close()


def table_rows(conn) -> int:
    cur = conn.cursor()
    try:
        cur.execute(f'select count(*) from {bulk.LANDING_FQS}."{TABLE}"')
        return int(cur.fetchone()[0])
    except Exception:
        return 0
    finally:
        cur.close()


def upload_rows(rows: list[dict], run_id: str) -> None:
    try:
        _upload_inner(get_conn(), rows, run_id)
    except Exception as e:
        if "390114" not in str(e) and "expired" not in str(e).lower():
            raise
        print("    (auth expired mid-upload -- reconnecting and retrying once)", flush=True)
        _reset_conn()
        _upload_inner(get_conn(), rows, run_id)


def _upload_inner(conn, rows: list[dict], run_id: str) -> None:
    from snowflake.connector.pandas_tools import write_pandas
    df = pd.DataFrame(rows, columns=COLUMNS + META)
    df["_INGESTED_AT"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    df["_SOURCE_RUN_ID"] = run_id
    df = df.astype(object).where(pd.notna(df), None)
    ensure_table(conn)
    ok, _c, _n, _ = write_pandas(conn, df, TABLE, database=bulk.LANDING_DB,
                                 schema=bulk.LANDING_SCHEMA, quote_identifiers=False,
                                 auto_create_table=False)
    if not ok:
        raise RuntimeError(f"write_pandas failed for {TABLE}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", action="store_true", help="land it; default is a dry run")
    ap.add_argument("--append-anyway", action="store_true",
                    help="allow a fresh crawl (no checkpoint) onto a non-empty table")
    args = ap.parse_args()

    first, body = fetch_page(None, count_total=True)
    total = first.get("totalCount")
    studies = first.get("studies") or []
    est_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total else "?"
    print(f"ClinicalTrials.gov v2: totalCount={total:,}  pageSize={PAGE_SIZE}  "
          f"~{est_pages} pages", flush=True)
    print(f"first page: {len(studies)} studies, next token present: "
          f"{bool(first.get('nextPageToken'))}")

    if not args.run:
        sample = flatten_study(studies[0]) if studies else {}
        print("\nfirst study, flattened to the 35-column shape:")
        for k in COLUMNS:
            v = sample.get(k)
            print(f"  {k:<26} {str(v)[:90] if v is not None else None}")
        filled = sum(1 for k in COLUMNS if sample.get(k) not in (None, "[]"))
        print(f"\n{filled} of {len(COLUMNS)} columns filled on the first study")
        print("\n(dry run -- add --run to land into "
              f"{bulk.LANDING_FQS}.{TABLE})")
        return

    cp = load_checkpoint()
    conn = get_conn()  # fail fast on credentials
    ensure_table(conn)
    existing = table_rows(conn)
    if cp:
        run_id = cp["run_id"]
        token = cp.get("next_token")
        pages_done = cp.get("pages_done", 0)
        rows_done = cp.get("rows_done", 0)
        if token is None and cp.get("finished"):
            print(f"checkpoint says finished: {rows_done:,} rows over {pages_done} pages. "
                  "Delete logs/clinicaltrials_checkpoint.json to crawl again.")
            return
        print(f"resuming run {run_id[:8]} at page {pages_done + 1}, "
              f"{rows_done:,} rows landed so far, table holds {existing:,}", flush=True)
    else:
        if existing and not args.append_anyway:
            print(f"{TABLE} already holds {existing:,} rows and there is no checkpoint. "
                  "Refusing to append a fresh crawl on top. Pass --append-anyway "
                  "if that is really wanted.")
            sys.exit(2)
        run_id = str(uuid.uuid4())
        token = None
        pages_done = rows_done = 0
        print(f"new run {run_id[:8]}", flush=True)

    buf: list[dict] = []
    buffered_pages = 0
    t0 = time.time()

    def flush(next_token, finished=False):
        nonlocal buf, buffered_pages, rows_done
        if buf:
            upload_rows(buf, run_id)
            rows_done += len(buf)
            buf = []
            buffered_pages = 0
        save_checkpoint({"run_id": run_id, "next_token": next_token,
                         "pages_done": pages_done, "rows_done": rows_done,
                         "finished": finished, "total_count": total,
                         "updated_at": datetime.now(timezone.utc).isoformat()})

    while True:
        if pages_done == 0 and token is None:
            data, body = first, body
        else:
            data, body = fetch_page(token)
        sha = hashlib.sha256(body).hexdigest()
        page_rows = [dict(flatten_study(s), _SRC_SHA256=sha)
                     for s in (data.get("studies") or [])]
        buf.extend(page_rows)
        buffered_pages += 1
        pages_done += 1
        next_token = data.get("nextPageToken")

        if pages_done % PROGRESS_EVERY == 0:
            el = time.time() - t0
            print(f"  page {pages_done}/{est_pages}  {rows_done + len(buf):,} rows  "
                  f"{el/60:.1f} min", flush=True)

        if not next_token:
            flush(None, finished=True)
            break
        token = next_token
        if buffered_pages >= FLUSH_PAGES:
            flush(token)

    final = table_rows(get_conn())
    print(f"\ndone: {pages_done} pages, {rows_done:,} rows landed this run, "
          f"{TABLE} now holds {final:,} rows, {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
