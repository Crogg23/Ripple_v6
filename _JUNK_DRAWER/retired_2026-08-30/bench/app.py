#!/usr/bin/env python
"""
THE BENCH - the three panes, wired together.

    python bench/app.py          then open http://127.0.0.1:8051

Left: every chart in bench/wall.py, grouped by the question it answers.
Middle: your chart, live, off demo data or a real warehouse query - and under
it, the Python that made it, editable. Right: every knob Plotly exposes for
that chart type, generated from Plotly's own validators.

This file owns nothing except the wiring. The five modules under it each own
one job, and none of them import Dash except controls.py, which has to,
because it returns components:

    knobs.py     Plotly's validators   -> a tiered tree of settings
    controls.py  one setting           -> one Dash control
    codegen.py   the state dict        <-> canonical Python source
    data.py      "where's the frame from?" - demo, or the guarded read lane,
                 and the cache in front of both (SPEC 7.1)
    registry.py  the 145 chart templates, and whether yours can be drawn

THE CALLBACKS, AND WHY EACH EXISTS
----------------------------------
    sync_spec      the ONE writer of the state object
    render_chart   the fast lane: figure, code, status, message, mode
    render_knobs   the slow lane: the right-hand pane
    render_picker  the 145 chart buttons, guarded by their own signature
    grow_open      which knob tiers are materialised - and, just as much,
                   which clicks are NOT asking for one (see its own note)
    source_face    demo box vs SQL box
    toggle_catalog / browse_catalog / pick_catalog_row / draft_starter
                   the catalog drawer - browse-first table discovery off a
                   disk snapshot; every warehouse touch is a labelled button
    (+ one clientside callback: the 600ms code debounce)

The first four used to be two. `render_all` had EIGHT Outputs off ONE Input,
and Dash returns a callback's outputs together - so the figure, which costs
1.3ms to build and 2.5 KB on the wire, could not appear until the knob pane
had finished. Measured: a chart click was 268ms and 4,128 KB, 94% of it the
pane. Splitting by cost is the fix, and it costs nothing in safety because
the three render lanes read the SPEC store and none of them writes it.

WHY THE TWO-WAY SYNC CANNOT LOOP - read this before you touch a callback
-----------------------------------------------------------------------
Turning a knob writes code. Editing the code moves the knobs. Written the
obvious way that is an infinite loop: the knob writes the code, the code write
looks like an edit, the edit writes the knob, forever. Three rules stop it, and
all three have to hold.

1. ONE WRITER. Exactly one callback (`sync_spec`) is allowed to write the SPEC
   store. Everything else reads it. Two callbacks that can both write the same
   store can always ping-pong; one callback cannot.

2. THE ECHO. The render lanes write what they put on screen into two "echo"
   stores - `render_chart` records the exact text it typed into the code box,
   `render_knobs` records the exact value it put in every knob widget. When
   `sync_spec` wakes up it compares what it was handed against those echoes.
   Identical means "this is my own writing coming back", and it stops there.
   Different means a human did it. Two stores and not one because the lanes
   fire together off the same store, and a shared echo would have them racing
   to overwrite each other's record of the screen.

3. THE FINAL DIFF. Even after all that, if the newly built SPEC is equal to the
   old one, nothing is written. A store that never changes fires nothing.

Rule 2 does the real work. Rules 1 and 3 are there so a bug in rule 2 is a
no-op instead of a runaway.

WHAT "CUSTOM MODE" IS
---------------------
SPEC section 1. Parsing arbitrary Python back into knob positions is not
solvable in general, so we do not pretend. Edit the code into something
`codegen.parse` does not recognise and the Bench drops into CUSTOM mode: the
chart still draws (we run the code), the knob panel greys out behind a one-line
banner, and Reset brings you back to the canonical form. That is the escape
hatch that stops this UI ever becoming a ceiling.

ONE HONEST WRINKLE, SAID OUT LOUD
---------------------------------
The canonical first line is `df = bench.data.frame({...})`, but the real
`bench.data.frame()` returns a PAIR - the frame, and the meta the status bar is
built from. So when CUSTOM mode runs your code, `bench.data.frame` in that
namespace is a thin shim handing back the frame alone. The snippet in the panel
is therefore true inside the Bench and one unpacking short of true in a plain
script. Better to say that than to quietly hand you a tuple.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import time
import traceback
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Anchor to the repo root so `python bench/app.py` works from anywhere.
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dash import (ALL, Dash, Input, Output, State, clientside_callback, ctx,  # noqa: E402
                  dcc, html, no_update)

from bench import codegen, controls, data, knobs, registry, settings  # noqa: E402


# =====================================================================
# THE LOOK
# ---------------------------------------------------------------------
# Borrowed wholesale from controls.py so the three panes match, and from
# wall.py's dark "wall" template, which importing bench.data already made
# the process-wide Plotly default.
# =====================================================================

SURFACE = controls.SURFACE
PANEL = controls.PANEL
PANEL_2 = controls.PANEL_2
INK = controls.INK
MUTED = controls.MUTED
FAINT = controls.FAINT
RULE = controls.RULE
ACCENT = controls.ACCENT
WARN = controls.WARN
GOOD = controls.GOOD
BAD = controls.BAD
MONO = controls.MONO
SANS = controls.SANS

_INPUT = {"background": SURFACE, "color": INK, "border": f"1px solid {RULE}",
          "borderRadius": "5px", "padding": "5px 8px", "font": f"12px {MONO}",
          "boxSizing": "border-box"}

# Secondary buttons sit on the raised BG_2 step with a real edge; the primary
# variant (save / RUN) is a filled accent block. Hover states live in
# assets/bench.css under .bench-btn / .bench-btn-primary.
_BTN = {"background": controls.BG_2, "color": INK,
        "border": f"1px solid {controls.RULE_STRONG}",
        "borderRadius": "5px", "padding": "5px 12px", "font": f"11px {MONO}",
        "letterSpacing": ".06em", "cursor": "pointer", "flex": "none"}

_BTN_PRIMARY = {**_BTN, "background": controls.ACCENT_FILL, "color": "#ffffff",
                "border": f"1px solid {controls.ACCENT_FILL}",
                "font": f"600 11px {MONO}"}

# How long the code panel waits after your last keystroke before it tries to
# read what you typed. SPEC section 8 asks for about this. The numbers live
# in bench/settings.py so an env var can tune them without an edit here.
DEBOUNCE_MS = settings.DEBOUNCE_MS

# How many rows the catalog drawer renders before asking you to narrow the
# filter. The list says when this cap trips, and by how much.
TABLE_CAP = settings.TABLE_CAP

# The colour of each lane badge. The badge is never allowed off the screen -
# you should never look at a number without knowing what guarded it.
LANE_COLOUR = {
    "enforced": GOOD,        # read-only proved server-side
    "client-guard": WARN,    # only this process stands between you and a write
    "demo": FAINT,           # generated here, nothing left the machine
    "refused": BAD,          # the guard said no
    "offline": BAD,
    "unknown": BAD,
    "idle": FAINT,           # restored SQL that has not run this session
}

LANE_MEANING = {
    "enforced": "read-only is enforced by the warehouse role, not by us",
    "client-guard": "read-only is enforced by this process ONLY - provision "
                    "SNOWFLAKE_SERVE_PAT to fix it",
    "demo": "fake data generated in this process; nothing left the machine",
    "refused": "the read guard refused this query",
    "offline": "no warehouse connection",
    "unknown": "the lane could not be determined",
    "idle": "restored SQL that has not run this session - press RUN to run it",
}

CUSTOM_BANNER = "custom code — knobs are read-only until you Reset"

# SPEC section 3 keeps the DATA bucket ("which column goes where") separate
# from the other five, because its legal values come from the data. Our
# mapping controls carry this prefix so one pattern callback can tell a
# mapping slot from a Plotly setting by looking at the path.
MAPPING_PREFIX = "mapping."


# =====================================================================
# THE STATE OBJECT
# ---------------------------------------------------------------------
# SPEC section 3. One dict, JSON-safe, living in a dcc.Store. Everything on
# screen is derived from it and nothing is derived from anything else.
# =====================================================================

START_CHART = "bar"
START_DEMO = "category"


def blank_spec(chart: str = START_CHART, demo: str = START_DEMO) -> dict:
    """A first SPEC that draws something the moment the page opens."""
    df, _meta = data.frame({"kind": "demo", "name": demo})
    return {
        "chart": chart,
        "source": {"kind": "demo", "name": demo},
        "mapping": registry.auto_map(df, registry.CHARTS[chart]),
        "knobs": {},
        "custom_code": None,
    }


# ---------------------------------------------------------------------
# The chart line: `px.bar(df, ...)` or `bench.registry.build("sankey", df, ...)`
# ---------------------------------------------------------------------
# codegen decides which by looking up the key in its own `PX_CHARTS` set,
# which ships holding the 40 measured Plotly Express functions. But only FOUR
# registry charts really are a bare px call - the other 141 have styling baked
# into their builder, so printing `px.violin(df, ...)` for them would be the
# panel telling you a line that does not make that picture. registry.PX_PURE
# is the honest set.
#
# We do NOT install it permanently. An earlier helper rewrote codegen's
# module-level set in place, and that leaked: the first run of this file turned
# two tests in tests/test_bench_codegen.py red, three files away, because they
# re-measure that same set. codegen.render's `px_charts` keyword narrows it for
# one call only, as a parameter - so there is no shared state to leak, and
# nothing to lock: no other thread can ever observe a value passed as an
# argument to a call it isn't part of.


def render_code(spec: dict) -> str:
    """`codegen.render`, with the chart line printed the way it was really built."""
    return codegen.render(spec, px_charts=registry.PX_PURE)


def _jsonable(value: Any) -> Any:
    """Make a value safe for a dcc.Store AND safe for codegen to write.

    Plotly's validators hand back tuples and numpy scalars. A dcc.Store would
    turn a tuple into a list behind our backs - so the echo comparison would
    quietly stop matching - and `codegen.render` refuses a tuple outright,
    because it only writes the JSON types. Normalising here keeps both honest.
    """
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return [_jsonable(v) for v in value.tolist()]
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (int, float)):
        return value
    return str(value)


# =====================================================================
# THE FRAME
# ---------------------------------------------------------------------
# Every repaint needs the DataFrame again, and without a cache that is a
# live Snowflake round trip per knob turn - a bare `SELECT 1` measured at
# 9.4s on this box. THE CACHE LIVES IN data.py (SPEC section 7.1), not
# here. app.py used to keep a second dict of its own in front of it; two
# caches over one seam is one cache too many, and the app's copy was the
# one that did not know how big a 100k-row result is, could not be told to
# refresh from anywhere else, and had no lock while the dev server serves
# on threads. So this is now a door, not a store.
#
# `copy=False` hands back the cached frame itself. That is exactly what the
# old dict did - it cached ONE copy and handed the same object out forever -
# so it is not a new risk, and every chart builder in registry.py copies
# before it mutates. The one caller that is allowed to mutate is CUSTOM
# code, and `run_custom` takes its own copy before it runs a line.
# =====================================================================


def get_frame(source: dict, refresh: bool = False) -> tuple[pd.DataFrame, dict]:
    """The DataFrame for a SPEC['source'], through bench.data and nothing else.

    `refresh=True` is what the RUN button passes: it drops the cached answer so
    the same SQL genuinely runs again. It has to be forwarded rather than
    handled here - `data.frame` is the only thing holding the entry now, so a
    RUN that does not pass this through is a RUN button that does nothing.
    """
    return data.frame(source or {}, refresh=refresh, copy=False)


def get_info(source: dict, refresh: bool = False) -> "data.FrameInfo":
    """Columns and column-roles for a source, worked out once per frame.

    The picker asks "what can this result draw?" on every repaint and the
    answer cannot have changed. `data.frame_info` keeps it with the frame.
    """
    return data.frame_info(source or {}, refresh=refresh)


def _columns(df: pd.DataFrame) -> list[str]:
    return [str(c) for c in df.columns]


# =====================================================================
# THE FIGURE
# =====================================================================


def message_figure(title: str, body: str = "") -> go.Figure:
    """An empty chart that explains itself - registry's, in the app's colours."""
    return registry.message_figure(title, body, width=74, color=MUTED, margin=True)


def _custom_namespace(df: pd.DataFrame) -> dict:
    """What custom code gets to see when we run it.

    `bench.data.frame` here hands back the frame alone - see the wrinkle in the
    module docstring. `bench.registry` is the real module, because
    `bench.registry.build(...)` is a line the code panel genuinely prints.
    """
    shim = SimpleNamespace(
        data=SimpleNamespace(frame=lambda source: get_frame(source)[0].copy()),
        registry=registry,
    )
    return {"bench": shim, "df": df, "px": px, "go": go, "pd": pd, "np": np,
            "make_subplots": make_subplots}


# How long custom code gets before we pull the plug. This is not a security
# boundary and is not pretending to be one - it is the thing that stops
# `while True:` in the code panel taking the whole app down with it.
CUSTOM_TIMEOUT_S = settings.CUSTOM_TIMEOUT_S


def _deadline_tracer(deadline: float):
    """A trace function that raises once the clock runs out.

    CPython fires a line event on a backwards jump, so this really does break
    a one-line `while True: pass` - checked, it stops on the nose. It costs
    about 0.15s on a normal chart build, which only ever happens in CUSTOM
    mode, so nobody pays for it while the knobs are driving.
    """
    def tracer(frame, event, arg):
        if time.monotonic() > deadline:
            raise TimeoutError(
                f"custom code ran for more than {CUSTOM_TIMEOUT_S:.0f}s and was "
                "stopped — an endless loop in the panel would take the app down")
        return tracer
    return tracer


def _needs_deadline(source: str) -> bool:
    """Does this code even contain something that can loop?

    The tracer above costs ~0.15s per build, and CUSTOM mode rebuilds on
    every 600ms debounce tick - so straight-line code (the overwhelmingly
    common case in the panel) skips the tracer entirely and pays nothing.
    Anything with a loop, a comprehension, or a function definition (which
    could recurse or hide a loop) keeps the full 5s guard.

    The one honest gap: loop-free code that recurses WITHOUT defining a
    function here (e.g. calling something recursive it built via exec) would
    escape. That needs exec-inside-exec to reach, and CPython's own recursion
    limit catches plain infinite recursion anyway.
    """
    try:
        parsed = ast.parse(source)
    except SyntaxError:
        return False        # it will not compile, so it cannot loop
    loopy = (ast.While, ast.For, ast.AsyncFor, ast.ListComp, ast.SetComp,
             ast.DictComp, ast.GeneratorExp, ast.FunctionDef,
             ast.AsyncFunctionDef, ast.Lambda)
    return any(isinstance(node, loopy) for node in ast.walk(parsed))


def run_custom(source: str, df: pd.DataFrame) -> tuple[go.Figure, str]:
    """Run the code in the panel and take whatever `fig` it left behind.

    This is CUSTOM mode's whole point: the UI must never stop you doing
    something Plotly can do. You typed the code, so we run it.

    Three things are held down while it runs:
      * `fig.show()` is neutered. The renderer on this machine is 'browser', so
        an unguarded show() would fling a new tab open every time you stop
        typing.
      * a five-second deadline, because the code panel re-runs itself 600ms
        after you stop typing and an endless loop would hang the server.
      * anything it raises becomes a figure printing the last traceback line,
        because an error you can read beats a dead pane.

    The frame is COPIED first. Everything else on the render path reads the
    cached frame in place (`data.frame(..., copy=False)`), which is safe
    because every builder in registry.py copies before it mutates - but this
    is the one place that runs code nobody has read, and `df["x"] = 0` in the
    panel must not be able to edit the cache underneath the next chart.
    """
    saved_show = go.Figure.show
    saved_trace = sys.gettrace()          # give it back - pytest/coverage use it
    go.Figure.show = lambda self, *a, **k: None  # type: ignore[assignment]
    namespace = _custom_namespace(df.copy())
    guard = _needs_deadline(source)
    try:
        if guard:
            sys.settrace(_deadline_tracer(time.monotonic() + CUSTOM_TIMEOUT_S))
        exec(compile(source, "<bench code panel>", "exec"), namespace)  # noqa: S102
    except KeyboardInterrupt:             # a real Ctrl-C is not "your code raised"
        raise
    except BaseException as exc:  # noqa: BLE001 - your code, your traceback
        line = traceback.format_exc().strip().splitlines()[-1]
        return (message_figure("custom code raised", line),
                f"custom code raised {type(exc).__name__}: {exc}")
    finally:
        if guard:
            sys.settrace(saved_trace)
        go.Figure.show = saved_show  # type: ignore[assignment]

    fig = namespace.get("fig")
    if not isinstance(fig, go.Figure):
        return (message_figure("custom code left no figure",
                               "The Bench draws whatever is in `fig` when your "
                               "code finishes. Assign one."),
                "custom code finished without leaving a `fig`")
    return fig, ""


def figure_for(spec: dict, df: pd.DataFrame, meta: dict) -> tuple[go.Figure, str]:
    """The chart this SPEC asks for, plus one line about anything that went wrong.

    Never raises. A chart that cannot be drawn says why - SPEC section 6's
    grey-out-with-a-reason rule, applied to the middle pane as well as to the
    picker.
    """
    if isinstance(spec.get("custom_code"), str):
        return run_custom(spec["custom_code"], df)

    key = spec.get("chart")
    template = registry.CHARTS.get(key)
    if template is None:
        return (message_figure(f"no chart called {key!r}",
                               "The code panel names a chart this registry does "
                               "not have. Pick one on the left."),
                f"unknown chart key {key!r}")

    if not meta.get("ok"):
        return (message_figure("no data", str(meta.get("error", "unknown"))),
                str(meta.get("error", "")))

    try:
        fig = template.builder(df, spec.get("mapping") or {}, spec.get("knobs") or {})
    except Exception as exc:  # noqa: BLE001 - a missing slot is a message
        _ok, why = registry.drawable(df, template)
        if template.missing(spec.get("mapping") or {}):
            # An empty required slot. `why` is ALREADY the sentence SPEC
            # section 6 asks for - the chart, what it needs, and what this
            # result actually has - and the builder's own "still needs" error
            # says the same thing in different words. Printing both made the
            # reader read the chart's name three times in a row. Say it once.
            return message_figure("cannot draw this yet", why), why
        # Slots are all filled and it still blew up. That is news, so the
        # exception goes on screen next to what we thought the data could do.
        return (message_figure(f"{template.name} could not be drawn",
                               f"{exc}   {why}"),
                f"{template.name}: {exc}")

    # ATLAS section 4.1's honourable mention: a constant uirevision means your
    # zoom survives a redraw. Only set it if you have not claimed that knob.
    if "layout.uirevision" not in (spec.get("knobs") or {}):
        fig.update_layout(uirevision=key)
    return fig, ""


# =====================================================================
# THE LEFT PANE - the picker
# =====================================================================


def picker(spec: dict, df: pd.DataFrame, query: str = "",
           roles: dict | None = None) -> html.Div:
    """All 145 charts, grouped by the question they answer.

    A chart this result cannot draw is dimmed - and its tooltip is the reason,
    in a sentence, because "Sankey diagram needs a source column, a target
    column and a value column - this result has one category column and one
    number" teaches more than a greyed-out button (SPEC section 6).

    `roles` is `registry.roles(df)`, which is a pure function of the frame and
    costs 4.1ms on a 100k-row result. Pass `data.frame_info(source).chart_roles`
    and it is worked out once per frame instead of once per repaint; leave it
    out and we derive it here, which is what every test and self-test does.
    """
    hits = {t.key for t in registry.search(query)} if (query or "").strip() else None
    if roles is None:
        roles = registry.roles(df) if len(df.columns) else {}
    df_roles = roles
    chosen = spec.get("chart")

    out: list = []
    shown = 0
    for section, question in registry.SECTIONS:
        rows: list = []
        for template in registry.BY_SECTION[section]:
            if hits is not None and template.key not in hits:
                continue
            ok, why = registry.drawable(df_roles, template) if df_roles else (True, "")
            selected = template.key == chosen
            shown += 1
            rows.append(html.Button(
                [
                    html.Span(template.name,
                              style={"font": f"{'600 ' if selected else ''}12px {SANS}"}),
                    html.Div(template.key,
                             style={"font": f"10px {MONO}", "color": FAINT,
                                    "marginTop": "1px"}),
                ],
                id={"bench": "chart", "key": template.key},
                n_clicks=0,
                title=why,
                style={
                    "display": "block", "width": "100%", "textAlign": "left",
                    "background": PANEL_2 if selected else "transparent",
                    "color": INK if (ok and not template.blocked) else FAINT,
                    "border": "none",
                    "borderLeft": f"3px solid {ACCENT if selected else 'transparent'}",
                    "borderRadius": "4px", "padding": "5px 8px",
                    "margin": "1px 0", "cursor": "pointer",
                    "opacity": "1" if ok else "0.55",
                },
            ))
        if not rows:
            continue
        out.append(html.Details(
            [
                html.Summary(
                    [
                        html.Span(section, style={"font": f"600 11.5px {SANS}",
                                                  "letterSpacing": ".08em"}),
                        html.Span(f"  {question}",
                                  style={"font": f"11px {SANS}", "color": FAINT,
                                         "marginLeft": "6px"}),
                    ],
                    style={"cursor": "pointer", "padding": "6px 2px",
                           "listStyle": "revert", "color": INK},
                ),
                html.Div(rows, style={"paddingLeft": "4px"}),
            ],
            open=bool((query or "").strip())
            or any(t.key == chosen for t in registry.BY_SECTION[section]),
            style={"borderTop": f"1px solid {RULE}"},
        ))

    header = html.Div(
        f"{shown} of {len(registry.TEMPLATES)} charts"
        + ("" if (query or "").strip() else " — dimmed ones say why in their tooltip"),
        style={"font": f"11px {SANS}", "color": FAINT, "margin": "0 0 6px"},
    )
    return html.Div([header, *out])


# =====================================================================
# THE RIGHT PANE - mapping slots on top, then the generated knob tree
# ---------------------------------------------------------------------
# One deliberate swap, and it is a decision rather than an omission.
#
# knobs.py fills the DATA bucket with every DataArrayValidator it finds -
# `trace.x`, but also `error_y.array`, `colorbar.ticktext` and `cells.format`.
# Those are not what "which column goes where" means, and binding a column
# name to `trace.x` through update_traces would set x to the six letters of
# the column name rather than to the column. So the DATA bucket you see is
# the chart template's OWN mapping slots - the thing registry.py can actually
# build from, and the thing the grey-out reason is written against. The
# advanced array bindings are out of v1.
# =====================================================================


def mapping_knobs(template: registry.ChartTemplate, columns: list[str]) -> list:
    """One column picker per slot the chosen chart declares.

    `required` first, then `optional`. The description is the slot's own
    plain-English `says` line - the same wording the grey-out reason uses, so
    the two can never disagree.
    """
    out = []
    for required, slots in ((True, template.required), (False, template.optional)):
        for slot in slots:
            out.append(controls.Knob(
                path=f"{MAPPING_PREFIX}{slot.name}",
                label=slot.name,
                # a `many` slot takes a LIST of columns, so it needs the
                # multi-select, not the single dropdown
                control="multi" if slot.many else "column",
                options=tuple(columns),
                description=("required — " if required else "optional — ")
                + slot.says
                + (f" (pick {slot.min_n} or more)" if slot.many else ""),
                depth=1,
            ))
    return out


def knob_tree(spec: dict, columns: list[str]) -> dict:
    """knobs.tree() with the DATA bucket swapped for the mapping slots."""
    template = registry.CHARTS.get(spec.get("chart"))
    if template is None:
        return {b: {t: [] for t in knobs.TIERS} for b in knobs.BUCKETS}
    tree = knobs.tree(spec["chart"], columns)
    tree[knobs.DATA] = {0: mapping_knobs(template, columns), 1: [], 2: []}
    return tree


@lru_cache(maxsize=16)
def _knob_index(chart: str, columns: tuple[str, ...]) -> dict[str, Any]:
    """{path: Knob} for one chart, so a callback can look one up in O(1).

    Cached because `sync_spec` needs the real Knob to coerce a widget's value
    (a multi-select hands back a list where a Plotly flaglist wants 'x+y+text',
    and only the Knob knows which is which), and rebuilding ~2,000 of them on
    every keystroke would be silly. knobs.py caches the underlying walk too, so
    a miss here is milliseconds, not seconds.
    """
    return {k.path: k for k in knobs.flat(chart, list(columns))}


def shown_values(spec: dict) -> dict:
    """Every value the pane has to display, keyed the way the widgets are.

    SPEC section 3 keeps the mapping in its own dict, but as far as controls.py
    is concerned a mapping slot is just another knob, and its widget id is
    `mapping.<slot>`. So the mapping is folded in here under that same prefix.

    THIS IS NOT COSMETIC. `controls._value_for` only reaches into `mapping` for
    a knob it drew as a single-column dropdown, and a `many` slot - the column
    LIST a correlation matrix, a splom, a treemap path or a table wants - is
    drawn as a multi-select instead. Without this it read `spec["knobs"]`,
    found nothing, and rendered empty: 17 of the 145 charts showed you an empty
    REQUIRED slot while drawing perfectly from five columns, and the first
    column you then picked replaced all five.

    Keying by the full dotted path also means no Plotly knob can ever collide
    with a slot name. `controls._value_for` matches a column dropdown on the
    LAST path segment, and 45 real Plotly paths end in one - `trace.values`,
    `trace.open`, `trace.color`, `trace.lat`. They are all in the DATA bucket
    that `knob_tree` replaces, so none of them is on screen today, but keying
    on the whole path is what keeps that true tomorrow.
    """
    out = dict(spec.get("knobs") or {})
    for slot, value in (spec.get("mapping") or {}).items():
        out[f"{MAPPING_PREFIX}{slot}"] = value
    return out


# Every bucket, every tier, materialised. This is what `lazy=False` used to
# build on every single repaint; it is now what you get only after clicking
# "show everything" on all six buckets. Kept as a named constant because the
# test harnesses drive it - a pretend browser with the whole panel open.
ALL_TIERS_OPEN: tuple[str, ...] = tuple(
    controls.open_token(bucket, tier)
    for bucket in controls.BUCKET_ORDER for tier in (1, 2)
)


def knob_pane(spec: dict, columns: list[str], query: str = "",
              opened: Any = ()):
    """The whole right-hand pane, built by controls.py from the generated tree.

    `opened` is the set of "MARK:1"-shaped tokens naming the tiers that are
    materialised right now. Empty - the first paint - means Tier 0 and nothing
    else: 39 knob rows and 87 KB instead of 1,895 rows and 3,808 KB, measured
    on `bar`. Tier 1 and Tier 2 are not hidden, they are ABSENT, which is the
    whole point: a knob behind a shut <details> is still serialised, still
    shipped, and still turns up in every pattern-matching Input payload.

    A SEARCH ignores `opened` entirely - controls.accordion reads the tree, not
    the components, so every tier of every bucket is reachable from the box.
    """
    custom = isinstance(spec.get("custom_code"), str)
    body = controls.accordion(
        knob_tree(spec, columns),
        shown_values(spec),
        mapping=dict(spec.get("mapping") or {}),
        query=query or "",
        disabled=custom,
        lazy=True,
        opened=opened or (),
    )
    if not custom:
        return body
    return html.Div([
        html.Div(CUSTOM_BANNER,
                 style={"font": f"12px {SANS}", "color": WARN,
                        "background": "rgba(201,133,0,.10)",
                        "border": f"1px solid {WARN}", "borderRadius": "5px",
                        "padding": "7px 9px", "margin": "0 0 8px"}),
        body,
    ])


# =====================================================================
# WHICH TIERS ARE OPEN
# ---------------------------------------------------------------------
# One `dcc.Store` holds the token set - "MARK:1", "SCALE:2" - naming the
# tiers that are materialised right now, plus the PANE it belongs to.
#
# The pane key is what makes the set self-expiring with ONE writer. Clicking
# a new chart, or dropping in or out of CUSTOM, builds a different pane, and
# tokens from the old one should not silently re-inflate it. The obvious fix
# is a second callback that resets the store - but then two callbacks write
# one store and can race. So staleness is decided when the set is READ: a
# token set stamped with a different key is simply not this pane's, and reads
# as empty. `grow_open` stays the only writer.
# =====================================================================


def open_key(spec: dict) -> str:
    """Which pane an open-token set belongs to.

    Chart and CUSTOM only. A column change rebuilds the DATA dropdowns but
    not the tiers, so re-collapsing the panel because a query returned a
    different column would be a rebuild the human did not ask for.
    """
    return json.dumps([spec.get("chart"),
                       isinstance(spec.get("custom_code"), str)], default=str)


def open_tokens(store: Any, key: str) -> tuple[str, ...]:
    """The open tokens this pane is entitled to. Anything else reads empty."""
    if not isinstance(store, dict) or store.get("key") != key:
        return ()
    return tuple(str(t) for t in (store.get("tokens") or ()))


def materialisable(spec: dict) -> set[str] | None:
    """The open tokens that would really put something new on this pane.

    A token names a bucket's TIER. A tier with no knobs in it has nothing to
    materialise, so a token for it is never a request - it is a click that
    landed somewhere in the bucket's body and bubbled up.

    THIS IS NOT AN OPTIMISATION, IT IS THE FIX FOR A CLICK THAT GOT EATEN.
    `html.Details` renders `<details onClick={n_clicks + 1}>` and React's
    onClick bubbles, so clicking the `mapping.x` dropdown fires n_clicks on
    the DATA bucket that contains it. DATA is the one bucket open on a first
    paint, and `knob_tree` gives it tiers 1 and 2 of exactly zero knobs - so
    that click used to add "DATA:1", change `bench-open`, and rebuild a pane
    that came back with the SAME 70 widgets and the SAME values, replacing
    the dropdown whose menu had just opened. Measured: 314 components and
    81.6 KB in, 314 components and 81.6 KB out. The menu shut, the click did
    nothing, and the second click worked - which is exactly what "you can't
    tell if it's broken" feels like.

    Returns None when the tree cannot be built, meaning "no opinion" - a
    click is then treated the way it always was rather than being swallowed
    by a helper that failed.
    """
    try:
        return _materialisable(str(spec.get("chart")))
    except Exception:  # noqa: BLE001 - a filter that fails must not filter
        return None


@lru_cache(maxsize=64)
def _materialisable(chart: str) -> frozenset[str]:
    """Which bucket tiers hold knobs for one chart. Cached, and per CHART only.

    Which tier a knob lands in is decided by its path, its bucket and its
    depth - `knobs.tier_for` - and none of those is a fact about the data. So
    the columns do not belong in this answer and are not asked for, which
    keeps a bucket click off the frame path entirely.

    DATA is subtracted rather than counted: `knob_tree` throws Plotly's DATA
    bucket away and puts the chart's own mapping slots at Tier 0 with nothing
    behind them, so DATA's deeper tiers cannot be materialised by anything.
    """
    tree = knobs.tree(chart, [])
    return frozenset(
        controls.open_token(bucket, tier)
        for bucket, tiers in tree.items() if bucket != knobs.DATA
        for tier in (1, 2) if (tiers or {}).get(tier))


# =====================================================================
# THE ECHO
# ---------------------------------------------------------------------
# Rule 2 of the no-loop contract. After building the knob pane we walk the
# component tree we just built and write down the value we put in every
# widget. When a knob callback fires, anything still equal to what we wrote
# is our own writing coming back, and is ignored.
#
# It is done by READING the components rather than by re-deriving the values,
# so it cannot drift from what controls.py actually rendered.
# =====================================================================


def echo_key(path: str, part: str) -> str:
    return f"{part}|{path}"


def knob_values_signature(spec: dict) -> str:
    """Everything the knob WIDGETS display, as one comparable string.

    This is how `render_knobs` tells the two cases apart without being told:

      * a knob was turned  -> `sync_spec` has already stamped this signature
        into the echo, so the two match and the pane is left alone. The widget
        you are holding does not get yanked out from under you, which is
        SPEC section 8's rule 2.
      * the CODE was edited -> nothing stamped it, so the signatures differ and
        the pane is rebuilt with the knobs in their new positions, which is
        SPEC section 10's rule 5.
    """
    return json.dumps({"knobs": spec.get("knobs") or {},
                       "mapping": spec.get("mapping") or {}}, sort_keys=True,
                      default=str)


def knob_echo(component) -> dict[str, Any]:
    """{part|path: the value we just put in that widget}."""
    out: dict[str, Any] = {}
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob":
            out[echo_key(str(cid.get("path")), str(cid.get("part")))] = _jsonable(
                getattr(node, "value", None))
    return out


# =====================================================================
# THE SOURCE BAR + STATUS
# =====================================================================


def status_bar(meta: dict) -> list:
    """Lane badge, row count, truncation warning and data-as-of.

    SPEC section 8 calls these non-negotiable, so they are rebuilt from `meta`
    on every single render and there is no branch that can leave one out.
    """
    lane = str(meta.get("lane") or "unknown")
    rows = int(meta.get("rows") or 0)
    as_of = meta.get("as_of")

    # SPEC section 7.1: a cached hit reports the ORIGINAL elapsed_s, so the
    # chip has to say which it is. Printing "0.00s" for a query that did not
    # run - or printing 9.40s as if it had just been paid again - are both the
    # status bar lying about the warehouse, and this is the one bar that is
    # never allowed off the screen.
    took = float(meta.get("elapsed_s") or 0)
    cached = bool(meta.get("cached"))
    age = float(meta.get("cache_age_s") or 0)
    took_why = ("that is what the ORIGINAL fetch took - this frame came out of "
                f"the cache {age:,.0f}s ago and nothing was re-queried. Press RUN "
                "to run it again." if cached
                else "how long this frame took to arrive")

    chips = [
        _chip("lane", lane, LANE_COLOUR.get(lane, BAD), LANE_MEANING.get(lane, "")),
        _chip("rows", f"{rows:,}", INK if rows else WARN,
              "rows in the frame this chart is drawn from"),
        _chip("data as of", str(as_of) if as_of else "unknown",
              INK if as_of else WARN,
              "the vintage stamp, or unknown when nothing in the result proved one"),
        _chip("took", f"{took:.2f}s" + (" · cached" if cached else ""),
              FAINT if cached else MUTED, took_why),
    ]
    if meta.get("truncated"):
        chips.append(_chip("TRUNCATED", f"cut at {rows:,} rows", BAD,
                           "this chart is showing a slice, not the whole answer"))
    if not meta.get("ok"):
        chips.append(_chip("error", str(meta.get("error", ""))[:80], BAD,
                           str(meta.get("error", ""))))
    return chips


# A semantic chip colour gets its own dark tint behind it, so the state
# reads as a coloured object across the room instead of 11px coloured text.
_CHIP_TINT = {GOOD: controls.GOOD_BG, BAD: controls.BAD_BG,
              WARN: controls.WARN_BG, ACCENT: controls.ACCENT_BG}


def _chip(label: str, value: str, colour: str, title: str):
    tint = _CHIP_TINT.get(colour)
    return html.Div(
        [
            html.Span(label + " ", style={"color": FAINT, "font": f"10px {MONO}",
                                          "letterSpacing": ".06em"}),
            html.Span(value, style={"color": colour, "font": f"600 11px {MONO}"}),
        ],
        title=title,
        style={"border": f"1px solid {colour if tint else RULE}",
               "background": tint or "transparent",
               "borderRadius": "4px", "padding": "3px 8px",
               "whiteSpace": "nowrap"},
    )


def source_bar(spec: dict, meta: dict) -> html.Div:
    """demo dropdown | SQL box + RUN, and the badges that are always on screen."""
    source = spec.get("source") or {}
    kind = source.get("kind", "demo")
    catalogue = data.demo_catalogue()
    return html.Div(
        [
            html.Div(
                [
                    dcc.RadioItems(
                        id="bench-src-kind",
                        options=[{"label": "demo", "value": "demo"},
                                 {"label": "warehouse SQL", "value": "warehouse"}],
                        value=kind, inline=True,
                        inputStyle={"marginRight": "5px", "accentColor": ACCENT},
                        labelStyle={"marginRight": "14px", "color": INK,
                                    "cursor": "pointer"},
                        style={"font": f"12px {SANS}", "flex": "none"},
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id="bench-src-demo",
                            options=[{"label": f"{c['label']}  ·  {c['rows']:,} rows  "
                                               f"·  {', '.join(c['columns'][:5])}",
                                      "value": c["name"]} for c in catalogue],
                            value=source.get("name", START_DEMO),
                            clearable=False, className="bench-dd",
                            style={"font": f"12px {MONO}"},
                        ),
                        id="bench-src-demo-box",
                        style={"flex": "1", "minWidth": "0"},
                    ),
                    html.Div(
                        [
                            html.Button("browse catalog", id="bench-cat-open",
                                        n_clicks=0, style=_BTN,
                                        className="bench-btn",
                                        title="browse the local catalog snapshot — "
                                              "reads a file on disk, never touches "
                                              "the warehouse"),
                            html.Button("draft starter SQL", id="bench-src-draft",
                                        n_clicks=0, style=_BTN,
                                        className="bench-btn",
                                        title="types the picked table's columns by "
                                              "profiling 10,000 rows IN THE WAREHOUSE "
                                              "(cached 7 days) — the only cost here "
                                              "besides RUN"),
                            html.Div(style={"flex": "1"}),
                            html.Button("RUN", id="bench-src-run", n_clicks=0,
                                        style=_BTN_PRIMARY,
                                        className="bench-btn-primary"),
                        ],
                        id="bench-src-sql-tools",
                        style={"display": "none", "gap": "6px", "flex": "1",
                               "alignItems": "center", "minWidth": "0"},
                    ),
                    html.Div(status_bar(meta), id="bench-status",
                             style={"display": "flex", "gap": "6px",
                                    "alignItems": "center", "flex": "none"}),
                ],
                style={"display": "flex", "gap": "10px", "alignItems": "center"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(id="bench-cat-domain", options=[],
                                         placeholder="all domains",
                                         clearable=True, className="bench-dd",
                                         style={"font": f"12px {MONO}",
                                                "width": "300px"}),
                            dcc.Input(id="bench-cat-filter", type="search",
                                      placeholder="filter by name…",
                                      debounce=True,
                                      style={**_INPUT, "width": "200px",
                                             "flex": "none"}),
                            html.Span(id="bench-cat-age",
                                      style={"font": f"11px {SANS}",
                                             "color": FAINT, "flex": "1"}),
                            html.Button("refresh catalog", id="bench-cat-refresh",
                                        n_clicks=0, style=_BTN,
                                        className="bench-btn",
                                        title="rebuilds the local snapshot: 2 "
                                              "warehouse queries, ~10s if the "
                                              "warehouse is cold — the only thing "
                                              "browsing ever costs"),
                        ],
                        style={"display": "flex", "gap": "8px",
                               "alignItems": "center"},
                    ),
                    html.Div(id="bench-cat-list",
                             style={"maxHeight": "280px", "overflowY": "auto",
                                    "marginTop": "8px"}),
                ],
                id="bench-cat-drawer",
                style={"display": "none", "marginTop": "8px",
                       "padding": "10px", "background": PANEL_2,
                       "border": f"1px solid {RULE}", "borderRadius": "6px"},
            ),
            dcc.Store(id="bench-cat-picked", data=None),
            dcc.Textarea(
                id="bench-src-sql",
                value=source.get("sql", ""),
                spellCheck=False,
                placeholder="SELECT ...  — runs through viz.sqlrun, the one guarded "
                            "read lane. Claim tables stay refused.",
                style={**_INPUT, "display": "none", "width": "100%",
                       "height": "72px", "marginTop": "8px", "resize": "vertical"},
            ),
            html.Div(id="bench-src-cols",
                     style={"display": "flex", "flexWrap": "wrap", "gap": "4px",
                            "marginTop": "6px"}),
            html.Div(id="bench-src-note",
                     style={"font": f"11px {SANS}", "color": MUTED,
                            "marginTop": "6px"}),
        ],
        style={"background": PANEL,
               "borderTop": f"1px solid {controls.RULE_STRONG}",
               "padding": "8px 12px", "flex": "none"},
    )


# =====================================================================
# THE APP
# =====================================================================

app = Dash(__name__, title="The Bench", suppress_callback_exceptions=True,
           update_title=None)

# The inlined <style> is only the generated :root{--bench-*} variables plus
# the page reset; every selector lives in assets/bench.css, which Dash
# auto-loads and which resolves against these variables. dcc.Dropdown is why
# the stylesheet is not decoration: it renders its own markup that a
# `style=` dict cannot reach - without bench.css the open menus are white
# boxes on a dark pane.
app.index_string = (
    "<!DOCTYPE html><html><head>{%metas%}<title>{%title%}</title>"
    "{%favicon%}{%css%}<style>"
    + controls.css_vars()
    + "html,body{margin:0;padding:0;background:" + SURFACE + ";height:100%;}"
    "#react-entry-point{height:100%;}"
    "</style></head><body>{%app_entry%}<footer>{%config%}{%scripts%}"
    "{%renderer%}</footer>"
    # Keyboard shortcuts: synthesised clicks on buttons that already exist,
    # so there is no second server surface to keep in step. Ctrl+Z/Y stay
    # native inside text boxes - hijacking undo in a textarea is hostile.
    + """<script>
