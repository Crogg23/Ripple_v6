#!/usr/bin/env python3
"""Turn reports/untested_marts_probe_<date>.tsv into dbt tests.

UNIQUE  -> unique + not_null on that column
PAIR    -> dbt_utils.unique_combination_of_columns on the two
NOTNULL -> not_null on the most-filled column (only if it has 0 nulls)
A mart that already has a schema yml gets the test appended to its entry
(or a new column block); one without gets models/marts/<dir>/schema_<name>.yml.
Every test written is one the probe already saw pass live.
"""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parents[1]
DBT = REPO / "library-onboarding" / "ripple_dbt"
NOTE = "PROBED LIVE 2026-09-22 (scripts/probe_untested_marts.py)"

def main(tsv: str):
    m = json.loads((DBT / "target" / "manifest.json").read_text(encoding="utf-8"))
    byname = {v["name"]: v for v in m["nodes"].values() if v["resource_type"] == "model"}
    written, skipped = [], []
    for r in csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"):
        name, verdict, col = r["model"], r["verdict"], r["column"]
        if verdict not in ("UNIQUE", "PAIR", "NOTNULL"):
            skipped.append((name, verdict, col)); continue
        nulls = 0
        if ":" in col:
            col, n = col.split(":", 1); nulls = int(n.replace("nulls", ""))
        v = byname[name]
        cols = [c.lower() for c in col.split("|")]
        model_entry = {"name": name}
        if verdict == "PAIR":
            model_entry["tests"] = [{"dbt_utils.unique_combination_of_columns": {"arguments": {"combination_of_columns": cols}}}]
            model_entry["description"] = f"{NOTE}: row key is ({', '.join(cols)}), {int(r['rows']):,} rows."
        else:
            tests = ["unique", "not_null"] if verdict == "UNIQUE" else ["not_null"]
            why = "row key" if verdict == "UNIQUE" else "no unique column or pair; a filled column"
            if nulls:
                tests = [{"not_null": {"config": {"warn_if": f">{nulls}", "error_if": f">{max(nulls + 1, int(nulls * 1.5))}"}}}]
                why = f"{nulls} null in source, measured 2026-09-22; threshold, fails above {max(nulls + 1, int(nulls * 1.5))}"
            model_entry["columns"] = [{"name": cols[0], "description": f"{NOTE}: {why}, {int(r['rows']):,} rows.", "tests": tests}]
        patch = v.get("patch_path")
        if patch:
            # an existing yml has comments a re-dump would erase: print the block, add by hand
            print("MANUAL", name, patch); print(yaml.safe_dump(model_entry, sort_keys=False, width=120))
            skipped.append((name, verdict, col)); continue
        else:
            p = DBT / Path(v["original_file_path"]).parent / f"schema_{name.split('__', 1)[1]}.yml"
            doc = {"version": 2, "models": [model_entry]}
        p.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
        written.append((name, verdict, col, str(p.relative_to(DBT))))
    for w in written: print("WROTE", *w)
    for s in skipped: print("SKIP ", *s)
    print(f"{len(written)} written, {len(skipped)} skipped")

if __name__ == "__main__":
    main(sys.argv[1])
