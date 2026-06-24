"""Join-key detection + value normalization.

Detection REUSES the battle-tested tagger in portal_recon/tag_portal_index.py
(the same KEY_TOKENS / tier discipline that tagged the 338k portal index), so
"what key does this column carry?" stays consistent across the whole platform.

What's NEW here is normalization: to actually JOIN two columns we have to
canonicalize their values the same way on both sides (strip punctuation, drop
leading zeros on entity IDs, upper-case names, etc.). That's the difference
between "both carry an EIN-shaped column" and "these rows actually match".
"""

from __future__ import annotations

import sys
from pathlib import Path

_PR = Path(__file__).resolve().parents[1] / "portal_recon"
if str(_PR) not in sys.path:
    sys.path.insert(0, str(_PR))

# Reuse the canonical tagger + tier reference.
from tag_portal_index import (  # noqa: E402
    KEY_TOKENS,
    PAIR_RULES,
    TIER_ORDER,
    TIER_RANK,
    tokens,
)


def detect_key(column_name: str) -> tuple[str | None, str | None]:
    """Return (key_label, tier) for a single column, or (None, None).

    Strongest tier wins (KEY_TOKENS is ordered STEEL-first). Mirrors the set
    logic in tag_portal_index.tag_columns, but per-column so we can pin which
    physical column carries the key.
    """
    tk = tokens(column_name)
    if not tk:
        return None, None
    for key, (tier, toks) in KEY_TOKENS.items():
        if tk & toks:
            return key, tier
    for key, (a, b) in PAIR_RULES:
        if a in tk and b in tk:
            return key, KEY_TOKENS[key][0]
    return None, None


# --------------------------------------------------------------------------- #
# Join mode per key
# --------------------------------------------------------------------------- #
# 'value'   : canonicalize the cell and equi-join on it (IDs, codes, names)
# 'spatial' : geographic (lat/lon point or geometry) — handled by overlap.spatial
# 'skip'    : detected but not directly join-able as a single column
SPATIAL_KEYS = {"LATLON", "GEOM"}

# Entity keys: a shared key TYPE here strongly implies a real connection (unlike
# GEO/NAME, where a type match can overlap nothing). Single source of truth =
# the tagger's tiers, so a new STEEL/STRONG key is picked up everywhere at once.
ENTITY_KEYS = [k for k, (tier, _toks) in KEY_TOKENS.items() if tier in ("STEEL", "STRONG")]


def join_mode(key: str) -> str:
    if key in SPATIAL_KEYS:
        return "spatial"
    return "value"


# --------------------------------------------------------------------------- #
# Value normalizers -- a Snowflake SQL expression canonicalizing a column for an
# equi-join. NULL/empty after normalization => excluded from the join.
#
# We PAD, never strip. Padding two distinct fixed-width IDs can never collapse
# them; LTRIM '0' provably can ('015009' and '15009' both -> '15009') -- the
# exact mechanism that manufactured the Alabama/Puerto-Rico false match.
#
# rule = (mode, width)
#   pad   N : alnum, upper, LPAD to width N; NULL if longer than N (dirty)
#   fixed N : alnum, upper, keep ONLY if exactly N chars (UEI/LEI), else NULL
#   code    : keep leading zeros, strip punctuation, upper (FIPS/ZIP/NAICS/docket)
#   country : upper letters only (ISO)
#   name    : upper, punctuation -> single space, trim (fuzzy by nature)
# --------------------------------------------------------------------------- #
NORM_RULES: dict[str, tuple[str, int]] = {
    "NPI": ("pad", 10), "EIN": ("pad", 9), "DUNS": ("pad", 9), "CIK": ("pad", 10),
    "CCN": ("pad", 6), "IMO": ("pad", 7), "MMSI": ("pad", 9),
    "UEI": ("fixed", 12), "LEI": ("fixed", 20),
    "NAICS": ("code", 0), "SIC": ("code", 0), "NCES": ("code", 0),
    "DOCKET": ("code", 0), "PATENT": ("code", 0), "FIPS": ("code", 0), "ZIP": ("code", 0),
    "COUNTRY": ("country", 0), "NAME": ("name", 0), "ADDRESS": ("name", 0),
}


def _alnum(col: str) -> str:
    return f"UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9A-Za-z]', ''))"


def normalize_sql(key: str, col: str) -> str:
    """SQL expression canonicalizing `col` for an equi-join on `key`.

    Raises on an unmapped value key -- fail loud, never silently mis-canonicalize
    (the old code fell back to a keep-zeros default, hiding newly-added keys).
    """
    if key not in NORM_RULES:
        raise KeyError(f"No NORM_RULES entry for key '{key}'. Add one before joining on it.")
    mode, width = NORM_RULES[key]
    clean = _alnum(col)
    if mode == "pad":
        return (f"CASE WHEN LENGTH({clean}) = 0 OR LENGTH({clean}) > {width} THEN NULL "
                f"ELSE LPAD({clean}, {width}, '0') END")
    if mode == "fixed":
        return f"CASE WHEN LENGTH({clean}) = {width} THEN {clean} ELSE NULL END"
    if mode == "code":
        return f"NULLIF({clean}, '')"
    if mode == "country":
        return f"NULLIF(UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^A-Za-z]', '')), '')"
    return f"NULLIF(TRIM(REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' ')), '')"


def quote_ident(name: str) -> str:
    """Quote a Snowflake identifier (landing columns can be odd)."""
    return '"' + str(name).replace('"', '""') + '"'