document.addEventListener('keydown', function (e) {
  var click = function (id) {
    var el = document.getElementById(id); if (el) { el.click(); } };
  var mod = e.ctrlKey || e.metaKey;
  if (!mod) { return; }
  var tag = (document.activeElement || {}).tagName || '';
  var typing = tag === 'TEXTAREA' || tag === 'INPUT';
  var key = (e.key || '').toLowerCase();
  if (key === 's') { e.preventDefault(); click('bench-save'); }
  else if (key === 'enter' &&
           (document.activeElement || {}).id === 'bench-src-sql') {
    click('bench-src-run');
  }
  else if (!typing && key === 'z' && !e.shiftKey) {
    e.preventDefault(); click('bench-undo');
  }
  else if (!typing && (key === 'y' || (key === 'z' && e.shiftKey))) {
    e.preventDefault(); click('bench-redo');
  }
});
</script></body></html>"""
)

_START = blank_spec()
_START_DF, _START_META = get_frame(_START["source"])
_START_PANE = knob_pane(_START, _columns(_START_DF))
_START_CODE = render_code(_START)

_PANE = {"height": "100%", "overflowY": "auto", "boxSizing": "border-box",
         "background": PANEL, "color": INK}

# How long a repaint is allowed to look like nothing before we say we are
# working. Under this it is a flicker and the spinner is the annoyance; over
# it, silence reads as broken. The brief's number, and it is the right one.
SPINNER_MS = settings.SPINNER_MS


def _loading(child, ident: str, **kw):
    """One spinner, the same one everywhere. Nothing here changes the layout.

    `overlay_style` keeps the old content on screen and dims it, so a slow
    repaint reads as "this is being replaced" rather than as a blank hole.
    """
    return dcc.Loading(
        child, id=ident, type="dot", color=ACCENT,
        delay_show=SPINNER_MS, delay_hide=0,
        overlay_style={"visibility": "visible", "opacity": 0.35,
                       "transition": "opacity .15s ease-in"},
        **kw,
    )


app.layout = html.Div(
    [
        # --- state -------------------------------------------------------
        dcc.Store(id="bench-spec", data=_START),
        # Rule 2 of the no-loop contract: what we last put on screen. TWO
        # stores, one per render lane, and that split is load-bearing rather
        # than tidy - `render_chart` and `render_knobs` fire from the same
        # Input at the same moment, so a single store would have two writers
        # racing and whichever answered last would erase the other's echo.
        # One store, one writer.
        dcc.Store(id="bench-echo", data={"code": _START_CODE}),
        dcc.Store(id="bench-knob-echo",
                  data={"knobs": knob_echo(_START_PANE), "sig": None,
                        "vals": None}),
        # which knob tiers are materialised - see `open_key` / `grow_open`
        dcc.Store(id="bench-open", data={}),
        # what the picker was last drawn from, so a knob turn does not ship
        # 145 chart buttons again for no reason
        dcc.Store(id="bench-picker-sig"),
        # the debounced code text - written from the browser, never typed into
        dcc.Store(id="bench-code-draft"),
        dcc.Store(id="bench-debounce-sink"),
        # undo/redo: past and future specs, written only by sync_spec
        dcc.Store(id="bench-history", data={"past": [], "future": []}),
        # the localStorage mirror of the spec, so F5 comes back here. Written
        # only by sync_spec; read once per page load by the restore below.
        dcc.Store(id="bench-persist", storage_type="local"),
        # the one-shot restore request: a clientside callback copies persist
        # into here exactly once per page load, and sync_spec adopts it. The
        # indirection is what keeps sync_spec the single writer of the spec.
        dcc.Store(id="bench-restore-req"),

        # --- three panes -------------------------------------------------
        html.Div(
            [
                # LEFT - the picker
                html.Div(
                    [
                        html.Div([html.Span("RIPPLE · ", style={"color": FAINT}),
                                  html.B("THE BENCH", style={"color": INK})],
                                 style={"font": f"11px {MONO}",
                                        "letterSpacing": ".2em",
                                        "padding": "10px 12px 6px"}),
                        html.Div(
                            dcc.Input(id="bench-picker-search", type="search",
                                      placeholder="search every chart…",
                                      debounce=300,
                                      style={**_INPUT, "width": "100%",
                                             "font": f"12.5px {SANS}"}),
                            style={"padding": "0 12px 8px"}),
                        html.Div(picker(_START, _START_DF), id="bench-picker",
                                 style={"padding": "0 8px 40px"}),
                    ],
                    style={**_PANE,
                           "borderRight": f"1px solid {controls.RULE_STRONG}"},
                ),
                # MIDDLE - the chart, then the code
                html.Div(
                    [
                        html.Div(
                            _loading(
                                dcc.Graph(id="bench-figure", figure=go.Figure(),
                                          style={"height": "100%"},
                                          config={"displaylogo": False,
                                                  "responsive": True,
                                                  # the modebar camera saves a
                                                  # real PNG at 2x - no kaleido,
                                                  # the browser does the work
                                                  "toImageButtonOptions": {
                                                      "format": "png",
                                                      "scale": 2,
                                                      "filename": "bench-chart",
                                                  }}),
                                "bench-figure-loading",
                                parent_style={"height": "100%"},
                                style={"height": "100%"}),
                            style={"flex": "1", "minHeight": "0",
                                   "padding": "8px 10px 0"},
                        ),
                        html.Div(id="bench-build-msg",
                                 style={"font": f"11.5px {SANS}", "color": WARN,
                                        "padding": "0 12px", "minHeight": "17px"}),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span("CODE",
                                                  style={"font": f"10px {MONO}",
                                                         "letterSpacing": ".14em",
                                                         "color": FAINT}),
                                        html.Span(id="bench-code-mode",
                                                  style={"font": f"11px {MONO}",
                                                         "marginLeft": "10px"}),
                                        html.Div(style={"flex": "1"}),
                                        html.Button("↶", id="bench-undo",
                                                    n_clicks=0, style=_BTN,
                                                    className="bench-btn",
                                                    title="undo (Ctrl+Z outside "
                                                          "a text box)"),
                                        html.Button("↷", id="bench-redo",
                                                    n_clicks=0, style=_BTN,
                                                    className="bench-btn",
                                                    title="redo (Ctrl+Y)"),
                                        html.Button("save", id="bench-save",
                                                    n_clicks=0,
                                                    style=_BTN_PRIMARY,
                                                    className="bench-btn-primary",
                                                    title="download this whole "
                                                          "setup as a .json spec "
                                                          "(Ctrl+S)"),
                                        dcc.Upload(
                                            html.Button("load", style=_BTN,
                                                        className="bench-btn",
                                                        title="load a saved "
                                                              ".json spec"),
                                            id="bench-load", multiple=False,
                                            accept=".json,application/json"),
                                        dcc.Clipboard(
                                            target_id="bench-code",
                                            title="copy the code",
                                            style={"color": FAINT,
                                                   "fontSize": "13px",
                                                   "cursor": "pointer"}),
                                        html.Button(".py", id="bench-export-py",
                                                    n_clicks=0, style=_BTN,
                                                    className="bench-btn",
                                                    title="download this code as a "
                                                          "runnable .py file"),
                                        html.Button("html", id="bench-export-html",
                                                    n_clicks=0, style=_BTN,
                                                    className="bench-btn",
                                                    title="download the chart as a "
                                                          "standalone interactive "
                                                          "HTML file"),
                                        dcc.Download(id="bench-download"),
                                        html.Button("Reset", id="bench-reset",
                                                    n_clicks=0, style=_BTN,
                                                    className="bench-btn"),
                                    ],
                                    style={"display": "flex", "alignItems": "center",
                                           "gap": "6px", "padding": "4px 0"},
                                ),
                                dcc.Textarea(
                                    id="bench-code", value=_START_CODE,
                                    spellCheck=False,
                                    style={**_INPUT, "width": "100%",
                                           "height": "205px", "resize": "vertical",
                                           "lineHeight": "1.45",
                                           "whiteSpace": "pre"},
                                ),
                            ],
                            style={"padding": "0 12px 10px", "flex": "none"},
                        ),
                    ],
                    style={"display": "flex", "flexDirection": "column",
                           "height": "100%", "minHeight": "0",
                           "background": SURFACE},
                ),
                # RIGHT - the knobs
                html.Div(
                    [
                        html.Div(controls.search_box(""),
                                 style={"padding": "10px 12px 0"}),
                        html.Div(id="bench-knob-msg",
                                 style={"font": f"11.5px {SANS}", "color": WARN,
                                        "padding": "0 12px", "minHeight": "17px"}),
                        _loading(
                            html.Div(_START_PANE, id="bench-knobs",
                                     style={"padding": "0 12px 60px"}),
                            "bench-knobs-loading"),
                    ],
                    style={**_PANE,
                           "borderLeft": f"1px solid {controls.RULE_STRONG}"},
                ),
            ],
            style={"display": "grid",
                   "gridTemplateColumns": "270px minmax(0, 1fr) 340px",
                   "flex": "1", "minHeight": "0"},
        ),

        # --- the source bar, always on screen ----------------------------
        source_bar(_START, _START_META),
    ],
    style={"display": "flex", "flexDirection": "column", "height": "100vh",
           "background": SURFACE, "font": f"13px {SANS}", "color": INK},
)


# =====================================================================
# CALLBACK 1 - THE ONLY WRITER OF THE SPEC
# ---------------------------------------------------------------------
# All four flows from SPEC section 8 land here - picker click, knob turn,
# code edit, source change - and `ctx.triggered_id` decides which it was.
# One writer means two callbacks can never argue over the state object.
#
# The four handlers below it (_apply_*) take plain arguments and return
# plain values, so every transition in SPEC section 8 can be tested
# headlessly without a browser. tests/test_bench_app.py does exactly that.
# =====================================================================

# Which Input index in the callback below carries the knob widgets. Read off
# the decorator rather than hardcoded in two places.
_KNOB_INPUT_INDEX = 1


@app.callback(
    Output("bench-spec", "data"),
    Output("bench-knob-echo", "data", allow_duplicate=True),
    Output("bench-knob-msg", "children"),
    Output("bench-history", "data"),
    Output("bench-persist", "data"),
    # 1. picker click
    Input({"bench": "chart", "key": ALL}, "n_clicks"),
    # 2. knob change - ONE pattern callback for every knob ON SCREEN.
    #    "on screen" is the whole point: with the pane lazy, an unopened tier
    #    has no components, so ALL matches nothing there and the browser stops
    #    posting ~4,000 widget values it never had a reason to send.
    Input({"bench": "knob", "path": ALL, "part": ALL}, "value"),
    # 2b. the annotations/shapes editor's add / remove buttons - their own id
    #     shape because a button has no `value` prop for the pattern above
    Input({"bench": "knobrow", "path": ALL, "op": ALL, "index": ALL},
          "n_clicks"),
    # 3. code edit, debounced in the browser (plus leaving the box)
    Input("bench-code-draft", "data"),
    Input("bench-code", "n_blur"),
    Input("bench-reset", "n_clicks"),
    # 4. source change
    Input("bench-src-kind", "value"),
    Input("bench-src-demo", "value"),
    Input("bench-src-run", "n_clicks"),
    # 5. history / files / the restore-on-load request
    Input("bench-undo", "n_clicks"),
    Input("bench-redo", "n_clicks"),
    Input("bench-load", "contents"),
    Input("bench-restore-req", "data"),
    State("bench-code", "value"),
    State("bench-src-sql", "value"),
    State("bench-spec", "data"),
    State("bench-echo", "data"),
    State("bench-knob-echo", "data"),
    State("bench-history", "data"),
    # THE ONE THING A HUMAN WAITS SECONDS FOR. A warehouse RUN goes through
    # this callback - `_apply_source` is where viz.sqlrun is called - and a
    # button that looks pressable while a 9.4s query is in flight is a button
    # you press twice. Dash swaps these props for the life of the call and
    # puts them back itself, so there is no second callback to keep in step.
    running=[
        (Output("bench-src-run", "disabled"), True, False),
        (Output("bench-src-run", "children"), "RUNNING SQL…", "RUN"),
    ],
    prevent_initial_call=True,
)
def sync_spec(_chart_clicks, knob_values, _row_clicks, draft, _blur, _reset,
              src_kind, src_demo, _run, _undo, _redo, load_contents,
              restore_data, code_value, sql, spec, echo, knob_echo, history):
    """Work out what the human just did, and write the one state object.

    Returns (spec, knob echo, message, history, persist). `no_update` for the
    spec means "nothing a human did changed anything", which is the normal
    answer when this fires because we ourselves just repainted the screen.

    `echo` is the CODE echo (written by `render_chart`); `knob_echo` is the
    widget echo (written by `render_knobs`, and stamped here on a knob turn).
    They are two stores because they have two writers - see the layout.

    `history` is the undo/redo record and `persist` is the localStorage
    mirror. Both are outputs HERE, and only here, so the one-writer rule
    holds for them the same way it holds for the spec.
    """
    try:
        return _sync_spec(_chart_clicks, knob_values, draft, _blur, _reset,
                          src_kind, src_demo, _run, load_contents,
                          restore_data, code_value, sql, spec, echo,
                          knob_echo, history)  # _row_clicks: trigger-only
    except Exception as exc:  # noqa: BLE001 - a bug here must be readable
        # Nothing below this line is reachable in a green suite. It exists
        # because the alternative is a 500 the browser swallows and a
        # traceback only the terminal ever sees, which is exactly the
        # "slow or broken?" question this pane is supposed to answer.
        return (no_update, no_update, _oops("reading that interaction", exc),
                no_update, no_update)


def _oops(doing: str, exc: BaseException) -> str:
    """One line a human can read, out of an exception nobody expected."""
    log = traceback.format_exc()
    print(log, file=sys.stderr)              # the terminal still gets all of it
    return (f"the Bench hit a bug {doing} — {type(exc).__name__}: {exc}. "
            "The full traceback is in the terminal.")


# How many steps back the undo stack keeps. Beyond this the oldest falls off.
HISTORY_CAP = 50


def _sync_spec(_chart_clicks, knob_values, draft, _blur, _reset, src_kind,
               src_demo, _run, load_contents, restore_data, code_value, sql,
               spec, echo, knob_echo, history):
    """`sync_spec`'s body, so the guard above it stays one line."""
    spec = json.loads(json.dumps(spec or blank_spec()))    # never mutate the store
    echo = echo or {"code": ""}
    knob_echo = knob_echo or {"knobs": {}}
    history = dict(history or {})
    past = list(history.get("past") or [])
    future = list(history.get("future") or [])
    before = json.dumps(spec, sort_keys=True)
    before_spec = json.loads(before)
    trigger = ctx.triggered_id
    message = ""
    echo_out: Any = no_update

    # -- undo / redo walk the history instead of making new ------------------
    if trigger in ("bench-undo", "bench-redo"):
        if trigger == "bench-undo":
            if not past:
                return no_update, no_update, "nothing to undo", no_update, no_update
            restored, past = past[-1], past[:-1]
            future = future + [before_spec]
        else:
            if not future:
                return no_update, no_update, "nothing to redo", no_update, no_update
            restored, future = future[-1], future[:-1]
            past = past + [before_spec]
        new_history = {"past": past, "future": future}
        return restored, echo_out, "", new_history, restored

    if isinstance(trigger, dict) and trigger.get("bench") == "chart":
        spec, message = _apply_chart(spec, trigger.get("key"))

    elif isinstance(trigger, dict) and trigger.get("bench") == "knob":
        ids = [item["id"] for item in ctx.inputs_list[_KNOB_INPUT_INDEX]]
        spec, message, echo_out = _apply_knobs(spec, ids, knob_values, knob_echo)

    elif isinstance(trigger, dict) and trigger.get("bench") == "knobrow":
        # Guard against the fire that happens when a pane rebuild ADDS these
        # buttons: a freshly rendered button reports n_clicks 0, a click 1+.
        clicked = False
        try:
            clicked = bool((ctx.triggered or [{}])[0].get("value"))
        except Exception:  # noqa: BLE001 - no context in some harnesses
            clicked = False
        if clicked:
            spec, message = _apply_compound_row(spec, trigger)

    elif trigger in ("bench-code-draft", "bench-code"):
        text = draft if trigger == "bench-code-draft" else code_value
        spec, message = _apply_code(spec, text, echo)

    elif trigger == "bench-reset":
        spec, message = _apply_reset(spec)

    elif trigger in ("bench-src-kind", "bench-src-demo", "bench-src-run"):
        spec, message = _apply_source(spec, trigger, src_kind, src_demo, sql)

    elif trigger == "bench-load":
        spec, message = _apply_load(spec, load_contents)

    elif trigger == "bench-restore-req":
        spec, message = _apply_restore(spec, restore_data)

    # Rule 3: if nothing actually moved, write nothing. A store that does not
    # change fires no callbacks, which is the last line of defence on a loop.
    if json.dumps(spec, sort_keys=True) == before:
        return no_update, echo_out, message, no_update, no_update
    # A real change: the old spec goes on the undo stack, the redo stack
    # empties (you cannot redo across a new edit), and localStorage gets the
    # new spec so an F5 comes back here.
    new_history = {"past": (past + [before_spec])[-HISTORY_CAP:], "future": []}
    return spec, echo_out, message, new_history, spec


