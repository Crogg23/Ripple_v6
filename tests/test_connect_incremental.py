"""Tests for connect/incremental.py -- the incremental (O(changed tables)) spine
updater. 2026-07-31: this was the largest module in connect/ (980 lines, the
most complex logic in the entity-resolution layer -- watermarks, keyset
diffing, bounded MERGE) with zero test coverage at all.

Most of this module's real work is Snowflake MERGE/temp-table orchestration
that can't be meaningfully tested without a warehouse -- those are marked
@pytest.mark.snowflake and self-skip without a live connection (see
tests/conftest.py). Everything that's pure Python or pure SQL-string
construction is tested offline here, including the exact diffing logic
(changed_tables' set arithmetic) via monkeypatched inputs -- no live
connection needed to prove that logic is right.
"""
from __future__ import annotations

import pytest

from connect import incremental as inc


class _FakeConn:
    """A stand-in for a Snowflake connection -- connect_one()/connect_changed()
    always call conn.close() in their finally block, so any mock connection
    object needs at least that."""
    def close(self):
        pass


# --------------------------------------------------------------------------- #
# pure helpers
# --------------------------------------------------------------------------- #
def test_entity_id_sql_is_content_addressed_and_deterministic():
    """ENTITY_ID = 'ENT_' || LEFT(MD5(key_type|val), 16) -- the whole incremental
    design depends on this being a pure function of (key_type, val), never a
    counter or a read of existing state (that's what lets a MERGE upsert
    converge with a full rebuild instead of renumbering entities)."""
    sql1 = inc._entity_id_sql("'NPI'", "'1234567890'")
    sql2 = inc._entity_id_sql("'NPI'", "'1234567890'")
    assert sql1 == sql2
    assert sql1.startswith("'ENT_' || LEFT(MD5(")
    assert "'NPI'" in sql1 and "'1234567890'" in sql1


def test_entity_id_sql_differs_by_key_type_and_value():
    a = inc._entity_id_sql("'NPI'", "'1234567890'")
    b = inc._entity_id_sql("'CCN'", "'1234567890'")
    c = inc._entity_id_sql("'NPI'", "'0000000000'")
    assert a != b
    assert a != c


def test_rowcount_handles_the_shapes_snowflake_actually_returns():
    assert inc._rowcount([(3,)]) == 3
    assert inc._rowcount([]) == 0
    assert inc._rowcount(None) == 0
    assert inc._rowcount([(None,)]) == 0
    assert inc._rowcount("not a rowset") == 0  # defensive: never raises


def test_json_passes_through_strings_and_dumps_lists():
    assert inc._json('["a","b"]') == '["a","b"]'
    assert inc._json(["a", "b"]) == '["a", "b"]'
    assert inc._json(None) == "[]"
    assert inc._json([]) == "[]"


def test_config_fingerprint_is_deterministic():
    """_config_fingerprint gates whether an incremental MERGE is safe to run at
    all (a NORM_RULES/DISPLAY_SPECS edit re-keys entities). It MUST be a pure,
    repeatable function of the current config -- two calls in the same process
    with no config change must agree, or the guard is meaningless."""
    a = inc._config_fingerprint()
    b = inc._config_fingerprint()
    assert a == b
    assert isinstance(a, str) and len(a) == 32  # md5 hexdigest


# --------------------------------------------------------------------------- #
# changed_tables() -- the diffing logic, offline via monkeypatched inputs
# --------------------------------------------------------------------------- #
def test_changed_tables_flags_a_moved_content_key(monkeypatch):
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {
        "FED_A": {"content_key": "new_hash"},
        "FED_B": {"content_key": "same_hash"},
    })
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {
        "FED_A": "old_hash", "FED_B": "same_hash"})
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: {"FED_A", "FED_B"})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {"FED_A": {}, "FED_B": {}})

    assert inc.changed_tables(None, scope="spine") == ["FED_A"]


