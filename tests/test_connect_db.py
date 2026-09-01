"""Tests for connect/db.py -- Snowflake credential loading, warehouse
lane-pinning, and fqn() table-name qualification. 2026-07-31: zero test
coverage on exactly the "errors matter" write/credential path CLAUDE.md and
the Bridge Fuel Reality memory flag as historically bug-prone on this
platform (masked/blank credential columns have already bitten it twice).
"""
from __future__ import annotations

import pytest

from connect import db


# --------------------------------------------------------------------------- #
# fqn() -- table-name qualification
# --------------------------------------------------------------------------- #
def test_fqn_qualifies_a_bare_table_name():
    assert db.fqn("fed_cms_nppes") == "LIBRARY_RAW.LANDING.FED_CMS_NPPES"


def test_fqn_passes_through_an_already_qualified_name():
    """A regression here would misqualify an already-3-part name into a wrong
    4-part or double-prefixed identifier -- silently pointing a query at the
    wrong table/schema."""
    assert db.fqn("OTHER_DB.OTHER_SCHEMA.SOME_TABLE") == "OTHER_DB.OTHER_SCHEMA.SOME_TABLE"


def test_fqn_uppercases_and_trims():
    assert db.fqn("  fed_x  ") == "LIBRARY_RAW.LANDING.FED_X"


def test_fqn_rejects_a_two_part_name():
    """Exactly one dot (schema.table) is neither a bare table nor a fully
    qualified name. The old code prefixed it into a 4-part garbage identifier
    that silently misrouted the query; ident() validation now raises instead
    (2026-09-01, hiring review connect W4)."""
    with pytest.raises(ValueError):
        db.fqn("SOME_SCHEMA.SOME_TABLE")


def test_ident_rejects_injection_shapes():
    for bad in ("T; DROP TABLE X", "T'||'", "T T", "T-1", ""):
        with pytest.raises(ValueError):
            db.ident(bad)
    assert db.ident(" fed_x ") == "FED_X"


# --------------------------------------------------------------------------- #
# connect() -- warehouse lane-pinning (the regression this file's own
# docstring says it was added to prevent: BUILD work silently sharing the
# serving warehouse with analyst reads)
# --------------------------------------------------------------------------- #
def test_connect_pins_the_etl_warehouse_when_set(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_ETL_WAREHOUSE", "DBT_WH")
    calls = {}
    monkeypatch.setattr(db.snow, "connect", lambda warehouse=None: calls.setdefault("warehouse", warehouse))
    db.connect()
    assert calls["warehouse"] == "DBT_WH"


def test_connect_falls_back_to_default_when_etl_warehouse_unset(monkeypatch):
    monkeypatch.delenv("SNOWFLAKE_ETL_WAREHOUSE", raising=False)
    calls = {}
    monkeypatch.setattr(db.snow, "connect", lambda warehouse=None: calls.setdefault("warehouse", warehouse))
    db.connect()
    assert calls["warehouse"] is None


def test_connect_treats_a_blank_etl_warehouse_as_unset(monkeypatch):
    """A blank-but-present env var (e.g. SNOWFLAKE_ETL_WAREHOUSE= in .env) must
    behave identically to unset, not silently pin to a warehouse named ''."""
    monkeypatch.setenv("SNOWFLAKE_ETL_WAREHOUSE", "   ")
    calls = {}
    monkeypatch.setattr(db.snow, "connect", lambda warehouse=None: calls.setdefault("warehouse", warehouse))
    db.connect()
    assert calls["warehouse"] is None


# --------------------------------------------------------------------------- #
# rows() / dicts() / scalar() -- cursor lifecycle
# --------------------------------------------------------------------------- #
class _FakeCursor:
    def __init__(self, data, cols):
        self.data = data
        self.description = [(c,) for c in cols]
        self.closed = False
        self.executed = None

    def execute(self, sql, params):
        self.executed = (sql, params)

    def fetchall(self):
        return self.data

    def close(self):
        self.closed = True


class _FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor


def test_rows_returns_raw_tuples_and_closes_the_cursor():
    cur = _FakeCursor([(1, "a"), (2, "b")], ["N", "S"])
    out = db.rows(_FakeConn(cur), "SELECT N, S FROM t")
    assert out == [(1, "a"), (2, "b")]
    assert cur.closed is True
    assert cur.executed == ("SELECT N, S FROM t", ())


def test_rows_binds_params_and_closes_cursor_even_on_error():
    class _BoomCursor(_FakeCursor):
        def execute(self, sql, params):
            raise RuntimeError("boom")

    cur = _BoomCursor([], [])
    with pytest.raises(RuntimeError):
        db.rows(_FakeConn(cur), "SELECT 1", (42,))
    assert cur.closed is True  # the finally: cur.close() must still run


def test_dicts_zips_columns_with_rows():
    cur = _FakeCursor([(1, "tulsa"), (2, "york")], ["ID", "CITY"])
    out = db.dicts(_FakeConn(cur), "SELECT ID, CITY FROM t")
    assert out == [{"ID": 1, "CITY": "tulsa"}, {"ID": 2, "CITY": "york"}]
    assert cur.closed is True


def test_dicts_empty_result_is_an_empty_list_not_none():
    cur = _FakeCursor([], ["ID"])
    assert db.dicts(_FakeConn(cur), "SELECT ID FROM t WHERE 1=0") == []
