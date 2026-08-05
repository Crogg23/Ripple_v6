"""
THE BENCH - controls.py.  One knob in, one Dash control out.

This is the right-hand pane of the Bench: the format panel. `knobs.py` reads
Plotly's own validators and hands us a tree of Knob objects. This file turns
each one into something you can click, and stacks them into the accordion.

It knows nothing about Plotly, nothing about Snowflake, and nothing about
callbacks. It builds components and hands them back. `app.py` does the wiring.


THE ID CONVENTION - app.py depends on this, read it before you write a callback
------------------------------------------------------------------------------
Every component this module makes carries a **dict id**, so `app.py` can catch
all 2,488 of them with a couple of pattern-matching callbacks instead of one
callback per knob.

Three families. The `bench` key names the family; the rest of the keys are
always the same within a family, which is what MATCH and ALL require.

    {"bench": "knob",   "path": "<dotted path>", "part": "<role>"}
    {"bench": "bucket", "bucket": "<DATA|MARK|...>", "part": "<role>"}
    {"bench": "panel",  "part": "<role>"}

Knob parts:

    "value"  the ONE editor whose `value` prop holds this knob's setting.
             Exactly one per knob. A "section" knob has none - it is a
             container, not a setting.
    "hex"    the second editor a colour knob gets: the `#rrggbb` text box.
             Same knob, same setting, different way in.
    "row"    the wrapper Div. No value. This is the styling target - it is
             what turns grey (at default) or lights up (you changed it).
    "body"   a section knob's expandable body Div. No value.

Bucket parts, all on an html.Details that carries `n_clicks`:

    "section"  the bucket itself - DATA, MARK, SCALE, ...
    "more"     that bucket's "show more"       expander (Tier 1)
    "all"      that bucket's "show everything" expander (Tier 2)
    "body"     the bucket's body Div. No n_clicks.

Panel parts:  "root", "search", "results", and "banner" when one is passed.

So the whole knob pane is two callbacks:

    @app.callback(Output("spec", "data"),
                  Input({"bench": "knob", "path": ALL, "part": ALL}, "value"),
                  State("spec", "data"))
    def knob_changed(values, spec):
        # ctx.inputs_list[0] gives you every id back, so you know which path
        # and which part fired. Use controls.coerce() to turn the widget's
        # raw value into the value Plotly actually wants.

    @app.callback(Output(controls.panel_id("results"), "children"),
                  Input(controls.panel_id("search"), "value"), ...)

Two things that will bite you if nobody says them out loud:

  1. **Do not re-render the search box.** `panel()` puts the search input
     OUTSIDE the results Div on purpose. Re-render `panel_id("results")`,
     never `panel_id("root")`, or the box loses focus on every keystroke.
  2. **A toggle's `value` is a plain bool, a multi-select's is a list.**
     Run every raw callback value through `coerce(knob, raw)` and you never
     have to remember which is which.
  3. **Size is real, and it is the whole reason `lazy=True` exists.**
     Measured on this install, `knobs.tree("bar", 4 columns)` = 2,094 knobs:
     `accordion(tree, vals)` builds 14,219 components, 1,895 knob rows and a
     4,070 KB layout payload - and Dash ships that whole payload on every
     repaint. `accordion(tree, vals, lazy=True)` builds 357 components, 39
     knob rows and 94 KB: the Tier 0 knobs and nothing else. Same shape
     across 16 trace types - 62,401 KB of layout became 1,453 KB, 43x.
     Tier 1 and Tier 2 do not EXIST as components until you ask for them.


LAZY - what app.py has to do to get that
----------------------------------------
    accordion(tree, values, ..., lazy=True, opened=opened)

`opened` is a set of string tokens - `"MARK:1"`, `"SCALE:2"` - naming the
bucket sections whose deeper tiers are materialised right now. Empty is the
first paint: Tier 0 of every bucket, nothing else.

The three expanders all carry a dict id and `n_clicks`, so ONE callback grows
that set:

    @app.callback(Output("bench-open", "data"),
                  Input({"bench": "bucket", "bucket": ALL, "part": ALL},
                        "n_clicks"),
                  State("bench-open", "data"), prevent_initial_call=True)
    def opened(_clicks, open_now):
        return list(controls.opened_with(open_now, ctx.triggered_id))

`opened_with` reads the id you were handed and returns the new token set.
Clicking a bucket header OR its "show more" both materialise Tier 1; "show
everything" materialises Tier 2. The set only ever grows within one pane -
closing a <details> hides it in the browser and costs nothing, and the set is
thrown away whenever the pane is rebuilt for a real reason (a new chart, new
columns, in or out of CUSTOM mode).

**Search never looks at `opened`.** A search that could not reach a collapsed
bucket would not be a search. It reads the TREE - plain Python objects, no
components - finds every hit in all six buckets and all three tiers, and then
builds components for the first `limit` of them. When there are more it says
so in a line you can read, rather than cutting silently.

`materialised(component)` hands back the knob paths that really exist in what
you just built, which is exactly the set the ALL-input will carry.


WHAT YOU SEE AT A GLANCE
------------------------
A knob sitting at its Plotly default is drawn grey with a dead left edge.
A knob you have actually changed gets a lit left edge, brighter text, and a
dot. That is the whole point of SPEC section 8: you should be able to look at
this pane and know what you have touched without reading a word.

Under every label is the dotted path in mono - `layout.xaxis.categoryorder`.
That is not decoration. That string is what shows up in the code pane, and
reading it here is how you learn where things live.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Iterable, Sequence

from dash import dcc, html

# =====================================================================
# THE LOOK
# ---------------------------------------------------------------------
# Same GitHub-dark surface the rest of the repo uses (viz/theme.py).
# =====================================================================

SURFACE = "#0d1117"   # the page
PANEL = "#161b22"     # the pane itself
PANEL_2 = "#0f1620"   # a changed row, lifted off the pane
INK = "#e6edf3"       # primary text
MUTED = "#8b949e"     # labels of untouched knobs, descriptions
FAINT = "#6b7684"     # the dotted path line
RULE = "#21262d"      # hairlines
ACCENT = "#3987e5"    # "you changed this"
WARN = "#c98500"      # the CUSTOM-mode banner

MONO = 'ui-monospace, SFMono-Regular, Consolas, monospace'
SANS = 'ui-sans-serif, system-ui, "Segoe UI", sans-serif'


# =====================================================================
# THE SIX BUCKETS
# ---------------------------------------------------------------------
# ATLAS section 1.1 order, verbatim. DATA and MARK live on the trace and
# change per chart type; the other four are identical for all 46 traces.
# =====================================================================

BUCKET_ORDER: tuple[str, ...] = (
    "DATA", "MARK", "SCALE", "FRAME", "INTERACTION", "MOTION",
)

BUCKET_BLURB: dict[str, str] = {
    "DATA": "which columns become which channel",
    "MARK": "what the drawn thing looks like",
    "SCALE": "how numbers and categories become space and colour",
    "FRAME": "everything around and behind the data",
    "INTERACTION": "what happens when a human touches it",
    "MOTION": "how one state becomes the next",
}

# Only DATA is open when the pane first draws. Everything else is one click.
OPEN_BY_DEFAULT = ("DATA",)

# How many search hits get built as real components before we stop and say how
# many are left. 60 is about three screens of scrolling; past that you are not
# reading the list, you are looking for a better word. Reach is not lost - the
# count of what is left is on screen and one more letter narrows it.
SEARCH_CAP = 60

# Which tier a click on each bucket expander asks for. Opening the bucket
# itself and clicking its "show more" both mean the same thing: Tier 1.
TIER_BY_PART: dict[str, int] = {
    "section": 1,     # the bucket <details>
    "more": 1,        # "show more"
    "all": 2,         # "show everything"
}

# The reverse, for building the expander ids.
PART_BY_TIER: dict[int, str] = {1: "more", 2: "all"}


# =====================================================================
# THE KNOB SHAPE
# ---------------------------------------------------------------------
# SPEC 4.5 names the fields. We duck-type on them, so knobs.py can hand us
# its own class and this still works - but having a real one here means
# controls.py can be built and tested before knobs.py exists.
# =====================================================================


@dataclass
class Knob:
    """One setting. The fields SPEC 4.5 names, plus two optional extras.

    path        dotted, always prefixed `layout.` or `trace.`
    label       the friendly name; falls back to the last path segment
    control     which widget to draw - see CONTROL_KINDS
    options     dropdown choices, flaglist flags, or df column names
    min / max   numeric bounds, when Plotly declares them
    default     what Plotly does when you don't set it. Drives the grey/lit
                distinction and nothing else.
    description a cleaned half-sentence, or "" if there isn't an honest one
    depth       how deep the path is; knobs.py uses it to pick the tier
    step        optional numeric step; we work one out if it's missing
    extras      optional flaglist escape words ('all', 'none', 'skip')
    """

    path: str
    label: str = ""
    control: str = "text"
    options: Sequence[Any] = field(default_factory=tuple)
    min: float | None = None
    max: float | None = None
    default: Any = None
    description: str = ""
    depth: int = 1
    step: float | None = None
    extras: Sequence[str] = field(default_factory=tuple)


# The nine widgets, exactly the control column of SPEC 4.1.
CONTROL_KINDS: tuple[str, ...] = (
    "dropdown",   # EnumeratedValidator
    "toggle",     # BooleanValidator
    "color",      # ColorValidator      - picker AND hex box, always
    "slider",     # NumberValidator with both bounds
    "number",     # NumberValidator without bounds, IntegerValidator, AngleValidator
    "text",       # StringValidator, AnyValidator
    "multi",      # FlaglistValidator
    "section",    # CompoundValidator   - an expandable sub-section
    "column",     # DataArrayValidator  - a dropdown of the df's columns
)

# knobs.py is expected to emit the short names above. It may not exist yet,
# and a future version may hand us the raw validator class name instead, so
# we accept both and a few obvious synonyms. Nothing here guesses at a
# Plotly property - it only translates a word we were given.
_KIND_ALIASES: dict[str, str] = {
    # validator class names, straight off type(validator).__name__
    "enumeratedvalidator": "dropdown",
    "booleanvalidator": "toggle",
    "colorvalidator": "color",
    "numbervalidator": "number",
    "integervalidator": "number",
    "anglevalidator": "number",
    "stringvalidator": "text",
    "anyvalidator": "text",
    "flaglistvalidator": "multi",
    "compoundvalidator": "section",
    "compoundarrayvalidator": "section",
    "dataarrayvalidator": "column",
    # human synonyms
    "select": "dropdown", "enum": "dropdown", "choice": "dropdown",
    "bool": "toggle", "boolean": "toggle", "switch": "toggle", "checkbox": "toggle",
    "colour": "color", "colorpicker": "color", "color picker": "color",
    "range": "slider",
    "int": "number", "integer": "number", "angle": "number",
    "number box": "number", "numberbox": "number", "num": "number",
    "string": "text", "textbox": "text", "text box": "text", "str": "text",
    "multiselect": "multi", "multi-select": "multi", "flaglist": "multi",
    "compound": "section", "subsection": "section", "sub-section": "section",
    "group": "section", "expandable": "section",
    "columns": "column", "dataarray": "column", "column dropdown": "column",
}


def kind(knob: Any) -> str:
    """Which of the nine widgets this knob wants.

    Anything we don't recognise becomes a text box rather than an exception.
    A knob you can still type into beats a pane that won't draw.
    """
    raw = str(getattr(knob, "control", "") or "").strip()
    low = raw.lower()
    if low in CONTROL_KINDS:
        got = low
    else:
        got = _KIND_ALIASES.get(low, "text")

    # A slider needs two real numbers to slide between. Plotly declares plenty
    # of bounds as `inf` (layout.width is min 10, max inf), and you cannot
    # slide to infinity - those degrade to a number box.
    if got == "slider" and not _has_bounds(knob):
        return "number"
    return got


def _has_bounds(knob: Any) -> bool:
    """True when min and max are both real, finite numbers."""
    lo, hi = getattr(knob, "min", None), getattr(knob, "max", None)
    try:
        return (lo is not None and hi is not None
                and math.isfinite(float(lo)) and math.isfinite(float(hi))
                and float(hi) > float(lo))
    except (TypeError, ValueError):
        return False


# =====================================================================
# IDS
# ---------------------------------------------------------------------
# Every id in this file goes through one of these three. Nothing builds an
# id dict by hand - if the convention ever changes it changes here.
# =====================================================================


def knob_id(path: str, part: str = "value") -> dict:
    """The id of one widget belonging to one knob. See the module docstring."""
    return {"bench": "knob", "path": str(path), "part": str(part)}


def bucket_id(bucket: str, part: str = "section") -> dict:
    """The id of one of the six accordion sections, or a piece of one."""
    return {"bench": "bucket", "bucket": str(bucket), "part": str(part)}


def panel_id(part: str) -> dict:
    """The id of a piece of the pane itself - the search box, the results Div."""
    return {"bench": "panel", "part": str(part)}


# =====================================================================
# WHICH SECTIONS ARE OPEN
# ---------------------------------------------------------------------
# One token per materialised bucket section: "MARK:1" is MARK's Tier 1.
# Strings and not tuples because this set lives in a dcc.Store, which is
# JSON - and JSON has no tuples.
# =====================================================================


def open_token(bucket: str, tier: int = 1) -> str:
    """The token naming one bucket's tier. `open_token("MARK", 1) -> "MARK:1"`."""
    return f"{bucket}:{int(tier)}"