# ---------------------------------------------------------------------
# 1. picker click
# ---------------------------------------------------------------------


def _apply_chart(spec: dict, key: str) -> tuple[dict, str]:
    """A new chart type. Guess a mapping so something draws on the click."""
    template = registry.CHARTS.get(key)
    if template is None:
        return spec, f"no chart called {key!r}"
    df, _meta = get_frame(spec.get("source") or {})
    spec["chart"] = key
    # registry.auto_map fills every required slot it can, so clicking a chart
    # gives you a picture rather than an empty pane with six dropdowns.
    spec["mapping"] = registry.auto_map(df, template)
    # Knobs the new chart also has come along; the rest are dropped, because
    # a knob with no widget here is one you could only reach by editing code.
    # (This used to nuke the lot - ten minutes of styling gone on a misclick.)
    old = spec.get("knobs") or {}
    kept = {p: v for p, v in old.items() if _knob_lives_on(p, key)}
    dropped = sorted(set(old) - set(kept))
    spec["knobs"] = kept
    spec["custom_code"] = None
    ok, why = registry.drawable(df, template)
    message = "" if ok else why
    if dropped:
        note = (f"dropped {', '.join(dropped)} — {key} has no such setting"
                if len(dropped) <= 3 else
                f"dropped {len(dropped)} settings {key} does not have")
        message = f"{message}  {note}".strip()
    return spec, message


