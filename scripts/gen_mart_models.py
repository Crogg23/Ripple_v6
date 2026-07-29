"""
Batch-generate dbt mart models for all unmodeled sources.

Connects to Snowflake, reads column metadata from LIBRARY_RAW.LANDING,
and writes mart SQL files following the established project pattern.

Usage:
    cd library-onboarding/ripple_dbt
    python ../../scripts/gen_mart_models.py
"""

import os
import re
import snowflake.connector
from pathlib import Path

# --- Config ---
DBT_MODELS_DIR = Path(__file__).parent.parent / "library-onboarding" / "ripple_dbt" / "models" / "marts"
SOURCES_DIR = Path(__file__).parent.parent / "library-onboarding" / "ripple_dbt" / "models" / "staging"

# Columns to always exclude from the mart projection
EXCLUDE_COLS = {'_INGESTED_AT', '_SOURCE_RUN_ID', '_SRC_SHA256', 'INGESTED_AT', 'SOURCE_RUN_ID', 'SRC_SHA256'}

# Domain to schema folder mapping
DOMAIN_MAP = {
    'health_medicine': 'health',
    'money_in_politics': 'finance',
    'money_finance': 'finance',
    'corporate_entities': 'economics',
    'spending_budget': 'economics',
    'economy_labor_trade': 'economics',
    'government_power': 'politics',
    'elections_voting': 'politics',
    'justice_courts': 'justice',
    'crime_security': 'justice',
    'sanctions_enforcement': 'justice',
    'energy_environment': 'environment',
    'transport_movement': 'transport',
    'housing_social': 'housing',
    'immigration_migration': 'immigration',
    'history_culture': 'history',
    'science_research': 'science',
    'geo_demographics': 'reference',
    'open_data_portal': 'open_data',
    'targeted_investigation': 'investigations',
    'procurement_intl': 'procurement',
    'education': 'education',
    None: 'uncategorized',
    'None': 'uncategorized',
    'UNCLASSIFIED': 'uncategorized',
}


def get_connection():
    return snowflake.connector.connect(
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ.get('SNOWFLAKE_PAT', os.environ.get('SNOWFLAKE_PASSWORD', '')),
        role=os.environ.get('SNOWFLAKE_ROLE', 'ACCOUNTADMIN'),
        warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    )


def get_unmodeled_sources(conn):
    """Get sources that need mart models generated."""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.source_id, c.name, c.domain_primary, c.run_rows, c.join_key_tier
        FROM LIBRARY_META.REGISTRY.CATALOG c
        WHERE c.lifecycle IN ('landed', 'stale')
          AND c._real_mart = FALSE
          AND COALESCE(c.run_rows, 0) > 0
        ORDER BY c.run_rows DESC NULLS LAST
    """)
    return cur.fetchall()


def get_columns(conn, table_name):
    """Get column names for a landing table."""
    cur = conn.cursor()
    cur.execute(f"""
        SELECT column_name, data_type
        FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'LANDING' AND table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    return [(row[0], row[1]) for row in cur.fetchall()]


def snake_case(name):
    """Convert a column name to snake_case."""
    # Handle dotted names (e.g. Entity.LegalName -> entity_legal_name)
    name = name.replace('.', '_')
    # Handle camelCase
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    # Handle sequences of caps (e.g. HTMLParser -> html_parser)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    # Replace non-alphanumeric with underscore
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Collapse multiple underscores
    name = re.sub(r'_+', '_', name)
    # Strip leading/trailing underscores
    name = name.strip('_').lower()
    return name


def needs_quoting(col_name):
    """Check if a column name needs double-quoting in Snowflake."""
    # Needs quoting if: contains dots, spaces, hyphens, starts with number, is mixed case, or is reserved
    reserved = {'GROUP', 'ORDER', 'SELECT', 'FROM', 'WHERE', 'TABLE', 'INDEX', 'CREATE',
                'DROP', 'ALTER', 'CONNECT', 'GRANT', 'REVOKE', 'DATE', 'TIME', 'YEAR',
                'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND', 'VALUE', 'VALUES', 'KEY',
                'PRIMARY', 'FOREIGN', 'UNIQUE', 'CHECK', 'DEFAULT', 'NULL', 'NOT',
                'AND', 'OR', 'IN', 'IS', 'LIKE', 'BETWEEN', 'EXISTS', 'CASE', 'WHEN',
                'THEN', 'ELSE', 'END', 'AS', 'ON', 'JOIN', 'LEFT', 'RIGHT', 'FULL',
                'INNER', 'OUTER', 'CROSS', 'NATURAL', 'UNION', 'ALL', 'ANY', 'SOME',
                'TRUE', 'FALSE', 'COMMENT', 'COLUMN', 'ROWS', 'RANK', 'PARTITION',
                'OVER', 'WINDOW', 'LIMIT', 'OFFSET', 'HAVING', 'SET', 'UPDATE',
                'DELETE', 'INSERT', 'INTO', 'MERGE', 'USING', 'MATCHED'}
    if col_name.upper() in reserved:
        return True
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col_name):
        return True
    if col_name != col_name.upper() and col_name != col_name.lower():
        return True  # mixed case
    return False