def token_for(bucket_id_dict: Any) -> str | None:
    """The token a clicked expander is asking for, or None if it is not one.

    Hand it `ctx.triggered_id` and it works out the rest: a click on the MARK
    bucket header or on MARK's "show more" both come back as "MARK:1", and
    "show everything" comes back as "MARK:2".
    """
    if not isinstance(bucket_id_dict, dict):
        return None
    if bucket_id_dict.get("bench") != "bucket":
        return None
    tier = TIER_BY_PART.get(str(bucket_id_dict.get("part") or ""))
    bucket = bucket_id_dict.get("bucket")
    if tier is None or not bucket:
        return None
    return open_token(str(bucket), tier)


def opened_with(opened: Iterable[str] | None, bucket_id_dict: Any) -> tuple[str, ...]:
    """The open-token set, grown by whatever the user just clicked.

    Returns a sorted tuple so it is stable in a dcc.Store and a `!=` against
    the old value means something really changed. An id that is not an
    expander hands the set straight back, unchanged.

    Opening Tier 2 implies Tier 1: "show everything" sitting under an unbuilt
    "show more" would be a hole you could see through.
    """
    out = {str(t) for t in (opened or ())}
    token = token_for(bucket_id_dict)
    if token is None:
        return tuple(sorted(out))
    out.add(token)
    bucket, _, tier = token.rpartition(":")
    if tier == "2":
        out.add(open_token(bucket, 1))
    return tuple(sorted(out))


