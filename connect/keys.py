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


# Connect-local exact-token-set keys (2026-08-05 ingestion-sweep wiring).
# The shared portal tagger can't express "COMPANY_NUMBER is an ID, COMPANY_NAME is
# a name": 'company' is a NAME token, and a pair-rule in tag_portal_index would be
# applied to the UNION of a dataset's tokens there, tagging any table that has both
# a company column and any *_NUMBER column. So this rule fires ONLY when a single
# column's token set matches EXACTLY -- verified live 2026-08-05: the only landing
# columns tokenizing to {company, number} are UK_COMPANIES_HOUSE_PSC.COMPANY_NUMBER
# and INT_UK_COMPANIES_HOUSE.CompanyNumber (both 8-char UK Companies House numbers;
# the Utah portal's PARENT_COMPANY_DB_NUMBER has an extra 'db'/'parent' token and
# is excluded by exactness). The portal index and ENTITY_KEYS are untouched.
EXACT_TOKEN_KEYS: dict[frozenset, tuple[str, str]] = {
    frozenset({"company", "number"}): ("COMPANY_NO", "STEEL"),
}


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
    exact = EXACT_TOKEN_KEYS.get(frozenset(tk))
    if exact:
        return exact
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


def key_tier(key: str) -> str | None:
    """Tier of a key label, covering BOTH the shared tagger's KEY_TOKENS and the
    connect-local EXACT_TOKEN_KEYS (which never appear in KEY_TOKENS -- callers
    that index KEY_TOKENS[key][0] directly crash on those; use this instead)."""
    if key in KEY_TOKENS:
        return KEY_TOKENS[key][0]
    for k, tier in EXACT_TOKEN_KEYS.values():
        if k == key:
            return tier
    return None


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
#   code    : keep leading zeros, strip punctuation, upper (FIPS/NAICS/docket)
#   zip5  N : US ZIP -> first N digits (ZIP+4 collapses to ZIP5); NULL if < N digits
#   country : upper letters only (ISO)
#   name    : upper, punctuation -> single space, trim (fuzzy by nature)
# --------------------------------------------------------------------------- #
NORM_RULES: dict[str, tuple[str, int]] = {
    "NPI": ("pad", 10), "EIN": ("pad", 9), "DUNS": ("pad", 9), "CIK": ("pad", 10),
    "CCN": ("pad", 6), "IMO": ("imo", 7), "MMSI": ("pad", 9),
    "UEI": ("fixed", 12), "LEI": ("fixed", 20), "DEA_NO": ("alnum_upper", 0),
    # COMPANY_NO -- UK Companies House company number (2026-08-05 wiring). Uniformly
    # 8 chars on BOTH landing sides (verified live: PSC 7,000,000/7,000,000 rows len 8;
    # CH registry 5,734,779/5,734,780 len 8, one NULL). Alphanumeric ('SC316600',
    # 'NI626580', '00000133'), zero-padded at source, so 'fixed' -- anything not
    # exactly 8 chars is dirty input, not a paddable value. Single namespace by
    # construction: only the two UK Companies House tables carry this key.
    "COMPANY_NO": ("fixed", 8),
    "NAICS": ("code", 0), "SIC": ("code", 0), "NCES": ("code", 0),
    "DOCKET": ("code", 0), "PATENT": ("code", 0), "FIPS": ("code", 0), "ZIP": ("zip5", 5),
    "COUNTRY": ("country", 0),
    # Politician IDs (Step-K politics). Both are opaque member IDs, not zero-
    # significant numeric codes, so 'alnum_upper': strip punctuation, upper-case, NO
    # width pad and NO leading-zero stripping. Verified against live values --
    # BIOGUIDE 'B001261' (1 letter + 6 digits), ICPSR '40305'/'5611' (small integer,
    # never zero-padded); the empty-string ICPSR placeholder NULLs out via NULLIF.
    "BIOGUIDE": ("alnum_upper", 0), "ICPSR": ("alnum_upper", 0),
    # --- Added 2026-07-30 (spine wiring pass). Every width/mode below was read off
    # LIVE values, not assumed -- see the sample evidence in each comment.
    #
    # FRS_ID -- EPA's Facility Registry Service ID. 12-digit numeric, uniform in both
    # spellings (ECHO's FRS_ID and the FRS registry's REGISTRY_ID), e.g.
    # '110003665793'. 'fixed' rather than 'pad': a 12-digit FRS ID is never written
    # short, so anything not exactly 12 chars is dirty input, not a paddable value.
    "FRS_ID": ("fixed", 12),
    # PWSID -- EPA Public Water System ID. 2-letter state prefix + 7 digits, always
    # 9 chars, e.g. 'FL6581003' / 'GA0310233'. Alphanumeric, so 'fixed' (pad-mode
    # would reject it outright for containing letters).
    "PWSID": ("fixed", 9),
    # MINE_ID -- MSHA mine ID. CAUTION, this one is a trap: the landing values are
    # 7-digit numbers WRAPPED IN LITERAL DOUBLE QUOTES ('"1600354"') from a bad CSV
    # parse, which is why a naive LENGTH() reads 9 and a naive 'fixed 9' rule would
    # key on the quotes and never join anything. _alnum() strips the quotes, leaving
    # a uniform 7-digit numeric value -- verified across BOTH MSHA tables (0 rows of
    # any other stripped length, 0 alpha chars), and 13,338 of 13,489 accident mines
    # then join to the violations table. Hence pad-7.
    "MINE_ID": ("pad", 7),
    # FEC committee / candidate IDs -- 9-char alphanumeric with a meaningful letter
    # prefix ('C00035006' committee; 'H0NJ07261' / 'S4WV00159' candidate, where the
    # letter is the chamber). Opaque IDs, so alnum_upper: no width pad, no
    # leading-zero stripping. Kept as TWO distinct keys on purpose -- see the
    # PAIR_RULES comment in portal_recon/tag_portal_index.py; fusing them would put
    # a PAC and a human in one entity.
    "FEC_CMTE_ID": ("alnum_upper", 0), "FEC_CAND_ID": ("alnum_upper", 0),
    # Names: token-SORT + strip legal-suffix / credential noise, so 'SMITH, JOHN MD'
    # == 'JOHN SMITH' and 'Memorial Health Inc' == 'HEALTH MEMORIAL'. PERSON is a
    # distinct key (person-name columns) but shares the canonicalizer for now.
    "NAME": ("name_canon", 0), "PERSON": ("name_canon", 0),
    # Address: standardize street-type abbreviations; do NOT sort (order matters).
    "ADDRESS": ("address", 0),
}

