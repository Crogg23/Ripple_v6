#!/usr/bin/env python3
"""Backfill GovInfo BILLSTATUS for the congresses the warehouse never had.

FED_GOVINFO_BILLSTATUS held congresses 118 and 119 only, 36,465 bills, and
FED_GOVINFO_BILL_COSPONSORS the same two, 367,742 rows. Everything before 2023
was missing, which is what blocks docket question 91. No loader for this existed
anywhere in the repo -- the tables were written by something that did not survive
into git -- so this is written fresh rather than recovered from the junk drawer,
which CLAUDE.md forbids building from anyway.

SOURCE: GovInfo publishes one zip per congress per bill type at
https://www.govinfo.gov/bulkdata/BILLSTATUS/<congress>/<type>/BILLSTATUS-<congress>-<type>.zip
No API key. Verified live 2026-09-06: 113/hr is 24.7 MB, 113/hres is 2.4 MB of
784 XML files.

THE XML TAG NAMES ARE NOT THE COLUMN NAMES. The bill's number is <number> and
its type is <type>, not <billNumber> and <billType>, which is what a first guess
reaches for and gets None from. Mapped by walking a real file, 2026-09-06.

META COLUMN NAMES: these two tables came from land(), so they carry
_INGESTED_AT with the leading underscore. ingest._sf_col strips that, and running
it over the meta columns kills the append with "invalid identifier
'INGESTED_AT'". Landing has both conventions live -- the FEC and IRS527 tables
have no underscore -- so a loader has to match its own target table.

IT APPENDS, and REFUSES a congress that is already in the table. The existing
118 and 119 rows were landed by the lost loader; re-fetching them here would
double them, silently, exactly the way the LDA loader nearly doubled 746,000
filings today because its checkpoint file was empty while the table was not.

MEMORY: one zip at a time, flushed to the warehouse per zip. A congress of HR
bills is thousands of XML documents and there is no reason to hold five
congresses of them at once.
"""
from __future__ import annotations

import argparse
import io
import sys
import uuid
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_LIB / ".env", override=True)

import ingest  # noqa: E402
import snow  # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

BASE = "https://www.govinfo.gov/bulkdata/BILLSTATUS"
UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

TBL_BILLS = "FED_GOVINFO_BILLSTATUS"
TBL_COSPON = "FED_GOVINFO_BILL_COSPONSORS"
SID_BILLS = "fed_govinfo_billstatus"
SID_COSPON = "fed_govinfo_bill_cosponsors"

CONGRESSES = [113, 114, 115, 116, 117]
TYPES = ["hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", "sres"]


def _text(node, path: str) -> str | None:
    e = node.find(path)
    return (e.text or "").strip() if e is not None and e.text else None


def parse_bill(x: bytes) -> tuple[dict, list[dict]]:
    bill = ET.fromstring(x).find("bill")
    if bill is None:
        return {}, []

    congress = _text(bill, "congress")
    btype = _text(bill, "type")
    bnum = _text(bill, "number")

    actions = bill.find("actions")
    action_items = actions.findall("item") if actions is not None else []
    # Distinct action types, pipe-joined, matching what the live table carries.
    kinds = []
    for a in action_items:
        t = _text(a, "type")
        if t and t not in kinds:
            kinds.append(t)

    cospon_el = bill.find("cosponsors")
    cospon_items = cospon_el.findall("item") if cospon_el is not None else []

    law = bill.find("laws/item")
    sponsor = bill.find("sponsors/item")

    row = {
        "CONGRESS": congress,
        "BILL_TYPE": btype,
        "BILL_NUMBER": bnum,
        "INTRODUCED_DATE": _text(bill, "introducedDate"),
        "TITLE": _text(bill, "title"),
        "SPONSOR_BIOGUIDE": _text(sponsor, "bioguideId") if sponsor is not None else None,
        "SPONSOR_NAME": _text(sponsor, "fullName") if sponsor is not None else None,
        "LAW_TYPE": _text(law, "type") if law is not None else None,
        "LAW_NUMBER": _text(law, "number") if law is not None else None,
        "ACTION_TYPES": "|".join(kinds) if kinds else None,
        "N_ACTIONS": str(len(action_items)),
        "LATEST_ACTION_DATE": _text(bill, "latestAction/actionDate"),
        "LATEST_ACTION_TEXT": _text(bill, "latestAction/text"),
        "N_COSPONSORS": str(len(cospon_items)),
    }

    cos = []
    for c in cospon_items:
        cos.append({
            "CONGRESS": congress,
            "BILL_TYPE": btype,
            "BILL_NUMBER": bnum,
            "COSPONSOR_BIOGUIDE": _text(c, "bioguideId"),
            "COSPONSOR_NAME": _text(c, "fullName"),
            "COSPONSOR_PARTY": _text(c, "party"),
            "COSPONSOR_STATE": _text(c, "state"),
            # The XML says 'True'/'False'; the live table carries that text.
            "IS_ORIGINAL": _text(c, "isOriginalCosponsor"),
            "SPONSORSHIP_DATE": _text(c, "sponsorshipDate"),
            "SPONSORSHIP_WITHDRAWN_DATE": _text(c, "sponsorshipWithdrawnDate"),
        })
    return row, cos


