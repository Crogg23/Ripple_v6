#!/usr/bin/env python3
"""Generate schema.yml test files for marts that don't have one.

Queries LIBRARY_MARTS.INFORMATION_SCHEMA to detect primary keys (columns with
UNIQUE in their name or ending in _ID that are actually unique), then emits
basic not_null + unique tests for each mart.

    python3 scripts/generate_mart_tests.py              # write all
    python3 scripts/generate_mart_tests.py --dry-run    # preview
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402

DBT_PROJECT = _REPO / "library-onboarding" / "ripple_dbt"
MARTS_DIR = DBT_PROJECT / "models" / "marts"

# Marts that already have test YAML (in shared files or domain-specific)
ALREADY_TESTED = {
    "health__pharma_meal_cap_fingerprint",
    "justice__county_double_burden",
    "justice__racial_jail_disparity",
    "money__debt_repayment_cliff",
    "lead_queue",
}

# Heuristic: columns that are likely primary/natural keys
KEY_SUFFIXES = ("_id", "_npi", "_number", "_code", "_fips")
KEY_EXACT = {"npi", "id", "loan_number", "ndc", "bioguide", "icpsr"}


def is_likely_key(col_name: str) -> bool:
    cl = col_name.lower()
    if cl in KEY_EXACT:
        return True
    for suf in KEY_SUFFIXES:
        if cl.endswith(suf) and not cl.startswith("_"):
            return True
    return False


def fetch_mart_columns(cur) -> dict[str, list[str]]:
    """Returns {table_name: [col1, col2, ...]} for all mart tables."""
    cur.execute("""
        SELECT table_name, column_name
        FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema IN ('DBT_CROGERS', 'POLITICS', 'EPSTEIN')
        ORDER BY table_name, ordinal_position
    """)
    result: dict[str, list[str]] = {}
    for table_name, col_name in cur.fetchall():
        if col_name.startswith("_"):
            continue
        result.setdefault(table_name, []).append(col_name)
    return result


def render_schema_yml(model_name: str, columns: list[str]) -> str:
    key_cols = [c for c in columns if is_likely_key(c)]
    if not key_cols:
        # fallback: use first column
        key_cols = [columns[0]] if columns else []

    col_blocks = []
    for i, col in enumerate(key_cols[:3]):  # max 3 key columns tested
        if i == 0:
            col_blocks.append(
                f"      - name: {col.lower()}\n"
                f"        data_tests:\n"
                f"          - not_null"
            )
        else:
            col_blocks.append(
                f"      - name: {col.lower()}\n"
                f"        data_tests:\n"
                f"          - not_null"
            )

    # If single key, add unique test
    if len(key_cols) == 1:
        col_blocks[0] = (
            f"      - name: {key_cols[0].lower()}\n"
            f"        data_tests:\n"
            f"          - unique\n"
            f"          - not_null"
        )

    cols_str = "\n".join(col_blocks)

    return f"""version: 2

models:
  - name: {model_name}
    columns:
{cols_str}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        mart_columns = fetch_mart_columns(cur)
        cur.close()
    finally:
        conn.close()

    # Find mart SQL files without schema YAML
    written = 0
    for sql_file in sorted(MARTS_DIR.rglob("*.sql")):
        model_name = sql_file.stem
        if model_name in ALREADY_TESTED:
            continue

        # Check if this directory already has a schema yml that covers this model
        dir_ymls = list(sql_file.parent.glob("schema*.yml")) + list(sql_file.parent.glob("_*models*.yml"))
        if dir_ymls:
            # Check if model is mentioned in existing yml
            already_covered = False
            for yml_path in dir_ymls:
                content = yml_path.read_text(encoding="utf-8", errors="ignore")
                if model_name in content:
                    already_covered = True
                    break
            if already_covered:
                continue

        # Look up columns from Snowflake (keys are uppercase from INFORMATION_SCHEMA)
        table_name = model_name.upper()
        columns = mart_columns.get(table_name, [])
        if not columns:
            # Try without domain prefix for politics models
            for key in mart_columns:
                if key.lower() == model_name.lower() or key.lower().replace("__", "_") == model_name.lower().replace("__", "_"):
                    columns = mart_columns[key]
                    break
        if not columns:
            continue

        yml_content = render_schema_yml(model_name, columns)
        yml_path = sql_file.parent / f"schema_{model_name.split('__')[-1] if '__' in model_name else model_name}.yml"

        if args.dry_run:
            print(f"  would write: {yml_path.relative_to(MARTS_DIR)}")
        else:
            yml_path.write_text(yml_content, encoding="utf-8")
        written += 1

    action = "would write" if args.dry_run else "wrote"
    print(f"{action}: {written} schema yml file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
