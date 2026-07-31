"""Tests for viz/sqlrun.py -- the platform's own documented "ONE chokepoint
between any surface and Snowflake." 2026-07-31: had zero test coverage while
every sibling viz/ module (card, guard, plugs, safety) had one.

Covers: the pure truncation-detecting LIMIT wrapper, connection/monitor error
classification, the on-disk budget cache, and run()'s guard/retry/error-
classification branches via a fake cursor -- no live Snowflake connection
needed for any of this.
"""
from __future__ import annotations

import json
import time

import pytest

from viz import sqlrun


# --------------------------------------------------------------------------- #
# wrap_limit -- pure, no DB
# --------------------------------------------------------------------------- #
def test_wrap_limit_wraps_a_select_with_a_plus_one_limit():
    out = sqlrun.wrap_limit("SELECT * FROM foo", 100)
    assert out == "SELECT * FROM (\nSELECT * FROM foo\n) LIMIT 101"


def test_wrap_limit_wraps_a_with_clause():
    out = sqlrun.wrap_limit("WITH x AS (SELECT 1) SELECT * FROM x", 50)
    assert out.startswith("SELECT * FROM (\nWITH x AS")
    assert out.endswith("LIMIT 51")


def test_wrap_limit_passes_show_through_unwrapped():
    assert sqlrun.wrap_limit("SHOW WAREHOUSES", 100) == "SHOW WAREHOUSES"


def test_wrap_limit_passes_desc_and_explain_through_unwrapped():
    assert sqlrun.wrap_limit("DESC TABLE foo", 100) == "DESC TABLE foo"
    assert sqlrun.wrap_limit("EXPLAIN SELECT 1", 100) == "EXPLAIN SELECT 1"


def test_wrap_limit_strips_trailing_semicolon():
    out = sqlrun.wrap_limit("SELECT 1;", 10)
    assert "1;" not in out
    assert out == "SELECT * FROM (\nSELECT 1\n) LIMIT 11"


def test_wrap_limit_survives_a_trailing_line_comment():
    """The docstring calls this out explicitly: without the newlines around the
    inner SQL, a trailing '-- comment' swallows the closing paren and LIMIT
    clause, producing invalid SQL."""
    out = sqlrun.wrap_limit("SELECT 1 -- a comment", 10)
    assert out.rstrip().endswith("LIMIT 11")


# --------------------------------------------------------------------------- #
# error classification -- pure string matching
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("msg", [
    "Connection is closed", "Connection was closed", "Token is expired",
    "Session no longer exists", "Connection reset", "Lost connection",
])
def test_is_conn_error_recognizes_stale_connection_shapes(msg):
    assert sqlrun._is_conn_error(Exception(msg)) is True


def test_is_conn_error_does_not_misclassify_a_real_sql_error():
    assert sqlrun._is_conn_error(Exception("SQL compilation error: invalid identifier")) is False


def test_is_monitor_suspended_requires_both_words():
    assert sqlrun._is_monitor_suspended(
        Exception("Warehouse suspended due to resource monitor")) is True
    assert sqlrun._is_monitor_suspended(Exception("resource monitor updated")) is False
    assert sqlrun._is_monitor_suspended(Exception("warehouse suspended manually")) is False


# --------------------------------------------------------------------------- #
# on-disk budget cache -- redirect CACHE_PATH to a tmp file
# --------------------------------------------------------------------------- #
def test_cache_put_then_get_round_trips(monkeypatch, tmp_path):
    monkeypatch.setattr(sqlrun, "CACHE_PATH", tmp_path / "_viz_cache.json")
    sqlrun._cache_put("budget", "SERVE_MON: 1.23/5 cr used")
    assert sqlrun._cache_get("budget", ttl_s=600) == "SERVE_MON: 1.23/5 cr used"


def test_cache_get_expires_after_ttl(monkeypatch, tmp_path):
    monkeypatch.setattr(sqlrun, "CACHE_PATH", tmp_path / "_viz_cache.json")
    cache_file = tmp_path / "_viz_cache.json"
    cache_file.write_text(json.dumps({"budget": {"t": time.time() - 700, "v": "stale"}}), encoding="utf-8")
    assert sqlrun._cache_get("budget", ttl_s=600) is None


def test_cache_get_missing_key_is_none(monkeypatch, tmp_path):
    monkeypatch.setattr(sqlrun, "CACHE_PATH", tmp_path / "_viz_cache.json")
    assert sqlrun._cache_get("nonexistent", ttl_s=600) is None


def test_cache_load_degrades_to_empty_dict_on_corrupt_file(monkeypatch, tmp_path):
    monkeypatch.setattr(sqlrun, "CACHE_PATH", tmp_path / "_viz_cache.json")
    (tmp_path / "_viz_cache.json").write_text("not json{{{", encoding="utf-8")
    assert sqlrun._cache_load() == {}


