"""Normalizer tests — offline assert the generated SQL shape, live assert behavior."""

import pytest

from connect import keys
from connect.keys import detect_key, normalize_sql


# ---- offline: the SQL the normalizer emits -------------------------------- #
def test_name_token_sorts_and_strips_noise():
    sql = normalize_sql("NAME", "X")
    assert "ARRAY_SORT" in sql and "FILTER" in sql            # token-sorted
    assert "'INC'" in sql and "'LLC'" in sql and "'MD'" in sql  # noise stripped


def test_name_strips_noise_with_filter_not_array_except():
    """ARRAY_EXCEPT is a MULTISET difference in Snowflake -- it removes ONE
    occurrence per element of the second array. 'ACME HOLDINGS GROUP HOLDINGS' kept
    a stray second HOLDINGS while 'ACME HOLDINGS GROUP' dropped its only one, so the
    same org canonicalized two ways and failed to match itself. FILTER removes every
    occurrence. ARRAY_DISTINCT would also have worked but would have collapsed
    duplicates of REAL tokens too, silently re-keying legitimate names."""
    sql = normalize_sql("NAME", "X")
    assert "ARRAY_EXCEPT" not in sql
    assert "ARRAY_CONTAINS" in sql and "ARRAY_DISTINCT" not in sql


def test_person_shares_the_name_canonicalizer():
    assert normalize_sql("PERSON", "X") == normalize_sql("NAME", "X")


def test_address_standardizes_but_does_not_sort():
    sql = normalize_sql("ADDRESS", "X")
    assert "STREET" in sql and "AVENUE" in sql and "TRANSFORM" in sql
    assert "ARRAY_SORT" not in sql      # address order is meaningful


def test_address_uses_transform_not_replace_chain():
    """REPLACE(' NORTH NORTH ', ' NORTH ', ' N ') only fires on non-overlapping
    matches: two adjacent NORTHs share one space, so replacing the first consumes
    it and the second NORTH never matches its own leading space. Verified live:
    '100 NORTH NORTH STREET' canonicalized to '100 N NORTH ST' (second NORTH
    untouched) and '2 SOUTH SOUTH SOUTH RD' to '2 S SOUTH S RD' (alternating hits
    and misses). TRANSFORM converts every token independently, so repeats behave
    uniformly regardless of position."""
    sql = normalize_sql("ADDRESS", "X")
    # REGEXP_REPLACE (structural cleanup) is fine; a chained bare REPLACE(...,
    # ' NORTH ', ' N ') per abbreviation -- the old, buggy approach -- is not.
    assert "', ' N '" not in sql and "REPLACE(' " not in sql
    assert "TRANSFORM(SPLIT(" in sql


def test_npi_pads_to_ten_never_strips():
    sql = normalize_sql("NPI", "X")
    assert "LPAD" in sql and "10" in sql


def test_zip_accepts_only_real_us_zip_lengths():
    """The gate was `>= 5`, which did not match its own comment. A ZIP+4 int-cast
    through a CSV load loses its leading zero and arrives 8 digits ('21151234' for
    02115-1234); `>= 5` accepted it and LEFT-5 produced '21151' -- a real, WRONG
    Pennsylvania ZIP standing in for a Boston one, with nothing to flag it. Only 5
    (ZIP5) and 9 (ZIP+4) are lengths a real US ZIP can have."""
    sql = normalize_sql("ZIP", "X")
    assert "IN (5, 9)" in sql
    assert ">= 5" not in sql       # the old permissive gate must be gone
    assert "LEFT(" in sql and ", 5)" in sql


def test_unknown_key_fails_loud():
    with pytest.raises(KeyError):
        normalize_sql("NOT_A_KEY", "X")


# ---- alnum_upper mode (Step-K enabler: was a KeyError before) -------------- #
def test_alnum_upper_mode_emits_clean_id_sql(monkeypatch):
    # A Step-K key declares ("alnum_upper", 0). Before the fix this raised
    # "Unknown norm mode". Now it canonicalizes: alnum + upper + NULLIF empty,
    # with NO width pad and NO leading-zero stripping (opaque IDs like TAIL/BIOGUIDE).
    monkeypatch.setitem(keys.NORM_RULES, "TAILX", ("alnum_upper", 0))
    sql = normalize_sql("TAILX", '"N_NUMBER"')
    assert "UPPER" in sql and "NULLIF" in sql
    assert "LPAD" not in sql          # not width-padded
    assert "ARRAY_SORT" not in sql    # not a name


