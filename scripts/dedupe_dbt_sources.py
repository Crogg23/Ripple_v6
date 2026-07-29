"""Remove duplicate dbt source table declarations, keeping the canonical file.

Convention: staging/<source>/schema.yml is canonical for a landing table because
it is the per-source home and carries the data tests. Mart-level
_<domain>__sources.yml files re-declared the same tables, which is a fatal
dbt compilation error (not a warning).

Usage: python scripts/dedupe_dbt_sources.py [--apply]
"""
import argparse
import os
import re
import sys

DBT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "library-onboarding", "ripple_dbt", "models")

# (relative yml path, table name to remove)
REMOVALS = [
    # staging/<source>/schema.yml is canonical -> drop the mart-level redeclaration
    ("marts/finance/_finance__sources.yml", "FED_CFPB_COMPLAINTS"),
    ("marts/education/_education__sources.yml", "FED_ED_EDFACTS"),
    ("marts/immigration/_immigration__sources.yml", "FED_EOIR_CASE_DATA"),
    ("marts/environment/_environment__sources.yml", "FED_EPA_ECHO"),
    ("marts/housing/_housing__sources.yml", "FED_FHFA_NMDB"),
    ("marts/justice/_justice__sources.yml", "FED_MSHA_VIOLATIONS"),
    ("marts/transport/_transport__sources.yml", "FED_NHTSA_COMPLAINTS"),
    ("marts/review/_review__sources.yml", "FED_SAM_EXCLUSIONS"),
    ("marts/review/_review__sources.yml", "FED_SEC_EDGAR_FINANCIALS"),
    ("marts/history/_history__sources.yml", "FED_SLAVEVOYAGES_TRANSATLANTIC"),
    ("marts/science/_science__sources.yml", "FED_USGS_EARTHQUAKES"),
    ("marts/procurement/_procurement__sources.yml", "INTL_ADB_DATA"),
    ("marts/politics/_politics__sources.yml", "INTL_VOETEN_UNGA_VOTES"),
    ("marts/reference/_reference__sources.yml", "XC_OWID_FERTILITY"),
    ("marts/open_data/_open_data__sources.yml", "XC_WAYBACK_DOJ_EPSTEIN"),
    ("marts/investigations/_investigations__sources.yml",
     "XC_WAYBACK_REPLAY_DOJ_LISTING"),
    # declared in economics + health + staging -> staging wins, drop both marts
    ("marts/economics/_economics__sources.yml", "FED_FOREIGNASSISTANCE"),
    ("marts/health/_health__sources.yml", "FED_FOREIGNASSISTANCE"),
    # per-source staging dirs are canonical over the politics rollup file
    ("staging/politics/_politics__sources.yml", "FED_GOVINFO_BILLSTATUS"),
    ("staging/politics/_politics__sources.yml", "FED_GOVINFO_BILL_COSPONSORS"),
    ("staging/politics/_politics__sources.yml", "FED_VOTEVIEW_MEMBERS"),
    ("staging/politics/_politics__sources.yml", "FED_VOTEVIEW_ROLLCALLS"),
    ("staging/politics/_politics__sources.yml", "FED_VOTEVIEW_ROLLCALL_META"),
    # mart-vs-mart on a 178M-row source: HEALTH owns it
    ("marts/uncategorized/_uncategorized__sources.yml", "FED_DEA_ARCOS_FULL"),
]

ENTRY = re.compile(r"^(\s*)-\s+name:\s*([A-Za-z0-9_]+)\s*$")


def strip_table(lines, table):
    """Drop the `- name: <table>` block from a yml table list. Returns new lines."""
    start = indent = None
    for i, line in enumerate(lines):
        m = ENTRY.match(line)
        if m and m.group(2) == table:
            start, indent = i, len(m.group(1))
            break
    if start is None:
        return lines, False
    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if not line.strip():
            continue
        cur = len(line) - len(line.lstrip())
        if cur <= indent:
            end = j
            break
    return lines[:start] + lines[end:], True


def remaining_tables(lines):
    """Count `- name:` entries that sit under a `tables:` key."""
    in_tables = False
    tables_indent = None
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped == "tables:":
            in_tables = True
            tables_indent = len(line) - len(line.lstrip())
            continue
        if in_tables:
            if not stripped:
                continue
            cur = len(line) - len(line.lstrip())
            if cur <= tables_indent and not stripped.startswith("-"):
                in_tables = False
                continue
            if ENTRY.match(line):
                count += 1
    return count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    by_file = {}
    for rel, table in REMOVALS:
        by_file.setdefault(rel, []).append(table)

    missing, changed, emptied = [], [], []
    for rel, tables in sorted(by_file.items()):
        path = os.path.join(DBT, rel.replace("/", os.sep))
        if not os.path.exists(path):
            missing.append(f"{rel} (file not found)")
            continue
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        for table in tables:
            lines, ok = strip_table(lines, table)
            if ok:
                changed.append(f"{rel}: removed {table}")
            else:
                missing.append(f"{rel}: {table} not found")
        if remaining_tables(lines) == 0:
            emptied.append(rel)
            if args.apply:
                os.remove(path)
            continue
        if args.apply:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.writelines(lines)

    for msg in changed:
        print("OK   ", msg)
    for rel in emptied:
        print("EMPTY", f"{rel} -> source list now empty, file deleted")
    for msg in missing:
        print("WARN ", msg)
    print(f"\n{len(changed)} removals, {len(emptied)} files deleted, "
          f"{len(missing)} warnings")
    if not args.apply:
        print("DRY RUN -- rerun with --apply to write changes")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
