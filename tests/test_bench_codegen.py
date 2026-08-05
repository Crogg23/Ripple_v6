"""The round-trip contract for bench/codegen.py.

Three things get proved here, in this order of importance:

1.  parse(render(spec)) == spec, EXACTLY, over a battery of 30-plus specs -
    same values, same Python types. This is the contract the Bench's two-way
    code panel rests on.
2.  parse() never raises and returns None on anything that is not the
    canonical shape. That is what puts the app into CUSTOM mode cleanly.
3.  The two measured tables inside codegen.py still match the plotly that is
    actually installed. Those tests skip if plotly is absent; everything else
    runs with nothing but the standard library.

Run just this file:   python -m pytest tests/test_bench_codegen.py -q
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bench import codegen  # noqa: E402


# =====================================================================
# HELPERS
# =====================================================================


def same(a, b) -> bool:
    """Equal AND the same Python type, all the way down.

    Plain `==` is not enough here: in Python `True == 1` and `1 == 1.0`, so a
    bool that came back as an int would slip through an `==` check. The whole
    point of the contract is that a value comes back as what it went in as.
    """
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def spec(chart="bar", source=None, mapping=None, knobs=None):
    """A complete SPEC dict with every key present."""
    return {
        "chart": chart,
        "source": source if source is not None else {"kind": "demo", "name": "demo_1"},
        "mapping": mapping if mapping is not None else {"x": "STATE", "y": "TOTAL"},
        "knobs": knobs if knobs is not None else {},
        "custom_code": None,
    }


# =====================================================================
# THE BATTERY - every spec here must survive parse(render(spec)) exactly
# =====================================================================

SPECS: list[tuple[str, dict]] = [
    # --- the empty end of the range ------------------------------------
    ("bare, no knobs at all", spec()),
    ("no mapping either", spec(mapping={})),
    ("registry chart (no px front door)", spec(chart="sankey")),
    ("registry chart with mapping",
     spec(chart="sankey", mapping={"source": "FROM", "target": "TO", "value": "AMT"})),
    ("hand-built recipe key", spec(chart="bump_chart", mapping={"x": "year", "y": "rank"})),

    # --- one bucket at a time ------------------------------------------
    ("MARK only", spec(knobs={"trace.marker.opacity": 0.8})),
    ("SCALE only", spec(knobs={"layout.xaxis.categoryorder": "total descending"})),
    ("FRAME only", spec(knobs={"layout.template": "plotly_dark"})),
    ("INTERACTION only", spec(knobs={"layout.hovermode": "x unified"})),
    ("MOTION only", spec(knobs={"layout.transition.duration": 500})),

    # --- all five buckets at once --------------------------------------
    ("all five buckets", spec(knobs={
        "trace.marker.opacity": 0.8,
        "layout.yaxis.tickformat": ",.0f",
        "layout.title.text": "Spend by state",
        "layout.dragmode": "pan",
        "layout.transition.easing": "cubic-in-out",
    })),

    # --- the value types -----------------------------------------------
    ("string value", spec(knobs={"layout.barmode": "group"})),
    ("empty string value", spec(knobs={"layout.title.text": ""})),
    ("int value", spec(knobs={"layout.height": 640})),
    ("zero", spec(knobs={"layout.margin.l": 0})),
    ("negative int", spec(knobs={"layout.legend.x": -1})),
    ("big int", spec(knobs={"layout.width": 10 ** 18})),
    ("float value", spec(knobs={"trace.marker.opacity": 0.8})),
    ("float that is a whole number", spec(knobs={"trace.opacity": 1.0})),
    ("negative float", spec(knobs={"layout.legend.y": -0.25})),
    ("tiny float", spec(knobs={"layout.uniformtext.minsize": 1e-09})),
    ("awkward float", spec(knobs={"trace.marker.opacity": 0.1 + 0.2})),
    ("bool True", spec(knobs={"layout.showlegend": True})),
    ("bool False", spec(knobs={"layout.showlegend": False})),
    ("None value", spec(knobs={"layout.width": None})),
    ("bool and int side by side",
     spec(knobs={"layout.showlegend": True, "layout.height": 1})),

    # --- lists ----------------------------------------------------------
    ("list of ints", spec(knobs={"layout.yaxis.range": [0, 100]})),
    ("empty list", spec(knobs={"layout.shapes": []})),
    ("list of strings", spec(knobs={"layout.colorway": ["#58a6ff", "#f778ba", "#3fb950"]})),
    ("mixed list", spec(knobs={"layout.xaxis.range": [0, 1.5, True, None, "auto"]})),
    ("nested list", spec(knobs={"layout.colorscale.sequential": [[0, "#000"], [1, "#fff"]]})),
    ("list in the mapping", spec(chart="treemap",
                                 mapping={"path": ["agency", "program", "vendor"],
                                          "values": "amount"})),

    # --- dicts -----------------------------------------------------------
    ("dict value", spec(knobs={"layout.legend": {"orientation": "h", "y": 1.08}})),
    ("empty dict", spec(knobs={"layout.grid": {}})),
    ("dict inside a list",
     spec(knobs={"layout.annotations": [{"text": "March outage", "x": 3, "showarrow": False}]})),

    # --- unicode and awkward strings -------------------------------------
    ("unicode value", spec(knobs={"layout.title.text": "Gastos por región — café ☕"})),
    ("unicode in the mapping", spec(mapping={"x": "ESTADO", "y": "MONTO_TOTAL_€"})),
    ("quotes and backslashes",
     spec(knobs={"layout.title.text": 'she said "no" \\ then left'})),
    ("newlines and tabs", spec(knobs={"layout.title.text": "line one\nline two\tend"})),
    ("control characters", spec(knobs={"layout.title.text": "bell\x07null-ish\x00end"})),
    ("right-to-left and emoji", spec(knobs={"layout.title.text": "مرحبا 👋🏽 done"})),

    # --- deep dotted paths ------------------------------------------------
    ("depth 3 path", spec(knobs={"layout.xaxis.title.font": "Inter"})),
    ("depth 4 path", spec(knobs={"layout.xaxis.title.font.size": 14})),
    ("depth 5 path", spec(knobs={"trace.marker.colorbar.title.font": "Inter"})),
    ("depth 6 path (deeper than plotly goes)",
     spec(knobs={"trace.marker.colorbar.title.font.color": "#e6edf3"})),
    ("underscore-carrying name", spec(knobs={"layout.paper_bgcolor": "#0b0f14"})),
    ("both underscore backgrounds",
     spec(knobs={"layout.paper_bgcolor": "#0b0f14", "layout.plot_bgcolor": "#0b0f14"})),
    ("underscore name mid-path", spec(knobs={"trace.error_y.visible": True})),
    ("underscore name deep", spec(knobs={"trace.error_x.color": "#ff7b9c"})),

    # --- the source seam ---------------------------------------------------
    ("warehouse source", spec(source={
        "kind": "warehouse",
        "sql": "SELECT state, SUM(total) AS total FROM mart.spend GROUP BY 1",
    })),
    ("multi-line sql", spec(source={
        "kind": "warehouse",
        "sql": "SELECT state,\n       SUM(total) AS total\nFROM mart.spend\nGROUP BY 1",
    })),
    ("sql with quotes", spec(source={
        "kind": "warehouse",
        "sql": "SELECT * FROM t WHERE name = 'O\\'Brien' AND x = \"y\"",
    })),
    ("empty source", spec(source={})),
    ("source with extra keys", spec(source={
        "kind": "warehouse", "sql": "SELECT 1", "limit_rows": 50000, "cached": False,
    })),

    # --- everything at once -------------------------------------------------
    ("the kitchen sink", spec(
        chart="scatter",
        source={"kind": "warehouse", "sql": "SELECT * FROM mart.entity_spend",
                "limit_rows": 100000},
        mapping={"x": "INSPECTIONS", "y": "VIOLATIONS", "color": "REGION",
                 "size": "EMPLOYEES", "hover_name": "ENTITY", "symbol": None},
        knobs={
            "trace.marker.opacity": 0.55,
            "trace.marker.line.width": 0,
            "trace.marker.symbol": "circle",
            "trace.error_y.visible": False,
            "layout.xaxis.type": "log",
            "layout.xaxis.title.text": "Inspections",
            "layout.yaxis.range": [0, 250],
            "layout.coloraxis.colorbar.thickness": 11,
            "layout.title.text": "Who gets inspected, and who gets cited",
            "layout.paper_bgcolor": "#0b0f14",
            "layout.plot_bgcolor": "#0b0f14",
            "layout.margin.l": 56,
            "layout.showlegend": True,
            "layout.width": None,
            "layout.hovermode": "x unified",
            "layout.hoverlabel.namelength": -1,
            "layout.dragmode": "pan",
            "layout.transition.duration": 400,
        },
    )),
    ("many knobs in one bucket, forces line wrapping", spec(knobs={
        f"layout.annotations{i}": f"note number {i}" for i in range(12)
    })),
]


@pytest.mark.parametrize("label,s", SPECS, ids=[lbl for lbl, _ in SPECS])
def test_round_trip_is_exact(label, s):
    """parse(render(spec)) == spec, same values AND same types."""
    code = codegen.render(s)
    back = codegen.parse(code)
    assert back is not None, f"{label}: canonical code failed to parse\n{code}"
    assert same(back, s), f"{label}:\n  wanted {s}\n  got    {back}\ncode:\n{code}"


def test_the_battery_is_big_enough():
    """A guard on this file, not on the module: keep the coverage honest."""
    assert len(SPECS) >= 30


@pytest.mark.parametrize("label,s", SPECS, ids=[lbl for lbl, _ in SPECS])
def test_render_is_deterministic(label, s):
    """The same spec always produces the same characters."""
    assert codegen.render(s) == codegen.render(s)


@pytest.mark.parametrize("label,s", SPECS, ids=[lbl for lbl, _ in SPECS])
def test_render_output_is_valid_python(label, s):
    """Whatever we write has to at least be parseable Python."""
    ast.parse(codegen.render(s))


def test_second_pass_is_stable():
    """render -> parse -> render lands on the same text. No drift on re-entry."""
    for _, s in SPECS:
        once = codegen.render(s)
        twice = codegen.render(codegen.parse(once))
        assert once == twice


# =====================================================================
# HOSTILE INPUT - parse must return None and must never raise
# =====================================================================

HOSTILE: list[tuple[str, str]] = [
    ("empty string", ""),
    ("only whitespace", "   \n\n\t  \n"),
    ("only a comment", "# just a comment\n"),
    ("only a docstring", '"""a module docstring and nothing else"""\n'),
    ("syntax error - unclosed paren", "df = bench.data.frame({\n"),
    ("syntax error - dangling operator", "1 +\n"),
    ("syntax error - bad indent", "df = 1\n    fig = 2\n"),
    ("an import", "import os\ndf = bench.data.frame({})\nfig = px.bar(df)\n"),
    ("a from-import", "from os import system\ndf = bench.data.frame({})\n"),
    ("a for loop",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfor i in range(3):\n    pass\n'),
    ("a while loop", 'df = bench.data.frame({})\nfig = px.bar(df)\nwhile True:\n    pass\n'),
    ("a def", 'df = bench.data.frame({})\nfig = px.bar(df)\ndef go():\n    return 1\n'),
    ("a class", 'df = bench.data.frame({})\nfig = px.bar(df)\nclass X:\n    pass\n'),
    ("a lambda in a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(x=lambda: 1)\n'),
    ("a walrus", 'df = bench.data.frame({})\nfig = px.bar(df)\n(x := 1)\n'),
    ("an f-string knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(title_text=f"{x}")\n'),
    ("arithmetic in a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(height=2 * 300)\n'),
    ("a name reference in a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(template=THEME)\n'),
    ("a call inside a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(x=dict(a=1))\n'),
    ("an unknown extra call",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.write_html("out.html")\n'),
    ("an unknown method on fig",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.add_hline(y=40)\n'),
    ("something after fig.show()",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.show()\nfig.update_layout(a=1)\n'),
    ("wrong first variable", 'data = bench.data.frame({})\nfig = px.bar(data)\n'),
    ("wrong source function", 'df = pd.read_csv("x.csv")\nfig = px.bar(df)\n'),
    ("source handed a string", 'df = bench.data.frame("demo")\nfig = px.bar(df)\n'),
    ("source handed keywords", 'df = bench.data.frame(kind="demo")\nfig = px.bar(df)\n'),
    ("chart not handed df", 'df = bench.data.frame({})\nfig = px.bar(other)\n'),
    ("chart call is bare, not dotted", 'df = bench.data.frame({})\nfig = bar(df)\n'),
    ("chart call is chained",
     'df = bench.data.frame({})\nfig = px.bar(df).update_xaxes(type="log")\n'),
    ("star-args on a knob call",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(**opts)\n'),
    ("positional arg on a knob call",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(dict(a=1))\n'),
    ("only one statement", 'df = bench.data.frame({})\n'),
    ("bytes literal in a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(a=b"x")\n'),
    ("complex number in a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(a=1j)\n'),
    ("ellipsis in a knob",
     'df = bench.data.frame({})\nfig = px.bar(df)\nfig.update_layout(a=...)\n'),
    ("non-string dict key",
     'df = bench.data.frame({1: "one"})\nfig = px.bar(df)\n'),
    ("non-ASCII identifiers", "Ω = 1\nλ = Ω\n"),
    ("non-ASCII prose", "это не питон, это просто текст\n"),
    ("null byte", "df = bench.data.frame({})\x00\n"),
    ("a very long line", "x = " + " + ".join(["1"] * 20000) + "\n"),
    ("a very long string literal", 'df = "' + "a" * 500_000 + '"\n'),
    ("deeply nested brackets", "x = " + "[" * 200 + "]" * 200 + "\n"),
    ("decorator", "@thing\ndef f():\n    pass\n"),
    ("try/except", "try:\n    pass\nexcept Exception:\n    pass\n"),
    ("exec-looking string", '__import__("os").system("echo hi")\n'),
]


@pytest.mark.parametrize("label,src", HOSTILE, ids=[lbl for lbl, _ in HOSTILE])
def test_hostile_input_returns_none_and_never_raises(label, src):
    assert codegen.parse(src) is None, f"{label}: expected CUSTOM mode (None)"


def test_the_hostile_list_is_big_enough():
    assert len(HOSTILE) >= 15


@pytest.mark.parametrize("value", [None, 123, 4.5, True, b"bytes", [], {}, object()])
def test_parse_never_raises_on_junk_types(value):
    """Even handed something that is not a string at all."""
    assert codegen.parse(value) is None


# =====================================================================
# SHAPE - the canonical form is what SPEC section 5 says it is
# =====================================================================


def test_matches_the_spec_example():
    """The example printed in SPEC section 5, rendered."""
    code = codegen.render(spec(
        chart="bar",
        mapping={"x": "STATE", "y": "TOTAL"},
        knobs={
            "trace.marker.opacity": 0.8,
            "layout.xaxis.categoryorder": "total descending",
            "layout.barmode": "group",
            "layout.template": "plotly_dark",
        },
    ))
    assert 'fig = px.bar(df, x="STATE", y="TOTAL")' in code
    assert "fig.update_traces(marker_opacity=0.8)" in code
    assert 'fig.update_layout(xaxis_categoryorder="total descending")' in code
    assert 'fig.update_layout(barmode="group", template="plotly_dark")' in code
    assert code.rstrip().endswith("fig.show()")


def test_buckets_come_out_in_the_fixed_order():
    code = codegen.render(spec(knobs={
        "layout.transition.duration": 100,   # MOTION
        "layout.dragmode": "pan",            # INTERACTION
        "layout.template": "plotly_dark",    # FRAME
        "layout.xaxis.type": "log",          # SCALE
        "trace.marker.opacity": 0.5,         # MARK
    }))
    seen = [b for b in codegen.BUCKET_ORDER if f"# --- {b} " in code]
    assert seen == list(codegen.BUCKET_ORDER)
    positions = [code.index(f"# --- {b} ") for b in codegen.BUCKET_ORDER]
    assert positions == sorted(positions)


def test_an_empty_bucket_emits_absolutely_nothing():
    """SPEC 5 rule 1: not an empty call, not a lonely comment."""
    code = codegen.render(spec(knobs={"trace.marker.opacity": 0.5}))
    assert "# --- MARK " in code
    for bucket in ("SCALE", "FRAME", "INTERACTION", "MOTION"):
        assert f"# --- {bucket} " not in code
    assert "update_layout()" not in code
    assert "update_traces()" not in code


def test_no_knobs_at_all_emits_no_bucket_sections():
    code = codegen.render(spec(knobs={}))
    assert "update_traces" not in code
    assert "update_layout" not in code
    for bucket in codegen.BUCKET_ORDER:
        assert f"# --- {bucket} " not in code


def test_every_section_carries_its_bucket_comment():
    code = codegen.render(spec(knobs={
        "trace.marker.opacity": 0.5, "layout.xaxis.type": "log",
        "layout.template": "plotly_dark", "layout.dragmode": "pan",
        "layout.transition.duration": 100,
    }))
    for line in code.splitlines():
        if line.startswith("fig.update_"):
            continue
        if line.startswith("# --- "):
            assert len(line) == codegen.HEADER_WIDTH, line


def test_headers_are_all_the_same_width():
    code = codegen.render(SPECS[-2][1])
    widths = {len(l) for l in code.splitlines() if l.startswith("# --- ")}
    assert widths == {codegen.HEADER_WIDTH}


def test_long_calls_wrap_one_argument_per_line():
    code = codegen.render(spec(knobs={
        f"layout.annotations{i}": f"a fairly long annotation value {i}" for i in range(8)
    }))
    assert "fig.update_layout(\n" in code
    assert all(len(l) < 200 for l in code.splitlines())


def test_registry_form_for_charts_with_no_px_route():
    code = codegen.render(spec(chart="sankey"))
    assert 'fig = bench.registry.build("sankey", df' in code
    assert "px.sankey" not in code


def test_px_form_for_charts_that_have_one():
    assert "fig = px.scatter_geo(df" in codegen.render(spec(chart="scatter_geo"))


def test_px_charts_can_be_adjusted_without_breaking_the_round_trip():
    """registry.py may edit PX_CHARTS; both forms still read back the same."""
    original = set(codegen.PX_CHARTS)
    try:
        codegen.PX_CHARTS.discard("bar")
        s = spec(chart="bar")
        assert 'bench.registry.build("bar"' in codegen.render(s)
        assert same(codegen.parse(codegen.render(s)), s)
        codegen.PX_CHARTS.add("bar")
        assert "px.bar(df" in codegen.render(s)
        assert same(codegen.parse(codegen.render(s)), s)
    finally:
        codegen.PX_CHARTS.clear()
        codegen.PX_CHARTS.update(original)


def test_custom_code_comes_back_untouched():
    """CUSTOM mode: the code panel holds the human's text, not ours."""
    typed = "df = whatever()\nfig = my_own_thing(df)\n"
    assert codegen.render(spec() | {"custom_code": typed}) == typed


