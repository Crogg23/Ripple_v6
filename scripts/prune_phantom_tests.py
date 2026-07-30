"""Remove column-level dbt tests that point at columns which do not exist.

The mart generator wrote schema.yml tests from guessed column names -- VOYAGE_ID where
the table has VOYAGEID, plus SETTLEMENT_SK / COMPANY_ID / PERSON_NAME / NACJD_ID that
exist nowhere. Those tests do not report as data failures; they error with
"invalid identifier", which reads like noise and is easy to ignore. The result is a
suite that looks like coverage but silently tests nothing on those columns.

This deletes only the offending `- name: <column>` blocks, scoped to the model they sit
under, so surrounding tests and comments survive. Verify with
scripts/audit_dbt_test_columns.py afterwards.

Usage: python scripts/prune_phantom_tests.py [--apply]
"""
import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models")

# file (relative to models/) -> {model name: [columns that do not exist]}
PHANTOM = {
    "staging/fed_bjs_data/schema.yml": {
        "criminal_justice__fed_bjs_data": [
            "access_level", "collection_name", "fips", "geographic_level", "nacjd_id"],
    },
    "staging/fed_fda_drug_enforcement/schema.yml": {
        "health__fed_fda_drug_enforcement": [
            "_ingested_at", "product_ndc", "source_id"],
    },
    "staging/fed_naag_multistate_settlements/schema.yml": {
        "legal_enforcement__fed_naag_multistate_settlements": [
            "company_id", "is_lead_state_row", "settlement_date", "settlement_sk",
            "state"],
    },
    "staging/fed_slavevoyages_intraamerican/schema.yml": {
        "historical_records__fed_slavevoyages_intraamerican": [
            "country", "country_of_departure", "date_of_departure", "person_name",
            "port_of_arrival", "port_of_departure", "source_id", "voyage_id",
            "year_of_departure"],
    },
}

NAME_RE = re.compile(r"^(\s*)-\s+name:\s*([A-Za-z0-9_\"']+)\s*$")


def indent_of(line):
    return len(line) - len(line.lstrip())


def prune(lines, model, columns):
    """Drop `- name: <col>` blocks for the given columns inside the given model."""
    wanted = {c.lower() for c in columns}
    out, i, removed = [], 0, []
    in_model = False
    model_indent = None
    while i < len(lines):
        line = lines[i]
        m = NAME_RE.match(line)
        if m:
            name = m.group(2).strip("\"'")
            ind = len(m.group(1))
            if name == model:
                in_model, model_indent = True, ind
                out.append(line)
                i += 1
                continue
            # a sibling entry at the model's own indent ends the model block
            if in_model and model_indent is not None and ind <= model_indent:
                in_model = False
            if in_model and name.lower() in wanted:
                # swallow this block: everything more-indented than the `- name:` line
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if nxt.strip() and indent_of(nxt) <= ind:
                        break
                    j += 1
                removed.append(name)
                i = j
                continue
        out.append(line)
        i += 1
    return out, removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total = 0
    for rel, models in sorted(PHANTOM.items()):
        path = os.path.join(MODELS, rel.replace("/", os.sep))
        if not os.path.exists(path):
            print(f"WARN  {rel} not found")
            continue
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        allremoved = []
        for model, columns in models.items():
            lines, removed = prune(lines, model, columns)
            allremoved += removed
            missing = sorted(set(c.lower() for c in columns) -
                             set(r.lower() for r in removed))
            if missing:
                print(f"WARN  {rel}: could not find blocks for {missing}")
        print(f"{rel}: removed {len(allremoved)} column blocks {sorted(allremoved)}")
        total += len(allremoved)
        if args.apply:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.writelines(lines)

    print(f"\n{total} phantom column blocks removed")
    if not args.apply:
        print("DRY RUN -- rerun with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
