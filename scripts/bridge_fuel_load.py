#!/usr/bin/env python3
"""Deterministic (LLM-free) bulk loader for known-good entity-crosswalk sources.

The onboarding agent (onboard.py) needs ANTHROPIC_API_KEY for recon/codegen. For
sources whose exact bulk URL + shape are ALREADY known (the bridge-fuel sources:
CMS provider crosswalks, IRS EO BMF, etc.), no recon/codegen is needed — so this
lands them straight into LIBRARY_RAW.LANDING with the SAME provenance stamps,
INGEST_RUNS log, and SOURCE_REGISTRY upsert as everything else, by reusing
library-onboarding/ingest.py + register.py. Mirrors connect/portal_loader.py,
just for arbitrary CMS/IRS bulk files instead of portal-index datasets.

Handles: direct CSV, zipped CSV (pick a member by name/regex), and chunked
streaming for files too big for memory. All columns land as TEXT (raw mirror).

    python scripts/bridge_fuel_load.py --spec fed_cms_pos_other --run
    python scripts/bridge_fuel_load.py --list
    python scripts/bridge_fuel_load.py --spec all --run

Safe by default: previews (downloads + profiles) unless --run; skips already-landed
unless --force; re-fetch + skip-if-unchanged with --refresh.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import os
import re
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

# Windows consoles default to cp1252; source names carry unicode (↔, —). Never let
# a print() crash the load — emit UTF-8, replacing anything unencodable.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
# Dual insert (repo root + library-onboarding): loadkit lives at the repo root,
# ingest/register/snow live under library-onboarding.
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

# Load library-onboarding/.env (PAT-as-password) before importing config.
try:
    from dotenv import load_dotenv

    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402  library-onboarding/ingest.py
import register      # noqa: E402  library-onboarding/register.py
import snow          # noqa: E402  library-onboarding/snow.py
from config import settings  # noqa: E402

from loadkit import atomic_load  # noqa: E402  staging-swap atomicity for chunked loads

UA = {"User-Agent": "Mozilla/5.0 (ripple-bridge-fuel-loader)"}

# --------------------------------------------------------------------------- #
# Source specs live in scripts/bridge_fuel_specs.py as a plain list `SPECS` of
# dicts (no import of this module → no cycle). Loaded lazily in main().
# --------------------------------------------------------------------------- #
def _load_specs() -> dict[str, dict]:
    import bridge_fuel_specs  # scripts/bridge_fuel_specs.py (curated crosswalk + payload specs)
    specs = {d["source_id"]: d for d in bridge_fuel_specs.SPECS}
    try:  # auto-generated, live-verified backfill batch (scripts/backfill_specs.py)
        import backfill_specs
        specs.update({d["source_id"]: d for d in backfill_specs.SPECS})
    except ModuleNotFoundError:
        pass
    return specs


# --------------------------------------------------------------------------- #
# Fetch helpers
# --------------------------------------------------------------------------- #
def _download(url: str, dest: Path, tries: int = 4) -> Path:
    """Stream a URL to a local file (handles big downloads without memory blow-up)."""
    last = None
    for i in range(tries):
        try:
            with requests.get(url, headers=UA, stream=True, timeout=180) as r:
                r.raise_for_status()
                with open(dest, "wb") as fh:
                    for chunk in r.iter_content(chunk_size=1 << 20):
                        if chunk:
                            fh.write(chunk)
            return dest
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"    download retry {i + 1}/{tries}: {str(e)[:80]}")
    raise RuntimeError(f"download failed after {tries} tries: {url}: {last}")


def _resolve_url(s: dict) -> str:
    """Resolve the current bulk download URL.

    CMS provider-data CSV URLs embed a dated/hashed filename that rotates on each
    refresh, so a hardcoded path 404s next cycle. When a spec gives `provider_data_id`,
    resolve the LIVE downloadURL from the metastore; otherwise use download_url.
    NPPES (download.cms.gov/nppes) rotates its monthly filename too — resolved by
    scraping the files page (_resolve_nppes_url).
    """
    pid = s.get("provider_data_id")
    if pid:
        meta = f"https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/{pid}?show-reference-ids"
        try:
            j = requests.get(meta, headers=UA, timeout=60).json()
            dist = j.get("distribution") or []
            for d in dist:
                dd = d.get("data", d)
                url = dd.get("downloadURL")
                if url and url.lower().endswith(".csv"):
                    print(f"    resolved via metastore: {url}")
                    return url
        except Exception as e:  # noqa: BLE001
            print(f"    metastore resolve failed ({str(e)[:60]}); using spec download_url")
    if "download.cms.gov/nppes" in s["download_url"]:
        return _resolve_nppes_url(s["download_url"])
    return s["download_url"]


# The full-replacement monthly zip: an ALPHABETIC month + 4-digit year (plus an
# optional _V2-style suffix). Weeklies carry MMDDYY digit ranges and the deactivated
# report has a different prefix, so neither can match. Hrefs on the page are
# single-quoted and relative ('./NPPES_...zip') — verified live 2026-07-02.
_NPPES_MONTHLY_RE = re.compile(
    r"href=['\"]\.?/?(NPPES_Data_Dissemination_[A-Za-z]+_\d{4}[^'\"]*\.zip)['\"]", re.I)


def _resolve_nppes_url(fallback: str) -> str:
    """Resolve the CURRENT NPPES Full Replacement Monthly NPI File URL.

    The filename embeds the month (NPPES_Data_Dissemination_<Month>_<Year>[_V2].zip)
    and rotates every month, so a hardcoded URL 404s on the next cycle. Scrape the
    stable files page for the current monthly href; fall back to the spec URL if the
    page shape ever changes (the download then fails loudly, never silently).
    """
    page = "https://download.cms.gov/nppes/NPI_Files.html"
    try:
        html = requests.get(page, headers=UA, timeout=60).text
        m = _NPPES_MONTHLY_RE.search(html)
        if m:
            url = "https://download.cms.gov/nppes/" + m.group(1)
            print(f"    resolved NPPES monthly full file: {url}")
            return url
        print("    NPI_Files.html had no monthly full-file href; using spec download_url")
    except Exception as e:  # noqa: BLE001
        print(f"    NPPES resolve failed ({str(e)[:60]}); using spec download_url")
    return fallback


def _prepare(df: pd.DataFrame, s: dict) -> pd.DataFrame:
    """Apply per-source row filter + canonical key-column aliasing.

    - `filter` = {column, value}: keep only rows where column == value (e.g. NBER
      othpidty=06 so the CCN column holds only real CCN values).
    - `key_cols` = [{col, as}]: rename the VERIFIED id column to a canonical name
      the tagger detects (CCN/NPI are STEEL tokens). Matched case-insensitively on
      stripped/space-collapsed names; errors loudly if a declared col is absent
      (so source schema drift is caught, not silently mis-loaded).
    """
    def _norm(x):
        return re.sub(r"\s+", " ", str(x).strip()).lower()

    # Normalized name -> actual column, built once. Renames below only ever target
    # columns distinct from later lookups, so it stays valid across the loop.
    match = {_norm(c): c for c in df.columns}

    flt = s.get("filter")
    if flt:
        col, val = flt["column"], str(flt["value"])
        real = match.get(_norm(col))
        if real is None:
            raise RuntimeError(f"filter column {col!r} not in {list(df.columns)[:20]}")
        df = df[df[real].astype(str).str.strip() == val]

    for kc in s.get("key_cols", []):
        real = match.get(_norm(kc["col"]))
        if real is None:  # fall back through standard CMS aliases for this id type
            for cand in _KEY_FALLBACKS.get(kc["as"], []):
                real = match.get(_norm(cand))
                if real is not None:
                    print(f"    key {kc['as']}: declared {kc['col']!r} absent; using {real!r}")
                    break
        if real is None:
            raise RuntimeError(
                f"key column {kc['col']!r} (as {kc['as']}) NOT FOUND. "
                f"Columns: {list(df.columns)}")
        df = df.rename(columns={real: kc["as"]})
    return df.loc[:, ~df.columns.duplicated()]


# Standard CMS column names for each hard ID, tried in order when a spec's declared
# key column is absent (CMS facility files vary: 'Facility ID' vs 'CMS Certification
# Number (CCN)' vs 'CCN' vs 'PRVDR_NUM' all denote the CCN).
_KEY_FALLBACKS = {
    "CCN": ["CMS Certification Number (CCN)", "Facility ID", "CCN", "PRVDR_NUM",
            "Provider ID", "Federal Provider Number", "CMS Certification Number"],
    "NPI": ["NPI", "npi"],
}


def _open_csv_source(s: dict, tmp: Path):
    """Return a file-like / path for pandas.read_csv, resolving zip members.

    For zip_csv, extract the chosen member to a temp file and return its path.
    For csv, download to a temp file and return its path.
    """
    url = _resolve_url(s)
    kind = s.get("kind", "csv")
    if kind == "csv":
        dl = _download(url, tmp / "src.csv")
        return dl
    if kind == "zip_csv":
        zpath = _download(url, tmp / "src.zip")
        with zipfile.ZipFile(zpath) as zf:
            members = [n for n in zf.namelist() if n.lower().endswith((".csv", ".txt"))]
            pat = s.get("member")
            chosen = None
            if pat:
                rx = re.compile(pat, re.I)
                chosen = next((m for m in members if rx.search(m)), None)
            if not chosen:
                # default: the largest CSV member
                chosen = max(members, key=lambda m: zf.getinfo(m).file_size) if members else None
            if not chosen:
                raise RuntimeError(f"no CSV member in zip; members={zf.namelist()[:10]}")
            print(f"    zip member: {chosen}")
            out = tmp / "member.csv"
            with zf.open(chosen) as src, open(out, "wb") as dst:
                while True:
                    b = src.read(1 << 20)
                    if not b:
                        break
                    dst.write(b)
            return out
    raise RuntimeError(f"unknown kind '{kind}'")


# Raw-mirror read defaults: every value as TEXT, no NA coercion (so '' stays '').
_READ_DEFAULTS = {"dtype": str, "keep_default_na": False, "na_values": [], "low_memory": False}


def _read_full(path, opts: dict) -> pd.DataFrame:
    return pd.read_csv(path, **{**_READ_DEFAULTS, **(opts or {})})


def _read_multi(s: dict, tmp: Path, opts: dict, preview: bool = False) -> pd.DataFrame:
    """Download + read several SAME-SCHEMA CSVs and concat into ONE frame.

    For sources published as regional/territory partitions that together form one
    dataset/table -- e.g. IRS EO BMF (eo1-4 + eo_xx + eo_pr). Fails LOUD on a column
    mismatch between parts: a drifted partition must NOT silently corrupt the concat
    (pandas would otherwise union columns and NaN-fill, masking the drift). In preview
    mode only the first file is fetched (cheap shape check, not a full multi-GB pull).
    """
    urls = list(s.get("urls") or [])
    if not urls:
        raise RuntimeError(f"{s['source_id']}: 'urls' is empty for a multi-file spec")
    if preview:
        urls = urls[:1]
    frames = []
    for i, url in enumerate(urls):
        dest = _download(url, tmp / f"part_{i}.csv")
        frames.append(_read_full(dest, opts))
    cols0 = list(frames[0].columns)
    for j, f in enumerate(frames[1:], 1):
        if list(f.columns) != cols0:
            raise RuntimeError(
                f"{s['source_id']}: part {j} columns {list(f.columns)[:8]} != "
                f"part 0 {cols0[:8]} -- refusing to concat mismatched schemas")
    out = pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]
    print(f"    multi-file: read {len(urls)} file(s)"
          + (" [PREVIEW: first file only]" if preview else "")
          + f" -> {len(out):,} rows x {len(out.columns)} cols")
    return out


def _iter_chunks(path, opts: dict, chunk_rows: int):
    yield from pd.read_csv(path, chunksize=chunk_rows, **{**_READ_DEFAULTS, **(opts or {})})


# --------------------------------------------------------------------------- #
# Register
# --------------------------------------------------------------------------- #
def _registry_has_row(conn, sid: str) -> bool:
    """One SELECT: does SOURCE_REGISTRY already carry a row for this source_id?"""
    return bool(snow.fetch_scalar(
        conn,
        f'SELECT COUNT(*) FROM "{settings.meta_database}"."{settings.registry_schema}"'
        f'."{settings.registry_table}" WHERE SOURCE_ID = %s',
        (sid,),
    ))


def _register(conn, s: dict) -> None:
    # FACET-CLOBBER GUARD: register's MERGE overwrites matched columns with this
    # spec's non-null defaults (UNCLASSIFIED domain, NONE/[] facets, generic notes).
    # A re-land or scheduled --refresh of an ALREADY-CATALOGED source would therefore
    # wipe every curated facet on its registry row. If the row exists, the source is
    # already in the catalog — skip registration entirely and say so.
    if _registry_has_row(conn, s["source_id"]):
        print(f"    registry row already exists for {s['source_id']} — skipping "
              "registration (a re-register MERGE would clobber curated facets)")
        return
    cfg = {
        "source_id": s["source_id"],
        "name": s.get("name", s["source_id"]),
        "publisher": s.get("publisher", ""),
        "url": s.get("url", s.get("download_url", "")),
        "description": s.get("description", s.get("name", "")),
        "jurisdiction": s.get("jurisdiction", "US"),
        "category": s.get("category", ""),
        "subcategory": s.get("subcategory", ""),
        "unit_of_observation": s.get("unit_of_observation", "one row = one record"),
        "geographic_scope": s.get("geographic_scope", "United States"),
        "temporal_coverage": s.get("temporal_coverage", ""),
        "access_method": s.get("access_method", "bulk"),
        "format": s.get("format", "csv"),
        "auth": {"type": "none"},
        "cost": "free",
        "update_cadence": s.get("update_cadence", "unknown"),
        "volume": s.get("volume", ""),
        "license_terms": s.get("license_terms", "Public domain (US Gov)"),
        "join_keys": s.get("join_keys", ""),
        "accountability_relevance": s.get("accountability_relevance", ""),
        "priority_tier": str(s.get("priority_tier", "2")),
        "landing_table": s["source_id"].upper(),
        "notes": s.get("notes", "Loaded by scripts/bridge_fuel_load.py (LLM-free, known shape)."),
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


# --------------------------------------------------------------------------- #
# Load one spec
# --------------------------------------------------------------------------- #
def _has_success(conn, sid: str) -> bool:
    """True iff this source has EVER landed cleanly (any STATUS='success' run).

    Gating the skip on this -- NOT on table existence -- is what makes the loader
    safe to re-run. A source that has never cleanly succeeded (a partial table left
    by a crashed chunked load, or a first load demoted to STATUS='empty'/'failed')
    is NOT 'already landed', so a default re-run RETRIES it instead of skipping a
    half/junk table as done. (Idempotency keys on INGEST_RUNS, the source of truth.)

    Note: a source that succeeded once and was LATER demoted to 'empty' still reads
    as landed and is skipped by default -- re-pull it with --refresh (sha-checked) or
    --force. The skip-gate's job is "don't re-pull what already landed clean once",
    not "chase a source that went bad"; that's --refresh's job.
    """
    return ingest._latest_success_sha(conn, sid) is not None


def load_spec(s: dict, do_run: bool = False, force: bool = False, refresh: bool = False,
              allow_schema_change: bool = False) -> dict:
    sid = s["source_id"]
    table = sid.upper()
    print(f"\n=== {sid}  ({s.get('name', '')}) ===")
    print(f"    {s['download_url']}")

    conn = snow.connect()
    # Scheduled/wrapper runs set RIPPLE_TASK_WAREHOUSE so a weekly refresh never contends
    # with a live pour on RIPPLE_WH. (SNOWFLAKE_WAREHOUSE can't carry this — config loads
    # .env with override=True, which clobbers a wrapper-set value.)
    _task_wh = os.environ.get("RIPPLE_TASK_WAREHOUSE", "").strip()
    if _task_wh and _task_wh.replace("_", "").isalnum():
        conn.cursor().execute(f"USE WAREHOUSE {_task_wh}")
    try:
        landed = _has_success(conn, sid)
        if landed and not force and not refresh and do_run:
            print("    already landed — skipping (use --force to reload)")
            return {"source_id": sid, "status": "skip (already landed)", "rows": 0}

        started = ingest._utcnow()
        run_id = str(uuid.uuid4())
        try:
            with tempfile.TemporaryDirectory(prefix="bridgefuel_") as td:
                tmp = Path(td)
                opts = s.get("csv_opts", {})

                if s.get("urls"):
                    # Multi-file: several same-schema partitions -> one table (e.g. IRS
                    # EO BMF eo1-4 + eo_xx + eo_pr). Goes through the full (non-chunked)
                    # path, so the density gate applies. Preview reads only the first file.
                    df = _read_multi(s, tmp, opts, preview=not do_run)
                else:
                    src = _open_csv_source(s, tmp)
                    if s.get("chunked"):
                        return _load_chunked(conn, s, src, opts, table, run_id, started,
                                             sid, do_run, allow_schema_change)
                    df = _read_full(src, opts)
                df = _prepare(df, s)
                n_raw = len(df)
                cap = int(s.get("max_rows") or 0)
                if cap and n_raw > cap:
                    df = df.head(cap)
                print(f"    parsed {n_raw:,} rows x {len(df.columns)} cols "
                      f"(landing {len(df):,}{' [capped]' if cap and n_raw > cap else ''})")
                print(f"    columns: {', '.join(map(str, list(df.columns)[:18]))}"
                      f"{' ...' if len(df.columns) > 18 else ''}")

                df_bytes = ingest._df_bytes(df)
                sha = hashlib.sha256(df_bytes).hexdigest()
                if not do_run:
                    print("    PREVIEW only (add --run to land)")
                    return {"source_id": sid, "status": "preview", "rows": len(df), "cols": len(df.columns)}

                if refresh and landed and ingest._latest_success_sha(conn, sid) == sha:
                    print("    unchanged (sha matches last success) — skipped")
                    return {"source_id": sid, "status": "skip (unchanged)", "rows": len(df)}

                out = ingest._stringify(df)
                out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
                out[ingest.META_SOURCE_RUN_ID] = run_id
                out[ingest.META_SRC_SHA256] = sha
                url = s.get("url", s["download_url"])
                try:
                    ingest._load_landing(conn, out, table, overwrite=True)
                    ended = ingest._utcnow()
                    # DENSITY GATE: did this carry real data, or is it an empty/parse-
                    # failure husk (the FED_FJC_IDB failure: rows landed, every source
                    # column blank)? An effectively-empty frame is logged STATUS='empty'
                    # and NOT registered -- it must never ride into the catalog as a source.
                    density = ingest.assess_density(out)
                    if density["empty"]:
                        ingest._log_run(conn, sid, run_id, "empty", len(out), len(df_bytes),
                                        sha, url, started, ended,
                                        f"EMPTY LOAD -- {density['reason']}. "
                                        f"{ingest._density_note(density)}. Landed {len(out):,} rows "
                                        f"into LIBRARY_RAW.LANDING.{table} but the frame carries no "
                                        "real data; NOT registered as a source.")
                        print(f"    EMPTY -- {density['reason']}; logged STATUS='empty', not registered.")
                        return {"source_id": sid, "status": "empty", "rows": len(out),
                                "density": density["populated_fraction"]}
                    ingest._log_run(conn, sid, run_id, "success", len(out),
                                    len(df_bytes), sha, url, started, ended,
                                    f"{s.get('name', sid)}. Bulk LLM-free load of {len(out):,} rows. "
                                    f"{ingest._density_note(density)}.")
                    _register(conn, s)
                    print(f"    LOADED {len(out):,} rows -> LIBRARY_RAW.LANDING.{table}; registered INCLUDE=Y")
                    return {"source_id": sid, "status": "loaded", "rows": len(out),
                            "density": density["populated_fraction"]}
                except Exception as exc:
                    ended = ingest._utcnow()
                    try:
                        ingest._log_run(conn, sid, run_id, "failed", None, None, "",
                                        s.get("url", s["download_url"]), started, ended, f"Load failed: {exc}")
                        exc._run_status_logged = True  # the outer catch must not log this run twice
                    except Exception:
                        pass
                    raise
        except Exception as exc:
            # FAILURE TRACE for everything the inner handlers don't cover: a download,
            # zip-member, parse, or _prepare failure used to die with NO INGEST_RUNS
            # row at all — invisible to the freshness ledger. Previews stay
            # side-effect-free; runs an inner handler already logged aren't re-logged.
            if do_run and not getattr(exc, "_run_status_logged", False):
                try:
                    ingest._log_run(conn, sid, run_id, "failed", None, None, "",
                                    s.get("url", s["download_url"]), started, ingest._utcnow(),
                                    f"Load failed before landing: {str(exc)[:500]}")
                except Exception:
                    pass
            raise
    finally:
        conn.close()


def _table_columns(conn, database: str, schema: str, table: str) -> list | None:
    """Column names of a table (ordinal order), or None if the table doesn't exist.

    INFORMATION_SCHEMA is qualified with the target database — never the session's
    current database, which just happens to be LIBRARY_RAW today.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            f'SELECT COLUMN_NAME FROM "{database}".INFORMATION_SCHEMA.COLUMNS '
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION",
            (schema, table))
        rows = cur.fetchall()
    finally:
        cur.close()
    return [r[0] for r in rows] if rows else None


