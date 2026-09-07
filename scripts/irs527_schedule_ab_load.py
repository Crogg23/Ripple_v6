#!/usr/bin/env python3
"""Land IRS 527 Schedule A and Schedule B, the itemized money the first pass skipped.

scripts/irs527_load.py lands record types 1 / D / R / E / 2 -- the organization
registry, its officers, its related entities and its report headers. Those say
WHICH political funds exist. They do not say who paid in or who got paid, which
is what docket question 88 asks. That is Schedule A and Schedule B, and the first
pass deferred them as "17.9M rows, disproportionate for this pass".

They share one 2.9 GB pipe-delimited file with everything else, so this streams
the zip and lands in chunks. Nothing here holds the file in memory.

THE LAYOUT WAS MEASURED, NOT READ OFF A DOC. The IRS's PolOrgsFileLayout is a
legacy binary .doc that this environment cannot render, and the first loader says
so plainly. So the field meanings below come from counting fields and reading
values on 1.1M A rows and 400k B rows, 2026-09-06:

  A and B are BOTH 18 fields wide. A full pass over the file counted 8 ragged
  A rows and 17 ragged B rows out of 17,893,129 -- 0.00014%. They are counted
  and dropped, never padded: padding a short row slides money into the wrong
  column, which is the whole reason the FEC parser hard-rejects instead.

  positions 0-14 mean the same thing in both, allowing for who the person is:
      0 record type   1 form id   2 schedule id   3 org name   4 EIN
      5 name   6 addr1   7 addr2   8 city   9 state   10 zip   11 zip ext
      12 employer   13 amount   14 occupation

  THEN THEY DIVERGE, which is the trap:
      A: 15 is the year-to-date aggregate, 16 is the contribution date
      B: 15 is the expenditure date,       16 is the purpose

      Read off the values, not the position: A's 15 holds 200 next to an amount
      of 200, and its 16 holds 20030402. B's 15 holds 20030521 and its 16 holds
      "City Council Race for Denver COlorado". Line them up by position across
      the two and the date column lands on an aggregate.

  17 is EMPTY on every row of both. A trailing pipe, not a field.

  Dates are YYYYMMDD text. A's date is filled on 98.4%, B's on 95.8%.
  addr2 is filled on 13.2% of A and 11.4% of B; zip ext on 48.7% and 7.2%.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_LIB / ".env", override=True)

import ingest  # noqa: E402
import snow  # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

ZIP_PATH = _LIB / "raw_downloads" / "irs527_full.zip"
URL = "https://forms.irs.gov/app/pod/dataDownload/fullData"
CHUNK = 250_000

SHARED = ["FORM_ID_NUMBER", "SCHEDULE_ID", "ORG_NAME", "EIN", "PERSON_NAME",
          "ADDR1", "ADDR2", "CITY", "STATE", "ZIP", "ZIP_EXT", "EMPLOYER",
          "AMOUNT", "OCCUPATION"]

SCHEMAS = {
    # PERSON_NAME is the contributor here and the recipient in B. Kept as one
    # name so the two tables stay comparable, with the role in the table name.
    "A": ("irs527_schedule_a_contributions", "IRS527_SCHEDULE_A_CONTRIBUTIONS",
          SHARED + ["AGG_CONTRIBUTION_YTD", "CONTRIBUTION_DATE", "_TRAILING"]),
    "B": ("irs527_schedule_b_expenditures", "IRS527_SCHEDULE_B_EXPENDITURES",
          SHARED + ["EXPENDITURE_DATE", "EXPENDITURE_PURPOSE", "_TRAILING"]),
}
WIDTH = 17  # fields after the record-type field


def _download() -> None:
    if ZIP_PATH.exists():
        print(f"  using {ZIP_PATH.name}, {ZIP_PATH.stat().st_size/1e6:,.0f} MB", flush=True)
        return
    import requests
    print("  downloading the POFD full file...", flush=True)
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(URL, timeout=1800)
    r.raise_for_status()
    ZIP_PATH.write_bytes(r.content)
    print(f"  got {len(r.content)/1e6:,.0f} MB", flush=True)


def write_chunk(conn, rows, rt, run_id, started, first: bool) -> int:
    sid, table, cols = SCHEMAS[rt]
    df = pd.DataFrame(rows, columns=cols).drop(columns=["_TRAILING"])
    out = ingest._stringify(df)
    out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    out[ingest.META_SOURCE_RUN_ID] = run_id
    out[ingest.META_SRC_SHA256] = hashlib.sha256(
        df.to_csv(index=False).encode("utf-8", "replace")).hexdigest()
    out.columns = [ingest._sf_col(c) for c in out.columns]
    ok, _c, _r, _ = write_pandas(
        conn, out, table_name=table, database=settings.raw_database,
        schema=settings.raw_schema, auto_create_table=True,
        overwrite=first, quote_identifiers=False)
    if not ok:
        raise RuntimeError(f"write_pandas failed on a {rt} chunk")
    return len(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--types", default="A,B", help="which schedules to load")
    ap.add_argument("--dry-run", action="store_true",
                    help="count and check the shape, land nothing")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after this many rows per type, for a smoke test")
    args = ap.parse_args()
    want = [t.strip().upper() for t in args.types.split(",") if t.strip()]

    print("=== IRS 527 Schedule A and B ===", flush=True)
    _download()

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = None if args.dry_run else snow.connect()
    bufs = {t: [] for t in want}
    firsts = {t: True for t in want}
    totals = {t: 0 for t in want}
    ragged = {t: 0 for t in want}

    try:
        zf = zipfile.ZipFile(ZIP_PATH)
        name = zf.infolist()[0].filename
        with zf.open(name) as raw:
            for line in io.TextIOWrapper(raw, encoding="latin-1"):
                rt = line[:1]
                if rt not in bufs:
                    continue
                parts = line.rstrip("\r\n").split("|")[1:]
                if len(parts) != WIDTH:
                    # 25 of these in 17.9M rows. Counted and dropped, never
                    # padded: padding slides money into the wrong column.
                    ragged[rt] += 1
                    continue
                bufs[rt].append(parts)
                if len(bufs[rt]) >= CHUNK:
                    if args.dry_run:
                        totals[rt] += len(bufs[rt])
                    else:
                        totals[rt] += write_chunk(conn, bufs[rt], rt, run_id,
                                                  started, firsts[rt])
                        firsts[rt] = False
                    print(f"    {rt}: {totals[rt]:,} rows", flush=True)
                    bufs[rt] = []
                if args.limit and all(totals[t] >= args.limit for t in want):
                    break
        for rt in want:
            if bufs[rt]:
                if args.dry_run:
                    totals[rt] += len(bufs[rt])
                else:
                    totals[rt] += write_chunk(conn, bufs[rt], rt, run_id,
                                              started, firsts[rt])
                    firsts[rt] = False

        print()
        for rt in want:
            sid, table, _ = SCHEMAS[rt]
            print(f"  {rt}: {totals[rt]:,} rows, {ragged[rt]:,} ragged -> {table}", flush=True)
            if args.dry_run or not totals[rt]:
                continue
            ingest._log_run(conn, sid, run_id, "success", totals[rt], 0, "", URL,
                            started, ingest._utcnow(),
                            f"IRS 527 Schedule {rt}, streamed from the POFD full file.")
    finally:
        if conn is not None:
            conn.close()

    print("\nDRY RUN: nothing landed" if args.dry_run else "\nDONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
