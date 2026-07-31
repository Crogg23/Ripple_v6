"""Tests for connect/dossier.py's _resolve() name search.

2026-07-30: _resolve() used to build its name-search WHERE clause as bare
`NAME_NORM LIKE '%TOKEN%'` -- an unanchored substring match. Since NAME_NORM
is a plain space-joined token list with no boundary delimiter, "jon smith"
could silently resolve to an unrelated entity like "JONES SMITHFIELD MEDICAL
GROUP" (JON inside JONES, SMITH inside SMITHFIELD) with no disambiguation
prompt shown -- exactly the wrong-entity failure class this platform exists
to prevent. Fixed by padding NAME_NORM with boundary spaces and requiring
'% TOKEN %'. These tests lock that in.
"""
import pytest

from connect import dossier


def test_resolve_name_search_anchors_tokens_to_word_boundaries(monkeypatch):
    """Offline: assert the WHERE clause / params _resolve builds are the
    boundary-anchored form, not the old bare-substring form."""
    captured = {}

    def fake_scalar(conn, sql, params):
        return "JON SMITH"  # stand-in for the normalized query text

    def fake_dicts(conn, sql, params):
        captured["sql"] = sql
        captured["params"] = params
        return []

    monkeypatch.setattr(dossier.db, "scalar", fake_scalar)
    monkeypatch.setattr(dossier.db, "dicts", fake_dicts)

    dossier._resolve(None, None, None, None, None, "jon smith")

    assert "(' ' || NAME_NORM || ' ') LIKE %s" in captured["sql"]
    # the exact old buggy clause must never reappear
    assert "NAME_NORM LIKE %s" not in captured["sql"]
    assert captured["params"] == ("% JON %", "% SMITH %")


@pytest.mark.snowflake
def test_resolve_name_search_excludes_substring_false_positives(sf):
    """Live: reproduces the exact failure scenario found in the portfolio
    sweep. A search for "jon smith" must never return an entity whose match
    is only a substring artifact (e.g. "JONES-SMITH FOUNDATION", "SMITHERS,
    JONATHAN") -- only entities where JON and SMITH appear as real whole
    tokens, matching how NAME_NORM itself is tokenized (split on non-alnum)."""
    import re

    _, cands = dossier._resolve(sf, None, None, None, None, "jon smith")
    for c in cands:
        tokens = re.split(r"[^A-Z0-9]+", c["CANONICAL_NAME"].upper())
        assert "JON" in tokens, f"{c['CANONICAL_NAME']!r} matched without a real JON token"
        assert "SMITH" in tokens, f"{c['CANONICAL_NAME']!r} matched without a real SMITH token"
    # the known false-positive shapes from the sweep must not appear at all
    names = {c["CANONICAL_NAME"].upper() for c in cands}
    assert not any("JONES-SMITH" in n or "SMITHERS" in n or "JONATHAN" in n for n in names)
