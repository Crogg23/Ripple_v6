"""Pins the 2026-09-23 catalog-audit key rules.

Every case below was a real mart column whose sampled values proved the old
label wrong (audit/catalog_audit_2026-09-23_verdict.md).
"""

from connect.keys import CATALOG_KEYS, NORM_RULES, TABLE_COLUMN_KEYS, catalog_key, detect_key


def test_a_describing_word_kills_the_hard_key():
    # Y/N flags, dates, types, counts, booleans, tickers, zip extensions
    for col in ("MULTIPLE_NPI_FLAG", "NPI_DEACTIVATION_DATE", "CCN_FACILITY_TYPE",
                "ISSUER_CIK_NONE", "NPI_IS_REAL", "PRIOR_DEA_REPORTS", "CIK_TICKER",
                "EIN_NTEE", "CONTRIBUTOR_ZIP_EXT", "RECIPIENT_ZIP_LAST_4_CODE"):
        assert detect_key(col) == (None, None), col


def test_a_where_or_who_word_takes_over_from_the_hard_key():
    assert detect_key("EIN_ZIP5") == ("ZIP", "GEO")
    assert detect_key("CCN_NAME") == ("NAME", "PROBABILISTIC")


def test_real_keys_still_fire():
    for col, key in (("NPI", "NPI"), ("PRSCRBR_NPI", "NPI"), ("RECIPIENT_EIN", "EIN"),
                     ("BUYER_DEA_NO", "DEA_NO"), ("CMTE_ID", "FEC_CMTE_ID"),
                     ("REGISTRY_ID", "FRS_ID"), ("LAST_NAME", "NAME"),
                     ("LAST_RPT_SPONS_EIN", "EIN")):   # skeptic 2026-09-23: 'last' is part of this ID's name
        assert detect_key(col)[0] == key, col


def test_catalog_only_keys_stay_out_of_the_engine():
    # TABLE_COLUMN_KEYS and NORM_RULES are pinned by connect/incremental.py;
    # anything added there forces an apply-config reslice.
    assert not set(CATALOG_KEYS) & set(TABLE_COLUMN_KEYS)
    assert "ACCESSION" not in NORM_RULES


def test_what_codes_and_their_vetoes():
    assert catalog_key("X__Y", "HCPCS_CD") == ("HCPCS", "THING")
    assert catalog_key("X__Y", "TOT_HCPCS_CDS") == (None, None)   # a count
    assert catalog_key("X__Y", "CFDA_TITLE") == (None, None)      # text
    assert catalog_key("ECONOMICS__FED_SEC_EDGAR", "ACCESSIONNUMBER") == ("ACCESSION", "STEEL")
