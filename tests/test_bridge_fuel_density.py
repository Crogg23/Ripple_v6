"""Offline behavioral tests for the backfill loader's hardening (scripts/bridge_fuel_load.py).

These pin the must-fix guarantees from the stress-tests, with ALL Snowflake/network I/O
stubbed (no connection, no download):

  * an empty / parse-failure husk is logged STATUS='empty' and NOT registered
    (the FED_FJC_IDB failure mode must never ride into the catalog), on BOTH the
    plain and the chunked path;
  * a healthy load is logged 'success' and registered;
  * the chunked path is ATOMIC: chunks write to <TABLE>__STAGING, a mid-stream crash
    drops the STAGING table ONLY (never the live table — the old code dropped LIVE,
    the path that would have deleted NPPES's surviving rows) and logs 'failed';
  * on chunked success the ordering is pinned: swap -> log 'success' -> register;
  * a schema-drifted staging table REFUSES the swap (--allow-schema-change overrides);
  * a download/parse failure before any landing write still logs a 'failed' run;
  * _register skips the MERGE when a registry row already exists (curated facets
    must never be clobbered by a re-land/--refresh).
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "scripts", ROOT / "library-onboarding", ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import bridge_fuel_load as bfl   # noqa: E402


class _Conn:
    """Stand-in Snowflake connection: only .close() is ever called on it here."""
    def close(self):
        pass


def _healthy_df():
    return pd.DataFrame({"EIN": ["123456789", "987654321"], "NAME": ["A Corp", "B Inc"]})


def _empty_df():
    # Source columns present but every cell blank -> the husk shape the gate demotes.
    return pd.DataFrame({"EIN": ["", "", ""], "NAME": ["", "", ""]})


def _spec(**over):
    s = {"source_id": "test_src", "download_url": "http://example/x.csv", "name": "Test Source"}
    s.update(over)
    return s


def _stub_common(monkeypatch, logged, registered):
    monkeypatch.setattr(bfl.snow, "connect", lambda *a, **k: _Conn())
    monkeypatch.setattr(bfl, "_has_success", lambda conn, sid: False)
    monkeypatch.setattr(bfl, "_open_csv_source", lambda s, tmp: Path(tmp) / "src.csv")
    monkeypatch.setattr(bfl.ingest, "_log_run",
                        lambda conn, sid, run_id, status, *a, **k: logged.append(status))
    monkeypatch.setattr(bfl, "_register", lambda conn, s: registered.append(s["source_id"]))


# --------------------------------------------------------------------------- #
# Non-chunked path
# --------------------------------------------------------------------------- #
def test_nonchunked_empty_load_is_demoted_not_registered(monkeypatch):
    logged, registered = [], []
    _stub_common(monkeypatch, logged, registered)
    monkeypatch.setattr(bfl.ingest, "_load_landing", lambda *a, **k: None)
    monkeypatch.setattr(bfl, "_read_full", lambda src, opts: _empty_df())

    res = bfl.load_spec(_spec(), do_run=True)

    assert res["status"] == "empty"
    assert logged == ["empty"]          # logged empty, never success
    assert registered == []             # the husk must NOT become a catalog source


def test_nonchunked_healthy_load_registers(monkeypatch):
    logged, registered = [], []
    _stub_common(monkeypatch, logged, registered)
    monkeypatch.setattr(bfl.ingest, "_load_landing", lambda *a, **k: None)
    monkeypatch.setattr(bfl, "_read_full", lambda src, opts: _healthy_df())

    res = bfl.load_spec(_spec(), do_run=True)

    assert res["status"] == "loaded"
    assert logged == ["success"]
    assert registered == ["test_src"]


def test_download_failure_logs_failed_run(monkeypatch):
    # A failure BEFORE any landing write (bad URL, missing zip member) used to die
    # with no INGEST_RUNS row at all — the outer catch must leave a 'failed' trace.
    logged, registered = [], []
    _stub_common(monkeypatch, logged, registered)

    def _boom(s, tmp):
        raise RuntimeError("404 not found")

    monkeypatch.setattr(bfl, "_open_csv_source", _boom)

    with pytest.raises(RuntimeError):
        bfl.load_spec(_spec(), do_run=True)

    assert logged == ["failed"]
    assert registered == []


def test_preview_download_failure_stays_side_effect_free(monkeypatch):
    # Previews must never write to INGEST_RUNS, even when they crash.
    logged, registered = [], []
    _stub_common(monkeypatch, logged, registered)

    def _boom(s, tmp):
        raise RuntimeError("404 not found")

    monkeypatch.setattr(bfl, "_open_csv_source", _boom)

    with pytest.raises(RuntimeError):
        bfl.load_spec(_spec(), do_run=False)

    assert logged == []


def test_nonchunked_load_failure_is_not_double_logged(monkeypatch):
    # The inner handler logs 'failed'; the outer catch must not log the run AGAIN.
    logged, registered = [], []
    _stub_common(monkeypatch, logged, registered)
    monkeypatch.setattr(bfl, "_read_full", lambda src, opts: _healthy_df())

    def _boom(*a, **k):
        raise RuntimeError("write exploded")

    monkeypatch.setattr(bfl.ingest, "_load_landing", _boom)

    with pytest.raises(RuntimeError):
        bfl.load_spec(_spec(), do_run=True)

    assert logged == ["failed"]         # exactly once


# --------------------------------------------------------------------------- #
# Chunked path (staging + atomic swap)
# --------------------------------------------------------------------------- #
def _stub_chunked(monkeypatch, logged, registered, executed, chunks,
                  write_fail_on=None, write_targets=None):
    _stub_common(monkeypatch, logged, registered)
    monkeypatch.setattr(bfl.snow, "execute", lambda conn, sql, *a, **k: executed.append(sql))
    monkeypatch.setattr(bfl, "_iter_chunks", lambda src, opts, n: iter(chunks))

    state = {"n": 0}

    def _fake_write_pandas(conn, df, **k):
        state["n"] += 1
        if write_targets is not None:
            write_targets.append(k.get("table_name"))
        if write_fail_on and state["n"] == write_fail_on:
            raise RuntimeError("simulated write_pandas crash")
        return True, 1, len(df), None

    monkeypatch.setattr("snowflake.connector.pandas_tools.write_pandas", _fake_write_pandas)


def test_chunked_writes_go_to_staging_never_live(monkeypatch):
    logged, registered, executed, targets = [], [], [], []
    chunks = [_healthy_df(), _healthy_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks, write_targets=targets)
    monkeypatch.setattr(bfl, "_table_columns", lambda *a, **k: None)   # first load
    monkeypatch.setattr(bfl.atomic_load, "execute_swap", lambda *a, **k: None)

    res = bfl.load_spec(_spec(chunked=True), do_run=True)

    assert res["status"] == "loaded"
    assert targets == ["TEST_SRC__STAGING", "TEST_SRC__STAGING"]


def test_chunked_success_order_is_swap_then_log_then_register(monkeypatch):
    # The pinned atomicity ordering: a 'success' row must mean the LIVE table holds
    # the rows (swap already done), and registration always comes last.
    events = []
    monkeypatch.setattr(bfl.snow, "connect", lambda *a, **k: _Conn())
    monkeypatch.setattr(bfl.snow, "execute", lambda conn, sql, *a, **k: None)
    monkeypatch.setattr(bfl, "_has_success", lambda conn, sid: False)
    monkeypatch.setattr(bfl, "_open_csv_source", lambda s, tmp: Path(tmp) / "src.csv")
    monkeypatch.setattr(bfl, "_iter_chunks", lambda src, opts, n: iter([_healthy_df()]))
    monkeypatch.setattr("snowflake.connector.pandas_tools.write_pandas",
                        lambda conn, df, **k: (True, 1, len(df), None))
    monkeypatch.setattr(bfl, "_table_columns", lambda *a, **k: None)
    monkeypatch.setattr(bfl.atomic_load, "execute_swap",
                        lambda *a, **k: events.append("swap"))
    monkeypatch.setattr(bfl.ingest, "_log_run",
                        lambda conn, sid, run_id, status, *a, **k: events.append(f"log:{status}"))
    monkeypatch.setattr(bfl, "_register", lambda conn, s: events.append("register"))

    res = bfl.load_spec(_spec(chunked=True), do_run=True)

    assert res["status"] == "loaded"
    assert events == ["swap", "log:success", "register"]


def test_chunked_crash_drops_staging_only_and_logs_failed(monkeypatch):
    logged, registered, executed = [], [], []
    chunks = [_healthy_df(), _healthy_df(), _healthy_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks, write_fail_on=2)

    with pytest.raises(RuntimeError):
        bfl.load_spec(_spec(chunked=True), do_run=True)

    drops = [s for s in executed if "DROP TABLE IF EXISTS" in s]
    assert drops and all("TEST_SRC__STAGING" in s for s in drops)   # staging cleaned up...
    assert not any('"TEST_SRC"' in s for s in drops)                # ...live NEVER dropped
    assert logged == ["failed"]                                     # logged failed, once
    assert registered == []                                         # never registered a crashed load


def test_chunked_empty_stream_drops_staging_not_registered(monkeypatch):
    logged, registered, executed = [], [], []
    chunks = [_empty_df(), _empty_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks)

    res = bfl.load_spec(_spec(chunked=True), do_run=True)

    assert res["status"] == "empty"
    assert logged == ["empty"]
    assert registered == []
    drops = [s for s in executed if "DROP TABLE IF EXISTS" in s]
    assert drops and all("TEST_SRC__STAGING" in s for s in drops)   # husk staging dropped
    assert not any('"TEST_SRC"' in s for s in drops)                # live untouched


def test_chunked_schema_drift_refuses_swap(monkeypatch):
    # Live table exists with a different column set -> the swap must be REFUSED
    # (the landed column names are the dbt/connect contract).
    logged, registered, executed = [], [], []
    chunks = [_healthy_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks)
    monkeypatch.setattr(
        bfl, "_table_columns",
        lambda conn, db, sc, t: ["EIN", "NAME"] if t.endswith("__STAGING") else ["EIN", "NAME", "EXTRA"])
    swaps = []
    monkeypatch.setattr(bfl.atomic_load, "execute_swap", lambda *a, **k: swaps.append(1))

    with pytest.raises(RuntimeError, match="schema drift"):
        bfl.load_spec(_spec(chunked=True), do_run=True)

    assert swaps == []                  # the drifted staging never went live
    assert logged == ["failed"]         # trace left by load_spec's outer catch
    assert registered == []


def test_chunked_schema_drift_override_allows_swap(monkeypatch):
    # --allow-schema-change: genuine source evolution may swap through the check.
    logged, registered, executed = [], [], []
    chunks = [_healthy_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks)
    monkeypatch.setattr(
        bfl, "_table_columns",
        lambda conn, db, sc, t: ["EIN", "NAME"] if t.endswith("__STAGING") else ["EIN", "NAME", "EXTRA"])
    swaps = []
    monkeypatch.setattr(bfl.atomic_load, "execute_swap", lambda *a, **k: swaps.append(1))

    res = bfl.load_spec(_spec(chunked=True), do_run=True, allow_schema_change=True)

    assert res["status"] == "loaded"
    assert swaps == [1]
    assert logged == ["success"]


# --------------------------------------------------------------------------- #
# Registry facet-clobber guard
# --------------------------------------------------------------------------- #
def test_register_skips_merge_when_row_exists(monkeypatch):
    # A re-land/--refresh of an already-cataloged source must NOT re-run the MERGE:
    # it would overwrite curated facets with the spec's non-null defaults.
    executed = []
    monkeypatch.setattr(bfl.snow, "execute", lambda conn, *a, **k: executed.append(a))
    monkeypatch.setattr(bfl, "_registry_has_row", lambda conn, sid: True)

    bfl._register(_Conn(), _spec())

    assert executed == []


def test_register_merges_when_row_absent(monkeypatch):
    executed = []
    monkeypatch.setattr(bfl.snow, "execute", lambda conn, *a, **k: executed.append(a))
    monkeypatch.setattr(bfl, "_registry_has_row", lambda conn, sid: False)

    bfl._register(_Conn(), _spec())

    assert len(executed) == 1           # the register MERGE ran exactly once