# =====================================================================
# THE FORGIVING BITS - documented leniencies in parse
# =====================================================================


def test_parse_ignores_comments_entirely():
    canonical = codegen.render(spec(knobs={"layout.barmode": "group"}))
    stripped = "\n".join(l for l in canonical.splitlines() if not l.startswith("#"))
    assert same(codegen.parse(stripped), codegen.parse(canonical))


def test_parse_accepts_a_missing_fig_show():
    canonical = codegen.render(spec(knobs={"layout.barmode": "group"}))
    without = canonical.replace("fig.show()\n", "")
    assert same(codegen.parse(without), codegen.parse(canonical))


def test_parse_merges_split_bucket_calls():
    src = ('df = bench.data.frame({"kind": "demo", "name": "demo_1"})\n'
           'fig = px.bar(df, x="STATE", y="TOTAL")\n'
           'fig.update_layout(barmode="group")\n'
           'fig.update_layout(template="plotly_dark")\n'
           'fig.show()\n')
    got = codegen.parse(src)
    assert got is not None
    assert got["knobs"] == {"layout.barmode": "group", "layout.template": "plotly_dark"}


def test_a_later_keyword_wins():
    src = ('df = bench.data.frame({})\n'
           'fig = px.bar(df)\n'
           'fig.update_layout(barmode="group")\n'
           'fig.update_layout(barmode="stack")\n')
    assert codegen.parse(src)["knobs"] == {"layout.barmode": "stack"}