# ---- detect_key picks the STRONGEST tier, order-independently -------------- #
def test_detect_key_basic_single_match():
    assert detect_key("ein_number") == ("EIN", "STEEL")
    assert detect_key("the_geom") == ("GEOM", "GEO")
    assert detect_key("nothing_here") == (None, None)


def test_detect_bioguide_and_icpsr_member_columns():
    # Step-K politics: BIOGUIDE + ICPSR are first-class STEEL member keys.
    assert detect_key("BIOGUIDE") == ("BIOGUIDE", "STEEL")
    assert detect_key("BIOGUIDE_ID") == ("BIOGUIDE", "STEEL")   # Voteview's name
    assert detect_key("ICPSR") == ("ICPSR", "STEEL")
    assert detect_key("ICPSR_ID") == ("ICPSR", "STEEL")


def test_detect_key_excludes_state_icpsr_false_friend():
    # STATE_ICPSR is a STATE code (tokens {icpsr, state}), NOT the member key ICPSR.
    # The 'state' exclusion token must veto the ICPSR match -> no tag.
    assert detect_key("STATE_ICPSR") == (None, None)
    assert "state" in keys.KEY_EXCLUDE["ICPSR"]


def test_bioguide_icpsr_normalize_as_opaque_ids():
    # alnum_upper: strip punctuation + upper, NO width pad, NO leading-zero strip.
    for k in ("BIOGUIDE", "ICPSR"):
        sql = normalize_sql(k, "X")
        assert "UPPER" in sql and "NULLIF" in sql
        assert "LPAD" not in sql          # not width-padded (would corrupt ICPSR ints)
        assert "ARRAY_SORT" not in sql    # not a name


def test_detect_key_strongest_tier_even_when_appended_last(monkeypatch):
    # Simulate a Step-K add: a NEW STEEL key appended to the END of KEY_TOKENS
    # (after the GEO/PROBABILISTIC keys) whose token also matches a column that
    # hits a weaker key. The OLD first-match-in-dict-order code returned the weaker
    # GEO key; detect_key must now return the STEEL one regardless of position.
    patched = dict(keys.KEY_TOKENS)
    patched["ZIPSTEEL"] = ("STEEL", {"zip"})   # 'zip' also matches the GEO key ZIP
    monkeypatch.setattr(keys, "KEY_TOKENS", patched)
    key, tier = detect_key("zip")
    assert tier == "STEEL" and key == "ZIPSTEEL"


# ---- vocabulary parity: the guard against the drift found on 2026-07-30 ---- #
# Three separate places name join keys, and they had silently diverged:
#   portal_recon/tag_portal_index.py KEY_TOKENS  -- what connect/ can DETECT
#   connect/keys.py NORM_RULES                  -- what connect/ can JOIN on
#   scripts/retier_join_keys.py STEEL_KEYS      -- what got WRITTEN to the registry
# The registry was advertising sources as "STEEL: FRS_ID" while normalize_sql
# raised KeyError on FRS_ID, so those sources could never actually be wired.
# These tests fail loudly if the three ever split again.
def test_every_entity_key_has_a_norm_rule():
    """Any STEEL/STRONG key the tagger can detect must be joinable, or the spine
    crashes the moment a source carrying it gets wired."""
    missing = sorted(k for k in keys.ENTITY_KEYS if k not in keys.NORM_RULES)
    assert not missing, (
        f"STEEL/STRONG keys in KEY_TOKENS with no NORM_RULES entry: {missing}. "
        f"normalize_sql() raises on these -- add a rule (with a width read off LIVE "
        f"values, not assumed) before any source keyed on them can be wired.")