def materialised(component: Any) -> list[str]:
    """The knob paths that really exist in a built pane, sorted, no repeats.

    This is the set the pattern-matching ALL input will actually carry, so it
    is read off the components rather than re-derived from the tree - it
    cannot drift from what was rendered.

        Input({"bench": "knob", "path": ALL, "part": ALL}, "value")

    A knob with no editor at all - a column dropdown on a result with no
    columns - is honestly absent, because no widget was built for it.
    """
    out: set[str] = set()
    for node in _walk(component):
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob" \
                and cid.get("part") in ("value", "hex"):
            out.add(str(cid.get("path")))
    return sorted(out)


def _knob_paths(component: Any) -> set[str]:
    """Every knob path with ANY component in a subtree - rows and sections too.

    `materialised` answers "what will the ALL input carry?"; this answers
    "what can the human see?", which is the bigger set by exactly the section
    headers and the column dropdowns that had no columns to offer.
    """
    out: set[str] = set()
    for node in _walk(component):
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob":
            out.add(str(cid.get("path")))
    return out


def _walk(component: Any):
    """Every Dash component in a subtree, root first. Nested lists included."""
    stack = [component]
    while stack:
        node = stack.pop()
        if isinstance(node, (list, tuple)):
            stack.extend(node)
            continue
        if not hasattr(node, "_prop_names"):
            continue
        yield node
        kids = getattr(node, "children", None)
        if kids is None:
            continue
        stack.append(kids)


# =====================================================================
# DEFAULT vs CHANGED
# ---------------------------------------------------------------------
# SPEC section 3: the spec dict only ever holds non-default values, so an
# untouched knob arrives here as None. We still want the widget to SHOW the
# default - just greyed - so you can see what Plotly is doing without you.
# =====================================================================


def is_changed(knob: Any, value: Any) -> bool:
    """Has the user actually moved this knob off Plotly's default?"""
    if value is None:
        return False
    default = getattr(knob, "default", None)
    if default is None:
        # No default recorded. Anything other than blank counts as touched.
        return value not in ("", [], ())
    try:
        return bool(value != default)
    except Exception:            # exotic default (a numpy array, say)
        return True


def _shown(knob: Any, value: Any) -> Any:
    """What the widget should display: the value if set, else the default."""
    return getattr(knob, "default", None) if value is None else value


# =====================================================================
# VALUES IN AND OUT
# ---------------------------------------------------------------------
# Two widgets don't hand back the value Plotly wants. The toggle is fine
# (a bool), but a multi-select gives a list where a flaglist wants "x+y+z".
# `coerce` is the one door app.py should push every raw value through.
# =====================================================================


def coerce(knob: Any, raw: Any) -> Any:
    """Turn what the widget handed back into the value Plotly wants.

    Returns None for "unset" - an empty text box, a cleared dropdown - which
    is exactly the signal SPEC section 3 wants: drop the key from spec["knobs"].
    """
    k = kind(knob)

    if raw is None:
        return None

    if k == "multi":
        # A flaglist is a plus-joined string: 'x+y+text'. The escape words
        # ('all', 'none', 'skip') stand alone and cancel the rest.
        if isinstance(raw, str):
            raw = [p for p in raw.split("+") if p]
        if not raw:
            return None
        extras = {str(e) for e in getattr(knob, "extras", ()) or ()}
        for item in raw:
            if str(item) in extras:
                return str(item)
        return "+".join(str(p) for p in raw)

    if k in ("text", "color", "column", "dropdown"):
        if isinstance(raw, str) and raw.strip() == "":
            return None
        return raw

    if k in ("number", "slider"):
        if raw == "":
            return None
        return raw

    return raw


def _widget_value(knob: Any, value: Any) -> Any:
    """The inverse of coerce: the shape the widget wants to be handed."""
    shown = _shown(knob, value)
    if kind(knob) == "multi":
        if shown is None:
            return []
        if isinstance(shown, str):
            return [p for p in shown.split("+") if p]
        return list(shown)
    return shown


# =====================================================================
# SEARCH
# ---------------------------------------------------------------------
# SPEC 4.3: the search box cuts every tier. "I know there's a setting for
# gridlines somewhere" is the question this answers.
# =====================================================================


def matches(knob: Any, query: str) -> bool:
    """Does this knob match a search? Path, label and description all count."""
    q = (query or "").strip().lower()
    if not q:
        return True
    hay = " ".join(str(x or "") for x in (
        getattr(knob, "path", ""),
        getattr(knob, "label", ""),
        getattr(knob, "description", ""),
    )).lower()
    # Every word must appear somewhere. "axis grid" finds xaxis.gridcolor.
    return all(word in hay for word in q.split())


# =====================================================================
# THE NINE CONTROLS
# ---------------------------------------------------------------------
# One function each, all the same shape: (knob, value, disabled) -> the
# editor component only. The label, the path line and the changed marker
# are wrapped around it by `_row` below, so every control looks the same
# on the outside no matter what it is on the inside.
# =====================================================================

_INPUT_STYLE = {
    "width": "100%", "boxSizing": "border-box",
    "background": SURFACE, "color": INK,
    "border": f"1px solid {RULE}", "borderRadius": "5px",
    "padding": "5px 8px", "font": f"12px {MONO}",
}


