"""Regenerate the Warehouse Compass data files. No AI, no warehouse writes.

  outputs/catalog/er.json     tables, columns, verified key per column, timeline grain
                              (scripts/audit_catalog.py catalog, from the audit cache;
                              run `audit_catalog.py fetch` first for a fresh inventory)
  outputs/catalog/plain.json  the plain-English layer, from the dbt seed
                              library-onboarding/ripple_dbt/seeds/plain_english.csv

    python scripts/export_compass.py
    cd outputs/catalog && python -m http.server 8765   ->  /compass.html
"""
from __future__ import annotations

import collections
import csv
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEED = REPO / "library-onboarding" / "ripple_dbt" / "seeds" / "plain_english.csv"
OUT = REPO / "outputs" / "catalog"


def plain() -> dict:
    out: dict = collections.defaultdict(lambda: {"cols": {}})
    for r in csv.DictReader(open(SEED, encoding="utf-8")):
        t = out[r["table_name"]]
        if r["kind"] == "summary":
            t["summary"] = r["plain"]
        elif r["kind"] == "row":
            t["row"] = r["plain"]
        else:
            t["cols"][r["column_name"]] = r["plain"]
    return dict(out)


def main() -> int:
    subprocess.run([sys.executable, str(REPO / "scripts" / "audit_catalog.py"), "catalog"], check=True)
    p = plain()
    json.dump(p, open(OUT / "plain.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    n_cols = sum(len(t["cols"]) for t in p.values())
    print(f"plain.json: {len(p)} tables, {n_cols} columns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
