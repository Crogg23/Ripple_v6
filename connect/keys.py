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


def join_mode(key: str) -> str:
    if key in SPATIAL_KEYS:
        return "spatial"
    return "value"


# --------------------------------------------------------------------------- #
# Value normalizers — return a Snowflake SQL expression that canonicalizes the
# column for joining. NULL/empty after normalization => excluded from the join.
# --------------------------------------------------------------------------- #
def _id_strip0(col: str) -> str:
    # Entity IDs (EIN/NPI/CIK/CCN/...): keep alphanumerics, upper, drop leading
    # zeros (so '015009' == '15009'). Same fix that doubled the CCN match earlier.
    return (
        f"NULLIF(LTRIM(UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9A-Za-z]', '')), '0'), '')"
    )


def _code_keep0(col: str) -> str:
    # Geographic codes (FIPS/ZIP): leading zeros are significant — keep them.
    return f"NULLIF(REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9A-Za-z]', ''), '')"


def _name(col: str) -> str:
    # Names/addresses: upper, punctuation -> single space, trim. Fuzzy by nature.
    return f"NULLIF(TRIM(REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' ')), '')"


def _country(col: str) -> str:
    return f"NULLIF(UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^A-Za-z]', '')), '')"


# key -> normalizer
_NORMALIZERS: dict[str, callable] = {}
for _k in ("EIN", "NPI", "CIK", "UEI", "DUNS", "LEI", "IMO", "MMSI", "PATENT",
           "CCN", "DOCKET", "NAICS", "NCES", "SIC"):
    _NORMALIZERS[_k] = _id_strip0
for _k in ("FIPS", "ZIP"):
    _NORMALIZERS[_k] = _code_keep0
_NORMALIZERS["COUNTRY"] = _country
for _k in ("NAME", "ADDRESS"):
    _NORMALIZERS[_k] = _name


def normalize_sql(key: str, col: str) -> str:
    """SQL expression canonicalizing `col` for an equi-join on `key`."""
    fn = _NORMALIZERS.get(key, _code_keep0)
    return fn(col)


def quote_ident(name: str) -> str:
    """Quote a Snowflake identifier (landing columns can be odd)."""
    return '"' + str(name).replace('"', '""') + '"'
