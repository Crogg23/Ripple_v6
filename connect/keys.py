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
    KEY_EXCLUDE,
    KEY_TOKENS,
    PAIR_RULES,
    TIER_ORDER,
    TIER_RANK,
    tokens,
)


def detect_key(column_name: str) -> tuple[str | None, str | None]:
    """Return (key_label, tier) for a single column, or (None, None).

    STRONGEST tier wins, computed explicitly via TIER_RANK -- NOT by relying on
    KEY_TOKENS insertion order. (A new STEEL key APPENDED to KEY_TOKENS during a
    Step-K key add would otherwise lose a first-match race to an earlier GEO/
    PROBABILISTIC token on an overlapping column. This makes selection order-
    independent.) Mirrors tag_columns' tier-sort, but per-column so we can pin
    which physical column carries the key.
    """
    tk = tokens(column_name)
    if not tk:
        return None, None
    best_key, best_tier = None, None
    for key, (tier, toks) in KEY_TOKENS.items():
        # A false-friend token vetoes the match (e.g. STATE_ICPSR -> {icpsr,state}
        # must NOT tag as ICPSR — the 'state' token is in KEY_EXCLUDE['ICPSR']).
        if tk & KEY_EXCLUDE.get(key, set()):
            continue
        if (tk & toks) and (best_tier is None or TIER_RANK[tier] < TIER_RANK[best_tier]):
            best_key, best_tier = key, tier
    if best_key is not None:
        return best_key, best_tier
    # No single-token match -> fall back to PAIR_RULES (e.g. postal+code -> ZIP),
    # again taking the strongest tier if several pair rules hit.
    for key, (a, b) in PAIR_RULES:
        if a in tk and b in tk:
            tier = KEY_TOKENS[key][0]
            if best_tier is None or TIER_RANK[tier] < TIER_RANK[best_tier]:
                best_key, best_tier = key, tier
    return best_key, best_tier


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
#   imo   N : digits only (tolerates an 'IMO' prefix, e.g. AIS 'IMO9187629');
#             keep iff exactly N digits and not the all-zero placeholder
#   fixed N : alnum, upper, keep ONLY if exactly N chars (UEI/LEI), else NULL
#   code    : keep leading zeros, strip punctuation, upper (FIPS/ZIP/NAICS/docket)
#   country : upper letters only (ISO)
#   name    : upper, punctuation -> single space, trim (fuzzy by nature)
# --------------------------------------------------------------------------- #
NORM_RULES: dict[str, tuple[str, int]] = {
    "NPI": ("pad", 10), "EIN": ("pad", 9), "DUNS": ("pad", 9), "CIK": ("pad", 10),
    "CCN": ("pad", 6), "IMO": ("imo", 7), "MMSI": ("pad", 9),
    "UEI": ("fixed", 12), "LEI": ("fixed", 20),
    "NAICS": ("code", 0), "SIC": ("code", 0), "NCES": ("code", 0),
    "DOCKET": ("code", 0), "PATENT": ("code", 0), "FIPS": ("code", 0), "ZIP": ("code", 0),
    "COUNTRY": ("country", 0),
    # Politician IDs (Step-K politics). Both are opaque member IDs, not zero-
    # significant numeric codes, so 'alnum_upper': strip punctuation, upper-case, NO
    # width pad and NO leading-zero stripping. Verified against live values --
    # BIOGUIDE 'B001261' (1 letter + 6 digits), ICPSR '40305'/'5611' (small integer,
    # never zero-padded); the empty-string ICPSR placeholder NULLs out via NULLIF.
    "BIOGUIDE": ("alnum_upper", 0), "ICPSR": ("alnum_upper", 0),
    # Names: token-SORT + strip legal-suffix / credential noise, so 'SMITH, JOHN MD'
    # == 'JOHN SMITH' and 'Memorial Health Inc' == 'HEALTH MEMORIAL'. PERSON is a
    # distinct key (person-name columns) but shares the canonicalizer for now.
    "NAME": ("name_canon", 0), "PERSON": ("name_canon", 0),
    # Address: standardize street-type abbreviations; do NOT sort (order matters).
    "ADDRESS": ("address", 0),
}

# tokens dropped from a name before matching (legal suffixes + person credentials +
# a few stopwords). Sorted set so the generated SQL is stable across runs.
_NAME_NOISE = sorted({
    "INC", "INCORPORATED", "LLC", "LLP", "LP", "LTD", "CO", "CORP", "CORPORATION",
    "COMPANY", "PC", "PLLC", "PA", "PLC", "GROUP", "HOLDINGS", "THE", "AND", "OF",
    "MD", "DO", "DDS", "DMD", "RN", "NP", "PHD", "ESQ", "JR", "SR", "II", "III", "IV",
    "MR", "MRS", "MS", "DR",
})

