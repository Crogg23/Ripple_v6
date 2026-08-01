"""Static locks on scripts/provision_pattern_desk.sql — the decision
inheritance is defined in SQL that only Chris can run (Snowsight), so these
tests pin the TEXT of the contract:

  * every latest-decision view breaks DECIDED_AT ties on DECISION_ID
  * the effective view COALESCEs lead-level BEFORE cohort-level
    (specific beats general)
  * every CREATE OR REPLACE VIEW carries COPY GRANTS
  * no cohort-writable path can produce 'published'
  * the v1 vessel retirement is idempotent (guarded UPDATE)
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SQL = (REPO / "scripts" / "provision_pattern_desk.sql").read_text(
    encoding="utf-8")


def _statements():
    return [s.strip() for s in SQL.split(";") if s.strip()]


def test_every_view_carries_copy_grants():
    for stmt in _statements():
        if "CREATE OR REPLACE VIEW" in stmt:
            assert "COPY GRANTS" in stmt, (
                "POLICY copy_grants_library_meta violated:\n" + stmt[:200])


def test_latest_views_have_deterministic_tiebreak():
    ties = re.findall(r"ORDER BY DECIDED_AT DESC, DECISION_ID DESC", SQL)
    assert len(ties) >= 2, (
        "both V_LATEST_DECISIONS and V_LATEST_COHORT_DECISIONS must break "
        "DECIDED_AT ties on DECISION_ID")


def test_effective_view_is_specific_beats_general():
    m = re.search(r"COALESCE\(ld\.DECISION,\s*cd\.DECISION\)", SQL)
    assert m, ("the effective decision must COALESCE lead-level (ld) before "
               "cohort-level (cd) — a blanket cohort verdict must never "
               "override a deliberate per-lead exception")
    # and DECISION_LEVEL says which one applied
    assert "IFF(ld.LEAD_ID IS NOT NULL, 'lead', 'cohort')" in SQL


def test_published_is_lead_level_only():
    """'published' must never be writable at cohort level: the only mention
    of it in this script is inside the V_LEADS_PUBLISHED gate, and no
    INSERT of any kind exists here."""
    assert "INSERT" not in SQL.upper().replace("-- ", ""), (
        "the provisioning script must not write decisions")
    # the gate still requires an explicit 'published' verdict
    assert "= 'published'" in SQL


def test_v1_vessel_retirement_is_guarded_and_idempotent():
    m = re.search(
        r"UPDATE LIBRARY_META\.\"CONNECT\"\.LEADS\s+SET STATUS = 'stale'\s+"
        r"WHERE RULE_NAME = 'sanctioned_vessel_broadcasting'\s+"
        r"AND COALESCE\(STATUS, 'active'\) = 'active'", SQL)
    assert m, "F3 retirement must target ONLY active v1 vessel leads"
    assert "sanctioned_vessel_broadcasting_v2" not in m.group(0)


def test_cohort_map_matches_the_mart_key_derivation():
    """The inheritance spine and cohort_queue must derive cohort_id the
    same way, or verdicts would silently miss their members."""
    key_expr = "EVIDENCE[0]:naics::STRING || '|' || EVIDENCE[0]:size_band::STRING"
    assert key_expr in SQL
    mart = (REPO / "library-onboarding" / "ripple_dbt" / "models" / "marts" /
            "review" / "cohort_queue.sql").read_text(encoding="utf-8")
    assert "naics || '|' || size_band" in mart


def test_smoke_test_rows_filtered_everywhere():
    assert SQL.count("!= 'SMOKE_TEST'") >= 2
