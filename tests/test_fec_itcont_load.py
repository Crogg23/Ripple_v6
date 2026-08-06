"""Offline behavioral tests for scripts/fec_itcont_load.py (no network, no Snowflake).

Pin the smoke-run and failure guarantees from the 2026-07-02 hardening:

  * a --max-rows SMOKE run never swaps — the live 84M-row table must never be
    replaced by a capped slice — and logs its own status ('smoke', not 'success');
  * a full run swaps then logs 'success';
  * a mid-stream crash logs a 'failed' INGEST_RUNS row and re-raises (a dead run
    must never be invisible to the freshness ledger).
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "scripts", ROOT / "library-onboarding", ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import fec_itcont_load as fec   # noqa: E402


class _Conn:
    def close(self):
        pass


def _stub(monkeypatch, tmp_path, logged, swaps, lines_per_cycle=3, write_fail=False,
          prev_success_rows=None):
    monkeypatch.setattr(fec.snow, "connect", lambda *a, **k: _Conn())
    monkeypatch.setattr(fec.snow, "execute", lambda conn, sql, *a, **k: None)
    monkeypatch.setattr(fec, "download", lambda url, path: None)
    monkeypatch.setattr(fec, "stream_lines", lambda z: iter(["a|b|c"] * lines_per_cycle))
    # keep the zip cache/cleanup away from the REAL temp dir (a full-run test would
    # otherwise delete a genuinely cached indiv24.zip on this machine)
    monkeypatch.setattr(fec.tempfile, "gettempdir", lambda: str(tmp_path))
    # never-shrink floor's row-count lookup (added 2026-08-06) -- None means "no
    # prior successful run", the same real-world default _latest_success_rows
    # returns, so the floor check is a no-op unless a test opts into a value.
    monkeypatch.setattr(fec.ingest, "_latest_success_rows",
                        lambda conn, sid: prev_success_rows)

    def _write_chunk(conn, lines, run_id, started, first):
        if write_fail:
            raise RuntimeError("boom mid-chunk")
        return len(lines), 0

    monkeypatch.setattr(fec, "write_chunk", _write_chunk)
    monkeypatch.setattr(fec.atomic_load, "execute_swap",
                        lambda *a, **k: swaps.append(a))
    monkeypatch.setattr(fec.ingest, "_log_run",
                        lambda conn, sid, run_id, status, *a, **k: logged.append(status))


def test_capped_smoke_never_swaps(monkeypatch, tmp_path):
    logged, swaps = [], []
    _stub(monkeypatch, tmp_path, logged, swaps)

    rc = fec.main(["--max-rows", "2"])

    assert rc == 0
    assert swaps == []              # live table untouched — the whole point
    assert logged == ["smoke"]      # its own status; 'success' whitelists stay clean


def test_full_run_swaps_then_logs_success(monkeypatch, tmp_path):
    logged, swaps = [], []
    _stub(monkeypatch, tmp_path, logged, swaps)

    rc = fec.main([])

    assert rc == 0
    assert len(swaps) == 1
    assert logged == ["success"]


def test_shrunk_run_refuses_swap(monkeypatch, tmp_path):
    """A run landing far fewer rows than the last success must NOT swap (the
    empty/near-empty-stream case the never-shrink floor exists to catch)."""
    logged, swaps = [], []
    # 2 cycles x 3 lines = 6 rows this run; prior success was 1,000,000 -- well
    # under the 50% floor.
    _stub(monkeypatch, tmp_path, logged, swaps, prev_success_rows=1_000_000)

    rc = fec.main([])

    assert rc == 1
    assert swaps == []               # live table untouched
    assert logged == ["partial"]     # visibly flagged, not silently 'success'


def test_run_above_floor_still_swaps(monkeypatch, tmp_path):
    """A run that's shrunk a little (normal variance) but stays above the 50%
    floor must swap normally -- the guard shouldn't false-positive on that."""
    logged, swaps = [], []
    # 2 cycles x 3 lines = 6 rows this run; floor only trips below 3.
    _stub(monkeypatch, tmp_path, logged, swaps, prev_success_rows=10)

    rc = fec.main([])

    assert rc == 0
    assert len(swaps) == 1
    assert logged == ["success"]


def test_crash_logs_failed_and_reraises(monkeypatch, tmp_path):
    logged, swaps = [], []
    _stub(monkeypatch, tmp_path, logged, swaps, write_fail=True)

    with pytest.raises(RuntimeError, match="boom mid-chunk"):
        fec.main([])

    assert swaps == []              # never swapped a broken run
    assert logged == ["failed"]     # the run left a trace
