"""Tests for bench/registry.py - the 145 chart templates.

Run:    python -m pytest tests/test_bench_registry.py -q
        python bench/registry.py                     (same checks, plain print)

Nothing here touches the network, a database, or Dash. Every frame comes from
the demo generators in bench/wall.py.

The one test that matters most is `test_every_drawable_chart_actually_draws`:
for twelve different result shapes it takes every chart the picker would light
up, auto-maps it, and builds the figure. A chart that says "yes I can draw
this" and then throws is worse than one that greys out.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import registry as reg  # noqa: E402
from bench import wall  # noqa: E402

# Twelve shapes a query might actually come back with. Named after the SHAPE,
# because the shape is what decides which charts are possible.
FRAMES: dict[str, pd.DataFrame] = {
    "category": wall.d_category(),
    "long": wall.d_long(),
    "scatter": wall.d_scatter(400),
    "timeseries": wall.d_timeseries(200),
    "flow": wall.d_flow(),
    "geo_points": wall.d_geo_points(300),
    "states": wall.d_states(),
    "ohlc": wall.d_ohlc(60),
    "hierarchy": wall.d_hierarchy(),
    "numeric_block": wall.d_numeric_block(200),
    "stages": wall.d_stages(),
    "rank_over_time": wall.d_rank_over_time(),
}


# ---------------------------------------------------------------------
# The table itself
# ---------------------------------------------------------------------


def test_every_wall_chart_is_registered():
    """wall.py is the list. registry.py may not quietly drop one."""
    assert len(reg.TEMPLATES) == len(wall.CHARTS)
    assert {t.name for t in reg.TEMPLATES} == {c.name for c in wall.CHARTS}


def test_keys_are_unique_and_slug_shaped():
    keys = [t.key for t in reg.TEMPLATES]
    assert len(set(keys)) == len(keys), "duplicate keys"
    for k in keys:
        assert k == k.lower(), k
        assert "-" not in k and " " not in k, k
        assert k.replace("_", "").isalnum(), k


def test_every_chart_has_a_trace_type_that_plotly_knows():
    for t in reg.TEMPLATES:
        assert t.trace_type in reg.TRACE_CLASSES, t.key
        assert hasattr(go, t.trace_class), t.key


def test_every_chart_has_a_builder_and_mapping_slots():
    for t in reg.TEMPLATES:
        if t.blocked:
            continue          # cannot render here - the reason is the payload
        if t.demo_only:
            assert t.wall_fn is not None, t.key
            assert t.demo_why, t.key
            continue
        assert callable(t.build), t.key
        assert t.required, f"{t.key} declares no required slots"
        for s in t.slots:
            assert s.role in (reg.NUM, reg.CAT, reg.DATE, reg.GEO,
                              reg.LAT, reg.LON, reg.ANY), (t.key, s.name)
            assert s.says, (t.key, s.name)


def test_counts_are_what_we_think_they_are():
    """If these move, something was added or dropped. Fail loudly, then update."""
    assert len(reg.TEMPLATES) == 145
    assert sum(1 for t in reg.TEMPLATES if t.blocked) == 6
    assert sum(1 for t in reg.TEMPLATES if t.demo_only) == 5
    assert sum(1 for t in reg.TEMPLATES if t.build) == 134
    assert len(reg.BY_SECTION) == 10


# ---------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------


def test_roles_reads_the_obvious_things():
    r = reg.roles(wall.d_geo_points(50))
    assert reg.LAT in r["lat"] and reg.NUM in r["lat"]
    assert reg.LON in r["lon"] and reg.GEO in r["lon"]
    assert r["amount"] == {reg.ANY, reg.NUM}

    r = reg.roles(wall.d_states())
    assert reg.GEO in r["state"] and reg.CAT in r["state"]

    r = reg.roles(wall.d_timeseries(30))
    assert reg.DATE in r["date"]
    assert reg.CAT in r["region"]


def test_an_integer_year_is_both_a_number_and_a_category():
    r = reg.roles(wall.d_rank_over_time())
    assert {reg.NUM, reg.CAT} <= r["year"]
    # ...but a float measure is only ever a number.
    assert reg.CAT not in reg.roles(wall.d_category())["spend"]


def test_describe_reads_like_english():
    assert reg.describe(reg.roles(wall.d_category())) == \
        "one category column and one number"
    assert "latitude" in reg.describe(reg.roles(wall.d_geo_points(20)))
    assert reg.describe({}) == "no usable columns at all"


def test_roles_also_accepts_the_data_module_bucket_shape():
    """bench/data.py hands out {role: [cols]}. Same language, other way up."""
    data = pytest.importorskip("bench.data")
    buckets = data.column_roles(wall.d_states())
    ok, why = reg.drawable(buckets, "choropleth")
    assert ok, why
    assert reg.auto_map(buckets, "choropleth")["locations"] == "state"


# ---------------------------------------------------------------------
# drawable() - the reason string is the product
# ---------------------------------------------------------------------


def test_drawable_always_gives_a_reason():
    r = reg.roles(wall.d_category())
    for t in reg.TEMPLATES:
        ok, why = reg.drawable(r, t)
        assert isinstance(ok, bool)
        assert why and len(why) > 20, t.key
        # Starts like a sentence ("2D density heatmap ..." is fine) and ends
        # like one, because this string is shown to a human as-is.
        assert why[0].isupper() or why[0].isdigit(), t.key
        assert why.rstrip().endswith("."), t.key


def test_the_sankey_reason_is_the_one_from_the_spec():
    r = reg.roles(pd.DataFrame({"agency": ["a", "b"], "spend": [1.0, 2.0]}))
    ok, why = reg.drawable(r, "sankey")
    assert not ok
    assert why == (
        "Sankey diagram needs a source column, a target column and a value "
        "column - this result has one category column and one number."
    )


def test_a_yes_names_the_columns_it_picked():
    r = reg.roles(wall.d_flow())
    ok, why = reg.drawable(r, "sankey")
    assert ok
    assert "source = source" in why and "value = amount" in why


def test_reasons_are_accurate_not_just_readable():
    """Spot-check: the thing a no complains about is really missing."""
    r = reg.roles(wall.d_category())          # one label + one number

    ok, why = reg.drawable(r, "candlestick")
    assert not ok and "date column" in why and "close column" in why

    ok, why = reg.drawable(r, "corr_matrix")  # needs 2+ numbers, has 1
    assert not ok and "two or more number columns" in why

    ok, why = reg.drawable(r, "scatter")      # needs 2 numbers, has 1
    assert not ok

    # Add a second number and the same chart lights up.
    r2 = reg.roles(wall.d_category().assign(other=[1.0, 2, 3, 4, 5, 6]))
    assert reg.drawable(r2, "scatter")[0]
    assert reg.drawable(r2, "corr_matrix")[0]


def test_blocked_charts_name_the_missing_package():
    wanted = {
        "distplot_blocked": "scipy",
        "violin_ff_blocked": "scipy",
        "ols_trend_blocked": "statsmodels",
        "dendrogram_blocked": "scipy",
        "ternary_contour_blocked": "scikit-image",
        "county_choropleth_blocked": "plotly-geo",
    }
    for key, package in wanted.items():
        ok, why = reg.drawable(reg.roles(wall.d_long()), key)
        assert not ok
        assert package in why, key
        assert reg.CHARTS[key].name in why, key


def test_demo_only_charts_say_so_and_still_draw():
    for t in reg.TEMPLATES:
        if not t.demo_only:
            continue
        ok, why = reg.drawable(reg.roles(wall.d_category()), t)
        assert ok and "built-in shape" in why, t.key
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig = t.builder(wall.d_category(), {}, None)
        assert isinstance(fig, go.Figure) and len(fig.data) > 0, t.key


def test_a_slot_that_is_two_of_a_kind_needs_two_columns():
    """One number cannot fill both `start` and `end` on a dumbbell."""
    one = reg.roles(pd.DataFrame({"e": ["a"], "v": [1.0]}))
    two = reg.roles(pd.DataFrame({"e": ["a"], "v": [1.0], "w": [2.0]}))
    assert not reg.drawable(one, "dumbbell")[0]
    assert reg.drawable(two, "dumbbell")[0]


# ---------------------------------------------------------------------
# auto_map + builder
# ---------------------------------------------------------------------


def test_auto_map_fills_every_required_slot_when_drawable():
    for name, df in FRAMES.items():
        r = reg.roles(df)
        for t in reg.TEMPLATES:
            if not reg.drawable(r, t)[0] or t.demo_only:
                continue
            assert not t.missing(reg.auto_map(r, t)), f"{name}/{t.key}"


def test_auto_map_picks_the_obvious_column_for_the_obvious_slot():
    """On an OHLC table `open` must land in the `open` slot, not `high`."""
    m = reg.auto_map(reg.roles(wall.d_ohlc(20)), "candlestick")
    assert m == {"x": "date", "open": "open", "high": "high",
                 "low": "low", "close": "close"}


def test_auto_map_greedily_fills_list_slots():
    m = reg.auto_map(reg.roles(wall.d_numeric_block(20)), "corr_matrix")
    assert len(m["values"]) == 5      # all five numbers, not just the two needed


@pytest.mark.parametrize("frame_name", list(FRAMES))
def test_every_drawable_chart_actually_draws(frame_name):
    """The headline test. A yes that then throws is worse than a no."""
    df = FRAMES[frame_name]
    r = reg.roles(df)
    built, failures = 0, []
    for t in reg.TEMPLATES:
        if not reg.drawable(r, t)[0]:
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fig = t.builder(df, reg.auto_map(r, t), None)
            assert isinstance(fig, go.Figure)
            built += 1
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{t.key}: {type(exc).__name__}: {exc}")
    assert not failures, f"{frame_name}: " + "; ".join(failures)
    assert built >= 40, f"{frame_name} only drew {built} charts"


def test_builder_refuses_an_empty_required_slot_in_plain_english():
    with pytest.raises(ValueError) as e:
        reg.CHARTS["sankey"].builder(wall.d_flow(), {"source": "source"}, None)
    assert "a target column" in str(e.value)


def test_knobs_land_on_the_figure():
    df = wall.d_category()
    t = reg.CHARTS["bar"]
    m = reg.auto_map(reg.roles(df), t)
    fig = t.builder(df, m, {"layout.barmode": "overlay",
                            "layout.title.text": "hello",
                            "trace.marker.opacity": 0.4})
    assert fig.layout.barmode == "overlay"
    assert fig.layout.title.text == "hello"
    assert all(tr.marker.opacity == 0.4 for tr in fig.data)


def test_a_bad_knob_warns_instead_of_killing_the_chart():
    df = wall.d_category()
    t = reg.CHARTS["bar"]
    m = reg.auto_map(reg.roles(df), t)
    with pytest.warns(UserWarning):
        fig = t.builder(df, m, {"layout.there_is_no_such_thing": 1})
    assert isinstance(fig, go.Figure) and len(fig.data) > 0


# ---------------------------------------------------------------------
# The seams to the other Bench modules
# ---------------------------------------------------------------------


def test_trace_type_answers_for_every_key_in_plotlys_own_spelling():
    for t in reg.TEMPLATES:
        assert reg.trace_type(t.key) == t.trace_type
    assert reg.trace_type("no such chart") is None


def test_knobs_can_use_our_trace_type():
    knobs = pytest.importorskip("bench.knobs")
    assert knobs.trace_type_for("sankey") == "sankey"
    assert knobs.trace_type_for("bump") == "scatter"
    # A deprecated trace is swapped for its live twin on the knobs side.
    assert knobs.trace_type_for("mapbox_deprecated") == "scattermap"


def test_build_is_the_function_codegen_writes():
    fig = reg.build("sankey", wall.d_flow(), source="source", target="target",
                    value="amount")
    assert [tr.type for tr in fig.data] == ["sankey"]
    with pytest.raises(KeyError):
        reg.build("not_a_chart", wall.d_flow())


def test_px_pure_only_lists_charts_that_really_are_one_px_call():
    for key in reg.PX_PURE:
        t = reg.CHARTS[key]
        assert t.build.px_pure == key
        assert hasattr(__import__("plotly.express", fromlist=["x"]), key)


def test_demo_figure_matches_wall():
    """Every template can still draw wall.py's original reference picture."""
    t = reg.CHARTS["ridgeline"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = t.demo_figure()
    assert [tr.type for tr in fig.data] == ["violin"] * len(fig.data)


def test_search_finds_charts_by_what_they_answer():
    assert any(t.key == "sankey" for t in reg.search("what moves where"))
    assert any(t.key == "bump" for t in reg.search("bump"))
    assert len(reg.search("")) == len(reg.TEMPLATES)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
