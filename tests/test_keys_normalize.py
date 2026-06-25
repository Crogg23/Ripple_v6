"""Normalizer tests — offline assert the generated SQL shape, live assert behavior."""

import pytest

from connect.keys import normalize_sql


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
