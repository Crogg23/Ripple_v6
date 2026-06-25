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


def test_confirmed_publishes_pending_does_not():
    out = {r["LEAD_ID"]: r for r in gate_rows([{"LEAD_ID": "b"}, {"LEAD_ID": "c"}],
                                              {"b": "confirmed"})}
    assert out["b"]["REVIEW_STATE"] == "confirmed" and out["b"]["PUBLISHED"] is True
    assert out["c"]["REVIEW_STATE"] == "pending" and out["c"]["PUBLISHED"] is False


def test_auto_tier_publishes_without_a_human():
    out = {r["LEAD_ID"]: r["PUBLISHED"]
           for r in gate_rows([{"LEAD_ID": "a", "auto_ok": True},
                               {"LEAD_ID": "b", "auto_ok": False}], {})}
    assert out["a"] is True and out["b"] is False


def test_a_later_verdict_can_revive_but_is_explicit():
    # gate_rows takes the LATEST verdict (computed upstream); a re-confirm overrides a retract
    assert gate_rows([{"LEAD_ID": "a"}], {"a": "confirmed"})       # survives
    assert gate_rows([{"LEAD_ID": "a"}], {"a": "retracted"}) == []  # gone


def test_suppress_is_subset_of_valid():
    assert SUPPRESS <= VALID
    assert "confirmed" in VALID and "confirmed" not in SUPPRESS
