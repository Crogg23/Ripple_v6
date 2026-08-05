"""Tests for bench/knobs.py - the Plotly introspection generator.

Run:    python -m pytest tests/test_bench_knobs.py -q
        python tests/test_bench_knobs.py          (same checks, plain print)

Nothing here touches the network, a database, or Dash. It is all
introspection over the plotly package installed on this machine.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import knobs  # noqa: E402

# The 21 trace types this module is checked against. Spread across all ten
# ATLAS questions, and both extremes of size.
TRACES = knobs.SELFTEST_TRACES

COLUMNS = ["agency", "region", "spend", "date"]


# ---------------------------------------------------------------------
# The walk itself
# ---------------------------------------------------------------------


@pytest.mark.parametrize("trace", TRACES)
def test_tree_builds_for_every_trace_type(trace):
    """Every trace type produces a tree with all six buckets and all three tiers."""
    built = knobs.tree(trace, COLUMNS)
    assert set(built) == set(knobs.BUCKETS)
    for bucket in knobs.BUCKETS:
        assert set(built[bucket]) == set(knobs.TIERS)
    total = sum(len(built[b][t]) for b in knobs.BUCKETS for t in knobs.TIERS)
    assert total > 1500, f"{trace} produced only {total} knobs"


@pytest.mark.parametrize("trace", TRACES)
def test_every_path_lands_in_exactly_one_bucket_and_tier(trace):
    """No knob is filed twice, and no path collides."""
    flat = knobs.flat(trace, COLUMNS)
    paths = [k.path for k in flat]
    assert len(paths) == len(set(paths)), f"{trace} has duplicate paths"


@pytest.mark.parametrize("trace", TRACES)
def test_no_skipped_validators_survive(trace):
    """src / literal / subplotid never reach the panel. SPEC 4.1."""
    for knob in knobs.flat(trace, COLUMNS):
        assert knob.validator not in knobs.SKIP_VALIDATORS
        assert not knob.path.endswith("src"), knob.path


@pytest.mark.parametrize("trace", TRACES)
def test_paths_are_prefixed_and_within_depth_cap(trace):
    """Paths start layout. or trace. and go no deeper than the cap. SPEC 3."""
    for knob in knobs.flat(trace, COLUMNS):
        assert knob.path.startswith(("layout.", "trace.")), knob.path
        assert 1 <= knob.depth <= knobs.MAX_DEPTH, knob.path


@pytest.mark.parametrize("trace", TRACES)
def test_every_knob_has_a_real_control(trace):
    """Every knob names a control the UI knows how to draw."""
    legal = set(knobs.CONTROL_BY_VALIDATOR.values()) | {"slider", "column"}
    for knob in knobs.flat(trace, COLUMNS):
        assert knob.control in legal, f"{knob.path} -> {knob.control}"


# ---------------------------------------------------------------------
# Buckets
# ---------------------------------------------------------------------


def test_data_bucket_gets_the_dataframe_columns():
    """DATA is the one bucket whose legal values come from the data. SPEC 3."""
    built = knobs.tree("bar", COLUMNS)
    data_knobs = [k for t in knobs.TIERS for k in built[knobs.DATA][t]]
    assert data_knobs
    for knob in data_knobs:
        assert knob.control == "column"
        assert knob.options == tuple(COLUMNS)


def test_data_bucket_holds_only_bindable_things():
    """Across all 49 registered trace types, nothing in DATA is a container.

    Checked against every trace Plotly registers, not just the 21 in TRACES,
    because a container wearing a "column" dropdown would be nonsense UI.
    """
    offenders = set()
    for trace in sorted(knobs.TRACE_CLASS_NAMES):
        for knob in knobs.flat(trace, COLUMNS):
            if knob.bucket == knobs.DATA and knob.control in ("section", "list"):
                offenders.add(knob.path)
    assert not offenders, sorted(offenders)


def test_data_bucket_follows_the_columns_it_is_given():
    a = knobs.tree("bar", ["ONE"])
    b = knobs.tree("bar", ["TWO", "THREE"])
    assert a[knobs.DATA][0][0].options == ("ONE",)
    assert b[knobs.DATA][0][0].options == ("TWO", "THREE")


def test_nested_data_arrays_reach_the_data_bucket():
    """Sankey and table hide their data one level down. SPEC 4.2, rule 3."""
    sankey = {k.path for k in knobs.flat("sankey", COLUMNS) if k.bucket == knobs.DATA}
    for path in ("trace.link.source", "trace.link.target", "trace.link.value", "trace.node.label"):
        assert path in sankey, f"sankey missing {path} from DATA"

    table = {k.path for k in knobs.flat("table", COLUMNS) if k.bucket == knobs.DATA}
    for path in ("trace.header.values", "trace.cells.values"):
        assert path in table, f"table missing {path} from DATA"


def test_marker_stays_in_mark_even_when_it_is_a_data_array():
    """trace.marker.* is claimed by MARK before the DataArray rule fires."""
    pie = {k.path: k.bucket for k in knobs.flat("pie", COLUMNS)}
    assert pie["trace.marker.colors"] == knobs.MARK


def test_text_is_data_but_textposition_is_mark():
    """The exact-path rules have to beat the prefix rules. SPEC 4.2."""
    bar = {k.path: k.bucket for k in knobs.flat("bar", COLUMNS)}
    assert bar["trace.text"] == knobs.DATA
    assert bar["trace.textposition"] == knobs.MARK
    assert bar["trace.orientation"] == knobs.MARK
    assert bar["trace.opacity"] == knobs.MARK


def test_layout_buckets_land_where_the_spec_says():
    bar = {k.path: k.bucket for k in knobs.flat("bar", COLUMNS)}
    assert bar["layout.xaxis.categoryorder"] == knobs.SCALE
    assert bar["layout.coloraxis.colorbar.title.text"] == knobs.SCALE
    assert bar["layout.colorway"] == knobs.SCALE
    assert bar["layout.geo.projection.type"] == knobs.SCALE
    assert bar["layout.title.text"] == knobs.FRAME
    assert bar["layout.legend.orientation"] == knobs.FRAME
    assert bar["layout.margin.l"] == knobs.FRAME
    assert bar["layout.template"] == knobs.FRAME
    assert bar["layout.hovermode"] == knobs.INTERACTION
    assert bar["layout.dragmode"] == knobs.INTERACTION
    assert bar["layout.modebar.orientation"] == knobs.INTERACTION
    assert bar["layout.transition.duration"] == knobs.MOTION


def test_unmatched_paths_are_recorded_not_swallowed():
    """SPEC 4.2: anything unmatched falls to FRAME and is logged."""
    knobs.tree("bar", COLUMNS)
    gaps = knobs.unmatched()
    assert isinstance(gaps, tuple)
    # These are real holes in the SPEC 4.2 table on this install. If the
    # table grows to cover them, update this list - do not delete the test.
    assert "layout.barmode" in gaps
    bar = {k.path: k.bucket for k in knobs.flat("bar", COLUMNS)}
    for path in gaps:
        if path in bar:
            assert bar[path] == knobs.FRAME


# ---------------------------------------------------------------------
# Tiers and descriptions
# ---------------------------------------------------------------------


def test_tier0_is_the_atlas_twenty_plus_this_chart_s_data():
    """SPEC 4.3. All 30 ATLAS paths show up, and every DATA knob is Tier 0."""
    built = knobs.tree("bar", COLUMNS)
    tier0 = {k.path for b in knobs.BUCKETS for k in built[b][0]}
    missing = set(knobs.TIER0) - tier0
    assert not missing, f"ATLAS Tier 0 paths missing from the tree: {sorted(missing)}"
    data_paths = {k.path for t in knobs.TIERS for k in built[knobs.DATA][t]}
    assert data_paths <= tier0


def test_tier0_descriptions_come_from_atlas_word_for_word():
    """SPEC 4.4 rule 1: hand-written half-sentences, not Plotly's prose."""
    built = knobs.tree("bar", COLUMNS)
    by_path = {k.path: k for b in knobs.BUCKETS for k in built[b][0]}
    assert by_path["layout.hovermode"].description == knobs.TIER0["layout.hovermode"][1]
    assert "usability win" in by_path["layout.hovermode"].description
    assert "property is an enumeration" not in by_path["layout.hovermode"].description


