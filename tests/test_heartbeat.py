"""Offline tests for scripts/heartbeat.py -- the scheduled automation spine.

2026-07-31: this 1,195-line module had NO tests. It is the thing that decides when
every other job runs, and it runs unattended, so a crash in it is silent by nature:
nothing fires, and nothing says why.

Offline only -- these cover the pure scheduling arithmetic (timestamp parsing,
tier ages, cadence). No Snowflake, no subprocesses.
"""

from __future__ import annotations

import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load_heartbeat():
    """Import heartbeat.py by path -- scripts/ is not a package."""
    spec = importlib.util.spec_from_file_location(
        "_heartbeat", REPO / "scripts" / "heartbeat.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hb = _load_heartbeat()


# --------------------------------------------------------------------------- #
# _parse -- must ALWAYS return an aware datetime
# --------------------------------------------------------------------------- #
def test_parse_keeps_an_explicit_offset():
    dt = hb._parse("2026-07-31T10:00:00+00:00")
    assert dt.tzinfo is not None
    assert dt.year == 2026 and dt.hour == 10


def test_parse_assumes_utc_for_a_naive_timestamp():
    """THE BUG. A naive-but-valid timestamp parsed fine and came back naive, then
    crashed tier_age_s with 'can't subtract offset-naive and offset-aware datetimes'
    -- an uncaught TypeError in the scheduled spine, which stops ALL automation
    silently. The old except: only covered UNPARSEABLE input, not this."""
    dt = hb._parse("2026-07-31T10:00:00")
    assert dt.tzinfo is not None, "a naive state timestamp must not escape _parse"
    assert dt.utcoffset() == timedelta(0)


def test_parse_falls_back_to_epoch_on_garbage():
    dt = hb._parse("not-a-timestamp")
    assert dt.tzinfo is not None
    assert dt.year == 1970


@pytest.mark.parametrize("ts", [
    "2026-07-31T10:00:00",            # naive -- the regression
    "2026-07-31T10:00:00+00:00",      # aware
    "2026-07-31T10:00:00-04:00",      # aware, non-UTC offset
    "garbage",                        # unparseable
    "",                               # empty
])
def test_tier_age_never_raises_whatever_the_state_file_holds(ts):
    """The real invariant: whatever ends up in the state file -- hand-edited,
    restored from a backup, written by an older build -- computing a tier age must
    return a number rather than take the scheduler down."""
    state = {"tiers": {"link": {"last_success": ts}}}
    age = hb.tier_age_s(state, "link")
    assert isinstance(age, float)
    assert age >= 0


def test_tier_age_is_huge_when_a_tier_never_succeeded():
    """No recorded success -> treated as maximally overdue, so a fresh tier runs
    rather than being skipped forever."""
    assert hb.tier_age_s({"tiers": {"link": {"last_success": None}}}, "link") >= 1e11
    assert hb.tier_age_s({"tiers": {}}, "link") >= 1e11


def test_tier_due_respects_cadence():
    """A tier that just succeeded is not due; one older than its cadence is."""
    now = datetime.now(timezone.utc)
    for tier, cadence in hb.CADENCE.items():
        fresh = {"tiers": {tier: {"last_success": now.isoformat()}}}
        assert hb.tier_due(fresh, tier) is False, f"{tier} just ran, should not be due"

        stale_at = now - timedelta(seconds=cadence + 60)
        stale = {"tiers": {tier: {"last_success": stale_at.isoformat()}}}
        assert hb.tier_due(stale, tier) is True, f"{tier} is past its cadence, should be due"


def test_bootstrap_state_timestamps_are_all_parseable_and_aware():
    """The first-run state dict feeds straight into _parse; every value in it must
    survive the round trip."""
    state = hb.load_state()
    for tier, rec in state["tiers"].items():
        dt = hb._parse(rec["last_success"])
        assert dt.tzinfo is not None, f"{tier} bootstrap timestamp is naive"
        assert isinstance(hb.tier_age_s(state, tier), float)
