"""Tests for the pure (non-Streamlit-rendering) helpers in serve/app.py.
2026-07-31: serve/ had zero test coverage. app.py's rendering functions need a
real Streamlit runtime to exercise meaningfully, but _int/_ts/fresh_caption/
receipt_caption are pure formatting logic used on every page -- tested here
without any Streamlit dependency.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "serve"))

import app  # noqa: E402


# --------------------------------------------------------------------------- #
# _int -- NaN/None-safe int(), the fix for the pandas-NULL-as-float64-NaN trap
# --------------------------------------------------------------------------- #
def test_int_passes_through_a_real_int():
    assert app._int(42) == 42


def test_int_casts_a_float_string():
    assert app._int("42") == 42


def test_int_defaults_on_none():
    assert app._int(None) == 0


def test_int_defaults_on_none_with_custom_default():
    assert app._int(None, default=-1) == -1


def test_int_defaults_on_nan_without_raising():
    """The original bug this helper exists to fix: a mixed int+NULL column read
    via pd.DataFrame(cur.fetchall()) arrives as float64 with float('nan') for
    the NULL rows -- bare int(nan) raises ValueError."""
    assert app._int(float("nan")) == 0
    assert app._int(math.nan, default=None) is None


def test_int_defaults_on_unparseable_string():
    assert app._int("not a number") == 0


# --------------------------------------------------------------------------- #
# _ts -- timestamp truncation to a stable display width
# --------------------------------------------------------------------------- #
def test_ts_truncates_to_19_chars():
    assert app._ts("2026-07-30T12:34:56.789123") == "2026-07-30T12:34:56"


def test_ts_empty_on_none():
    assert app._ts(None) == ""


def test_ts_handles_a_short_value_without_padding():
    assert app._ts("2026") == "2026"


# --------------------------------------------------------------------------- #
# fresh_caption -- the freshness badge line, one branch per _BADGE state
# --------------------------------------------------------------------------- #
def test_fresh_caption_unknown_state_with_no_prior_load():
    assert app.fresh_caption({}) == "⚪ recency unverified · never loaded"


def test_fresh_caption_unknown_state_with_a_prior_load():
    out = app.fresh_caption({"freshness_state": "unknown", "loaded_at": "2026-07-01T00:00:00"})
    assert out == "⚪ recency unverified · last loaded 2026-07-01T00:00:00"


def test_fresh_caption_fresh_state_includes_data_through_and_age():
    out = app.fresh_caption({
        "freshness_state": "fresh", "data_through": "2026-07-29T00:00:00",
        "data_age_days": 1.7, "cadence": "daily",
    })
    assert out == "🟢 fresh · data through 2026-07-29T00:00:00 · 1d old · daily"


def test_fresh_caption_omits_fields_that_are_absent():
    out = app.fresh_caption({"freshness_state": "stale"})
    assert out == "🔴 stale"


def test_fresh_caption_unrecognized_state_falls_back_to_unknown_badge():
    out = app.fresh_caption({"freshness_state": "some_new_state_nobody_added_yet"})
    assert out.startswith("⚪ recency unverified")


# --------------------------------------------------------------------------- #
# receipt_caption -- the provenance receipt line
# --------------------------------------------------------------------------- #
def test_receipt_caption_no_run_on_record():
    assert app.receipt_caption({}) == "receipt: no successful ingest run on record"
    assert app.receipt_caption(None) == "receipt: no successful ingest run on record"


def test_receipt_caption_full_receipt_with_link():
    out = app.receipt_caption({
        "run_id": "abcdef1234567890", "sha256": "deadbeefcafef00d1234",
        "loaded_at": "2026-07-30T01:02:03", "source_url": "https://example.gov/data",
    })
    assert "run `abcdef12`" in out
    assert "sha `deadbeefcafe…`" in out
    assert "loaded 2026-07-30T01:02:03" in out
    assert "[verify source ↗](https://example.gov/data)" in out


def test_receipt_caption_no_sha_no_url():
    out = app.receipt_caption({"run_id": "abcdef1234567890", "loaded_at": "2026-07-30T01:02:03"})
    assert "sha `—`" in out
    assert "verify source" not in out


# --------------------------------------------------------------------------- #
# _friendly_error -- 2026-07-31 fix: raw Snowflake exceptions used to be shown
# directly to the user (st.error(f"...{e}")) on every failure path.
# --------------------------------------------------------------------------- #
def test_friendly_error_classifies_connection_problems():
    msg = app._friendly_error(Exception("Connection is closed"))
    assert "warehouse" in msg.lower()
    assert "closed" not in msg.lower()  # the raw driver text must not leak through


def test_friendly_error_classifies_permission_problems():
    msg = app._friendly_error(Exception("SQL access control error: Insufficient privileges"))
    assert "access" in msg.lower()


def test_friendly_error_classifies_sql_syntax_problems():
    msg = app._friendly_error(Exception("SQL compilation error: invalid identifier 'FOO'"))
    assert "valid sql" in msg.lower()


def test_friendly_error_has_a_generic_fallback():
    msg = app._friendly_error(Exception("some totally novel driver failure"))
    assert msg and "totally novel" not in msg