def test_parse_reads_a_tuple_as_a_list():
    src = ('df = bench.data.frame({})\n'
           'fig = px.bar(df)\n'
           'fig.update_layout(yaxis_range=(0, 100))\n')
    assert codegen.parse(src)["knobs"] == {"layout.yaxis.range": [0, 100]}


# =====================================================================
# BUCKET ASSIGNMENT
# =====================================================================


@pytest.mark.parametrize("path,bucket", [
    ("trace.x", "DATA"), ("trace.y", "DATA"), ("trace.z", "DATA"),
    ("trace.labels", "DATA"), ("trace.parents", "DATA"), ("trace.values", "DATA"),
    ("trace.marker.opacity", "MARK"), ("trace.line.dash", "MARK"),
    ("trace.fillcolor", "MARK"), ("trace.opacity", "MARK"),
    ("trace.orientation", "MARK"), ("trace.textposition", "MARK"),
    ("trace.hovertemplate", "MARK"),
    ("layout.xaxis.categoryorder", "SCALE"), ("layout.yaxis.range", "SCALE"),
    ("layout.xaxis2.type", "SCALE"), ("layout.coloraxis.cmid", "SCALE"),
    ("layout.colorway", "SCALE"), ("layout.piecolorway", "SCALE"),
    ("layout.polar.gridshape", "SCALE"), ("layout.geo.projection", "SCALE"),
    ("layout.scene.camera", "SCALE"), ("layout.ternary.sum", "SCALE"),
    ("layout.map.zoom", "SCALE"), ("layout.smith.bgcolor", "SCALE"),
    ("layout.title.text", "FRAME"), ("layout.legend.orientation", "FRAME"),
    ("layout.margin.l", "FRAME"), ("layout.font.size", "FRAME"),
    ("layout.annotations", "FRAME"), ("layout.shapes", "FRAME"),
    ("layout.images", "FRAME"), ("layout.paper_bgcolor", "FRAME"),
    ("layout.plot_bgcolor", "FRAME"), ("layout.width", "FRAME"),
    ("layout.height", "FRAME"), ("layout.template", "FRAME"),
    ("layout.showlegend", "FRAME"), ("layout.grid.rows", "FRAME"),
    ("layout.uniformtext.mode", "FRAME"),
    ("layout.hovermode", "INTERACTION"), ("layout.hoverlabel.font", "INTERACTION"),
    ("layout.clickmode", "INTERACTION"), ("layout.dragmode", "INTERACTION"),
    ("layout.selectdirection", "INTERACTION"), ("layout.modebar.remove", "INTERACTION"),
    ("layout.updatemenus", "INTERACTION"), ("layout.sliders", "INTERACTION"),
    ("layout.spikedistance", "INTERACTION"), ("layout.newshape.line", "INTERACTION"),
    ("layout.transition.duration", "MOTION"),
    # the deliberate catch-all
    ("layout.barmode", "FRAME"), ("layout.separators", "FRAME"),
    ("layout.uirevision", "FRAME"),
])
def test_bucket_assignment(path, bucket):
    assert codegen.bucket_for(path) == bucket


