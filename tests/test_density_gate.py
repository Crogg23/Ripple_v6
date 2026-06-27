"""Offline tests for the load-time DENSITY gate (P0-1). Pure Python, no Snowflake.

The gate is the systemic trust fix: FED_FJC_IDB landed 4.1M rows, logged
STATUS='success', and rode into the catalog as a 'modeled' mart -- while being 100%
EMPTY across every column (a parse failure). These tests pin the behaviour that
demotes that case to STATUS='empty' WITHOUT false-demoting a real-but-sparse table.

conftest.py puts library-onboarding on sys.path, so `import ingest` works offline.
"""

import pandas as pd
import pytest

from ingest import (
    DENSITY_MIN_POPULATED_FRACTION,
    _META_COLS,
    assess_density,
)


# ---------------------------------------------------------------------------
# Healthy frame -- must PASS (keeps STATUS='success')
# ---------------------------------------------------------------------------
def test_healthy_frame_passes():
    df = pd.DataFrame({
        "FIPS": ["06037", "36061", "17031"],
        "NAME": ["Los Angeles", "New York", "Cook"],
        "POPULATION": ["10039107", "1628706", "5275541"],
    })
    d = assess_density(df)
    assert d["empty"] is False
    assert d["reason"] == ""
    assert d["populated_fraction"] == 1.0
    assert d["all_blank_cols"] == 0
    assert d["source_cols"] == 3


# ---------------------------------------------------------------------------
# FJC_IDB shape -- a WIDE frame where every column is all-empty -> DEMOTED
# ---------------------------------------------------------------------------
def test_all_empty_wide_frame_is_demoted():
    # 40 columns, 500 rows, every cell an empty string (the FED_FJC_IDB failure).
    cols = {f"COL_{i}": [""] * 500 for i in range(40)}
    df = pd.DataFrame(cols)
    d = assess_density(df)
    assert d["empty"] is True
    assert d["populated_fraction"] == 0.0
    assert d["all_blank_cols"] == 40
    assert d["source_cols"] == 40
    assert d["single_distinct_blank"] is True
    assert d["reason"]  # non-empty explanation


def test_whitespace_only_wide_frame_is_demoted():
    # Whitespace that strips to empty must also count as blank (not a stray value).
    cols = {f"COL_{i}": ["   ", "\t", "\n", " "] for i in range(30)}
    df = pd.DataFrame(cols)
    d = assess_density(df)
    assert d["empty"] is True
    assert d["all_blank_cols"] == 30


def test_one_stray_cell_still_demotes_via_floor():
    # ~every column blank but ONE cell populated -> populated_fraction is tiny
    # (1/50_000 << 1%), so the FLOOR demotes it. This is the FJC_IDB "a stray cell
    # nudged us off exactly 0%" case -- still caught.
    cols = {f"COL_{i}": [""] * 1000 for i in range(50)}
    cols["COL_0"][0] = "x"  # 1 real cell out of 50_000
    df = pd.DataFrame(cols)
    d = assess_density(df)
    frac = 1 / 50_000
    assert frac < DENSITY_MIN_POPULATED_FRACTION   # below the 1% floor
    assert d["all_blank_cols"] == 49               # 49/50 columns entirely blank
    assert d["empty"] is True
    assert "floor" in d["reason"]


# ---------------------------------------------------------------------------
# All-NULL frame -> DEMOTED
# ---------------------------------------------------------------------------
def test_all_null_frame_is_demoted():
    df = pd.DataFrame({
        "A": [None, None, None, None],
        "B": [None, None, None, None],
        "C": [None, None, None, None],
    })
    d = assess_density(df)
    assert d["empty"] is True
    assert d["populated_fraction"] == 0.0
    assert d["all_blank_cols"] == 3


def test_nan_frame_is_demoted():
    # Numeric NaN (not None) must also read as blank.
    df = pd.DataFrame({"X": [float("nan")] * 10, "Y": [float("nan")] * 10})
    d = assess_density(df)
    assert d["empty"] is True
    assert d["populated_fraction"] == 0.0


