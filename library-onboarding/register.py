"""Checkpoint 5 -- REGISTRY.

Upsert the source into ``RIPPLE_META.REGISTRY.SOURCE_REGISTRY`` (keyed on
SOURCE_ID) so it's discoverable in the catalog alongside the other ~900 sources.
This is the Ripple-native catalog; there is no OpenMetadata in this stack.
"""

from __future__ import annotations

from typing import Optional

import snow
from config import settings
from llm import call_claude, extract_json, render_prompt

# Ordered SOURCE_REGISTRY columns the agent writes (excluding _LOADED_AT).
_COLUMNS = [
    "SOURCE_ID", "JURISDICTION", "CATEGORY", "SUBCATEGORY", "PUBLISHER", "NAME",
    "DESCRIPTION", "UNIT_OF_OBSERVATION", "TEMPORAL_COVERAGE", "GEOGRAPHIC_SCOPE",
    "ACCESS_METHOD", "FORMAT", "AUTH_REQUIRED", "COST", "UPDATE_CADENCE", "VOLUME",
    "LICENSE_TERMS", "URL", "JOIN_KEYS", "ACCOUNTABILITY_RELEVANCE", "EPSTEIN_RELEVANT",
    "PRIORITY_TIER", "INCLUDE", "NOTES",
]


def register_source(config: dict) -> dict:
    enrichment = _enrich(config)
    row = _build_row(config, enrichment)
    fqt = f"{settings.meta_database}.{settings.registry_schema}.{settings.registry_table}"

    if settings.fake_llm or not settings.snowflake_ready():
        why = "fake mode" if settings.fake_llm else "Snowflake creds not set"
        return {
            "source_id": row["SOURCE_ID"],
            "fqn": fqt,
            "preview": {k: row[k] for k in ("SOURCE_ID", "JURISDICTION", "CATEGORY", "ACCESS_METHOD", "PRIORITY_TIER")},
            "join_keys": row["JOIN_KEYS"],
            "status": f"DRY RUN ({why}) -- would upsert SOURCE_ID '{row['SOURCE_ID']}' into {fqt}",
        }

    conn = snow.connect()
    try:
        existed = snow.fetch_scalar(
            conn,
            f'SELECT COUNT(*) FROM "{settings.meta_database}"."{settings.registry_schema}"."{settings.registry_table}" WHERE SOURCE_ID=%s',
            (row["SOURCE_ID"],),
        )
        snow.execute(conn, *_merge_sql(row))
        verb = "updated" if existed else "inserted"
    finally:
        conn.close()

    return {
        "source_id": row["SOURCE_ID"],
        "fqn": fqt,
        "join_keys": row["JOIN_KEYS"],
        "status": f"Registry row {verb} for SOURCE_ID '{row['SOURCE_ID']}'",
    }


def _build_row(config: dict, enrichment: dict) -> dict:
    return {
        "SOURCE_ID": config["source_id"],
        "JURISDICTION": config.get("jurisdiction", ""),
        "CATEGORY": config.get("category", ""),
        "SUBCATEGORY": config.get("subcategory", ""),
        "PUBLISHER": config.get("publisher", ""),
        "NAME": config.get("name", ""),
        "DESCRIPTION": config.get("description", ""),
        "UNIT_OF_OBSERVATION": config.get("unit_of_observation", ""),
        "TEMPORAL_COVERAGE": config.get("temporal_coverage", ""),
        "GEOGRAPHIC_SCOPE": config.get("geographic_scope", ""),
        "ACCESS_METHOD": config.get("access_method", ""),
        "FORMAT": config.get("format", ""),
        "AUTH_REQUIRED": config.get("auth", {}).get("type", "none"),
        "COST": config.get("cost", ""),
        "UPDATE_CADENCE": config.get("update_cadence", ""),
        "VOLUME": config.get("volume", ""),
        "LICENSE_TERMS": config.get("license_terms", ""),
        "URL": config.get("url", ""),
        "JOIN_KEYS": config.get("join_keys", ""),
        "ACCOUNTABILITY_RELEVANCE": enrichment.get("accountability_relevance")
        or config.get("accountability_relevance", ""),
        "EPSTEIN_RELEVANT": enrichment.get("epstein_relevant", ""),
        "PRIORITY_TIER": str(config.get("priority_tier", "2")),
        "INCLUDE": "Y",  # the agent onboarded it
        "NOTES": enrichment.get("notes") or config.get("notes", ""),
    }


def _merge_sql(row: dict):
    fqt = f'"{settings.meta_database}"."{settings.registry_schema}"."{settings.registry_table}"'
    using = ", ".join(f"%s AS {c}" for c in _COLUMNS)
    update_set = ", ".join(f"t.{c}=s.{c}" for c in _COLUMNS if c != "SOURCE_ID")
    insert_cols = ", ".join(_COLUMNS) + ", _LOADED_AT"
    insert_vals = ", ".join(f"s.{c}" for c in _COLUMNS) + ", CURRENT_TIMESTAMP()"
    sql = (
        f"MERGE INTO {fqt} t USING (SELECT {using}) s ON t.SOURCE_ID = s.SOURCE_ID "
        f"WHEN MATCHED THEN UPDATE SET {update_set}, t._LOADED_AT=CURRENT_TIMESTAMP() "
        f"WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals})"
    )
    params = tuple(row[c] for c in _COLUMNS)
    return sql, params


def _enrich(config: dict) -> dict:
    """Ask Claude for accountability relevance + notes. Best-effort."""
    try:
        prompt = render_prompt(
            "generate_catalog",
            name=config["name"],
            source_id=config["source_id"],
            landing_table=config["landing_table"],
            description=config.get("description", ""),
            join_keys=config.get("join_keys", "(none)"),
            update_cadence=config.get("update_cadence", "unknown"),
        )
        raw = call_claude(
            user=prompt,
            system="You write concise, factual data-catalog metadata for an investigative-journalism platform. Output strict JSON.",
            kind="registry",
            fake_context=config,
            max_tokens=1024,
        )
        return extract_json(raw)
    except Exception:
        return {}
