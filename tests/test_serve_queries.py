"""Tests for serve/serve_queries.py -- every read query the Atlas makes.
2026-07-31: serve/ had zero test coverage. Covers the pure helpers
(normalize_sql, entity_id_for, safe_json, preview_pairs) and the SQL/bind-param
shape of every query function, via a monkeypatched run_df that captures what
was actually sent instead of hitting Snowflake. Query functions are wrapped in
@st.cache_data -- .clear() before each call so a prior test's cached result
can't leak into the next test's assertions.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "serve"))

import serve_queries as q  # noqa: E402


@pytest.fixture(autouse=True)
def _clear_streamlit_caches():
    """st.cache_data caches across calls even outside a real Streamlit app --
    without this, test B calling a function with the same args as test A
    could silently get test A's captured (mocked) result instead of running
    against test B's own monkeypatched run_df."""
    for fn in (q.resolve_hard_id, q.search_names, q.search_sources, q.get_dossier,
              q.get_affiliations, q.get_source, q.normalize_name):
        fn.clear()
    yield


def _capture_run_df(monkeypatch):
    calls = []

    def fake(sql, params=None):
        calls.append((sql, params))
        return "RESULT"
    monkeypatch.setattr(q, "run_df", fake)
    return calls


# --------------------------------------------------------------------------- #
# pure helpers
# --------------------------------------------------------------------------- #
def test_entity_id_for_matches_the_spine_scheme():
    """Must match connect/keys.py's ENTITY_ID = 'ENT_' || LEFT(MD5(key_type|val), 16)
    exactly -- this is how the Atlas deep-links a facility (CCN) from an
    affiliation row without an extra round-trip query."""
    import hashlib
    key_type, key_value = "CCN", "123456"
    expected = "ENT_" + hashlib.md5(f"{key_type}|{key_value}".encode()).hexdigest()[:16]
    assert q.entity_id_for(key_type, key_value) == expected


def test_entity_id_for_is_deterministic():
    assert q.entity_id_for("NPI", "1234567890") == q.entity_id_for("NPI", "1234567890")


def test_safe_json_passes_through_dict_and_list():
    assert q.safe_json({"a": 1}) == {"a": 1}
    assert q.safe_json([1, 2]) == [1, 2]


def test_safe_json_parses_a_json_string():
    assert q.safe_json('{"a": 1}') == {"a": 1}


def test_safe_json_none_on_sentinel_blanks():
    assert q.safe_json(None) is None
    assert q.safe_json("") is None
    assert q.safe_json("null") is None


def test_safe_json_none_on_unparseable_string():
    assert q.safe_json("not json") is None


def test_preview_pairs_drops_null_and_blank_values():
    pairs = q.preview_pairs('{"city": "Tulsa", "state": "", "zip": null, "county": "Osage"}')
    assert pairs == [("city", "Tulsa"), ("county", "Osage")]


def test_preview_pairs_empty_on_non_dict():
    assert q.preview_pairs("[1,2,3]") == []
    assert q.preview_pairs(None) == []


def test_normalize_sql_npi_pads_and_nulls_all_zero():
    sql = q.normalize_sql("NPI", "V")
    assert "LPAD" in sql and "10" in sql
    assert "REPEAT('0', 10)" in sql  # the all-zero sentinel guard


def test_normalize_sql_unknown_key_raises():
    with pytest.raises(KeyError):
        q.normalize_sql("NOT_A_REAL_KEY", "V")


def test_normalize_sql_rejects_text_sentinels_in_pad_mode():
    """The 2026-07-28 digits-only guard. _alnum() strips punctuation but KEEPS
    letters, so NPPES EIN's literal '<UNAVAIL>' becomes 'UNAVAIL' -- 7 chars, which
    LPADs into a perfectly plausible 9-digit EIN. serve/ missed this guard for three
    days while get_affiliations() ran the expression over raw LANDING columns."""
    for key in ("NPI", "EIN", "CIK", "CCN"):
        assert "REGEXP_LIKE" in q.normalize_sql(key, "V"), key


