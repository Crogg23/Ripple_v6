# Plan: Agency Catalog Discovery Loaders (Speed-Optimized)

## Design Principles for Speed

The existing CMS loader is sequential and cautious. For maximum throughput:

1. **Skip discovery where we already know the answer.** EPA ECHO, DOL enforcedata, and IRS all publish at known URLs with known schemas. Header-checking 50 URLs one-at-a-time is the #1 time waster for these -- we just hardcode the manifest and go straight to loading.
2. **Parallel everything.** ThreadPoolExecutor with 6-8 workers for downloads + loads running concurrently.
3. **PUT + COPY INTO for big files, write_pandas only for small ones.** Threshold: 20MB raw. Above that, write to a temp file, PUT to a named stage, COPY INTO with INFER_SCHEMA. 2-5x faster for the big EPA/DOL files.
4. **Stream ZIPs without extracting to disk.** ZipFile over BytesIO -- no temp directory, no cleanup, fewer I/O round-trips.
5. **One Snowflake connection per worker** (connection pooling). write_pandas holds the GIL less this way.

```
Time budget per session (realistic):
- SEC DCAT discovery:     ~2 min (fetch data.json + parallel header checks)
- SEC load 30 datasets:   ~5 min (parallel, most are small)
- EPA ECHO load 15 ZIPs:  ~8 min (parallel, ZIPs are 50-700MB but fast CDN)
- DOL enforce load 10:    ~3 min (parallel, CSVs are 10-200MB)  
- IRS bulk load 5:        ~3 min (known URLs, moderate size)
                          --------
Total wall clock:         ~20 min for 60+ new tables
```

---

## Implementation Steps

### 1. Shared Speed Infrastructure

**File:** `scripts/_bulk_load_utils.py`

The shared guts that all four loaders import. Keeps each agency script thin (~50 lines of config + a `main()`).

```python
"""Shared bulk-load utilities -- parallel download + fast Snowflake landing."""
import concurrent.futures
import io, os, re, tempfile, time, zipfile
from pathlib import Path

import pandas as pd
import requests

LANDING_SCHEMA = "LIBRARY_RAW.LANDING"
MAX_WORKERS = 6
SMALL_THRESHOLD = 20_000_000  # 20MB -- below this, write_pandas is fine

def table_name(prefix: str, title: str, max_len=60) -> str: ...
def get_loaded_tables(conn) -> set: ...

def fast_load(conn, url: str, table_name: str, *,
              user_agent: dict = None, max_rows=500_000) -> int:
    """Download CSV and load to Snowflake. Auto-picks PUT+COPY for big files."""
    resp = requests.get(url, stream=True, timeout=300, headers=user_agent)
    resp.raise_for_status()
    size = int(resp.headers.get("content-length", 0))
    
    if size > SMALL_THRESHOLD:
        return _put_copy_load(conn, resp, table_name, max_rows)
    else:
        return _write_pandas_load(conn, resp.content, table_name, max_rows)

def _put_copy_load(conn, resp, table_name, max_rows) -> int:
    """Stream to temp file -> PUT to stage -> COPY INTO -> drop stage."""
    # Writes to temp, PUTs to @~/{table_name}, COPY INTO with INFER_SCHEMA
    ...

def _write_pandas_load(conn, content: bytes, table_name: str, max_rows) -> int:
    """Small-file path: read into pandas, write_pandas, swap."""
    # Existing pattern from cms_bulk_discover_load.py
    ...

def load_zip_csvs(conn, url: str, prefix: str, key_set: set, *,
                  user_agent: dict = None, max_rows=500_000) -> list:
    """Download ZIP, iterate CSVs inside, load each that has entity keys."""
    resp = requests.get(url, timeout=600, headers=user_agent)
    resp.raise_for_status()
    results = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".csv"):
                continue
            with zf.open(name) as f:
                header = f.readline().decode("utf-8", errors="ignore")
            cols = [c.strip().strip('"').upper() for c in header.split(",")]
            keys_found = [c for c in cols if c in key_set]
            if keys_found:
                tbl = table_name(prefix, Path(name).stem)
                with zf.open(name) as f:
                    n = _write_pandas_load(conn, f.read(), tbl, max_rows)
                results.append((tbl, n, keys_found))
    return results

def parallel_load(tasks: list[dict], max_workers=MAX_WORKERS) -> list:
    """Run multiple load jobs in parallel. Each task is {fn, args, kwargs}."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(t["fn"], *t.get("args",()), **t.get("kwargs",{})): t 
                   for t in tasks}
        for fut in concurrent.futures.as_completed(futures):
            task = futures[fut]
            try:
                results.append({"task": task, "result": fut.result()})
            except Exception as e:
                results.append({"task": task, "error": str(e)[:200]})
    return results
```