# --- 2026-08 spine batch (STAGED behind one flag) ----------------------------- #
# Five new key axes, all verified live 2026-08-17 before staging (evidence:
# reports/census_grid_2026-08-12/fill/courtlistener_edges.json and
# spine_batch_verification.jsonl):
#   CL_PERSON_ID -- CourtListener judge/person PK: plain integer ('370'), no
#                   leading zeros -> alnum_upper (opaque ID, no pad).
#   CL_COURT_ID  -- CourtListener court PK: lowercase slug ('scotus', 'ca9')
#                   -> alnum_upper canonicalizes case.
#   NPDES_ID     -- EPA water-discharge permit ID ('AK0000345'): 2-letter state
#                   prefix + digits; 100.0% referential across all 7 event
#                   tables vs the 1.21M-facility authority table.
#   NCUA_CHARTER -- NCUA credit-union charter number (integer, no leading-zero
#                   convention); 98-100% referential vs the insured-CU list
#                   (merged-away charters legitimately absent from the current
#                   quarter's list).
#   ICE_FACILITY -- ICE detention facility code ('CSCNCAADULT'-style); 100.0%
#                   of 2.6M detention stints match the 1,470-code authority.
# All five are single-publisher namespaces and deliberately NOT in
# KEY_TOKENS/EXACT_TOKEN_KEYS: their carrying columns have generic names
# (PERSON_ID, COURT_ID, CU_NUMBER...) that token detection would mis-tag in
# unrelated sources. The spine specs pin exact columns instead
# (entity_index_specs.SPINE_BATCH_2026_08_DISPLAY_SPECS).
#
# THE FLAG: flipping this changes the incremental-config fingerprint, which
# freezes `connect-one`/`connect-changed` until the next FULL spine rebuild
# re-pins it (incremental._guard_config, by design). The full rebuild is a
# parked money decision (~$10-15). So the whole batch ships dark: flip to True
# in the same session that runs `python -m connect spine`, never before.
ENABLE_SPINE_BATCH_2026_08 = True

