#!/usr/bin/env python3
"""Generic batch loader for the keyless/public-domain first-wave sources from the
75-issue coverage analysis. One direct-file fetch per source -> all-TEXT landing,
snapshot-replace, logged + registered. Per-source error isolation; registry meta
is pulled from the scout agents' verified output (scratchpad/scout_results.json).

    python scripts/issue_batch_load.py --probe     # check every URL is reachable
    python scripts/issue_batch_load.py --run        # load all that probe OK
    python scripts/issue_batch_load.py --run sid1 sid2   # load only these
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import uuid
import zipfile
from pathlib import Path

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

SCOUT = Path("/private/tmp/claude-501/-Users-chrisr--Documents-GitHub-Ripple-v6/"
             "1f0128f4-5c2c-4b54-95f4-72d2ed4e3517/scratchpad/scout_results.json")
MAX_BYTES = 260_000_000  # skip giant files in autonomous mode

# (sid, direct_fetch_url, fmt)   fmt in {csv, zip_csv, xlsx, json}
SPECS = [
    ("xc_owid_nuclear_warheads",      "https://ourworldindata.org/grapher/nuclear-warhead-stockpiles-lines.csv?v=1&csvType=full", "csv"),
    ("intl_owid_milspend",            "https://ourworldindata.org/grapher/military-spending-sipri.csv?v=1&csvType=full", "csv"),
    ("xc_owid_ai_incidents_annual",   "https://ourworldindata.org/grapher/annual-reported-ai-incidents-controversies.csv?v=1&csvType=full", "csv"),
    ("xc_ransomwarelive_victims",     "https://data.ransomware.live/victims.csv", "csv"),
    ("fed_fhfa_hpi",                  "https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv", "csv"),
    ("fed_fbi_nics_checks",           "https://raw.githubusercontent.com/BuzzFeedNews/nics-firearm-background-checks/master/data/nics-firearm-background-checks.csv", "csv"),
    ("xc_wapo_fatal_force",           "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/v2/fatal-police-shootings-data.csv", "csv"),
    ("xc_vera_incarceration_trends",  "https://raw.githubusercontent.com/vera-institute/incarceration-trends/master/incarceration_trends.csv", "csv"),
    ("xc_guttmacher_monthly_abortion","https://osf.io/download/kqb9n/", "csv"),
    ("intl_nti_cns_dprk_missile_tests","https://www.nti.org/wp-content/uploads/2021/10/north_korea_missile_test_database.xlsx", "xlsx"),
    ("xc_nagix_dprk_missile_tests",   "https://raw.githubusercontent.com/nagix/nk-missile-tests/master/data/test.en.json", "json"),
    ("intl_fao_faostat_food_security","https://bulks-faostat.fao.org/production/Food_Security_Data_E_All_Data_(Normalized).zip", "zip_csv"),
    ("intl_freedomhouse",             "https://freedomhouse.org/sites/default/files/2025-02/All_data_FIW_2013-2024.xlsx", "xlsx"),
    ("intl_ti_cpi",                   "https://images.transparencycdn.org/images/CPI2024-Results-and-trends.xlsx", "xlsx"),
    # --- tranche 3 (resolved gov-bulk URLs) ---
    ("intl_wb_ids",                   "https://databank.worldbank.org/data/download/IDS_CSV.zip", "zip_csv"),
    ("fed_cms_nadac",                 "https://download.medicaid.gov/data/nadac-national-average-drug-acquisition-cost-12-25-2024.csv", "csv"),
    ("intl_ipc_food_insecurity_global","https://data.humdata.org/dataset/7a7e7428-b8d7-4d2e-91d3-19100500e016/resource/6926dff7-658a-49e1-8d61-0ed8a983fbe1/download/ipc_global_national_long_latest.csv", "csv"),
    ("fed_noaa_storm_events",         "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2025_c20260526.csv.gz", "gz_csv"),
]

UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; contact w.rogers9999@gmail.com)"}
_SCOUT = {}
if SCOUT.exists():
    raw = json.load(open(SCOUT))
    for n, r in raw.items():
        for rc in r.get("recommendations", []):
            _SCOUT[rc.get("ripple_source_id", "")] = {**rc, "_issue": r.get("title", "")}


def _juris(sid: str) -> str:
    return {"fed": "federal", "intl": "international", "xc": "cross-cutting",
            "st": "state", "loc": "local"}.get(sid.split("_", 1)[0], "cross-cutting")


def _to_df(content: bytes, fmt: str) -> pd.DataFrame:
    if fmt == "csv":
        return pd.read_csv(io.BytesIO(content), dtype=str, keep_default_na=False, low_memory=False)
    if fmt == "zip_csv":
        zf = zipfile.ZipFile(io.BytesIO(content))
        csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        name = max(csvs, key=lambda n: zf.getinfo(n).file_size)
        with zf.open(name) as fh:
            return pd.read_csv(fh, dtype=str, keep_default_na=False, low_memory=False, encoding_errors="replace")
    if fmt == "gz_csv":
        import gzip
        return pd.read_csv(gzip.GzipFile(fileobj=io.BytesIO(content)), dtype=str,
                           keep_default_na=False, low_memory=False, encoding_errors="replace")
    if fmt == "xlsx":
        sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, dtype=str)
        name = max(sheets, key=lambda s: len(sheets[s]))   # largest sheet = the data
        df = sheets[name]
        return df.fillna("")
    if fmt == "json":
        obj = json.loads(content)
        if isinstance(obj, dict):
            lists = [v for v in obj.values() if isinstance(v, list)]
            obj = max(lists, key=len) if lists else [obj]
        return pd.json_normalize(obj).astype(str)
    raise ValueError(f"unknown fmt {fmt}")


def _fetch(url: str) -> bytes:
    r = requests.get(url, headers=UA, timeout=300, stream=True)
    r.raise_for_status()
    chunks, total = [], 0
    for c in r.iter_content(1 << 20):
        chunks.append(c); total += len(c)
        if total > MAX_BYTES:
            raise RuntimeError(f"exceeds {MAX_BYTES//1_000_000}MB cap")
    return b"".join(chunks)


def _register(conn, sid, rows, url) -> None:
    m = _SCOUT.get(sid, {})
    cfg = {
        "source_id": sid, "name": m.get("name", sid)[:200],
        "publisher": m.get("publisher", "")[:200], "url": url,
        "description": (m.get("relevance", "") + " " + m.get("quirks", ""))[:900],
        "jurisdiction": _juris(sid), "category": "Issue-coverage", "subcategory": m.get("_issue", "")[:80],
        "unit_of_observation": m.get("unit_of_observation", "")[:200],
        "geographic_scope": "", "access_method": "bulk_download",
        "format": m.get("data_format", "")[:40], "auth": {"type": "none"}, "cost": "free",
        "update_cadence": m.get("update_cadence", "")[:80], "volume": f"{rows:,} rows",
        "license_terms": m.get("license", "")[:200],
        "join_keys": ", ".join(m.get("join_keys", []))[:200],
        "accountability_relevance": m.get("relevance", "")[:300],
        "priority_tier": "2", "landing_table": sid.upper(),
        "notes": "Loaded by scripts/issue_batch_load.py (75-issue first wave).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def _load_one(conn, sid, url, fmt) -> tuple[bool, str]:
    try:
        content = _fetch(url)
        df = _to_df(content, fmt)
        if df.empty:
            return False, "empty dataframe"
        # blank-name columns -> positional
        df.columns = [str(c) if str(c).strip() and not str(c).startswith("Unnamed") else f"col_{i}"
                      for i, c in enumerate(df.columns)]
        started = ingest._utcnow(); run_id = str(uuid.uuid4())
        sha = hashlib.sha256(content).hexdigest()
        from snowflake.connector.pandas_tools import write_pandas
        out = ingest._stringify(df)
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        out.columns = [ingest._sf_col(c) for c in out.columns]
        ok, _c, _n, _ = write_pandas(conn, out, table_name=sid.upper(),
                                     database=settings.raw_database, schema=settings.raw_schema,
                                     auto_create_table=True, overwrite=True, quote_identifiers=False)
        if not ok:
            return False, "write_pandas failed"
        ended = ingest._utcnow()
        dens = ingest.assess_density(df)
        status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
        ingest._log_run(conn, sid, run_id, status, len(df), len(content), sha, url, started, ended,
                        f"first-wave batch; {len(df):,} rows x {len(df.columns)} cols; density {dens.get('populated_fraction')}")
        _register(conn, sid, len(df), url)
        return True, f"{len(df):,} rows x {len(df.columns)} cols (status={status})"
    except Exception as ex:  # noqa: BLE001
        return False, f"{type(ex).__name__}: {str(ex)[:120]}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("sids", nargs="*")
    args = ap.parse_args(argv)
    specs = [s for s in SPECS if not args.sids or s[0] in args.sids]

    if args.probe or not args.run:
        print("=== PROBE ===", flush=True)
        for sid, url, fmt in specs:
            try:
                r = requests.get(url, headers=UA, timeout=60, stream=True)
                ct = r.headers.get("content-type", "?")[:30]
                cl = r.headers.get("content-length", "?")
                first = next(r.iter_content(2048), b"")
                print(f"  {'OK ' if r.status_code==200 else r.status_code} {sid:32} {fmt:8} ct={ct:30} len={cl} bytes0={len(first)}")
                r.close()
            except Exception as ex:  # noqa: BLE001
                print(f"  ERR {sid:32} {fmt:8} {type(ex).__name__}: {str(ex)[:80]}")
        if not args.run:
            return 0

    print("\n=== LOAD ===", flush=True)
    conn = snow.connect()
    ok = fail = 0
    try:
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        for sid, url, fmt in specs:
            good, msg = _load_one(conn, sid, url, fmt)
            print(f"  {'✓' if good else '✗'} {sid:32} {msg}", flush=True)
            ok += good; fail += (not good)
    finally:
        conn.close()
    print(f"\nDONE: {ok} loaded, {fail} failed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
