#!/usr/bin/env python3
"""Deterministic (LLM-free) loader for the OFAC SDN sanctions list.

OFAC's SDN.csv is a legacy, HEADERLESS CSV: 12 fixed columns, the literal '-0-'
for empty, and a vessel's IMO number buried in the free-text REMARKS field
(e.g. "... IMO 9187629 ..."). The generic bridge_fuel_load can't handle that
shape (no header, key derived by regex), so this lands it directly — with the
SAME provenance stamps, INGEST_RUNS log, and SOURCE_REGISTRY upsert as every
other source (reusing library-onboarding/ingest.py + register.py).

A derived 7-digit IMO column is extracted from REMARKS so sanctioned vessels
join to FED_NOAA_AIS on IMO — the "sanctioned hull still broadcasting AIS" lead.
The full SDN list lands (individuals + entities + vessels); only vessel rows
carry an IMO. Entities/individuals are kept for future money-side name leads.

    python scripts/ofac_load.py            # preview (download + parse, no write)
    python scripts/ofac_load.py --run      # land into LIBRARY_RAW.LANDING.FED_OFAC_SDN
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
import uuid
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

import ingest        # noqa: E402  library-onboarding/ingest.py
import register      # noqa: E402  library-onboarding/register.py
import snow          # noqa: E402  library-onboarding/snow.py

SID = "fed_ofac_sdn"
TABLE = SID.upper()
SDN_URL = "https://sanctionslistservice.ofac.treas.gov/api/download/sdn.csv"
UA = {"User-Agent": "Mozilla/5.0 (ripple-ofac-loader)"}

# Fixed SDN.csv layout (no header row in the file).
COLS = ["ENT_NUM", "SDN_NAME", "SDN_TYPE", "PROGRAM", "TITLE", "CALL_SIGN",
        "VESS_TYPE", "TONNAGE", "GRT", "VESS_FLAG", "VESS_OWNER", "REMARKS"]


def _fetch(dest: Path) -> Path:
    with requests.get(SDN_URL, headers=UA, stream=True, timeout=180) as r:
        r.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    return dest


def _parse(path: Path) -> pd.DataFrame:
    # Raw mirror: every value as TEXT exactly as the source emits it (incl. OFAC's
    # '-0-' empty sentinel) — cleaning belongs in staging, not the raw layer. The
    # ONE added column is the derived IMO the spine needs (OFAC buries it in REMARKS).
    df = pd.read_csv(path, header=None, names=COLS, dtype=str, keep_default_na=False,
                     na_values=[], encoding="latin-1", engine="python", quotechar='"')
    df["IMO"] = df["REMARKS"].str.extract(r"IMO\s+(\d{7})", expand=False).fillna("")
    return df


def _register(conn) -> None:
    cfg = {
        "source_id": SID,
        "name": "OFAC Specially Designated Nationals (SDN) List",
        "publisher": "U.S. Treasury — Office of Foreign Assets Control",
        "url": "https://ofac.treasury.gov/specially-designated-nationals-and-blocked-persons-list-sdn-human-readable-lists",
        "description": "OFAC SDN sanctions list (individuals, entities, vessels). Vessel rows carry a derived 7-digit IMO.",
        "jurisdiction": "US",
        "category": "Sanctions",
        "subcategory": "Sanctions List",
        "unit_of_observation": "one row = one sanctioned party (individual / entity / vessel)",
        "geographic_scope": "Global",
        "access_method": "bulk",
        "format": "csv",
        "auth": {"type": "none"},
        "cost": "free",
        "update_cadence": "daily",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "IMO",
        "accountability_relevance": "Sanctioned vessels (IMO) join to FED_NOAA_AIS broadcasts — 'sanctioned hull still operating'. Sanctioned entities/individuals seed money-side name leads.",
        "priority_tier": "1",
        "landing_table": TABLE,
        "notes": "Loaded by scripts/ofac_load.py (LLM-free). SDN.csv is headerless; IMO regex-extracted from REMARKS.",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for the OFAC SDN list")
    ap.add_argument("--run", action="store_true", help="actually land (default previews)")
    args = ap.parse_args(argv)

    with tempfile.TemporaryDirectory(prefix="ofac_") as td:
        src = _fetch(Path(td) / "sdn.csv")
        df = _parse(src)

    vessels = int((df["IMO"] != "").sum())
    print(f"parsed {len(df):,} SDN rows x {len(df.columns)} cols; {vessels:,} carry an IMO")
    print("  SDN_TYPE breakdown:", df["SDN_TYPE"].replace("", "(entity)").value_counts().to_dict())
    print("  sample sanctioned vessels:")
    print(df[df["IMO"] != ""][["SDN_NAME", "PROGRAM", "VESS_FLAG", "IMO"]].head(6).to_string(index=False))

    df_bytes = ingest._df_bytes(df)
    sha = hashlib.sha256(df_bytes).hexdigest()

    if not args.run:
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = snow.connect()
    try:
        out = ingest._stringify(df)
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        try:
            ingest._load_landing(conn, out, TABLE, overwrite=True)
            ended = ingest._utcnow()
            ingest._log_run(conn, SID, run_id, "success", len(out), len(df_bytes), sha,
                            SDN_URL, started, ended,
                            f"OFAC SDN list. LLM-free load of {len(out):,} rows ({vessels:,} vessels w/ IMO).")
            _register(conn)
            print(f"\nLOADED {len(out):,} rows -> LIBRARY_RAW.LANDING.{TABLE}; registered INCLUDE=Y")
        except Exception as exc:
            ended = ingest._utcnow()
            try:
                ingest._log_run(conn, SID, run_id, "failed", None, None, "", SDN_URL,
                                started, ended, f"Load failed: {exc}")
            except Exception:
                pass
            raise
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