def test_changed_tables_ignores_a_table_with_no_landing_table():
    """~31 source_ids log success/empty in INGEST_RUNS but never materialize a
    landing table (portal harvests). Reslicing one would read a table that
    doesn't exist -- changed_tables must filter these out, not just changed_tables'
    caller."""
    orig = inc.compute_watermarks, inc._stored_keys, inc._landing_tables, inc.DISPLAY_SPECS
    try:
        inc.compute_watermarks = lambda conn: {
            "FED_GHOST": {"content_key": "new_hash"},
            "FED_REAL": {"content_key": "new_hash"},
        }
        inc._stored_keys = lambda conn: {}  # both look brand-new (never seeded)
        inc._landing_tables = lambda conn: {"FED_REAL"}  # FED_GHOST has no landing table
        inc.DISPLAY_SPECS = {"FED_GHOST": {}, "FED_REAL": {}}
        assert inc.changed_tables(None, scope="spine") == ["FED_REAL"]
    finally:
        inc.compute_watermarks, inc._stored_keys, inc._landing_tables, inc.DISPLAY_SPECS = orig


def test_changed_tables_scope_all_covers_every_watermarked_table_not_just_spine(monkeypatch):
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {
        "FED_SPINE_TBL": {"content_key": "new"},
        "FED_NONSPINE_TBL": {"content_key": "new"},
    })
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {})
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: {"FED_SPINE_TBL", "FED_NONSPINE_TBL"})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {"FED_SPINE_TBL": {}})  # only one is a spine table

    assert inc.changed_tables(None, scope="spine") == ["FED_SPINE_TBL"]
    assert sorted(inc.changed_tables(None, scope="all")) == ["FED_NONSPINE_TBL", "FED_SPINE_TBL"]


def test_changed_tables_empty_when_nothing_moved(monkeypatch):
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {"FED_A": {"content_key": "x"}})
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {"FED_A": "x"})  # unchanged
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: {"FED_A"})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {"FED_A": {}})

    assert inc.changed_tables(None, scope="spine") == []


# --------------------------------------------------------------------------- #
# connect_one() -- the skip/no-op guard logic (offline, monkeypatched db)
# --------------------------------------------------------------------------- #
def test_connect_one_skips_a_source_with_no_ingest_runs_row(monkeypatch):
    monkeypatch.setattr(inc, "_reset_caches", lambda: None)
    monkeypatch.setattr(inc.db, "connect", lambda: _FakeConn())
    monkeypatch.setattr(inc, "validate_key_config", lambda: None)
    monkeypatch.setattr(inc, "_ddl", lambda conn: None)
    monkeypatch.setattr(inc, "_apply_config_drift_or_raise", lambda conn: None)
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: 1)  # SKEYSET_FQN already seeded
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {})  # no watermark at all
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {})

    out = inc.connect_one("fed_never_ran")
    assert out["mode"].startswith("skip (no success/empty")


def test_connect_one_skips_a_source_with_no_landing_table(monkeypatch):
    monkeypatch.setattr(inc, "_reset_caches", lambda: None)
    monkeypatch.setattr(inc.db, "connect", lambda: _FakeConn())
    monkeypatch.setattr(inc, "validate_key_config", lambda: None)
    monkeypatch.setattr(inc, "_ddl", lambda conn: None)
    monkeypatch.setattr(inc, "_apply_config_drift_or_raise", lambda conn: None)
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: 1)
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {"FED_PORTAL_ONLY": {"content_key": "x"}})
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {})  # not a spine table
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: set())  # and no landing table

    out = inc.connect_one("fed_portal_only")
    assert out["mode"].startswith("skip (no LIBRARY_RAW.LANDING")


def test_connect_one_is_a_noop_when_content_key_unchanged(monkeypatch):
    monkeypatch.setattr(inc, "_reset_caches", lambda: None)
    monkeypatch.setattr(inc.db, "connect", lambda: _FakeConn())
    monkeypatch.setattr(inc, "validate_key_config", lambda: None)
    monkeypatch.setattr(inc, "_ddl", lambda conn: None)
    monkeypatch.setattr(inc, "_apply_config_drift_or_raise", lambda conn: None)
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: 1)
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {"FED_A": {"content_key": "same"}})
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {"FED_A": "same"})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {"FED_A": {}})
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: {"FED_A"})

    out = inc.connect_one("fed_a")
    assert out["mode"] == "no-op (content-key unchanged)"


