#!/usr/bin/env python3
"""Deterministic loader for the Missouri State Highway Patrol Sex Offender Registry.

One row = one registered offender's offense record (a person with N offenses
appears N times; the file's own `Count` column tells you how many offenses that
person has on file). Columns: name, current address/city/state/zip/county,
offense description, offense count, compliance status, tier, date of birth.
This is a public government safety-notification record (RSMo 589.400-425 and
43.650) -- the same legal category as the ~200 other named-individual
public-record sources already landed in this warehouse (SAM exclusions, OFAC
SDN, etc.), not a new category of sensitivity for this platform. Human sign-off
still gates anything before it is ever published anywhere.

Chris explicitly authorized loading sex-offender registry data on 2026-08-05
(CHRIS_DECISIONS.md, "R2. Sex-offender registries -- DONE, explicit yes given
in chat").

SCOPE, stated plainly: this is Missouri only, not a nationwide registry. There
is no nationwide bulk source -- NSOPW (the federal registry site) is
search-only by its own FAQ, with no bulk export or API, and no free/public
aggregator republishes all 50 state registries in bulk. Missouri is the clean,
immediately-buildable case: one anonymous HTTPS GET of a static ZIP, no login,
no CAPTCHA. Confirmed live 2026-08-05: report date embedded in the file itself
read 08/05/2026, same day as this build. Other states checked and found NOT
scriptable right now: Texas (bulk file exists but sits behind a login wall --
would need Chris to create a "TxDPS Public Website Account" and hand off
credentials), Florida (bulk CSVs exist but the download form requires solving a
CAPTCHA on every request), California and New York (individual-name-search
only, no bulk export exists at all), Hawaii (real bulk API, but costs $100 per
download -- a real-money call for Chris, not built here). Each of those is a
separate follow-up, not part of this loader.

The source ZIP bundles 4 files; this loader lands ONLY the main registry
(msor.xlsx -- the one with the Name/Address/City/St/Zip/County/Offense/Count/
Compliant/Tier/DOB columns below). Not loaded here, left as a documented
follow-up: msor_alias.xlsx (name aliases per offender), msor_offense.xlsx
(offense-level detail incl. conviction/confinement/parole dates and victim
age/gender), msor_veh.xls (registered vehicle info -- despite the .xls
extension this file is actually HTML-formatted, so it needs a different parser
than the other three true .xlsx files).

The main registry sheet has a 14-row title/report-summary header block before
the real table starts (row 14, 0-indexed 13, is the header row) -- verified by
downloading and reading the actual file, not assumed from the extension.

    python scripts/mo_sex_offender_registry_load.py          # preview
    python scripts/mo_sex_offender_registry_load.py --run     # land it
"""
from __future__ import annotations
import argparse, io, sys, zipfile
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "state_mo_sex_offender_registry"
TABLE = SID.upper()
URL = "https://www.mshp.dps.missouri.gov/MSHPWeb/PatrolDivisions/CRID/SOR/msor.zip"
MEMBER = "msor.xlsx"
HEADER_ROW = 13  # 0-indexed; rows 0-12 are a title/report-summary block, row 13 is the header


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== Missouri Sex Offender Registry (state MSHP, main registry only) ===", flush=True)
    r = requests.get(URL, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    raw = zf.read(MEMBER)
    df = pd.read_excel(io.BytesIO(raw), header=HEADER_ROW)
    cfg = {
        "source_id": SID,
        "name": "Missouri Sex Offender Registry",
        "publisher": "Missouri State Highway Patrol (MSHP)",
        "url": "https://www.mshp.dps.missouri.gov/MSHPWeb/PatrolDivisions/CRID/SOR/SORPage.html",
        "description": "State sex offender registry: one row per registered offender's "
                       "offense record (name, current address/city/state/zip/county, "
                       "offense description, offense count, compliance status, tier, DOB). "
                       "Public safety-notification record per RSMo 589.400-425 and 43.650.",
        "jurisdiction": "state:MO", "category": "Justice", "subcategory": "Sex offender registry",
        "unit_of_observation": "one row = one registered offender's offense record",
        "geographic_scope": "Missouri", "access_method": "bulk_download", "format": "xlsx (in zip)",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily (report-dated)",
        "volume": f"{len(df):,} rows", "license_terms": "Missouri public record (RSMo 589.400-425, 43.650)",
        "join_keys": "name+dob (no state-issued person ID in this file)",
        "accountability_relevance": "Named-individual public safety record; first state loaded "
                                    "in this category. No nationwide bulk source exists (NSOPW "
                                    "is search-only) -- other states are separate follow-ups, "
                                    "documented in this script's docstring.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/mo_sex_offender_registry_load.py (snapshot-replace). "
                "Source ZIP also contains msor_alias.xlsx, msor_offense.xlsx (offense-level "
                "detail incl. conviction/victim info), msor_veh.xls (HTML despite extension) "
                "-- none loaded yet, real follow-up work.",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