def _dropdown(knob: Any, value: Any, disabled: bool):
    """EnumeratedValidator -> a dropdown of the legal values.

    Options come from the validator, so a wrong value is not reachable.
    Clearable, because clearing is how you go back to the default.
    """
    return dcc.Dropdown(
        id=knob_id(knob.path, "value"),
        options=_options(getattr(knob, "options", ()) or ()),
        value=_widget_value(knob, value),
        clearable=True,
        disabled=disabled,
        placeholder="default",
        className="bench-dd",
        style={"font": f"12px {MONO}"},
    )


def _toggle(knob: Any, value: Any, disabled: bool):
    """BooleanValidator -> two little pills, on and off.

    A radio rather than a checkbox on purpose: the value that comes back is
    a plain `True` / `False`, not a list of one thing.
    """
    opts = [{"label": "on", "value": True, "disabled": disabled},
            {"label": "off", "value": False, "disabled": disabled}]
    return dcc.RadioItems(
        id=knob_id(knob.path, "value"),
        options=opts,
        value=_widget_value(knob, value),
        inline=True,
        inputStyle={"marginRight": "5px", "accentColor": ACCENT},
        labelStyle={"marginRight": "14px", "color": INK if not disabled else FAINT,
                    "cursor": "pointer" if not disabled else "default"},
        style={"font": f"12px {SANS}"},
    )


def _color(knob: Any, value: Any, disabled: bool):
    """ColorValidator -> a picker AND a hex box. Always both.

    SPEC 4.1 is firm about this and it is worth saying why: the picker is how
    you find the colour, the hex box is how you learn what the generated code
    is about to say. Take the text away and the panel stops teaching.

    Two ids for one knob - `part="value"` on the picker, `part="hex"` on the
    box. app.py's ALL callback sees both and writes the same knob either way.
    """
    shown = _shown(knob, value)
    return html.Div(
        [
            dcc.Input(
                id=knob_id(knob.path, "value"),
                type="color",
                value=_as_hex(shown) or "#000000",
                disabled=disabled,
                style={"width": "38px", "height": "28px", "padding": "1px",
                       "background": SURFACE, "border": f"1px solid {RULE}",
                       "borderRadius": "5px", "flex": "none",
                       "cursor": "pointer" if not disabled else "default"},
            ),
            dcc.Input(
                id=knob_id(knob.path, "hex"),
                type="text",
                value="" if shown is None else str(shown),
                debounce=True,
                disabled=disabled,
                placeholder="#rrggbb, rgba(), or a css name",
                style={**_INPUT_STYLE, "flex": "1", "minWidth": "0"},
            ),
        ],
        style={"display": "flex", "gap": "6px", "alignItems": "center"},
    )


def _slider(knob: Any, value: Any, disabled: bool):
    """NumberValidator with both bounds -> a slider you can drag.

    No tick marks: on `marker.opacity` (0-1) they are clutter, and on
    `layout.width` there is no sensible set of them. The tooltip carries
    the number instead.
    """
    lo, hi = float(knob.min), float(knob.max)
    shown = _shown(knob, value)
    return dcc.Slider(
        id=knob_id(knob.path, "value"),
        min=lo, max=hi, step=_step(knob, lo, hi),
        value=shown if isinstance(shown, (int, float)) else lo,
        marks=None,
        disabled=disabled,
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode="mouseup",
    )


def _number(knob: Any, value: Any, disabled: bool):
    """IntegerValidator, AngleValidator, or an unbounded NumberValidator.

    A box, not a slider - you cannot drag to infinity, and `layout.width`
    honestly has no top end.
    """
    lo, hi = getattr(knob, "min", None), getattr(knob, "max", None)
    kw: dict[str, Any] = {}
    if lo is not None and math.isfinite(_num(lo, math.inf)):
        kw["min"] = float(lo)
    if hi is not None and math.isfinite(_num(hi, math.inf)):
        kw["max"] = float(hi)
    step = getattr(knob, "step", None)
    if step is not None:
        kw["step"] = step

    shown = _shown(knob, value)
    return dcc.Input(
        id=knob_id(knob.path, "value"),
        type="number",
        value=shown if isinstance(shown, (int, float)) else None,
        debounce=True,
        disabled=disabled,
        placeholder="default",
        style=_INPUT_STYLE,
        **kw,
    )


def _text(knob: Any, value: Any, disabled: bool):
    """StringValidator and AnyValidator -> a plain text box.

    `debounce=True` means it fires when you leave the box or press Enter,
    not on every keystroke. Re-rendering a figure per character is how you
    make an app feel broken.
    """
    shown = _shown(knob, value)
    return dcc.Input(
        id=knob_id(knob.path, "value"),
        type="text",
        value="" if shown is None else str(shown),
        debounce=True,
        disabled=disabled,
        placeholder="default",
        style=_INPUT_STYLE,
    )


def _multi(knob: Any, value: Any, disabled: bool):
    """FlaglistValidator -> a multi-select.

    A flaglist is Plotly's plus-joined string: `hoverinfo='x+y+text'`. You
    tick the parts, `coerce` joins them back up. The escape words ('all',
    'none', 'skip') sit in the same list and cancel everything else.
    """
    opts = list(getattr(knob, "options", ()) or ())
    opts += [e for e in (getattr(knob, "extras", ()) or ()) if e not in opts]
    return dcc.Dropdown(
        id=knob_id(knob.path, "value"),
        options=_options(opts),
        value=_widget_value(knob, value),
        multi=True,
        disabled=disabled,
        placeholder="default",
        className="bench-dd",
        style={"font": f"12px {MONO}"},
    )


def _column(knob: Any, value: Any, disabled: bool):
    """DataArrayValidator -> a dropdown of THIS dataframe's columns.

    The one bucket whose legal values come from the data rather than from
    Plotly, which is why SPEC section 3 keeps it in `mapping` and not in
    `knobs`. If the current result has no columns we say so instead of
    showing an empty list.
    """
    cols = list(getattr(knob, "options", ()) or ())
    if not cols:
        return html.Div(
            "no columns in this result",
            style={"font": f"12px {SANS}", "color": FAINT, "padding": "5px 0"},
        )
    return dcc.Dropdown(
        id=knob_id(knob.path, "value"),
        options=_options(cols),
        value=_widget_value(knob, value),
        clearable=True,
        disabled=disabled,
        placeholder="pick a column",
        className="bench-dd",
        style={"font": f"12px {MONO}"},
    )


def _section(knob: Any, value: Any, disabled: bool, children=None):
    """CompoundValidator -> an expandable sub-section holding its own knobs.

    `marker`, `line`, `title`, `legend` - the container objects. This is a
    native <details>, so opening and closing it costs no callback at all.
    """
    body = html.Div(
        children if children is not None else [],
        id=knob_id(knob.path, "body"),
        style={"padding": "2px 0 2px 12px", "marginLeft": "3px",
               "borderLeft": f"1px solid {RULE}"},
    )
    n = len(children) if children else 0
    return html.Details(
        [
            html.Summary(
                [
                    html.Span(_label(knob),
                              style={"color": MUTED, "font": f"12px {SANS}"}),
                    html.Span(f"  {n}" if n else "",
                              style={"color": FAINT, "font": f"11px {MONO}",
                                     "marginLeft": "6px"}),
                ],
                style={"cursor": "pointer", "padding": "3px 0",
                       "listStyle": "revert"},
            ),
            body,
        ],
        style={"margin": "2px 0"},
    )


