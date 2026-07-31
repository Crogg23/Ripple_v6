"""Offline locks for the Reading Room app — no network, no browser, no
Snowflake. What they hold:

  * app.py contains NO SQL (queries.py owns every statement)
  * every user value is BOUND, never interpolated into SQL text
  * the button->verdict map stays inside the safety vocabulary and
    needs_work stays non-suppressing
  * the write lane NEVER falls back to another credential
  * render helpers cover every tier/verdict the mart can emit
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "reading_room"))
sys.path.insert(0, str(REPO))

import connections  # noqa: E402
import queries  # noqa: E402
import render  # noqa: E402
from connect import safety  # noqa: E402


# ── SQL hygiene ─────────────────────────────────────────────────────────────

def test_app_py_contains_no_sql():
    text = (REPO / "reading_room/app.py").read_text(encoding="utf-8")
    for token in ("SELECT ", "INSERT ", "UPDATE ", "DELETE ", "MERGE "):
        assert token not in text, f"SQL ({token.strip()}) leaked into app.py"


def test_user_values_are_bound_never_interpolated():
    hostile = "x'; DROP TABLE LEADS; --"
    sql, params = queries.queue_sql(detector=hostile, tier=hostile, limit=20)
    assert hostile not in sql
    assert params == (hostile, hostile, 20)


def test_queue_sql_composes_filters():
    sql, params = queries.queue_sql()
    assert "detector = %s" not in sql and params == (20,)
    sql, params = queries.queue_sql("banned_but_paid", "TWO_SOURCE", 5)
    assert sql.count("%s") == 3 and params == ("banned_but_paid",
                                               "TWO_SOURCE", 5)
    assert "ORDER BY q.priority_rank" in sql


def test_queue_filter_keeps_needs_work_visible():
    sql, _ = queries.queue_sql()
    assert "'needs_work'" not in sql, (
        "needs_work must NOT be in the drop-list — flagged leads stay "
        "visible in the queue")
    for verdict in ("confirmed", "rejected", "retracted", "stale"):
        assert f"'{verdict}'" in sql


# ── verdict vocabulary ──────────────────────────────────────────────────────

def test_button_verdicts_stay_inside_safety_vocabulary():
    assert set(queries.VERDICTS.values()) <= safety.VALID
    assert "needs_work" not in safety.SUPPRESS, (
        "needs_work must be non-suppressing: visible, flagged, unpublished")
    assert queries.VERDICTS == {"confirm": "confirmed", "reject": "rejected",
                                "needs_work": "needs_work"}


def test_decision_params_guardrails():
    row = {"lead_id": "LEAD_x", "headline": "h", "priority_rank": 1}
    with pytest.raises(ValueError):
        queries.decision_params("LEAD_x", "nuke", "chris", "", row)
    with pytest.raises(ValueError):
        queries.decision_params("LEAD_x", "confirm", "   ", "", row)
    params = queries.decision_params("LEAD_x", "confirm", "chris", "  ", row)
    lead_id, verdict, note, reviewer, snap = params
    assert (lead_id, verdict, note, reviewer) == ("LEAD_x", "confirmed",
                                                  None, "chris")
    import json
    assert json.loads(snap)["headline"] == "h"


def test_snapshot_carries_what_the_analyst_saw():
    import json
    snap = json.loads(queries.snapshot_json({
        "lead_id": "L", "headline": "H", "priority_rank": 3,
        "priority_score": 6.5, "confidence_tier": "TWO_SOURCE",
        "receipt_verdict": "NOT_EVALUATED", "detector": "d", "caveat": None,
        "extra_column_not_kept": "x"}))
    assert snap["headline"] == "H" and snap["priority_rank"] == 3
    assert "extra_column_not_kept" not in snap


# ── the no-fallback rule ────────────────────────────────────────────────────

def test_writer_status_missing_pat(monkeypatch):
    monkeypatch.delenv(connections.WRITER_PAT_ENV, raising=False)
    state, msg = connections.writer_status()
    assert state == "missing"
    assert "RIPPLE_REVIEW_WRITER" in msg and "RIPPLE_REVIEW_PAT" in msg


def test_writer_connect_never_falls_back(monkeypatch):
    monkeypatch.delenv(connections.WRITER_PAT_ENV, raising=False)
    monkeypatch.setenv("SNOWFLAKE_PAT", "some-other-credential")
    with pytest.raises(RuntimeError):
        connections.writer_connect()  # must raise, never borrow SNOWFLAKE_PAT


def test_writer_status_ready(monkeypatch):
    monkeypatch.setenv(connections.WRITER_PAT_ENV, "tok")
    assert connections.writer_status()[0] == "ready"


# ── render coverage ─────────────────────────────────────────────────────────

def test_tier_definitions_cover_every_mart_tier():
    assert set(queries.TIERS) <= set(render.TIER_DEFS)


def test_verdict_text_covers_every_mart_verdict():
    for v in ("PAID_ON_OR_AFTER_EXCLUSION", "PAYMENTS_PREDATE_EXCLUSION",
              "TIMELINE_UNKNOWN", "NOT_EVALUATED"):
        assert v in render.VERDICT_TEXT


def test_linkage_features_for_every_detector_key():
    for kt in ("NPI", "UEI", "IMO", "EIN"):
        feats = render.linkage_features("any", kt, "123", "HARD_ID_ONLY")
        assert feats and all(isinstance(f, str) and f for f in feats)


def test_source_panel_never_hides_nulls():
    panel = render.source_rows_to_panel([{"A": None, "B": " ", "C": "x"}], "t")
    rec = panel["records"][0]
    assert rec["A"] == "—" and rec["B"] == "—" and rec["C"] == "x"