_SPINE_BATCH_NORM_RULES: dict[str, tuple[str, int]] = {
    "CL_PERSON_ID": ("alnum_upper", 0),
    "CL_COURT_ID": ("alnum_upper", 0),
    "NPDES_ID": ("alnum_upper", 0),
    "NCUA_CHARTER": ("alnum_upper", 0),
    "ICE_FACILITY": ("alnum_upper", 0),
}
if ENABLE_SPINE_BATCH_2026_08:
    NORM_RULES.update(_SPINE_BATCH_NORM_RULES)

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
    """Token-sorted, noise-stripped name: order- and suffix-insensitive matching.

    FILTER, not ARRAY_EXCEPT. ARRAY_EXCEPT is a MULTISET difference in Snowflake:
    it removes one occurrence per element of the second array, so
    'ACME HOLDINGS GROUP HOLDINGS' kept a stray second HOLDINGS while
    'ACME HOLDINGS GROUP' dropped its only one -- the two canonicalized
    differently and the same org failed to match itself. FILTER removes EVERY
    occurrence of a noise token while preserving duplicates of REAL tokens
    (ARRAY_DISTINCT would have collapsed those too, silently re-keying names).
    """
    base = f"TRIM(REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' '))"
    noise = ", ".join(f"'{t}'" for t in _NAME_NOISE)
    return (f"NULLIF(ARRAY_TO_STRING(ARRAY_SORT(FILTER("
            f"SPLIT({base}, ' '), t -> NOT ARRAY_CONTAINS(t, ARRAY_CONSTRUCT({noise})))), ' '), '')")


def _addr_canon(col: str) -> str:
    """Standardize street-type words, order preserved (address order is meaningful).

    TRANSFORM over tokens, not REPLACE chains. REPLACE(' ...NORTH NORTH...',
    ' NORTH ', ' N ') only replaces NON-OVERLAPPING matches left to right: the two
    NORTHs share the space between them, so replacing the first consumes it and the
    second NORTH never matches its own leading space -- '100 NORTH NORTH STREET'
    canonicalized to '100 N NORTH ST' (second NORTH untouched), while a differently
    -formatted repeat like '2 SOUTH SOUTH SOUTH RD' came out '2 S SOUTH S RD'
    (alternating hits and misses). Both are real addresses (a "North North Street"
    exists; a road can appear twice in an inconsistently-formatted feed). Token-wise
    TRANSFORM converts every occurrence independently, so repeats behave uniformly:
    '2 SOUTH SOUTH SOUTH RD' -> '2 S S S RD'.
    """
    base = f"TRIM(REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' '))"
    whens = " ".join(f"WHEN '{long}' THEN '{short}'" for long, short in _ADDR_ABBR)
    return (f"NULLIF(ARRAY_TO_STRING(TRANSFORM(SPLIT({base}, ' '), "
            f"x -> CASE x::VARCHAR {whens} ELSE x::VARCHAR END), ' '), '')")


# Normalized (letters-only, upper) spellings that mean "United States" in landing
# country columns. Checked AFTER the 'country' normalizer, so 'U.S.', 'us', 'U S A'
# all collapse into these. Blank/NULL country passes the gate: unknown is not foreign.
US_COUNTRY_ALIASES = ("US", "USA", "UNITEDSTATES", "UNITEDSTATESOFAMERICA")


# Keyboard-walk placeholders seen in ID columns across the Library (spine audit
# 2026-08-11). Repeated-digit fillers are handled structurally in pad mode; these
# are the sequential ones no structural rule catches. Never issued as real IDs.
PAD_PLACEHOLDERS = (
    "123456789", "987654321", "1234567890", "0987654321",
    "12345678", "87654321", "123456", "654321",
)