_BUILDERS = {
    "dropdown": _dropdown,
    "toggle": _toggle,
    "color": _color,
    "slider": _slider,
    "number": _number,
    "text": _text,
    "multi": _multi,
    "column": _column,
}


# =====================================================================
# ONE KNOB, WRAPPED
# =====================================================================


def control(knob: Any, value: Any = None, *, children=None, disabled: bool = False):
    """Turn one Knob into one Dash component. The public entry point.

    `value` is what the spec currently holds for this path, or None when the
    knob has never been touched. None is what makes it render grey.

    `children` is only for a "section" knob - the already-rendered controls
    that live inside it. `panel()` fills this in from the tree.
    """
    k = kind(knob)

    if k == "section":
        return _section(knob, value, disabled, children=children)

    builder = _BUILDERS.get(k, _text)
    editor = builder(knob, value, disabled)
    return _row(knob, value, editor, disabled=disabled)


# _row() builds one of these on every knob row - up to ~1,895 times for one
# chart with every tier open (see the module docstring, point 3). Only two
# things ever vary: whether the knob is CHANGED and whether the pane is
# disabled (CUSTOM mode). Precomputed once so a row build shares one of these
# four dicts instead of constructing a fresh one every time; nothing in this
# file mutates a built component's `.style` in place, so sharing is safe.
_ROW_HEAD_STYLE = {"display": "flex", "alignItems": "center"}
_ROW_PATH_STYLE = {"font": f"10.5px {MONO}", "color": FAINT,
                   "margin": "1px 0 4px", "wordBreak": "break-all"}
_ROW_DESC_STYLE = {"font": f"11px/1.45 {SANS}", "color": MUTED,
                   "marginTop": "4px"}
_ROW_DOT_STYLE = {"color": ACCENT, "font": "9px sans-serif",
                  "marginLeft": "6px", "verticalAlign": "middle"}
_ROW_LABEL_STYLE = {
    False: {"color": MUTED, "font": f"12.5px {SANS}"},
    True: {"color": INK, "font": f"600 12.5px {SANS}"},
}
_ROW_STYLE = {
    (changed, disabled): {
        "padding": "7px 9px",
        "margin": "3px 0",
        "borderRadius": "5px",
        "borderLeft": f"2px solid {ACCENT if changed else 'transparent'}",
        "background": PANEL_2 if changed else "transparent",
        "opacity": "0.55" if disabled else "1",
    }
    for changed in (False, True) for disabled in (False, True)
}


def _row(knob: Any, value: Any, editor, *, disabled: bool):
    """The line around one control: label, dotted path, the editor, the marker.

    The left edge is the tell. Dead grey means Plotly's default is in charge.
    Lit blue means you changed it, and it will show up in the code pane.
    """
    changed = is_changed(knob, value)
    desc = str(getattr(knob, "description", "") or "").strip()

    head = [
        html.Span(_label(knob), style=_ROW_LABEL_STYLE[changed]),
        html.Span(
            "●" if changed else "",
            title="changed - this one is in the generated code",
            style=_ROW_DOT_STYLE,
        ),
    ]

    body = [
        html.Div(head, style=_ROW_HEAD_STYLE),
        html.Div(getattr(knob, "path", ""), style=_ROW_PATH_STYLE),
        editor,
    ]
    if desc:
        body.append(html.Div(desc, style=_ROW_DESC_STYLE))

    return html.Div(
        body,
        id=knob_id(getattr(knob, "path", ""), "row"),
        title=desc or None,
        style=_ROW_STYLE[(changed, disabled)],
    )


# =====================================================================
# THE ACCORDION
# ---------------------------------------------------------------------
# Six buckets in ATLAS order, tiered. Native <details> throughout, so
# opening a bucket or a "show more" needs no callback and no store.
# =====================================================================


def panel(tree: Any, spec_knobs: dict | None = None, *,
          mapping: dict | None = None, query: str = "",
          disabled: bool = False, banner: str | None = None,
          expanded: Iterable[str] | None = None,
          lazy: bool = False, opened: Iterable[str] | None = (),
          limit: int | None = SEARCH_CAP, tier_limit: int | None = None):
    """The whole right-hand pane: search box on top, six buckets below.

    tree        {bucket: {tier: [Knob]}} as knobs.tree() returns it
    spec_knobs  SPEC["knobs"] - dotted path -> value, non-defaults only
    mapping     SPEC["mapping"] - optional; column knobs are looked up here
                first, by the last segment of their path ('x', 'y', 'color')
    query       current search text; non-empty flattens the tiers
    disabled    CUSTOM mode - grey the lot out, read-only
    banner      one line above everything, for the CUSTOM-mode message
    expanded    which buckets get built at all. None (the default) is all six.
    lazy        build Tier 0 only, and Tier 1/2 only where `opened` says so
    opened      the open-token set - see `opened_with`
    limit       how many search hits become components before we say how many
                are left. None means no cap.
    tier_limit  the same cap on a materialised Tier 1 / Tier 2 body. None
                (the default) means you asked for that tier, you get all of it.

    Re-render `panel_id("results")`, not this. The search box is deliberately
    outside the results Div so typing in it does not destroy it.
    """
    kids: list = [search_box(query)]
    if banner:
        kids.append(
            html.Div(
                banner,
                id=panel_id("banner"),
                style={"font": f"12px {SANS}", "color": WARN,
                       "background": "rgba(201,133,0,.10)",
                       "border": f"1px solid {WARN}", "borderRadius": "5px",
                       "padding": "7px 9px", "margin": "0 0 8px"},
            )
        )
    kids.append(accordion(tree, spec_knobs, mapping=mapping, query=query,
                          disabled=disabled, expanded=expanded, lazy=lazy,
                          opened=opened, limit=limit, tier_limit=tier_limit))

    return html.Div(
        kids,
        id=panel_id("root"),
        style={"background": PANEL, "color": INK, "height": "100%",
               "overflowY": "auto", "boxSizing": "border-box",
               "padding": "12px 12px 60px", "font": f"13px {SANS}"},
    )


def search_box(query: str = ""):
    """One box over every knob path and description. SPEC 4.3's real answer
    to "I know there's a setting for this somewhere."
    """
    return html.Div(
        dcc.Input(
            id=panel_id("search"),
            type="search",
            value=query or "",
            debounce=300,
            placeholder="search every knob…",
            style={**_INPUT_STYLE, "font": f"12.5px {SANS}", "padding": "7px 10px"},
        ),
        style={"marginBottom": "10px"},
    )


