"""Checkpoint 5 -- CATALOG.

Register the freshly loaded raw table in OpenMetadata via its REST API: a table
entity with column-level metadata, the source URL, update cadence, and the key
identifiers (recorded as tags). Talks plain REST so the heavy OpenMetadata SDK
is not required.
"""

from __future__ import annotations

from typing import Optional

import requests

from config import ConfigError, settings
from llm import call_claude, extract_json, render_prompt

# A single logical Snowflake service in OpenMetadata that all raw tables hang off.
SERVICE_NAME = "ripple_snowflake"

# Map our coarse schema types to OpenMetadata column dataTypes.
_OM_TYPES = {
    "VARCHAR": "VARCHAR", "STRING": "VARCHAR", "TEXT": "TEXT", "CHAR": "CHAR",
    "INT": "INT", "INTEGER": "INT", "BIGINT": "BIGINT", "NUMBER": "NUMBER",
    "FLOAT": "FLOAT", "DOUBLE": "DOUBLE", "DECIMAL": "DECIMAL",
    "BOOL": "BOOLEAN", "BOOLEAN": "BOOLEAN",
    "DATE": "DATE", "TIMESTAMP": "TIMESTAMP", "TIMESTAMP_NTZ": "TIMESTAMP",
    "JSON": "JSON", "VARIANT": "JSON", "GEOGRAPHY": "GEOGRAPHY",
}


def _om_type(raw: str) -> str:
    return _OM_TYPES.get((raw or "").strip().upper(), "VARCHAR")


def _build_columns(config: dict) -> list:
    cols = []
    for f in config.get("schema_fields", []):
        cols.append(
            {
                "name": f.get("name", "col"),
                "dataType": _om_type(f.get("type", "VARCHAR")),
                "dataLength": 255 if _om_type(f.get("type", "")) in ("VARCHAR", "CHAR") else None,
                "description": f.get("description", ""),
            }
        )
    # Standard metadata columns every raw table carries.
    cols += [
        {"name": "_LOADED_AT", "dataType": "TIMESTAMP", "description": "When the agent loaded this row."},
        {"name": "_SOURCE_URL", "dataType": "VARCHAR", "dataLength": 1024, "description": "Exact source URL."},
        {"name": "_SOURCE_FILE", "dataType": "VARCHAR", "dataLength": 1024, "description": "Source filename if bulk."},
    ]
    # Drop null dataLength keys OpenMetadata rejects.
    return [{k: v for k, v in c.items() if v is not None} for c in cols]


def _enrich(config: dict) -> dict:
    """Ask Claude for a catalog description + tags. Best-effort."""
    try:
        prompt = render_prompt(
            "generate_catalog",
            name=config["name"],
            raw_table=config["raw_table"],
            description=config.get("description", ""),
            identifiers=", ".join(config.get("key_identifiers", [])) or "(none)",
            update_frequency=config.get("update_frequency", "unknown"),
        )
        raw = call_claude(
            user=prompt,
            system="You write concise data-catalog metadata. Output strict JSON.",
            kind="catalog",
            fake_context={**config, "table": config.get("raw_table_short")},
            max_tokens=1024,
        )
        return extract_json(raw)
    except Exception:
        return {}


def register_in_openmetadata(config: dict, load_result: Optional[dict] = None) -> dict:
    enrichment = _enrich(config)
    description = enrichment.get("description") or config.get("description") or (
        f"Raw landing table for {config['name']}. Source: {config['url']}"
    )
    columns = _build_columns(config)
    identifiers = config.get("key_identifiers", [])
    fqn = f"{SERVICE_NAME}.{config['raw_database']}.{config['raw_schema']}.{config['raw_table_short']}"

    # Dry run: fake mode or no token configured.
    if settings.fake_llm or not settings.openmetadata_token.strip():
        note = "fake mode" if settings.fake_llm else "OPENMETADATA_TOKEN not set"
        return {
            "fqn": fqn,
            "url": settings.openmetadata_host,
            "column_count": len(columns),
            "identifiers": identifiers,
            "status": f"DRY RUN ({note}) -- would create table entity + {len(columns)} columns",
        }

    _ensure_hierarchy(config)
    payload = {
        "name": config["raw_table_short"],
        "databaseSchema": f"{SERVICE_NAME}.{config['raw_database']}.{config['raw_schema']}",
        "description": description,
        "columns": columns,
        "sourceUrl": config["url"],
    }
    table = _om_put("tables", payload)
    _tag_identifiers(table, identifiers)

    return {
        "fqn": table.get("fullyQualifiedName", fqn),
        "url": f"{settings.openmetadata_host}/table/{table.get('fullyQualifiedName', fqn)}",
        "column_count": len(columns),
        "identifiers": identifiers,
        "status": "Registered in OpenMetadata",
    }


# ---------------------------------------------------------------------------
# OpenMetadata REST helpers
# ---------------------------------------------------------------------------
def _headers() -> dict:
    settings.require("openmetadata_token")
    return {
        "Authorization": f"Bearer {settings.openmetadata_token}",
        "Content-Type": "application/json",
    }


def _om_put(entity: str, payload: dict) -> dict:
    url = f"{settings.openmetadata_host}/api/v1/{entity}"
    resp = requests.put(url, json=payload, headers=_headers(), timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(
            f"OpenMetadata PUT /{entity} failed ({resp.status_code}): {resp.text[:500]}"
        )
    return resp.json()


def _ensure_hierarchy(config: dict) -> None:
    """Create the service -> database -> schema chain (idempotent)."""
    _om_put(
        "services/databaseServices",
        {
            "name": SERVICE_NAME,
            "serviceType": "Snowflake",
            "connection": {"config": {"type": "Snowflake"}},
        },
    )
    _om_put(
        "databases",
        {"name": config["raw_database"], "service": SERVICE_NAME},
    )
    _om_put(
        "databaseSchemas",
        {
            "name": config["raw_schema"],
            "database": f"{SERVICE_NAME}.{config['raw_database']}",
        },
    )


def _tag_identifiers(table: dict, identifiers: list) -> None:
    """Best-effort: record key identifiers as a description note via PATCH-free PUT.

    Tag glossary terms may not exist; rather than fail the whole step we simply
    skip tagging if the API rejects it.
    """
    if not identifiers:
        return
    try:
        note = "Key identifiers: " + ", ".join(identifiers)
        existing = table.get("description", "") or ""
        if "Key identifiers" not in existing:
            payload = {
                "name": table["name"],
                "databaseSchema": table["databaseSchema"]["fullyQualifiedName"]
                if isinstance(table.get("databaseSchema"), dict)
                else table.get("databaseSchema"),
                "description": (existing + "\n\n" + note).strip(),
                "columns": table.get("columns", []),
            }
            _om_put("tables", payload)
    except Exception:
        pass