def test_bucket_for_rejects_an_unprefixed_path():
    with pytest.raises(ValueError):
        codegen.bucket_for("barmode")


def test_data_knobs_still_get_written_out():
    """A DATA path parked in `knobs` must not vanish. It rides with MARK."""
    s = spec(knobs={"trace.x": "STATE"})
    code = codegen.render(s)
    assert "fig.update_traces(x=\"STATE\")" in code
    assert same(codegen.parse(code), s)


# =====================================================================
# FLATTEN / UNFLATTEN
# =====================================================================


@pytest.mark.parametrize("path,keyword", [
    ("layout.barmode", "barmode"),
    ("layout.xaxis.categoryorder", "xaxis_categoryorder"),
    ("layout.xaxis.rangeslider.visible", "xaxis_rangeslider_visible"),
    ("layout.xaxis.title.font.size", "xaxis_title_font_size"),
    ("layout.paper_bgcolor", "paper_bgcolor"),
    ("layout.plot_bgcolor", "plot_bgcolor"),
    ("trace.marker.opacity", "marker_opacity"),
    ("trace.marker.colorbar.title.font.color", "marker_colorbar_title_font_color"),
    ("trace.error_y.visible", "error_y_visible"),
    ("trace.error_x.color", "error_x_color"),
    ("trace.contours.x.highlight", "contours_x_highlight"),
])
def test_flatten_and_back(path, keyword):
    assert codegen._flatten(path) == keyword
    assert codegen._unflatten(path.split(".")[0], keyword) == path