def infer_cast(col_name, snake_name):
    """Infer an appropriate type cast based on column name patterns."""
    upper = col_name.upper()
    # Date patterns
    if any(x in upper for x in ['_DATE', 'DATE_', 'EFFECTIVE_DATE', 'CREATED', 'UPDATED',
                                  'FILED_DATE', 'START_DATE', 'END_DATE', 'EXPIR']):
        if 'TIME' in upper or 'DATETIME' in upper:
            return 'try_to_timestamp'
        return 'try_to_date'
    # Numeric patterns (amounts, counts, rates)
    if any(x in upper for x in ['AMOUNT', 'AMT', 'COST', 'PRICE', 'TOTAL', 'VALUE',
                                  'DOLLARS', 'PROCEEDS', 'OBLIGATION', 'DISBURSEMENT']):
        return 'try_to_double'
    if any(x in upper for x in ['COUNT', 'CNT', 'NUM_', 'NUMBER_OF', 'QUANTITY',
                                  'DEATHS', 'INJURED', 'MILES', 'SPEED', 'ROWS']):
        return 'try_to_number'
    if any(x in upper for x in ['_PCT', 'PERCENT', 'RATIO', 'RATE', 'SCORE', 'INDEX']):
        return 'try_to_double'
    if any(x in upper for x in ['LATITUDE', 'LONGITUDE', 'LAT', 'LON', 'LNG']):
        return 'try_to_double'
    if upper in ('YEAR', 'FISCAL_YEAR', 'FY', 'CONGRESS'):
        return 'try_to_number'
    return None  # keep as text


def generate_mart_sql(source_id, table_name, columns, domain, source_name, run_rows):
    """Generate the mart model SQL."""
    # Filter out metadata columns
    proj_cols = [(c, t) for c, t in columns if c.upper() not in EXCLUDE_COLS]

    if not proj_cols:
        return None

    # Determine schema from domain
    schema_folder = DOMAIN_MAP.get(domain, 'uncategorized')
    schema_upper = schema_folder.upper()

    # Build model name
    model_name = f"{schema_folder}__{source_id.lower()}"

    lines = []
    lines.append(f"{{{{ config(materialized='table', schema='{schema_upper}') }}}}")
    lines.append("")
    safe_name = (source_name or table_name).encode('ascii', 'replace').decode('ascii')
    lines.append(f"-- Source: {safe_name} ({run_rows or '?'} rows)")
    lines.append(f"-- Generated by gen_mart_models.py")
    lines.append("")
    lines.append("with source as (")
    lines.append(f"    select * from {{{{ source('ripple_raw', '{table_name}') }}}}")
    lines.append(")")
    lines.append("")
    lines.append("select")

    col_lines = []
    for i, (col_name, data_type) in enumerate(proj_cols):
        sname = snake_case(col_name)
        # Avoid duplicate snake names
        quoted = f'"{col_name}"' if needs_quoting(col_name) else col_name
        cast = infer_cast(col_name, sname)

        if cast:
            expr = f"    {cast}({quoted}) as {sname}"
        elif quoted != sname:
            expr = f"    {quoted} as {sname}"
        else:
            expr = f"    {quoted}"

        col_lines.append(expr)

    lines.append(",\n".join(col_lines))
    lines.append("from source")
    lines.append("")

    return model_name, schema_folder, "\n".join(lines)


def ensure_source_yaml(schema_folder, table_name):
    """Ensure a _sources.yml exists for this mart folder referencing the raw table."""
    folder = DBT_MODELS_DIR / schema_folder
    sources_file = folder / f"_{schema_folder}__sources.yml"

    if sources_file.exists():
        content = sources_file.read_text(encoding='utf-8')
        if table_name in content:
            return  # already referenced

        # Append table to existing source
        if '      tables:' in content:
            content = content.rstrip() + f"\n        - name: {table_name}\n"
            sources_file.write_text(content, encoding='utf-8')
    else:
        # Create new sources file
        yaml_content = f"""version: 2

sources:
  - name: ripple_raw
    database: LIBRARY_RAW
    schema: LANDING
    tables:
      - name: {table_name}
"""
        folder.mkdir(parents=True, exist_ok=True)
        sources_file.write_text(yaml_content, encoding='utf-8')


def main():
    # Load env
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / "library-onboarding" / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)

    conn = get_connection()
    sources = get_unmodeled_sources(conn)
    print(f"Found {len(sources)} unmodeled sources to process")

    generated = 0
    skipped = 0
    errors = 0

    for source_id, name, domain, run_rows, key_tier in sources:
        table_name = source_id.upper()

        # Check if columns exist
        columns = get_columns(conn, table_name)
        if not columns:
            skipped += 1
            continue

        # Check if model already exists
        schema_folder = DOMAIN_MAP.get(domain, 'uncategorized')
        model_name = f"{schema_folder}__{source_id.lower()}"
        target_dir = DBT_MODELS_DIR / schema_folder
        target_file = target_dir / f"{model_name}.sql"

        if target_file.exists():
            skipped += 1
            continue

        # Generate
        result = generate_mart_sql(source_id, table_name, columns, domain, name, run_rows)
        if result is None:
            skipped += 1
            continue

        model_name, schema_folder, sql = result
        target_dir = DBT_MODELS_DIR / schema_folder
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"{model_name}.sql"
        target_file.write_text(sql, encoding='utf-8')

        # Ensure source yaml
        try:
            ensure_source_yaml(schema_folder, table_name)
        except Exception as e:
            print(f"  WARN: source yaml issue for {table_name}: {e}")

        generated += 1
        if generated % 20 == 0:
            print(f"  ...generated {generated} models so far")

    print(f"\nDone! Generated: {generated}, Skipped: {skipped}, Errors: {errors}")
    print(f"Total unmodeled sources: {len(sources)}")
    conn.close()


if __name__ == '__main__':
    main()