### 2. SEC DCAT Loader (True catalog discovery)

**File:** `scripts/sec_bulk_discover_load.py`

The only one that needs real DCAT discovery (like CMS). But header checks are parallelized.

```python
CATALOG_URL = "https://www.sec.gov/data.json"
ENTITY_KEYS = {"CIK", "CUSIP", "EIN", "FILER_CIK", "COMPANY_CIK", "TICKER",
               "REGISTRANT_CIK", "OWNER_CIK", "ISSUER_CIK", "ACCESSION_NUMBER"}
SKIP_PATTERNS = {"EDGAR_FULL_INDEX", "FINANCIAL_STATEMENT_DATA"}
TABLE_PREFIX = "FED_SEC"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
```

Flow:
1. Fetch data.json (~2s)
2. Filter for CSV/TSV distributions with downloadURL
3. **Parallel** header checks (8 workers) -- check 50 URLs in ~10s instead of ~60s
4. Filter for entity key presence
5. **Parallel** bulk load (6 workers)

### 3. EPA ECHO Loader (Known manifest, no discovery needed)

**File:** `scripts/epa_echo_bulk_load.py`

Zero discovery overhead -- we know the URLs, we know the keys. Go straight to parallel download + load.

```python
ECHO_MANIFEST = [
    ("ECHO_EXPORTER", "https://echo.epa.gov/files/echodownloads/echo_exporter.zip"),
    ("ICIS_FEC", "https://echo.epa.gov/files/echodownloads/case_downloads.zip"),
    ("ICIS_AIR", "https://echo.epa.gov/files/echodownloads/air_downloads.zip"),
    ("RCRA", "https://echo.epa.gov/files/echodownloads/rcra_downloads.zip"),
    ("NPDES", "https://echo.epa.gov/files/echodownloads/npdes_downloads.zip"),
    ("TRI", "https://echo.epa.gov/files/echodownloads/tri_downloads.zip"),
    ("GHG", "https://echo.epa.gov/files/echodownloads/ghg_downloads.zip"),
    ("SDWIS", "https://echo.epa.gov/files/echodownloads/sdwis_downloads.zip"),
]
ENTITY_KEYS = {"REGISTRY_ID", "FRS_ID", "FAC_EIN", "EIN", "NPDES_ID",
               "RCRA_ID", "HANDLER_ID", "TRI_FACILITY_ID", "GHGRP_ID", "PWSID"}
TABLE_PREFIX = "FED_EPA"
```