def test_registry_side_key_vocabulary_is_joinable():
    """Every canonical key scripts/retier_join_keys.py can stamp into the registry
    must be joinable by connect/, EXCEPT the documented non-entity keys."""
    import importlib.util
    import pathlib

    path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "retier_join_keys.py"
    spec = importlib.util.spec_from_file_location("_retier", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Deliberately NOT spine entity keys (2026-07-30 call): an ACCESSION_NUMBER is a
    # FILING and a CUSIP is a SECURITY -- neither is a real-world actor, and making
    # them entities would bury every dossier under ~400M document "entities". They
    # belong as edges hanging off the CIK (company) axis instead. The rest are
    # genuine keys that simply have no spine wiring yet.
    NOT_ENTITY_KEYS = {"ACCESSION_NUMBER", "CUSIP", "RECALL_NUMBER"}
    # retier lumps FEC candidate+committee into one 'FEC_ID'; connect/ splits them
    # into FEC_CAND_ID / FEC_CMTE_ID on purpose (a PAC is not a person).
    RENAMED = {"FEC_ID", "NCES_ID", "DOCKET_ID"}

    unjoinable = sorted(
        k for k in mod.STEEL_KEYS
        if k not in keys.NORM_RULES and k not in NOT_ENTITY_KEYS and k not in RENAMED)
    assert not unjoinable, (
        f"retier_join_keys.py can stamp these into JOIN_KEYS_STD but connect/ cannot "
        f"join on them: {unjoinable}. Either add a NORM_RULES entry or add the key to "
        f"NOT_ENTITY_KEYS with a reason.")


def test_new_2026_07_30_axes_are_detectable_and_joinable():
    """The five keys added in the spine-wiring pass, end to end."""
    assert detect_key("FRS_ID") == ("FRS_ID", "STEEL")
    assert detect_key("REGISTRY_ID") == ("FRS_ID", "STEEL")   # EPA's other spelling
    assert detect_key("PWSID") == ("PWSID", "STEEL")
    assert detect_key("MINE_ID") == ("MINE_ID", "STEEL")
    assert detect_key("CMTE_ID") == ("FEC_CMTE_ID", "STEEL")
    assert detect_key("CAND_ID") == ("FEC_CAND_ID", "STEEL")
    for k in ("FRS_ID", "PWSID", "MINE_ID", "FEC_CMTE_ID", "FEC_CAND_ID"):
        normalize_sql(k, "X")      # must not raise


def test_mine_and_frs_false_friends_do_not_tag():
    # These live alongside the real key columns in the SAME tables. A bare-token
    # rule would have tagged all of them; the pair rules must not.
    assert detect_key("MINE_NAME") != ("MINE_ID", "STEEL")
    assert detect_key("MINE_TYPE") != ("MINE_ID", "STEEL")
    assert detect_key("MINE_EXPER") != ("MINE_ID", "STEEL")
    assert detect_key("FRS_FACILITY_DETAIL_REPORT_URL") != ("FRS_ID", "STEEL")


def test_mine_id_normalizer_survives_the_quoted_landing_values():
    """MSHA landing values are 7-digit IDs wrapped in literal double quotes
    ('"1600354"'). The emitted SQL must strip to digits and pad to 7, NOT key on
    the quote characters (which would make the column join to nothing)."""
    sql = normalize_sql("MINE_ID", "X")
    assert "LPAD" in sql and ", 7, '0'" in sql
    assert "[^0-9A-Za-z]" in sql          # the quote-stripping regex
    assert "'^[0-9]+$'" in sql            # digits-only guard rejects text sentinels


# ---- live: real Snowflake canonicalization -------------------------------- #
def _norm(sf, key, value):
    from connect import db
    return db.scalar(sf, f"SELECT {normalize_sql(key, 'V')} FROM (SELECT %s AS V)", (value,))


@pytest.mark.snowflake
@pytest.mark.parametrize("a,b", [
    ("Smith, John MD", "JOHN SMITH"),
    ("Memorial Health, Inc.", "MEMORIAL HEALTH"),
    ("FRANK, ALEXANDER", "Alexander Frank PLLC"),
])
def test_name_canon_collapses_variants(sf, a, b):
    assert _norm(sf, "NAME", a) == _norm(sf, "NAME", b)


@pytest.mark.snowflake
def test_address_canon_abbreviates(sf):
    assert _norm(sf, "ADDRESS", "100 North Main Street") == "100 N MAIN ST"


@pytest.mark.snowflake
def test_address_canon_handles_repeated_tokens(sf):
    """The REPLACE-chain bug, live. Both are real addresses -- inconsistent source
    formatting can genuinely repeat a directional/street-type word."""
    assert _norm(sf, "ADDRESS", "100 North North Street") == "100 N N ST"
    assert _norm(sf, "ADDRESS", "2 South South South Rd") == "2 S S S RD"


@pytest.mark.snowflake
def test_bioguide_icpsr_roundtrip_real_values(sf):
    # BIOGUIDE: case-normalized, empty -> NULL. ICPSR: integer kept as-is (no zero
    # strip), empty -> NULL. Verified against live LANDING sample values.
    assert _norm(sf, "BIOGUIDE", "B001261") == "B001261"
    assert _norm(sf, "BIOGUIDE", "b001261") == "B001261"
    assert _norm(sf, "BIOGUIDE", "") is None
    assert _norm(sf, "ICPSR", "40305") == "40305"
    assert _norm(sf, "ICPSR", "5611") == "5611"
    assert _norm(sf, "ICPSR", "") is None