def test_budget_line_returns_the_cached_value_without_connecting(monkeypatch):
    monkeypatch.setattr(sqlrun, "_cache_get", lambda key, ttl_s: "cached budget line")
    called = {"connect": False}
    monkeypatch.setattr(sqlrun, "connect", lambda: called.__setitem__("connect", True))
    assert sqlrun.budget_line() == "cached budget line"
    assert called["connect"] is False


# --------------------------------------------------------------------------- #
# run() -- guard enforcement and error-recovery branches, via a fake cursor
# --------------------------------------------------------------------------- #
class _FakeCursor:
    def __init__(self, rows=None, cols=("N",), raise_once=None):
        self.rows = rows if rows is not None else [(1,)]
        self.description = [(c,) for c in cols]
        self._raise_once = raise_once
        self.executed = []

    def execute(self, sql):
        self.executed.append(sql)
        if self._raise_once is not None:
            exc, self._raise_once = self._raise_once, None
            raise exc

    def fetch_pandas_all(self):
        import pandas as pd
        return pd.DataFrame(self.rows, columns=[c[0] for c in self.description])

    def fetchall(self):
        return self.rows

    def close(self):
        pass


class _FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor


def test_run_refuses_a_query_the_guard_rejects(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (False, "not a read-only statement"))
    with pytest.raises(sqlrun.GuardError, match="not a read-only statement"):
        sqlrun.run("DELETE FROM foo")


def test_run_refuses_a_raw_claim_table_read_without_the_unsafe_flag(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (True, ""))
    monkeypatch.setattr(sqlrun.guard, "claim_refs", lambda sql: {"LEADS"})
    with pytest.raises(sqlrun.GuardError, match="unreviewed leads are not facts"):
        sqlrun.run("SELECT * FROM LEADS")


def test_run_allows_a_claim_table_read_with_unsafe_claims(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (True, ""))
    monkeypatch.setattr(sqlrun.guard, "claim_refs", lambda sql: {"LEADS"})
    cur = _FakeCursor(rows=[(1,), (2,)])
    monkeypatch.setattr(sqlrun, "connect", lambda refresh=False: _FakeConn(cur))
    monkeypatch.setattr(sqlrun, "budget_line", lambda: "n/a")

    df, meta = sqlrun.run("SELECT * FROM LEADS", unsafe_claims=True)
    assert meta["claim_refs"] == ["LEADS"]
    assert len(df) == 2


def test_run_retries_once_on_a_stale_connection(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (True, ""))
    monkeypatch.setattr(sqlrun.guard, "claim_refs", lambda sql: set())
    monkeypatch.setattr(sqlrun, "budget_line", lambda: "n/a")

    dead_cursor = _FakeCursor(raise_once=Exception("Connection is closed"))
    live_cursor = _FakeCursor(rows=[(42,)])
    conns = [_FakeConn(dead_cursor), _FakeConn(live_cursor)]
    monkeypatch.setattr(sqlrun, "connect", lambda refresh=False: conns.pop(0))

    df, meta = sqlrun.run("SELECT 1")
    assert len(df) == 1
    assert df.iloc[0]["N"] == 42


def test_run_raises_a_guard_error_on_monitor_suspension(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (True, ""))
    monkeypatch.setattr(sqlrun.guard, "claim_refs", lambda sql: set())
    cur = _FakeCursor(raise_once=Exception("Warehouse suspended: resource monitor cap hit"))
    monkeypatch.setattr(sqlrun, "connect", lambda refresh=False: _FakeConn(cur))

    with pytest.raises(sqlrun.GuardError, match="resource monitor"):
        sqlrun.run("SELECT 1")


def test_run_propagates_a_real_sql_error_without_retrying(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (True, ""))
    monkeypatch.setattr(sqlrun.guard, "claim_refs", lambda sql: set())
    connect_calls = []
    cur = _FakeCursor(raise_once=Exception("SQL compilation error: invalid identifier"))
    monkeypatch.setattr(sqlrun, "connect", lambda refresh=False: connect_calls.append(1) or _FakeConn(cur))

    with pytest.raises(Exception, match="invalid identifier"):
        sqlrun.run("SELECT bogus")
    assert len(connect_calls) == 1  # never reconnected -- this isn't a connection problem


def test_run_caps_limit_rows_at_max_limit_rows(monkeypatch):
    monkeypatch.setattr(sqlrun.guard, "check", lambda sql: (True, ""))
    monkeypatch.setattr(sqlrun.guard, "claim_refs", lambda sql: set())
    monkeypatch.setattr(sqlrun, "budget_line", lambda: "n/a")
    cur = _FakeCursor(rows=[(1,)])
    monkeypatch.setattr(sqlrun, "connect", lambda refresh=False: _FakeConn(cur))

    sqlrun.run("SELECT 1", limit_rows=999_999_999)
    assert f"LIMIT {sqlrun.MAX_LIMIT_ROWS + 1}" in cur.executed[0]