def _knob_lives_on(path: str, chart_key: str) -> bool:
    """Does this knob path exist on that chart too?"""
    try:
        return knobs.validator_for(path, chart_key) is not None
    except Exception:  # noqa: BLE001 - an unreadable path does not carry over
        return False


# ---------------------------------------------------------------------
# 2. knob change
# ---------------------------------------------------------------------


def _apply_knobs(spec: dict, ids: list, values: list,
                 echo: dict) -> tuple[dict, str, Any]:
    """Fold every widget that differs from the echo into the SPEC.

    THE ECHO COMPARISON IS THE GUARD. `render_knobs` wrote down exactly what it
    put in each widget; anything still equal to that is our own paint coming
    back, and re-applying it is how you get a loop. Anything different is a
    human, and only that gets applied.

    `ids` and `values` line up one-to-one - they are what Dash hands a
    pattern-matching callback. Passing them in rather than reading
    `ctx.inputs_list` inside here is what makes this function testable with no
    browser and no callback context.
    """
    known = dict(echo.get("knobs") or {})
    template = registry.CHARTS.get(spec.get("chart"))
    index: dict[str, Any] = {}
    messages: list[str] = []
    touched = False

    for cid, raw in zip(ids, values):
        path, part = str(cid.get("path")), str(cid.get("part"))
        key = echo_key(path, part)
        raw = _jsonable(raw)
        if key in known and known[key] == raw:
            continue                     # our own writing, coming home
        if key not in known and raw is None:
            continue                     # a widget with no `value` prop at all
        known[key] = raw
        touched = True

        # --- a mapping slot: which column goes in which channel ----------
        if path.startswith(MAPPING_PREFIX):
            slot_name = path[len(MAPPING_PREFIX):]
            spec.setdefault("mapping", {})[slot_name] = _coerce_mapping(
                template, slot_name, raw)
            continue

        # --- a field inside an annotations/shapes row --------------------
        m = _COMPOUND_FIELD_RE.match(path)
        if m:
            _fold_compound_field(spec, m.group(1), int(m.group(2)),
                                 m.group(3), raw)
            continue

        # --- a real Plotly setting --------------------------------------
        # Ask Plotly whether it likes the value BEFORE it goes near the
        # figure, so a typo is a sentence and not a broken chart.
        if not index and template is not None:
            df, _meta = get_frame(spec.get("source") or {})
            index = _knob_index(spec["chart"], tuple(_columns(df)))
        knob = index.get(path) or controls.Knob(path=path, control="text")
        ok, coerced = knobs.validate(path, controls.coerce(knob, raw),
                                     spec.get("chart"))
        if not ok:
            messages.append(f"{path}: {coerced}")
            continue
        if coerced is None:
            spec.setdefault("knobs", {}).pop(path, None)   # cleared -> default
        else:
            spec.setdefault("knobs", {})[path] = _jsonable(coerced)

    if not touched:
        return spec, "", no_update
    # Stamping the value signature here is what tells `render_knobs` that the
    # widgets are ALREADY showing these values, so it must not rebuild the
    # pane underneath the control you are still holding.
    return spec, "; ".join(messages), {
        **echo, "knobs": known, "vals": knob_values_signature(spec)}


