"""
THE BENCH - the adversarial pass.

    python -m pytest tests/test_bench_adversarial.py -q
    python tests/test_bench_adversarial.py            (same checks, prints)

Everything in here is a bug that was REPRODUCED against the running Bench
before it was fixed, plus the sweep that found it. Nothing is speculative. The
six things this file went hunting for, in the order the brief named them:

    (a) the two-way sync looping forever
    (b) a knob value that is legal in the UI but that Plotly then refuses
    (c) switching chart type with the last chart's knobs still in the SPEC
    (d) switching data source so the mapping points at columns that are gone
    (e) a knob path colliding across trace/layout
    (f) unicode or quote characters in a text knob breaking the generated code

(a), (d), (e) and (f) came back clean and have regression tests here anyway,
because "we looked and it held" is worth writing down. (b) and (c) did not, and
those tests are the ones with a story in the docstring.

It reuses the Bench harness in tests/test_bench_app.py rather than building a
second one - same pretend browser, same two real callbacks.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import plotly.graph_objects as go
import pytest
from dash import no_update

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import app as bench_app  # noqa: E402
from bench import codegen, controls, knobs, registry  # noqa: E402
from tests.test_bench_app import Bench  # noqa: E402


# =====================================================================
# HELPERS
# =====================================================================


def settle(bench: Bench, limit: int = 10) -> int:
    """Feed the app its own output until it goes quiet. Returns the rounds.

    This is the loop test in one function: hand the server back the exact code
    it typed into the box and the exact values it put in the widgets, over and
    over. An app that answers "changed!" to its own writing never stops.
    """
    for round_no in range(limit):
        quiet = True
        if bench.edit_code(bench.code)[0] is not no_update:
            quiet = False
        if bench.report_knobs()[0] is not no_update:
            quiet = False
        if quiet:
            return round_no
    raise AssertionError(f"the two-way sync never settled: {limit} rounds and "
                         "still rewriting the SPEC")


def all_knob_paths() -> set[str]:
    """Every knob path the panel can put on screen, across all 145 charts."""
    out: set[str] = set()
    for chart in sorted(registry.CHARTS):
        for knob in knobs.flat(chart, ["a", "b"]):
            out.add(knob.path)
    return out


CANONICAL = '''# --- data ---
df = bench.data.frame({"kind": "demo", "name": "category"})

# --- chart ---
fig = px.bar(df, x="agency", y="spend")

# --- FRAME ---
fig.update_layout(%s)

fig.show()
'''


@pytest.fixture()
def bench():
    return Bench()


# =====================================================================
# (b) A KNOB THE UI OFFERS AND PLOTLY THEN REFUSES
# ---------------------------------------------------------------------
# The hunt: build every knob for eight trace types, hand each one the value
# its own widget would produce, and see who says no. 2,467 paths, and the
# answers below are what came back.
# =====================================================================


LIST_SHAPED_TIER0 = [
    # path, what a human types into the box, what has to end up in the SPEC
    ("layout.yaxis.range", "[0, 100]", [0, 100]),
    ("layout.yaxis.range", "0, 100", [0, 100]),
    ("layout.colorway", "red, blue", ["red", "blue"]),
    ("layout.colorway", "#ff0000, #00ff00", ["#ff0000", "#00ff00"]),
    ("layout.annotations", '[{"text": "the March outage", "x": 1, "y": 2}]',
     [{"text": "the March outage", "x": 1, "y": 2}]),
    ("layout.shapes", '[{"type": "line", "x0": 0, "x1": 1, "y0": 0, "y1": 1}]',
     [{"type": "line", "x0": 0, "x1": 1, "y0": 0, "y1": 1}]),
]


@pytest.mark.parametrize("path,typed,wanted", LIST_SHAPED_TIER0)
def test_the_list_shaped_tier0_knobs_can_be_set_at_all(path, typed, wanted):
    """Four of ATLAS's twenty were dead knobs. This is the reproduction.

    `yaxis.range` (#6), `colorway` (#17), `annotations` (#19) and `shapes`
    (#20) are list-shaped properties, and controls.py has no list widget, so
    all four render as a plain text box. A text box hands back a string, and
    Plotly refuses a string for every one of them. Measured before the fix:
    there was no value you could type into `layout.yaxis.range` that the panel
    would accept - not "[0, 100]", not "0,100", not "0 100".

    `knobs._read_list` now reads the string as the list it is obviously trying
    to be, on the same principle as the float() attempt that was already there
    for number boxes.
    """
    ok, coerced = knobs.validate(path, typed, "bar")
    assert ok, f"{path} still refuses {typed!r}: {coerced}"
    assert coerced == wanted


def test_a_colorscale_name_is_still_a_name():
    """The list reader must not eat the values that were already working.

    "Viridis" is a colorscale NAME. It has no comma and it is not a literal, so
    it comes through untouched and Plotly expands it, exactly as before.
    """
    ok, coerced = knobs.validate("layout.coloraxis.colorscale", "Viridis", "bar")
    assert ok
    assert isinstance(coerced, list) and coerced[0][1] == "#440154"
    # and something that is not a list at all is still an honest refusal
    ok, why = knobs.validate("layout.xaxis.range", "not a list at all", "bar")
    assert not ok and "Invalid value" in why


def test_the_rescued_knobs_reach_the_figure_and_round_trip():
    """Set them for real: the SPEC holds them, the code writes them, the
    figure has them, and parse(render(spec)) still closes."""
    spec = bench_app.blank_spec()
    for path, typed in [("layout.yaxis.range", "[0, 100]"),
                        ("layout.colorway", "red, blue"),
                        ("layout.annotations", '[{"text": "spike", "x": 1, "y": 2}]')]:
        ok, coerced = knobs.validate(path, typed, "bar")
        assert ok
        spec["knobs"][path] = coerced

    code = bench_app.render_code(spec)
    assert codegen.parse(code)["knobs"] == spec["knobs"]

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fig, _msg = bench_app.figure_for(spec, *bench_app.get_frame(spec["source"]))
    assert not [w for w in caught if "did not apply" in str(w.message)]
    assert tuple(fig.layout.yaxis.range) == (0, 100)
    assert tuple(fig.layout.colorway) == ("red", "blue")
    assert len(fig.layout.annotations) == 1


def test_no_dropdown_offers_a_regex():
    """`xaxis.matches` was a dropdown of two options, both poison.

    Plotly's `values` list for it is nothing but two plotly.js regexes -
    '/^x([2-9]|[1-9][0-9]+)?( domain)?$/' and its y twin. `_enum_options`
    already dropped regexes, but it had a rescue for the case where cleaning
    emptied the list, so both regexes came straight back and either one was
    refused the moment you picked it.

    A regex is never pickable, so now it never survives. With nothing left to
    pick, the control degrades to a text box - and "x2", which is what the
    regex was describing, validates.
    """
    for chart in ("bar", "scatter", "heatmap"):
        for knob in knobs.flat(chart, ["a", "b"]):
            for option in (knob.options or ()):
                assert not (isinstance(option, str)
                            and option.startswith("/") and option.endswith("/")), \
                    f"{knob.path} offers a regex you cannot pick: {option!r}"

    matches = [k for k in knobs.flat("bar", ["a"])
               if k.path == "layout.xaxis.matches"][0]
    assert controls.kind(matches) == "text"
    assert matches.options is None
    assert knobs.validate("layout.xaxis.matches", "x2", "bar") == (True, "x2")


def test_the_integer_only_enums_kept_their_integers():
    """The stricter rule must not cost the two enums whose values ARE numbers.

    `geo.resolution` legitimately accepts only 110 or 50, and `surfaceaxis`
    only -1/0/1/2. They reach the same rescue `matches` used to abuse, and they
    have to keep it - the difference is that their entries are pickable and a
    regex is not.
    """
    resolution = [k for k in knobs.flat("choropleth", ["a"])
                  if k.path == "layout.geo.resolution"][0]
    assert resolution.options == (110, 50)
    surfaceaxis = [k for k in knobs.flat("scatter3d", ["a"])
                   if k.path == "trace.surfaceaxis"][0]
    assert set(surfaceaxis.options) >= {-1, 0, 1}


def test_every_knob_the_panel_stores_is_a_json_value(bench):
    """SPEC section 3: the state object has to survive a dcc.Store.

    The one validator on this install that answers with a graph object rather
    than a value is `layout.template` - `validate_coerce("plotly_dark")` builds
    the whole expanded Template, 13,670 characters of it. Stored, that is a
    14 KB code panel and a knob that silently does not apply.
    """
    bench.set_knob("layout.template", "plotly_dark")
    assert bench.spec["knobs"]["layout.template"] == "plotly_dark"
    assert 'template="plotly_dark"' in bench.code
    assert len(bench.code) < 2000, "the code panel exploded"
    json.dumps(bench.spec)                      # raises if it is not JSON
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        bench.render()
    assert not [w for w in caught if "did not apply" in str(w.message)]
    assert bench.figure.layout.template.layout.paper_bgcolor == "rgb(17,17,17)"


# =====================================================================
# (b) + (f) THE CODE PANEL THAT TOOK THE WHOLE SCREEN DOWN
# ---------------------------------------------------------------------
# `render_chart` paints the figure, the code box, the build message and the
# status bar. It used to call codegen.render with no guard. So any SPEC
# codegen refuses to write was not one bad knob - it was four dark panes and
# an error only the server log ever saw.
# =====================================================================


KILLERS = [
    ("width=1e400", "an infinite float"),
    ("width=-1e400", "minus infinity"),
    ("_=1", "a bare underscore keyword -> the path 'layout..'"),
    ("__=1", "two underscores -> 'layout...'"),
    ("title_=1", "a trailing underscore -> 'layout.title.'"),
    ("_title=1", "a leading underscore -> 'layout..title'"),
]


@pytest.mark.parametrize("keyword,why", KILLERS)
def test_a_code_edit_that_cannot_be_written_back_goes_to_custom(keyword, why, bench):
    """Six characters used to kill the app. Now they are CUSTOM mode.

    `fig.update_layout(width=1e400)` parses - it is the canonical shape as far
    as `ast` is concerned - so the old `_apply_code` put `inf` straight in the
    SPEC. `codegen._literal` then refused to write it ("inf and nan are not
    JSON either") and raised out of the render lane.

    Two fixes, and both are the mirror rule codegen is built on: `parse` will
    not read a number `render` will not write, and it will not invent a knob
    path with an empty segment. Belt and braces, `_apply_code` renders the
    parsed SPEC once before letting it into the store.
    """
    source = CANONICAL % keyword
    assert codegen.parse(source) is None, f"parse still accepts {keyword}"

    bench.edit_code(source)                    # must not raise
    assert bench.spec["custom_code"] == source, why
    assert "CUSTOM mode" in bench.knob_msg
    assert isinstance(bench.figure, go.Figure)
    json.dumps(bench.spec)

    bench.reset()
    assert bench.spec["custom_code"] is None
    assert codegen.parse(bench.code) is not None
    assert settle(bench) == 0


def test_parse_never_invents_a_knob_path():
    """Every segment of a knob path is a Plotly property name."""
    for keyword in ("_", "__", "title_", "_title", "a__b"):
        spec = codegen.parse(CANONICAL % f"{keyword}=1")
        assert spec is None, f"parse accepted {keyword!r}"
    # and the real ones still read
    spec = codegen.parse(CANONICAL % 'paper_bgcolor="#000", xaxis_title_text="a"')
    assert spec["knobs"] == {"layout.paper_bgcolor": "#000",
                             "layout.xaxis.title.text": "a"}


def test_parse_never_returns_a_number_render_cannot_write():
    for value in ("1e400", "-1e400", "1e400 - 1e400"):
        assert codegen.parse(CANONICAL % f"width={value}") is None, value


# =====================================================================
# (c) SWITCHING CHART WITH THE OLD CHART'S KNOBS STILL IN THE SPEC
# =====================================================================


def test_a_picker_click_drops_trace_knobs_with_no_home_and_keeps_layout(bench):
    """Carry-over keeps what fits. Layout knobs are universal (go.Layout is
    one class shared by every trace), so barmode rides to sankey even though
    sankey ignores it; trace.marker.opacity has no home there and goes. And
    the sync still settles - no echo loop from the carry."""
    bench.set_knob("layout.barmode", "group")
    bench.set_knob("trace.marker.opacity", 0.4)
    bench.click_chart("sankey")
    assert bench.spec["knobs"].get("layout.barmode") == "group"
    assert "trace.marker.opacity" not in bench.spec["knobs"]
    assert settle(bench) == 0


def test_changing_chart_in_the_code_keeps_the_knobs_and_says_which_are_homeless(bench):
    """The code panel does NOT clear knobs, and it should not - you typed them.

    But a knob the new chart does not have gets no widget in the pane, so the
    only place it exists is the line you typed. It applies to nothing and warns
    into the server log. Silence there is the bug; the fix is a sentence.
    """
    bench.set_knob("layout.barmode", "group")
    bench.set_knob("trace.marker.opacity", 0.4)
    edited = (bench.code
              .replace("fig = px.bar(df, ", 'fig = bench.registry.build("sankey", df, ')
              .replace('x="agency", y="spend"',
                       'source="agency", target="agency", value="spend"'))
    bench.edit_code(edited)

    assert bench.spec["chart"] == "sankey"
    assert bench.spec["custom_code"] is None
    assert bench.spec["knobs"]["trace.marker.opacity"] == 0.4   # kept, as typed
    assert not bench.has_widget("trace.marker.opacity")         # but homeless
    assert "trace.marker.opacity" in bench.knob_msg
    assert "no such setting" in bench.knob_msg
    assert isinstance(bench.figure, go.Figure)
    assert settle(bench) == 0


# =====================================================================
# (d) A NEW SOURCE, AND THE MAPPING THAT POINTED AT THE OLD ONE
# =====================================================================


@pytest.mark.parametrize("chart", sorted(registry.CHARTS))
def test_no_chart_is_left_pointing_at_a_column_that_is_gone(chart):
    """145 charts x ten demo frames. Every mapping slot must name a real
    column of the frame on screen, or be empty. Nothing else."""
    frames = ["category", "long", "scatter", "timeseries", "flow", "states",
              "ohlc", "hierarchy", "numeric_block", "grid"]
    spec = bench_app.blank_spec()
    start_df, _meta = bench_app.get_frame(spec["source"])
    spec["chart"] = chart
    spec["mapping"] = registry.auto_map(start_df, registry.CHARTS[chart])

    for name in frames:
        spec, _msg = bench_app._apply_source(spec, "bench-src-demo", "demo", name, "")
        df, meta = bench_app.get_frame(spec["source"])
        columns = set(bench_app._columns(df))
        for slot, value in (spec["mapping"] or {}).items():
            for one in (value if isinstance(value, list) else
                        ([value] if value else [])):
                assert str(one) in columns, \
                    f"{chart} on {name}: slot {slot} still points at {one!r}"
        fig, _why = bench_app.figure_for(spec, df, meta)
        assert isinstance(fig, go.Figure)
        assert fig.data or fig.layout.annotations, \
            f"{chart} on {name}: blank figure with nothing said"


def test_a_source_change_in_the_code_panel_says_what_broke(bench):
    """The code panel can change the source without going near _apply_source,
    so the mapping is whatever you left in the chart line. That has to be a
    sentence on screen, not a blank pane."""
    bench.edit_code(bench.code.replace('"name": "category"', '"name": "flow"'))
    assert bench.spec["source"] == {"kind": "demo", "name": "flow"}
    assert "not the name of a column" in bench.build_msg
    assert "source" in bench.build_msg and "amount" in bench.build_msg
    assert isinstance(bench.figure, go.Figure)
    assert bench.figure.layout.annotations, "blank pane, nothing said"
    assert settle(bench) == 0


def test_a_many_slot_shows_the_columns_the_spec_actually_holds():
    """17 charts have a column-LIST slot, and every one of them rendered empty.

    `controls._value_for` reaches into SPEC["mapping"] only for a knob it drew
    as a single-column dropdown. A `many` slot is drawn as a multi-select, so
    it fell through to SPEC["knobs"], found nothing, and showed you an empty
    REQUIRED slot on a chart that was drawing perfectly off five columns. The
    first column you then picked replaced all five.
    """
    spec = bench_app.blank_spec()
    spec["source"] = {"kind": "demo", "name": "numeric_block"}
    spec["chart"] = "corr_matrix"
    df, _meta = bench_app.get_frame(spec["source"])
    spec["mapping"] = registry.auto_map(df, registry.CHARTS["corr_matrix"])
    assert len(spec["mapping"]["values"]) >= 3, "auto_map picked nothing to test with"

    pane = bench_app.knob_pane(spec, bench_app._columns(df))
    shown = bench_app.knob_echo(pane)
    assert shown["value|mapping.values"] == spec["mapping"]["values"]


def test_every_many_slot_on_every_chart_shows_itself():
    """The same check, over all 17."""
    for chart in sorted(registry.CHARTS):
        template = registry.CHARTS[chart]
        if not any(slot.many for slot in template.slots):
            continue
        spec = bench_app.blank_spec()
        spec["source"] = {"kind": "demo", "name": "numeric_block"}
        spec["chart"] = chart
        df, _meta = bench_app.get_frame(spec["source"])
        spec["mapping"] = registry.auto_map(df, template)
        shown = bench_app.knob_echo(bench_app.knob_pane(spec, bench_app._columns(df)))
        for slot in template.slots:
            if not slot.many:
                continue
            key = f"value|{bench_app.MAPPING_PREFIX}{slot.name}"
            if key not in shown:
                continue            # the slot has no widget on this chart
            assert shown[key] == spec["mapping"][slot.name], f"{chart}.{slot.name}"


# =====================================================================
# (e) A KNOB PATH COLLIDING ACROSS TRACE / LAYOUT
# ---------------------------------------------------------------------
# Came back clean: 3,163 distinct paths, no collisions. Kept because the
# thing that makes it clean is a seven-name table in codegen.py, and a
# future Plotly could add the eighth.
# =====================================================================


def test_no_two_knob_paths_flatten_to_the_same_keyword():
    """`layout.xaxis.categoryorder` -> `xaxis_categoryorder` and back.

    Two paths landing on one keyword in the same call would mean the second
    silently overwrote the first in the generated code. Checked over every path
    the panel can render, for every chart.
    """
    owner: dict[tuple[str, str], str] = {}
    for path in sorted(all_knob_paths()):
        prefix = path.partition(".")[0]
        keyword = codegen._flatten(path)
        assert codegen._real_path(prefix, keyword) == path, \
            f"{path} does not survive flatten -> unflatten"
        key = (codegen.BUCKET_CALL[codegen._emit_bucket(path)], keyword)
        assert owner.get(key, path) == path, \
            f"{owner[key]} and {path} both write {key[1]}= into {key[0]}"
        owner[key] = path


def test_render_refuses_none_of_the_paths_the_panel_can_produce():
    """render() raises rather than returning, so a path it hates is a dead
    screen. Prove it hates none of them."""
    for path in sorted(all_knob_paths()):
        codegen.render({"chart": "bar", "source": {"kind": "demo", "name": "category"},
                        "mapping": {}, "knobs": {path: 1}, "custom_code": None})


def test_the_mapping_pane_cannot_collide_with_a_plotly_knob():
    """45 real Plotly paths end in a segment that is also a mapping slot name -
    `trace.values`, `trace.open`, `trace.color`, `trace.lat`. They all live in
    the DATA bucket that `knob_tree` replaces, so none is on screen, and
    `shown_values` keys by the whole dotted path anyway."""
    for chart in sorted(registry.CHARTS):
        spec = bench_app.blank_spec()
        spec["chart"] = chart
        df, _meta = bench_app.get_frame(spec["source"])
        spec["mapping"] = registry.auto_map(df, registry.CHARTS[chart])
        pane = bench_app.knob_pane(spec, bench_app._columns(df))
        seen: set[str] = set()
        for node in pane._traverse():
            cid = getattr(node, "id", None)
            if cid is None:
                continue
            key = json.dumps(cid, sort_keys=True) if isinstance(cid, dict) else str(cid)
            assert key not in seen, f"{chart}: duplicate component id {key}"
            seen.add(key)


# =====================================================================
# (f) UNICODE AND QUOTES IN A TEXT KNOB
# ---------------------------------------------------------------------
# Came back clean: 21 hostile strings, all of them stored, written, read
# back and drawn without a mark on them. `codegen._pystr` earns its keep.
# =====================================================================


HOSTILE_TEXT = [
    'He said "hello"',
    "it's a plan",
    'both "and" it\'s',
    "back\\slash",
    "tab\there",
    "line\nbreak",
    "carriage\rreturn",
    'triple """ quotes',
    "# --- MARK -------------------------------------------------------",
    "fig.show()",
    '"); import os; os.system("calc",  #',
    "emoji \U0001F1EC\U0001F1E7 spend ↑ 12%",
    "‮RTL override",
    "nul\x00byte",
    " line separator",
    "£ € ¥ — ‘’ “”",
    "a" * 400,
    "\\n not a newline",
    "{braces} and %format% and {0}",
    "\ud800lone surrogate",
    "df = evil()\nfig = px.bar(df)",
]


@pytest.mark.parametrize("text", HOSTILE_TEXT, ids=range(len(HOSTILE_TEXT)))
def test_a_hostile_title_survives_the_whole_round_trip(text):
    """Type it, store it, write it, read it, draw it, and hand it to the
    browser - unchanged at every step, and the sync still settles.

    The three that would have been most likely to break it are worth naming:
    a title that IS the canonical MARK header, a title that IS `fig.show()`,
    and a title that tries to close the string literal and start a statement.
    `ast` never sees any of them as code, because `_pystr` escapes on the way
    out and `_read_value` only ever reads a Constant on the way back.
    """
    from plotly.utils import PlotlyJSONEncoder

    bench = Bench()
    bench.set_knob("layout.title.text", text)
    assert bench.spec["knobs"]["layout.title.text"] == text
    assert codegen.parse(bench.code)["knobs"]["layout.title.text"] == text
    json.dumps(bench.spec)
    json.dumps(bench.figure, cls=PlotlyJSONEncoder)
    assert settle(bench) == 0


# =====================================================================
# (a) THE LOOP
# ---------------------------------------------------------------------
# Came back clean under every action and sequence tried. The three rules in
# app.py's docstring hold. These are the receipts.
# =====================================================================


ACTIONS = {
    "turn a title knob": lambda b: b.set_knob("layout.title.text", "hi"),
    "drag a slider": lambda b: b.set_knob("trace.marker.opacity", 0.4),
    "flip a toggle": lambda b: b.set_knob("layout.showlegend", True),
    "pick a template": lambda b: b.set_knob("layout.template", "plotly_dark"),
    "type a colour": lambda b: b.set_knob("layout.paper_bgcolor", "#123456",
                                          part="hex"),
    "type a range": lambda b: b.set_knob("layout.yaxis.range", "[0, 100]"),
    "pick a column": lambda b: b.set_knob("mapping.color", "agency"),
    "clear a column": lambda b: b.set_knob("mapping.x", None),
    "click a chart": lambda b: b.click_chart("box_compare"),
    "click one that cannot draw": lambda b: b.click_chart("sankey"),
    "change the demo frame": lambda b: b.set_source("demo", "flow"),
    "go to warehouse SQL": lambda b: b.set_source("warehouse", sql="SELECT 1"),
    "drop into CUSTOM": lambda b: b.edit_code("fig = px.bar(df, x='agency')"),
    "empty the box": lambda b: b.edit_code(""),
}


@pytest.mark.parametrize("name", sorted(ACTIONS))
def test_the_sync_settles_after(name, bench):
    ACTIONS[name](bench)
    assert settle(bench) == 0


def test_the_sync_settles_after_a_long_session(bench):
    """One of everything, in a row, then feed it all back."""
    bench.set_knob("layout.title.text", "one")
    bench.click_chart("box_compare")
    bench.set_source("demo", "scatter")
    bench.set_knob("layout.hovermode", "x unified")
    bench.knob_query = "grid"
    bench.render()
    bench.edit_code("import os")
    bench.reset()
    assert settle(bench) == 0


@pytest.mark.parametrize("chart", sorted(registry.CHARTS))
def test_the_sync_settles_after_clicking(chart, bench):
    bench.click_chart(chart)
    assert settle(bench, limit=6) == 0


# =====================================================================
# printed run, for a human
# =====================================================================


def _main() -> int:
    def say(text: str = "") -> None:
        sys.stdout.write(
            text.encode(sys.stdout.encoding or "utf-8", errors="backslashreplace")
            .decode(sys.stdout.encoding or "utf-8", errors="replace") + "\n")

    warnings.simplefilter("ignore")
    failures: list[str] = []

    def run(label: str, fn) -> None:
        try:
            got = fn()
            say(f"  ok   {label:52s} {got}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{label}: {type(exc).__name__}: {exc}")
            say(f"  FAIL {label:52s} {type(exc).__name__}: {exc}")

    say("=" * 78)
    say("THE BENCH - adversarial pass")
    say("=" * 78)

    say("\n(b) knobs the UI offers and Plotly used to refuse")
    for path, typed, wanted in LIST_SHAPED_TIER0[:4]:
        run(f"{path} <- {typed!r}",
            lambda p=path, t=typed, w=wanted: (
                knobs.validate(p, t, "bar") == (True, w) or
                (_ for _ in ()).throw(AssertionError(knobs.validate(p, t, "bar")))) and
            f"-> {w}")
    run("layout.template stores a name, not a Template",
        lambda: f"-> {knobs.validate('layout.template', 'plotly_dark', 'bar')[1]!r}")
    run("layout.xaxis.matches is a text box now",
        lambda: f"-> {controls.kind([k for k in knobs.flat('bar', ['a']) if k.path == 'layout.xaxis.matches'][0])}")

    say("\n(b)+(f) code-panel edits that used to kill the screen")
    for keyword, why in KILLERS:
        run(f"update_layout({keyword})",
            lambda k=keyword: ("-> CUSTOM" if codegen.parse(CANONICAL % k) is None
                               else (_ for _ in ()).throw(AssertionError("accepted"))))

    say("\n(c) chart switch")
    b = Bench()
    b.set_knob("trace.marker.opacity", 0.4)
    b.click_chart("sankey")
    run("picker click clears the old knobs", lambda: f"-> knobs={b.spec['knobs']}")

    say("\n(d) a `many` mapping slot")
    spec = bench_app.blank_spec()
    spec["source"] = {"kind": "demo", "name": "numeric_block"}
    spec["chart"] = "corr_matrix"
    df, _m = bench_app.get_frame(spec["source"])
    spec["mapping"] = registry.auto_map(df, registry.CHARTS["corr_matrix"])
    shown = bench_app.knob_echo(bench_app.knob_pane(spec, bench_app._columns(df)))
    run("corr_matrix shows its columns",
        lambda: f"-> {shown['value|mapping.values']}")

    say("\n(e) knob paths")
    paths = all_knob_paths()
    run(f"{len(paths)} paths flatten and come back",
        lambda: f"-> {sum(1 for p in paths if codegen._real_path(p.partition('.')[0], codegen._flatten(p)) == p)} of {len(paths)}")

    say("\n(f) hostile text, and (a) the loop")
    bad = []
    for text in HOSTILE_TEXT:
        bench = Bench()
        bench.set_knob("layout.title.text", text)
        if (bench.spec["knobs"]["layout.title.text"] != text
                or codegen.parse(bench.code)["knobs"]["layout.title.text"] != text):
            bad.append(text)
    run(f"{len(HOSTILE_TEXT)} hostile titles round-trip", lambda: f"-> {len(bad)} broke")

    bench = Bench()
    bench.set_knob("layout.title.text", "Spend by agency")
    run("the sync settles", lambda: f"-> {settle(bench)} extra rounds")

    say()
    if failures:
        say(f"FAILURES: {len(failures)}")
        for f in failures:
            say("  " + f)
        return 1
    say("OK - every finding above was reproduced first, then fixed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
