"""MERGE logic against a real database engine, no warehouse (DuckDB).

The review's blocker: connect's MERGE/keyset SQL had ZERO executing coverage --
validate() needs scratch twins only the retired full rebuild wrote. This file
runs the actual SQL strings the module builds, against DuckDB, on fixture rows.

The regression proven here: _merge_nodes used to DELETE on TABLE_NAME +
KEY_VALUE only, while the re-INSERT joined on KEY_TYPE + VAL. A value shared
by two key types on a two-key table was deleted for BOTH types and restored
for one -- silent row loss. The fix scopes the DELETE to the (KEY_TYPE,
KEY_VALUE) pair.
"""
import duckdb
import pytest

from connect import incremental


def _dialect(sql: str) -> str:
    """The one Snowflake-ism DuckDB rejects: CURRENT_TIMESTAMP takes no parens."""
    return sql.replace("CURRENT_TIMESTAMP()", "CURRENT_TIMESTAMP")


class DuckDb:
    """Shim matching connect.db's rows/scalar surface over a DuckDB conn."""

    @staticmethod
    def rows(conn, sql, params=None):
        return conn.execute(_dialect(sql), params or []).fetchall()

    @staticmethod
    def scalar(conn, sql, params=None):
        row = conn.execute(sql, params or []).fetchone()
        return row[0] if row else None


@pytest.fixture
def duck(monkeypatch):
    conn = duckdb.connect()
    monkeypatch.setattr(incremental.db, "rows", DuckDb.rows)
    monkeypatch.setattr(incremental.db, "scalar", DuckDb.scalar)
    monkeypatch.setattr(incremental, "NODES_FQN", "CONNECT_NODES")
    monkeypatch.setattr(incremental, "EMAP_FQN", "ENTITY_MAP")
    monkeypatch.setattr(incremental, "LEADS_FQN", "LEADS")
    conn.execute("""CREATE TABLE CONNECT_NODES (
        NODE_ID VARCHAR, KEY_TYPE VARCHAR, KEY_VALUE VARCHAR,
        TABLE_NAME VARCHAR, RUN_ID VARCHAR, BUILT_AT TIMESTAMP)""")
    conn.execute("CREATE TABLE _AFFECTED (KEY_TYPE VARCHAR, VAL VARCHAR)")
    conn.execute("CREATE TABLE _NEW (KEY_TYPE VARCHAR, VAL VARCHAR)")
    yield conn
    conn.close()


def _nodes(conn):
    return sorted(conn.execute(
        "SELECT KEY_TYPE, KEY_VALUE, TABLE_NAME FROM CONNECT_NODES").fetchall())


def test_merge_nodes_cross_key_collision_survives(duck):
    """EIN and DUNS share the value on one table; only EIN is affected.
    The DUNS row must survive the merge -- the old code deleted it forever."""
    duck.execute("""INSERT INTO CONNECT_NODES VALUES
        ('n1', 'EIN',  '123456789', 'T1', 'r0', now()),
        ('n2', 'DUNS', '123456789', 'T1', 'r0', now())""")
    duck.execute("INSERT INTO _AFFECTED VALUES ('EIN', '123456789')")
    duck.execute("INSERT INTO _NEW VALUES ('EIN', '123456789')")

    incremental._merge_nodes(duck, "T1", "r1")

    assert _nodes(duck) == [
        ("DUNS", "123456789", "T1"),   # untouched -- the regression
        ("EIN", "123456789", "T1"),    # re-inserted for run r1
    ]


def test_merge_nodes_retracts_a_vanished_key(duck):
    """Affected but absent from _NEW -> deleted and NOT re-inserted."""
    duck.execute("""INSERT INTO CONNECT_NODES VALUES
        ('n1', 'EIN', '999', 'T1', 'r0', now())""")
    duck.execute("INSERT INTO _AFFECTED VALUES ('EIN', '999')")
    # _NEW is empty: the key vanished from the landing slice

    incremental._merge_nodes(duck, "T1", "r1")

    assert _nodes(duck) == []


def test_merge_nodes_other_tables_untouched(duck):
    """The per-table scope: sibling tables keep their rows for affected vals."""
    duck.execute("""INSERT INTO CONNECT_NODES VALUES
        ('n1', 'EIN', '111', 'T1', 'r0', now()),
        ('n2', 'EIN', '111', 'T2', 'r0', now())""")
    duck.execute("INSERT INTO _AFFECTED VALUES ('EIN', '111')")
    duck.execute("INSERT INTO _NEW VALUES ('EIN', '111')")

    incremental._merge_nodes(duck, "T1", "r1")

    assert ("EIN", "111", "T2") in _nodes(duck)
    assert ("EIN", "111", "T1") in _nodes(duck)


def test_backfill_leads_counts_only_restamped_rows(duck, monkeypatch):
    """The run stat is rows the UPDATE touched, not every non-null id ever."""
    monkeypatch.setattr(incremental, "_table_exists", lambda conn, name: True)
    duck.execute("""CREATE TABLE LEADS (
        LEFT_KEY_TYPE VARCHAR, LEFT_KEY_VALUE VARCHAR, LEFT_ENTITY_ID VARCHAR)""")
    duck.execute("""CREATE TABLE ENTITY_MAP (
        KEY_TYPE VARCHAR, KEY_VALUE VARCHAR, ENTITY_ID VARCHAR)""")
    duck.execute("""INSERT INTO LEADS VALUES
        ('EIN', '111', NULL),
        ('EIN', '222', 'ENT_already_stamped')""")
    duck.execute("INSERT INTO ENTITY_MAP VALUES ('EIN', '111', 'ENT_new')")
    duck.execute("INSERT INTO _AFFECTED VALUES ('EIN', '111')")

    n = incremental._backfill_leads(duck)

    assert n == 1  # the old stat would have said 2
    stamped = duck.execute(
        "SELECT LEFT_ENTITY_ID FROM LEADS WHERE LEFT_KEY_VALUE='111'").fetchone()
    assert stamped[0] == "ENT_new"