# "layout.annotations[2].line.color" -> (parent, index, dotted field)
_COMPOUND_FIELD_RE = re.compile(
    r"^(layout\.(?:annotations|shapes))\[(\d+)\]\.(.+)$")


def _coerce_compound(field: str, raw: Any) -> Any:
    """A row-field widget value, as the type the figure wants.

    text stays a string; showarrow is the yes/no radio; anything else tries
    a number first so "0.5" folds as 0.5 but "March" stays a category label.
    """
    last = field.rsplit(".", 1)[-1]
    if raw is None:
        return None
    if field == "showarrow":
        return raw == "yes"
    if last in ("text", "type") or last.endswith("color"):
        return str(raw)
    try:
        num = float(raw)
        return int(num) if num.is_integer() else num
    except (TypeError, ValueError):
        return str(raw)


def _fold_compound_field(spec: dict, parent: str, index: int, field: str,
                         raw: Any) -> None:
    """Write one edited row field back into the parent list knob."""
    rows = list(spec.get("knobs", {}).get(parent) or [])
    if not (0 <= index < len(rows)) or not isinstance(rows[index], dict):
        return
    row = json.loads(json.dumps(rows[index]))
    cur = row
    parts = field.split(".")
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
        if not isinstance(cur, dict):
            return
    cur[parts[-1]] = _coerce_compound(field, raw)
    rows[index] = row
    spec.setdefault("knobs", {})[parent] = rows