def test_tier0_renders_in_atlas_order():
    built = knobs.tree("bar", COLUMNS)
    frame0 = [k.path for k in built[knobs.FRAME][0]]
    ranks = [knobs.TIER0[p][0] for p in frame0 if p in knobs.TIER0]
    assert ranks == sorted(ranks)


def test_tier1_is_shallow_and_tier2_is_deep():
    built = knobs.tree("bar", COLUMNS)
    for bucket in knobs.BUCKETS:
        assert all(k.depth <= 2 for k in built[bucket][1])
        assert all(k.depth >= 3 for k in built[bucket][2])


def test_descriptions_are_cleaned_and_capped():
    """SPEC 4.4 rule 2: strip the boilerplate, cap at ~160 chars."""
    for knob in knobs.flat("scatter", COLUMNS):
        assert len(knob.description) <= 165, f"{knob.path}: {len(knob.description)}"
        assert not knob.description.startswith("The '")


def test_clean_description_strips_the_prefix():
    raw = "    The 'hovermode' property is an enumeration that may be\n    specified as: x"
    assert knobs.clean_description(raw) == "is an enumeration that may be specified as: x"
    assert knobs.clean_description("") == ""
    assert knobs.clean_description(None) == ""


def test_no_description_is_never_invented():
    """A knob with nothing usable shows an empty string, not made-up text."""
    assert knobs.clean_description("   ") == ""


