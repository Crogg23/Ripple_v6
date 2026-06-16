"""Naming conventions shared across recon, ingest, dbt, and catalog steps.

One place decides how a source name + entity become a Snowflake table, a dbt
model name, and a schema -- so every step agrees on where data lives.
"""

from __future__ import annotations

import re

from config import settings

# Maps a Library layer to a default dbt mart "domain" prefix. Recon can override
# this when Claude proposes a more specific domain (e.g. "economics").
LAYER_DOMAIN = {
    "us_federal": "gov",
    "international": "global",
    "corporate": "entity",
    "investigative": "civic",
    "geospatial": "geo",
}


def slug(text: str) -> str:
    """Lower-case, underscore-separated identifier. 'SEC EDGAR' -> 'sec_edgar'."""
    s = re.sub(r"[^0-9a-zA-Z]+", "_", text.strip().lower())
    return re.sub(r"_+", "_", s).strip("_")


def _sf_ident(text: str) -> str:
    """Uppercase, underscore-separated Snowflake identifier."""
    return slug(text).upper()


def source_schema(source_name: str) -> str:
    return _sf_ident(source_name)


def raw_table_parts(source_name: str, entity: str) -> dict:
    """Resolve the database / schema / table for a source's raw landing table."""
    database = settings.snowflake_database
    if settings.snowflake_raw_layout == "single_schema":
        schema = settings.snowflake_schema
        table = f"{_sf_ident(source_name)}_{_sf_ident(entity)}"
    else:  # schema_per_source (default)
        schema = source_schema(source_name)
        table = _sf_ident(entity)
    return {"database": database, "schema": schema, "table": table}


def qualified_raw_table(source_name: str, entity: str) -> str:
    p = raw_table_parts(source_name, entity)
    return f"{p['database']}.{p['schema']}.{p['table']}"


def staging_model(source_name: str, entity: str) -> str:
    return f"stg_{slug(source_name)}__{slug(entity)}"


def mart_model(domain: str, source_name: str, entity: str) -> str:
    return f"{slug(domain)}__{slug(source_name)}_{slug(entity)}"