def accordion(tree: Any, spec_knobs: dict | None = None, *,
              mapping: dict | None = None, query: str = "",
              disabled: bool = False, expanded: Iterable[str] | None = None,
              lazy: bool = False, opened: Iterable[str] | None = (),
              limit: int | None = SEARCH_CAP, tier_limit: int | None = None):
    """The six bucket sections. THIS is what app.py re-renders.

    THE PAYLOAD LEVER IS `lazy`, and it exists because of a measured number.
    `knobs.tree("bar", 4 columns)` is 2,094 knobs. Built whole it is 14,219
    Dash components, 1,895 knob rows and a 4,070 KB layout payload, and Dash
    ships that over the wire on every re-render. With `lazy=True` it is 357
    components, 39 knob rows and 94 KB - Tier 0, and nothing else built.

    Not hidden - ABSENT. A knob that exists but is behind a shut <details> is
    still serialised, still shipped, and still turns up in every ALL-input
    payload. That was the bug. So an unopened tier is not built.

    Reach is not lost, and it is worth being exact about how:

      * `opened` names the tiers that are materialised right now, as tokens -
        `"MARK:1"`. Every expander carries `n_clicks` and a dict id, so one
        callback grows that set through `opened_with(opened, ctx.triggered_id)`.
      * a SEARCH ignores `opened` completely. It reads the tree - plain
        objects, no components, 0.14s for the whole thing - finds every hit in
        all six buckets and all three tiers, builds the first `limit` of them
        and then SAYS how many are left. An honest line beats a silent cut.

    `lazy=False` (the default) is the old behaviour, kept because plenty of
    callers and tests want the whole tree in one object: every tier of every
    bucket named by `expanded`, or of all six when `expanded is None`.
    """
    spec_knobs = spec_knobs or {}
    buckets = _as_buckets(tree)
    q = (query or "").strip()
    want = None if expanded is None else {str(b) for b in expanded}
    open_set = {str(t) for t in (opened or ())}

    sections: list = []
    total = 0          # how many knobs matched the search, across everything
    scheduled = 0      # how many of those we handed to the renderer
    for name in _bucket_order(buckets):
        tiers = _as_tiers(buckets.get(name, {}))
        if q:
            # Search the TREE, not the components. Every tier, every bucket,
            # whether or not it is open - that is what makes it a search.
            hits = _prune_sections(
                [k for tier in (0, 1, 2) for k in tiers.get(tier, [])
                 if matches(k, q)])
            total += len(hits)
            if not hits:
                continue
            room = None if limit is None else max(0, limit - scheduled)
            build, took = _take(hits, room)
            scheduled += took
            sections.append(
                _bucket_section(name, {0: build, 1: [], 2: []},
                                spec_knobs, mapping, disabled,
                                force_open=True, found=len(hits),
                                build_tiers=(0,),
                                # the cap ran out before this bucket: say where
                                # the rest of the hits are, don't draw a header
                                # over an empty box
                                note=("" if build else
                                      f"{len(hits)} hits here — none drawn yet. "
                                      "Narrow your search."))
            )
        else:
            if not any(tiers.get(t) for t in (0, 1, 2)):
                continue
            drawn = want is None or name in want
            if not lazy:
                build_tiers = (0, 1, 2) if drawn else ()
                stub_tiers: tuple[int, ...] = ()
            else:
                build_tiers = tuple(
                    t for t in (0, 1, 2)
                    if (t == 0 and drawn) or (t and open_token(name, t) in open_set)
                )
                # An unbuilt tier still draws its "show more (732)" header, so
                # there is something to click. The body behind it is empty.
                stub_tiers = tuple(t for t in (1, 2) if t not in build_tiers)
            sections.append(
                _bucket_section(
                    name, tiers, spec_knobs, mapping, disabled,
                    force_open=(name in OPEN_BY_DEFAULT
                                or any(open_token(name, t) in open_set
                                       for t in (1, 2))),
                    build_tiers=build_tiers, stub_tiers=stub_tiers,
                    tier_limit=tier_limit, reveal=lazy)
            )

    if q:
        # Counted off the components we really built, not off what we meant to
        # build. `_render` drops a section knob whose children all missed the
        # search, so "we scheduled 60" is not the same as "60 are on screen",
        # and the number a human reads has to be the one they can scroll to.
        on_screen = len(_knob_paths(sections))
        line = (f"{total} knob{'' if total == 1 else 's'} match “{q}”"
                + ("" if total else " — try a shorter word"))
        if total > on_screen:
            line += (f" — showing {on_screen}, {total - on_screen} more. "
                     "Narrow your search.")
        sections.insert(0, html.Div(
            line,
            style={"font": f"11.5px {SANS}",
                   "color": WARN if total > on_screen else MUTED,
                   "margin": "0 0 8px"},
        ))
    if not sections:
        sections = [html.Div("no knobs for this chart yet",
                             style={"font": f"12px {SANS}", "color": FAINT})]

    return html.Div(sections, id=panel_id("results"))


def _bucket_section(name, tiers, spec_knobs, mapping, disabled, *,
                    force_open: bool, found: int | None = None,
                    build_tiers: Iterable[int] = (0, 1, 2),
                    stub_tiers: Iterable[int] = (),
                    tier_limit: int | None = None,
                    reveal: bool = False, note: str = ""):
    """One bucket: Tier 0 on top, then two nested <details> for the rest.

    `build_tiers` names the tiers whose rows are really constructed.
    `stub_tiers` names the ones that draw their expander and an empty body -
    the click target that tells app.py to materialise them next round.
    `reveal` opens a tier that was just materialised, because the user asked
    for it by clicking and a shut <details> would look like nothing happened.
    """
    t0 = list(tiers.get(0, []))
    t1 = list(tiers.get(1, []))
    t2 = list(tiers.get(2, []))
    build_tiers = set(build_tiers)
    stub_tiers = set(stub_tiers) - build_tiers
    # Counted off the TREE, so a collapsed bucket still tells you the truth
    # about how many of its knobs you have touched.
    n_changed = sum(1 for k in (t0 + t1 + t2)
                    if is_changed(k, _value_for(k, spec_knobs, mapping)))

    body: list = [
        html.Div(BUCKET_BLURB.get(name, ""),
                 style={"font": f"11px {SANS}", "color": FAINT,
                        "margin": "2px 0 6px 2px"}),
    ]
    if note:
        body.append(html.Div(note, style={"font": f"11px {SANS}", "color": WARN,
                                          "padding": "2px 0 4px"}))
    if 0 in build_tiers:
        body.append(html.Div(_render(t0, spec_knobs, mapping, disabled)))
    for tier, label, knobs_at_tier in ((1, "show more", t1),
                                       (2, "show everything", t2)):
        if not knobs_at_tier:
            continue
        if tier in build_tiers:
            kept, over = _cap(knobs_at_tier, tier_limit)
            body.append(_more(name, tier, label, len(knobs_at_tier),
                              _render(kept, spec_knobs, mapping, disabled),
                              is_open=reveal, overflow=over))
        elif tier in stub_tiers:
            body.append(_more(name, tier, label, len(knobs_at_tier), [],
                              is_open=False))

    count = found if found is not None else len(t0) + len(t1) + len(t2)
    return html.Details(
        [
            html.Summary(
                [
                    html.Span(name, style={"font": f"600 12px {SANS}",
                                           "letterSpacing": ".08em",
                                           "color": INK}),
                    html.Span(f"  {count}",
                              style={"font": f"11px {MONO}", "color": FAINT,
                                     "marginLeft": "8px"}),
                    html.Span(f"  {n_changed} changed" if n_changed else "",
                              style={"font": f"11px {MONO}", "color": ACCENT,
                                     "marginLeft": "8px"}),
                ],
                style={"cursor": "pointer", "padding": "6px 2px",
                       "listStyle": "revert"},
            ),
            html.Div(body, id=bucket_id(name, "body"),
                     style={"padding": "0 0 6px 6px"}),
        ],
        id=bucket_id(name, "section"),
        open=bool(force_open),
        n_clicks=0,          # so app.py can hear a bucket being opened
        style={"borderTop": f"1px solid {RULE}", "padding": "2px 0"},
    )


