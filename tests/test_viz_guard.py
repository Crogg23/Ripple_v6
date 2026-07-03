"""viz/guard.py — the read-lane text guard. Pure, offline."""

import pytest

from viz import guard


# ---- allow ----------------------------------------------------------------- #
@pytest.mark.parametrize("sql", [
    "SELECT 1",
    "select count(*) from LIBRARY_RAW.LANDING.FED_CISA_KEV",
    "WITH t AS (SELECT 1 AS x) SELECT * FROM t",
    "  (SELECT 1) UNION (SELECT 2)",
    "SHOW WAREHOUSES",
    "DESCRIBE TABLE LIBRARY_META.REGISTRY.CATALOG",
    "DESC TABLE LIBRARY_META.REGISTRY.CATALOG",
    "EXPLAIN SELECT 1",
    "SELECT ';' AS semi",                      # ; inside a string literal
    "SELECT 1; ",                              # trailing semicolon is fine
    "/* leading DROP in a comment */ SELECT 1",
    "-- DROP TABLE X\nSELECT 1",
    "SELECT budget, target_state, copy_number FROM t",  # deny words as substrings only
    "SELECT * FROM t WHERE note = 'call me; drop by'",
])
def test_allows(sql):
    ok, reason = guard.check(sql)
    assert ok, reason


# ---- deny ------------------------------------------------------------------ #
@pytest.mark.parametrize("sql,frag", [
    ("", "empty"),
    ("DROP TABLE X", "first keyword"),
    ("INSERT INTO t VALUES (1)", "first keyword"),
    ("CREATE TABLE t (x INT)", "first keyword"),
    ("CALL my_proc()", "first keyword"),
    ("/* sneaky */ DELETE FROM t", "first keyword"),
    ("SELECT 1; DROP TABLE x", "multiple statements"),
    ("SELECT * FROM TABLE(TO_QUERY('DROP TABLE X'))", "TO_QUERY"),
    ("SELECT SYSTEM$ABORT_SESSION(1)", "SYSTEM$"),
    ("SELECT * FROM t WHERE x = (CALL p())", "CALL"),
    ("EXECUTE IMMEDIATE 'DROP TABLE X'", "first keyword"),
])
def test_denies(sql, frag):
    ok, reason = guard.check(sql)
    assert not ok
    assert frag.lower() in reason.lower()


# ---- claim tables ------------------------------------------------------------ #
def test_claim_refs_detects_leads_quoted_and_bare():
    assert guard.claim_refs('SELECT * FROM LIBRARY_META."CONNECT".LEADS') == {"LEADS"}
    assert guard.claim_refs("SELECT * FROM LIBRARY_META.CONNECT.ENTITY_LINKS") == {"ENTITY_LINKS"}


def test_claim_refs_lets_the_published_view_through():
    assert guard.claim_refs('SELECT * FROM LIBRARY_META."CONNECT".V_LEADS_PUBLISHED') == set()


def test_claim_refs_ignores_comments():
    assert guard.claim_refs('-- "CONNECT".LEADS\nSELECT 1') == set()


# ---- identifiers ------------------------------------------------------------- #
@pytest.mark.parametrize("fqn,expect", [
    ("library_raw.landing.fed_x", "LIBRARY_RAW.LANDING.FED_X"),
    ("LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES",
     "LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES"),
    ('LIBRARY_META."CONNECT".V_LEADS_PUBLISHED', 'LIBRARY_META."CONNECT".V_LEADS_PUBLISHED'),
    ("CATALOG", "CATALOG"),
])
def test_validate_fqn_accepts(fqn, expect):
    assert guard.validate_fqn(fqn) == expect


@pytest.mark.parametrize("fqn", [
    "a.b.c.d", "a..b", "", "x; DROP TABLE y", "tab le", 'a."b"c".d',
])
def test_validate_fqn_rejects(fqn):
    with pytest.raises(ValueError):
        guard.validate_fqn(fqn)


def test_quote_ident_escapes_quotes():
    assert guard.quote_ident('we"ird') == '"we""ird"'


# ---- review regressions (2026-07-03) ------------------------------------------ #
def test_identifier_function_is_denied():
    # IDENTIFIER('...') would smuggle claim tables past claim_refs (string
    # literals are blanked before the scan) - reviewed and denied outright
    ok, reason = guard.check("SELECT * FROM IDENTIFIER('LIBRARY_META.\"CONNECT\".LEADS')")
    assert not ok and "IDENTIFIER" in reason
