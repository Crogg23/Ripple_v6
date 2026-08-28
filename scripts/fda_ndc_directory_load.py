#!/usr/bin/env python3
"""Deterministic loader for the FDA National Drug Code (NDC) Directory.

One row = one drug product (finished + unfinished listed drugs) with its
NDC product code, proprietary/nonproprietary names, labeler, application
number, substance and DEA schedule. Source: FDA's daily-refreshed
ndctext.zip bulk file; product.txt is the directory proper (package.txt is
the per-package roll-down and is not landed here).

    python scripts/fda_ndc_directory_load.py          # preview
    python scripts/fda_ndc_directory_load.py --run    # land it
"""
from __future__ import annotations
import argparse, io, sys, zipfile
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_fda_ndc_directory"
TABLE = SID.upper()
URL = "https://www.accessdata.fda.gov/cder/ndctext.zip"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== FDA NDC Directory (product file) ===", flush=True)
    r = requests.get(URL, timeout=300,
                     headers={"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"})
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        with zf.open("product.txt") as f:
            # Tab-delimited, cp1252-ish characters in drug names; all text.
            df = pd.read_csv(f, sep="\t", dtype=str, low_memory=False,
                             encoding="cp1252", encoding_errors="replace")
    cfg = {
        "source_id": SID,
        "name": "FDA National Drug Code (NDC) Directory",
        "publisher": "U.S. Food and Drug Administration (FDA)",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory",
        "description": "All listed drug products with NDC product code, proprietary and "
                       "nonproprietary names, dosage form/route, marketing category, FDA "
                       "application number, labeler name, active substances and DEA schedule.",
        "jurisdiction": "federal", "category": "Health", "subcategory": "Drugs",
        "unit_of_observation": "one row = one listed drug product (PRODUCTNDC)",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily full replacement",
        "volume": f"{len(df):,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "PRODUCTNDC, APPLICATIONNUMBER, LABELERNAME, SUBSTANCENAME",
        "accountability_relevance": "The NDC spine key: bridges FAERS adverse events, drug "
                                    "spending (Medicare Part D), ARCOS and recall data to a "
                                    "named product and labeler.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/fda_ndc_directory_load.py (snapshot-replace of "
                 "product.txt inside FDA's ndctext.zip).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
