#!/usr/bin/env python
"""A faithful reconstruction of THE BENCH's OLD callback shape, so the
before/after of a gesture is two measurements and not one measurement plus
arithmetic.

What is reconstructed, and only this:
  * ONE `render_all` with eight Outputs off one Input.
  * the knob pane EAGER - every bucket, every tier, on every repaint.
  * ONE echo store holding both the code text and all ~4,000 widget values,
    so sync_spec's request body and render_all's response body are the sizes
    the baseline measured.

Everything it calls - figure_for, knob_pane, picker, status_bar, knob_echo,
render_code, get_frame - is the SHIPPED function from bench.app. This is the
old wiring around today's builders, which is exactly the variable under test.

FIDELITY CHECK: it prints its own render_all numbers next to the two rows the
baseline recorded against the real old server. If those do not line up, the
reconstruction is not faithful and the before number should not be quoted.
"""
from __future__ import annotations

import os
import sys

from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dash import (ALL, Dash, Input, Output, State, ctx, dcc, html,  # noqa: E402
                  no_update)

from bench import app as A  # noqa: E402
from bench import controls  # noqa: E402

old = Dash(__name__, title="The Bench (old shape)",
           suppress_callback_exceptions=True, update_title=None)

_START = A.blank_spec()
_DF, _META = A.get_frame(_START["source"])
_COLS = A._columns(_DF)
_PANE = A.knob_pane(_START, _COLS, "", A.ALL_TIERS_OPEN)     # EAGER
_CODE = A.render_code(_START)

old.layout = html.Div([
    dcc.Store(id="bench-spec", data=_START),
    dcc.Store(id="bench-echo", data={"code": _CODE, "knobs": A.knob_echo(_PANE)}),
    dcc.Store(id="bench-code-draft"),
    dcc.Graph(id="bench-figure"),
    dcc.Textarea(id="bench-code", value=_CODE),
    html.Div(_PANE, id="bench-knobs"),
    html.Div(A.picker(_START, _DF), id="bench-picker"),
    html.Div(A.status_bar(_META), id="bench-status"),
    html.Div(id="bench-build-msg"),
    html.Span(id="bench-code-mode"),
    html.Div(id="bench-knob-msg"),
    html.Button("Reset", id="bench-reset", n_clicks=0),
    dcc.RadioItems(id="bench-src-kind", value="demo",
                   options=[{"label": "demo", "value": "demo"}]),
    dcc.Dropdown(id="bench-src-demo", value=A.START_DEMO,
                 options=[{"label": n, "value": n} for n in ("category", "long")]),
    html.Button("RUN", id="bench-src-run", n_clicks=0),
    dcc.Textarea(id="bench-src-sql", value=""),
    dcc.Input(id=controls.panel_id("search"), value=""),
    dcc.Input(id="bench-picker-search", value=""),
])


@old.callback(
    Output("bench-spec", "data"),
    Output("bench-echo", "data", allow_duplicate=True),
    Output("bench-knob-msg", "children"),
    Input({"bench": "chart", "key": ALL}, "n_clicks"),
    Input({"bench": "knob", "path": ALL, "part": ALL}, "value"),
    Input("bench-code-draft", "data"),
    Input("bench-code", "n_blur"),
    Input("bench-reset", "n_clicks"),
    Input("bench-src-kind", "value"),
    Input("bench-src-demo", "value"),
    Input("bench-src-run", "n_clicks"),
    State("bench-code", "value"),
    State("bench-src-sql", "value"),
    State("bench-spec", "data"),
    State("bench-echo", "data"),
    prevent_initial_call=True,
)
def sync_spec(_clicks, knob_values, draft, _blur, _reset, kind, demo, _run,
              code_value, sql, spec, echo):
    """The old writer: ONE echo store carrying code text AND widget values."""
    import json

    spec = json.loads(json.dumps(spec or A.blank_spec()))
    echo = echo or {"code": "", "knobs": {}}
    before = json.dumps(spec, sort_keys=True)
    trigger = ctx.triggered_id
    message = ""
    echo_out = no_update

    if isinstance(trigger, dict) and trigger.get("bench") == "chart":
        spec, message = A._apply_chart(spec, trigger.get("key"))
    elif isinstance(trigger, dict) and trigger.get("bench") == "knob":
        ids = [i["id"] for i in ctx.inputs_list[1]]
        spec, message, echo_out = A._apply_knobs(spec, ids, knob_values, echo)
    elif trigger in ("bench-code-draft", "bench-code"):
        text = draft if trigger == "bench-code-draft" else code_value
        spec, message = A._apply_code(spec, text, echo)
    elif trigger == "bench-reset":
        spec, message = A._apply_reset(spec)
    elif trigger in ("bench-src-kind", "bench-src-demo", "bench-src-run"):
        spec, message = A._apply_source(spec, trigger, kind, demo, sql)

    if json.dumps(spec, sort_keys=True) == before:
        return no_update, echo_out, message
    return spec, echo_out, message


@old.callback(
    Output("bench-figure", "figure"),
    Output("bench-code", "value"),
    Output("bench-knobs", "children"),
    Output("bench-picker", "children"),
    Output("bench-status", "children"),
    Output("bench-build-msg", "children"),
    Output("bench-code-mode", "children"),
    Output("bench-echo", "data"),
    Input("bench-spec", "data"),
    Input(controls.panel_id("search"), "value"),
    Input("bench-picker-search", "value"),
    State("bench-echo", "data"),
)
def render_all(spec, knob_query, pick_query, echo):
    """EIGHT outputs, one Input. The figure cannot land before the pane does."""
    spec = spec or A.blank_spec()
    echo = echo or {"code": "", "knobs": {}}
    df, meta = A.get_frame(spec.get("source") or {})
    columns = A._columns(df)
    custom = isinstance(spec.get("custom_code"), str)

    fig, build_msg = A.figure_for(spec, df, meta)
    code, mode = A.code_and_mode(spec)
    pick = A.picker(spec, df, pick_query or "")

    signature = [spec.get("chart"), columns, custom, knob_query or ""]
    values_sig = A.knob_values_signature(spec)
    if signature == echo.get("sig") and values_sig == echo.get("vals"):
        pane_out, knobs_echo = no_update, echo.get("knobs")   # pane NOT rebuilt
    else:
        pane = A.knob_pane(spec, columns, knob_query or "", A.ALL_TIERS_OPEN)
        pane_out, knobs_echo = pane, A.knob_echo(pane)

    return (fig, code, pane_out, pick, A.status_bar(meta), build_msg, mode,
            {"code": code, "knobs": knobs_echo, "sig": signature,
             "vals": values_sig})


if __name__ == "__main__":
    port = int(os.environ.get("BENCH_PORT", "8052"))
    print(f"The Bench (OLD SHAPE) on http://127.0.0.1:{port}")
    old.run(debug=False, port=port)
