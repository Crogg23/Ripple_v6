"""Offline locks for the Pattern Desk — no network, no browser, no
Snowflake. What they hold:

  * the cohort write path is parameterized, its TARGET_KIND is the
    hard-coded literal 'cohort' (never app-supplied), and it can never
    write 'published'
  * decided cohorts drop out of the queue but needs_work stays visible
  * cohort snapshot records the BLAST RADIUS (n_outliers) the reviewer saw
  * render helpers are pure, deterministic, and never hide a value
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "reading_room"))
sys.path.insert(0, str(REPO))

import queries  # noqa: E402
import render  # noqa: E402
from connect import safety  # noqa: E402


# ── queue contract ──────────────────────────────────────────────────────────

def test_cohort_queue_filter_keeps_needs_work_visible():
    sql, params = queries.cohort_queue_sql(limit=20)
    assert params == (20,)
    assert "'needs_work'" not in sql
    for verdict in ("confirmed", "rejected", "retracted", "stale", "published"):
        assert f"'{verdict}'" in sql
    assert "ORDER BY c.priority_rank" in sql
    assert "V_LATEST_COHORT_DECISIONS" in sql


def test_case_queue_binds_hostile_values():
    hostile = "x'; DROP TABLE LEADS; --"
    sql, params = queries.case_queue_sql(detector=hostile, tier=hostile,
                                         limit=20)
    assert hostile not in sql
    assert params == (hostile, hostile, 20)
    sql, params = queries.case_queue_sql()
    assert params == (20,)


# ── the cohort write path ───────────────────────────────────────────────────

def test_cohort_insert_kind_is_hardcoded_literal():
    """App input picks the verdict, NEVER the kind: 'cohort' must be a
    literal in the SQL text, and the insert must bind exactly the five
    value slots (target_id, decision, reason, reviewer, snapshot)."""
    assert "'cohort'" in queries.INSERT_COHORT_DECISION_SQL
    assert queries.INSERT_COHORT_DECISION_SQL.count("%s") == 5
    assert "'cohort'" in queries.CONFIRM_COHORT_DECISION_SQL


def test_cohort_decision_params_guardrails():
    row = {"cohort_id": "6231|100-249", "headline": "h", "n_outliers": 214}
    with pytest.raises(ValueError):
        queries.cohort_decision_params("6231|100-249", "nuke", "chris", "", row)
    with pytest.raises(ValueError):
        queries.cohort_decision_params("6231|100-249", "confirm", "  ", "", row)
    params = queries.cohort_decision_params("6231|100-249", "confirm",
                                            "chris", " ", row)
    cid, verdict, note, reviewer, snap = params
    assert (cid, verdict, note, reviewer) == ("6231|100-249", "confirmed",
                                              None, "chris")
    assert json.loads(snap)["n_outliers"] == 214


def test_cohort_verdicts_share_the_safety_vocabulary_and_cannot_publish():
    assert set(queries.VERDICTS.values()) <= safety.VALID
    assert safety.PUBLISHED_VERDICT not in queries.VERDICTS.values()
    assert "cohort" in safety.KINDS


def test_cohort_snapshot_records_blast_radius():
    snap = json.loads(queries.cohort_snapshot_json({
        "cohort_id": "6231|100-249", "headline": "H", "priority_rank": 1,
        "priority_score": 4.2, "naics": "6231", "industry": "Nursing care",
        "size_band": "100-249", "cohort_n": 913, "n_outliers": 214,
        "n_implausible": 3, "worst_fold_plausible": 12.4, "caveat": "c",
        "not_kept": "x"}))
    assert snap["n_outliers"] == 214 and snap["cohort_n"] == 913
    assert "not_kept" not in snap


# ── render helpers ──────────────────────────────────────────────────────────

def test_parse_receipts_normalizes_variant_shapes():
    assert render.parse_receipts(None) == []
    assert render.parse_receipts("not json") == []
    assert render.parse_receipts('{"a": 1}') == []
    assert render.parse_receipts('[{"lead_id": "L1"}, "junk"]') == [
        {"lead_id": "L1"}]
    assert render.parse_receipts([{"lead_id": "L2"}]) == [{"lead_id": "L2"}]


def test_receipts_table_never_hides_missing_values():
    rows = render.receipts_table([{"lead_id": "L1", "title": "T",
                                   "fold": 3.1}])
    assert rows[0]["Lead"] == "L1"
    assert rows[0]["vs cohort"] == "3.1x"
    assert rows[0]["Employees"] == "—"
    assert rows[0]["Deaths"] == "—"


def test_cohort_features_cover_the_inheritance_rule():
    feats = render.cohort_features({"naics": "6231", "size_band": "100-249",
                                    "cohort_n": 913,
                                    "cohort_pooled_dart": 1.42})
    text = " ".join(feats)
    assert "individual lead decisions always win" in text.lower()
    assert "publish" in text.lower()
    assert all(isinstance(f, str) and f for f in feats)


def test_name_conflict_message_names_both_sources():
    msg = render.name_conflict_message("Kyung", "William")
    assert "Kyung" in msg and "William" in msg
    assert "LEIE" in msg and "NPPES" in msg
    # never hides a missing side
    msg2 = render.name_conflict_message(None, None)
    assert "—" in msg2
