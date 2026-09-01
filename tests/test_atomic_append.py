"""Atomic incremental append + never-shrink floor (offline, no warehouse).

The old append was a bare multi-chunk write_pandas(overwrite=False): a crash
mid-write left half the slice landed, the next run read MAX(cursor) off the
half-loaded table and advanced past the gap -- permanent silent data loss.
The fix stages into <TABLE>__STAGE_APPEND and lands with one INSERT..SELECT.

conftest.py puts library-onboarding on sys.path, so `import ingest` works offline.
"""
import sys
import types

import pandas as pd
import pytest

import ingest


class FakeSnow:
    """Records every SQL statement; scriptable failures + scalar answers."""

    def __init__(self, scalars=None, fail_on=None):
        self.calls = []
        self.scalars = list(scalars or [])
        self.fail_on = fail_on  # substring: execute() raises when SQL contains it

    def execute(self, conn, sql, params=None):
        self.calls.append(sql)
        if self.fail_on and self.fail_on in sql:
            raise RuntimeError(f"boom on: {self.fail_on}")

    def fetch_scalar(self, conn, sql, params=None):
        self.calls.append(sql)
        return self.scalars.pop(0) if self.scalars else None


def _install_write_pandas(monkeypatch, log, ok=True, fail=False):
    mod = types.ModuleType("snowflake.connector.pandas_tools")

    def write_pandas(conn, df, table_name=None, **kw):
        if fail:
            raise RuntimeError("write_pandas died mid-stage")
        log.append(("write_pandas", table_name, kw.get("overwrite"), len(df)))
        return ok, 1, len(df), None

    mod.write_pandas = write_pandas
    monkeypatch.setitem(sys.modules, "snowflake.connector.pandas_tools", mod)


DF = pd.DataFrame({"A": ["1", "2"], "B": ["x", "y"]})


def _patch_snow(monkeypatch, fake):
    monkeypatch.setattr(ingest.snow, "execute", fake.execute)
    monkeypatch.setattr(ingest.snow, "fetch_scalar", fake.fetch_scalar)


def test_append_stages_then_single_insert(monkeypatch):
    wp_log = []
    fake = FakeSnow(scalars=[1])  # target exists
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, wp_log)

    ingest._load_landing(None, DF, "T1", overwrite=False)

    # write_pandas hit the STAGE table only, as a full replace
    assert wp_log == [("write_pandas", "T1__STAGE_APPEND", True, 2)]
    inserts = [c for c in fake.calls if c.startswith("INSERT INTO")]
    assert len(inserts) == 1
    # named columns on BOTH sides -- physical order can't shift data
    assert '"T1" (A, B) SELECT A, B FROM' in inserts[0]
    assert "T1__STAGE_APPEND" in inserts[0]
    # stage dropped on success
    assert any("DROP TABLE IF EXISTS" in c and "STAGE_APPEND" in c for c in fake.calls)


def test_append_crash_leaves_target_untouched(monkeypatch):
    wp_log = []
    fake = FakeSnow(scalars=[1], fail_on="INSERT INTO")
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, wp_log)

    with pytest.raises(RuntimeError):
        ingest._load_landing(None, DF, "T1", overwrite=False)

    # the failed INSERT is the ONLY statement that ever named the live table
    target_hits = [c for c in fake.calls
                   if '"T1"' in c and "STAGE_APPEND" not in c.replace('"T1"', "", 1)]
    assert all(c.startswith("INSERT INTO") for c in target_hits)
    # stage still cleaned up on the way out
    assert any("DROP TABLE IF EXISTS" in c and "STAGE_APPEND" in c for c in fake.calls)


def test_append_stage_crash_never_touches_target(monkeypatch):
    fake = FakeSnow()
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, [], fail=True)

    with pytest.raises(RuntimeError):
        ingest._load_landing(None, DF, "T1", overwrite=False)

    assert not any(c.startswith("INSERT INTO") for c in fake.calls)


def test_first_incremental_run_renames_stage_in(monkeypatch):
    wp_log = []
    fake = FakeSnow(scalars=[0])  # target absent
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, wp_log)

    ingest._load_landing(None, DF, "T1", overwrite=False)

    assert any("RENAME TO" in c for c in fake.calls)
    assert not any(c.startswith("INSERT INTO") for c in fake.calls)


def test_snapshot_path_unchanged(monkeypatch):
    wp_log = []
    fake = FakeSnow()
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, wp_log)

    ingest._load_landing(None, DF, "T1", overwrite=True)

    assert wp_log == [("write_pandas", "T1", True, 2)]
    assert not any(c.startswith("INSERT INTO") for c in fake.calls)


# --- never-shrink floor -----------------------------------------------------

def test_shrink_refused_below_floor(monkeypatch):
    fake = FakeSnow(scalars=[167_000])
    _patch_snow(monkeypatch, fake)
    monkeypatch.setattr(ingest.settings, "allow_shrink", False)
    msg = ingest._shrink_refusal(None, "SAM_EXCLUSIONS", 1_000)
    assert msg and "SHRINK REFUSED" in msg


def test_shrink_allowed_at_or_above_floor(monkeypatch):
    monkeypatch.setattr(ingest.settings, "allow_shrink", False)
    fake = FakeSnow(scalars=[100])
    _patch_snow(monkeypatch, fake)
    assert ingest._shrink_refusal(None, "S", 100) is None


def test_shrink_no_prior_run_is_fine(monkeypatch):
    monkeypatch.setattr(ingest.settings, "allow_shrink", False)
    fake = FakeSnow(scalars=[None])
    _patch_snow(monkeypatch, fake)
    assert ingest._shrink_refusal(None, "S", 5) is None


def test_append_drop_failure_never_masks_the_load_error(monkeypatch):
    """Connection dies on INSERT; the cleanup DROP dies too. The INSERT error
    must surface, not the DROP's -- it becomes the 'failed' log message."""
    fake = FakeSnow(scalars=[1])
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, [])

    real_execute = fake.execute

    def dying_execute(conn, sql, params=None):
        if sql.startswith("INSERT INTO"):
            raise RuntimeError("the real load error")
        if sql.startswith("DROP TABLE"):
            raise RuntimeError("connection reset by peer")
        return real_execute(conn, sql, params)

    monkeypatch.setattr(ingest.snow, "execute", dying_execute)
    with pytest.raises(RuntimeError, match="the real load error"):
        ingest._load_landing(None, DF, "T1", overwrite=False)


def test_chunked_fresh_load_refuses_shrink_before_swap(monkeypatch):
    """A fresh chunked load below the floor must drop staging and raise --
    live table never swapped."""
    monkeypatch.setattr(ingest.settings, "allow_shrink", False)
    fake = FakeSnow(scalars=[1_000_000])  # floor from last successful run
    _patch_snow(monkeypatch, fake)
    _install_write_pandas(monkeypatch, [])

    with pytest.raises(RuntimeError, match="SHRINK REFUSED"):
        ingest._load_landing_chunked(
            None, iter([DF]), "T1", "run-1", ingest._utcnow(),
            resume_from_row=0, fresh=True, max_rows=0, source_id="S1",
        )

    assert not any("SWAP WITH" in c for c in fake.calls)
    assert any("DROP TABLE IF EXISTS" in c and "__STAGING" in c for c in fake.calls)


def test_shrink_override_flag(monkeypatch):
    monkeypatch.setattr(ingest.settings, "allow_shrink", True)
    fake = FakeSnow(scalars=[999_999])
    _patch_snow(monkeypatch, fake)
    assert ingest._shrink_refusal(None, "S", 1) is None