# ---- the drift guard: serve/ is a COPY of connect/, so prove it stays one ---- #
def test_serve_normalizers_are_character_identical_to_connect():
    """serve/ deliberately reproduces connect/keys.py rather than importing it, so
    the reading room lifts into Streamlit-in-Snowflake with no connect/ dependency
    (connect/keys.py sys.path-hacks portal_recon/ at import time and cannot come
    along). That copy is only safe if it is provably a copy -- on 2026-07-31 it had
    drifted three days behind and was resolving text sentinels into apparent
    providers. Any one-sided edit now fails here instead of shipping."""
    from connect import keys as ckeys

    assert q._NAME_NOISE == ckeys._NAME_NOISE, (
        "serve/serve_queries.py _NAME_NOISE has drifted from connect/keys.py. A name "
        "canonicalized against a different noise list is a DIFFERENT entity.")

    for key in list(q._NORM) + ["NAME", "PERSON"]:
        assert q.normalize_sql(key, '"C"') == ckeys.normalize_sql(key, '"C"'), (
            f"serve/ and connect/ emit different SQL for {key}. The reading room and "
            f"the connect engine would disagree about which rows are the same entity.")


# --------------------------------------------------------------------------- #
# resolve_hard_id -- typed ID -> ENTITY_MAP lookup, one bound raw value
# --------------------------------------------------------------------------- #
def test_resolve_hard_id_binds_key_type_and_raw_value(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    q.resolve_hard_id("NPI", "1164450573")
    sql, params = calls[0]
    assert params == ("NPI", "1164450573")
    assert "ENTITY_MAP" in sql
    assert "LIMIT 25" in sql


# --------------------------------------------------------------------------- #
# search_names -- whole-token-anchored (2026-07-30 fix), with TOTAL_MATCHES
# --------------------------------------------------------------------------- #
def test_search_names_anchors_each_token_to_a_word_boundary(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    monkeypatch.setattr(q, "normalize_name", lambda raw: "JON SMITH")
    q.search_names("jon smith")
    sql, params = calls[0]
    assert "(' ' || g.NAME_NORM || ' ') LIKE %s" in sql
    assert "g.NAME_NORM LIKE %s" not in sql  # the old, unanchored bug must never come back
    assert params[:2] == ("% JON %", "% SMITH %")
    assert params[-1] == 50  # default limit, bound last


def test_search_names_empty_query_short_circuits_to_a_trivially_empty_query(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    monkeypatch.setattr(q, "normalize_name", lambda raw: "")
    q.search_names("   ")
    assert len(calls) == 1
    sql, params = calls[0]
    assert "WHERE 1=0" in sql  # a real query, but structurally always empty
    assert params is None


def test_search_names_carries_total_matches_window_function(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    monkeypatch.setattr(q, "normalize_name", lambda raw: "SMITH")
    q.search_names("smith")
    sql, _ = calls[0]
    assert "COUNT(*) OVER () AS TOTAL_MATCHES" in sql


# --------------------------------------------------------------------------- #
# search_sources -- LIFECYCLE-filtered catalog search
# --------------------------------------------------------------------------- #
def test_search_sources_binds_the_same_term_three_times_for_ilike(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    q.search_sources("opioid")
    sql, params = calls[0]
    assert params[:3] == ("%opioid%", "%opioid%", "%opioid%")
    assert "LIFECYCLE IN ('landed','modeled')" in sql


# --------------------------------------------------------------------------- #
# get_affiliations -- provider -> CMS facility CCNs, whole-value NPI bind
# --------------------------------------------------------------------------- #
def test_get_affiliations_binds_the_npi_value(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    q.get_affiliations("1164450573")
    sql, params = calls[0]
    assert params == ("1164450573",)
    assert "FED_CMS_FACILITY_AFFILIATION" in sql
    assert "LIMIT 100" in sql
    assert "TOTAL_AFFILIATIONS" in sql


# --------------------------------------------------------------------------- #
# get_dossier -- three parameterized SELECTs, all keyed on the same entity_id
# --------------------------------------------------------------------------- #
def test_get_dossier_queries_golden_map_and_index_for_one_entity(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    q.get_dossier("ENT_abc123")
    assert len(calls) == 3
    for sql, params in calls:
        assert params == ("ENT_abc123",)
    assert "ENTITY_GOLDEN" in calls[0][0]
    assert "ENTITY_MAP" in calls[1][0]
    assert "ENTITY_INDEX" in calls[2][0]


# --------------------------------------------------------------------------- #
# get_source -- catalog lookup, lower-cased id
# --------------------------------------------------------------------------- #
def test_get_source_lowercases_the_id_to_match_the_bind(monkeypatch):
    calls = _capture_run_df(monkeypatch)
    q.get_source("FED_CMS_NPPES")
    sql, params = calls[0]
    assert params == ("fed_cms_nppes",)
    assert "LOWER(SOURCE_ID) = %s" in sql
