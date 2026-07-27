"""LLM-free dbt staging scaffold for deterministic loaders.

After bridge_fuel or server_side lands a table, this generates the staging model
+ schema.yml if they don't already exist. Follows the exact same pattern as the
LLM-scaffolded models (source → view with dedup + key renames), just without
needing Claude to write it.

The LLM scaffold (scaffold_dbt.py) is still used for novel sources via onboard.py.
This is the cheap, instant, deterministic fallback for known-spec sources.
"""
from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[1]
DBT_ROOT = REPO / "library-onboarding" / "ripple_dbt"
MODELS_DIR = DBT_ROOT / "models"


# ---------------------------------------------------------------------------
# Pure generators (unit-testable, no I/O)
# ---------------------------------------------------------------------------

def staging_model_sql(source_id: str, table_name: str,
                      columns: list[str], key_cols: list[dict]) -> str:
    """Generate stg_<source_id>__all.sql content.

    key_cols: [{"col": "Original Name", "as": "CANONICAL"}] — renames in SELECT.
    columns: raw column names from DESCRIBE TABLE (excludes _ meta columns).
    """
    source_id_lower = source_id.lower()
    # Build SELECT list: rename key columns, pass through the rest
    renames = {kc["col"].upper(): kc.get("as") or kc.get("alias") for kc in key_cols}
    selects = []
    pk_col = None
    for col in columns:
        canon = renames.get(col.upper())
        if canon:
            selects.append(f'    "{col}" as {canon}')
            if pk_col is None:
                pk_col = canon
        else:
            selects.append(f'    "{col}"')

    # Add meta columns
    selects.append('    _INGESTED_AT')
    selects.append('    _SOURCE_RUN_ID')

    select_block = ",\n".join(selects)

    # Dedup clause: partition by the first key column (or first column if no keys)
    dedup_col = pk_col or (f'"{columns[0]}"' if columns else '"_SOURCE_RUN_ID"')

    return dedent(f"""\
        with source as (
            select * from {{{{ source('ripple_raw', '{table_name}') }}}}
        )

        select
        {select_block}
        from source
        qualify row_number() over (
            partition by {dedup_col}
            order by _INGESTED_AT desc
        ) = 1
    """).rstrip() + "\n"


def schema_yml(source_id: str, table_name: str, model_name: str,
               key_cols: list[dict], description: str = "") -> str:
    """Generate schema.yml with source declaration + model tests."""
    source_id_lower = source_id.lower()
    desc = description or f"Staging model for {source_id}"

    # Key column tests
    col_tests = ""
    for kc in key_cols:
        canon = kc.get("as") or kc.get("alias") or kc["col"]
        col_tests += f"""
      - name: {canon}
        tests:
          - not_null
          - unique"""

    return dedent(f"""\
        version: 2

        sources:
          - name: ripple_raw
            database: LIBRARY_RAW
            schema: LANDING
            tables:
              - name: {table_name}

        models:
          - name: {model_name}
            description: "{desc}"
            columns:{col_tests}
    """).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Scaffold orchestrator
# ---------------------------------------------------------------------------

def scaffold_if_missing(source_id: str, table_name: str | None = None,
                        key_cols: list[dict] | None = None,
                        description: str = "",
                        conn=None) -> str | None:
    """Generate staging model + schema.yml if they don't exist.

    Args:
        source_id: e.g. "FED_FEC_LEADERSHIP_PAC"
        table_name: landing table name (defaults to source_id upper)
        key_cols: [{"col": "src_name", "as": "CANONICAL"}]
        description: one-line description for schema.yml
        conn: optional Snowflake connection for DESCRIBE TABLE

    Returns:
        Path of created model directory, or None if already exists.
    """
    source_id_lower = source_id.lower()
    table_name = table_name or source_id.upper()
    key_cols = key_cols or []

    model_dir = MODELS_DIR / "staging" / source_id_lower
    model_name = f"stg_{source_id_lower}__all"
    model_path = model_dir / f"{model_name}.sql"

    if model_path.exists():
        return None  # already scaffolded

    # Get columns from Snowflake if connection available
    columns = _describe_columns(table_name, conn) if conn else []
    if not columns:
        # Fallback: use key_cols names + generic placeholder
        columns = [kc["col"] for kc in key_cols] if key_cols else ["ID"]

    # Generate files
    model_sql = staging_model_sql(source_id, table_name, columns, key_cols)
    schema = schema_yml(source_id, table_name, model_name, key_cols, description)

    # Write
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path.write_text(model_sql, encoding="utf-8")
    (model_dir / "schema.yml").write_text(schema, encoding="utf-8")

    return str(model_dir)


def _describe_columns(table_name: str, conn) -> list[str]:
    """Get column names from LIBRARY_RAW.LANDING.<table>, excluding _ meta columns."""
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = 'LANDING' AND TABLE_NAME = %s "
            "ORDER BY ORDINAL_POSITION",
            (table_name,),
        )
        cols = [r[0] for r in cur.fetchall()]
        return [c for c in cols if not c.startswith("_")]
    except Exception:
        return []