# ---------------------------------------------------------------------
# Controls, options and bounds
# ---------------------------------------------------------------------


def test_enum_becomes_a_dropdown_with_real_options():
    bar = {k.path: k for k in knobs.flat("bar", COLUMNS)}
    orient = bar["trace.orientation"]
    assert orient.control == "dropdown"
    assert orient.options == ("v", "h")

    order = bar["layout.xaxis.categoryorder"]
    assert order.control == "dropdown"
    # ATLAS 4.1 says 18 values. Check the count against Plotly, not memory.
    assert len(order.options) == 18
    assert "total descending" in order.options


def test_bool_option_survives_the_enum_cleaning():
    """layout.hovermode legitimately accepts False."""
    bar = {k.path: k for k in knobs.flat("bar", COLUMNS)}
    assert False in bar["layout.hovermode"].options


def test_numeric_twins_and_regexes_are_dropped_from_options():
    scat = {k.path: k for k in knobs.flat("scatter", COLUMNS)}
    symbols = scat["trace.marker.symbol"].options
    assert "circle" in symbols
    assert 0 not in symbols and "0" not in symbols
    dashes = scat["trace.line.dash"].options
    assert "solid" in dashes
    assert not any(str(d).startswith("/") for d in dashes)


def test_slider_only_when_both_bounds_are_real():
    bar = {k.path: k for k in knobs.flat("bar", COLUMNS)}
    op = bar["trace.opacity"]
    assert op.control == "slider" and op.min == 0 and op.max == 1
    # layout.width is [10, inf] - a half-open range is a number box.
    width = bar["layout.width"]
    assert width.control == "number"
    assert width.min == 10 and width.max is None


def test_boolean_color_and_flaglist_controls():
    bar = {k.path: k for k in knobs.flat("bar", COLUMNS)}
    assert bar["layout.showlegend"].control == "toggle"
    assert bar["layout.paper_bgcolor"].control == "color"
    hoverinfo = bar["trace.hoverinfo"]
    assert hoverinfo.control == "multiselect"
    assert set(hoverinfo.options) >= {"x", "y", "all", "none", "skip"}


def test_template_and_colorscale_options_come_from_this_install():
    import plotly.colors as pcolors
    import plotly.io as pio

    bar = {k.path: k for k in knobs.flat("bar", COLUMNS)}
    template = bar["layout.template"]
    assert template.control == "dropdown"
    assert set(template.options) == set(str(t) for t in pio.templates)
    scale = bar["trace.marker.colorscale"]
    assert scale.control == "colorscale"
    assert len(scale.options) == len(pcolors.named_colorscales())


def test_compound_becomes_a_section_and_arrays_become_lists():
    bar = {k.path: k for k in knobs.flat("bar", COLUMNS)}
    assert bar["trace.marker"].control == "section"
    assert bar["layout.title"].control == "section"
    assert bar["layout.annotations"].control == "list"
    assert bar["layout.shapes"].control == "list"


# ---------------------------------------------------------------------
# default() and validate()
# ---------------------------------------------------------------------


def test_default_is_none_because_plotly_defaults_live_in_javascript():
    assert knobs.default("layout.hovermode") is None
    assert knobs.default("layout.margin.l") is None
    assert knobs.default("trace.opacity", "bar") is None
    # A compound container is not a value.
    assert knobs.default("layout.title") is None


