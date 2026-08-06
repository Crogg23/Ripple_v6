#!/usr/bin/env python3
"""Deterministic loader for ICE PERSON-LEVEL detention records: Detention Stints + Detainers.

Chris explicitly authorized loading this. See CHRIS_DECISIONS.md, "R1. ICE person-level
detention data -- DONE, explicit yes given in chat" (confirmed 2026-08-05 after two
rounds of clarification). This is the person-level half that scripts/ice_facility_codes_load.py
deliberately left RED-gated -- that script only loads the facility reference table (code,
name, address, lat/long -- no people). This script loads the actual person-level records.

SOURCE: Deportation Data Project (DDP) -- deportationdata.org, github.com/deportationdata/ice.
DDP is run by researchers at UC Berkeley School of Law and Stanford Law School, publishing
FOIA-obtained ICE datasets used by journalists/researchers (TRAC, Vera Institute, etc.). DDP's
own R processing scripts (code/detention-stints-latest.R, code/detainers-latest.R) write their
final cleaned output to exactly the two parquet files this loader fetches -- confirmed by
reading those scripts directly. License is CC0 (no rights reserved).

Two tables:
  fed_ice_detention_stints -- one row = one detention STINT (a continuous stay at one
      facility; a person transferred between facilities has multiple stints). ~2.6M rows.
  fed_ice_detainers        -- one row = one DETAINER ICE lodged against a person (a request
      that a jail/prison hold someone past their release date for ICE pickup). ~610K rows.

DE-IDENTIFICATION (verified against the live schema at build time, not assumed): NEITHER
file carries a name, street address, SSN, full date-of-birth, or raw/plaintext A-number.
Individuals link across rows only via `unique_identifier`, which DDP's own codebook defines
verbatim as "Anonymized unique individual identifier based on Alien Registration Number
(A-number)" -- a hashed/recoded derivative, not the real A-number -- plus `birth_year` only
(never full DOB). DDP's "fields in previous releases" table lists a `Name` field that existed
in an earlier ICE release and has since been dropped; DDP does tighten identifiers over time,
so a future re-run of this loader should re-check the live column list rather than assume it
never changes. Even de-identified, this is still sensitive government microdata about real
people (demographics, criminal-charge fields, detention dates/facilities) -- combined with
public facility+date info it could in principle narrow to a small population in an edge case
(classic quasi-identifier risk with government microdata). Not a reason to block the load --
DDP itself publishes this openly under CC0 for exactly this kind of research use -- but worth
keeping in mind if any downstream output ever gets close to describing one specific record.

FETCH GOTCHA: these files are Git-LFS objects on GitHub. The plain raw.githubusercontent.com
host (used by ice_facility_codes_load.py for its plain, non-LFS CSV) returns only a 133-byte
LFS pointer STUB for these -- not the data. Must fetch from media.githubusercontent.com/media/...
instead. This loader verifies the download is real (parquet magic bytes "PAR1", not a pointer
stub or HTML error page) before ever handing it to pandas, so a silently-broken fetch fails
loud instead of landing garbage.

Files are big (241 MB stints, 23 MB detainers) so this streams to a temp file on disk and reads
with pd.read_parquet, rather than assuming an in-memory grab like the small facility CSV.

A third DDP file at the same path pattern, detention-stays-latest.parquet (individual-level,
DDP's own recommended table for person-level -- as opposed to stints' facility-transfer-level --
analysis), was NOT requested and is NOT loaded by this script. Flagging it here as a same-effort
follow-up opportunity sitting at the same URL pattern, not building it without a separate go-ahead.

    python scripts/ice_detention_records_load.py --source stints              # preview
    python scripts/ice_detention_records_load.py --source detainers           # preview
    python scripts/ice_detention_records_load.py --source stints --run        # land it
    python scripts/ice_detention_records_load.py --source detainers --run     # land it
    python scripts/ice_detention_records_load.py --source all --run          # both
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

UA = {"User-Agent": "Mozilla/5.0 (ripple-ice-detention-loader; w.rogers9999@gmail.com)"}

_BASE = "https://media.githubusercontent.com/media/deportationdata/ice/main/data"

SOURCES = {
    "stints": {
        "sid": "fed_ice_detention_stints",
        "url": f"{_BASE}/detention-stints-latest.parquet",
        "name": "ICE Detention Stints (person-level)",
        "unit_of_observation": (
            "one row = one detention stint (a continuous stay at one ICE facility; a "
            "single person's detention can span multiple stints if transferred between "
            "facilities, linked via unique_identifier + stint_ID/stay_ID)"
        ),
        "description": (
            "Person-level ICE detention records at the facility-STAY grain: book-in/book-out "
            "timestamps, detention facility + code, release reason, case status/category, "
            "criminal-charge fields (msc_charge, felon flag, sentence), bond posted date/amount, "
            "final order date, departed date/country, demographics (gender, race, ethnicity, "
            "marital status, religion, birth_country, citizenship_country, birth_year -- no full "
            "DOB). De-identified at the case level: no name, no street address, no SSN, no raw "
            "A-number. Individuals link across rows only via unique_identifier, which DDP's "
            "codebook defines as an anonymized/hashed derivative of the ICE Alien Registration "
            "Number (A-number)."
        ),
        "accountability_relevance": (
            "The core dataset for mapping ICE detention patterns at person-level grain: which "
            "facilities hold people longest, release-reason patterns, criminal-charge severity "
            "vs. detention length, demographic skews -- without exposing who any specific person "
            "is. Joins to fed_ice_detention_facility_codes on detention_facility_code."
        ),
    },
    "detainers": {
        "sid": "fed_ice_detainers",
        "url": f"{_BASE}/detainers-latest.parquet",
        "name": "ICE Detainers (person-level)",
        "unit_of_observation": (
            "one row = one detainer ICE lodged against a person (a request that a jail/prison "
            "hold someone past their scheduled release for ICE pickup), linked across rows via "
            "unique_identifier"
        ),
        "description": (
            "Person-level ICE detainer records: detainer prepare date, detention facility + code, "
            "facility state/AOR/city, case status/category, apprehension method/date, entry "
            "status/date, most-serious-conviction charge + sentence, felon flag, final order "
            "date, departed date/country, port of departure, prior-felony flag, demographics "
            "(gender, birth_country, citizenship_country, birth_year -- no full DOB). "
            "De-identified at the case level: no name, no street address, no SSN, no raw "
            "A-number. Individuals link across rows only via unique_identifier, which DDP's "
            "codebook defines as an anonymized/hashed derivative of the ICE Alien Registration "
            "Number (A-number)."
        ),
        "accountability_relevance": (
            "Person-level detainer record: who ICE asked local jails to hold, on what charge "
            "basis, and what happened next (departed / final order) -- without exposing who any "
            "specific person is. Joins to fed_ice_detention_facility_codes on "
            "detention_facility_code."
        ),
    },
}


def _fetch_parquet(url: str, tmp_dir: Path) -> pd.DataFrame:
    """Stream a (possibly large) Git-LFS-backed parquet file to disk, then read it.

    Verifies parquet magic bytes before handing anything to pandas, so a silently-broken
    fetch (LFS pointer stub, HTML error page, truncated download) fails loud instead of
    landing garbage.
    """
    dest = tmp_dir / "src.parquet"
    with requests.get(url, headers=UA, stream=True, timeout=300) as r:
        r.raise_for_status()
        ctype = r.headers.get("Content-Type", "")
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    size = dest.stat().st_size
    with open(dest, "rb") as fh:
        magic = fh.read(4)
    if size < 1000 or magic != b"PAR1":
        head = dest.read_bytes()[:200]
        raise RuntimeError(
            f"download from {url} does not look like a real parquet file "
            f"(size={size} bytes, magic={magic!r}, Content-Type={ctype!r}). "
            f"First 200 bytes: {head!r}. Likely an LFS pointer stub (wrong host) or an "
            "HTML error page -- NOT landing this."
        )
    print(f"    downloaded {size:,} bytes, magic OK -- reading parquet", flush=True)
    return pd.read_parquet(dest, engine="pyarrow")


def _build_cfg(spec: dict, df: pd.DataFrame) -> dict:
    table = spec["sid"].upper()
    return {
        "source_id": spec["sid"],
        "name": spec["name"],
        "publisher": (
            "Deportation Data Project (UC Berkeley School of Law + Stanford Law School), "
            "based on FOIA-obtained U.S. Immigration and Customs Enforcement (ICE) records"
        ),
        "url": "https://github.com/deportationdata/ice",
        "description": spec["description"],
        "jurisdiction": "federal",
        "category": "Justice",
        "subcategory": "Immigration detention",
        "unit_of_observation": spec["unit_of_observation"],
        "geographic_scope": "United States",
        "access_method": "bulk_download",
        "format": "parquet",
        "auth": {"type": "none"},
        "cost": "free",
        "update_cadence": (
            "irregular -- DDP states verbatim 'ICE has not agreed to release these datasets "
            "on any schedule, so it is impossible to predict when...we will receive updates'"
        ),
        "volume": f"{len(df):,} rows",
        "license_terms": "CC0 (no rights reserved); FOIA-obtained public record data",
        "join_keys": (
            "unique_identifier (anonymized/hashed derivative of the ICE Alien Registration "
            "Number, per DDP's codebook -- links a person's records across rows without "
            "identifying them); detention_facility_code (joins to "
            "fed_ice_detention_facility_codes)"
        ),
        "accountability_relevance": spec["accountability_relevance"],
        "priority_tier": "1",
        "landing_table": table,
        "notes": (
            "Loaded by scripts/ice_detention_records_load.py (snapshot-replace). Person-level "
            "ICE detention data -- explicitly authorized by Chris in chat, twice, on 2026-08-05; "
            "see CHRIS_DECISIONS.md 'R1. ICE person-level detention data -- DONE, explicit yes "
            "given in chat'. Sibling facility reference table (codes/names/addresses only, no "
            "people) already landed separately as FED_ICE_DETENTION_FACILITY_CODES via "
            "scripts/ice_facility_codes_load.py. A third DDP file at the same URL pattern, "
            "detention-stays-latest.parquet (individual-level, DDP's own recommended table for "
            "person-level analysis), was NOT requested and is NOT loaded here -- flagged as a "
            "same-effort follow-up, not built without a separate go-ahead."
        ),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["stints", "detainers", "all"], default="all")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    targets = list(SOURCES) if args.source == "all" else [args.source]
    failed = []
    for key in targets:
        spec = SOURCES[key]
        print(f"\n=== {spec['name']} (person-level; Chris-authorized, CHRIS_DECISIONS.md R1) ===",
              flush=True)
        print(f"    fetching {spec['url']}", flush=True)
        with tempfile.TemporaryDirectory(prefix="ice_detention_") as td:
            df = _fetch_parquet(spec["url"], Path(td))
            cfg = _build_cfg(spec, df)
            table = spec["sid"].upper()
            status = load_and_register(df, spec["sid"], table, spec["url"], cfg, args.run)
            if status not in ("preview", "skipped", "success"):
                failed.append(f"{spec['sid']}={status}")
    if failed:
        print(f"\nFAILED (non-success status): {', '.join(failed)}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