def _load_chunked(conn, s, src, opts, table, run_id, started, sid, do_run,
                  allow_schema_change: bool = False) -> dict:
    """Stream a big CSV in row-chunks THROUGH A STAGING TABLE; atomic-swap on success.

    Pinned ordering (the atomicity contract — test_loader_conformance fences it):
      1. every chunk writes to <TABLE>__STAGING (chunk-0 overwrite self-cleans any
         stale staging left by an earlier crash)
      2. mid-stream crash  -> drop the STAGING table ONLY + log 'failed'
                              (the live table is untouched by construction)
      3. density gate on the staged rows -> empty: drop staging + log 'empty',
                              live table untouched, nothing registered
      4. schema check staging vs live -> refuse the swap on column drift
                              (--allow-schema-change overrides for real evolution)
      5. atomic_load.execute_swap -> THEN log 'success' -> _register LAST
    """
    from snowflake.connector.pandas_tools import write_pandas

    chunk_rows = int(s.get("chunk_rows") or 100_000)
    cap = int(s.get("max_rows") or 0)
    if not do_run:
        # preview: just read the first chunk for shape
        first = next(_iter_chunks(src, opts, min(chunk_rows, 1000)))
        print(f"    PREVIEW (chunked): {len(first.columns)} cols: "
              f"{', '.join(map(str, list(first.columns)[:18]))}")
        return {"source_id": sid, "status": "preview", "rows": 0, "cols": len(first.columns)}

    database, schema = settings.raw_database, settings.raw_schema
    stg = atomic_load.staging_name(table)
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{database}"."{schema}"')
    url = s.get("url", s["download_url"])
    appended, n, chunk_shas, columns = 0, 0, [], []
    density_frames, density_rows = [], 0   # bounded leading-row sample for the gate
    try:
        for chunk in _iter_chunks(src, opts, chunk_rows):
            chunk = _prepare(chunk, s)
            if len(chunk) == 0:
                continue  # filtered to nothing (e.g. NBER othpidty!=06) — skip
            if cap and appended >= cap:
                break
            if cap and appended + len(chunk) > cap:
                chunk = chunk.head(cap - appended)
            csv_bytes = chunk.to_csv(index=False).encode("utf-8")
            csha = hashlib.sha256(csv_bytes).hexdigest()
            chunk_shas.append(csha)
            out = ingest._stringify(chunk)
            out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = csha
            ok, _c, _r, _ = write_pandas(conn, out, table_name=stg, database=database,
                                         schema=schema, auto_create_table=True,
                                         overwrite=(n == 0), quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write_pandas failed on chunk {n + 1}")
            if n == 0:
                columns = list(out.columns)
            # Bounded leading-row sample for the density gate (the whole file is never
            # in memory; a parse failure is uniform, so the head is representative).
            if density_rows < ingest.DENSITY_SAMPLE_ROWS:
                take = out.head(ingest.DENSITY_SAMPLE_ROWS - density_rows)
                density_frames.append(take)
                density_rows += len(take)
            appended += len(chunk)
            n += 1
            print(f"    chunk {n}: +{len(chunk):,} (total {appended:,})", flush=True)
    except Exception as exc:
        # Mid-stream crash: every write went to STAGING, so the LIVE table is intact
        # by construction — drop the STAGING table ONLY. (The old code dropped the
        # LIVE table here: the catastrophic path where a failed NPPES re-land would
        # have deleted the surviving rows.) Log 'failed' so the crash leaves a trace.
        ended = ingest._utcnow()
        try:
            snow.execute(conn, f'DROP TABLE IF EXISTS "{database}"."{schema}"."{stg}"')
        except Exception:
            pass
        try:
            ingest._log_run(conn, sid, run_id, "failed", None, None, "", url, started, ended,
                            f"Chunked load failed after {appended:,} staged rows "
                            f"(staging {stg} dropped, live {table} UNTOUCHED): {exc}")
            exc._run_status_logged = True  # load_spec's outer catch must not re-log
        except Exception:
            pass
        raise

    if appended == 0:
        # Loudly fail an all-empty stream (bad URL / parse / over-aggressive filter)
        # rather than registering a 0-row source as a clean success. Chunk 0 never
        # wrote, so no staging table exists; load_spec's outer catch logs 'failed'.
        raise RuntimeError(
            f"chunked load produced 0 rows for {sid} (bad URL / parse / filter removed all?)")

    manifest = hashlib.sha256("".join(chunk_shas).encode()).hexdigest()
    ended = ingest._utcnow()
    # DENSITY GATE on the STAGED rows: an empty/parse-failure stream is logged
    # STATUS='empty', staging is dropped, the LIVE table stays untouched, and
    # nothing is registered — the husk can't masquerade as a real source.
    if density_frames:
        density = ingest.assess_density(pd.concat(density_frames, ignore_index=True))
    else:
        density = ingest.assess_density(pd.DataFrame(columns=list(columns) or ["COL"]))
    if density["empty"]:
        snow.execute(conn, f'DROP TABLE IF EXISTS "{database}"."{schema}"."{stg}"')
        ingest._log_run(conn, sid, run_id, "empty", appended, None, manifest, url, started, ended,
                        f"EMPTY LOAD -- {density['reason']}. {ingest._density_note(density)}. "
                        f"Chunked-streamed {appended:,} rows into staging {stg} but the frame "
                        f"carries no real data; staging dropped, live {table} untouched, "
                        "NOT registered.")
        print(f"    EMPTY -- {density['reason']}; staging dropped, logged STATUS='empty', not registered.")
        return {"source_id": sid, "status": "empty", "rows": appended,
                "density": density["populated_fraction"]}

    # PRE-SWAP SCHEMA ASSERTION: never swap a staging table whose column set drifted
    # from the live table — the landed column names ARE the dbt/connect contract
    # (NPPES's 333 columns especially). The refusal leaves staging in place for
    # inspection (the next run's chunk-0 overwrite self-cleans it); pass
    # --allow-schema-change when the source genuinely evolved.
    live_cols = _table_columns(conn, database, schema, table)
    if live_cols is not None and not allow_schema_change:
        stg_cols = _table_columns(conn, database, schema, stg) or []
        if set(stg_cols) != set(live_cols):
            missing = sorted(set(live_cols) - set(stg_cols))[:8]
            added = sorted(set(stg_cols) - set(live_cols))[:8]
            raise RuntimeError(
                f"schema drift: staging {stg} has {len(stg_cols)} cols vs live {table} "
                f"{len(live_cols)} (missing={missing}, added={added}). REFUSING the swap "
                "— re-run with --allow-schema-change if the source genuinely changed shape.")

    atomic_load.execute_swap(conn, table, database=database, schema=schema)
    # 'success' is logged ONLY AFTER the swap returns: a success row must mean the
    # LIVE table actually holds this run's rows, never just a staged copy.
    ingest._log_run(conn, sid, run_id, "success", appended, None, manifest, url, started, ended,
                    f"{s.get('name', sid)}. Chunked LLM-free load of {appended:,} rows "
                    f"(staged + atomic swap). {ingest._density_note(density)}.")
    try:
        _register(conn, s)   # register LAST — data + success row already durable
    except Exception as exc:
        exc._run_status_logged = True  # run already logged 'success'; don't add 'failed'
        raise
    print(f"    LOADED {appended:,} rows (chunked, atomic swap) -> LIBRARY_RAW.LANDING.{table}")
    return {"source_id": sid, "status": "loaded", "rows": appended,
            "density": density["populated_fraction"]}


# --------------------------------------------------------------------------- #
def _run_one(s: dict, args) -> dict:
    """Load one spec, catching its own errors so one failure can't kill a batch."""
    try:
        return load_spec(s, do_run=args.run, force=args.force, refresh=args.refresh,
                         allow_schema_change=getattr(args, "allow_schema_change", False))
    except Exception as e:  # noqa: BLE001
        print(f"    [{s['source_id']}] ERROR: {str(e)[:160]}")
        return {"source_id": s["source_id"], "status": f"ERROR: {str(e)[:90]}"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free bulk loader for known bridge-fuel sources")
    ap.add_argument("--spec", help="source_id, comma-list of source_ids, or 'all'")
    ap.add_argument("--list", action="store_true", help="list known specs")
    ap.add_argument("--run", action="store_true", help="actually land (default previews)")
    ap.add_argument("--force", action="store_true", help="reload even if already landed")
    ap.add_argument("--refresh", action="store_true", help="re-fetch; skip if content sha unchanged")
    ap.add_argument("--allow-schema-change", action="store_true",
                    help="chunked loads: permit the staging->live swap when the column "
                         "set drifted from the live table (default REFUSES — the landed "
                         "column names are the dbt/connect contract)")
    ap.add_argument("--workers", type=int, default=1,
                    help="parallel loads (each gets its own Snowflake connection). The warehouse "
                         "runs concurrent COPYs at no extra credit cost — uptime is billed, not "
                         "queries — so N>1 is near-free speedup for a many-source backfill. Keep "
                         "modest (4-8): local download bandwidth + disk, not the warehouse, is the cap.")
    args = ap.parse_args(argv)

    try:
        specs = _load_specs()
    except Exception as e:  # noqa: BLE001
        print(f"(no bridge_fuel_specs module yet: {e})")
        specs = {}

    if args.list or not args.spec:
        print("Known specs:")
        for k, v in specs.items():
            print(f"  {k:36} keys={v.get('join_keys','')!r:24} {v.get('name','')[:50]}")
        return 0

    if args.spec == "all":
        targets = list(specs.values())
    else:                                   # single id or comma-separated list
        ids = [s.strip() for s in args.spec.split(",") if s.strip()]
        missing = [i for i in ids if i not in specs]
        if missing:
            raise SystemExit(f"unknown spec(s): {missing}. known: {list(specs)}")
        targets = [specs[i] for i in ids]

    workers = max(1, min(args.workers, len(targets)))
    if workers > 1:
        print(f"running {len(targets)} specs across {workers} workers "
              f"({'LANDING' if args.run else 'PREVIEW'})…")
        import concurrent.futures as cf
        with cf.ThreadPoolExecutor(max_workers=workers) as ex:
            results = list(ex.map(lambda s: _run_one(s, args), targets))
    else:
        results = [_run_one(s, args) for s in targets]

    landed = [r for r in results if r.get("status") == "loaded"]
    errored = [r for r in results if str(r.get("status", "")).startswith("ERROR")]
    print(f"\n{len(landed)}/{len(results)} loaded, {sum(r.get('rows', 0) for r in landed):,} rows."
          + (f" {len(errored)} errored: {[r['source_id'] for r in errored]}" if errored else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