def _prune_sections(hits: list) -> list:
    """Drop a matched section that has no matched child in this result.

    A section knob is a container, not a setting - `trace.marker` matching
    "marker" is not a knob you can turn. `_render` already refuses to draw an
    empty expander, so leaving them in the hit list would inflate the count a
    human reads AND eat slots in the cap that never become anything on screen.
    Measured on a "color" search over `bar`: 60 slots spent, 44 widgets drawn.
    """
    reachable: set[str] = set()
    for k in hits:
        if kind(k) == "section":
            continue
        parts = str(getattr(k, "path", "")).split(".")
        for cut in range(1, len(parts)):
            reachable.add(".".join(parts[:cut]))
    return [k for k in hits
            if kind(k) != "section" or str(getattr(k, "path", "")) in reachable]


def _take(hits: list, room: int | None) -> tuple[list, int]:
    """The first `room` SETTINGS out of a hit list, plus the sections holding them.

    Only real settings are counted against the cap. A section knob rides along
    free, because it is furniture rather than a knob you can turn - counting it
    would mean a search for "color" spent 16 of its 60 slots on expander
    headers and put 44 widgets on screen instead of 60. Measured: it did.

    Returns (what to build, how many settings that used up).
    """
    if room is None:
        return list(hits), sum(1 for k in hits if kind(k) != "section")
    taken: list = []
    leaves = 0
    for knob in hits:
        if leaves >= room:
            break
        taken.append(knob)
        if kind(knob) != "section":
            leaves += 1
    return _prune_sections(taken), leaves


def _cap(knobs: list, limit: int | None) -> tuple[list, int]:
    """The first `limit` knobs, and how many were left behind."""
    if limit is None or len(knobs) <= limit:
        return list(knobs), 0
    return list(knobs[:limit]), len(knobs) - limit


def _more(bucket: str, tier: int, label: str, n: int, children, *,
          is_open: bool = False, overflow: int = 0):
    """A 'show more (37)' expander, with an id so app.py can hear the click.

    Native <details> opens itself with no callback - but an EMPTY one has
    nothing to open onto, which is why it carries `n_clicks` and a dict id.
    app.py adds the tier to its open set, re-renders, and the rows are there.
    """
    inside: list = [html.Div(children)]
    if overflow:
        inside.append(html.Div(
            f"{overflow} more here — search to reach them",
            style={"font": f"11px {SANS}", "color": WARN, "padding": "4px 0"},
        ))
    return html.Details(
        [
            html.Summary(
                f"{label}  ({n})",
                style={"cursor": "pointer", "font": f"11.5px {SANS}",
                       "color": MUTED, "padding": "5px 0", "listStyle": "revert"},
            ),
            *inside,
        ],
        id=bucket_id(bucket, PART_BY_TIER.get(tier, "more")),
        open=bool(is_open),
        n_clicks=0,
        style={"marginTop": "4px"},
    )


def _render(knobs: Iterable[Any], spec_knobs, mapping, disabled) -> list:
    """Render a flat list of knobs, nesting each one under its section parent."""
    out = []
    for node_knob, node_children in _nest(list(knobs)):
        if kind(node_knob) == "section":
            kids = _render(node_children, spec_knobs, mapping, disabled)
            if not kids:
                continue          # an empty expander teaches nobody anything
            out.append(control(node_knob, None, children=kids, disabled=disabled))
        else:
            out.append(control(node_knob,
                               _value_for(node_knob, spec_knobs, mapping),
                               disabled=disabled))
    return out


def _nest(knobs: list) -> list[tuple[Any, list]]:
    """Split a flat knob list into (top-level knob, everything under it).

    `trace.marker` is a section; `trace.marker.color` and `trace.marker.size`
    go inside it. A knob whose section parent is not in this list stays at
    the top level rather than disappearing.

    THE PAYLOAD IS THE WHOLE SUBTREE, NOT THE DIRECT CHILDREN, and that is a
    bug fix rather than a flourish. `_render` recurses through this function,
    so handing back direct children only meant a grandchild was assigned to a
    section that was itself not a root - and its list was then thrown away.
    Reproduced on a search for "color" over the `bar` tree: 14 knobs under
    `trace.marker.colorbar.tickfont` and `.tickformatstopdefaults` matched,
    were selected, and never appeared, and the empty expanders holding them
    were dropped too. A search that cannot reach a knob is not a search.
    Each knob still renders exactly once: only the outermost section is a root
    here, and re-nesting inside it picks the next level down the same way.
    """
    sections = {str(getattr(k, "path", "")): k for k in knobs
                if kind(k) == "section"}
    under: dict[str, list] = {p: [] for p in sections}
    roots: list = []

    for k in knobs:
        path = str(getattr(k, "path", ""))
        parts = path.split(".")
        owned = False
        for cut in range(1, len(parts)):             # every section ancestor
            candidate = ".".join(parts[:cut])
            if candidate in sections and candidate != path:
                under[candidate].append(k)
                owned = True
        if not owned:
            roots.append(k)

    return [(k, under.get(str(getattr(k, "path", "")), [])) for k in roots]


def _value_for(knob: Any, spec_knobs: dict, mapping: dict | None):
    """Where this knob's current value lives.

    Column knobs read SPEC["mapping"] first - it is keyed by channel ('x',
    'y', 'color'), which is the last segment of the path. Everything else
    reads SPEC["knobs"] by the full dotted path.
    """
    path = str(getattr(knob, "path", ""))
    if mapping and kind(knob) == "column":
        channel = path.rsplit(".", 1)[-1]
        if channel in mapping:
            return mapping[channel]
    return (spec_knobs or {}).get(path)