def test_connect_one_raises_if_never_seeded(monkeypatch):
    monkeypatch.setattr(inc, "_reset_caches", lambda: None)
    monkeypatch.setattr(inc.db, "connect", lambda: _FakeConn())
    monkeypatch.setattr(inc, "validate_key_config", lambda: None)
    monkeypatch.setattr(inc, "_ddl", lambda conn: None)
    monkeypatch.setattr(inc, "_apply_config_drift_or_raise", lambda conn: None)
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: 0)  # SKEYSET_FQN empty -> never seeded

    with pytest.raises(RuntimeError, match="not seeded"):
        inc.connect_one("fed_a")


def test_connect_one_routes_spine_table_to_reslice_spine_not_discover(monkeypatch):
    monkeypatch.setattr(inc, "_reset_caches", lambda: None)
    monkeypatch.setattr(inc.db, "connect", lambda: _FakeConn())
    monkeypatch.setattr(inc, "validate_key_config", lambda: None)
    monkeypatch.setattr(inc, "_ddl", lambda conn: None)
    monkeypatch.setattr(inc, "_apply_config_drift_or_raise", lambda conn: None)
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: 1)
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {"FED_A": {"content_key": "new"}})
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {"FED_A": "old"})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {"FED_A": {}})
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: {"FED_A"})

    calls = {}
    monkeypatch.setattr(inc, "reslice_spine",
                        lambda conn, table, run_id, dry_run=False: calls.setdefault("spine", table) or {"mode": "merged"})
    monkeypatch.setattr(inc, "reslice_discover",
                        lambda conn, table, run_id, dry_run=False: calls.setdefault("discover", table) or {"mode": "linked"})

    inc.connect_one("fed_a")
    assert calls == {"spine": "FED_A"}


def test_connect_one_routes_nonspine_table_to_reslice_discover(monkeypatch):
    monkeypatch.setattr(inc, "_reset_caches", lambda: None)
    monkeypatch.setattr(inc.db, "connect", lambda: _FakeConn())
    monkeypatch.setattr(inc, "validate_key_config", lambda: None)
    monkeypatch.setattr(inc, "_ddl", lambda conn: None)
    monkeypatch.setattr(inc, "_apply_config_drift_or_raise", lambda conn: None)
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: 1)
    monkeypatch.setattr(inc, "compute_watermarks", lambda conn: {"FED_B": {"content_key": "new"}})
    monkeypatch.setattr(inc, "_stored_keys", lambda conn: {"FED_B": "old"})
    monkeypatch.setattr(inc, "DISPLAY_SPECS", {})  # not a spine table
    monkeypatch.setattr(inc, "_landing_tables", lambda conn: {"FED_B"})
    monkeypatch.setattr(inc, "_upsert_watermark", lambda conn, table, wm: None)

    calls = {}
    monkeypatch.setattr(inc, "reslice_spine",
                        lambda conn, table, run_id, dry_run=False: calls.setdefault("spine", table) or {"mode": "merged"})
    monkeypatch.setattr(inc, "reslice_discover",
                        lambda conn, table, run_id, dry_run=False: calls.setdefault("discover", table) or {"mode": "linked"})

    inc.connect_one("fed_b")
    assert calls == {"discover": "FED_B"}


# --------------------------------------------------------------------------- #
# CLI dispatch
# --------------------------------------------------------------------------- #
def test_cli_dispatches_seed(monkeypatch):
    calls = {}
    monkeypatch.setattr(inc, "seed", lambda reseed=False: calls.setdefault("seed", reseed))
    inc.main(["seed", "--reseed"])
    assert calls == {"seed": True}


def test_cli_dispatches_connect_one(monkeypatch):
    calls = {}
    monkeypatch.setattr(inc, "connect_one",
                        lambda source, dry_run=False: calls.setdefault("connect_one", (source, dry_run)))
    inc.main(["connect-one", "--source", "fed_x", "--dry-run"])
    assert calls == {"connect_one": ("fed_x", True)}


def test_cli_dispatches_connect_changed(monkeypatch):
    calls = {}
    monkeypatch.setattr(inc, "connect_changed",
                        lambda scope="spine", dry_run=False: calls.setdefault("connect_changed", (scope, dry_run)))
    inc.main(["connect-changed", "--scope", "all"])
    assert calls == {"connect_changed": ("all", False)}


