"""Load Senate LDA (Lobbying Disclosure Act) filings via REST API.

Endpoints:
  - /filings/         (LD-1 registrations + LD-2 quarterly reports)
  - /contributions/   (LD-203 political contribution reports)
  - /lobbyists/       (registered lobbyist directory)

Auth: Token-based (LDA_API_KEY in .env)
Rate limit: 120 req/min (authenticated), 25 results/page
Pagination strategy: by filing_year (required for pagination beyond page 1)

REWRITTEN 2026-09-06, two problems, both measured:

  it held a whole year in memory
      paginate_all() built one list of every filing in a year before returning,
      and only then did the upload fire. A year is tens of thousands of filings
      of deeply nested JSON. A 2026-09-06 run was killed after 90 minutes with
      nothing landed. Pages now stream: each one is flattened and appended to a
      buffer, and the buffer uploads whenever it passes FLUSH_ROWS. Peak memory
      is one flush, not one year.

  it threw the revolving door away
      Each lobbyist inside lobbying_activities[].lobbyists[] carries
      covered_position -- free text naming the government job that person left,
      e.g. "Chief of Staff, Rep. Donald McEachin" or "Professional Staff, Senate
      Appropriations Committee". The old flatten kept first and last name and
      dropped the rest. Measured on 253 lobbyist rows from 2024: 53.4% carry a
      covered position. That field is the only real revolving-door source in
      reach, and it now lands in FED_SENATE_LDA_LOBBYIST_POSITIONS, one row per
      filing per lobbyist.

      GOVERNANCE__FED_REVOLVINGDOOR_PROJECT is NOT that source and never was.
      Its 406 rows are government JOB SLOTS and the industry sectors each one
      touches. There is no person in it, which is why PERSON_NAME reads 'nan'
      on 405 of 406 rows.

    python scripts/senate_lda_load.py              # preview
    python scripts/senate_lda_load.py --run        # load all years
    python scripts/senate_lda_load.py --run --start-year 2020  # recent only
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
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

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_URL = "https://lda.senate.gov/api/v1"
API_KEY = os.environ.get("LDA_API_KEY", "").strip()
USER_AGENT = "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"

HEADERS = {"User-Agent": USER_AGENT}
if API_KEY:
    HEADERS["Authorization"] = f"Token {API_KEY}"

# Rate limiting: 120/min with key = 2/sec. Stay conservative.
REQUEST_DELAY = 0.55  # seconds between requests

CHECKPOINT_FILE = _REPO / "logs" / "senate_lda_checkpoint.json"
FIRST_YEAR = 1999
CURRENT_YEAR = 2026

# Table names
TBL_FILINGS = "FED_SENATE_LDA_FILINGS"
TBL_CONTRIBUTIONS = "FED_SENATE_LDA_CONTRIBUTIONS"
TBL_LOBBYISTS = "FED_SENATE_LDA_LOBBYISTS"
# One row per filing per lobbyist, carrying covered_position. This is the
# revolving door: the government job that person left before lobbying.
TBL_POSITIONS = "FED_SENATE_LDA_LOBBYIST_POSITIONS"

# Upload whenever the buffer passes this. Small enough that a year never sits
# in memory, big enough that write_pandas is not called once per page.
FLUSH_ROWS = 20_000


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------
def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {}


def save_checkpoint(cp: dict):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(json.dumps(cp, indent=2))


def seed_checkpoint_from_warehouse(cp: dict, conn) -> dict:
    """Trust the table, not the file.

    The checkpoint lives in logs/, which is gitignored and was EMPTY on
    2026-09-06 while landing already held 1999-2010 and 2020-2021, about
    746,000 filings. upload_df appends, so a fresh run would have silently
    doubled every one of those years. Any year already in the table is marked
    done before the loop starts.

    Lobbyist seats are tracked separately, because the years loaded before
    2026-09-06 were written by the old flatten and carry no covered_position.
    A year can therefore be done for filings and not done for seats."""
    cur = conn.cursor()
    for table, prefix, col in ((TBL_FILINGS, "filings", "FILING_YEAR"),
                               (TBL_CONTRIBUTIONS, "contributions", "FILING_YEAR"),
                               (TBL_POSITIONS, "positions", "FILING_YEAR")):
        try:
            rows = cur.execute(
                f'select "{col}", count(*) from {bulk.LANDING_FQS}."{table}" '
                f'group by 1').fetchall()
        except Exception:
            continue  # table does not exist yet, nothing to seed
        for year, n in rows:
            if year is None:
                continue
            try:
                key = f"{prefix}_{int(year)}"
            except (TypeError, ValueError):
                continue
            if key not in cp:
                cp[key] = int(n)
    cur.close()
    return cp


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
def api_get(endpoint: str, params: dict | None = None) -> dict:
    """GET with rate limiting; retries 429 AND transient network drops.
    (2026-08-22: the first full-crawl attempt died on an uncaught
    RemoteDisconnected mid-year — a multi-hour crawl must survive those.)"""
    url = f"{BASE_URL}/{endpoint}"
    for attempt in range(8):
        time.sleep(REQUEST_DELAY)
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=60)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as exc:
            wait = min(300, 15 * (attempt + 1))
            print(f"    network error ({str(exc)[:60]}), retry in {wait}s...")
            time.sleep(wait)
            continue
        if r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 60))
            print(f"    429 throttled, waiting {retry_after}s...")
            time.sleep(retry_after + 1)
            continue
        if r.status_code >= 500:
            wait = min(300, 15 * (attempt + 1))
            print(f"    HTTP {r.status_code}, retry in {wait}s...")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"Failed after 8 retries: {url}")


def paginate_pages(endpoint: str, year: int, year_param: str = "filing_year"):
    """Yield one page of results at a time, never the whole year at once.

    This is the fix for the 90-minute kill with nothing landed. The caller
    flattens and flushes as pages arrive, so peak memory is one flush buffer
    rather than a year of nested JSON."""
    # page_size 250 requires the LDA_API_KEY (anonymous cap is 25). Key verified
    # live 2026-08-22; 250 cuts the full crawl from ~12h to ~2-4h.
    params = {year_param: year, "page_size": 250 if API_KEY else 25, "page": 1}
    seen = 0
    while True:
        data = api_get(endpoint, params)
        batch = data.get("results", [])
        seen += len(batch)
        yield batch
        if not data.get("next"):
            break
        params["page"] += 1
        if params["page"] % 20 == 0:
            print(f"      page {params['page']}, {seen:,} records so far...", flush=True)


def paginate_all(endpoint: str, year: int, year_param: str = "filing_year") -> list[dict]:
    """Whole-year fetch, kept for callers that genuinely need it. Prefer
    paginate_pages: this one is what ran the loader out of memory."""
    out = []
    for batch in paginate_pages(endpoint, year, year_param):
        out.extend(batch)
    return out


# ---------------------------------------------------------------------------
# Flatten filings (nested JSON -> flat rows)
# ---------------------------------------------------------------------------
def flatten_filing(f: dict) -> dict:
    """Extract key flat fields from a filing JSON object."""
    reg = f.get("registrant") or {}
    client = f.get("client") or {}

    # Flatten lobbying activities into pipe-delimited strings
    activities = f.get("lobbying_activities") or []
    issues = "|".join(set(
        a.get("general_issue_code_display", "") for a in activities if a.get("general_issue_code_display")
    ))
    govt_entities = "|".join(set(
        e.get("name", "") for a in activities for e in (a.get("government_entities") or [])
    ))
    lobbyist_names = "|".join(set(
        f"{l.get('first_name', '')} {l.get('last_name', '')}".strip()
        for a in activities for l in (a.get("lobbyists") or [])
    ))
    specific_issues = " || ".join(
        a.get("description", "") for a in activities if a.get("description")
    )

    return {
        "FILING_UUID": f.get("filing_uuid"),
        "FILING_TYPE": f.get("filing_type"),
        "FILING_TYPE_DISPLAY": f.get("filing_type_display"),
        "FILING_YEAR": f.get("filing_year"),
        "FILING_PERIOD": f.get("filing_period"),
        "FILING_PERIOD_DISPLAY": f.get("filing_period_display"),
        "DT_POSTED": f.get("dt_posted"),
        "INCOME": f.get("income"),
        "EXPENSES": f.get("expenses"),
        "REGISTRANT_ID": reg.get("id"),
        "REGISTRANT_NAME": reg.get("name"),
        "REGISTRANT_DESCRIPTION": reg.get("description"),
        "REGISTRANT_CITY": reg.get("city"),
        "REGISTRANT_STATE": reg.get("state"),
        "REGISTRANT_COUNTRY": reg.get("country"),
        "CLIENT_ID": (client.get("id") or client.get("client_id")),
        "CLIENT_NAME": client.get("name"),
        "CLIENT_DESCRIPTION": client.get("general_description"),
        "CLIENT_STATE": client.get("state"),
        "CLIENT_COUNTRY": client.get("country"),
        "LOBBYING_ISSUES": issues[:4000] if issues else None,
        "GOVERNMENT_ENTITIES": govt_entities[:4000] if govt_entities else None,
        "LOBBYIST_NAMES": lobbyist_names[:4000] if lobbyist_names else None,
        "SPECIFIC_ISSUES": specific_issues[:8000] if specific_issues else None,
        "TERMINATION_DATE": f.get("termination_date"),
        "FOREIGN_ENTITY_LISTED": f.get("foreign_entity_listed_indicator") if "foreign_entity_listed_indicator" in (f or {}) else (
            bool(f.get("foreign_entities")) if f.get("foreign_entities") else False
        ),
    }


def flatten_lobbyists(f: dict) -> list[dict]:
    """One row per (filing, lobbyist). Keeps covered_position, which the old
    flatten dropped -- see the module docstring for what that field is."""
    reg = f.get("registrant") or {}
    client = f.get("client") or {}
    rows = []
    seen = set()
    for a in (f.get("lobbying_activities") or []):
        issue = a.get("general_issue_code_display")
        for l in (a.get("lobbyists") or []):
            person = l.get("lobbyist") or l
            first = (person.get("first_name") or "").strip()
            last = (person.get("last_name") or "").strip()
            covered = l.get("covered_position")
            # A lobbyist repeats across activities in one filing. Keep one row
            # per person per issue; the issue is what varies and is worth having.
            key = (person.get("id"), first, last, issue)
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "FILING_UUID": f.get("filing_uuid"),
                "FILING_YEAR": f.get("filing_year"),
                "FILING_TYPE": f.get("filing_type"),
                "DT_POSTED": f.get("dt_posted"),
                "REGISTRANT_ID": reg.get("id"),
                "REGISTRANT_NAME": reg.get("name"),
                "CLIENT_ID": (client.get("id") or client.get("client_id")),
                "CLIENT_NAME": client.get("name"),
                "LOBBYIST_ID": person.get("id"),
                "LOBBYIST_FIRST_NAME": first or None,
                "LOBBYIST_MIDDLE_NAME": person.get("middle_name"),
                "LOBBYIST_LAST_NAME": last or None,
                "LOBBYIST_SUFFIX": person.get("suffix_display") or person.get("suffix"),
                "GENERAL_ISSUE": issue,
                # Free text, and long. It names the member and the committee:
                # "Chief of Staff, Rep. Donald McEachin" / "Professional Staff,
                # Senate Appropriations Cmte". Multiple jobs arrive separated by
                # ';' or '/'. Parse downstream, land it whole.
                "COVERED_POSITION": (covered[:4000] if covered else None),
                "HAS_COVERED_POSITION": str(bool(covered)),
                "IS_NEW_LOBBYIST": str(l.get("new")) if l.get("new") is not None else None,
            })
    return rows


def flatten_contribution(c: dict) -> list[dict]:
    """Flatten a contribution report into one row per contribution item."""
    reg = c.get("registrant") or {}
    lob = c.get("lobbyist") or {}
    items = c.get("contribution_items") or []

    base = {
        "FILING_UUID": c.get("filing_uuid"),
        "FILING_TYPE": c.get("filing_type"),
        "FILING_YEAR": c.get("filing_year"),
        "FILING_PERIOD": c.get("filing_period"),
        "DT_POSTED": c.get("dt_posted"),
        "FILER_TYPE": c.get("filer_type"),
        "REGISTRANT_ID": reg.get("id"),
        "REGISTRANT_NAME": reg.get("name"),
        "LOBBYIST_FIRST_NAME": lob.get("first_name"),
        "LOBBYIST_LAST_NAME": lob.get("last_name"),
        "LOBBYIST_ID": lob.get("id"),
        "NO_CONTRIBUTIONS": c.get("no_contributions"),
    }

    if not items or c.get("no_contributions"):
        base["CONTRIBUTION_TYPE"] = None
        base["CONTRIBUTOR_NAME"] = None
        base["PAYEE_NAME"] = None
        base["HONOREE_NAME"] = None
        base["AMOUNT"] = None
        base["CONTRIBUTION_DATE"] = None
        return [base]

    rows = []
    for item in items:
        row = dict(base)
        row["CONTRIBUTION_TYPE"] = item.get("contribution_type")
        row["CONTRIBUTOR_NAME"] = item.get("contributor_name")
        row["PAYEE_NAME"] = item.get("payee_name")
        row["HONOREE_NAME"] = item.get("honoree_name")
        row["AMOUNT"] = item.get("amount")
        row["CONTRIBUTION_DATE"] = item.get("date")
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Upload to Snowflake
# ---------------------------------------------------------------------------
# FIXED 2026-08-26: the connection used to be opened ONCE at the top of main()
# and never re-established. A single year's fetch can take hours under the
# API's 429 throttling, so by the time the upload fired, the Snowflake auth
# token had expired ("390114: Authentication token has expired") and the whole
# run died -- twice on 2026-08-26 alone, each time losing a finished multi-hour
# download. Every upload now goes through get_conn(), which health-checks the
# session and reconnects if the server has closed it, and retries once on an
# auth-expiry raised mid-write.
_conn = None


def get_conn():
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


def upload_df(df: pd.DataFrame, table: str, run_id: str):
    """Upload a DataFrame to Snowflake landing using write_pandas.

    Retries once on an expired-session error: the hours-long fetch that precedes
    an upload routinely outlives the auth token."""
    try:
        return _upload_df_inner(get_conn(), df, table, run_id)
    except Exception as e:
        if "390114" not in str(e) and "expired" not in str(e).lower():
            raise
        print("    (auth expired mid-upload -- reconnecting and retrying once)",
              flush=True)
        _reset_conn()
        return _upload_df_inner(get_conn(), df, table, run_id)


def _upload_df_inner(conn, df: pd.DataFrame, table: str, run_id: str):
    from snowflake.connector.pandas_tools import write_pandas

    df["_INGESTED_AT"] = pd.Timestamp.utcnow()
    df["_SOURCE_RUN_ID"] = run_id

    # Ensure table exists
    cur = conn.cursor()
    cols_sql = ", ".join(
        f'"{c}" VARCHAR' for c in df.columns
    )
    cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{table}" ({cols_sql})')
    cur.close()

    # Convert all to string for safe VARCHAR load
    df = df.astype(str).replace({"None": None, "nan": None, "NaT": None})

    write_pandas(conn, df, table, database=bulk.LANDING_DB,
                 schema=bulk.LANDING_SCHEMA, quote_identifiers=False,
                 auto_create_table=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--start-year", type=int, default=FIRST_YEAR)
    ap.add_argument("--end-year", type=int, default=CURRENT_YEAR)
    args = ap.parse_args()

    if not API_KEY:
        # The API answers without a key, just far slower: roughly 15 requests a
        # minute against 120 with one. Verified live 2026-09-06, filing_year
        # 2015 returned count=73,908 unauthenticated. So run anyway and say what
        # it costs, rather than refusing to start.
        global REQUEST_DELAY
        REQUEST_DELAY = max(REQUEST_DELAY, 4.2)
        print("No LDA_API_KEY. Running unauthenticated at about 15 requests a "
              "minute, roughly eight times slower.")
        print("A key at https://lda.senate.gov/api/register/ takes two minutes "
              "and makes this eight times faster.")
    else:
        print(f"LDA API key: ...{API_KEY[-8:]}")
    print(f"Years: {args.start_year} - {args.end_year}")

    if not args.run:
        # Preview: just show counts for one year
        test = api_get("filings/", {"filing_year": args.end_year, "page_size": 1})
        print(f"  Filings in {args.end_year}: {test.get('count', '?')}")
        test2 = api_get("contributions/", {"filing_year": args.end_year, "page_size": 1})
        print(f"  Contributions in {args.end_year}: {test2.get('count', '?')}")
        print("\n(preview only -- add --run to load)")
        return

    cp = load_checkpoint()
    run_id = str(uuid.uuid4())
    conn = get_conn()  # fail fast on credentials before the first multi-hour fetch
    before = len(cp)
    cp = seed_checkpoint_from_warehouse(cp, conn)
    if len(cp) > before:
        save_checkpoint(cp)
        print(f"  seeded {len(cp) - before} year(s) from what landing already holds")

    years = list(range(args.start_year, args.end_year + 1))

    # --- FILINGS ---
    print(f"\n{'='*60}")
    print(f"FILINGS (LD-1 / LD-2) — {len(years)} years")
    print(f"{'='*60}")
    for year in years:
        cp_key = f"filings_{year}"
        pos_key = f"positions_{year}"
        want_filings = cp_key not in cp
        want_positions = pos_key not in cp
        if not want_filings and not want_positions:
            print(f"  [{year}] already loaded ({cp[cp_key]} filings) -- skip")
            continue
        if not want_filings:
            print(f"  [{year}] filings already landed; fetching lobbyist seats only",
                  flush=True)

        print(f"  [{year}] streaming...", flush=True)
        # Two buffers, flushed independently. Nothing accumulates a whole year.
        fil_buf: list[dict] = []
        pos_buf: list[dict] = []
        n_fil = n_pos = n_covered = 0

        def flush(force: bool = False):
            nonlocal fil_buf, pos_buf
            if not want_filings:
                fil_buf = []
            if not want_positions:
                pos_buf = []
            if fil_buf and (force or len(fil_buf) >= FLUSH_ROWS):
                upload_df(pd.DataFrame(fil_buf), TBL_FILINGS, run_id)
                print(f"      flushed {len(fil_buf):,} filings", flush=True)
                fil_buf = []
            if pos_buf and (force or len(pos_buf) >= FLUSH_ROWS):
                upload_df(pd.DataFrame(pos_buf), TBL_POSITIONS, run_id)
                print(f"      flushed {len(pos_buf):,} lobbyist seats", flush=True)
                pos_buf = []

        for page in paginate_pages("filings/", year):
            for f in page:
                fil_buf.append(flatten_filing(f))
                seats = flatten_lobbyists(f)
                pos_buf.extend(seats)
                n_fil += 1
                n_pos += len(seats)
                n_covered += sum(1 for r in seats if r["COVERED_POSITION"])
            flush()
        flush(force=True)

        if not n_fil:
            print(f"  [{year}] 0 filings")
            cp[cp_key] = 0
            save_checkpoint(cp)
            continue

        share = (n_covered / n_pos * 100) if n_pos else 0.0
        print(f"  [{year}] {n_fil:,} filings, {n_pos:,} lobbyist seats, "
              f"{n_covered:,} with a covered position, {share:.1f}%", flush=True)
        if want_filings:
            cp[cp_key] = n_fil
        if want_positions:
            cp[pos_key] = n_pos
        save_checkpoint(cp)

    # --- CONTRIBUTIONS ---
    print(f"\n{'='*60}")
    print(f"CONTRIBUTIONS (LD-203) — {len(years)} years")
    print(f"{'='*60}")
    # LD-203 only exists from 2008 onward
    contrib_years = [y for y in years if y >= 2008]
    for year in contrib_years:
        cp_key = f"contributions_{year}"
        if cp_key in cp:
            print(f"  [{year}] already loaded ({cp[cp_key]} rows) -- skip")
            continue

        print(f"  [{year}] streaming...", flush=True)
        buf: list[dict] = []
        n_items = 0
        for page in paginate_pages("contributions/", year):
            for c in page:
                buf.extend(flatten_contribution(c))
            if len(buf) >= FLUSH_ROWS:
                upload_df(pd.DataFrame(buf), TBL_CONTRIBUTIONS, run_id)
                n_items += len(buf)
                print(f"      flushed {len(buf):,} contribution items", flush=True)
                buf = []
        if buf:
            upload_df(pd.DataFrame(buf), TBL_CONTRIBUTIONS, run_id)
            n_items += len(buf)

        if not n_items:
            print(f"  [{year}] 0 contributions")
            cp[cp_key] = 0
            save_checkpoint(cp)
            continue

        print(f"  [{year}] {n_items:,} contribution items", flush=True)
        cp[cp_key] = n_items
        save_checkpoint(cp)

    # --- LOBBYIST SEATS ---
    # The standalone /lobbyists/ directory is deliberately NOT loaded. It is a
    # name list with no covered_position on it, so it cannot answer the
    # revolving-door question. The seats that CAN answer it were written
    # alongside the filings above, one row per filing per lobbyist, because
    # covered_position only exists inside a filing's activities.
    print(f"\n{'='*60}")
    print("LOBBYIST SEATS")
    print(f"{'='*60}")
    print(f"  written alongside filings -> {TBL_POSITIONS}")

    # --- Summary ---
    total_filings = sum(v for k, v in cp.items() if k.startswith("filings_") and isinstance(v, int))
    total_contribs = sum(v for k, v in cp.items() if k.startswith("contributions_") and isinstance(v, int))
    total_positions = sum(v for k, v in cp.items() if k.startswith("positions_") and isinstance(v, int))
    print(f"\n{'='*60}")
    print(f"COMPLETE: {total_filings:,} filings, {total_positions:,} lobbyist seats, "
          f"{total_contribs:,} contribution items")
    print(f"{'='*60}")

    # Quality gate
    # Gate verdict must reach the exit code (audit 2026-08-05 finding: same
    # discarded-return bug class fixed in fda_faers_load.py / sec_13f_load.py
    # -- this loader still had it as of 2026-08-06).
    gate_failed = []
    if total_filings > 0:
        passed, report = bulk.run_quality_gate(
            get_conn(), "fed_senate_lda_filings", TBL_FILINGS, run_id,
            row_count=total_filings, source_url=BASE_URL)
        if not passed:
            print(f"QUALITY GATE FAILED {TBL_FILINGS}: {report}")
            gate_failed.append(TBL_FILINGS)
    if total_contribs > 0:
        passed, report = bulk.run_quality_gate(
            get_conn(), "fed_senate_lda_contributions", TBL_CONTRIBUTIONS, run_id,
            row_count=total_contribs, source_url=BASE_URL)
        if not passed:
            print(f"QUALITY GATE FAILED {TBL_CONTRIBUTIONS}: {report}")
            gate_failed.append(TBL_CONTRIBUTIONS)
    if total_positions > 0:
        passed, report = bulk.run_quality_gate(
            get_conn(), "fed_senate_lda_lobbyist_positions", TBL_POSITIONS, run_id,
            row_count=total_positions, source_url=BASE_URL)
        if not passed:
            print(f"QUALITY GATE FAILED {TBL_POSITIONS}: {report}")
            gate_failed.append(TBL_POSITIONS)

    _reset_conn()
    if gate_failed:
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