def _apply_compound_row(spec: dict, trigger: dict) -> tuple[dict, str]:
    """An add or remove click on the annotations/shapes editor."""
    path = str(trigger.get("path"))
    if path not in controls.COMPOUND_DEFAULTS:
        return spec, ""
    rows = list(spec.get("knobs", {}).get(path) or [])
    if trigger.get("op") == "add":
        rows.append(json.loads(json.dumps(controls.COMPOUND_DEFAULTS[path])))
    elif trigger.get("op") == "remove":
        index = int(trigger.get("index", -1))
        if 0 <= index < len(rows):
            del rows[index]
    if rows:
        spec.setdefault("knobs", {})[path] = rows
    else:
        spec.setdefault("knobs", {}).pop(path, None)   # empty -> Plotly default
    return spec, ""


def _coerce_mapping(template, slot_name: str, raw: Any) -> Any:
    """A widget value turned into what a mapping slot wants.

    A `many` slot (a correlation matrix's column list) wants a real list of
    column names. Everything else wants one column name or None. This is the
    one place `controls.coerce` is the wrong tool - it would join a list into
    Plotly's plus-separated flaglist string, which a mapping slot is not.
    """
    slot = template.slot(slot_name) if template is not None else None
    if slot is not None and slot.many:
        if raw is None:
            return []
        return [raw] if isinstance(raw, str) else list(raw)
    if isinstance(raw, str) and not raw.strip():
        return None
    return raw


# ---------------------------------------------------------------------
# 3. code edit
# ---------------------------------------------------------------------


def _apply_code(spec: dict, text: Any, echo: dict) -> tuple[dict, str]:
    """Read the code panel back. Canonical -> the knobs move. Anything else -> CUSTOM.

    The first check is the echo guard: if this is character-for-character what
    `render_chart` typed into the box, it is not an edit, it is the round trip
    closing - and acting on it is how the two panes end up shouting at each
    other forever.

    THE THIRD CHECK IS THE ONE THAT KEEPS THE SCREEN ALIVE. `codegen.parse`
    saying yes is not enough - the SPEC it hands back also has to be one
    `codegen.render` can write out again, because `render_chart` renders on
    every single repaint and it is the callback that paints the figure, the
    code box AND the status bar. If it raises, all three go dark at once and
    the reason is only in the server log. Six characters used to do it:

        fig.update_layout(width=1e400)

    So nothing enters the SPEC from this box until it has been written back
    once. Anything that will not write is not the canonical form, and the
    canonical form is the only thing the knob panel can drive - which is
    exactly what CUSTOM mode is for.
    """
    if not isinstance(text, str):
        return spec, ""
    if text == (echo.get("code") or ""):
        return spec, ""                    # our own writing, coming home
    if not text.strip():
        return spec, "the code box is empty — press Reset to bring it back"

    parsed, reason = codegen.parse_why(text)
    why = ""
    if parsed is None:
        why = reason or "this is not the canonical form"
    elif parsed.get("chart") not in registry.CHARTS:
        why = f"{parsed.get('chart')!r} is not a chart in the registry"
    else:
        try:
            render_code(parsed)
        except Exception as exc:  # noqa: BLE001 - any refusal means "not canonical"
            why = f"the Bench cannot write that back out — {exc}"

    if why:
        # SPEC section 1: this is a feature, not a failure. The chart still
        # draws, the knobs go read-only, Reset comes home.
        spec["custom_code"] = text
        return spec, f"CUSTOM mode — {why}. Reset returns to the knobs."

    parsed["custom_code"] = None
    # A chart change through the code panel does NOT clear the old chart's
    # knobs the way a picker click does - you typed them, so they stay. Say
    # which ones the new chart has no home for, because a knob with no widget
    # is one you can only reach by editing this box.
    homeless = _homeless_knobs(parsed)
    return parsed, ("" if not homeless else
                    f"{', '.join(homeless)} — {parsed['chart']} has no such "
                    "setting, so those lines do nothing")


def _homeless_knobs(spec: dict) -> list[str]:
    """Knob paths in this SPEC that the chosen chart does not have."""
    chart = spec.get("chart")
    if chart not in registry.CHARTS:
        return []
    out = []
    for path in sorted(spec.get("knobs") or {}):
        try:
            if knobs.validator_for(path, chart) is None:
                out.append(path)
        except Exception:  # noqa: BLE001 - an unreadable path is a homeless one
            out.append(path)
    return out


def _apply_reset(spec: dict) -> tuple[dict, str]:
    """Leave CUSTOM mode. Everything else about the SPEC is left alone."""
    if spec.get("custom_code") is None:
        return spec, "already on the canonical form — nothing to reset"
    spec["custom_code"] = None
    return spec, ""


# ---------------------------------------------------------------------
# 4. source change
# ---------------------------------------------------------------------


def _apply_source(spec: dict, trigger: str, kind: str, demo_name: str,
                  sql: str) -> tuple[dict, str]:
    """A new source means a new frame, so the mapping has to be re-checked.

    SPEC section 8, rule 4: mapping slots pointing at columns the new result
    does not have are cleared, and we say which ones - a chart that silently
    empties is a chart you cannot debug.
    """
    source = ({"kind": "demo", "name": demo_name or START_DEMO}
              if (kind or "demo") != "warehouse"
              else {"kind": "warehouse", "sql": sql or ""})
    spec["source"] = source
    spec["custom_code"] = None

    df, meta = get_frame(source, refresh=(trigger == "bench-src-run"))
    if not meta.get("ok"):
        return spec, str(meta.get("error", "that source did not load"))

    columns = set(_columns(df))
    mapping = dict(spec.get("mapping") or {})
    dropped: list[str] = []
    for slot_name, value in list(mapping.items()):
        if isinstance(value, list):
            keep = [v for v in value if str(v) in columns]
            if len(keep) != len(value):
                dropped.append(slot_name)
            mapping[slot_name] = keep
        elif value is not None and str(value) not in columns:
            dropped.append(slot_name)
            mapping[slot_name] = None
    spec["mapping"] = mapping

    template = registry.CHARTS.get(spec.get("chart"))
    if template is not None and template.missing(mapping):
        # Nothing usable left - take the first guess again so something draws.
        spec["mapping"] = registry.auto_map(df, template)

    if dropped:
        return spec, ("cleared " + ", ".join(sorted(set(dropped)))
                      + " — those columns are not in this result")
    return spec, ""


# ---------------------------------------------------------------------
# 5. files and the restore-on-load request
# ---------------------------------------------------------------------


def _valid_spec(candidate: Any) -> tuple[dict | None, str]:
    """A dict from a file or localStorage, checked before it may become THE spec.

    The same gate `_apply_code` runs: the chart must be in the registry, and a
    canonical spec must survive `render_code` - anything that will not write
    back out would take the fast lane down on the next repaint.
    """
    if not isinstance(candidate, dict) or not candidate.get("chart"):
        return None, "that is not a Bench spec"
    chart = candidate.get("chart")
    if chart not in registry.CHARTS:
        return None, f"{chart!r} is not a chart in this registry"
    custom = candidate.get("custom_code")
    spec = {
        "chart": chart,
        "source": (candidate.get("source")
                   if isinstance(candidate.get("source"), dict)
                   else blank_spec()["source"]),
        "mapping": dict(candidate.get("mapping") or {}),
        "knobs": dict(candidate.get("knobs") or {}),
        "custom_code": custom if isinstance(custom, str) else None,
    }
    if spec["custom_code"] is None:
        try:
            render_code(spec)
        except Exception as exc:  # noqa: BLE001 - refusal means invalid
            return None, f"the Bench cannot write that spec back out — {exc}"
    return spec, ""


def _defer_warehouse(spec: dict) -> tuple[dict, str]:
    """A restored/loaded warehouse source must not hit Snowflake by itself.

    The SQL stays in the spec, but marked deferred: bench.data answers it with
    "press RUN" instead of running it. Switching the source bar to warehouse
    (the SQL is already in the box) and pressing RUN runs it - both of those
    are the human asking, which is the whole point.
    """
    source = spec.get("source") or {}
    if source.get("kind") != "warehouse" or not source.get("sql"):
        return spec, ""
    spec["source"] = {**source, "deferred": True}
    return spec, ("this spec reads the warehouse — the SQL is restored but has "
                  "not run. Switch the source bar to warehouse SQL and press "
                  "RUN when you want it.")


