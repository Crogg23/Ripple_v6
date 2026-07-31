"""Tests for serve/serve_session.py -- the local/Streamlit-in-Snowflake data-access
shim every serve/ query runs through. 2026-07-31: all of serve/ (5 files, 1,236
lines) had zero test coverage; this covers the pure connection-error-detection
and retry-on-stale-connection logic, the highest-risk part since it's on every
single query path.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "serve"))

import serve_session as ss  # noqa: E402


# --------------------------------------------------------------------------- #
# _is_conn_error -- decides whether run_df retries once or lets the error raise
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("msg", [
    "Connection is closed",
    "Session no longer exists",
    "Authentication token has expired",
    "Could not connect to Snowflake backend",
    "OperationalError: something",
    "Connection reset by peer",
])
def test_is_conn_error_recognizes_stale_connection_shapes(msg):
    assert ss._is_conn_error(Exception(msg)) is True


def test_is_conn_error_is_case_insensitive():
    assert ss._is_conn_error(Exception("CONNECTION RESET BY PEER")) is True


@pytest.mark.parametrize("msg", [
    "SQL compilation error: invalid identifier 'FOO'",
    "Table does not exist",
    "division by zero",
])
def test_is_conn_error_does_not_misclassify_real_query_errors(msg):
    """A real SQL/logic error must NOT be treated as a stale connection -- that
    would silently retry (and re-fail) a query that's just wrong, wasting a
    round-trip and muddying the actual error the user sees."""
    assert ss._is_conn_error(Exception(msg)) is False


# --------------------------------------------------------------------------- #
# run_df -- retries exactly once on a connection error, never on a real error
# --------------------------------------------------------------------------- #
def test_run_df_retries_once_on_connection_error(monkeypatch):
    calls = {"n": 0, "cleared": False}

    def fake_run(sql, params):
        calls["n"] += 1
        if calls["n"] == 1:
            raise Exception("Connection is closed")
        return "SUCCESS"

    monkeypatch.setattr(ss, "_run", fake_run)
    monkeypatch.setattr(ss._handle, "clear", lambda: calls.__setitem__("cleared", True))

    result = ss.run_df("SELECT 1")
    assert result == "SUCCESS"
    assert calls["n"] == 2
    assert calls["cleared"] is True


def test_run_df_does_not_retry_a_real_query_error(monkeypatch):
    calls = {"n": 0}

    def fake_run(sql, params):
        calls["n"] += 1
        raise Exception("SQL compilation error: invalid identifier")

    monkeypatch.setattr(ss, "_run", fake_run)

    with pytest.raises(Exception, match="invalid identifier"):
        ss.run_df("SELECT bogus_col")
    assert calls["n"] == 1  # never retried


def test_run_df_gives_up_if_the_retry_also_fails(monkeypatch):
    calls = {"n": 0}

    def fake_run(sql, params):
        calls["n"] += 1
        raise Exception("Connection is closed")

    monkeypatch.setattr(ss, "_run", fake_run)
    monkeypatch.setattr(ss._handle, "clear", lambda: None)

    with pytest.raises(Exception, match="Connection is closed"):
        ss.run_df("SELECT 1")
    assert calls["n"] == 2  # tried once, retried once, then gave up


# --------------------------------------------------------------------------- #
# boot_status -- merges the live query result with the module-level BOOT_NOTES
# --------------------------------------------------------------------------- #
def test_boot_status_merges_query_result_with_boot_notes(monkeypatch):
    import pandas as pd

    monkeypatch.setattr(ss, "run_df", lambda sql: pd.DataFrame(
        [{"ROLE": "CLAUDE_MCP_READONLY", "WH": "SERVE_WH", "ACCT": "acct1", "REGION": "us-east-1"}]))
    ss.BOOT_NOTES[:] = ["mode: local streamlit", "role: CLAUDE_MCP_READONLY"]

    status = ss.boot_status()
    assert status["ROLE"] == "CLAUDE_MCP_READONLY"
    assert status["notes"] == ["mode: local streamlit", "role: CLAUDE_MCP_READONLY"]


def test_boot_status_degrades_to_empty_dict_on_empty_result(monkeypatch):
    import pandas as pd

    monkeypatch.setattr(ss, "run_df", lambda sql: pd.DataFrame())
    ss.BOOT_NOTES[:] = []

    status = ss.boot_status()
    assert status == {"notes": []}
