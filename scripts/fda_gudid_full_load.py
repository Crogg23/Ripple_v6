"""Load the AccessGUDID Delimited Full Release (device registry, ~4M devices).

Lands two tables (all columns VARCHAR, raw landing, no dedup):
  FED_FDA_GUDID_FULL_DEVICE       <- device.txt       (one row per device version)
  FED_FDA_GUDID_FULL_IDENTIFIERS  <- identifiers.txt  (one row per device identifier)

Existing FED_FDA_GUDID (2,542-row stub) is left untouched.
Pattern copied from scripts/fda_faers_load.py: explicit VARCHAR landing DDL,
write_pandas append, NaN->None, checkpoint per member file for resume,
quality gate + INGEST_RUNS logging, SOURCE_REGISTRY registration.

    python scripts/fda_gudid_full_load.py --run [--url <full-release-zip-url>]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
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
import _bulk_load_utils as bulk  # noqa: E402
from bridge_fuel_load import _register  # noqa: E402

USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
CHECKPOINT = _REPO / "logs" / "gudid_full_checkpoint.json"
DEFAULT_URL = ("https://accessgudid.nlm.nih.gov/release_files/download/"
               "AccessGUDID_Delimited_Full_Release_20260803.zip")
CHUNK_ROWS = 250_000

# zip member basename (case-insensitive, any folder) -> (table, source_id)
TARGETS = {
    "device.txt": ("FED_FDA_GUDID_FULL_DEVICE", "fed_fda_gudid_full_device"),
    "identifiers.txt": ("FED_FDA_GUDID_FULL_IDENTIFIERS", "fed_fda_gudid_full_identifiers"),
}

SPECS = {
    "fed_fda_gudid_full_device": {
        "source_id": "FED_FDA_GUDID_FULL_DEVICE",
        "name": "AccessGUDID Full Release -- device master (delimited)",
        "publisher": "FDA / NLM (AccessGUDID)",
        "url": DEFAULT_URL,
        "description": ("Full GUDID device registry -- one row per device record: "
                        "brand, company, model/version, device class flags. "
                        "Pipe-delimited full release, all columns text."),
        "category": "Health", "subcategory": "device_safety",
        "unit_of_observation": "one row = one GUDID device record",
        "format": "psv", "update_cadence": "monthly",
        "join_keys": "PrimaryDI; companyName; brandName",
        "accountability_relevance": ("The who-makes-which-device backbone; joins device "
                                     "adverse events and recalls to manufacturers."),
    },
    "fed_fda_gudid_full_identifiers": {
        "source_id": "FED_FDA_GUDID_FULL_IDENTIFIERS",
        "name": "AccessGUDID Full Release -- device identifiers (delimited)",
        "publisher": "FDA / NLM (AccessGUDID)",
        "url": DEFAULT_URL,
        "description": ("All device identifiers (DIs) per GUDID device record, incl. "
                        "primary/secondary/package DIs. Pipe-delimited, all text."),
        "category": "Health", "subcategory": "device_safety",
        "unit_of_observation": "one row = one device identifier",
        "format": "psv", "update_cadence": "monthly",
        "join_keys": "PrimaryDI; deviceId",
        "accountability_relevance": ("Identifier crosswalk for the GUDID device master; "
                                     "the join spine for UDI-keyed sources."),
    },
}


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        try:
            return json.loads(CHECKPOINT.read_text())
        except Exception:
            return {}
    return {}


def save_checkpoint(cp: dict):
    CHECKPOINT.parent.mkdir(exist_ok=True)
    CHECKPOINT.write_text(json.dumps(cp, indent=1))


def download(url: str, dest: Path) -> str:
    """Stream-download the zip; returns sha256. Reuses an existing complete file."""
    sha_file = dest.with_suffix(".sha256")
    if dest.exists() and sha_file.exists():
        print(f"reusing downloaded {dest} ({dest.stat().st_size:,} bytes)")
        return sha_file.read_text().strip()
    h = hashlib.sha256()
    tmp = dest.with_suffix(".part")
    with requests.get(url, stream=True, timeout=1800, headers=USER_AGENT) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    f.write(chunk)
                    h.update(chunk)
    tmp.replace(dest)
    sha = h.hexdigest()
    sha_file.write_text(sha)
    print(f"downloaded {dest.stat().st_size:,} bytes  sha={sha[:12]}")
    return sha


def ensure_table(conn, tbl: str, cols: list[str], existing: dict[str, set]) -> None:
    cur = conn.cursor()
    if tbl not in existing:
        cur.execute(f"SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
        existing[tbl] = {r[0] for r in cur.fetchall()}
    if not existing[tbl]:
        meta = (f", {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR")
        cur.execute(f'CREATE TABLE {bulk.LANDING_FQS}."{tbl}" '
                    f'({", ".join(c + " VARCHAR" for c in cols)}{meta})')
        existing[tbl] = set(cols) | {bulk.META_INGESTED_AT, bulk.META_SOURCE_RUN_ID,
                                     bulk.META_SRC_SHA256}
    else:
        for c in cols:
            if c not in existing[tbl]:
                cur.execute(f'ALTER TABLE {bulk.LANDING_FQS}."{tbl}" ADD COLUMN {c} VARCHAR')
                existing[tbl].add(c)


def load_member(conn, zf: zipfile.ZipFile, member: str, tbl: str,
                sha: str, run_id: str, existing: dict[str, set]) -> int:
    from snowflake.connector.pandas_tools import write_pandas
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    total = 0
    with zf.open(member) as f:
        reader = pd.read_csv(f, sep="|", dtype=str, chunksize=CHUNK_ROWS,
                             low_memory=False, encoding_errors="replace",
                             on_bad_lines="skip", index_col=False, quoting=3)
        for df in reader:
            df.columns = [bulk.sf_col(c) for c in df.columns]
            ensure_table(conn, tbl, list(df.columns), existing)
            df = df.astype(object).where(df.notna(), None)
            df[bulk.META_INGESTED_AT] = started
            df[bulk.META_SOURCE_RUN_ID] = run_id
            df[bulk.META_SRC_SHA256] = sha
            ok, _c, _n, _ = write_pandas(
                conn, df, table_name=tbl,
                database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                auto_create_table=False, overwrite=False,
                quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write_pandas failed {tbl}")
            total += len(df)
            print(f"  [{tbl}] {total:,} rows so far", flush=True)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--url", default=DEFAULT_URL)
    args = ap.parse_args()
    if not args.run:
        print("preview only; add --run")
        return

    dest = _REPO / "logs" / "gudid_full_release.zip"
    sha = download(args.url, dest)
    cp = load_checkpoint()
    conn = snow.connect()
    existing: dict[str, set] = {}
    gate_failed = []
    try:
        with zipfile.ZipFile(dest) as zf:
            names = {Path(n).name.lower(): n for n in zf.namelist()}
            for base, (tbl, sid) in TARGETS.items():
                if base not in names:
                    raise RuntimeError(f"member {base} not found in zip: {sorted(names)[:20]}")
                if cp.get(tbl, {}).get("sha") == sha:
                    print(f"[{tbl}] already loaded for this release -- skipping")
                    continue
                run_id = str(uuid.uuid4())
                n = load_member(conn, zf, names[base], tbl, sha, run_id, existing)
                print(f"[{tbl}] loaded {n:,} rows")
                passed, report = bulk.run_quality_gate(
                    conn, sid, tbl, run_id, sha256=sha, row_count=n,
                    source_url=args.url, file_bytes=dest.stat().st_size)
                if not passed:
                    gate_failed.append(tbl)
                _register(conn, SPECS[sid])
                cp[tbl] = {"sha": sha, "rows": n,
                           "at": dt.datetime.now(dt.timezone.utc).isoformat()}
                save_checkpoint(cp)
    finally:
        conn.close()
    if gate_failed:
        print(f"QUALITY GATE FAILED: {gate_failed}")
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
