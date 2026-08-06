#!/usr/bin/env python3
"""Deterministic loader for the UN Security Council Consolidated Sanctions List.

One row = one individual or entity sanctioned under a UN Security Council regime
(DRC, ISIL/Al-Qaida, DPRK, etc). Small XML file, refreshed as designations change.
Individuals and entities are flattened to a single table with a RECORD_TYPE flag;
nested/multi-value fields (aliases, nationalities) are joined with "; ".

    python scripts/un_consolidated_sanctions_load.py          # preview
    python scripts/un_consolidated_sanctions_load.py --run     # land it
"""
from __future__ import annotations
import argparse, sys
import xml.etree.ElementTree as ET
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "intl_un_consolidated_sanctions"
TABLE = SID.upper()
URL = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"


def _flatten(el: ET.Element) -> dict:
    """One level of flattening: direct children become columns; children that
    repeat or have their own children get their text joined with '; '."""
    out: dict[str, str] = {}
    for child in el:
        tag = child.tag
        if list(child):  # has sub-children (e.g. NATIONALITY/VALUE, ALIAS_LIST)
            texts = [c.text.strip() for c in child.iter() if c.text and c.text.strip()]
            val = "; ".join(dict.fromkeys(texts))  # dedupe, keep order
        else:
            val = (child.text or "").strip()
        if tag in out:
            out[tag] = f"{out[tag]}; {val}" if val else out[tag]
        else:
            out[tag] = val
    return out


def _fetch_df() -> pd.DataFrame:
    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    rows = []
    for section, rtype in (("INDIVIDUALS", "INDIVIDUAL"), ("ENTITIES", "ENTITY")):
        sec = root.find(section)
        if sec is None:
            continue
        for rec in sec.findall(rtype):
            d = _flatten(rec)
            d["RECORD_TYPE"] = rtype
            rows.append(d)
    return pd.DataFrame(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== UN Security Council Consolidated Sanctions List ===", flush=True)
    df = _fetch_df()
    cfg = {
        "source_id": SID,
        "name": "UN Security Council Consolidated Sanctions List",
        "publisher": "United Nations Security Council",
        "url": "https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list",
        "description": "All individuals and entities sanctioned under active UN Security "
                       "Council sanctions regimes (DRC, ISIL/Al-Qaida, DPRK, etc), flattened "
                       "from the official XML consolidated list. RECORD_TYPE distinguishes "
                       "INDIVIDUAL vs ENTITY rows.",
        "jurisdiction": "international", "category": "Sanctions", "subcategory": "UN sanctions",
        "unit_of_observation": "one row = one sanctioned individual or entity",
        "geographic_scope": "Global", "access_method": "bulk_download", "format": "xml",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "as designations change",
        "volume": f"{len(df):,} rows", "license_terms": "UN public document",
        "join_keys": "DATAID, REFERENCE_NUMBER",
        "accountability_relevance": "Global sanctions/ban list; core entity-resolution spine "
                                    "source for 'banned but still operating' cross-checks.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/un_consolidated_sanctions_load.py (XML flatten, snapshot-replace).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