def test_list_valued_defaults_are_empty_lists_not_none():
    """The one honest exception: an untouched list reads as empty, not unset."""
    assert knobs.default("layout.shapes") == []
    assert knobs.default("layout.annotations") == []
    built = knobs.tree("bar", COLUMNS)
    by_path = {k.path: k for b in knobs.BUCKETS for k in built[b][0]}
    assert by_path["layout.shapes"].default == []
    assert by_path["layout.title.text"].default is None


def test_tree_defaults_match_the_default_function():
    """The cached walk and the from-the-root lookup must agree."""
    for knob in knobs.flat("bar", COLUMNS)[:400]:
        assert knob.default == knobs.default(knob.path, "bar"), knob.path


def test_default_on_a_nonsense_path_returns_none_and_does_not_raise():
    assert knobs.default("layout.no_such_thing") is None
    assert knobs.default("banana") is None
    assert knobs.default("trace.opacity") is None  # no chart_key given


def test_validate_accepts_good_values():
    ok, val = knobs.validate("trace.orientation", "h", "bar")
    assert ok and val == "h"
    ok, val = knobs.validate("layout.hovermode", "x unified")
    assert ok and val == "x unified"
    ok, val = knobs.validate("layout.showlegend", False)
    assert ok and val is False


def test_validate_rejects_bad_values_without_raising():
    ok, msg = knobs.validate("trace.orientation", "sideways", "bar")
    assert not ok and isinstance(msg, str) and msg
    ok, msg = knobs.validate("trace.opacity", 5, "bar")
    assert not ok
    ok, msg = knobs.validate("layout.no_such_knob", 1)
    assert not ok


def test_validate_coerces_a_number_typed_into_a_text_box():
    ok, val = knobs.validate("trace.opacity", "0.5", "bar")
    assert ok and val == 0.5
    ok, val = knobs.validate("layout.margin.l", "200")
    assert ok and val == 200


def test_empty_means_clear_the_knob():
    assert knobs.validate("layout.hovermode", None) == (True, None)
    assert knobs.validate("layout.hovermode", "") == (True, None)
    assert knobs.validate("layout.hovermode", "   ") == (True, None)


def test_validate_never_raises_on_junk():
    for path, value in [
        ("", 1),
        ("layout", 1),
        ("trace.x", object()),
        ("layout.margin.l", ["a", "b"]),
        ("layout.width", "not a number"),
    ]:
        ok, _ = knobs.validate(path, value, "bar")
        assert isinstance(ok, bool)


# ---------------------------------------------------------------------
# Trace type lookup and depth cap
# ---------------------------------------------------------------------


def test_trace_type_lookup_and_deprecation_swap():
    assert knobs.trace_type_for("bar") == "bar"
    assert knobs.trace_type_for("densitymapbox") == "densitymap"
    assert knobs.trace_type_for("scattermapbox") == "scattermap"
    with pytest.raises(ValueError) as err:
        knobs.trace_type_for("not_a_chart")
    assert "sankey" in str(err.value)  # the error prints the legal list


def test_depth_cap_records_what_it_cut():
    knobs.tree("bar", COLUMNS)
    cut = knobs.cut_at_depth()
    assert cut, "the depth cap cut nothing - did MAX_DEPTH change?"
    assert all(isinstance(p, str) for p in cut)
    # Every cut path is itself in some tree as a "section" knob, so the UI
    # can still show that something lives under there. The recorders are
    # module-wide, so gather sections from every trace type we build.
    sections = {
        k.path
        for trace in TRACES
        for k in knobs.flat(trace, COLUMNS)
        if k.control == "section"
    }
    for path in cut:
        assert path in sections, f"{path} was cut but is not in any tree at all"


def test_loop_guard_is_belt_and_braces_on_this_install():
    """No real loop exists once template and compound arrays are excluded.

    Checked by walking layout to depth 12 with the guard instrumented. If
    this ever starts failing, Plotly grew a cycle and the guard earned its
    keep - read cut_as_cycle() to see where.
    """
    knobs.tree("bar", COLUMNS)
    assert knobs.cut_as_cycle() == ()


