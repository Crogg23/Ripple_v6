"""Load the remaining CourtListener bulk exports into LIBRARY_RAW.LANDING.

Ripple already holds dockets, judges, judicial positions, the parent financial
disclosure and its investments. This loads everything else the publisher ships
as a bulk file: the judge background + money detail (education, political
affiliation, retention elections, gifts, debts, agreements, outside income,
reimbursements, spousal income, positions), the court dimension, the decision
metadata layer (opinion clusters), the citation network, parentheticals, oral
arguments, originating-court info, and -- only with --tier text -- the 54.6 GB
full opinion text.

NOTE: parties and attorneys have NO bulk export (API-only). Not loadable here.

Same proven path as scripts/courtlistener_dockets_load.py:
  download .csv.bz2 -> PUT as-is to a stage -> COPY INTO a pre-created
  all-VARCHAR table, with column order taken from the publisher's own
  load-bulk-data-<date>.sh (the CSVs carry a header but the script is the
  authority), stamping provenance columns in the COPY transformation.

    python scripts/courtlistener_bulk_load.py --list
    python scripts/courtlistener_bulk_load.py --tier small --run
    python scripts/courtlistener_bulk_load.py --tier meta --run
    python scripts/courtlistener_bulk_load.py --tier text --run   # 54.6 GB
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import shutil
import sys
import uuid
from pathlib import Path

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

DATE = "2026-06-30"
S3 = "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data"
LOADSH_URL = f"{S3}/load-bulk-data-{DATE}.sh"
# Stable, project-relative -- NOT a Claude-Code session scratchpad (those are
# tied to one session UUID and vanish, so the re-use check below would
# silently re-download gigabytes every session).
CACHE_DIR = _REPO / "outputs" / "_bulk_cache"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# stem (without -DATE.csv.bz2)  ->  (Snowflake table suffix, tier)
# tiers: small = tiny judge/court files; meta = decision metadata + citations;
#        text = the 54.6 GB opinion bodies.
FILES: dict[str, tuple[str, str]] = {
    "courts": ("COURTS", "small"),
    "courthouses": ("COURTHOUSES", "small"),
    "court-appeals-to": ("COURT_APPEALS_TO", "small"),
    "people-db-schools": ("SCHOOLS", "small"),
    "people-db-educations": ("JUDGE_EDUCATIONS", "small"),
    "people-db-political-affiliations": ("JUDGE_POLITICAL_AFFILIATIONS", "small"),
    "people-db-retention-events": ("JUDGE_RETENTION_EVENTS", "small"),
    "people-db-races": ("JUDGE_RACES", "small"),
    "people_db_race": ("RACE_CODES", "small"),
    "financial-disclosures-positions": ("DISCLOSURE_POSITIONS", "small"),
    "financial-disclosures-agreements": ("DISCLOSURE_AGREEMENTS", "small"),
    "financial-disclosures-non-investment-income": ("DISCLOSURE_NON_INVESTMENT_INCOME", "small"),
    "financial-disclosures-spousal-income": ("DISCLOSURE_SPOUSAL_INCOME", "small"),
    "financial-disclosures-reimbursements": ("DISCLOSURE_REIMBURSEMENTS", "small"),
    "financial-disclosures-gifts": ("DISCLOSURE_GIFTS", "small"),
    "financial-disclosures-debts": ("DISCLOSURE_DEBTS", "small"),
    "originating-court-information": ("ORIGINATING_COURT_INFO", "meta"),
    "opinion-clusters": ("OPINION_CLUSTERS", "meta"),
    "citations": ("CITATIONS", "meta"),
    "citation-map": ("CITATION_MAP", "meta"),
    "parentheticals": ("PARENTHETICALS", "meta"),
    "oral-arguments": ("ORAL_ARGUMENTS", "meta"),
    # CourtListener's own copy of the FJC integrated database. Ripple already
    # holds the FJC's direct publication (24M rows across four tables); this
    # copy earns its place only because it carries CourtListener docket ids.
    "fjc-integrated-database": ("FJC_IDB_CL_LINKED", "meta"),
    "opinions": ("OPINIONS", "text"),
}
TBL_PREFIX = "FED_COURTLISTENER_"
# Free local disk we insist on keeping AFTER a download completes.
DISK_HEADROOM_BYTES = 10 * 1024 ** 3


def load_sh() -> str:
    cache = CACHE_DIR / f"load-bulk-data-{DATE}.sh"
    if not cache.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text(requests.get(LOADSH_URL, timeout=120,
                                      headers=USER_AGENT).text, encoding="utf-8")
    return cache.read_text(encoding="utf-8", errors="replace")


def column_map() -> dict[str, list[str]]:
    """file stem -> ordered column list, per the publisher's own load script."""
    out: dict[str, list[str]] = {}
    pat = r"\\COPY public\.(\w+)\s*\((.*?)\)\s*FROM\s*'\$BULK_DIR/([^']+)'"
    for m in re.finditer(pat, load_sh(), re.S):
        cols = [c.strip().upper() for c in m.group(2).replace("\n", " ").split(",")]
        stem = m.group(3).replace(f"-{DATE}.csv", "")
        out[stem] = cols
    return out


def remote_size(url: str) -> int:
    r = requests.head(url, timeout=60, headers=USER_AGENT, allow_redirects=True)
    r.raise_for_status()
    return int(r.headers.get("Content-Length", 0))


