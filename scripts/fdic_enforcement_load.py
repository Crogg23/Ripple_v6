"""Load FDIC Enforcement Decisions and Orders, one row per order.

Docket 118. The old FED_FDIC_ENFORCEMENT table (14 rows) is the fdic.gov
navigation menu scraped as data. It is left alone. This lands a NEW table:

    LIBRARY_RAW.LANDING.FED_FDIC_ENFORCEMENT_ORDERS

WHERE THE DATA COMES FROM (found 2026-09-07)
    orders.fdic.gov is a Salesforce Experience Cloud site. A plain GET gets a JS
    shell. There is no CSV link, no REST API, and FDIC's BankFind API has no
    enforcement endpoint. But the search form talks to an Apex controller over
    the Aura endpoint, and that endpoint answers a plain POST with no browser,
    no cookie and no token:

        POST https://orders.fdic.gov/s/sfsites/aura
        apex://EDOSSearchFormController/ACTION$countResults     -> int
        apex://EDOSSearchFormController/ACTION$buildWrapperList -> list of orders

    Each order arrives as JSON with the docket number, dates, category, type,
    the PDF link, and two child lists: Order_Banks__r (bank name, city, state,
    CERT number) and Respondents__r (people or banks named, CMP amount, NMLS id).

    The site's own "Download All" button calls convertCSV and hands back the
    same 10,838 orders as a CSV, but with the child lists squashed into
    semicolon strings and the order title blank on 23 rows. The JSON is the
    cleaner of the two, so that is what lands.

    Measured 2026-09-07: countResults with no date filter = 10,838. Of those,
    23 carry no issued date at all (the site's own CSV shows the same 23 with a
    blank date); they land under the "undated" bucket. Dated orders run from
    1975 (one) and 1979 (one), then 1 in 1980 up through 2026. The 1980s are
    thin (14 in 1985, 129 in 1989) and 1990 is the first full year at 293. So
    "back to 1990" is met with fifteen thin years before it.

PAGING
    Salesforce SOQL OFFSET stops at 2,000. The busiest year (2010) is 902
    orders, so one page of 2,000 covers any year today. The loader still walks
    offsets inside a year and splits a year into months if the count ever
    passes the cap, so it does not silently lose rows the year that happens.

GRAIN
    One row per order (Salesforce Id). An order can name more than one bank;
    the first bank fills BANK_NAME / BANK_CITY / BANK_STATE / CERT_NUMBER and
    every bank is kept in BANKS_ALL. Respondents are joined with ' ; '. The
    whole order JSON is kept in RAW_JSON so nothing is lost by the flatten.

    python scripts/fdic_enforcement_load.py            # dry run: counts by year, first 20 rows
    python scripts/fdic_enforcement_load.py --run      # land everything, resumes by year
    python scripts/fdic_enforcement_load.py --run --start-year 2020
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import date
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
AURA_URL = "https://orders.fdic.gov/s/sfsites/aura"
SOURCE_URL = "https://orders.fdic.gov/s/searchform"
SOURCE_ID = "fed_fdic_enforcement_orders"
TABLE = "FED_FDIC_ENFORCEMENT_ORDERS"
USER_AGENT = "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"

# The Aura framework id and app version, read off the page shell. If Salesforce
# rolls the framework the POST answers with a "framework version mismatch"
# JSON; refresh_context() re-reads it from the shell and retries once.
FWUID = "WUdfaXlIZDNDQ0lZLWNFZDMtVGZ3d2tVMjdnTGFERUU2S3FfSVdrcU92bkExNC4xOTIuODM4ODYwOA"
APP_LOADED = "1712_xZHiuQoc1HHcvGz4vs6mGA"

# The status filter the search form itself sends. Copied verbatim so the loader
# sees exactly what a person sees on the site, nothing more.
CRIT_BASE = (
    "(Status__c = 'Published' OR (Status__c = 'Recall Requested' AND "
    "Public_Order_Action__c = 'Open for Recall') OR (Status__c = 'Archive Requested' "
    "AND Public_Order_Action__c = 'Archive') OR (Status__c IN ('Open for Termination', "
    "'Legal Review', 'Ready to Publish', 'Rejected to Legal Specialist') AND "
    "Public_Order_Action__c = 'Open for Termination'))"
)
# File_URL__c is NOT in this list on purpose. The controller adds it itself;
# naming it here returns ZERO rows with no error (tested 2026-09-07). So
# DOCUMENT_URL rides on controller behaviour, and the loader checks it landed.
FIELDS = ("Order_Title__c, Order_Issued_Date__c, Termination_Date__c, "
          "Termination_Comments__c, Docket_Number__c, Order_Category2__c, "
          "Order_Type__c, Public_Order_Action__c, Status__c")
RELATIONS = (", (SELECT Id, Order_and_Hearing_Number__c, Bank_Name__c, Bank_City__c, "
             "Bank_State__c, CERT_Number__c FROM Order_Banks__r ) , (SELECT Id, "
             "Order_and_Hearing_Number__c, Restitution_Amount__c, Restitution_Comment__c, "
             "Individual_Respondent_Name__c, CMP_Amount__c, Bank_Institution_Name__c, "
             "NMLS_ID__c FROM Respondents__r ) ")

PAGE = 500          # rows per POST
SOQL_OFFSET_CAP = 2000
REQUEST_DELAY = 0.5
FIRST_YEAR = 1975   # oldest dated order is 1975-, one each in 1975 and 1979
CURRENT_YEAR = date.today().year
CHECKPOINT_FILE = _REPO / "logs" / "fdic_enforcement_orders_checkpoint.json"


# ---------------------------------------------------------------------------
# Aura endpoint
# ---------------------------------------------------------------------------
def _context() -> dict:
    return {"mode": "PROD", "fwuid": FWUID, "app": "siteforce:communityApp",
            "loaded": {"APPLICATION@markup://siteforce:communityApp": APP_LOADED},
            "dn": [], "globals": {}, "uad": False}


def refresh_context() -> None:
    """Re-read fwuid and app version from the page shell."""
    global FWUID, APP_LOADED
    import re
    import urllib.parse
    html = requests.get(SOURCE_URL, headers={"User-Agent": USER_AGENT}, timeout=60).text
    m = re.search(r'sfsites/l/(%7B[^"]+%7D)/', html)
    if not m:
        raise RuntimeError("could not find the Aura context in the page shell")
    ctx = json.loads(urllib.parse.unquote(m.group(1)))
    FWUID = ctx["fwuid"]
    APP_LOADED = ctx["loaded"]["APPLICATION@markup://siteforce:communityApp"]
    print(f"  aura context refreshed: fwuid ...{FWUID[-8:]}")


def apex(action: str, params: dict):
    """One Apex action over the Aura endpoint. Retries network drops and 5xx,
    refreshes the framework id once on a version mismatch."""
    msg = {"actions": [{"id": "1;a",
                        "descriptor": f"apex://EDOSSearchFormController/ACTION${action}",
                        "callingDescriptor": "markup://c:EDOSSearchForm",
                        "params": params}]}
    refreshed = False
    for attempt in range(8):
        time.sleep(REQUEST_DELAY)
        try:
            r = requests.post(
                f"{AURA_URL}?r=1&other.EDOSSearchForm.{action}=1",
                data={"message": json.dumps(msg), "aura.context": json.dumps(_context()),
                      "aura.token": "null", "aura.pageURI": "/s/searchform"},
                headers={"User-Agent": USER_AGENT}, timeout=120)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            wait = min(300, 15 * (attempt + 1))
            print(f"    network error ({str(exc)[:60]}), retry in {wait}s...")
            time.sleep(wait)
            continue
        if r.status_code >= 500 or r.status_code == 429:
            wait = min(300, 15 * (attempt + 1))
            print(f"    HTTP {r.status_code}, retry in {wait}s...")
            time.sleep(wait)
            continue
        r.raise_for_status()
        body = r.json()
        if body.get("exceptionEvent") or not body.get("actions"):
            text = json.dumps(body)[:300]
            if "COOS" in text or "mismatch" in text.lower() or "fwuid" in text.lower():
                if not refreshed:
                    refresh_context()
                    refreshed = True
                    continue
            raise RuntimeError(f"aura error: {text}")
        a = body["actions"][0]
        if a["state"] != "SUCCESS":
            raise RuntimeError(f"apex {action} failed: {a.get('error')}")
        return a["returnValue"]
    raise RuntimeError(f"failed after 8 tries: {action}")


def criteria(d0: str, d1: str) -> str:
    return f"{CRIT_BASE} AND Order_Issued_Date__c <= {d1} AND Order_Issued_Date__c >= {d0} "


def count_orders(d0: str, d1: str) -> int:
    return int(apex("countResults", {"objectToQuery": "Order_and_Hearing__c",
                                     "searchCriteria": criteria(d0, d1)}))


def fetch_window(d0: str, d1: str):
    """Yield every order issued in [d0, d1], walking offsets."""
    offset = 0
    while True:
        rv = apex("buildWrapperList", {
            "fields": FIELDS, "objectToQuery": "Order_and_Hearing__c",
            "searchCriteria": criteria(d0, d1), "resultsPerPage": str(PAGE),
            "relationshipQueries": RELATIONS, "offsetToUse": offset})
        for w in rv:
            yield w
        if len(rv) < PAGE:
            return
        offset += PAGE
        if offset >= SOQL_OFFSET_CAP:
            raise RuntimeError(f"window {d0}..{d1} passes the SOQL offset cap; split it")


def month_windows(year: int):
    for m in range(1, 13):
        last = (date(year + (m == 12), (m % 12) + 1, 1) - pd.Timedelta(days=1)).day
        yield f"{year}-{m:02d}-01", f"{year}-{m:02d}-{last:02d}"


UNDATED = "undated"
CRIT_UNDATED = f"{CRIT_BASE} AND Order_Issued_Date__c = null "


def count_undated() -> int:
    return int(apex("countResults", {"objectToQuery": "Order_and_Hearing__c",
                                     "searchCriteria": CRIT_UNDATED}))


def fetch_undated():
    rv = apex("buildWrapperList", {
        "fields": FIELDS, "objectToQuery": "Order_and_Hearing__c",
        "searchCriteria": CRIT_UNDATED, "resultsPerPage": str(SOQL_OFFSET_CAP),
        "relationshipQueries": RELATIONS, "offsetToUse": 0})
    yield from rv


def fetch_year(year: int):
    d0, d1 = f"{year}-01-01", f"{year}-12-31"
    if count_orders(d0, d1) < SOQL_OFFSET_CAP:
        yield from fetch_window(d0, d1)
        return
    for m0, m1 in month_windows(year):
        yield from fetch_window(m0, m1)


# ---------------------------------------------------------------------------
# Flatten
# ---------------------------------------------------------------------------
def _s(v) -> str | None:
    if v is None:
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    s = str(v).strip()
    return s or None


def flatten(w: dict) -> dict:
    o = w.get("order") or {}
    banks = o.get("Order_Banks__r") or []
    resps = o.get("Respondents__r") or []
    first = banks[0] if banks else {}

    def bank_str(b):
        return "|".join(_s(b.get(k)) or "" for k in
                        ("Bank_Name__c", "Bank_City__c", "Bank_State__c", "CERT_Number__c"))

    def resp_name(r):
        return _s(r.get("Individual_Respondent_Name__c")) or _s(r.get("Bank_Institution_Name__c"))

    def money(key):
        vals = [r.get(key) for r in resps if isinstance(r.get(key), (int, float))]
        return _s(sum(vals)) if vals else None

    return {
        "ORDER_ID": _s(o.get("Id")),
        "ORDER_ISSUED_DATE": _s(o.get("Order_Issued_Date__c")),
        "ORDER_TITLE": _s(o.get("Order_Title__c")),
        "DOCKET_NUMBER": _s(o.get("Docket_Number__c")),
        "ORDER_CATEGORY": _s(o.get("Order_Category2__c")),
        "ORDER_TYPE": _s(o.get("Order_Type__c")),
        "BANK_NAME": _s(first.get("Bank_Name__c")),
        "BANK_CITY": _s(first.get("Bank_City__c")),
        "BANK_STATE": _s(first.get("Bank_State__c")),
        "CERT_NUMBER": _s(first.get("CERT_Number__c")),
        "BANK_COUNT": str(len(banks)),
        "BANKS_ALL": " ; ".join(bank_str(b) for b in banks) or None,
        "RESPONDENTS": " ; ".join(n for n in (resp_name(r) for r in resps) if n) or None,
        "RESPONDENT_COUNT": str(len(resps)),
        "CMP_AMOUNT_TOTAL": money("CMP_Amount__c"),
        "RESTITUTION_AMOUNT_TOTAL": money("Restitution_Amount__c"),
        "NMLS_IDS": " ; ".join(n for n in (_s(r.get("NMLS_ID__c")) for r in resps) if n) or None,
        "TERMINATION_DATE": _s(o.get("Termination_Date__c")),
        "TERMINATION_COMMENTS": _s(o.get("Termination_Comments__c")),
        "PUBLIC_ORDER_ACTION": _s(o.get("Public_Order_Action__c")),
        "STATUS": _s(o.get("Status__c")),
        "DOCUMENT_URL": _s(o.get("File_URL__c")),
        "RAW_JSON": json.dumps(o, separators=(",", ":"))[:64000],
    }


# ---------------------------------------------------------------------------
# Checkpoint + upload (same shape as senate_lda_load.py)
# ---------------------------------------------------------------------------
def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {}


def save_checkpoint(cp: dict):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(json.dumps(cp, indent=2))


def seed_checkpoint_from_warehouse(cp: dict, conn) -> dict:
    """Trust the table, not the file: any year already landed is marked done,
    because upload appends and a lost checkpoint would double it."""
    cur = conn.cursor()
    try:
        rows = cur.execute(
            f'select coalesce(left("ORDER_ISSUED_DATE", 4), ''{UNDATED}''), count(*) '
            f'from {bulk.LANDING_FQS}."{TABLE}" group by 1').fetchall()
    except Exception:
        return cp
    finally:
        cur.close()
    for year, n in rows:
        if year == UNDATED:
            cp.setdefault(f"year_{UNDATED}", int(n))
            continue
        try:
            key = f"year_{int(year)}"
        except (TypeError, ValueError):
            continue
        cp.setdefault(key, int(n))
    return cp


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
    _conn = snow.connect()
    return _conn


def upload_df(df: pd.DataFrame, run_id: str):
    from snowflake.connector.pandas_tools import write_pandas
    conn = get_conn()
    df = df.copy()
    df["INGESTED_AT"] = pd.Timestamp.utcnow().isoformat()
    df["_SOURCE_RUN_ID"] = run_id
    cols_sql = ", ".join(f'"{c}" VARCHAR' for c in df.columns)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{TABLE}" ({cols_sql})')
    cur.close()
    df = df.astype(object).where(df.notna(), None)
    write_pandas(conn, df, TABLE, database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                 quote_identifiers=False, auto_create_table=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land it; without this, dry run")
    ap.add_argument("--start-year", type=int, default=FIRST_YEAR)
    ap.add_argument("--end-year", type=int, default=CURRENT_YEAR)
    args = ap.parse_args()
    years = list(range(args.start_year, args.end_year + 1))

    total_site = int(apex("countResults", {"objectToQuery": "Order_and_Hearing__c",
                                           "searchCriteria": CRIT_BASE}))
    print(f"orders.fdic.gov says {total_site:,} orders on the site (no date filter)")
    counts = {y: count_orders(f"{y}-01-01", f"{y}-12-31") for y in years}
    n_undated = count_undated()
    first_year = next((y for y in years if counts[y]), None)
    print("orders by year: " + ", ".join(f"{y}:{n}" for y, n in counts.items() if n))
    print(f"  span {first_year}-{max(y for y in years if counts[y])}, "
          f"dated {sum(counts.values()):,}, undated {n_undated}, "
          f"total {sum(counts.values()) + n_undated:,}")

    if not args.run:
        print(f"\nfirst 20 rows, oldest first from {first_year}:")
        rows = []
        for y in years:
            if not counts[y]:
                continue
            for w in fetch_year(y):
                rows.append(flatten(w))
                if len(rows) >= 20:
                    break
            if len(rows) >= 20:
                break
        df = pd.DataFrame(rows).drop(columns=["RAW_JSON"])
        with pd.option_context("display.max_columns", None, "display.width", 250,
                               "display.max_colwidth", 40):
            print(df.to_string(index=False))
        print(f"\n(dry run -- {sum(counts.values()) + n_undated:,} rows would land; add --run)")
        return

    cp = load_checkpoint()
    run_id = str(uuid.uuid4())
    conn = get_conn()
    cp = seed_checkpoint_from_warehouse(cp, conn)
    save_checkpoint(cp)

    landed = 0
    for y in years:
        key = f"year_{y}"
        if not counts[y]:
            continue
        if key in cp:
            print(f"  [{y}] already landed ({cp[key]}) -- skip")
            continue
        rows = [flatten(w) for w in fetch_year(y)]
        if len(rows) != counts[y]:
            print(f"  [{y}] WARNING fetched {len(rows)} vs count {counts[y]}")
        if rows and not any(r["DOCUMENT_URL"] for r in rows):
            raise RuntimeError(f"[{y}] no DOCUMENT_URL on any row: the controller "
                               "stopped returning File_URL__c; fix before landing")
        upload_df(pd.DataFrame(rows), run_id)
        cp[key] = len(rows)
        save_checkpoint(cp)
        landed += len(rows)
        print(f"  [{y}] {len(rows):,} orders landed", flush=True)

    key = f"year_{UNDATED}"
    if n_undated and key not in cp:
        rows = [flatten(w) for w in fetch_undated()]
        if len(rows) != n_undated:
            print(f"  [{UNDATED}] WARNING fetched {len(rows)} vs count {n_undated}")
        upload_df(pd.DataFrame(rows), run_id)
        cp[key] = len(rows)
        save_checkpoint(cp)
        landed += len(rows)
        print(f"  [{UNDATED}] {len(rows):,} orders with no issued date landed", flush=True)
    elif key in cp:
        print(f"  [{UNDATED}] already landed ({cp[key]}) -- skip")

    total = sum(v for k, v in cp.items() if k.startswith("year_"))
    print(f"\nCOMPLETE: {landed:,} landed this run, {total:,} in the table by checkpoint")
    passed, report = bulk.run_quality_gate(
        get_conn(), SOURCE_ID, TABLE, run_id, row_count=total, source_url=SOURCE_URL)
    if not passed:
        print(f"QUALITY GATE FAILED {TABLE}: {report}")
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
