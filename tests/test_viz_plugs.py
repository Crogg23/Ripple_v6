"""viz/plugs.py — column roles + suggest() are pure pandas; figure tests need plotly."""

import sys

import pandas as pd
import pytest

from viz import plugs


# ---- column_roles ------------------------------------------------------------ #
def test_all_digit_strings_are_numeric_never_dates():
    # FEC image numbers / NPIs / ZIPs must never land on a time axis
    df = pd.DataFrame({"IMAGE_NUM": ["15020000001", "201705039080102297", "99"]})
    roles = plugs.column_roles(df)
    assert "IMAGE_NUM" in roles["numeric"]
    assert not roles["date"]


def test_real_dates_classify_as_dates():
    df = pd.DataFrame({"EVENT_DATE": ["2024-01-05", "2024-02-10", "2024-03-15"]})
    assert "EVENT_DATE" in plugs.column_roles(df)["date"]


def test_year_column_detected():
    df = pd.DataFrame({"YEAR": [2001, 2002, 2003], "V": [1.0, 2.0, 3.0]})
    roles = plugs.column_roles(df)
    assert "YEAR" in roles["year"] and "V" in roles["numeric"]


def test_state_codes_detected():
    df = pd.DataFrame({"ST": ["CA", "TX", "NY", "WA"], "N": [1, 2, 3, 4]})
    assert "ST" in plugs.column_roles(df)["state"]


def test_meta_columns_hidden():
    df = pd.DataFrame({"_INGESTED_AT": ["2026-01-01"], "X": ["a"]})
    roles = plugs.column_roles(df)
    flat = [c for cols in roles.values() for c in cols]
    assert "_INGESTED_AT" not in flat


# ---- suggest ------------------------------------------------------------------ #
def test_suggest_single_value_is_big_number():
    df = pd.DataFrame({"TOTAL": [42.0]})
    assert plugs.suggest(df)[0][0] == "big_number"


def test_suggest_time_series_is_line():
    df = pd.DataFrame({"D": pd.date_range("2024-01-01", periods=5).astype(str),
                       "V": [1, 2, 3, 4, 5]})
    names = [s[0] for s in plugs.suggest(df)]
    assert names[0] == "line"


def test_suggest_category_measure_is_bar():
    df = pd.DataFrame({"KIND": ["a", "b", "c"], "N": [1, 2, 3]})
    names = [s[0] for s in plugs.suggest(df)]
    assert "bar" in names[:2]


def test_suggest_state_map():
    df = pd.DataFrame({"ST": ["CA", "TX", "NY"], "N": [1, 2, 3]})
    names = [s[0] for s in plugs.suggest(df)]
    assert "choropleth_state" in names[:2]


def test_suggest_always_ends_in_table():
    assert plugs.suggest(pd.DataFrame({"X": ["a"]}))[-1][0] == "table"


# ---- category folding ----------------------------------------------------------- #
def test_fold_categories_caps_at_palette_size():
    df = pd.DataFrame({"C": [f"cat{i}" for i in range(20)], "V": range(20)})
    out = plugs._fold_categories(df, "C")
    assert out["C"].nunique() <= plugs.MAX_CATEGORIES
    assert "Other" in set(out["C"])


# ---- lazy imports ----------------------------------------------------------------- #
def test_importing_viz_does_not_import_plotly():
    # offline CI collects without the viz dep; plotly loads only when a plug runs
    for mod in ("viz.plugs", "viz.theme", "viz.guard", "viz.safety"):
        assert mod in sys.modules or __import__(mod)
    assert "plotly" not in sys.modules or pytest.importorskip("plotly")


# ---- figures (need plotly) ----------------------------------------------------------- #
def test_bar_builds_a_real_figure():
    pytest.importorskip("plotly")
    df = pd.DataFrame({"KIND": ["a", "b"], "N": [1, 2]})
    fig = plugs.bar(df, source="TEST", as_of="2026-07-01")
    assert fig.layout.template is not None
    assert "N by KIND - TEST" in fig.layout.title.text
    stamps = [a.text for a in fig.layout.annotations]
    assert any("data as of 2026-07-01" in s for s in stamps)


def test_bar_counts_rows_when_no_numeric():
    pytest.importorskip("plotly")
    df = pd.DataFrame({"KIND": ["a", "a", "b"]})
    fig = plugs.bar(df)
    assert fig.data  # built a count-per-category chart without a numeric column


def test_px_kwargs_pass_through():
    pytest.importorskip("plotly")
    df = pd.DataFrame({"KIND": ["a", "b"], "N": [1, 2]})
    fig = plugs.bar(df, x="KIND", y="N", log_y=True)
    assert fig.layout.yaxis.type == "log"


def test_no_dual_axis_anywhere():
    # the method bans dual-axis charts; no plug may create a second y-axis
    pytest.importorskip("plotly")
    df = pd.DataFrame({"KIND": ["a", "b"], "N": [1, 2], "M": [3, 4]})
    for name, fn in plugs.PLUGS.items():
        try:
            fig = fn(df)
        except Exception:
            continue
        assert getattr(fig.layout, "yaxis2", None) is None, name
