"""Guard on how loaders stringify values for all-VARCHAR landing tables.

THE BUG (2026-08-11): every bulk loader did `None if v is None else str(v)`.
pandas turns a JSON null into float NaN, not None, so that check missed it and
`str(NaN)` wrote the literal text 'nan' into the warehouse. FDIC's LEI column --
a real cross-dataset join key -- came back 6,260 "populated", of which 4,008
were the string 'nan'. A key column full of 'nan' is worse than an empty one,
because 'nan' happily joins to 'nan'.

This is the third time sentinel-masked blanks have fooled this platform, so the
coercion now has its own tests.
"""
import importlib.util
import os

import pandas as pd
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOADERS = [
    "fdic_institutions_load.py",
    "fdic_sod_load.py",
    "fema_ia_load.py",
    "nih_reporter_load.py",
    "treasury_dts_deposits_load.py",
]


def _as_text_of(fname):
    """Pull just the coercion helper out of a loader without importing the
    module (importing would try to open a warehouse connection)."""
    src = open(os.path.join(REPO, "scripts", fname), encoding="utf-8").read()
    start = src.index("def _as_text(")
    end = src.index("\n\n\n", start) if "\n\n\n" in src[start:] else len(src)
    ns = {"pd": pd}
    exec(compile(src[start:end], fname, "exec"), ns)
    return ns["_as_text"]


@pytest.mark.parametrize("fname", LOADERS)
def test_every_loader_has_the_helper(fname):
    src = open(os.path.join(REPO, "scripts", fname), encoding="utf-8").read()
    assert "def _as_text(" in src
    # The old, broken coercion must be gone AS CODE. Match the whole call, not
    # the bare lambda body -- the helper's docstring quotes that body to explain
    # what went wrong, and matching the fragment flags the explanation itself.
    assert "apply(lambda v: None if v is None else str(v))" not in src
    assert "df[c] = df[c].apply(_as_text)" in src


@pytest.mark.parametrize("fname", LOADERS)
def test_missing_values_never_become_the_text_nan(fname):
    as_text = _as_text_of(fname)
    for missing in (None, float("nan"), pd.NA, pd.NaT):
        assert as_text(missing) is None, f"{missing!r} -> {as_text(missing)!r}"


@pytest.mark.parametrize("fname", LOADERS)
def test_blank_and_whitespace_become_null(fname):
    as_text = _as_text_of(fname)
    assert as_text("") is None
    assert as_text("   ") is None


@pytest.mark.parametrize("fname", LOADERS)
def test_real_values_survive_unchanged(fname):
    as_text = _as_text_of(fname)
    assert as_text("549300XYZ") == "549300XYZ"
    assert as_text(0) == "0"          # zero is a value, not a blank
    assert as_text(False) == "False"
    assert as_text(12.5) == "12.5"
    # the STRING "nan" from a real source is data, and must not be destroyed
    assert as_text("nan") == "nan"


@pytest.mark.parametrize("fname", LOADERS)
def test_a_dataframe_column_of_nulls_lands_as_nulls(fname):
    """The end-to-end shape of the bug: a column pandas has coerced to NaN."""
    as_text = _as_text_of(fname)
    df = pd.DataFrame({"lei": ["549300XYZ", None, None]})
    out = df["lei"].apply(as_text).tolist()
    assert out == ["549300XYZ", None, None]
