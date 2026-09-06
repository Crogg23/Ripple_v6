"""The landing helper decides whether a load is allowed to replace a live table.

A wrong answer here silently overwrites good data with a truncated pull, which
is what happened to SAM: 1,000 rows of ~167,000 landed and logged success.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "scripts"))

import land_frame  # noqa: E402


class _Cur:
    def __init__(self, prior):
        self.prior = prior

    def execute(self, *a, **k):
        return self

    def fetchone(self):
        return (self.prior,) if self.prior is not None else None

    def close(self):
        pass


class _Conn:
    def __init__(self, prior=None):
        self.prior = prior

    def cursor(self):
        return _Cur(self.prior)

    def close(self):
        pass


@pytest.fixture
def logged(monkeypatch):
    seen = []
    monkeypatch.setattr(land_frame.ingest, "_log_run",
                        lambda *a, **k: seen.append(a[3]))
    monkeypatch.setattr(land_frame.ingest, "_load_landing",
                        lambda *a, **k: seen.append("WROTE"))
    # NOT faked. The first cut mocked assess_density with {"ok": True}, a key
    # the real function never returns, so the gate was a rubber stamp and the
    # tests agreed with the bug.
    return seen


def _df(n):
    return pd.DataFrame({"A": [f"v{i}" for i in range(n)]})


def test_a_healthy_table_is_not_overwritten_by_a_truncated_pull(logged):
    out = land_frame.land(_df(1000), "SRC", "u", "m", conn=_Conn(prior=167000))
    assert out["status"] == "partial"
    assert "WROTE" not in logged


def test_a_normal_reload_lands(logged):
    out = land_frame.land(_df(170000), "SRC", "u", "m", conn=_Conn(prior=167000))
    assert out["status"] == "success"
    assert "WROTE" in logged


def test_a_small_wobble_still_lands(logged):
    # 99% of last time is normal churn, not a truncated pull.
    out = land_frame.land(_df(99000), "SRC", "u", "m", conn=_Conn(prior=100000))
    assert out["status"] == "success"


def test_a_declared_floor_is_enforced(logged):
    out = land_frame.land(_df(50), "SRC", "u", "m", expect_rows=1000,
                          conn=_Conn(prior=None))
    assert out["status"] == "partial"
    assert "WROTE" not in logged


def test_a_real_shrink_can_be_authorised(logged):
    # expect_rows=0 is how a caller says the source really did get smaller.
    out = land_frame.land(_df(10), "SRC", "u", "m", expect_rows=0,
                          conn=_Conn(prior=100000))
    assert out["status"] == "success"


def test_the_real_density_gate_says_empty_on_an_all_blank_frame(monkeypatch):
    # The real ingest.assess_density, not a stand-in for it.
    monkeypatch.setattr(land_frame.ingest, "_log_run", lambda *a, **k: None)
    monkeypatch.setattr(land_frame.ingest, "_load_landing", lambda *a, **k: None)
    blank = pd.DataFrame({"A": [""] * 50, "B": [None] * 50})
    out = land_frame.land(blank, "SRC", "u", "m", conn=_Conn(prior=None))
    assert out["status"] == "empty", out


def test_the_real_density_gate_passes_a_normal_frame(monkeypatch):
    monkeypatch.setattr(land_frame.ingest, "_log_run", lambda *a, **k: None)
    monkeypatch.setattr(land_frame.ingest, "_load_landing", lambda *a, **k: None)
    out = land_frame.land(_df(500), "SRC", "u", "m", conn=_Conn(prior=None))
    assert out["status"] == "success", out


def test_the_gate_reads_the_key_the_real_function_returns():
    src = (_REPO / "scripts" / "land_frame.py").read_text()
    assert 'density["empty"]' in src
    assert 'density.get("ok"' not in src


def test_the_run_log_gets_a_real_byte_count(monkeypatch):
    seen = {}
    monkeypatch.setattr(land_frame.ingest, "_load_landing", lambda *a, **k: None)
    monkeypatch.setattr(land_frame.ingest, "_log_run",
                        lambda *a, **k: seen.update(bytes=a[5]))
    land_frame.land(_df(500), "SRC", "u", "m", conn=_Conn(prior=None))
    assert seen["bytes"] > 0


def test_no_live_loader_imports_the_drawer():
    import glob
    bad = []
    for f in glob.glob(str(_REPO / "scripts" / "*.py")):
        if "land_frame" in f:
            continue
        if "from build_skeleton import" in Path(f).read_text():
            bad.append(Path(f).name)
    assert not bad, bad


def test_every_row_gets_the_three_stamps(monkeypatch):
    got = {}
    monkeypatch.setattr(land_frame.ingest, "_log_run", lambda *a, **k: None)
    monkeypatch.setattr(land_frame.ingest, "_load_landing",
                        lambda conn, df, table, **k: got.update(cols=list(df.columns)))
    land_frame.land(_df(5), "SRC", "u", "m", conn=_Conn(prior=None))
    for c in land_frame.META:
        assert c in got["cols"]


def test_the_two_repaired_loaders_no_longer_import_the_drawer():
    for name in ("congress_committee_membership_load",
                 "fec_independent_expenditure_load"):
        src = (_REPO / "scripts" / f"{name}.py").read_text()
        assert "build_skeleton" not in src, name
        assert "from land_frame import land" in src, name