def test_cli_dispatches_validate(monkeypatch):
    calls = {}
    monkeypatch.setattr(inc, "validate", lambda table=None: calls.setdefault("validate", table))
    inc.main(["validate", "--table", "FED_X"])
    assert calls == {"validate": "FED_X"}


# --------------------------------------------------------------------------- #
# live equivalence proof -- the module ships its own non-destructive validator;
# use it. self-skips without a Snowflake connection.
# --------------------------------------------------------------------------- #
def _twin_lag(conn):
    """How far behind each rebuild twin is, in rows and in write time.

    The equivalence checks compare a live keyset against a transient twin that
    a full rebuild writes. If a load lands rows into the live table after the
    twin was last built, the two disagree for a reason that says nothing about
    whether the incremental logic is correct — the twin is simply older. This
    reads INFORMATION_SCHEMA only, so it costs no warehouse credits.
    """
    from connect import db
    rows = db.rows(conn, """
        SELECT TABLE_NAME, ROW_COUNT, LAST_ALTERED
        FROM LIBRARY_META.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'CONNECT'
          AND TABLE_NAME IN ('SPINE_KEYSET_LIVE', 'SPINE_KEYSET',
                             'KEYSET_LIVE', 'KEYSET_SCRATCH')
    """)
    seen = {name: (count, altered) for name, count, altered in rows}
    lag = []
    for live, twin in (("SPINE_KEYSET_LIVE", "SPINE_KEYSET"),
                       ("KEYSET_LIVE", "KEYSET_SCRATCH")):
        if live not in seen or twin not in seen:
            continue
        live_rows, live_at = seen[live]
        twin_rows, twin_at = seen[twin]
        if twin_at < live_at:
            lag.append(f"{twin} is {live_rows - twin_rows:,} rows and "
                       f"{(live_at - twin_at).days} days behind {live}")
    return lag


@pytest.mark.snowflake
def test_incremental_state_matches_full_rebuild_backstop(sf):
    """EFFECTIVELY RETIRED with the full rebuild (2026-08-30): validate()
    compares against transient scratch twins that only the retired rebuild
    wrote, so the staleness skip below fires on every run and this test never
    executes its assertion. It stays as the harness for a future re-pointed
    validate(); offline executing coverage for the MERGE logic lives in
    tests/test_connect_merge_offline.py (DuckDB).

    Skips when the rebuild twins are older than the live keysets -- with the
    rebuild retired, that is always.
    """
    lag = _twin_lag(sf)
    if lag:
        pytest.skip("rebuild twins are stale, so the comparison is meaningless: "
                    + "; ".join(lag))

    checks = inc.validate(table="FED_HHS_OIG_LEIE")
    failed = {k: v for k, v in checks.items() if not (v == "PASS" or v.startswith("PASS") or v.startswith("SKIP"))}
    assert not failed, f"incremental state diverged from the full-rebuild backstop: {failed}"


def test_drift_gate_refuses_implicit_apply(monkeypatch):
    """Implicit config drift inside connect_one/connect_changed must NOT
    reslice on its own -- it raises with the preview instructions unless
    RIPPLE_APPLY_CONFIG says go (2026-09-01 gate)."""
    monkeypatch.delenv("RIPPLE_APPLY_CONFIG", raising=False)
    monkeypatch.setattr(inc, "_config_drifted", lambda conn: True)
    applied = []
    monkeypatch.setattr(inc, "_apply_config_conn",
                        lambda conn, dry_run=False: applied.append(dry_run))
    with pytest.raises(RuntimeError, match="apply-config --dry-run"):
        inc._apply_config_drift_or_raise(None)
    assert applied == []


def test_drift_gate_opens_with_the_env_flag(monkeypatch):
    monkeypatch.setenv("RIPPLE_APPLY_CONFIG", "1")
    monkeypatch.setattr(inc, "_config_drifted", lambda conn: True)
    applied = []
    monkeypatch.setattr(inc, "_apply_config_conn",
                        lambda conn, dry_run=False: applied.append(dry_run))
    monkeypatch.setattr(inc.db, "scalar", lambda conn, sql: None)
    inc._apply_config_drift_or_raise(None)
    assert applied == [False]