def download(stem: str) -> tuple[Path, str, int]:
    """Stream-download the bz2 (re-using a complete prior download); sha256."""
    url = f"{S3}/{stem}-{DATE}.csv.bz2"
    local = CACHE_DIR / f"{stem}-{DATE}.csv.bz2"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    size = remote_size(url)
    if local.exists() and local.stat().st_size == size:
        print(f"  Using existing {local.name} ({size/1e9:.2f} GB)")
    else:
        free = shutil.disk_usage(CACHE_DIR).free
        if free < size + DISK_HEADROOM_BYTES:
            raise SystemExit(
                f"  REFUSING {stem}: needs {size/1e9:.1f} GB + 10 GB headroom, "
                f"only {free/1e9:.1f} GB free.")
        print(f"  Downloading {url} ({size/1e9:.2f} GB)")
        tmp = local.with_suffix(".part")
        with requests.get(url, stream=True, timeout=7200, headers=USER_AGENT) as r:
            r.raise_for_status()
            done = 0
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(1 << 22):
                    f.write(chunk)
                    done += len(chunk)
                    if done % (1 << 30) < (1 << 22):
                        print(f"    {done/1e9:.1f} GB", flush=True)
        tmp.replace(local)
        if local.stat().st_size != size:
            raise SystemExit(f"  {stem}: short download "
                             f"{local.stat().st_size} != {size}")
    h = hashlib.sha256()
    with open(local, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return local, h.hexdigest(), size


def load_one(conn, stem: str, tbl_suffix: str, cols: list[str]) -> int:
    tbl = TBL_PREFIX + tbl_suffix
    stage = f"STG_CL_{tbl_suffix}"
    url = f"{S3}/{stem}-{DATE}.csv.bz2"
    local, sha, nbytes = download(stem)
    run_id = str(uuid.uuid4())
    cur = conn.cursor()
    cols_sql = ", ".join(f'"{c}" VARCHAR' for c in cols)
    cur.execute(f'CREATE OR REPLACE TABLE {bulk.LANDING_FQS}."{tbl}" ({cols_sql}, '
                f"{bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR)")
    cur.execute(f'CREATE OR REPLACE STAGE {bulk.LANDING_FQS}."{stage}"')
    print(f"  PUT {local.name} ...", flush=True)
    cur.execute(f"PUT 'file://{local.as_posix()}' @{bulk.LANDING_FQS}.\"{stage}\" "
                f"AUTO_COMPRESS=FALSE PARALLEL=8")
    sel = ", ".join(f"${i+1}" for i in range(len(cols)))
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat()
    print("  COPY INTO ...", flush=True)
    cur.execute(f"""
COPY INTO {bulk.LANDING_FQS}."{tbl}"
FROM (SELECT {sel}, '{now}'::TIMESTAMP_NTZ, '{run_id}', '{sha}'
      FROM @{bulk.LANDING_FQS}."{stage}")
FILE_FORMAT=(TYPE=CSV COMPRESSION=BZ2 SKIP_HEADER=1
             FIELD_OPTIONALLY_ENCLOSED_BY='"' ESCAPE='\\\\'
             NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE ENCODING='UTF8'
             ERROR_ON_COLUMN_COUNT_MISMATCH=TRUE)
ON_ERROR=ABORT_STATEMENT
""")
    for row in cur.fetchall():
        print("  COPY:", row[:4])
    cur.execute(f'SELECT COUNT(*) FROM {bulk.LANDING_FQS}."{tbl}"')
    rows = cur.fetchone()[0]
    print(f"  ROWS={rows:,}  {url}  sha256={sha}")
    cur.execute(f'DROP STAGE {bulk.LANDING_FQS}."{stage}"')
    passed, _ = bulk.run_quality_gate(
        conn, tbl.lower(), tbl, run_id,
        sha256=sha, row_count=rows, source_url=url, file_bytes=nbytes)
    if not passed:
        print(f"  [WARN] quality gate failed for {tbl}")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default="small", choices=["small", "meta", "text", "all"])
    ap.add_argument("--only", default="", help="comma-separated file stems")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()

    cmap = column_map()
    wanted = [s for s, (_, t) in FILES.items()
              if (a.tier == "all" or t == a.tier)]
    if a.only:
        wanted = [s for s in a.only.split(",") if s in FILES]

    if a.list or not a.run:
        for s in wanted:
            n = len(cmap.get(s, []))
            print(f"{s:48s} -> {TBL_PREFIX + FILES[s][0]:44s} {n} cols"
                  f"{'  [NO COLUMN SPEC]' if not n else ''}")
        return

    missing = [s for s in wanted if s not in cmap]
    if missing:
        raise SystemExit(f"no column spec in the publisher load script for: {missing}")

    conn = snow.connect()
    ok, bad = [], []
    try:
        for s in wanted:
            print(f"\n=== {s} -> {TBL_PREFIX + FILES[s][0]}", flush=True)
            try:
                rows = load_one(conn, s, FILES[s][0], cmap[s])
                ok.append((s, rows))
            except SystemExit:
                raise
            except Exception as e:
                print(f"  [FAILED] {s}: {e}")
                bad.append((s, str(e)))
    finally:
        conn.close()
    print("\n--- SUMMARY ---")
    for s, r in ok:
        print(f"  OK    {s:48s} {r:>12,}")
    for s, e in bad:
        print(f"  FAIL  {s:48s} {e[:80]}")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