def _apply_load(spec: dict, contents: Any) -> tuple[dict, str]:
    """A .json spec file dropped on the load button."""
    if not isinstance(contents, str) or "," not in contents:
        return spec, "could not read that file"
    import base64

    try:
        raw = base64.b64decode(contents.split(",", 1)[1])
        candidate = json.loads(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - a bad file is a message
        return spec, f"could not read that file — {type(exc).__name__}: {exc}"
    loaded, why = _valid_spec(candidate)
    if loaded is None:
        return spec, why
    loaded, note = _defer_warehouse(loaded)
    return loaded, note or "spec loaded"


def _apply_restore(spec: dict, data: Any) -> tuple[dict, str]:
    """The one-shot restore on page load, from the localStorage mirror."""
    restored, why = _valid_spec(data)
    if restored is None:
        return spec, ""      # nothing worth saying on a fresh boot
    restored, note = _defer_warehouse(restored)
    return restored, note or "restored where you left off"


# =====================================================================
# CALLBACKS 2, 3 and 4 - THE SCREEN, SPLIT BY WHAT IT COSTS
# ---------------------------------------------------------------------
# This used to be ONE callback with EIGHT Outputs off one Input, and that
# is why the app felt broken. Dash returns a callback's outputs together,
# so the figure - 1.3ms to build, 2.5 KB on the wire - could not appear
# until the knob pane had finished. Measured: clicking a chart took 268ms
# and 4,128 KB, of which 94% was Output 3.
#
# Three callbacks now, one per cost class, all fanning out from the same
# `bench-spec` store so they start together and land as they finish:
#
#   render_chart   figure + code + status + build message + code mode.
#                  ~8ms, ~40 KB. This is the one you are waiting for.
#   render_knobs   the right-hand pane. Lazy, so ~5ms and ~90 KB on a
#                  first paint, and only bigger when you asked for it.
#   render_picker  the 145 chart buttons. 4ms, 133 KB, and now guarded by
#                  its own signature so a knob turn does not ship it again.
#
# WHY THIS CANNOT LOOP - the callback_context guard, said once, here.
# `sync_spec` is still the only writer of `bench-spec`. These three read it
# and never write it, so there is no cycle in the graph at all. The thing
# that could still ping-pong is the ECHO: each lane writes down what it put
# on screen, the browser reports that back, and `sync_spec` has to be able
# to tell its own paint from a human's edit. It does it by comparing
# against the echo, NOT by looking at what triggered it - `ctx.triggered_id`
# only picks WHICH handler runs (chart / knob / code / source), never
# whether to act. That matters here because the split gave the echo two
# writers where there was one, so each lane got its own store: `bench-echo`
# holds the code text and only `render_chart` writes it; `bench-knob-echo`
# holds the widget values and only `render_knobs` (and `sync_spec` itself,
# on a knob turn) writes that. Two callbacks that fire from the same Input
# at the same instant cannot clobber each other's record of what is on
# screen, because they no longer share one.
# =====================================================================


@app.callback(
    Output("bench-figure", "figure"),
    Output("bench-code", "value"),
    Output("bench-status", "children"),
    Output("bench-build-msg", "children"),
    Output("bench-code-mode", "children"),
    Output("bench-echo", "data"),
    Input("bench-spec", "data"),
    State("bench-echo", "data"),
)
def render_chart(spec, echo):
    """THE FAST LANE. The chart, the code under it, and the badges.

    Nothing in here waits on the knob pane or the picker, which is the whole
    reason it exists. It also writes the code echo - what `sync_spec` compares
    an incoming code edit against, so the round trip closing does not read as
    a human typing (rule 2 in the module docstring).
    """
    spec = spec or blank_spec()
    echo = echo or {"code": ""}
    try:
        df, meta = get_frame(spec.get("source") or {})
        fig, build_msg = figure_for(spec, df, meta)
        code, mode = code_and_mode(spec)
    except Exception as exc:  # noqa: BLE001 - a bug must be on the screen
        why = _oops("drawing this chart", exc)
        return (message_figure("the Bench hit a bug", why), no_update,
                status_bar({"ok": False, "error": why, "lane": "unknown"}),
                why, html.Span("errored", style={"color": BAD}), no_update)

    # --- the code box, only when the canonical text changed ------------
    # Leaving it alone keeps your cursor where you put it, and keeps whatever
    # formatting you used when your edit meant the same thing anyway.
    code_out = code if code != (echo.get("code") or "") else no_update
    return fig, code_out, status_bar(meta), build_msg, mode, {"code": code}


def code_and_mode(spec: dict) -> tuple[str, Any]:
    """The text for the code box and the one-line badge above it.

    `render_code` is guarded the same way `figure_for` is: a knob value that
    `knobs.validate` accepts but `codegen.render` refuses (a non-finite float
    is the live example) must not take the pane down with a 500 - the box says
    what happened and everything else keeps repainting.
    """
    if isinstance(spec.get("custom_code"), str):
        return spec["custom_code"], html.Span(CUSTOM_BANNER, style={"color": WARN})
    try:
        return render_code(spec), html.Span("canonical — two-way",
                                            style={"color": FAINT})
    except Exception as exc:  # noqa: BLE001 - any refusal is a message
        why = f"{type(exc).__name__}: {exc}"
        return (f"# this value can't be written as Python — {why}\n"
                "# the knob is set, but the code below is stale.\n"
                "# clear that knob, or hit Reset.\n",
                html.Span(f"code not renderable — {why}", style={"color": WARN}))


@app.callback(
    Output("bench-knobs", "children"),
    Output("bench-knob-echo", "data"),
    Input("bench-spec", "data"),
    Input(controls.panel_id("search"), "value"),
    Input("bench-open", "data"),
    State("bench-knob-echo", "data"),
)
def render_knobs(spec, knob_query, open_store, echo):
    """THE SLOW LANE. The right-hand pane, and what it put in every widget.

    The pane is deliberately NOT rebuilt when only a knob moved (SPEC section
    8, rule 2) - yanking the control out from under the hand holding it. It is
    rebuilt when the SIGNATURE changes: a different chart, different columns,
    in or out of CUSTOM, a new search, or a tier the human just opened.
    """
    spec = spec or blank_spec()
    echo = echo or {"knobs": {}, "sig": None, "vals": None}
    try:
        info = get_info(spec.get("source") or {})
        columns = list(info.columns)
        custom = isinstance(spec.get("custom_code"), str)
        opened = open_tokens(open_store, open_key(spec))

        # `sig` is WHICH knobs exist; `vals` is what they are set to. Rebuild
        # on either, except that a knob turn stamps `vals` itself (see
        # knob_values_signature) so turning a knob never rebuilds the pane.
        #
        # `opened` is in the signature ONLY when there is no search. Under a
        # search `controls.accordion` never reads it - it folds every hit from
        # every tier into Tier 0 - so a token arriving mid-search would rebuild
        # a byte-identical pane and take the open dropdown with it. Reproduced:
        # 136 widgets in, the same 136 out, and the click gone.
        signature = [spec.get("chart"), columns, custom, knob_query or "",
                     [] if (knob_query or "").strip() else list(opened)]
        values_signature = knob_values_signature(spec)
        if signature == echo.get("sig") and values_signature == echo.get("vals"):
            return no_update, no_update

        pane = knob_pane(spec, columns, knob_query or "", opened)
    except Exception as exc:  # noqa: BLE001 - a bug must be on the screen
        # The echo is CLEARED, not left alone. Leaving it would keep the
        # signature of the last pane that built, so coming back to that exact
        # state - click the chart that broke, click the one that worked -
        # matches, returns no_update, and leaves the red box on screen with a
        # working chart beside it. An error you cannot get out of is worse
        # than the error. Reproduced before it was fixed.
        return (html.Div(_oops("building the knob pane", exc),
                         style={"font": f"12px {SANS}", "color": BAD,
                                "border": f"1px solid {BAD}",
                                "borderRadius": "5px", "padding": "8px 10px"}),
                {"knobs": {}, "sig": None, "vals": None})
    # The echo is stamped in the SAME return as the pane, and it has to be:
    # opening a tier puts widgets on screen carrying their displayed defaults,
    # and anything not in the echo when they report in reads as a human edit.
    return pane, {"knobs": knob_echo(pane), "sig": signature,
                  "vals": values_signature}


@app.callback(
    Output("bench-picker", "children"),
    Output("bench-picker-sig", "data"),
    Input("bench-spec", "data"),
    Input("bench-picker-search", "value"),
    State("bench-picker-sig", "data"),
)
def render_picker(spec, query, sig):
    """The 145 chart buttons, and only when one of them would look different.

    It depends on three things and none of them is a knob: which chart is
    selected, which frame is on screen (that is what greys a chart out), and
    the search box. Turning a knob changes none of them, so the guard here is
    133 KB of buttons NOT shipped on every single knob turn.
    """
    spec = spec or blank_spec()
    source = spec.get("source") or {}
    try:
        info = get_info(source)
        # The frame's SHAPE is in the signature, not just the source dict.
        # Pressing RUN on the same SQL against a table that has changed is the
        # same source and a different answer, and the answer is what decides
        # which charts are greyed out.
        signature = [spec.get("chart"), data.source_key(source),
                     list(info.columns), info.rows, query or ""]
        if signature == sig:
            return no_update, no_update
        return picker(spec, info.df, query or "",
                      roles=info.chart_roles), signature
    except Exception as exc:  # noqa: BLE001 - a bug must be on the screen
        # `None`, not `no_update` - see the same note in `render_knobs`. A
        # kept signature makes the error box sticky: come back to the state
        # that drew fine and it matches, so nothing is rebuilt and the red
        # text stays where 145 buttons should be.
        return (html.Div(_oops("building the chart picker", exc),
                         style={"font": f"12px {SANS}", "color": BAD}),
                None)


# =====================================================================
# CALLBACK 5 - WHICH KNOB TIERS ARE MATERIALISED
# ---------------------------------------------------------------------
# The only writer of `bench-open`. Clicking a bucket header or its
# "show more" asks for Tier 1; "show everything" asks for Tier 2, and
# `controls.opened_with` folds the clicked id into the set.
#
# Every triggered id is folded in, not just `ctx.triggered_id`. A nested
# <details> click bubbles, so opening MARK's "show everything" bumps
# n_clicks on the expander AND on the bucket around it - taking only the
# first would ask for Tier 1 when the human asked for Tier 2.
#
# THAT SAME BUBBLE IS ALSO A TRAP, and it is the one this app was reported
# for. `<details onClick>` fires for a click ANYWHERE inside it, so opening
# the `mapping.x` dropdown is indistinguishable, at this callback, from
# clicking the DATA header. Two guards below keep a body click from
# rebuilding the pane out from under the menu you just opened:
#
#   * `materialisable` drops a token for a tier with no knobs in it. That is
#     DATA, always - `knob_tree` gives it three mapping slots and two empty
#     tiers - and DATA is the one bucket open on a first paint.
#   * a SEARCH draws no tier expanders at all (`build_tiers=(0,)`), so while
#     one is on, every bucket id on screen is a <details> a click bubbled to.
#     There is nothing to ask for, so nothing is asked for.
# =====================================================================


@app.callback(
    Output("bench-open", "data"),
    Input({"bench": "bucket", "bucket": ALL, "part": ALL}, "n_clicks"),
    State("bench-open", "data"),
    State("bench-spec", "data"),
    State(controls.panel_id("search"), "value"),
    prevent_initial_call=True,
)
def grow_open(_clicks, store, spec, query=""):
    if (query or "").strip():
        # Searching. `controls.accordion` folds every hit from every tier
        # into Tier 0 and never draws "show more", so no click here can be
        # asking for a tier - it is a click on a row that bubbled up.
        return no_update
    key = open_key(spec or {})
    before = set(open_tokens(store, key))
    tokens = set(before)
    fired = list((getattr(ctx, "triggered_prop_ids", None) or {}).values())
    for cid in (fired or [ctx.triggered_id]):
        tokens |= set(controls.opened_with(tokens, cid))
    real = materialisable(spec or {})
    if real is not None:
        tokens &= real
    out = {"key": key, "tokens": sorted(tokens)}
    # A store that does not change fires nothing. Closing a <details> is free
    # and a click on a bucket body is not a request for anything.
    if out == (store or {}) or tokens == before:
        return no_update
    return out


# =====================================================================
# CALLBACK 3 - THE 600ms DEBOUNCE, done in the browser
# ---------------------------------------------------------------------
# dcc.Textarea has no `debounce` prop on dash 4.4.1 - checked against the
# install: dcc.Input has one, dcc.Textarea does not - so its value fires on
# every keystroke. Parsing half-typed Python sixty times a second would drop
# you into CUSTOM mode mid-word. This waits until you stop, then hands the
# text to the server through a store, which is what sync_spec listens to.
# =====================================================================

clientside_callback(
    """
    function (text) {
        if (window.__benchCodeTimer) { clearTimeout(window.__benchCodeTimer); }
        window.__benchCodeTimer = setTimeout(function () {
            window.dash_clientside.set_props('bench-code-draft', {data: text});
        }, __MS__);
        return window.dash_clientside.no_update;
    }
    """.replace("__MS__", str(DEBOUNCE_MS)),
    Output("bench-debounce-sink", "data"),
    Input("bench-code", "value"),
    prevent_initial_call=True,
)


# =====================================================================
# THE RESTORE - once per page load, localStorage -> the spec
# ---------------------------------------------------------------------
# bench-persist (storage_type="local") arrives holding whatever sync_spec
# last mirrored into it, possibly from a previous session. This copies it
# into bench-restore-req exactly once - the window flag survives every later
# write to persist, so sync_spec's own mirroring can never re-trigger a
# restore - and sync_spec validates and adopts it from there. The SQL text
# rides along into the query box (a State, so writing it triggers nothing);
# `allow_duplicate` because the catalog drawer also writes that box.
# =====================================================================

clientside_callback(
    """
    function (ts, data) {
        const nu = window.dash_clientside.no_update;
        if (window.__benchRestored) { return [nu, nu]; }
        window.__benchRestored = true;
        if (!data || !data.chart) { return [nu, nu]; }
        const sql = (data.source && data.source.sql) ? data.source.sql : nu;
        return [data, sql];
    }
    """,
    Output("bench-restore-req", "data"),
    Output("bench-src-sql", "value", allow_duplicate=True),
    Input("bench-persist", "modified_timestamp"),
    State("bench-persist", "data"),
    prevent_initial_call="initial_duplicate",
)


# =====================================================================
# CALLBACK 4 - the source bar's two faces
# =====================================================================


@app.callback(
    Output("bench-src-demo-box", "style"),
    Output("bench-src-sql-tools", "style"),
    Output("bench-src-sql", "style"),
    Input("bench-src-kind", "value"),
    State("bench-src-sql", "style"),
)
def source_face(kind, sql_style):
    """demo picks a generated frame; warehouse shows the query box and RUN."""
    demo = kind != "warehouse"
    return (
        {"flex": "1", "minWidth": "0", "display": "block" if demo else "none"},
        {"display": "none" if demo else "flex", "gap": "6px", "flex": "1",
         "alignItems": "center", "minWidth": "0"},
        {**(sql_style or {}), "display": "none" if demo else "block"},
    )


# =====================================================================
# CALLBACKS 5a-5d - the catalog drawer
# ---------------------------------------------------------------------
# SPEC section 7: reuse viz/catalog.py rather than hardcoding a list. The
# old shape was a blind term box + "look up" that fired live SQL and threw
# away every fact the catalog returned except the FQN. This one is
# browse-first off a DISK SNAPSHOT, so browsing costs nothing and works on
# a plane. Exactly three actions here touch Snowflake, each behind its own
# labelled button, each writing what it did to the note line:
#     refresh catalog   two live queries, rebuilds the snapshot
#     pick a row        DESCRIBE TABLE - metadata only, no compute
#     draft starter SQL a 10k-row profile, cached 7 days
# =====================================================================

# The lifecycle badge colours: modeled means a typed mart exists, landed is
# raw-but-real, sampled is a proof slice pretending to be small.
_LIFE_COLOUR = {"modeled": GOOD, "landed": MUTED, "sampled": WARN}


def _fmt_count(n) -> str:
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "?"
    for cut, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "k")):
        if n >= cut:
            return f"{n / cut:.1f}{suffix}".replace(".0", "")
    return str(n)


