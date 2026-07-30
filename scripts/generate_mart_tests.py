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
MODELS_DIR = DBT_PROJECT / "models"


def _project_wide_model_coverage() -> set[str]:
    """Every model name already documented in ANY schema.yml/models.yml across
    the whole project -- not just the mart's own directory. 2026-07-30: the
    directory-only check missed 33 marts that share their model name with an
    already-tested staging model, producing dbt1005 'duplicate resource
    definitions' the first time this was actually run project-wide."""
    covered: set[str] = set()
    for yml_path in MODELS_DIR.rglob("*.yml"):
        content = yml_path.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("- name:"):
                covered.add(s.split(":", 1)[1].strip())
    return covered

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


# Schemas that hold real dbt-built marts. Excludes INFORMATION_SCHEMA (not a
# real schema), PUBLIC (holds views, not marts) and _RESTORE_20260701 (a
# snapshotted archive of tables dropped in the 2026-07-01 housekeeping pass,
# not live marts). 2026-07-30: this used to be hardcoded to 3 schemas
# (DBT_CROGERS/POLITICS/EPSTEIN), a leftover from before marts were split
# across 36+ domain schemas via config(schema=...) — that restriction made
# this tool blind to ~90% of the warehouse. Fixed to see everything real.
_EXCLUDED_SCHEMAS = {"INFORMATION_SCHEMA", "PUBLIC", "_RESTORE_20260701"}


def fetch_mart_columns(cur) -> dict[str, list[tuple[str, str]]]:
    """Returns {table_name: [(schema, col1), (schema, col2), ...]} for all mart
    tables across every real domain schema (not just a hardcoded 3)."""
    cur.execute("""
        SELECT table_schema, table_name, column_name
        FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
        ORDER BY table_name, ordinal_position
    """)
    result: dict[str, list[tuple[str, str]]] = {}
    for schema, table_name, col_name in cur.fetchall():
        if schema in _EXCLUDED_SCHEMAS:
            continue
        if col_name.startswith("_"):
            continue
        result.setdefault(table_name, []).append((schema, col_name))
    return result


def verify_key_columns(cur, schema: str, table: str, candidates: list[str]) -> dict[str, dict]:
    """Live-check each candidate key column against the real data: never guess
    'unique'/'not_null' from a column NAME alone (CLAUDE.md's bare-COUNT
    trap — a heuristic name match is not proof). Returns
    {col: {'total': n, 'distinct': n, 'nulls': n}} so the caller only asserts
    a test the live data already actually satisfies.
    """
    if not candidates:
        return {}
    exprs = []
    for c in candidates:
        q = f'"{c}"'
        exprs.append(f'COUNT(DISTINCT {q}) AS "{c}__distinct"')
        exprs.append(f'COUNT_IF({q} IS NULL) AS "{c}__nulls"')
    sql = f'SELECT COUNT(*) AS "__total", {", ".join(exprs)} FROM "LIBRARY_MARTS"."{schema}"."{table}"'
    try:
        cur.execute(sql)
    except Exception as exc:  # a genuinely broken/empty mart shouldn't kill the whole run
        print(f"  ! skipped {schema}.{table}: {exc}")
        return {}
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    vals = dict(zip(cols, row))
    total = vals["__total"]
    out = {}
    for c in candidates:
        out[c] = {
            "total": total,
            "distinct": vals[f"{c}__distinct"],
            "nulls": vals[f"{c}__nulls"],
        }
    return out


def render_schema_yml(model_name: str, verified: dict[str, dict]) -> str | None:
    """Only ever asserts a test the LIVE data already satisfies today — never
    a name-heuristic guess. unique requires distinct == total (and total > 0);
    not_null requires nulls == 0. A column that fails both is skipped, not
    forced in with a test that would just start red."""
    col_blocks = []
    for col, stats in verified.items():
        total = stats["total"]
        if total == 0:
            continue
        tests = []
        if stats["nulls"] == 0:
            tests.append("not_null")
        if stats["distinct"] == total:
            tests.append("unique")
        if not tests:
            continue
        test_lines = "\n".join(f"          - {t}" for t in tests)
        col_blocks.append(
            f"      - name: {col.lower()}\n"
            f"        data_tests:\n{test_lines}"
        )

    if not col_blocks:
        return None

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
    cur = conn.cursor()
    try:
        mart_columns = fetch_mart_columns(cur)
        project_covered = _project_wide_model_coverage()

        # Find mart SQL files without schema YAML
        written = 0
        skipped_no_verified_key = 0
        for sql_file in sorted(MARTS_DIR.rglob("*.sql")):
            model_name = sql_file.stem
            if model_name in ALREADY_TESTED or model_name in project_covered:
                continue

            # Look up columns from Snowflake (keys are uppercase from INFORMATION_SCHEMA)
            table_name = model_name.upper()
            schema_cols = mart_columns.get(table_name, [])
            if not schema_cols:
                for key in mart_columns:
                    if key.lower() == model_name.lower() or key.lower().replace("__", "_") == model_name.lower().replace("__", "_"):
                        schema_cols = mart_columns[key]
                        break
            if not schema_cols:
                continue

            schema = schema_cols[0][0]
            columns = [c for _s, c in schema_cols]
            candidates = [c for c in columns if is_likely_key(c)] or columns[:1]

            verified = verify_key_columns(cur, schema, table_name, candidates)
            yml_content = render_schema_yml(model_name, verified)
            if yml_content is None:
                skipped_no_verified_key += 1
                continue

            yml_path = sql_file.parent / f"schema_{model_name.split('__')[-1] if '__' in model_name else model_name}.yml"

            if args.dry_run:
                print(f"  would write: {yml_path.relative_to(MARTS_DIR)}")
            else:
                yml_path.write_text(yml_content, encoding="utf-8")
            written += 1
    finally:
        cur.close()
        conn.close()

    action = "would write" if args.dry_run else "wrote"
    print(f"{action}: {written} schema yml file(s); "
          f"{skipped_no_verified_key} mart(s) had no column whose current data "
          f"actually satisfies not_null/unique (skipped rather than asserting an untrue test)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
