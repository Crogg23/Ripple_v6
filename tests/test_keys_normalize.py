"""Normalizer tests — offline assert the generated SQL shape, live assert behavior."""

import pytest

from connect import keys
from connect.keys import detect_key, normalize_sql


# ---- offline: the SQL the normalizer emits -------------------------------- #
def test_name_token_sorts_and_strips_noise():
    sql = normalize_sql("NAME", "X")
    assert "ARRAY_SORT" in sql and "ARRAY_EXCEPT" in sql      # token-sorted
    assert "'INC'" in sql and "'LLC'" in sql and "'MD'" in sql  # noise stripped


def test_person_shares_the_name_canonicalizer():
    assert normalize_sql("PERSON", "X") == normalize_sql("NAME", "X")


def test_address_standardizes_but_does_not_sort():
    sql = normalize_sql("ADDRESS", "X")
    assert "STREET" in sql and "AVENUE" in sql and "REPLACE" in sql
    assert "ARRAY_SORT" not in sql      # address order is meaningful


def test_npi_pads_to_ten_never_strips():
    sql = normalize_sql("NPI", "X")
    assert "LPAD" in sql and "10" in sql


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
def test_bioguide_icpsr_roundtrip_real_values(sf):
    # BIOGUIDE: case-normalized, empty -> NULL. ICPSR: integer kept as-is (no zero
    # strip), empty -> NULL. Verified against live LANDING sample values.
    assert _norm(sf, "BIOGUIDE", "B001261") == "B001261"
    assert _norm(sf, "BIOGUIDE", "b001261") == "B001261"
    assert _norm(sf, "BIOGUIDE", "") is None
    assert _norm(sf, "ICPSR", "40305") == "40305"
    assert _norm(sf, "ICPSR", "5611") == "5611"
    assert _norm(sf, "ICPSR", "") is None
