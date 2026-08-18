"""Build the staging-model -> raw-landing-table crosswalk by parsing each
staging model's source() reference out of its SQL. Pure local parse.

This is the first hard key in the parked source-registry reconciliation: it
joins the dbt staging layer to the raw landing tables by declared reference,
not by name guessing. Combined with Tier A catalog metadata it attaches a
measured row count to every staging model whose raw table exists.

Writes reports/census_grid_2026-08-12/fill/staging_to_raw.csv.
"""
import csv
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STAGING_GLOB = os.path.join(
    REPO, "library-onboarding", "ripple_dbt", "models", "staging", "**", "*.sql")
FILL = os.path.join(REPO, "reports", "census_grid_2026-08-12", "fill")

SOURCE_RE = re.compile(r"source\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)")


def main():
    raw = {}
    for r in csv.DictReader(open(os.path.join(FILL, "tier_a_tables.csv"), encoding="utf-8")):
        if r["database"] == "LIBRARY_RAW":
            raw[r["table"].upper()] = (r["row_count"], r["bytes"])

    out = os.path.join(FILL, "staging_to_raw.csv")
    n = hit = multi = 0
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["staging_model", "source_name", "raw_table", "raw_exists",
                    "raw_row_count", "raw_bytes"])
        for path in sorted(glob.glob(STAGING_GLOB, recursive=True)):
            model = os.path.splitext(os.path.basename(path))[0]
            sql = open(path, encoding="utf-8", errors="replace").read()
            refs = SOURCE_RE.findall(sql)
            n += 1
            if not refs:
                w.writerow([model, "", "", "NO_SOURCE_REF", "", ""])
                continue
            if len(set(refs)) > 1:
                multi += 1
            for src, tab in dict.fromkeys(refs):
                rc, by = raw.get(tab.upper(), ("", ""))
                exists = "yes" if tab.upper() in raw else "MISSING_IN_RAW"
                if exists == "yes":
                    hit += 1
                w.writerow([model, src, tab, exists, rc, by])
    print(f"staging models parsed: {n}; refs resolved to live raw tables: {hit}; "
          f"multi-source models: {multi}")
    print("wrote", out)


if __name__ == "__main__":
    main()