def test_every_validator_with_children_is_classified():
    """A validator that holds a data_class is either walked into or explicitly not.

    This is the tripwire for a future Plotly release. If it adds a new
    compound-ish validator class, this fails and someone has to decide
    whether the walk should open it - instead of it silently vanishing.
    """
    import plotly.graph_objects as go

    classified = knobs.RECURSE_VALIDATORS | knobs.NO_RECURSE_VALIDATORS
    found: set[str] = set()

    def scan(obj, depth):
        if depth > 2:
            return
        for name in obj._valid_props:
            try:
                v = obj._get_validator(name)
            except Exception:
                continue
            cls_name = type(v).__name__
            if cls_name in knobs.SKIP_VALIDATORS:
                continue
            if getattr(v, "data_class", None) is not None:
                found.add(cls_name)
                if cls_name in knobs.RECURSE_VALIDATORS:
                    scan(v.data_class(), depth + 1)

    scan(go.Layout(), 0)
    for trace in TRACES:
        scan(getattr(go, knobs.TRACE_CLASS_NAMES[knobs.trace_type_for(trace)])(), 0)

    assert found <= classified, f"unclassified compound validators: {sorted(found - classified)}"
    assert not (knobs.RECURSE_VALIDATORS & knobs.NO_RECURSE_VALIDATORS)


def test_knob_is_json_ready():
    import json

    knob = knobs.tree("bar", COLUMNS)[knobs.FRAME][0][0]
    json.dumps(knob.as_dict())


# ---------------------------------------------------------------------
# The _tree_cached contract: fresh containers, shared frozen Knobs
# ---------------------------------------------------------------------


def test_tree_hands_back_fresh_containers_every_call():
    """Mutating one tree() result must never leak into the next.

    app.py's knob_tree() rebinds tree[DATA] in place; if tree() ever handed
    out the cached containers themselves, that rebind would corrupt the
    cache for every later caller.
    """
    first = knobs.tree("bar", COLUMNS)
    second_before = sum(
        len(knobs.tree("bar", COLUMNS)[b][t]) for b in knobs.BUCKETS for t in knobs.TIERS)

    first[knobs.DATA] = {t: [] for t in knobs.TIERS}
    first[knobs.MARK][1].clear()
    first[knobs.FRAME][0].append("not even a Knob")

    third = knobs.tree("bar", COLUMNS)
    total = sum(len(third[b][t]) for b in knobs.BUCKETS for t in knobs.TIERS)
    assert total == second_before
    assert all(hasattr(k, "path") for k in third[knobs.FRAME][0])


def test_tree_shares_the_frozen_knob_objects():
    """The containers are fresh but the Knobs inside are the SAME objects -
    that identity is what makes the cache worth having."""
    a = knobs.tree("bar", COLUMNS)
    b = knobs.tree("bar", COLUMNS)
    shared = 0
    for bucket in knobs.BUCKETS:
        for tier in knobs.TIERS:
            for ka, kb in zip(a[bucket][tier], b[bucket][tier]):
                if ka.validator == "BaseTemplateValidator":
                    continue  # rebuilt fresh each call, by design
                assert ka is kb, ka.path
                shared += 1
    assert shared > 1000


def test_template_registered_after_first_build_still_appears():
    """A pio.templates entry added between two tree() calls must show up in
    layout.template's options - the one fact about the PROCESS, not Plotly."""
    import plotly.io as pio

    def template_knob(built):
        for bucket in knobs.BUCKETS:
            for tier in knobs.TIERS:
                for k in built[bucket][tier]:
                    if k.validator == "BaseTemplateValidator":
                        return k
        return None

    knobs.tree("bar", COLUMNS)  # warm the cache first
    name = "bench_test_template_freshness"
    pio.templates[name] = pio.templates["plotly_dark"]
    try:
        knob = template_knob(knobs.tree("bar", COLUMNS))
        assert knob is not None
        assert name in (knob.options or ())
    finally:
        del pio.templates[name]
    knob = template_knob(knobs.tree("bar", COLUMNS))
    assert name not in (knob.options or ())


def test_trace_type_for_still_raises_on_a_bad_key():
    """The lru_cache must not swallow or alter the ValueError contract."""
    for _ in range(2):  # twice: the second call exercises the cached path
        with pytest.raises(ValueError):
            knobs.trace_type_for("no_such_chart_key_ever")
    assert knobs.trace_type_for("bar") == knobs.trace_type_for("bar")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
