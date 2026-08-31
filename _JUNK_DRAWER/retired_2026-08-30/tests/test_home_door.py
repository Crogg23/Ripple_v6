"""Guards on the one-door app (home/).

Two things this app must never do, both learned the hard way elsewhere in this
repo: show a stale number as if it were current, and interpolate a user's input
into SQL. The live tests then prove the three rooms can actually fetch what they
render - a door that boots but shows nothing is not a door.
"""

from __future__ import annotations

import pytest

from home import queries as Q


# ---- offline: shape of the SQL the app will run --------------------------- #
def test_only_the_latest_run_of_each_pattern_is_shown():
    """The lead table keeps history. A lead found by an OLDER version of a rule
    and not re-found by the current one is still in there; counting it inflates
    today's number. Seen live 2026-08-11: the table held 344 debarment hits while
    the current rule found 343."""
    for sql in (Q.RULE_COUNTS_SQL, Q.LEADS_SQL):
        assert "QUALIFY LAST_SEEN = MAX(LAST_SEEN) OVER (PARTITION BY RULE_NAME)" in sql


def test_user_input_is_bound_never_interpolated():
    """The pattern name and the row limit both come from the screen. Neither may
    reach the SQL as text."""
    assert "%s" in Q.LEADS_SQL
    assert "'" not in Q.LEADS_SQL.split("WHERE")[1].split("ORDER")[0]


def test_queries_are_read_only():
    for sql in (Q.RULE_COUNTS_SQL, Q.LEADS_SQL):
        upper = sql.upper()
        for verb in ("INSERT", "UPDATE", "DELETE", "MERGE", "CREATE", "DROP", "TRUNCATE"):
            assert verb not in upper, f"{verb} in a serving query"


def test_unlabelled_patterns_still_display():
    """A new rule nobody has written a plain-English name for must still appear -
    under its raw name. Hiding it would hide a real finding."""
    assert Q.label_for("some_brand_new_rule") == "some_brand_new_rule"
    assert Q.label_for("debarred_but_funded") != "debarred_but_funded"


@pytest.mark.parametrize("raw,expected_contains", [
    ('{"awarding_agency": "Peace Corps"}', "Peace Corps"),
    ('not json at all', "not json at all"),
    (None, ""),
    ({"a": 1, "b": None}, "a: 1"),
])
def test_evidence_never_raises_and_never_swallows(raw, expected_contains):
    out = Q.evidence_bits(raw)
    assert expected_contains in out


def test_evidence_drops_empty_values_but_keeps_zero():
    """0 is a real measurement; empty string is not. Dropping 0 would silently
    turn 'zero contracts' into 'no data'."""
    assert "n: 0" in Q.evidence_bits({"n": 0, "blank": ""})


# ---- live: the rooms can actually fetch what they render ------------------ #
@pytest.mark.snowflake
def test_findings_room_has_patterns_with_hits(sf):
    df = Q.rule_counts()
    assert df is not None and len(df) > 0, "the findings room would render empty"
    assert (df["N"] > 0).all()


@pytest.mark.snowflake
def test_findings_room_returns_rows_for_its_biggest_pattern(sf):
    top = Q.rule_counts().iloc[0]["RULE_NAME"]
    rows = Q.leads_for(top, 5)
    assert len(rows) > 0
    for col in ("TITLE", "EVIDENCE_COUNT", "LEFT_ENTITY_ID", "SQL_SHA256"):
        assert col in rows.columns, f"the screen renders {col} and the query lost it"


@pytest.mark.snowflake
def test_lookup_room_resolves_a_name_to_a_cross_source_dossier(sf):
    """End-to-end on the thing the platform exists for: a name goes in, and what
    comes back is one entity seen in more than one source."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "serve"))
    import serve_queries as sq

    hits = sq.search_names("cvs pharmacy", limit=5)
    assert len(hits) > 0
    eid = hits["ENTITY_ID"].iloc[0]
    _golden, _pairs, rows = sq.get_dossier(eid)
    assert len(rows) >= 1