def normalize_sql(key: str, col: str, country_col: str | None = None) -> str:
    """SQL expression canonicalizing `col` for an equi-join on `key`.

    Raises on an unmapped value key -- fail loud, never silently mis-canonicalize
    (the old code fell back to a keep-zeros default, hiding newly-added keys).

    country_col (ZIP only, Chris-approved 2026-08-09): when the table carries a
    country column, pass it (quoted) and the ZIP normalizer returns NULL for rows
    whose country is present and NOT a US spelling. Closes the residual foreign-
    postal trap the length gate can't ('Y21 T449' Eircode -> '21449', a real VA
    ZIP; 'KY1-1106' Cayman -> '11106', a real NY ZIP). Rows with no country info
    still pass -- the gate narrows, it never widens.
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
        # 2026-07-28: also require digits-only. _alnum() strips punctuation but KEEPS
        # letters, so a text sentinel (e.g. NPPES EIN's literal '<UNAVAIL>' -> 'UNAVAIL'
        # after stripping) would otherwise pad to a plausible-looking 9-char value
        # instead of being rejected -- every pad-mode key (NPI/EIN/DUNS/CIK/CCN/MMSI) is
        # purely numeric, so a letter anywhere means dirty input, not a real ID.
        # 2026-08-11 spine audit: all-zeros was not the only filler. EIN
        # '999999999' merged CVS, SK Telecom, Kingsway Financial, Enstar and a
        # literal 'TEST Company' into ONE entity across 16 sources -- filers who
        # can't or won't give an ID type a placeholder, and a placeholder shared
        # by N filers is a false merge. So NULL any value that is a single digit
        # repeated (>=4 long, before OR after padding: '9999999' and '99-9999999'
        # are the same filler) and the keyboard-walk sequentials. These are not
        # issued as real EIN/NPI/CCN values, and dropping is the safe direction:
        # a lost row is a missing edge, a false merge accuses the wrong company.
        padded = f"LPAD({clean}, {width}, '0')"
        placeholders = ", ".join(f"'{v}'" for v in PAD_PLACEHOLDERS)
        return (f"CASE WHEN LENGTH({clean}) = 0 OR LENGTH({clean}) > {width} "
                f"OR NOT REGEXP_LIKE({clean}, '^[0-9]+$') "
                f"OR {padded} = REPEAT('0', {width}) "
                f"OR (LENGTH({clean}) >= 4 AND {clean} = REPEAT(LEFT({clean}, 1), LENGTH({clean}))) "
                f"OR {padded} = REPEAT(LEFT({padded}, 1), {width}) "
                f"OR {clean} IN ({placeholders}) OR {padded} IN ({placeholders}) THEN NULL "
                f"ELSE {padded} END")
    if mode == "fixed":
        return f"CASE WHEN LENGTH({clean}) = {width} THEN {clean} ELSE NULL END"
    if mode == "code":
        return f"NULLIF({clean}, '')"
    if mode == "zip5":
        # D18: US ZIP -> first `width` digits, so a ZIP+4 (NPPES '021151234' or
        # '02115-1234') equi-joins a ZIP5 (LEIE '02115'). Before this, ZIP used 'code'
        # (no truncation) so the 8.7M ZIP9 rows in NPPES could never match any ZIP5
        # store. Digits only; a numeric ZIP that lost its leading zero is DROPPED,
        # never risked as a false match.
        #
        # 2026-07-31: the gate was `>= width`, which did not do what the line above
        # claims. A ZIP+4 int-cast through a CSV load loses its leading zero and
        # arrives 8 digits ('21151234' for 02115-1234); `>= 5` accepted it and LEFT-5
        # produced '21151' -- a real, WRONG, Pennsylvania ZIP silently standing in for
        # a Boston one. Same for any 6/7-digit run (foreign postal codes). Only the two
        # lengths a real US ZIP can have are accepted: 5 (ZIP5) and 9 (ZIP+4).
        digits = f"REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9]', '')"
        expr = (f"CASE WHEN LENGTH({digits}) IN ({width}, {width + 4}) "
                f"THEN LEFT({digits}, {width}) ELSE NULL END")
        if country_col:
            cnorm = f"UPPER(REGEXP_REPLACE(TO_VARCHAR({country_col}), '[^A-Za-z]', ''))"
            aliases = ", ".join(f"'{a}'" for a in US_COUNTRY_ALIASES)
            expr = (f"CASE WHEN COALESCE({cnorm}, '') = '' "
                    f"OR {cnorm} IN ({aliases}) THEN {expr} ELSE NULL END")
        return expr
    if mode == "country":
        return f"NULLIF(UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^A-Za-z]', '')), '')"
    raise KeyError(f"Unknown norm mode '{mode}' for key '{key}'.")


def quote_ident(name: str) -> str:
    """Quote a Snowflake identifier (landing columns can be odd)."""
    return '"' + str(name).replace('"', '""') + '"'