def test_render_refuses_a_path_it_could_not_read_back():
    """A made-up path that flattens ambiguously must fail loudly, not quietly."""
    with pytest.raises(ValueError):
        codegen.render(spec(knobs={"layout.paper.bgcolor": "#000"}))


def test_render_rejects_a_bad_prefix():
    with pytest.raises(ValueError):
        codegen.render(spec(knobs={"figure.barmode": "group"}))


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_render_rejects_non_finite_floats(value):
    with pytest.raises(ValueError):
        codegen.render(spec(knobs={"layout.height": value}))


@pytest.mark.parametrize("value", [{1, 2}, (1, 2), b"bytes", object(), 1j])
def test_render_rejects_non_json_values(value):
    with pytest.raises((TypeError, ValueError)):
        codegen.render(spec(knobs={"layout.height": value}))


def test_render_rejects_a_missing_chart():
    with pytest.raises(ValueError):
        codegen.render({"source": {}, "mapping": {}, "knobs": {}, "custom_code": None})


# =====================================================================
# MODULE BOUNDARIES - SPEC section 2
# =====================================================================


def test_codegen_imports_nothing_it_is_not_allowed_to():
    """SPEC 2: codegen.py must not import dash, snowflake or plotly."""
    tree = ast.parse(Path(codegen.__file__).read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for banned in ("dash", "plotly", "snowflake", "pandas", "numpy"):
        assert banned not in imported, f"codegen.py imports {banned}"
    assert imported <= {"ast", "math", "warnings", "typing", "__future__"}


def test_render_never_leaves_trailing_whitespace():
    for _, s in SPECS:
        for line in codegen.render(s).splitlines():
            assert line == line.rstrip(), repr(line)


def test_parse_stays_quiet_on_half_typed_code():
    """It runs on every keystroke. It must not spray warnings at the log."""
    import warnings as _w

    with _w.catch_warnings(record=True) as caught:
        _w.simplefilter("always")
        for src in ("0x", "1_", "x = 1if True else 2", "df = 077", "'\\d'"):
            assert codegen.parse(src) is None
    assert not caught, [str(c.message) for c in caught]


# =====================================================================
# THE MEASURED TABLES - do they still match the plotly that is installed?
# ---------------------------------------------------------------------
# These are the only tests here that need plotly. They exist so the two
# hardcoded tables in codegen.py cannot drift silently on an upgrade.
# =====================================================================

plotly = pytest.importorskip("plotly", reason="table guards need plotly installed")


def _walk_every_plotly_name():
    """Every property name in the library, and which ones open a sub-object."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import plotly.graph_objects as go

        names: set[str] = set()
        containers: set[str] = set()
        seen: set[type] = set()

        def walk(obj):
            cls = type(obj)
            if cls in seen:
                return
            seen.add(cls)
            try:
                props = obj._valid_props
            except Exception:
                return
            for p in sorted(props):
                names.add(p)
                try:
                    v = obj._get_validator(p)
                except Exception:
                    continue
                data_class = getattr(v, "data_class", None)
                if data_class is not None:
                    containers.add(p)
                    try:
                        walk(data_class())
                    except Exception:
                        pass

        walk(go.Layout())
        fig = go.Figure()
        for t in sorted(fig._data_validator.class_strs_map):
            try:
                walk(fig._data_validator.get_trace_class(t)())
            except Exception:
                pass
        walk(go.Frame())
        return names, containers


def test_underscore_table_still_matches_the_installed_plotly():
    names, _ = _walk_every_plotly_name()
    measured = {n for n in names if "_" in n}
    assert measured == set(codegen.UNDERSCORE_NAMES), (
        "bench/codegen.py UNDERSCORE_NAMES has drifted from the installed plotly. "
        f"missing={measured - set(codegen.UNDERSCORE_NAMES)} "
        f"stale={set(codegen.UNDERSCORE_NAMES) - measured}")


def test_underscore_split_is_unambiguous():
    """Greedy is only safe while no underscore name starts with a real name."""
    names, containers = _walk_every_plotly_name()
    for u in codegen.UNDERSCORE_NAMES:
        head = u.split("_")[0]
        assert head not in names, f"{u!r} is ambiguous: {head!r} is also a property"
        assert head not in containers
    for a in codegen.UNDERSCORE_NAMES:
        for b in codegen.UNDERSCORE_NAMES:
            assert a == b or not b.startswith(a + "_")


def test_every_real_plotly_path_survives_flatten_and_back():
    """The strongest version of the claim: walk the real tree and check it."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import plotly.graph_objects as go

        checked = 0
        seen: set[type] = set()

        def walk(obj, prefix):
            nonlocal checked
            cls = type(obj)
            if cls in seen:
                return
            seen.add(cls)
            try:
                props = obj._valid_props
            except Exception:
                return
            for p in sorted(props):
                path = f"{prefix}.{p}"
                assert codegen._unflatten(
                    path.split(".")[0], codegen._flatten(path)) == path, path
                checked += 1
                try:
                    v = obj._get_validator(p)
                except Exception:
                    continue
                data_class = getattr(v, "data_class", None)
                if data_class is not None:
                    try:
                        walk(data_class(), path)
                    except Exception:
                        pass

        walk(go.Layout(), "layout")
        fig = go.Figure()
        for t in sorted(fig._data_validator.class_strs_map):
            try:
                walk(fig._data_validator.get_trace_class(t)(), "trace")
            except Exception:
                pass
        assert checked > 800, f"only walked {checked} paths - the walk broke"


def test_px_chart_table_still_matches_the_installed_plotly():
    import inspect
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import plotly.express as px

        measured = {"imshow"}
        for name in dir(px):
            if name.startswith("_"):
                continue
            fn = getattr(px, name)
            if inspect.isfunction(fn) and "data_frame" in inspect.signature(fn).parameters:
                measured.add(name)
    assert measured == codegen.PX_CHARTS, (
        f"missing={measured - codegen.PX_CHARTS} stale={codegen.PX_CHARTS - measured}")


def test_every_px_chart_key_renders_as_a_px_call():
    for key in sorted(codegen.PX_CHARTS):
        code = codegen.render(spec(chart=key))
        assert f"fig = px.{key}(df" in code
        assert same(codegen.parse(code), spec(chart=key))


# =====================================================================
# THE px_charts PARAMETER - one call, no shared state
# =====================================================================


def test_px_charts_override_narrows_without_touching_the_module_set():
    """render(px_charts=...) decides the head for ONE call only."""
    before = set(codegen.PX_CHARTS)
    s = spec(chart="bar")

    narrowed = codegen.render(s, px_charts=frozenset())
    assert 'fig = bench.registry.build("bar", df' in narrowed

    widened = codegen.render(spec(chart="bar"), px_charts={"bar"})
    assert "fig = px.bar(df" in widened

    assert codegen.PX_CHARTS == before          # module set untouched
    assert same(codegen.parse(narrowed), s)     # both shapes still parse
    assert same(codegen.parse(widened), s)


def test_px_charts_none_keeps_the_default_behaviour():
    s = spec(chart="bar")
    assert codegen.render(s, px_charts=None) == codegen.render(s)


# =====================================================================
# parse_why - the reason that rides along with the None
# =====================================================================


def test_parse_why_succeeds_quietly_on_canonical_code():
    s = spec(knobs={"trace.marker.opacity": 0.5})
    got, why = codegen.parse_why(codegen.render(s))
    assert same(got, s)
    assert why == ""


def test_parse_why_names_the_line_of_a_stray_call():
    code = codegen.render(spec()) + "\nprint('hello')\n"
    got, why = codegen.parse_why(code)
    assert got is None
    assert why.startswith("line ") and "fig.show()" in why


def test_parse_why_names_the_line_of_a_syntax_error():
    got, why = codegen.parse_why("df = bench.data.frame({)\n")
    assert got is None
    assert why.startswith("line 1:")


def test_parse_why_explains_a_wrong_first_statement():
    got, why = codegen.parse_why("x = 1\nfig = px.bar(df)\n")
    assert got is None
    assert "df = " in why and "line 1:" in why


def test_parse_why_explains_kwargs_on_the_chart_call():
    got, why = codegen.parse_why(
        'df = bench.data.frame({"kind": "demo", "name": "d"})\n'
        "fig = px.bar(df, **extra)\n")
    assert got is None
    assert "**kwargs" in why


def test_parse_why_never_raises_on_garbage():
    for bad in (None, 123, "", "\x00", "import os", "fig.show()\nfig.show()"):
        got, why = codegen.parse_why(bad)  # type: ignore[arg-type]
        assert got is None
        assert isinstance(why, str) and why


def test_parse_still_returns_plain_none():
    assert codegen.parse("not code at all (") is None