# street-type abbreviations (longest forms -> USPS short forms)
_ADDR_ABBR = [
    ("STREET", "ST"), ("AVENUE", "AVE"), ("BOULEVARD", "BLVD"), ("ROAD", "RD"),
    ("DRIVE", "DR"), ("LANE", "LN"), ("COURT", "CT"), ("PLACE", "PL"),
    ("SUITE", "STE"), ("APARTMENT", "APT"), ("BUILDING", "BLDG"),
    ("NORTH", "N"), ("SOUTH", "S"), ("EAST", "E"), ("WEST", "W"),
]


def _alnum(col: str) -> str:
    return f"UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9A-Za-z]', ''))"


def _name_canon(col: str) -> str:
    """Token-sorted, noise-stripped name: order- and suffix-insensitive matching."""
    base = f"TRIM(REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' '))"
    noise = ", ".join(f"'{t}'" for t in _NAME_NOISE)
    return (f"NULLIF(ARRAY_TO_STRING(ARRAY_SORT(ARRAY_EXCEPT("
            f"SPLIT({base}, ' '), ARRAY_CONSTRUCT({noise}))), ' '), '')")


def _addr_canon(col: str) -> str:
    """Standardize street-type words on a space-padded string, then collapse."""
    expr = f"' ' || REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' ') || ' '"
    for long, short in _ADDR_ABBR:
        expr = f"REPLACE({expr}, ' {long} ', ' {short} ')"
    return f"NULLIF(TRIM(REGEXP_REPLACE({expr}, ' +', ' ')), '')"


def normalize_sql(key: str, col: str) -> str:
    """SQL expression canonicalizing `col` for an equi-join on `key`.

    Raises on an unmapped value key -- fail loud, never silently mis-canonicalize
    (the old code fell back to a keep-zeros default, hiding newly-added keys).
    """
    if key not in NORM_RULES:
        raise KeyError(f"No NORM_RULES entry for key '{key}'. Add one before joining on it.")
    mode, width = NORM_RULES[key]
    if mode == "name_canon":
        return _name_canon(col)
    if mode == "address":
        return _addr_canon(col)
    if mode == "imo":
        # AIS broadcasts 'IMO9187629'; OFAC stores bare '9187629' — both are the same
        # hull. Take digits only (the 'IMO' letters drop out), keep iff exactly N
        # digits and not the all-zero non-IMO placeholder. No leading-zero stripping.
        digits = f"REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9]', '')"
        return (f"CASE WHEN LENGTH({digits}) <> {width} OR {digits} = REPEAT('0', {width}) "
                f"THEN NULL ELSE {digits} END")
    clean = _alnum(col)
    if mode == "alnum_upper":
        # Variable-length alphanumeric entity IDs: BIOGUIDE ('S000148'), TAIL_NUMBER
        # ('N12345'), ICAO24 (hex), ORI. Strip punctuation, upper-case, NO width
        # constraint and NO leading-zero stripping. (Canonicalization matches 'code'
        # today, but it's a DISTINCT named mode on purpose -- an opaque ID, not a
        # zero-significant numeric code -- so Step-K NORM_RULES can declare it
        # explicitly and the two can diverge later without a silent behaviour change.)
        return f"NULLIF({clean}, '')"
    if mode == "pad":
        # NULL the all-zero placeholder too (e.g. LEIE NPI '0000000000' on ~90% of
        # rows, discovery sweep #1): a zero-filled ID is never a real entity, and
        # left unguarded it fans out -- one placeholder on the active side would
        # match every placeholder on the flag side. Width-padded so '0','00',... all collapse.
        return (f"CASE WHEN LENGTH({clean}) = 0 OR LENGTH({clean}) > {width} "
                f"OR LPAD({clean}, {width}, '0') = REPEAT('0', {width}) THEN NULL "
                f"ELSE LPAD({clean}, {width}, '0') END")
    if mode == "fixed":
        return f"CASE WHEN LENGTH({clean}) = {width} THEN {clean} ELSE NULL END"
    if mode == "code":
        return f"NULLIF({clean}, '')"
    if mode == "country":
        return f"NULLIF(UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^A-Za-z]', '')), '')"
    raise KeyError(f"Unknown norm mode '{mode}' for key '{key}'.")


def quote_ident(name: str) -> str:
    """Quote a Snowflake identifier (landing columns can be odd)."""
    return '"' + str(name).replace('"', '""') + '"'
