"""Guard for connect/normalize.py — the name/addr SQL lifted from the
retired full-rebuild module on 2026-08-30. Pins the exact strings the two
live importers (entity_index, incremental) depend on, so a future edit
that changes the SQL shape fails loudly instead of drifting silently."""
from connect.normalize import _addr_expr, _name_expr


def test_name_expr_org_only():
    assert _name_expr({"org": "ORG_NAME"}) == (
        "NULLIF(NULLIF(TRIM(\"ORG_NAME\"), ''), 'nan')"
    )


def test_name_expr_person_only():
    assert _name_expr({"person": ("LAST", "FIRST")}) == (
        "NULLIF(TRIM(\"LAST\") || ', ' || TRIM(\"FIRST\"), ', ')"
    )


def test_name_expr_org_and_person_coalesces():
    out = _name_expr({"org": "ORG", "person": ("L", "F")})
    assert out.startswith("COALESCE(") and "'nan'" in out


def test_name_expr_empty_spec_is_null():
    assert _name_expr({}) == "CAST(NULL AS STRING)"


def test_addr_expr_city_state_zip():
    out = _addr_expr({"city": "CITY", "state": "ST", "zip": "ZIP"})
    assert out == (
        "NULLIF(TRIM(TRIM(COALESCE(\"CITY\", '')) || ' ' || "
        "TRIM(COALESCE(\"ST\", '')) || ' ' || TRIM(COALESCE(\"ZIP\", ''))), '')"
    )


def test_addr_expr_empty_spec_is_null():
    assert _addr_expr({}) == "CAST(NULL AS STRING)"
