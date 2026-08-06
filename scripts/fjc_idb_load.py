#!/usr/bin/env python3
"""Loader for the FJC Integrated Database (IDB) -- real case-level federal court records.

LIBRARY_RAW.LANDING.FED_FJC_IDB (the old table) was confirmed dead weight: 4,126,450
rows where every single column was an empty string. Its registered URL
(https://www.fjc.gov/research/idb) is the IDB's navigation/landing page, not a data
endpoint -- whoever built the original loader scraped the page shell, not a real bulk
file.

The real bulk files are NOT on that landing page's static HTML -- they only appear
after submitting the page's "Court Type" exposed filter (a Drupal view), which is a
plain GET with a taxonomy-term id (field_type_tid=6871/6876/6881/6886). Found by
fetching the landing page with each filter value and following the resulting
"[Dataset Download]" links down to the real files under
https://www.fjc.gov/sites/default/files/idb/{textfiles,datasets}/... -- confirmed
live via HTTP HEAD/GET this session, 2026-08-05.

The IDB is actually FOUR separate FJC products -- civil, criminal, appellate,
bankruptcy -- each with its own codebook and a genuinely different column layout /
unit of observation. Cramming them into one table (what the dead loader's schema
implied) doesn't fit reality, so this loader replaces the one dead table with four
real ones:

  FED_FJC_IDB_CIVIL       one row = one civil case,            SY1988-present  (~10.9M rows, 46 cols)
  FED_FJC_IDB_CRIMINAL    one row = one criminal defendant,     FY1996-present  (~6.3M rows, 144 cols)
  FED_FJC_IDB_APPELLATE   one row = one appellate case,         FY2008-present  (~1.0M rows, 54 cols)
  FED_FJC_IDB_BANKRUPTCY  one row = one bankruptcy case AS OF a fiscal-year-end
                           snapshot date (SNAPSHOT column) -- FY2021-2026Q2      (~7.0M rows, 87 cols)

Civil/criminal/appellate are FJC's full current-era combined files (each is already
FJC's own single deduplicated "one row per case" cumulative extract covering the
whole span shown). Pre-1988/1996/2008 data uses an older, incompatible coding scheme
that FJC keeps in separate legacy files -- not landed here (a much smaller, secondary
scope, not the live "current" product).

SCOPE CUT (disclosed): bankruptcy is NOT the full FY2008-present archive. FJC's own
full bankruptcy text archive is two files (cpbank08to17.zip + cpbank18on_0.zip,
~2.3GB compressed combined) built on "snapshot" semantics -- the SAME case recurs
once per fiscal-year-end snapshot it was open for, so row count balloons far faster
than case count. That one dataset alone would be bigger than civil+criminal+appellate
COMBINED for a similar or longer span. Landed FJC's own pre-built "5 Year File"
(cpbank21to26.zip: FY2021 through 2026-03-31, 6,965,441 rows) instead. A follow-up
pass could land the two full-archive files back to FY2008 if the extra ~15-20M rows
are wanted -- not done this pass, flagged here and in the registry NOTES rather than
silently thrown away.

Deflate64: FJC's zips use zip compress_type=9 (Deflate64/"Enhanced Deflate"), which
Python's stdlib zipfile CANNOT decode on its own (confirmed: raises
"NotImplementedError: That compression method is not supported"). The
zipfile-deflate64 package patches stdlib zipfile to support it; it's a hard
requirement for this loader (see requirements.txt).

    python scripts/fjc_idb_load.py                        # preview all 4 (download + peek, no write)
    python scripts/fjc_idb_load.py --run                   # land all 4 tables, then drop the old dead table
    python scripts/fjc_idb_load.py --run --only civil      # land just one table (does NOT drop the old table)
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

import zipfile_deflate64  # noqa: F401  -- must be imported before zipfile.ZipFile() is
                           # used anywhere below; patches stdlib zipfile to decode
                           # compress_type=9 (Deflate64), which FJC's IDB zips use.
import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402

SID = "fed_fjc_idb"
OLD_TABLE = "FED_FJC_IDB"
LANDING_PAGE = "https://www.fjc.gov/research/idb"
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "Ripple-Research/1.0 (w.rogers9999@gmail.com)"}
CHUNK_ROWS = 200_000
CACHE_DIR = Path(tempfile.gettempdir()) / "ripple_fjc_idb"

DATASETS = {
    "civil": dict(
        table="FED_FJC_IDB_CIVIL",
        zip_url="https://www.fjc.gov/sites/default/files/idb/textfiles/cv88on_0.zip",
        inner="cv88on.txt",
        kind="text",
        unit="one row = one civil case (U.S. district courts)",
        temporal="SY 1988-present (pre-1988 uses an incompatible legacy coding scheme; not landed)",
        codebook="https://www.fjc.gov/sites/default/files/idb/codebooks/"
                 "Civil%20Codebook%201988%20Forward%2010252023.pdf",
    ),
    "criminal": dict(
        table="FED_FJC_IDB_CRIMINAL",
        zip_url="https://www.fjc.gov/sites/default/files/idb/textfiles/cr96on_0.zip",
        inner="cr96on.txt",
        kind="text",
        unit="one row = one criminal defendant (U.S. district courts)",
        temporal="FY 1996-present (pre-1996 uses an incompatible legacy coding scheme; not landed)",
        codebook="https://www.fjc.gov/sites/default/files/idb/codebooks/"
                 "Criminal%20Code%20Book%201996%20Forward.pdf",
    ),
    "appellate": dict(
        table="FED_FJC_IDB_APPELLATE",
        zip_url="https://www.fjc.gov/sites/default/files/idb/textfiles/ap08on.zip",
        inner="ap08on.txt",
        kind="text",
        unit="one row = one appellate case (U.S. courts of appeals)",
        temporal="FY 2008-present (pre-2008 uses an incompatible legacy coding scheme; not landed)",
        codebook="https://www.fjc.gov/sites/default/files/idb/codebooks/"
                 "Appeals%20Codebook%202008%20Forward%20rev%2002102021.pdf",
    ),
    "bankruptcy": dict(
        table="FED_FJC_IDB_BANKRUPTCY",
        zip_url="https://www.fjc.gov/sites/default/files/idb/datasets/cpbank21to26.zip",
        inner="cpbank21to26.sas7bdat",
        kind="sas",
        unit="one row = one bankruptcy case AS OF one fiscal-year-end snapshot date "
             "(SNAPSHOT column) -- a case pending across multiple snapshots recurs "
             "multiple times; NOT deduplicated to one row per case",
        temporal="FY2021 through 2026-03-31 (FJC's own pre-built '5 Year File'). "
                 "SCOPE CUT: full FY2008-present archive (2 more files, ~2.3GB "
                 "compressed combined, tens of millions more rows because of the "
                 "recurring-snapshot semantics) was NOT landed this pass.",
        codebook="https://www.fjc.gov/sites/default/files/idb/codebooks/"
                 "Bankruptcy%20IDB%20Online%20Codebook%20rev%2002282023.pdf",
    ),
}


def _download(url: str, dest: Path) -> str:
    """Stream-download url to dest (skip if a same-size copy is already cached). Returns sha256."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    remote_size = None
    try:
        head = requests.head(url, headers=USER_AGENT, timeout=30, allow_redirects=True)
        if head.ok:
            cl = head.headers.get("Content-Length")
            remote_size = int(cl) if cl else None
    except Exception:
        pass

    if dest.exists() and remote_size and dest.stat().st_size == remote_size:
        print(f"    cached: {dest.name} ({dest.stat().st_size:,} bytes, matches remote Content-Length)", flush=True)
    else:
        print(f"    downloading {url} ...", flush=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        with requests.get(url, headers=USER_AGENT, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        tmp.replace(dest)
        print(f"    downloaded {dest.stat().st_size:,} bytes", flush=True)

    h = hashlib.sha256()
    with open(dest, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _text_chunk_iter(zip_path: Path, inner: str, chunk_rows: int):
    """Stream a tab-delimited member out of a (Deflate64) zip in bounded-memory chunks."""
    zf = zipfile.ZipFile(zip_path)
    f = zf.open(inner)
    try:
        reader = pd.read_csv(
            f, sep="\t", dtype=str, chunksize=chunk_rows,
            encoding="latin1", keep_default_na=False, na_values=[],
            engine="c", on_bad_lines="warn",
        )
        for chunk in reader:
            yield chunk
    finally:
        f.close()
        zf.close()


def _sas_chunk_iter(zip_path: Path, inner: str, chunk_rows: int, work_dir: Path):
    """Extract the sas7bdat member to disk (SAS reader needs real seeking) then stream chunks."""
    zf = zipfile.ZipFile(zip_path)
    try:
        info = zf.getinfo(inner)
        extracted = work_dir / inner
        if not extracted.exists() or extracted.stat().st_size != info.file_size:
            print(f"    extracting {inner} ({info.file_size:,} bytes uncompressed) ...", flush=True)
            zf.extract(inner, work_dir)
    finally:
        zf.close()
    reader = pd.read_sas(str(extracted), format="sas7bdat", encoding="latin1", chunksize=chunk_rows)
    for chunk in reader:
        yield chunk


def _make_chunk_iter(cfg: dict, zip_path: Path, chunk_rows: int):
    if cfg["kind"] == "text":
        return _text_chunk_iter(zip_path, cfg["inner"], chunk_rows)
    return _sas_chunk_iter(zip_path, cfg["inner"], chunk_rows, CACHE_DIR)


def load_dataset(conn, key: str, cfg: dict) -> dict:
    print(f"\n=== {key} -> LIBRARY_RAW.LANDING.{cfg['table']} ===", flush=True)
    zip_path = CACHE_DIR / Path(cfg["zip_url"]).name
    sha = _download(cfg["zip_url"], zip_path)
    chunk_iter = _make_chunk_iter(cfg, zip_path, CHUNK_ROWS)

    run_id = str(uuid.uuid4())
    started = ingest._utcnow()
    appended, manifest_sha, file_bytes, columns, sample, density = ingest._load_landing_chunked(
        conn, chunk_iter, cfg["table"], run_id, started,
        resume_from_row=0, fresh=True, max_rows=0,
    )
    ended = ingest._utcnow()
    status = "empty" if density["empty"] else "success"
    msg = (f"FJC IDB -- {key}: {cfg['unit']}. {cfg['temporal']}. "
           f"{appended:,} rows -> LIBRARY_RAW.LANDING.{cfg['table']} ({len(columns)} cols). "
           f"Source zip sha256 {sha[:16]}. One of 4 tables replacing the dead single-table "
           f"FED_FJC_IDB load (was 4,126,450 all-empty rows).")
    ingest._log_run(conn, SID, run_id, status, appended, file_bytes, manifest_sha,
                     cfg["zip_url"], started, ended, msg)
    print(f"  -> {appended:,} rows landed, {len(columns)} cols, status={status}, "
          f"density={density.get('populated_fraction')}", flush=True)
    return {"key": key, "table": cfg["table"], "rows": appended, "status": status, "sha": sha}


def _build_registry_cfg(counts: dict) -> dict:
    volume = "; ".join(
        f"{DATASETS[k]['table']}: {counts[k]:,} rows" if counts.get(k) is not None
        else f"{DATASETS[k]['table']}: not yet landed"
        for k in DATASETS
    )
    urls = "; ".join(f"{k}={DATASETS[k]['zip_url']}" for k in DATASETS)
    notes = (
        "REPLACES the dead single-table FED_FJC_IDB (was 4,126,450 rows, every column "
        "an empty string -- the original loader scraped the /research/idb navigation "
        "page shell, not a real bulk file; confirmed and retired 2026-08-05). The IDB "
        "is actually 4 separate FJC products, each with its own codebook and column "
        "layout -- landed as 4 tables, not 1:\n"
        + "\n".join(f"  - {DATASETS[k]['table']}: {DATASETS[k]['unit']}. {DATASETS[k]['temporal']}"
                     for k in DATASETS)
        + "\nAll columns land as raw TEXT (house landing convention); decode against the "
        "per-table codebook links below.\n"
        "VERIFIED REDACTION (checked real value density, not just a null count, per house "
        "rule): the JUDGE identity field is 0% populated in EVERY table -- civil "
        "FILEJUDG/TERMJUDG, criminal FJUDGE, appellate DJUDGE/JDGCODE1/JDGCODE2/JDGCODE3 are "
        "ALL blank on every single row (confirmed by direct COUNT of non-blank values, not "
        "assumed). Criminal defendant NAME is ALSO 0% populated on every row (confirmed same "
        "way) -- FJC's public criminal release carries no defendant name field. Civil "
        "PLT/DEF (party name) and appellate APPELLAN/APPELLEE ARE populated (civil ~100%, "
        "appellate ~76.5%) -- civil/appellate party identity works, judge identity does NOT, "
        "criminal defendant identity does NOT. THIS MEANS: judge-level accountability "
        "patterns are NOT directly buildable from this source as landed -- there is no "
        "judge name or judge code column with real values anywhere in it. Would need FJC's "
        "separate fed_fjc_judges/fed_fjc_service tables (already in this warehouse) plus "
        "some other crosswalk FJC does not appear to publish in this product to reconnect "
        "cases to judges. Flagging this now rather than letting the ACCOUNTABILITY_RELEVANCE "
        "text below overclaim what the data can actually do.\n"
        "KNOWN FOLLOW-UP (not done this pass): the existing dbt models "
        "(stg_fed_fjc_idb__federal_court_cases, justice__fed_fjc_idb under "
        "library-onboarding/ripple_dbt) were built against the OLD single-table "
        "FED_FJC_IDB shape/column names (which never matched real data) and a source "
        "table that no longer exists after this load -- they will need a rebuild "
        "against the new 4-table shape before they'll run.\n"
        "Codebooks -- civil: " + DATASETS["civil"]["codebook"]
        + " | criminal: " + DATASETS["criminal"]["codebook"]
        + " | appellate: " + DATASETS["appellate"]["codebook"]
        + " | bankruptcy: " + DATASETS["bankruptcy"]["codebook"]
    )
    return {
        "source_id": SID,
        "name": "FJC Integrated Database (IDB) -- Federal Court Cases",
        "publisher": "Federal Judicial Center (FJC), under a working arrangement with the "
                     "Administrative Office of the U.S. Courts (AOUSC)",
        "url": urls,
        "description": "Case-level federal court records -- civil cases, criminal "
                        "defendants, appellate cases, and bankruptcy cases (by "
                        "fiscal-year-end snapshot) -- as reported by the courts to AOUSC "
                        "and redistributed by FJC. Landed as 4 tables, one per case type, "
                        "because each has a genuinely different unit of observation and "
                        "column layout per FJC's own codebooks.",
        "jurisdiction": "federal", "category": "Justice", "subcategory": "Federal court case records",
        "unit_of_observation": "varies by table -- see NOTES (civil case / criminal "
                                "defendant / appellate case / bankruptcy case-per-snapshot)",
        "temporal_coverage": "Civil SY1988-present; Criminal FY1996-present; Appellate "
                              "FY2008-present; Bankruptcy FY2021 through 2026-03-31 "
                              "(scope cut from full FY2008-present -- see NOTES)",
        "geographic_scope": "United States (federal district, appellate, and bankruptcy courts)",
        "access_method": "bulk_download",
        "format": "tab-delimited text, zipped (civil/criminal/appellate); SAS7BDAT, zipped (bankruptcy)",
        "auth": {"type": "none"}, "cost": "free",
        "update_cadence": "periodic (FJC republishes cumulative extracts several times a year)",
        "volume": volume,
        "license_terms": "U.S. Government work, public domain (FJC/AOUSC)",
        "join_keys": "circuit+district+office+docket (civil/criminal/appellate case identity); "
                     "casekey+snapshot (bankruptcy); civil PLT/DEF and appellate APPELLAN/"
                     "APPELLEE party names are free text, not standardized IDs; NO judge "
                     "identity field has real values anywhere in this source (verified "
                     "0% populated in all 4 tables -- see NOTES)",
        "accountability_relevance": "Case-level record of who was sued or filed for "
                                     "bankruptcy in federal court (civil party names, "
                                     "appellate party names ~76.5% populated), what NOS/offense "
                                     "code, what outcome, and district/office -- a district- and "
                                     "party-level pattern base. Judge-level patterns are NOT "
                                     "directly supported: the judge identity field is verified "
                                     "0% populated in every one of the 4 tables (see NOTES). "
                                     "Criminal defendant NAME is also 0% populated (see NOTES) "
                                     "-- criminal-side accountability here is code/outcome-level "
                                     "(offense, disposition, sentence), not named-defendant-level.",
        "priority_tier": "1",
        "landing_table": "FED_FJC_IDB_CIVIL, FED_FJC_IDB_CRIMINAL, FED_FJC_IDB_APPELLATE, FED_FJC_IDB_BANKRUPTCY",
        "notes": notes,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--only", choices=list(DATASETS), default=None,
                     help="land a single table only (skips the old-table drop)")
    args = ap.parse_args(argv)
    keys = [args.only] if args.only else list(DATASETS)

    print("=== FJC Integrated Database (IDB) -- real case-level federal court records ===", flush=True)
    print(f"Replacing dead FED_FJC_IDB (4,126,450 all-empty rows) with {len(keys)} real table(s): "
          f"{[DATASETS[k]['table'] for k in keys]}", flush=True)

    if not args.run:
        for key in keys:
            cfg = DATASETS[key]
            print(f"\n[preview] {key} -> {cfg['table']}  ({cfg['unit']})", flush=True)
            print(f"  url: {cfg['zip_url']}", flush=True)
            zip_path = CACHE_DIR / Path(cfg["zip_url"]).name
            sha = _download(cfg["zip_url"], zip_path)
            print(f"  sha256: {sha}", flush=True)
            head_iter = _make_chunk_iter(cfg, zip_path, 5)
            head = next(head_iter)
            print(f"  cols ({len(head.columns)}): {list(head.columns)}", flush=True)
            print(f"  sample row: {head.iloc[0].to_dict()}", flush=True)
        print("\nPREVIEW only -- add --run to land, --only <key> to land a single table.", flush=True)
        return 0

    conn = snow.connect()
    try:
        results = [load_dataset(conn, key, DATASETS[key]) for key in keys]

        # Recompute LIVE counts for all 4 tables (not just this run's subset) so the
        # registry VOLUME always reflects current warehouse state, even after --only runs.
        counts = {}
        for key, cfg in DATASETS.items():
            try:
                counts[key] = snow.fetch_scalar(
                    conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{cfg["table"]}"'
                )
            except Exception:
                counts[key] = None

        cfg_reg = _build_registry_cfg(counts)
        snow.execute(conn, *register._merge_sql(register._build_row(cfg_reg, {})))
        print(f"\nRegistry row upserted for SOURCE_ID='{SID}'. VOLUME={cfg_reg['volume']}", flush=True)

        if not args.only:
            all_ok = all(r["status"] == "success" for r in results)
            if all_ok:
                snow.execute(conn, f'DROP TABLE IF EXISTS "{settings.raw_database}"."{settings.raw_schema}"."{OLD_TABLE}"')
                print(f"\nDropped dead table {OLD_TABLE} (was 4,126,450 all-empty rows).", flush=True)
            else:
                print("\nNOT dropping old FED_FJC_IDB -- one or more new tables did not land cleanly "
                      "(see statuses above).", flush=True)

        print("\n=== SUMMARY ===", flush=True)
        for r in results:
            print(f"  {r['table']}: {r['rows']:,} rows landed this run (status={r['status']})", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