def _snapshot_age(built_at: str) -> str:
    try:
        built = time.mktime(time.strptime(built_at, "%Y-%m-%dT%H:%M:%S"))
        mins = max(0, int((time.time() - built) / 60))
        ago = (f"{mins}m ago" if mins < 120 else
               f"{mins // 60}h ago" if mins < 48 * 60 else
               f"{mins // (24 * 60)}d ago")
        return f"snapshot built {ago} · browsing it is free"
    except ValueError:
        return f"snapshot built {built_at}"


def _catalog_row(t: dict) -> html.Button:
    badges = [html.Span(f"{_fmt_count(t.get('rows'))} rows",
                        style={"color": FAINT, "font": f"10px {MONO}",
                               "flex": "none"})]
    life = t.get("lifecycle") or ""
    if life:
        badges.append(html.Span(life, style={
            "color": _LIFE_COLOUR.get(life, FAINT), "font": f"10px {MONO}",
            "border": f"1px solid {RULE}", "borderRadius": "3px",
            "padding": "0 4px", "flex": "none"}))
    if t.get("is_sample"):
        badges.append(html.Span("SAMPLE", title="a proof slice, not the full data",
                                style={"color": WARN, "font": f"600 10px {MONO}",
                                       "border": f"1px solid {WARN}",
                                       "borderRadius": "3px", "padding": "0 4px",
                                       "flex": "none"}))
    top = [html.Span(t.get("name") or t.get("fqn"),
                     style={"color": INK, "font": f"600 12px {SANS}"}),
           html.Span(t.get("fqn") or "",
                     style={"color": FAINT, "font": f"10px {MONO}",
                            "marginLeft": "8px"})]
    line2 = t.get("one_liner") or ""
    return html.Button(
        [html.Div([html.Div(top, style={"minWidth": "0", "overflow": "hidden",
                                        "textOverflow": "ellipsis",
                                        "whiteSpace": "nowrap", "flex": "1"}),
                   *badges],
                  style={"display": "flex", "gap": "6px",
                         "alignItems": "center"}),
         html.Div(line2, style={"color": MUTED, "font": f"11px {SANS}",
                                "marginTop": "1px", "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "whiteSpace": "nowrap"}) if line2 else None],
        id={"type": "bench-cat-row", "fqn": t.get("fqn") or ""},
        n_clicks=0, className="bench-cat-row",
        style={"display": "block", "width": "100%", "textAlign": "left",
               "background": "transparent", "border": "none",
               "borderBottom": f"1px solid {RULE}", "padding": "6px 8px",
               "cursor": "pointer"},
    )


def _catalog_body(snap: dict | None, domain, term):
    """(rows children, domain options, age line) off the snapshot alone."""
    if not snap or not snap.get("tables"):
        why = data.LAST_CATALOG_ERROR
        empty = html.Div(
            "no catalog snapshot yet — press refresh catalog (2 warehouse "
            "queries)" + (f" · last error: {why}" if why else ""),
            style={"color": MUTED, "font": f"12px {SANS}", "padding": "12px"})
        return empty, [], ""
    tables = snap["tables"]
    by_dom: dict[str, list] = {}
    for t in tables:
        by_dom.setdefault(t.get("domain") or "unfiled", []).append(t)
    dom_options = [
        {"label": f"{d}  ·  {len(ts)} tables  ·  "
                  f"{_fmt_count(sum(int(t.get('rows') or 0) for t in ts))} rows",
         "value": d}
        for d, ts in sorted(by_dom.items(),
                            key=lambda kv: -sum(int(t.get("rows") or 0)
                                                for t in kv[1]))]
    shown = by_dom.get(domain, tables) if domain else tables
    if term:
        low = term.lower()
        shown = [t for t in shown
                 if low in (t.get("name") or "").lower()
                 or low in (t.get("fqn") or "").lower()
                 or low in (t.get("one_liner") or "").lower()]
    rows = [_catalog_row(t) for t in shown[:TABLE_CAP]]
    if len(shown) > TABLE_CAP:
        rows.append(html.Div(
            f"showing {TABLE_CAP} of {len(shown)} — narrow the filter",
            style={"color": FAINT, "font": f"11px {SANS}", "padding": "8px"}))
    elif not rows:
        rows = [html.Div("nothing matches that filter",
                         style={"color": MUTED, "font": f"12px {SANS}",
                                "padding": "12px"})]
    return rows, dom_options, _snapshot_age(snap.get("built_at") or "")


@app.callback(
    Output("bench-cat-drawer", "style"),
    Input("bench-cat-open", "n_clicks"),
    State("bench-cat-drawer", "style"),
    prevent_initial_call=True,
)
def toggle_catalog(_n, style):
    """Open/close the drawer. Pure style flip - costs nothing anywhere."""
    style = dict(style or {})
    style["display"] = "none" if style.get("display") != "none" else "block"
    return style


@app.callback(
    Output("bench-cat-list", "children"),
    Output("bench-cat-domain", "options"),
    Output("bench-cat-age", "children"),
    Output("bench-src-note", "children"),
    Input("bench-cat-open", "n_clicks"),
    Input("bench-cat-domain", "value"),
    Input("bench-cat-filter", "value"),
    Input("bench-cat-refresh", "n_clicks"),
    running=[
        (Output("bench-cat-refresh", "disabled"), True, False),
        (Output("bench-cat-refresh", "children"), "refreshing…", "refresh catalog"),
    ],
    prevent_initial_call=True,
)
def browse_catalog(_open, domain, term, _refresh):
    """Serve the drawer. Only the refresh button ever leaves this machine."""
    if ctx.triggered_id == "bench-cat-refresh":
        t0 = time.time()
        snap = data.catalog_refresh()
        if snap is None:
            note = (f"catalog refresh failed — {data.LAST_CATALOG_ERROR}"
                    if data.LAST_CATALOG_ERROR else "catalog refresh failed")
        else:
            note = (f"⚡ warehouse: rebuilt the catalog snapshot in "
                    f"{time.time() - t0:.1f}s — {len(snap.get('tables', []))} "
                    f"tables · {data.budget()}")
    else:
        snap = data.catalog_snapshot()
        note = no_update    # browsing is silent because it costs nothing
    rows, dom_options, age = _catalog_body(snap, domain, term)
    return rows, dom_options, age, note


@app.callback(
    Output("bench-src-sql", "value", allow_duplicate=True),
    Output("bench-src-cols", "children"),
    Output("bench-cat-picked", "data"),
    Output("bench-src-note", "children", allow_duplicate=True),
    Input({"type": "bench-cat-row", "fqn": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def pick_catalog_row(clicks):
    """A row click: cheap SELECT * in the box + column chips off DESCRIBE.

    DESCRIBE is metadata-only - no warehouse compute - and the note says so.
    The 10k-row profile the old picker ran silently now only happens behind
    the labelled `draft starter SQL` button."""
    if not ctx.triggered_id or not isinstance(ctx.triggered_id, dict) \
            or not any(c for c in (clicks or []) if c):
        return no_update, no_update, no_update, no_update
    fqn = ctx.triggered_id.get("fqn") or ""
    sql = f"SELECT *\nFROM {fqn}\nLIMIT {settings.SQL_LIMIT}"
    cols = data.table_columns(fqn)
    if cols:
        chips = [html.Span(f"{c['column']} · {c['sf_type']}",
                           title=f"{c['column']}  ({c['sf_type']})",
                           style={"color": MUTED, "font": f"10px {MONO}",
                                  "border": f"1px solid {RULE}",
                                  "borderRadius": "3px", "padding": "1px 5px"})
                 for c in cols]
        note = (f"⚡ warehouse: DESCRIBE {fqn} (metadata only, no compute) — "
                f"{len(cols)} columns below. Edit the SQL and press RUN, or "
                "press `draft starter SQL` to type the columns first.")
    else:
        chips = []
        why = data.LAST_CATALOG_ERROR
        note = (f"picked {fqn} — column preview unavailable "
                f"({why})" if why else f"picked {fqn}")
    return sql, chips, fqn, note


@app.callback(
    Output("bench-src-sql", "value", allow_duplicate=True),
    Output("bench-src-note", "children", allow_duplicate=True),
    Input("bench-src-draft", "n_clicks"),
    State("bench-cat-picked", "data"),
    running=[
        (Output("bench-src-draft", "disabled"), True, False),
        (Output("bench-src-draft", "children"), "profiling…", "draft starter SQL"),
    ],
    prevent_initial_call=True,
)
def draft_starter(_n, fqn):
    """The one deliberate profile: casted starter SQL for the picked table."""
    if not fqn:
        return no_update, ("pick a table in the catalog first — draft needs to "
                           "know which table's columns to type")
    t0 = time.time()
    sql = data.starter_sql(fqn)
    if data.LAST_CATALOG_ERROR:
        note = (f"profile failed ({data.LAST_CATALOG_ERROR}) — dropped a plain "
                f"SELECT * for {fqn} instead")
    else:
        note = (f"⚡ warehouse: profiled 10,000 rows of {fqn} in "
                f"{time.time() - t0:.1f}s (cached 7 days) — the casted starter "
                f"SQL is in the box; edit it, then RUN · {data.budget()}")
    return sql, note


# =====================================================================
# CALLBACK 6 - export
# ---------------------------------------------------------------------
# Two doors out of the Bench that are not a screenshot. `.py` hands over the
# code panel's text as a file; `html` rebuilds the current figure server-side
# and writes a standalone interactive page. PNG needs neither - the modebar
# camera on the Graph does it in the browser.
# =====================================================================


@app.callback(
    Output("bench-download", "data"),
    Input("bench-export-py", "n_clicks"),
    Input("bench-export-html", "n_clicks"),
    Input("bench-save", "n_clicks"),
    State("bench-spec", "data"),
    prevent_initial_call=True,
)
def export_chart(_py, _html, _save, spec):
    """Download the chart as .py / standalone HTML, or the spec as .json."""
    spec = spec or blank_spec()
    name = str(spec.get("chart") or "chart").replace("/", "-")
    if ctx.triggered_id == "bench-save":
        return dcc.send_string(json.dumps(spec, indent=2),
                               f"bench-{name}.json")
    if ctx.triggered_id == "bench-export-py":
        code = (spec.get("custom_code")
                if isinstance(spec.get("custom_code"), str)
                else render_code(spec))
        header = ("# Written by the Bench. Run it anywhere bench/ and its\n"
                  "# data lane are importable.\n"
                  "import plotly.express as px  # noqa: F401\n"
                  "import bench.data\nimport bench.registry\n\n")
        return dcc.send_string(header + code + "\n", f"bench-{name}.py")

    df, meta = get_frame(spec.get("source") or {})
    fig, why = figure_for(spec, df, meta)
    if why:
        # export exactly what is on screen, even when that is the message
        # figure - a silent no-op download button reads as broken
        pass
    html_text = fig.to_html(include_plotlyjs="cdn", full_html=True)
    return dcc.send_string(html_text, f"bench-{name}.html")


# =====================================================================
# GO
# =====================================================================

if __name__ == "__main__":
    print(f"The Bench — {len(registry.TEMPLATES)} charts, "
          f"{len(data.DEMO)} demo frames.  http://127.0.0.1:{settings.PORT}"
          + ("  [debug]" if settings.DEBUG else ""))
    app.run(debug=settings.DEBUG, port=settings.PORT)
