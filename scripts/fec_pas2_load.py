#!/usr/bin/env python3
"""Load FEC pas2 -- committee->candidate contributions (+ coordinated/independent
expenditures), cycles 2024 + 2026. This is the PAC-money-to-member edge: each row
carries CMTE_ID (the donor committee) AND CAND_ID (the recipient candidate), so it
joins straight to the member spine via the existing fec_cand_id bridge.

Uses loadkit.fec_parse.parse_pipe -- a row with an embedded pipe in a free-text
field is QUARANTINED (not padded into the money columns), so no shifted figure can
land. Lands via the shared `land()` helper (TEXT mirror, provenance, density gate,
INGEST_RUNS log, snapshot-replace = idempotent).
"""
from __future__ import annotations

import io
import sys
import zipfile

import pandas as pd
import requests

sys.path.insert(0, r"c:\Code\Ripple_v6")
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
sys.path.insert(0, r"c:\Code\Ripple_v6\politics\loaders")

from dotenv import load_dotenv  # noqa: E402

load_dotenv(r"c:\Code\Ripple_v6\library-onboarding\.env", override=True)

from build_skeleton import land  # noqa: E402  (the shared first-class land helper)
from loadkit import fec_parse    # noqa: E402

# pas2 layout (22 cols) -- CAND_ID is at position 17, the direct candidate key.
PAS2_COLS = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM", "TRANSACTION_TP",
    "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE", "EMPLOYER", "OCCUPATION",
    "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID", "CAND_ID", "TRAN_ID", "FILE_NUM",
    "MEMO_CD", "MEMO_TEXT", "SUB_ID",
]
CYCLES = {"2024": "24", "2026": "26"}
SID = "fed_fec_committee_to_candidate"


def fetch(cycle: str, yy: str) -> pd.DataFrame:
    url = f"https://www.fec.gov/files/bulk-downloads/{cycle}/pas2{yy}.zip"  # 302 -> GovCloud, requests follows
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    name = [n for n in zf.namelist() if n.lower().endswith(".txt")][0]
    res = fec_parse.parse_pipe(zf.read(name), PAS2_COLS).require_clean(0.002)
    df = res.good
    df["CYCLE"] = cycle
    print(f"  pas2{yy}: {len(df):,} rows kept ({res.n_bad} quarantined)", flush=True)
    return df


def main() -> int:
    print(f"=== FEC pas2 (committee->candidate) cycles {'+'.join(CYCLES)} ===", flush=True)
    df = pd.concat([fetch(c, yy) for c, yy in CYCLES.items()], ignore_index=True)
    land(df, SID, "https://www.fec.gov/files/bulk-downloads/",
         "FEC pas2 committee->candidate contributions + IEs (cycles 2024+2026); one row = one transaction.")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