# =====================================================================
# SMALL HELPERS
# =====================================================================


def _label(knob: Any) -> str:
    """The friendly name, or the last bit of the path if nobody wrote one."""
    lab = str(getattr(knob, "label", "") or "").strip()
    if lab:
        return lab
    return str(getattr(knob, "path", "")).rsplit(".", 1)[-1] or "(unnamed)"


def _build_options(values: Sequence[Any]) -> list[dict]:
    out = []
    for v in values:
        if isinstance(v, dict) and "value" in v:      # already an option dict
            out.append(v)
        elif isinstance(v, bool) or isinstance(v, (str, int, float)):
            out.append({"label": str(v), "value": v})
    return out


@lru_cache(maxsize=512)
def _options_cached(values: tuple) -> tuple[dict, ...]:
    return tuple(_build_options(values))


def _options(values: Iterable[Any]) -> list[dict]:
    """Dropdown options from a bare list.

    SPEC 4.1: drop the non-str/bool oddities. Some Plotly enums carry regex
    objects and other non-JSON things that would break the wire.

    Plotly's enum vocabularies (94 named colorscales, categoryorder's 18
    values, ...) are fixed for the life of the process and recur across many
    knobs and many renders, so the common case is cached. `values` is
    materialised once so the same list still works when caching a particular
    call is impossible - an "already an option dict" entry (line above) is
    unhashable, so that one call falls back to building fresh, uncached.
    """
    values = list(values)
    try:
        return list(_options_cached(tuple(values)))
    except TypeError:
        return _build_options(values)


def _num(v: Any, fallback: float) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return fallback


def _step(knob: Any, lo: float, hi: float) -> float:
    """A step size that feels right for the span, unless the knob names one."""
    given = getattr(knob, "step", None)
    if given:
        return given
    span = hi - lo
    if span <= 2:
        return 0.01
    if span <= 20:
        return 0.1
    return 1


_CSS_NAMES = {          # just enough to keep the picker honest on common ones
    "white": "#ffffff", "black": "#000000", "red": "#ff0000", "blue": "#0000ff",
    "green": "#008000", "grey": "#808080", "gray": "#808080",
    "orange": "#ffa500", "yellow": "#ffff00", "purple": "#800080",
}


def _as_hex(value: Any) -> str | None:
    """Best-effort `#rrggbb` for the native colour picker.

    The picker only speaks `#rrggbb`. Plotly happily takes `rgba(0,0,0,0)`,
    `red`, and `#abc` too - so the hex TEXT box keeps whatever you actually
    typed, and this only feeds the swatch. If we can't read it, the swatch
    goes black and the text box still tells the truth.
    """
    if not isinstance(value, str):
        return None
    s = value.strip().lower()
    if s in _CSS_NAMES:
        return _CSS_NAMES[s]
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3 and all(c in "0123456789abcdef" for c in h):
            return "#" + "".join(c * 2 for c in h)
        if len(h) in (6, 8) and all(c in "0123456789abcdef" for c in h[:6]):
            return "#" + h[:6]
        return None
    if s.startswith("rgb"):
        inside = s[s.find("(") + 1: s.find(")")] if "(" in s and ")" in s else ""
        parts = [p.strip() for p in inside.split(",")[:3]]
        try:
            rgb = [max(0, min(255, int(round(float(p))))) for p in parts]
        except (TypeError, ValueError):
            return None
        if len(rgb) != 3:
            return None
        return "#%02x%02x%02x" % tuple(rgb)
    return None


def _as_buckets(tree: Any) -> dict:
    """Accept a KnobTree object or a plain dict. Never raise on a shape."""
    if tree is None:
        return {}
    if isinstance(tree, dict):
        return tree
    for attr in ("buckets", "tree", "data"):
        got = getattr(tree, attr, None)
        if isinstance(got, dict):
            return got
    return {}


def _bucket_order(buckets: dict) -> list[str]:
    """ATLAS order first; anything unexpected gets listed after, not dropped."""
    known = [b for b in BUCKET_ORDER if b in buckets]
    extra = [b for b in buckets if b not in BUCKET_ORDER]
    return known + sorted(str(e) for e in extra)


def _as_tiers(tiers: Any) -> dict[int, list]:
    """Normalise tier keys. 0 / '0' / 'tier0' / 'Tier 0' all mean tier zero."""
    out: dict[int, list] = {0: [], 1: [], 2: []}
    if not isinstance(tiers, dict):
        return out
    for key, knobs in tiers.items():
        digits = "".join(c for c in str(key) if c.isdigit())
        try:
            t = int(digits)
        except ValueError:
            t = 2
        out.setdefault(min(max(t, 0), 2), []).extend(list(knobs or []))
    return out


# =====================================================================
# THE ONE BIT OF CSS
# ---------------------------------------------------------------------
# Everything else in this file is inline styles, house-style. dcc.Dropdown
# is the exception: it renders its own react-select markup and cannot be
# reached with a `style=` dict, so a dark dropdown needs real CSS.
#
# app.py should drop this into `assets/bench.css`, or inline it via
# `app.index_string`. Without it the pane still works - the dropdowns are
# just white boxes on a dark pane.
# =====================================================================

PANEL_CSS = """
.bench-dd .Select-control,
.bench-dd .Select-menu-outer,
.bench-dd .Select-menu {
  background: #0d1117 !important;
  border-color: #21262d !important;
  color: #e6edf3 !important;
}
.bench-dd .Select-value-label,
.bench-dd .Select-placeholder,
.bench-dd .Select-input > input { color: #e6edf3 !important; }
.bench-dd .Select-placeholder { color: #6b7684 !important; }
.bench-dd .Select-option { background: #0d1117 !important; color: #e6edf3 !important; }
.bench-dd .Select-option.is-focused { background: #161b22 !important; }
.bench-dd .Select-arrow { border-top-color: #8b949e !important; }
.bench-dd .Select--multi .Select-value {
  background: #161b22 !important;
  border-color: #21262d !important;
  color: #e6edf3 !important;
}
.bench-dd .Select--multi .Select-value-icon { border-right-color: #21262d !important; }

/* the accordion triangles, so they read as grey furniture not as text */
summary::marker { color: #6b7684; }
summary:focus { outline: none; }

/* the pane's own scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #21262d; border-radius: 5px; }
::-webkit-scrollbar-track { background: transparent; }
"""


# =====================================================================
# SELF-TEST
# ---------------------------------------------------------------------
#   python bench/controls.py
# Builds one of every control type, checks the ids, then builds a whole
# panel from a fake six-bucket, three-tier tree.
# =====================================================================

if __name__ == "__main__":       # pragma: no cover
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from tests.test_bench_controls import main

    raise SystemExit(main())