# ---------------------------------------------------------------------------
# The critical guard: a REAL-but-SPARSE table must NOT be false-demoted
# ---------------------------------------------------------------------------
def test_sparse_but_real_frame_passes():
    # A wide table: a couple of always-populated KEY columns + 18 mostly-empty
    # optional columns. This is a legitimate real table -- it must PASS.
    rows = 1000
    data = {
        "EIN": [f"{10_000_000 + i:08d}" for i in range(rows)],  # always populated
        "NAME": [f"Org {i}" for i in range(rows)],              # always populated
    }
    # 18 optional columns, each populated on only ~5% of rows (the rest blank).
    for c in range(18):
        col = [""] * rows
        for i in range(0, rows, 20):  # 5% populated
            col[i] = f"val_{c}_{i}"
        data[f"OPT_{c}"] = col
    df = pd.DataFrame(data)
    d = assess_density(df)
    # 2 of 20 columns always full => >= 10% density, far above the 1% floor.
    assert d["populated_fraction"] >= 0.10
    assert d["empty"] is False, "a real-but-sparse table must not be demoted"
    assert d["all_blank_cols"] == 0


def test_two_full_key_columns_in_a_200_col_frame_passes():
    # The worst legitimate case the floor must clear: a 200-column frame where ONLY
    # 2 key columns are ever populated. 2/200 = 1.0% == exactly the floor -> passes.
    rows = 200
    data = {"FIPS": ["06037"] * rows, "GEOID": ["06037"] * rows}
    for c in range(198):
        data[f"M_{c}"] = [""] * rows
    df = pd.DataFrame(data)
    d = assess_density(df)
    assert d["source_cols"] == 200
    assert abs(d["populated_fraction"] - 0.01) < 1e-9
    assert d["empty"] is False  # >= the floor, not below it


# ---------------------------------------------------------------------------
# Meta/provenance columns must be ignored (they'd otherwise mask an empty source)
# ---------------------------------------------------------------------------
def test_meta_columns_do_not_rescue_an_empty_source():
    import datetime as dt
    df = pd.DataFrame({
        "COL_0": [""] * 100,
        "COL_1": [""] * 100,
        "COL_2": [""] * 100,
        "_INGESTED_AT": [dt.datetime(2026, 6, 27)] * 100,
        "_SOURCE_RUN_ID": ["run-123"] * 100,
        "_SRC_SHA256": ["abc"] * 100,
    })
    # Sanity: those three names really are the meta set.
    assert {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"} == set(_META_COLS)
    d = assess_density(df)
    assert d["source_cols"] == 3            # meta columns excluded from the count
    assert d["empty"] is True              # source columns are all blank -> demoted
    assert d["populated_fraction"] == 0.0


def test_meta_columns_excluded_from_a_healthy_frame_too():
    import datetime as dt
    df = pd.DataFrame({
        "FIPS": ["06037", "36061"],
        "VAL": ["1", "2"],
        "_INGESTED_AT": [dt.datetime(2026, 6, 27)] * 2,
        "_SOURCE_RUN_ID": ["r"] * 2,
        "_SRC_SHA256": ["s"] * 2,
    })
    d = assess_density(df)
    assert d["source_cols"] == 2
    assert d["empty"] is False
    assert d["populated_fraction"] == 1.0


# ---------------------------------------------------------------------------
# Degenerate shapes
# ---------------------------------------------------------------------------
def test_zero_row_frame_is_empty():
    df = pd.DataFrame(columns=["A", "B"])
    d = assess_density(df)
    assert d["empty"] is True
    assert d["rows_sampled"] == 0


def test_no_source_columns_is_empty():
    # Only meta columns -> no real source columns at all.
    df = pd.DataFrame({"_SOURCE_RUN_ID": ["r"], "_SRC_SHA256": ["s"]})
    d = assess_density(df)
    assert d["source_cols"] == 0
    assert d["empty"] is True


def test_single_real_column_is_not_structurally_demoted():
    # A legit narrow 1-column frame with real values must pass (the structural
    # all-blank signal requires >= 2 columns precisely so this can't trip it).
    df = pd.DataFrame({"VESSEL_IMO": [f"IMO{i}" for i in range(50)]})
    d = assess_density(df)
    assert d["source_cols"] == 1
    assert d["empty"] is False
    assert d["populated_fraction"] == 1.0


# ---------------------------------------------------------------------------
# Sampling cap -- the gate stays cheap on a huge frame and reads it correctly
# ---------------------------------------------------------------------------
def test_sampling_caps_rows_scanned():
    big = pd.DataFrame({"A": ["x"] * 100_000, "B": ["y"] * 100_000})
    d = assess_density(big)            # default sample cap is 2000
    assert d["rows_sampled"] == 2000
    assert d["empty"] is False
    assert d["populated_fraction"] == 1.0


def test_sampling_cap_catches_uniform_empty_in_a_huge_frame():
    big = pd.DataFrame({f"C{i}": [""] * 100_000 for i in range(20)})
    d = assess_density(big)
    assert d["rows_sampled"] == 2000
    assert d["empty"] is True
