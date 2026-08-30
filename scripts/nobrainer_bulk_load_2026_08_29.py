#!/usr/bin/env python3
"""Deterministic (LLM-free) loaders for the 2026-08-29 "no-brainer" acquisitions.

Four public sources that each plug straight into an ID family the warehouse
already carries (see reports/recon/master_connections_pass1_2026-08-29.md):

  sam            SAM.gov Entity Management PUBLIC monthly extract (V2)
                 -> FED_SAM_ENTITY_PUBLIC          UEI + CAGE + legacy DUNS on one row
  uscg           USCG "Merchant Vessels of the United States" (vesdoc, tab/csv release)
                 -> FED_USCG_VESSEL_DOCUMENTATION  official # + IMO + call sign + owner
  fmcsa          FMCSA Company Census File (data.transportation.gov az4n-8mr2)
                 -> FED_FMCSA_COMPANY_CENSUS       USDOT # + DUNS + legal/DBA name
  campd_facility EPA CAMPD facility attributes, one file per year
                 -> FED_EPA_CAMPD_FACILITY         ORISPL (= EIA plant id) + unit + lat/lon
  campd_daily    EPA CAMPD daily unit emissions, one file per state-year
                 -> FED_EPA_CAMPD_EMISSIONS_DAILY  ORISPL + unit + date + SO2/NOx/CO2

All columns land as VARCHAR (raw mirror) with the standard provenance stamps,
chunked write_pandas appends, a per-file checkpoint for resume, and the shared
quality gate + INGEST_RUNS log at the end. Pattern copied from
scripts/fda_faers_load.py / scripts/gleif_relationships_load.py.

    python scripts/nobrainer_bulk_load_2026_08_29.py --source sam --run
    python scripts/nobrainer_bulk_load_2026_08_29.py --source campd_daily --years 2015-2025 --run
    python scripts/nobrainer_bulk_load_2026_08_29.py --source all --run

Preview (no --run) downloads/parses the first chunk and prints a sample.
Local file cache: --cache <dir> (defaults to the session scratchpad if set via
RIPPLE_DL_CACHE, else ./_dl_cache).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd
import requests

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
for p in (str(_REPO), str(_LIB), str(_REPO / "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import _bulk_load_utils as bulk  # noqa: E402

CHUNK_ROWS = 100_000
UA = {"User-Agent": "Ripple/1.0 (public-records research; bulk loader)"}
CACHE = Path(os.environ.get("RIPPLE_DL_CACHE") or (_REPO / "_dl_cache"))
CHECKPOINT = _REPO / "outputs" / "nobrainer_load_checkpoint_2026-08-29.json"

# ---------------------------------------------------------------------------
# layouts
# ---------------------------------------------------------------------------
SAM_COLUMNS = [
    "UEI_SAM", "UEI_DUNS", "ENTITY_EFT_INDICATOR", "CAGE_CODE", "DODAAC", "SAM_EXTRACT_CODE",
    "PURPOSE_OF_REGISTRATION", "INITIAL_REGISTRATION_DATE", "REGISTRATION_EXPIRATION_DATE",
    "LAST_UPDATE_DATE", "ACTIVATION_DATE", "LEGAL_BUSINESS_NAME", "DBA_NAME", "ENTITY_DIVISION",
    "ENTITY_DIVISION_NUMBER", "PHYSICAL_ADDRESS_LINE_1", "PHYSICAL_ADDRESS_LINE_2",
    "PHYSICAL_ADDRESS_CITY", "PHYSICAL_ADDRESS_STATE", "PHYSICAL_ADDRESS_ZIP",
    "PHYSICAL_ADDRESS_ZIP4", "PHYSICAL_ADDRESS_COUNTRY_CODE", "PHYSICAL_ADDRESS_CONGRESSIONAL_DISTRICT",
    "DB_OPEN_DATA_FLAG", "ENTITY_START_DATE", "FISCAL_YEAR_END_CLOSE_DATE", "ENTITY_URL",
    "ENTITY_STRUCTURE", "STATE_OF_INCORPORATION", "COUNTRY_OF_INCORPORATION",
    "BUSINESS_TYPE_COUNTER", "BUSINESS_TYPE_STRING", "PRIMARY_NAICS", "NAICS_CODE_COUNTER",
    "NAICS_CODE_STRING", "PSC_CODE_COUNTER", "PSC_CODE_STRING", "CREDIT_CARD_USAGE",
    "CORRESPONDENCE_FLAG", "MAILING_ADDRESS_LINE_1", "MAILING_ADDRESS_LINE_2",
    "MAILING_ADDRESS_CITY", "MAILING_ADDRESS_ZIP", "MAILING_ADDRESS_ZIP4",
    "MAILING_ADDRESS_COUNTRY", "MAILING_ADDRESS_STATE",
]
for _poc in ("GOVT_BUS_POC", "ALT_GOVT_BUS_POC", "PAST_PERF_POC", "ALT_PAST_PERF_POC",
             "ELEC_BUS_POC", "ALT_ELEC_BUS_POC"):
    SAM_COLUMNS += [f"{_poc}_{s}" for s in (
        "FIRST_NAME", "MIDDLE_INITIAL", "LAST_NAME", "TITLE", "ST_ADD_1", "ST_ADD_2", "CITY",
        "ZIP", "ZIP4", "COUNTRY_CODE", "STATE")]
SAM_COLUMNS += [
    "NAICS_EXCEPTION_COUNTER", "NAICS_EXCEPTION_STRING", "DEBT_SUBJECT_TO_OFFSET_FLAG",
    "EXCLUSION_STATUS_FLAG", "SBA_BUSINESS_TYPES_COUNTER", "SBA_BUSINESS_TYPES_STRING",
    "NO_PUBLIC_DISPLAY_FLAG", "DISASTER_RESPONSE_COUNTER", "DISASTER_RESPONSE_STRING",
] + [f"FLEX_FIELD_{i}" for i in range(1, 21)] + ["END_OF_RECORD"]
assert len(SAM_COLUMNS) == 142, len(SAM_COLUMNS)

USCG_COLUMNS = [
    "VESSEL_ID", "VESSEL_NAME", "CALL_SIGN", "OFFICIAL_NUMBER", "IMO_NUMBER", "HULL_NUMBER", "HIN",
    "SERVICE", "FLAG", "SELF_PROPELLED_IND", "GROSS_TON", "NET_TON", "LENGTH", "BREADTH", "DEPTH",
    "ITC_GROSS_TON", "ITC_NET_TON", "ITC_LENGTH", "ITC_BREADTH", "ITC_DEPTH", "DEAD_WEIGHT_TON",
    "DEAD_WEIGHT_TON_MEASURE_UNIT", "MEASURING_ORGANIZATION_NAME", "HAILING_PORT",
    "HAILING_PORT_STATE", "HAILING_PORT_COUNTRY",
    "TRADE_COASTWISE_UNRESTRICTED", "TRADE_LIMITED_COASTWISE_BOWATERS", "TRADE_LIMITED_COASTWISE_MARAD_WAIVER",
    "TRADE_LIMITED_COASTWISE_OIL_SPILL", "TRADE_LIMITED_COASTWISE_CHARTER_CITIZEN",
    "TRADE_LIMITED_COASTWISE_FISH_PRODUCTS", "TRADE_FISHERY", "TRADE_LIMITED_FISHERY",
    "TRADE_RECREATION", "TRADE_LIMITED_RECREATION_GREAT_LAKES", "TRADE_REGISTRY",
    "TRADE_LIMITED_REGISTRY_CROSS_BORDER", "TRADE_LIMITED_REGISTRY_NO_FOREIGN_VOYAGE",
    "TRADE_LIMITED_REGISTRY_CANADA_ONLY", "TRADE_GREAT_LAKES",
    "BUILDER", "SHIPYARD", "BUILD_YEAR", "COMPLETE_BUILD_CITY", "COMPLETE_BUILD_STATE",
    "COMPLETE_BUILD_PROVINCE", "COMPLETE_BUILD_COUNTRY", "HULL_BUILD_CITY", "HULL_BUILD_STATE",
    "HULL_BUILD_PROVINCE", "HULL_BUILD_COUNTRY",
    "PARTY_ID", "ORGANIZATION_NAME", "ORGANIZATION_TYPE", "PERSON_NAME_FIRST", "PERSON_NAME_MIDDLE",
    "PERSON_NAME_LAST", "PERSON_NAME_SUFFIX", "ADDRESS_LINE_1", "ADDRESS_LINE_2", "ADDRESS_LINE_3",
    "ADDRESS_LINE_4", "CITY", "STATE", "PROVINCE", "COUNTRY", "POSTAL_CODE",
    "MAIN_HP_AHEAD", "MAIN_HP_ASTERN", "PROPULSION_TYPE", "HULL_MATERIAL", "HULL_CONFIGURATION",
    "HULL_SHAPE", "COD_STATUS", "COD_ISSUE_DATE", "COD_EXPIRE_DATE", "FILLER",
]
assert len(USCG_COLUMNS) == 78, len(USCG_COLUMNS)

STATES = ("al ak az ar ca co ct de dc fl ga hi id il in ia ks ky la me md ma mi mn ms mo mt ne nv nh "
          "nj nm ny nc nd oh ok or pa pr ri sc sd tn tx ut vt va wa wv wi wy").split()

SOURCES = {
    "sam": dict(table="FED_SAM_ENTITY_PUBLIC", sid="fed_sam_entity_public",
                url="https://api.sam.gov/data-services/v1/extracts?fileType=ENTITY&sensitivity=PUBLIC&frequency=MONTHLY"),
    "uscg": dict(table="FED_USCG_VESSEL_DOCUMENTATION", sid="fed_uscg_vessel_documentation",
                 url="https://www.dco.uscg.mil/Portals/9/DCO%20Documents/5p/CG-5PC/INV/Merchant%20Vessels%20of%20US/"),
    "fmcsa": dict(table="FED_FMCSA_COMPANY_CENSUS", sid="fed_fmcsa_company_census",
                  url="https://data.transportation.gov/api/views/az4n-8mr2/rows.csv?accessType=DOWNLOAD"),
    "campd_facility": dict(table="FED_EPA_CAMPD_FACILITY", sid="fed_epa_campd_facility",
                           url="https://api.epa.gov/easey/bulk-files/facility/"),
    "campd_daily": dict(table="FED_EPA_CAMPD_EMISSIONS_DAILY", sid="fed_epa_campd_emissions_daily",
                        url="https://api.epa.gov/easey/bulk-files/emissions/daily/state/"),
}

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _cp_load() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {}


def _cp_save(cp: dict):
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(cp, indent=1))


def _download(url: str, dest: Path, *, params: dict | None = None, timeout: int = 900) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, params=params, headers=UA, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    tmp.replace(dest)
    return dest


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _ensure_table(conn, tbl: str, cols: list[str], existing: dict[str, set], extra_meta: list[str]):
    cur = conn.cursor()
    if tbl not in existing:
        cur.execute(f"SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
        existing[tbl] = {r[0] for r in cur.fetchall()}
    meta_cols = [bulk.META_SOURCE_RUN_ID, bulk.META_SRC_SHA256] + extra_meta
    if not existing[tbl]:
        meta = f", {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, " + ", ".join(f"{c} VARCHAR" for c in meta_cols)
        cur.execute(f'CREATE TABLE {bulk.LANDING_FQS}."{tbl}" ({", ".join(c + " VARCHAR" for c in cols)}{meta})')
        existing[tbl] = set(cols) | set(meta_cols) | {bulk.META_INGESTED_AT}
    else:
        for c in cols + meta_cols:
            if c not in existing[tbl]:
                cur.execute(f'ALTER TABLE {bulk.LANDING_FQS}."{tbl}" ADD COLUMN {c} VARCHAR')
                existing[tbl].add(c)


def _append(conn, tbl: str, df: pd.DataFrame, run_id: str, sha: str, started, extra: dict[str, str],
            existing: dict[str, set]) -> int:
    from snowflake.connector.pandas_tools import write_pandas
    df.columns = [bulk.sf_col(c) for c in df.columns]
    _ensure_table(conn, tbl, list(df.columns), existing, list(extra))
    df = df.astype(object).where(df.notna(), None)
    df[bulk.META_INGESTED_AT] = started
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    for k, v in extra.items():
        df[k] = v
    ok, _c, _n, _ = write_pandas(conn, df, table_name=tbl, database=bulk.LANDING_DB,
                                 schema=bulk.LANDING_SCHEMA, auto_create_table=False,
                                 overwrite=False, quote_identifiers=False)
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    return len(df)


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    # loaders must never write the literal text 'nan' (memory: loader-writes-nan-sentinel)
    return df.replace({"nan": None, "NaN": None, "": None})


def _preview(df: pd.DataFrame, n: int = 3):
    print(f"{len(df):,} rows in first chunk, {len(df.columns)} cols")
    for _, row in df.head(n).iterrows():
        print("  ", {k: v for k, v in list(row.items())[:8]})


# ---------------------------------------------------------------------------
# sources
# ---------------------------------------------------------------------------
def load_sam(conn, run: bool, existing: dict) -> tuple[str, int, str]:
    key = os.environ.get("SAM_API_KEY", "").strip()
    if not key:
        raise SystemExit("SAM_API_KEY missing from library-onboarding/.env")
    today = dt.date.today()
    dest = CACHE / f"SAM_PUBLIC_MONTHLY_V2_{today:%Y%m}.ZIP"
    url = SOURCES["sam"]["url"]
    _download(f"{url}&api_key={key}&date={today:%m/%Y}", dest)
    sha = _sha_file(dest)
    tbl = SOURCES["sam"]["table"]
    run_id, started, total = str(uuid.uuid4()), dt.datetime.utcnow(), 0
    with zipfile.ZipFile(dest) as z:
        name = z.infolist()[0].filename
        extract_date = re.search(r"(\d{8})", name)
        with z.open(name) as raw:
            text = io.TextIOWrapper(raw, encoding="latin-1", errors="replace", newline="")
            buf: list[list] = []
            for line in text:
                if line.startswith("BOF ") or line.startswith("EOF "):
                    continue
                parts = line.rstrip("\r\n").split("|")
                if len(parts) < 142:
                    parts += [None] * (142 - len(parts))
                buf.append(parts[:142])
                if len(buf) >= CHUNK_ROWS:
                    df = _clean(pd.DataFrame(buf, columns=SAM_COLUMNS, dtype=object))
                    if not run:
                        _preview(df)
                        return tbl, 0, sha
                    total += _append(conn, tbl, df, run_id, sha, started,
                                     {"_SRC_EXTRACT_DATE": extract_date.group(1) if extract_date else None}, existing)
                    print(f"  [sam] {total:,} rows", flush=True)
                    buf = []
            if buf:
                df = _clean(pd.DataFrame(buf, columns=SAM_COLUMNS, dtype=object))
                if not run:
                    _preview(df)
                    return tbl, 0, sha
                total += _append(conn, tbl, df, run_id, sha, started,
                                 {"_SRC_EXTRACT_DATE": extract_date.group(1) if extract_date else None}, existing)
    return tbl, total, sha


def load_uscg(conn, run: bool, existing: dict, archive_url: str | None) -> tuple[str, int, str]:
    # dco.uscg.mil refuses non-browser clients (403); the Wayback Machine holds the
    # monthly release. Pass --uscg-url to point at a newer archived (or live) zip.
    url = archive_url or ("https://web.archive.org/web/20260301114647id_/" + SOURCES["uscg"]["url"] + "vesdocDec25Rtab.zip")
    dest = CACHE / Path(url.split("/")[-1]).name
    _download(url, dest)
    sha = _sha_file(dest)
    tbl = SOURCES["uscg"]["table"]
    run_id, started, total = str(uuid.uuid4()), dt.datetime.utcnow(), 0
    release = re.search(r"vesdoc([A-Za-z]{3}\d{2})", url)
    with zipfile.ZipFile(dest) as z:
        member = max(z.infolist(), key=lambda i: i.file_size).filename
        with z.open(member) as raw:
            text = io.TextIOWrapper(raw, encoding="latin-1", errors="replace", newline="")
            reader = csv.reader(text)
            buf: list[list] = []
            for parts in reader:
                if not parts:
                    continue
                if len(parts) < 78:
                    parts += [None] * (78 - len(parts))
                buf.append(parts[:78])
                if len(buf) >= CHUNK_ROWS:
                    df = _clean(pd.DataFrame(buf, columns=USCG_COLUMNS, dtype=object))
                    if not run:
                        _preview(df)
                        return tbl, 0, sha
                    total += _append(conn, tbl, df, run_id, sha, started,
                                     {"_SRC_RELEASE": release.group(1) if release else None}, existing)
                    print(f"  [uscg] {total:,} rows", flush=True)
                    buf = []
            if buf:
                df = _clean(pd.DataFrame(buf, columns=USCG_COLUMNS, dtype=object))
                if not run:
                    _preview(df)
                    return tbl, 0, sha
                total += _append(conn, tbl, df, run_id, sha, started,
                                 {"_SRC_RELEASE": release.group(1) if release else None}, existing)
    return tbl, total, sha


def load_fmcsa(conn, run: bool, existing: dict) -> tuple[str, int, str]:
    dest = CACHE / "fmcsa_company_census.csv"
    _download(SOURCES["fmcsa"]["url"], dest, timeout=1800)
    sha = _sha_file(dest)
    tbl = SOURCES["fmcsa"]["table"]
    run_id, started, total = str(uuid.uuid4()), dt.datetime.utcnow(), 0
    for df in pd.read_csv(dest, dtype=str, chunksize=CHUNK_ROWS, low_memory=False,
                          encoding_errors="replace", on_bad_lines="skip", keep_default_na=False):
        df = _clean(df)
        if not run:
            _preview(df)
            return tbl, 0, sha
        total += _append(conn, tbl, df, run_id, sha, started, {}, existing)
        print(f"  [fmcsa] {total:,} rows", flush=True)
    return tbl, total, sha


def _campd_files(kind: str, years: list[int]) -> list[tuple[str, str, str]]:
    base = SOURCES[kind]["url"]
    out = []
    for y in years:
        if kind == "campd_facility":
            out.append((f"facility-{y}.csv", base + f"facility-{y}.csv", str(y)))
        else:
            for st in STATES:
                out.append((f"emissions-daily-{y}-{st}.csv", base + f"emissions-daily-{y}-{st}.csv", f"{y}-{st}"))
    return out


def load_campd(conn, run: bool, existing: dict, kind: str, years: list[int]) -> tuple[str, int, str]:
    tbl = SOURCES[kind]["table"]
    cp = _cp_load()
    done = cp.setdefault(kind, {})
    run_id, started, total = str(uuid.uuid4()), dt.datetime.utcnow(), 0
    last_sha = ""
    for fname, url, tag in _campd_files(kind, years):
        if tag in done and run:
            continue
        dest = CACHE / "campd" / fname
        try:
            _download(url, dest)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code in (403, 404):
                done[tag] = {"missing": True}
                _cp_save(cp)
                continue
            raise
        sha = _sha_file(dest)
        last_sha = sha
        n = 0
        for df in pd.read_csv(dest, dtype=str, chunksize=CHUNK_ROWS, low_memory=False,
                              encoding_errors="replace", keep_default_na=False):
            df = _clean(df)
            if not run:
                _preview(df)
                return tbl, 0, sha
            n += _append(conn, tbl, df, run_id, sha, started, {"_SRC_FILE": fname}, existing)
        total += n
        done[tag] = {"rows": n, "sha": sha}
        _cp_save(cp)
        print(f"  [{kind}] {fname}: {n:,} rows (running total {total:,})", flush=True)
    return tbl, total, last_sha


# ---------------------------------------------------------------------------
def _years(spec: str) -> list[int]:
    if "-" in spec:
        a, b = spec.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in spec.split(",")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, choices=list(SOURCES) + ["all"])
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--years", default="1995-2025", help="campd: e.g. 2015-2025 or 2020,2021")
    ap.add_argument("--uscg-url", default=None)
    ap.add_argument("--cache", default=None)
    a = ap.parse_args()
    global CACHE
    if a.cache:
        CACHE = Path(a.cache)
    CACHE.mkdir(parents=True, exist_ok=True)

    conn = bulk.new_conn()
    existing: dict[str, set] = {}
    failed = []
    try:
        for src in (list(SOURCES) if a.source == "all" else [a.source]):
            print(f"=== {src} -> {SOURCES[src]['table']}", flush=True)
            if src == "sam":
                tbl, n, sha = load_sam(conn, a.run, existing)
            elif src == "uscg":
                tbl, n, sha = load_uscg(conn, a.run, existing, a.uscg_url)
            elif src == "fmcsa":
                tbl, n, sha = load_fmcsa(conn, a.run, existing)
            else:
                tbl, n, sha = load_campd(conn, a.run, existing, src, _years(a.years))
            if not a.run:
                print("PREVIEW only -- add --run to land.")
                continue
            passed, report = bulk.run_quality_gate(conn, SOURCES[src]["sid"], tbl, str(uuid.uuid4()),
                                                   sha256=sha, row_count=n, source_url=SOURCES[src]["url"])
            print(f"{tbl}: {n:,} rows appended; gate {'PASS' if passed else 'FAIL'} {report}", flush=True)
            if not passed:
                failed.append(tbl)
    finally:
        conn.close()
    if failed:
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
