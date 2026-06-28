"""Offline behavioral tests for the backfill loader's hardening (scripts/bridge_fuel_load.py).

These pin the must-fix guarantees from the stress-test, with ALL Snowflake/network I/O
stubbed (no connection, no download):

  * an empty / parse-failure husk is logged STATUS='empty' and NOT registered
    (the FED_FJC_IDB failure mode must never ride into the catalog), on BOTH the
    plain and the chunked path;
  * a healthy load is logged 'success' and registered;
  * a chunked load that crashes mid-stream DROPS its partial table and logs 'failed'
    (the partial must not read as 'landed').
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "scripts", ROOT / "library-onboarding"):
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


# --------------------------------------------------------------------------- #
# Chunked path
# --------------------------------------------------------------------------- #
def _stub_chunked(monkeypatch, logged, registered, executed, chunks, write_fail_on=None):
    _stub_common(monkeypatch, logged, registered)
    monkeypatch.setattr(bfl.snow, "execute", lambda conn, sql, *a, **k: executed.append(sql))
    monkeypatch.setattr(bfl, "_iter_chunks", lambda src, opts, n: iter(chunks))

    state = {"n": 0}

    def _fake_write_pandas(conn, df, **k):
        state["n"] += 1
        if write_fail_on and state["n"] == write_fail_on:
            raise RuntimeError("simulated write_pandas crash")
        return True, 1, len(df), None

    monkeypatch.setattr("snowflake.connector.pandas_tools.write_pandas", _fake_write_pandas)


def test_chunked_crash_drops_partial_and_logs_failed(monkeypatch):
    logged, registered, executed = [], [], []
    chunks = [_healthy_df(), _healthy_df(), _healthy_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks, write_fail_on=2)

    with pytest.raises(RuntimeError):
        bfl.load_spec(_spec(chunked=True), do_run=True)

    assert any("DROP TABLE IF EXISTS" in s for s in executed)   # partial table cleaned up
    assert logged == ["failed"]                                 # logged failed, not success
    assert registered == []                                     # never registered a crashed load


def test_chunked_empty_stream_is_demoted_not_registered(monkeypatch):
    logged, registered, executed = [], [], []
    chunks = [_empty_df(), _empty_df()]
    _stub_chunked(monkeypatch, logged, registered, executed, chunks)

    res = bfl.load_spec(_spec(chunked=True), do_run=True)

    assert res["status"] == "empty"
    assert logged == ["empty"]
    assert registered == []
