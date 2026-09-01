"""Final retry -- fixes for OSHA (via DOL API), CourtListener (bad lines),
Google Polads (new URL).

    python scripts/tier1_bulk_retry2.py --run
"""
from __future__ import annotations

import argparse
import bz2
import hashlib
import io
import datetime as dt
import sys
import uuid
import zipfile
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
sys.path.insert(0, str(_REPO))
import _bulk_load_utils as bulk  # noqa: E402
from loadkit.archive import pick_member  # noqa: E402

USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


MANIFEST = [
    # --- OSHA via DOL enforcement data (new download mechanism) ---
    # DOL moved to requiring session cookies. Use their bulk data API instead.
    # https://enforcedata.dol.gov/views/data_summary.php shows the data is
    # available but download links route through Drupal. Alternative: OSHA ITA.
    {
        "table": "FED_DOL_OSHA_INSPECTIONS",
        "url": "https://www.osha.gov/sites/default/files/osha_inspection.csv",
        "description": "OSHA Inspections (osha.gov direct)",
        "format": "csv",
    },
    {
        "table": "FED_DOL_OSHA_VIOLATIONS",
        "url": "https://www.osha.gov/sites/default/files/osha_violation.csv",
        "description": "OSHA Violations (osha.gov direct)",
        "format": "csv",
    },
    {
        "table": "FED_DOL_OSHA_ACCIDENTS",
        "url": "https://www.osha.gov/sites/default/files/osha_accident.csv",
        "description": "OSHA Accidents (osha.gov direct)",
        "format": "csv",
    },
    {
        "table": "FED_DOL_WHD_WHISARD",
        "url": "https://enfxfr.dol.gov/data_catalog/WHD/whd_whisard.csv.zip",
        "description": "DOL WHD WHISARD (alternate endpoint)",
        "format": "zip_csv",
    },
    # --- CourtListener (fix: on_bad_lines='skip') ---
    {
        "table": "FED_COURTLISTENER_POSITIONS",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/people-db-positions-2026-06-30.csv.bz2",
        "description": "CourtListener judicial positions (Jun 2026, skip bad lines)",
        "format": "bz2_csv_permissive",
    },
    {
        "table": "FED_COURTLISTENER_FINANCIAL_DISCLOSURES",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/financial-disclosures-2026-06-30.csv.bz2",
        "description": "CourtListener financial disclosures (Jun 2026)",
        "format": "bz2_csv_permissive",
    },
    {
        "table": "FED_COURTLISTENER_INVESTMENTS",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/financial-disclosure-investments-2026-06-30.csv.bz2",
        "description": "CourtListener judge investments (Jun 2026)",
        "format": "bz2_csv_permissive",
    },
    # --- Google Political Ads (new URL from README) ---
    {
        "table": "FED_GOOGLE_POLADS_CREATIVE_STATS",
        "url": "https://storage.googleapis.com/political-csv/google-political-ads-transparency-bundle.zip",
        "description": "Google Political Ads (new URL, full bundle)",
        "format": "zip_multi_google",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _provenance(content: bytes):
    sha = hashlib.sha256(content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)
    return sha, run_id, started


def _stamp(df, sha, run_id, started):
    df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    return df


def _write(conn, df, tbl):
    from snowflake.connector.pandas_tools import write_pandas
    df.columns = [bulk.sf_col(c) for c in df.columns]
    ok, _c, _n, _ = write_pandas(
        conn, df, table_name=tbl,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    return len(df)


def load_csv(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    df = pd.read_csv(io.BytesIO(resp.content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace",
                     on_bad_lines="skip")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_zip_csv(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        # ONE member or entry["member"] pattern -- never largest-wins
        # (the EIA-860 multi-file truncation trap).
        chosen = pick_member(zf, pattern=entry.get("member"),
                             suffixes=(".csv", ".txt"))
        with zf.open(chosen) as f:
            content = f.read()
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace",
                     on_bad_lines="skip")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_bz2_csv_permissive(conn, entry, max_rows):
    """bz2 CSV with on_bad_lines='skip' for malformed rows."""
    resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    decompressed = bz2.decompress(resp.content)
    df = pd.read_csv(io.BytesIO(decompressed), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace",
                     on_bad_lines="skip")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_zip_multi_google(conn, entry, max_rows):
    """Google Political Ads -- load largest CSVs from bundle."""
    print("  Downloading Google Political Ads bundle...")
    resp = requests.get(entry["url"], timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    print(f"  Bundle size: {len(resp.content):,} bytes")
    sha, run_id, started = _provenance(resp.content)
    total = 0
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        all_files = zf.namelist()
        csv_files = [n for n in all_files
                     if n.lower().endswith('.csv') and '__MACOSX' not in n]
        print(f"  All files: {len(all_files)}, CSVs: {len(csv_files)}")
        if not csv_files:
            # Show all files for debugging
            for n in all_files[:20]:
                print(f"    {zf.getinfo(n).file_size:>10,} {n}")
            # Maybe nested zip?
            inner_zips = [n for n in all_files if n.lower().endswith('.zip')]
            if inner_zips:
                print(f"  Found inner ZIP: {inner_zips[0]}")
                with zf.open(inner_zips[0]) as inner_f:
                    inner_content = inner_f.read()
                with zipfile.ZipFile(io.BytesIO(inner_content)) as izf:
                    csv_files = [n for n in izf.namelist()
                                 if n.lower().endswith('.csv') and '__MACOSX' not in n]
                    print(f"  Inner CSVs: {len(csv_files)}")
                    # Deliberate multi-file load: top-8 by size, picks printed.
                    csv_files.sort(key=lambda n: izf.getinfo(n).file_size, reverse=True)  # archive-gate: allow
                    for name in csv_files[:8]:
                        stem = Path(name).stem.replace("google-political-ads-", "")
                        tbl = bulk.table_name("FED_GOOGLE_POLADS", stem)
                        try:
                            with izf.open(name) as f:
                                content = f.read()
                            df = pd.read_csv(io.BytesIO(content), dtype=str,
                                             nrows=max_rows + 1, low_memory=False,
                                             encoding_errors="replace")
                            if len(df) > max_rows:
                                raise RuntimeError(
                                    f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
                                    f"refusing to silently truncate. Pass a higher max_rows explicitly.")
                            if df.empty:
                                continue
                            df = _stamp(df, sha, run_id, started)
                            n = _write(conn, df, tbl)
                            print(f"    {tbl}: {n:,} rows")
                            total += n
                        except Exception as e:
                            print(f"    FAILED {tbl}: {str(e)[:100]}")
            return total

        # Deliberate multi-file load: top-8 by size, picks printed.
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)  # archive-gate: allow
        for name in csv_files[:8]:
            stem = Path(name).stem.replace("google-political-ads-", "")
            tbl = bulk.table_name("FED_GOOGLE_POLADS", stem)
            try:
                with zf.open(name) as f:
                    content = f.read()
                df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                                 low_memory=False, encoding_errors="replace")
                if len(df) > max_rows:
                    raise RuntimeError(
                        f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
                        f"refusing to silently truncate. Pass a higher max_rows explicitly.")
                if df.empty:
                    continue
                df = _stamp(df, sha, run_id, started)
                n = _write(conn, df, tbl)
                print(f"    {tbl}: {n:,} rows")
                total += n
            except Exception as e:
                print(f"    FAILED {tbl}: {str(e)[:100]}")
    return total


FORMAT_LOADERS = {
    "csv": load_csv,
    "zip_csv": load_zip_csv,
    "bz2_csv_permissive": load_bz2_csv_permissive,
    "zip_multi_google": load_zip_multi_google,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--max-rows", type=int, default=5_000_000)
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING\n")

    to_load = [e for e in MANIFEST if e["table"] not in loaded]
    print(f"{len(to_load)} datasets to retry\n")

    if not args.run:
        for i, e in enumerate(to_load, 1):
            print(f"  {i}. {e['table']:50s} [{e['format']}]")
            print(f"     {e['url'][:100]}")
        print("\n(add --run to execute)")
        return 0

    results = []
    for i, entry in enumerate(to_load, 1):
        print(f"\n[{i}/{len(to_load)}] {entry['table']}")
        print(f"  {entry['description']}")
        loader = FORMAT_LOADERS.get(entry["format"])
        try:
            n = loader(conn, entry, args.max_rows)
            print(f"  -> {n:,} rows loaded")
            if n > 0:
                # Quality gate + INGEST_RUNS row (this loader had no density/
                # regression check at all -- a load could log rows with every
                # column blank and nothing would catch it). No expected_min_rows
                # override: matches every other run_quality_gate() caller in
                # scripts/, which lean on the density + never-shrink-vs-last-run
                # checks rather than a hardcoded floor.
                passed, report = bulk.run_quality_gate(
                    conn, entry["table"], entry["table"], str(uuid.uuid4()),
                    row_count=n, source_url=entry["url"])
                if not passed:
                    print(f"  QUALITY GATE FAILED {entry['table']}: {report}")
                    results.append({"name": entry["table"],
                                     "error": f"DQ failed: {report}"[:200]})
                    continue
            results.append({"name": entry["table"], "rows": n})
        except Exception as e:
            print(f"  FAILED: {str(e)[:200]}")
            results.append({"name": entry["table"], "error": str(e)[:200]})

    ok = sum(1 for r in results if r.get("rows", 0) > 0)
    total = sum(r.get("rows", 0) for r in results)
    failed = [r for r in results if "error" in r]
    print(f"\n{'='*60}")
    print(f"DONE: {ok}/{len(to_load)} loaded, {total:,} total rows")
    if failed:
        print(f"\nStill failing ({len(failed)}):")
        for r in failed:
            print(f"  - {r['name']}: {r['error'][:80]}")
    print(f"{'='*60}")
    conn.close()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