def append(conn, rows: list[dict], table: str, run_id: str, started) -> int:
    if not rows:
        return 0
    out = ingest._stringify(pd.DataFrame(rows))
    # Reserved-word guard on the DATA columns only. Running it over the meta
    # columns strips their leading underscore and the append dies on "invalid
    # identifier 'INGESTED_AT'": these two tables were written by land(), which
    # keeps _INGESTED_AT, while the FEC and IRS527 tables carry the stripped
    # form. Both conventions are live in landing. Match the target table.
    out.columns = [ingest._sf_col(c) for c in out.columns]
    out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    out[ingest.META_SOURCE_RUN_ID] = run_id
    out[ingest.META_SRC_SHA256] = ""
    ok, _c, _r, _ = write_pandas(
        conn, out, table_name=table, database=settings.raw_database,
        schema=settings.raw_schema, auto_create_table=False,
        overwrite=False, quote_identifiers=False)
    if not ok:
        raise RuntimeError(f"write_pandas failed appending to {table}")
    return len(out)


def already_loaded(cur) -> set[str]:
    got = {r[0] for r in cur.execute(
        f'select distinct CONGRESS from {settings.raw_database}.'
        f'{settings.raw_schema}."{TBL_BILLS}"').fetchall() if r[0]}
    return got


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--congresses", default=",".join(str(c) for c in CONGRESSES))
    ap.add_argument("--types", default=",".join(TYPES))
    ap.add_argument("--dry-run", action="store_true",
                    help="parse and count, land nothing")
    ap.add_argument("--force", action="store_true",
                    help="load a congress even if the table already has it")
    args = ap.parse_args()

    want = [c.strip() for c in args.congresses.split(",") if c.strip()]
    types = [t.strip() for t in args.types.split(",") if t.strip()]

    print("=== GovInfo BILLSTATUS backfill ===", flush=True)
    conn = snow.connect()
    cur = conn.cursor()
    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    n_bills = n_cos = 0
    try:
        have = already_loaded(cur)
        print(f"  table already holds congresses: {sorted(have)}", flush=True)
        skip = [c for c in want if c in have and not args.force]
        if skip:
            print(f"  SKIPPING {skip}: already loaded. --force to reload.", flush=True)
        want = [c for c in want if c not in skip]
        if not want:
            print("  nothing to do")
            return 0

        for cong in want:
            for t in types:
                url = f"{BASE}/{cong}/{t}/BILLSTATUS-{cong}-{t}.zip"
                r = requests.get(url, headers=UA, timeout=900)
                if r.status_code == 404:
                    print(f"  {cong}/{t}: no file", flush=True)
                    continue
                r.raise_for_status()
                z = zipfile.ZipFile(io.BytesIO(r.content))
                bills, cos = [], []
                for nm in z.namelist():
                    if not nm.lower().endswith(".xml"):
                        continue
                    row, cc = parse_bill(z.read(nm))
                    if row:
                        bills.append(row)
                        cos.extend(cc)
                print(f"  {cong}/{t}: {len(bills):,} bills, {len(cos):,} cosponsorships, "
                      f"{len(r.content)/1e6:.1f} MB", flush=True)
                if args.dry_run:
                    n_bills += len(bills)
                    n_cos += len(cos)
                    continue
                n_bills += append(conn, bills, TBL_BILLS, run_id, started)
                n_cos += append(conn, cos, TBL_COSPON, run_id, started)

        print(f"\n  {n_bills:,} bills, {n_cos:,} cosponsorships", flush=True)
        if args.dry_run:
            print("DRY RUN: nothing landed", flush=True)
            return 0
        for sid, tbl, n in ((SID_BILLS, TBL_BILLS, n_bills), (SID_COSPON, TBL_COSPON, n_cos)):
            ingest._log_run(conn, sid, run_id, "success", n, 0, "", BASE, started,
                            ingest._utcnow(),
                            f"GovInfo BILLSTATUS backfill, congresses {','.join(want)}.")
        print(f"\nDONE -> {TBL_BILLS} and {TBL_COSPON}", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
