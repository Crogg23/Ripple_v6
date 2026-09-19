"""Pins for the 2026-09-18 hardening: the keyset DELETE-then-INSERT is one
transaction, the watermark memo is keyed on the Snowflake session id, and the
panel's connection pool never leaks a permit -- not even on KeyboardInterrupt.
All offline: a recording fake stands in for the connection."""
from __future__ import annotations

import sys
import threading
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from connect import incremental as inc  # noqa: E402


class _Conn:
    def __init__(self, fail_on: str | None = None):
        self.log, self.fail_on = [], fail_on


@pytest.fixture
def fake_rows(monkeypatch):
    def rows(conn, sql, params=None):
        verb = sql.split()[0]
        conn.log.append(verb)
        if conn.fail_on == verb:
            raise RuntimeError("boom")
        return []
    monkeypatch.setattr(inc.db, "rows", rows)


def test_txn_commits_in_order(fake_rows):
    c = _Conn()
    with inc._txn(c):
        inc.db.rows(c, "DELETE x")
        inc.db.rows(c, "INSERT y")
    assert c.log == ["BEGIN", "DELETE", "INSERT", "COMMIT"]


def test_txn_rolls_back_and_reraises_when_the_insert_fails(fake_rows):
    c = _Conn(fail_on="INSERT")
    with pytest.raises(RuntimeError, match="boom"):
        with inc._txn(c):
            inc.db.rows(c, "DELETE x")
            inc.db.rows(c, "INSERT y")
    assert c.log == ["BEGIN", "DELETE", "INSERT", "ROLLBACK"]


def test_txn_rolls_back_on_keyboard_interrupt(fake_rows):
    c = _Conn()
    with pytest.raises(KeyboardInterrupt):
        with inc._txn(c):
            raise KeyboardInterrupt()
    assert c.log == ["BEGIN", "ROLLBACK"]


def test_discover_keyset_refresh_is_one_transaction(fake_rows, monkeypatch):
    monkeypatch.setattr(inc, "_discover_keyset_inserts",
                        lambda conn, table: [("EIN", '"EIN"'), ("NPI", '"NPI"')])
    c = _Conn()
    inc._refresh_discover_keyset(c, "FED_SOME_TABLE")
    assert c.log == ["BEGIN", "DELETE", "INSERT", "INSERT", "COMMIT"]


def test_memo_key_is_the_session_id_not_the_memory_address():
    class S:
        session_id = 42
    assert inc._conn_key(S()) == inc._conn_key(S()) == ("session", 42)
    assert inc._conn_key(_Conn())[0] == "pyid"   # a test double has no session id


def _panel(monkeypatch, dicts):
    ps = pytest.importorskip("ripple.panel_server")

    class K:
        def close(self):
            pass
    monkeypatch.setattr(ps, "_pool_sem", threading.BoundedSemaphore(2))
    monkeypatch.setattr(ps, "_pool", [])
    monkeypatch.setattr(ps.common, "connect", lambda pat=None: K())
    monkeypatch.setattr(ps.common, "dicts", dicts)
    return ps


def test_pool_permit_survives_keyboard_interrupt(monkeypatch):
    def boom(conn, sql, params):
        raise KeyboardInterrupt()
    ps = _panel(monkeypatch, boom)
    for _ in range(5):                       # 5 > 2 permits: a leak would deadlock here
        with pytest.raises(KeyboardInterrupt):
            ps.qd("select 1")
    assert ps._pool_sem._value == 2 and ps._pool == []


def test_qd_retries_once_on_a_dead_connection_only(monkeypatch):
    calls = []

    def flaky(conn, sql, params):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("connection terminated")
        return [{"ok": 1}]
    ps = _panel(monkeypatch, flaky)
    assert ps.qd("select 1") == [{"ok": 1}]
    assert len(calls) == 2 and ps._pool_sem._value == 2

    def bad_sql(conn, sql, params):
        calls.append(1)
        raise ValueError("syntax error")
    calls.clear()
    monkeypatch.setattr(ps.common, "dicts", bad_sql)
    with pytest.raises(ValueError):
        ps.qd("selec 1")
    assert len(calls) == 1 and ps._pool_sem._value == 2
