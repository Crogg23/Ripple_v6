"""Offline tests for the publish-safety gate (pure logic, no Snowflake)."""

from connect.safety import SUPPRESS, VALID, gate_rows


def test_rejected_claim_is_hidden():
    rows = [{"LEAD_ID": "a"}, {"LEAD_ID": "b"}, {"LEAD_ID": "c"}]
    out = gate_rows(rows, {"a": "rejected", "b": "confirmed"})
    ids = {r["LEAD_ID"] for r in out}
    assert "a" not in ids                       # rejected -> suppressed
    assert ids == {"b", "c"}


def test_retracted_and_stale_are_suppressed():
    rows = [{"LEAD_ID": x} for x in "wxyz"]
    decisions = {"w": "retracted", "x": "stale", "y": "confirmed", "z": "rejected"}
    ids = {r["LEAD_ID"] for r in gate_rows(rows, decisions)}
    assert ids == {"y"}                          # only the confirmed survives


def test_confirm_nominates_only_publish_verdict_publishes():
    # Two-step gate (2026-07-20): 'confirmed' is a private nomination —
    # PUBLISHED needs the explicit 'published' verdict.
    out = {r["LEAD_ID"]: r for r in gate_rows(
        [{"LEAD_ID": "a"}, {"LEAD_ID": "b"}, {"LEAD_ID": "c"}],
        {"a": "published", "b": "confirmed"})}
    assert out["a"]["REVIEW_STATE"] == "published" and out["a"]["PUBLISHED"] is True
    assert out["b"]["REVIEW_STATE"] == "confirmed" and out["b"]["PUBLISHED"] is False
    assert out["c"]["REVIEW_STATE"] == "pending" and out["c"]["PUBLISHED"] is False


def test_auto_tier_can_no_longer_publish():
    # Auto-publish is structurally blocked: auto_ok is inert under the two-step gate.
    out = {r["LEAD_ID"]: r["PUBLISHED"]
           for r in gate_rows([{"LEAD_ID": "a", "auto_ok": True},
                               {"LEAD_ID": "b", "auto_ok": False}], {})}
    assert out["a"] is False and out["b"] is False


def test_a_later_verdict_can_revive_but_is_explicit():
    # gate_rows takes the LATEST verdict (computed upstream); a re-confirm overrides a retract
    assert gate_rows([{"LEAD_ID": "a"}], {"a": "confirmed"})       # survives
    assert gate_rows([{"LEAD_ID": "a"}], {"a": "retracted"}) == []  # gone


def test_suppress_is_subset_of_valid():
    assert SUPPRESS <= VALID
    assert "confirmed" in VALID and "confirmed" not in SUPPRESS


def test_published_is_not_writable_by_review_lanes():
    # The review buttons/CLI (record() validates against VALID) can never write
    # 'published' — the only sanctioned writer is scripts/publish_lead.py.
    from connect.safety import PUBLISHED_VERDICT
    assert PUBLISHED_VERDICT == "published"
    assert PUBLISHED_VERDICT not in VALID
    assert PUBLISHED_VERDICT not in SUPPRESS