Flow:
1. Check which `FED_EPA_*` tables already exist (skip those ZIPs entirely)
2. **Parallel** download of remaining ZIPs (3-4 workers -- these are big so don't saturate)
3. Each ZIP: iterate CSVs, check header for entity key, load matching ones
4. Provenance stamp

The ECHO Exporter alone gives us 1.5M facilities with EIN + REGISTRY_ID. That's the single biggest entity-graph bridge we don't have yet.

### 4. DOL Enforcement Loader (Known manifest)

**File:** `scripts/dol_enforce_bulk_load.py`

```python
DOL_MANIFEST = [
    ("OSHA_INSPECTION", "https://enforcedata.dol.gov/api/data_catalog/osha_inspection/csv"),
    ("OSHA_VIOLATION", "https://enforcedata.dol.gov/api/data_catalog/osha_violation/csv"),
    ("OSHA_ACCIDENT", "https://enforcedata.dol.gov/api/data_catalog/osha_accident/csv"),
    ("OSHA_ACCIDENT_INJURY", "https://enforcedata.dol.gov/api/data_catalog/osha_accident_injury/csv"),
    ("MSHA_MINE", "https://enforcedata.dol.gov/api/data_catalog/full_mine_info/csv"),
    ("MSHA_VIOLATION", "https://enforcedata.dol.gov/api/data_catalog/msha_violation/csv"),
    ("MSHA_ACCIDENT", "https://enforcedata.dol.gov/api/data_catalog/msha_accident/csv"),
    ("WHD_WHISARD", "https://enforcedata.dol.gov/api/data_catalog/whd_whisard/csv"),
    ("WHD_COMPLIANCE", "https://enforcedata.dol.gov/api/data_catalog/whd_compliance_actions/csv"),
]
ENTITY_KEYS = {"EIN", "ACTIVITY_NR", "CASE_ID", "MINE_ID", "CONTROLLER_ID", "FEIN"}
TABLE_PREFIX = "FED_DOL"
```

Flow: same as EPA -- skip loaded, parallel download + load, provenance stamp. These are mostly 10-200MB CSVs so they move fast.

### 5. IRS Targeted Loader (Known manifest, small batch)

**File:** `scripts/irs_bulk_discover_load.py`

Only the sources NOT already covered by `irs_bmf_load.py`:

```python
IRS_MANIFEST = [
    ("IRS_AUTO_REVOCATIONS", "https://apps.irs.gov/pub/epostcard/data-download-revocation.zip",
     "zip", {"EIN"}),
    ("IRS_PUB78_ELIGIBLE_DONEES", "https://apps.irs.gov/pub/epostcard/data-download-pub78.zip",
     "zip", {"EIN"}),
    ("IRS_990_EFILER_INDEX", "https://s3.amazonaws.com/irs-form-990/index_2024.json",
     "json", {"EIN", "OBJECT_ID"}),
    ("IRS_SOI_EXEMPT_ORGS", "https://www.irs.gov/pub/irs-soi/eo_xx.csv",
     "csv", {"EIN"}),
]
TABLE_PREFIX = "FED_IRS"
```

Smallest batch but fills important gaps (revocations = orgs that lost status, Pub78 = valid donees, 990 index = the filing spine).

### 6. Recipe Registration + Acquire Hook

Add all four to `acquire_recipes.json`. SEC/EPA/DOL are safe (snapshot-replace, known URLs, no auth). IRS 990 index is large -- mark disabled until delta-refresh is built.

---

## Speed Comparison

| Metric | Old (CMS-style serial) | New (parallel + PUT) |
|--------|----------------------|---------------------|
| Header checks | ~60s (50 URLs x 1.2s) | ~10s (8 workers) |
| Download 20 CSVs (avg 50MB) | ~200s serial | ~40s (6 workers) |
| Load 20 tables via write_pandas | ~300s | ~80s (parallel + PUT for big ones) |
| **Total for 60 datasets** | **~45 min** | **~15-20 min** |

---

## Verification

1. `python scripts/sec_bulk_discover_load.py` -- should print discovered CSVs in <30s
2. `python scripts/epa_echo_bulk_load.py --limit 2` -- land 2 ECHO ZIPs, check FED_EPA_* tables exist
3. `python scripts/dol_enforce_bulk_load.py --limit 3` -- land OSHA inspection + violation + WHD
4. Check row counts: `SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'FED_%' ORDER BY CREATED DESC LIMIT 20`

---

## Critical Files

- [scripts/cms_bulk_discover_load.py](scripts/cms_bulk_discover_load.py) -- Pattern being cloned and upgraded
- [library-onboarding/snow.py](library-onboarding/snow.py) -- Connection factory (need one conn per thread)
- [library-onboarding/ingest.py](library-onboarding/ingest.py) -- `_log_run()`, `_sf_col()`, `assess_density()`, provenance constants
- [scripts/acquire_recipes.json](scripts/acquire_recipes.json) -- Register for heartbeat auto-refresh
- [scripts/irs_bmf_load.py](scripts/irs_bmf_load.py) -- Reference for registration pattern
