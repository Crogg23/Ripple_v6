"""Naming conventions for the Ripple warehouse.

The whole platform hangs off ``SOURCE_ID`` -- a lowercase, underscore-separated
key like ``fed_usgs_earthquakes``. From it everything else is derived:

    landing table : LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>
    registry row  : SOURCE_REGISTRY keyed on SOURCE_ID
    ingest log    : INGEST_RUNS keyed on SOURCE_ID
    dbt staging   : stg_<source_id>__<entity>
    dbt mart      : <domain>__<source_id>

The first token of SOURCE_ID is a jurisdiction prefix.
"""

from __future__ import annotations

import re

# Jurisdiction <-> SOURCE_ID prefix, taken from the live registry.
JURISDICTION_PREFIX = {
    "federal": "fed",
    "international": "intl",
    "cross-cutting": "xc",
    "local": "loc",
    "state": "st",
}
PREFIXES = set(JURISDICTION_PREFIX.values())

# Build-plan "layer" -> registry jurisdiction (recon can override per source).
LAYER_JURISDICTION = {
    "us_federal": "federal",
    "international": "international",
    "corporate": "cross-cutting",
    "investigative": "cross-cutting",
    "geospatial": "federal",
}

# Jurisdiction -> default dbt mart "domain" prefix (recon may override).
JURISDICTION_DOMAIN = {
    "federal": "gov",
    "international": "global",
    "cross-cutting": "xc",
    "local": "local",
    "state": "state",
}


def slug(text: str) -> str:
    """Lower-case, underscore-separated identifier. 'SEC EDGAR' -> 'sec_edgar'."""
    s = re.sub(r"[^0-9a-zA-Z]+", "_", text.strip().lower())
    return re.sub(r"_+", "_", s).strip("_")


def prefix_for(jurisdiction: str) -> str:
    return JURISDICTION_PREFIX.get((jurisdiction or "").strip().lower(), "xc")


def source_id(name: str, jurisdiction: str) -> str:
    """Derive a conforming SOURCE_ID: ``<prefix>_<slug(name)>``.

    Already-prefixed names are left alone so recon/foreman can hand us a final
    SOURCE_ID directly (e.g. 'fed_usgs_earthquakes').
    """
    base = slug(name)
    first = base.split("_", 1)[0]
    if first in PREFIXES:
        return base
    return f"{prefix_for(jurisdiction)}_{base}"


def landing_table(source_id_value: str) -> str:
    """LIBRARY_RAW.LANDING table name == UPPER(SOURCE_ID)."""
    return slug(source_id_value).upper()


def staging_model(source_id_value: str, entity: str) -> str:
    return f"stg_{slug(source_id_value)}__{slug(entity)}"


def mart_model(domain: str, source_id_value: str) -> str:
    return f"{slug(domain)}__{slug(source_id_value)}"
