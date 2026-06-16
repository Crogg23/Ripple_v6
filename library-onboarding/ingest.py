"""Checkpoints 2 + 3 -- SCRIPT and LOAD.

Checkpoint 2: Claude writes a source-specific ``fetch_data(context)`` function
that downloads/parses the source and returns a pandas DataFrame.

Checkpoint 3: we run that function, stamp every row with the standard metadata
columns (``_loaded_at`` / ``_source_url`` / ``_source_file``), and load the
result into the source's raw table in Snowflake.

The generated function deliberately does NOT touch Snowflake itself -- the load
is standardized here so every source lands the same way. The foreman reviews the
generated code at Checkpoint 2 before it is ever executed.
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Optional

from config import ConfigError, settings
from llm import call_claude, extract_code, render_prompt

META_LOADED_AT = "_LOADED_AT"
META_SOURCE_URL = "_SOURCE_URL"
META_SOURCE_FILE = "_SOURCE_FILE"
SAMPLE_ROWS = 5


# ---------------------------------------------------------------------------
# Checkpoint 2 -- generate the ingestion script
# ---------------------------------------------------------------------------
def generate_ingest_script(config: dict, feedback: Optional[str] = None) -> str:
    schema_repr = "\n".join(
        f"  - {f.get('name')} ({f.get('type')}): {f.get('description','')}"
        for f in config.get("schema_fields", [])
    ) or "  (schema unknown -- infer from the source)"

    prompt = render_prompt(
        "generate_ingest",
        name=config["name"],
        url=config["url"],
        access_pattern=config.get("access_pattern", "unknown"),
        auth_type=config.get("auth", {}).get("type", "none"),
        auth_notes=config.get("auth", {}).get("notes", ""),
        data_format=config.get("format", "unknown"),
        rate_limits=config.get("rate_limits", "unspecified"),
        schema=schema_repr,
        feedback=feedback or "(none)",
    )
    raw = call_claude(
        user=prompt,
        system=(
            "You write robust Python data-ingestion functions. Output ONLY a "
            "Python code block defining `def fetch_data(context):` that returns a "
            "pandas.DataFrame. No Snowflake code."
        ),
        kind="ingest",
        fake_context=config,
        max_tokens=4096,
    )
    return extract_code(raw, "python")


# ---------------------------------------------------------------------------
# Checkpoint 3 -- execute + load
# ---------------------------------------------------------------------------
def run_ingest(config: dict, code: str) -> dict:
    """Execute the generated fetch_data() and load the result to Snowflake."""
    df = _execute_fetch(config, code)

    # Stamp standard metadata columns (raw table spec).
    df[META_LOADED_AT] = _dt.datetime.now(_dt.timezone.utc).replace(tzinfo=None)
    df[META_SOURCE_URL] = config["url"]
    if META_SOURCE_FILE not in df.columns:
        df[META_SOURCE_FILE] = config.get("_source_file", "")

    sample = df.head(SAMPLE_ROWS).astype(str).to_dict(orient="records")
    base = {
        "rows": int(len(df)),
        "columns": ", ".join(map(str, df.columns)),
        "sample_rows": sample,
    }

    if settings.fake_llm and not settings.snowflake_password:
        base["status"] = "DRY RUN (fake mode -- not written to Snowflake)"
        return base

    written = _load_dataframe(df, config)
    base["status"] = f"Loaded into {written}"
    return base


def _execute_fetch(config: dict, code: str):
    """Run Claude-generated code and return the DataFrame it produces.

    SECURITY: this executes model-generated Python. It only runs after the
    foreman approved the exact code shown at Checkpoint 2.
    """
    try:
        import pandas as pd  # noqa: F401  (made available to generated code)
    except ImportError as exc:  # pragma: no cover
        raise ConfigError("pandas is required. Run `pip install -r requirements.txt`.") from exc

    namespace: dict = {}
    exec(compile(code, "<generated_ingest>", "exec"), namespace)  # noqa: S102
    fetch = namespace.get("fetch_data")
    if not callable(fetch):
        raise RuntimeError("Generated script did not define fetch_data(context).")

    context = {
        "url": config["url"],
        "source_name": config["name"],
        "auth_type": config.get("auth", {}).get("type", "none"),
        "env": dict(os.environ),  # generated code reads API keys from here
        "source_file": "",
    }
    df = fetch(context)
    config["_source_file"] = context.get("source_file", "")

    if not hasattr(df, "columns"):
        raise RuntimeError("fetch_data must return a pandas.DataFrame.")
    if len(df) == 0:
        raise RuntimeError("fetch_data returned 0 rows -- failing loudly (schema drift?).")
    return df


def _load_dataframe(df, config: dict) -> str:
    """Create the schema/table if needed and load the frame. Fails loudly."""
    settings.require(
        "snowflake_account", "snowflake_user", "snowflake_password", "snowflake_database"
    )
    if not settings.snowflake_warehouse:
        raise ConfigError("SNOWFLAKE_WAREHOUSE must be set for writes.")

    try:
        import snowflake.connector
        from snowflake.connector.pandas_tools import write_pandas
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "snowflake-connector-python is required. Run `pip install -r requirements.txt`."
        ) from exc

    database = config["raw_database"]
    schema = config["raw_schema"]
    table = config["raw_table_short"]

    conn = snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        database=database,
        warehouse=settings.snowflake_warehouse,
        role=settings.snowflake_role or None,
    )
    try:
        cur = conn.cursor()
        cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{database}"."{schema}"')
        success, _nchunks, nrows, _ = write_pandas(
            conn,
            df,
            table_name=table,
            database=database,
            schema=schema,
            auto_create_table=True,
            overwrite=False,
            quote_identifiers=True,
        )
        if not success:
            raise RuntimeError(f"write_pandas reported failure loading {table}.")
        return f"{database}.{schema}.{table} ({nrows} rows)"
    finally:
        conn.close()
