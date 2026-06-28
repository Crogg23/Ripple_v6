"""Offline tests for the Wave-0 foundation: multi-file loader, EO BMF spec, budget DDL."""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "scripts", ROOT / "library-onboarding"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import bridge_fuel_load as bfl   # noqa: E402


# --------------------------------------------------------------------------- #
# Multi-file concat loader (_read_multi)
# --------------------------------------------------------------------------- #
def test_read_multi_concats_same_schema(monkeypatch, tmp_path):
    parts = [pd.DataFrame({"EIN": ["1", "2"], "NAME": ["A", "B"]}),
             pd.DataFrame({"EIN": ["3"], "NAME": ["C"]})]
    it = iter(parts)
    monkeypatch.setattr(bfl, "_download", lambda url, dest, **k: dest)
    monkeypatch.setattr(bfl, "_read_full", lambda path, opts: next(it))

    out = bfl._read_multi({"source_id": "x", "urls": ["u1", "u2"]}, tmp_path, {})

    assert list(out.columns) == ["EIN", "NAME"]
    assert len(out) == 3


def test_read_multi_rejects_schema_drift(monkeypatch, tmp_path):
    # A drifted partition (different columns) must FAIL LOUD, not silently union+NaN.
    parts = [pd.DataFrame({"EIN": ["1"]}), pd.DataFrame({"DIFFERENT": ["x"]})]
    it = iter(parts)
    monkeypatch.setattr(bfl, "_download", lambda url, dest, **k: dest)
    monkeypatch.setattr(bfl, "_read_full", lambda path, opts: next(it))

    with pytest.raises(RuntimeError, match="mismatched schemas"):
        bfl._read_multi({"source_id": "x", "urls": ["u1", "u2"]}, tmp_path, {})


def test_read_multi_preview_reads_first_only(monkeypatch, tmp_path):
    calls = {"n": 0}

    def _rf(path, opts):
        calls["n"] += 1
        return pd.DataFrame({"EIN": ["1"]})

    monkeypatch.setattr(bfl, "_download", lambda url, dest, **k: dest)
    monkeypatch.setattr(bfl, "_read_full", _rf)

    bfl._read_multi({"source_id": "x", "urls": ["u1", "u2", "u3"]}, tmp_path, {}, preview=True)
    assert calls["n"] == 1          # only the first file fetched in preview


# --------------------------------------------------------------------------- #
# EO BMF spec (the first-GO source)
# --------------------------------------------------------------------------- #
def test_eo_bmf_spec_is_wellformed():
    import bridge_fuel_specs as bfs
    specs = {d["source_id"]: d for d in bfs.SPECS}
    assert "xc_irs_eo_bmf" in specs
    s = specs["xc_irs_eo_bmf"]
    assert s["kind"] == "csv_multi"
    assert len(s["urls"]) == 6 and all(u.startswith("https://www.irs.gov/") for u in s["urls"])
    assert s["join_keys_std"] == ["EIN"] and s["join_key_tier"] == "STEEL"


# --------------------------------------------------------------------------- #
# Budget monitor DDL (pure)
# --------------------------------------------------------------------------- #
def test_alter_sql_uses_alter_not_replace():
    from budget_sprint import _alter_sql
    sql = _alter_sql(100, 90)
    assert sql.startswith("ALTER RESOURCE MONITOR RIPPLE_BUDGET")
    assert "CREATE OR REPLACE" not in sql          # replace would detach the binding
    assert "CREDIT_QUOTA = 100" in sql
    assert "SUSPEND_IMMEDIATE" in sql
    assert "90 PERCENT DO SUSPEND " in sql         # SUSPEND below the 100% hard stop


def test_alter_sql_rejects_out_of_range_suspend():
    from budget_sprint import _alter_sql
    with pytest.raises(ValueError):
        _alter_sql(100, 100)
    with pytest.raises(ValueError):
        _alter_sql(100, 0)
