"""Generate one non-destructive view per flagged LANDING table, exposing every
date/time column this session's inventory found alongside the original raw
columns. Mirrors library-onboarding/ripple_dbt/scripts/census/gen_time_views.py's
own reasoning: a view costs nothing to create, leaves the underlying table
untouched, and can be regenerated in seconds when a rule is corrected.

Inputs (both already on disk, both read-only here):
  reports/recon/date_cast_inventory_2026-09-03.csv   content_date / audit_num
  reports/recon/date_derive_rules_2026-09-03.csv      range / granularity / time_pair

Output, under library-onboarding/ripple_dbt/:
  models/landing_clean/landing_clean__<table_lower>.sql   one view per table
  models/landing_clean/_landing_clean__sources.yml         source decls this
                                                            layer needs that
                                                            don't exist yet

Every table keeps ITS raw source declaration wherever it already lives
(staging or marts sources.yml) -- this only adds declarations for the ~861
tables that had none. Read-only against the warehouse: this writes local
files only. No dbt run, no materialization, until that's explicitly asked for.
"""
from __future__ import annotations

import csv
import glob
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DBT = REPO / "library-onboarding" / "ripple_dbt"
INV_CSV = REPO / "reports" / "recon" / "date_cast_inventory_2026-09-03.csv"
DERIVE_CSV = REPO / "reports" / "recon" / "date_derive_rules_2026-09-03.csv"
OUT_DIR = DBT / "models" / "landing_clean"
SOURCES_YML = OUT_DIR / "_landing_clean__sources.yml"


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def alias(name: str) -> str:
    # column names can carry spaces, dots, question marks (e.g. CFPB's "Date received",
    # GLEIF's "Entity.EntityCreationDate") -- a bare alias needs a clean identifier, not
    # a straight lowercase of the raw name, or the compiler reads the dot/space as SQL syntax.
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    if not s or s[0].isdigit():
        s = "c_" + s
    return s


def find_declared_sources() -> set[str]:
    declared = set()
    for f in glob.glob(str(DBT / "models" / "**" / "*.yml"), recursive=True):
        if "target" in Path(f).parts:
            continue
        in_sources = False
        for line in Path(f).read_text(encoding="utf-8").splitlines():
            if re.match(r"^sources:\s*$", line):
                in_sources = True
            if in_sources and re.match(r"^\s{6}- name:\s*[A-Z0-9_]+\s*$", line):
                declared.add(line.split("name:", 1)[1].strip())
    return declared


# Known false positives from the content classifier -- logged in .claude/traps.md
# 2026-09-03. A column that looks like a date is not a date until checked: HUC8 is
# an 8-digit watershed ID that happens to parse as a valid ymd8 date.
EXCLUDE = {("FED_USGS_WBD_HUC8", "HUC8")}


def load_inventory():
    by_table = defaultdict(list)
    for r in csv.DictReader(open(INV_CSV, encoding="utf-8")):
        if (r["table"], r["column"]) in EXCLUDE:
            continue
        if r["bucket"] in ("content_date", "audit_num"):
            by_table[r["table"]].append(r)
    return by_table


def load_derive():
    by_table = defaultdict(list)
    for r in csv.DictReader(open(DERIVE_CSV, encoding="utf-8")):
        if r["rule"] in ("range", "granularity", "time_pair"):
            by_table[r["table"]].append(r)
    return by_table


def select_lines_for_table(table: str, inv_rows: list[dict], derive_rows: list[dict]) -> list[str]:
    lines = []
    for r in inv_rows:
        col, bucket, pattern, typ = r["column"], r["bucket"], r["pattern"], r["type"]
        a = f"{alias(col)}_clean_ts"
        if bucket == "audit_num":
            lines.append(f'    {{{{ landing_parse_audit_epoch(\'{q(col)}\') }}}} as {a},')
        else:
            lines.append(f'    {{{{ landing_parse_date(\'{q(col)}\', \'{pattern}\', \'{typ}\') }}}} as {a},')

    for r in derive_rows:
        col, rule, pattern, sibling = r["column"], r["rule"], r["pattern"], r["sibling"]
        if rule == "range":
            lines.append(f'    {{{{ landing_range_start(\'{q(col)}\', \'{pattern}\') }}}} as {alias(col)}_start,')
            lines.append(f'    {{{{ landing_range_end(\'{q(col)}\', \'{pattern}\') }}}} as {alias(col)}_end,')
        elif rule == "granularity":
            lines.append(f'    {{{{ landing_translate_granularity(\'{q(col)}\') }}}} as {alias(col)}_label,')
        elif rule == "time_pair":
            # pattern here holds the sibling's own bucket (native/content_date); rebuild its cast inline.
            sib_row = next((x for x in inv_rows if x["column"] == sibling), None)
            if sib_row and sib_row["bucket"] == "content_date":
                date_call = f"landing_parse_date('{q(sibling)}', '{sib_row['pattern']}', '{sib_row['type']}')"
            else:
                date_call = q(sibling)
            lines.append(
                f'    {{{{ landing_combine_time_date(\'{q(col)}\', {date_call}) }}}} as {alias(col)}_full_ts,'
            )
    return lines


def aliases_for_table(inv_rows: list[dict], derive_rows: list[dict]) -> list[str]:
    out = [f"{alias(r['column'])}_clean_ts" for r in inv_rows]
    for r in derive_rows:
        if r["rule"] == "range":
            out += [f"{alias(r['column'])}_start", f"{alias(r['column'])}_end"]
        elif r["rule"] == "granularity":
            out.append(f"{alias(r['column'])}_label")
        elif r["rule"] == "time_pair":
            out.append(f"{alias(r['column'])}_full_ts")
    return out


def load_raw_columns() -> dict[str, set[str]]:
    import json
    cols = {}
    for path in (REPO / "reports" / "recon" / "content" / "json").glob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        cols[doc.get("table", path.stem)] = set(doc.get("profile", {}).keys())
    return cols


def main():
    declared = find_declared_sources()
    inv = load_inventory()
    derive = load_derive()
    raw_columns = load_raw_columns()

    tables = sorted(set(inv) | set(derive))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUT_DIR.glob("landing_clean__*.sql"):
        stale.unlink()

    missing_sources = []
    written = 0
    collisions = []
    for table in tables:
        inv_rows = inv.get(table, [])
        derive_rows = derive.get(table, [])

        gen_aliases = aliases_for_table(inv_rows, derive_rows)
        raw_lower = {c.lower() for c in raw_columns.get(table, set())}
        seen = set()
        bad = False
        for a in gen_aliases:
            if a in seen or a in raw_lower:
                collisions.append((table, a))
                bad = True
            seen.add(a)
        if bad:
            continue

        select_lines = select_lines_for_table(table, inv_rows, derive_rows)
        if not select_lines:
            continue

        select_lines[-1] = select_lines[-1].rstrip(",")
        body = "\n".join(select_lines)
        model_name = table.lower()

        sql = f"""{{{{ config(materialized='view', schema='LANDING_CLEAN', alias='{table}') }}}}

-- GENERATED by scripts/gen_landing_date_views.py -- do not hand-edit.
-- Regenerate after any change to reports/recon/date_cast_inventory_*.csv or
-- reports/recon/date_derive_rules_*.csv.
--
-- Clean date/time columns for LIBRARY_RAW.LANDING.{table}, from the
-- 2026-09-03 warehouse-wide date/time inventory. Every original column
-- passes through untouched via source.*; the clean columns sit beside them.
-- See macros/landing_date_casts.sql for how each is built, and
-- macros/ripple_time.sql for the separate mart-level canonical-clock standard
-- this does not replace.

select
    source.*,
{body}
from {{{{ source('ripple_raw', '{table}') }}}} as source
"""
        (OUT_DIR / f"landing_clean__{model_name}.sql").write_text(sql, encoding="utf-8")
        written += 1

        if table not in declared:
            missing_sources.append(table)

    if missing_sources:
        yml_lines = [
            "version: 2",
            "",
            "sources:",
            "  - name: ripple_raw",
            "    database: LIBRARY_RAW",
            "    schema: LANDING",
            "    tables:",
        ]
        for t in sorted(missing_sources):
            yml_lines.append(f"      - name: {t}")
        SOURCES_YML.write_text("\n".join(yml_lines) + "\n", encoding="utf-8")

    print(f"tables with a view generated: {written}")
    print(f"of those, needed a new source declaration: {len(missing_sources)}")
    skipped = {t for t, _ in collisions}
    print(f"tables skipped for an alias collision: {len(skipped)}")
    for t, a in collisions[:20]:
        print(f"  {t}: {a}")
    print(f"output dir: {OUT_DIR}")


if __name__ == "__main__":
    main()
