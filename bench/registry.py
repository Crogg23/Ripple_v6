#!/usr/bin/env python
"""
THE REGISTRY - every chart on The Wall, turned into a template you can point
at a real DataFrame.

SPEC section 6. This module is the answer to one question:

    "I have these columns. Which of the 145 charts can I actually draw,
     and if I can't draw one, WHY not?"

WHAT A TEMPLATE IS
------------------
`bench/wall.py` already holds every chart with its section, name, one-line
call, data shape and use-when. It is the source of truth for that metadata and
this file does not retype a word of it - it looks each chart up by name and
fails loudly at import time if a name drifts.

What this file ADDS, per chart:

    key         a stable slug you can put in a URL or a state object
    required    the mapping slots the chart cannot be drawn without
    optional    the slots that make it better but are not load-bearing
    trace_type  which trace knobs.py introspects for the MARK bucket, written
                the way Plotly writes it - "bar", "sankey", "scattermap".
                `.trace_class` gives you the "Bar" / "Sankey" spelling if you
                want `go.<Trace>` directly.
    builder     builder(df, mapping, knobs) -> go.Figure

A "slot" is one channel of the chart - x, y, colour, source, target, value -
and it names the ROLE of column it needs: a number, a category, a date, a
place code, a latitude, a longitude. That is what lets the picker grey out a
chart AND say why in a sentence a human learns something from.

THE ROLES
---------
The spec names four: numeric / category / date / geo. `geo` is split three
ways here, because a map has to know which column is which:

    numeric   a number you can measure with
    category  a label - a name, a code, a bucket
    date      a real datetime column
    geo       a place code a map can look up (state code, ISO country, FIPS)
    lat       a latitude column
    lon       a longitude column
    any       anything at all (a table takes any column)

A column can hold several roles at once. A latitude is numeric AND lat. A
state code is category AND geo. An integer year is numeric AND category,
because Plotly will happily treat it as either.

HOW app.py USES THIS
--------------------
    import bench.registry as reg

    r     = reg.roles(df)                       # column -> {roles}
    ok, why = reg.drawable(r, reg.CHARTS["sankey"])
    m     = reg.auto_map(r, reg.CHARTS["sankey"])
    fig   = reg.CHARTS["sankey"].builder(df, m, spec["knobs"])

`why` is never empty. On a no it teaches; on a yes it names the columns it
picked.

THE THREE SEAMS TO THE OTHER MODULES
------------------------------------
    registry.trace_type(key)        knobs.py calls this to decide which trace
                                    to introspect (bench/knobs.py trace_type_for)
    registry.build(key, df, **map)  the function codegen.py writes into the
                                    generated code for charts with no px route
    registry.roles(df) also accepts bench.data.column_roles(df) output, so the
                                    data lane and the picker speak one language
"""

from __future__ import annotations

import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Let `python bench/registry.py` work as well as `python -m bench.registry`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# wall.py is the metadata source AND the demo-data source. Importing it also
# registers the dark "wall" template and makes it the plotly default - that is
# a side effect the app inherits, and it is the look the whole Bench uses.
from bench import wall  # noqa: E402

__all__ = [
    "NUM", "CAT", "DATE", "GEO", "LAT", "LON", "ANY",
    "Slot", "ChartTemplate",
    "TEMPLATES", "CHARTS", "BY_SECTION", "SECTIONS", "PX_PURE",
    "roles", "describe", "drawable", "auto_map", "search",
    "trace_type", "build",
]

# The 49 trace names Plotly registers, mapped to their go class names. Read off
# this install, never typed out.
TRACE_CLASSES: dict[str, str] = dict(go.Figure()._data_validator.class_strs_map)


# =====================================================================
# ROLES - what kind of column is this?
# =====================================================================

NUM = "numeric"
CAT = "category"
DATE = "date"
GEO = "geo"
LAT = "lat"
LON = "lon"
ANY = "any"

# Column-name words that mean "this holds a place a map can find".
_PLACE_WORDS = {
    "state", "states", "country", "countries", "nation", "province",
    "iso", "iso2", "iso3", "fips", "county", "counties",
    "zip", "zipcode", "postcode", "location", "locations", "place",
}
_LAT_WORDS = {"lat", "latitude", "lats", "y_lat"}
_LON_WORDS = {"lon", "lng", "long", "longitude", "lons", "x_lon"}

# An integer column with few distinct values (a year, a FIPS band, a team id)
# is a category as much as it is a number. Above this it is just a number.
_INT_CATEGORY_MAX = 25


def _tokens(name: str) -> set[str]:
    """Split a column name into lowercase words. 'START_LAT' -> {'start','lat'}."""
    out, buf = set(), ""
    for ch in str(name).lower():
        if ch.isalnum():
            buf += ch
        elif buf:
            out.add(buf)
            buf = ""
    if buf:
        out.add(buf)
    return out


def _looks_like_place_codes(s: pd.Series) -> bool:
    """True when most values are short uppercase codes - 'CA', 'TX', 'USA'."""
    vals = s.dropna().astype(str).head(200)
    if len(vals) < 3:
        return False
    hits = sum(1 for v in vals if 2 <= len(v) <= 3 and v.isalpha() and v.isupper())
    return hits / len(vals) >= 0.8


def roles(df: pd.DataFrame) -> dict[str, set[str]]:
    """
    Read a DataFrame and say what each column COULD be used as.

    Returns {column_name: {role, role, ...}}. This is the `df_roles` argument
    every other function in this module takes, so you compute it once per
    result set and pass it around.
    """
    out: dict[str, set[str]] = {}
    for col in df.columns:
        s = df[col]
        got: set[str] = {ANY}
        tok = _tokens(col)

        if pd.api.types.is_datetime64_any_dtype(s):
            got.add(DATE)
        elif pd.api.types.is_bool_dtype(s):
            got.add(CAT)
        elif pd.api.types.is_numeric_dtype(s):
            got.add(NUM)
            if pd.api.types.is_integer_dtype(s) and s.nunique(dropna=True) <= _INT_CATEGORY_MAX:
                got.add(CAT)
            if tok & _LAT_WORDS and s.dropna().between(-90, 90).all():
                got.add(LAT)
                got.add(GEO)
            if tok & _LON_WORDS and s.dropna().between(-180, 180).all():
                got.add(LON)
                got.add(GEO)
        else:
            got.add(CAT)
            if tok & _PLACE_WORDS or _looks_like_place_codes(s):
                got.add(GEO)

        out[col] = got
    return out


# bench/data.py sorts columns into buckets instead: {"numeric": [...],
# "geo_state": [...], "year": [...]}. Same idea, other way up. This is the
# translation, so the data lane and the picker never disagree about a column.
_DATA_BUCKET_ROLES: dict[str, set[str]] = {
    "numeric": {NUM},
    "category": {CAT},
    "date": {DATE},
    "geo_state": {CAT, GEO},
    "year": {NUM, CAT},
    "empty": set(),
}


def _as_roles(x) -> dict[str, set[str]]:
    """
    Take whatever the caller has and give back {column: {roles}}.

    Accepts a DataFrame, this module's own roles dict, or the bucket dict
    bench.data.column_roles() returns. Nobody has to remember which.
    """
    if isinstance(x, pd.DataFrame):
        return roles(x)
    if not x:
        return {}
    first = next(iter(x.values()))
    if isinstance(first, (list, tuple)):          # data.py's bucket shape
        out: dict[str, set[str]] = {}
        for bucket, cols in x.items():
            for col in cols:
                got = out.setdefault(col, {ANY})
                got.update(_DATA_BUCKET_ROLES.get(bucket, {CAT}))
                # data.py has no lat/lon bucket, so a map would never light up
                # coming through this door. The column NAME is all we have here
                # - no values to range-check - so this is a name-only read.
                tok = _tokens(col)
                if NUM in got and tok & _LAT_WORDS:
                    got |= {LAT, GEO}
                if NUM in got and tok & _LON_WORDS:
                    got |= {LON, GEO}
        return out
    return {c: set(r) | {ANY} for c, r in x.items()}


_NUMBER_WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven",
                 "eight", "nine", "ten", "eleven", "twelve"]


def _count_word(n: int) -> str:
    return _NUMBER_WORDS[n] if n < len(_NUMBER_WORDS) else str(n)


def _plural(n: int, one: str, many: str) -> str:
    return f"{_count_word(n)} {one if n == 1 else many}"


def _join(parts: Sequence[str]) -> str:
    """'a', 'b', 'c' -> 'a, b and c'. The plain-English list."""
    parts = [p for p in parts if p]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def describe(df_roles: Mapping[str, set[str]]) -> str:
    """
    One plain sentence fragment saying what this result actually holds.

    "one category column and two numbers" - the right-hand half of every
    can't-draw-this reason.
    """
    n_num = sum(1 for r in df_roles.values() if NUM in r)
    n_cat = sum(1 for r in df_roles.values() if CAT in r)
    n_date = sum(1 for r in df_roles.values() if DATE in r)
    n_geo = sum(1 for r in df_roles.values() if GEO in r and LAT not in r and LON not in r)
    n_lat = sum(1 for r in df_roles.values() if LAT in r)
    n_lon = sum(1 for r in df_roles.values() if LON in r)

    parts = []
    if n_cat:
        parts.append(_plural(n_cat, "category column", "category columns"))
    if n_num:
        parts.append(_plural(n_num, "number", "numbers"))
    if n_date:
        parts.append(_plural(n_date, "date column", "date columns"))
    if not parts:
        return "no usable columns at all"

    tail = ""
    if n_lat and n_lon:
        tail = " (a latitude and a longitude among them)"
    elif n_geo:
        tail = f" ({_plural(n_geo, 'place-code column', 'place-code columns')} among them)"

    # A column can be two things at once - an integer year is a number AND a
    # category - so the roles can outnumber the columns. Say so, or "two
    # category columns and one number" on a two-column result reads like a lie.
    if n_cat + n_num + n_date > len(df_roles):
        tail += f", from {_plural(len(df_roles), 'column', 'columns')} in all"

    return _join(parts) + tail


# =====================================================================
# SLOTS AND TEMPLATES
# =====================================================================


@dataclass(frozen=True)
class Slot:
    """
    One channel of a chart, and the kind of column it eats.

    name   the key in the mapping dict, e.g. "x", "source", "value"
    role   one of the role constants above
    says   how to say this slot out loud: "a source column". Used verbatim
           inside the grey-out reason, so write it like a human.
    many   True when the slot takes a LIST of columns (dimensions, path)
    min_n  how many columns a `many` slot needs before the chart can draw
    """

    name: str
    role: str
    says: str
    many: bool = False
    min_n: int = 1


@dataclass
class ChartTemplate:
    """One of the charts, ready to be pointed at a DataFrame."""

    key: str
    name: str
    section: str
    call: str
    shape: str
    use_when: str
    note: str
    trace_type: str
    required: tuple[Slot, ...] = ()
    optional: tuple[Slot, ...] = ()
    build: Callable[[pd.DataFrame, dict], go.Figure] | None = None
    wall_fn: Callable[[], go.Figure] | None = None
    # Set when the chart draws a shape a SQL result cannot carry (pixels, a
    # geojson, a triangulation). It ignores the df and draws wall.py's demo.
    demo_only: bool = False
    demo_why: str = ""
    # Set when the chart cannot render on this machine at all (missing package).
    blocked: str = ""
    height: int = 340

    # -- slot helpers -------------------------------------------------

    @property
    def trace_class(self) -> str:
        """"bar" -> "Bar". The name to hand `getattr(go, ...)`."""
        return TRACE_CLASSES[self.trace_type]

    @property
    def slots(self) -> tuple[Slot, ...]:
        return tuple(self.required) + tuple(self.optional)

    def slot(self, name: str) -> Slot | None:
        for s in self.slots:
            if s.name == name:
                return s
        return None

    def blank_mapping(self) -> dict[str, Any]:
        """Every declared slot, all empty. The starting SPEC['mapping']."""
        return {s.name: ([] if s.many else None) for s in self.slots}

    def normalise(self, mapping: Mapping[str, Any] | None) -> dict[str, Any]:
        """Keep only slots this chart declares; fill the rest with None."""
        clean = self.blank_mapping()
        for s in self.slots:
            v = (mapping or {}).get(s.name)
            if v is None:
                continue
            if s.many:
                clean[s.name] = [v] if isinstance(v, str) else list(v)
            else:
                clean[s.name] = v
        return clean

    def missing(self, mapping: Mapping[str, Any] | None) -> list[Slot]:
        """Required slots that are still empty."""
        clean = self.normalise(mapping)
        out = []
        for s in self.required:
            v = clean[s.name]
            if s.many:
                if len(v) < s.min_n:
                    out.append(s)
            elif not v:
                out.append(s)
        return out

    # -- the two things you actually call -----------------------------

    def builder(
        self,
        df: pd.DataFrame,
        mapping: Mapping[str, Any] | None = None,
        knobs: Mapping[str, Any] | None = None,
    ) -> go.Figure:
        """
        Draw this chart from a real DataFrame.

        `mapping` is SPEC['mapping'] - slot name to column name.
        `knobs`   is SPEC['knobs']   - dotted paths like "layout.barmode" to
                  values. They are applied with the same underscore flattening
                  codegen writes, so the figure and the printed code agree.
        """
        if self.blocked:
            return _message_figure(f"{self.name} cannot render here", self.blocked)

        if self.demo_only:
            fig = self.wall_fn()
        else:
            clean = self.normalise(mapping)
            gaps = self.missing(clean)
            if gaps:
                raise ValueError(
                    f"{self.name} still needs {_join([s.says for s in gaps])}. "
                    f"Fill those mapping slots first."
                )
            fig = self.build(df, clean)

        _apply_knobs(fig, knobs)
        return fig

    def demo_figure(self) -> go.Figure:
        """wall.py's original, untouched. The reference picture."""
        if self.blocked:
            return _message_figure(f"{self.name} cannot render here", self.blocked)
        return self.wall_fn()


def message_figure(title: str, body: str = "", *, width: int = 62,
                   color: str | None = None,
                   margin: bool = False) -> go.Figure:
    """An empty figure that explains itself. Never a blank rectangle.

    The one implementation - app.py used to carry a near-identical copy and
    the two drifted; now app.py calls this with its own colour and margins.
    """
    text = f"<b>{title}</b>"
    if body:
        text += "<br><br>" + "<br>".join(_wrap(body, width))
    fig = go.Figure()
    font = dict(size=12) if color is None else dict(size=12, color=color)
    fig.add_annotation(text=text, xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, align="center", font=font)
    fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False),
                      **({"margin": dict(l=30, r=30, t=30, b=30)} if margin else {}))
    return fig


def _message_figure(title: str, body: str) -> go.Figure:
    return message_figure(title, body)


def _wrap(text: str, width: int) -> list[str]:
    """Break a sentence into lines. No textwrap import for four lines of work."""
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def _apply_knobs(fig: go.Figure, knobs: Mapping[str, Any] | None) -> None:
    """
    Push SPEC['knobs'] onto a figure.

    "trace.marker.opacity" becomes fig.update_traces(marker_opacity=...)
    "layout.barmode"       becomes fig.update_layout(barmode=...)

    One knob at a time, so one bad path warns instead of killing the chart.
    That matters in a UI: a typo in the code panel should show you a message,
    not a stack trace.
    """
    for path, value in (knobs or {}).items():
        try:
            if path.startswith("trace."):
                fig.update_traces(**{path[6:].replace(".", "_"): value})
            elif path.startswith("layout."):
                fig.update_layout(**{path[7:].replace(".", "_"): value})
            else:
                warnings.warn(f"knob path must start with 'trace.' or 'layout.': {path}")
        except Exception as exc:  # noqa: BLE001 - a bad knob is a message, not a crash
            warnings.warn(f"knob {path}={value!r} did not apply: {type(exc).__name__}: {exc}")


# =====================================================================
# CAN I DRAW THIS?
# =====================================================================


def _candidates(slot: Slot, df_roles: Mapping[str, set[str]]) -> list[str]:
    """Columns that could fill this slot."""
    if slot.role == ANY:
        return list(df_roles)
    return [c for c, r in df_roles.items() if slot.role in r]


def _expand(slots: Iterable[Slot]) -> list[Slot]:
    """A `many` slot needing 3 columns becomes 3 ordinary slots for matching."""
    out = []
    for s in slots:
        out.extend([s] * (s.min_n if s.many else 1))
    return out


def _assign(slots: Sequence[Slot], df_roles: Mapping[str, set[str]]) -> dict[int, str] | None:
    """
    Give every slot its own distinct column, or say it cannot be done.

    This is a tiny bipartite matching, done in two passes per slot.

    Pass one takes the first FREE column that fits. That is what keeps the
    obvious answer obvious: on a date/open/high/low/close table the `open`
    slot gets `open`, not whatever a clever algorithm shuffled it to.

    Pass two only runs when nothing is free, and bumps a column off an earlier
    slot if that slot can move somewhere else. Plain greedy would give up
    there and grey out a chart that was perfectly drawable, so a no from this
    function is a real no.
    """
    cand = {i: _candidates(s, df_roles) for i, s in enumerate(slots)}
    used: dict[str, int] = {}  # column -> slot index

    def try_slot(i: int, seen: set[str]) -> bool:
        for col in cand[i]:  # pass one: anything nobody has taken
            if col not in used and col not in seen:
                seen.add(col)
                used[col] = i
                return True
        for col in cand[i]:  # pass two: ask the current holder to move
            if col in seen:
                continue
            seen.add(col)
            if try_slot(used[col], seen):
                used[col] = i
                return True
        return False

    for i in range(len(slots)):
        if not try_slot(i, set()):
            return None
    return {i: col for col, i in used.items()}


def drawable(
    df_roles: Mapping[str, set[str]] | pd.DataFrame,
    chart: ChartTemplate | str,
) -> tuple[bool, str]:
    """
    Can this chart be drawn from a result with these columns - and why not?

    Returns (ok, reason). The reason is never empty and never jargon:

        drawable(r, CHARTS["sankey"])
        (False, "Sankey diagram needs a source column, a target column and a
                 value column - this result has one category column and one
                 number.")

    Pass a DataFrame, the dict from `roles(df)`, or the bucket dict from
    `bench.data.column_roles(df)`. All three work.
    """
    df_roles = _as_roles(df_roles)
    if isinstance(chart, str):
        chart = CHARTS[chart]

    if chart.blocked:
        return False, f"{chart.name} cannot render on this machine. {chart.blocked}"

    if chart.demo_only:
        return True, (
            f"{chart.name} draws its own built-in shape - {chart.demo_why} "
            f"Your columns are not used."
        )

    if not chart.required:
        return True, f"{chart.name} needs nothing from your columns - it always draws."

    slots = _expand(chart.required)
    picked = _assign(slots, df_roles)
    if picked is None:
        needs = _join([s.says for s in chart.required])
        return False, f"{chart.name} needs {needs} - this result has {describe(df_roles)}."

    named = []
    for i, s in enumerate(slots):
        named.append(f"{s.name} = {picked[i]}")
    return True, f"{chart.name} can draw: {_join(named)}."


def auto_map(
    df_roles: Mapping[str, set[str]] | pd.DataFrame,
    chart: ChartTemplate | str,
) -> dict[str, Any]:
    """
    A first-guess mapping: fill every required slot, then any optional ones
    that still have a spare column of the right kind.

    This is what the picker hands app.py the moment you click a chart, so
    something draws immediately instead of an empty pane with six dropdowns.
    """
    df_roles = _as_roles(df_roles)
    if isinstance(chart, str):
        chart = CHARTS[chart]

    out = chart.blank_mapping()
    if chart.demo_only or chart.blocked:
        return out

    req = _expand(chart.required)
    picked = _assign(req, df_roles)
    if picked is None:
        return out

    taken: set[str] = set(picked.values())
    for i, s in enumerate(req):
        if s.many:
            out[s.name].append(picked[i])
        else:
            out[s.name] = picked[i]

    # Top up the list-slots with anything else that fits - a correlation
    # matrix wants ALL the numbers, not the two it strictly needs.
    for s in chart.required:
        if s.many:
            for col in _candidates(s, df_roles):
                if col not in taken and len(out[s.name]) < 8:
                    out[s.name].append(col)
                    taken.add(col)

    # Then optional slots, in declaration order, out of what is left.
    for s in chart.optional:
        for col in _candidates(s, df_roles):
            if col in taken:
                continue
            if s.many:
                if len(out[s.name]) < 8:
                    out[s.name].append(col)
                    taken.add(col)
            else:
                out[s.name] = col
                taken.add(col)
                break
    return out


def search(text: str) -> list[ChartTemplate]:
    """
    Find charts by anything printed about them - key, name, section, the
    section's question, the one-line call, the data shape, the use-when, the
    watch-out note. For the picker's search box.
    """
    t = text.strip().lower()
    if not t:
        return list(TEMPLATES)
    questions = {name: q for name, q in wall.SECTIONS}
    hay = lambda c: " ".join(  # noqa: E731
        [c.key, c.name, c.section, questions.get(c.section, ""),
         c.call, c.shape, c.use_when, c.note]
    ).lower()
    return [c for c in TEMPLATES if t in hay(c)]


# =====================================================================
# SMALL BUILDER HELPERS
# =====================================================================

CATS = wall.CATS          # the colour-blind-safe categorical palette
MUTED = wall.MUTED
INK = wall.INK
PANEL = wall.PANEL
GRID = wall.GRID


def _pivot(df: pd.DataFrame, m: dict, rows: str, cols: str, vals: str) -> pd.DataFrame:
    """
    Long table -> grid. (row label, column label, number) becomes the
    rows x columns block that every heatmap, contour and surface wants.
    """
    g = df.pivot_table(index=m[rows], columns=m[cols], values=m[vals], aggfunc="mean")
    return g.sort_index()


def _tail(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """Cap a frame so a 500k-row result does not hang the browser."""
    return df if len(df) <= n else df.head(n)


def _groups(df: pd.DataFrame, col: str | None, cap: int = 12) -> list:
    """The distinct values of a grouping column, biggest first, capped."""
    if not col:
        return [None]
    return list(df[col].value_counts().head(cap).index)


def _few(df: pd.DataFrame, col: str, cap: int = 12) -> pd.DataFrame:
    """
    Keep only the `cap` most common values of a column.

    Faceting on a 47-state column asks Plotly for 47 panels and it refuses
    outright ("vertical spacing cannot be greater than 1/(rows-1)"). Twelve
    panels is already more than anyone reads.
    """
    keep = df[col].value_counts().head(cap).index
    return df[df[col].isin(keep)]


def _sankey_index(df: pd.DataFrame, src: str, tgt: str):
    """
    from/to names -> the integer positions go.Sankey actually needs.

    The trap ATLAS calls out: link.source and link.target must be positions
    into node.label. Handing them names validates fine and draws nothing.
    """
    names = list(dict.fromkeys(list(df[src].astype(str)) + list(df[tgt].astype(str))))
    idx = {n: i for i, n in enumerate(names)}
    return names, df[src].astype(str).map(idx).to_list(), df[tgt].astype(str).map(idx).to_list()


def _magnitude(df: pd.DataFrame, m: dict, slot: str = "size") -> tuple[pd.DataFrame, dict]:
    """
    A dot's size is a radius, and a radius cannot be negative.

    Plotly refuses `marker.size = -12` outright - it is not a warning, it is a
    ValueError that kills the chart. So the moment you drop a signed column - a
    change, a delta, a swing, anything that can go down - on a size slot, a
    bubble chart dies. Measured: bubble, scatter_geo, scatter_map,
    mapbox_deprecated and animation all raised on a column holding -12.

    So we plot how BIG the number is, not which way it went, and we RENAME the
    column to `|change|` while we do it. The rename is the honest half: the
    hover then says "magnitude", and nobody reads a small bubble as a fall when
    it is really a big drop. Same call `_b_marimekko` already makes about bar
    width, for the same reason.

    A column with no negatives is handed straight back, untouched.
    """
    col = (m or {}).get(slot)
    if not col or not isinstance(col, str) or col not in df.columns:
        return df, m
    values = pd.to_numeric(df[col], errors="coerce")
    if not bool((values < 0).any()):
        return df, m
    name = f"|{col}|"
    while name in df.columns:          # never clobber a column that is already there
        name = f"|{name}|"
    out = df.copy(deep=False)
    out[name] = values.abs()
    return out, {**m, slot: name}


def _px(func: str, arg_map: dict[str, str] | None = None, **fixed):  # noqa: D417
    """
    Build a Plotly Express builder.

    Slot names are chosen to BE the px argument names wherever possible, so
    most charts need nothing but this line. `arg_map` renames the handful
    that cannot (px calls a pie's label column `names`, not `x`).
    """
    def build(df: pd.DataFrame, m: dict) -> go.Figure:
        df, m = _magnitude(df, m)      # a negative radius is a ValueError, not a chart
        kw = dict(fixed)
        for slot, col in m.items():
            if col is None or (isinstance(col, list) and not col):
                continue
            kw[(arg_map or {}).get(slot, slot)] = col
        return getattr(px, func)(df, **kw)

    # A builder that is NOTHING but a px call with the mapping is the only
    # kind codegen can honestly print as `px.thing(df, x=..., y=...)`. Anything
    # with styling baked in has to go through registry.build() instead, or the
    # code panel would be showing you a line that does not make that picture.
    build.px_pure = func if not (fixed or arg_map) else None
    return build


# =====================================================================
# BUILDERS - COMPARE
# =====================================================================


def _b_bar_h(df, m):
    # Ascending sort, because a horizontal bar draws bottom-to-top: ascending
    # is what puts the biggest bar at the TOP.
    d = df.sort_values(m["x"])
    return px.bar(d, x=m["x"], y=m["y"], orientation="h", color=m["color"])


def _b_bar_sorted(df, m):
    return px.bar(df, x=m["x"], y=m["y"], color=m["color"]).update_xaxes(
        categoryorder="total descending"
    )


def _b_imshow_pivot(df, m):
    g = _pivot(df, m, "y", "x", "z")
    return px.imshow(g, aspect="auto", color_continuous_scale="Viridis",
                     labels=dict(color=m["z"]))


def _b_corr(df, m):
    cols = m["values"]
    return px.imshow(df[cols].corr().round(2), text_auto=".2f", zmin=-1, zmax=1,
                     color_continuous_scale="RdBu", aspect="auto")


def _b_heatmap(df, m):
    g = _pivot(df, m, "y", "x", "z")
    return go.Figure(
        go.Heatmap(z=g.values, x=[str(c) for c in g.columns], y=[str(i) for i in g.index],
                   xgap=1, ygap=1, colorscale="Viridis", colorbar=dict(title=m["z"]))
    )


def _b_annotated_heatmap(df, m):
    g = _pivot(df, m, "y", "x", "z").round(1)
    fig = ff.create_annotated_heatmap(
        z=g.values, x=[str(c) for c in g.columns], y=[str(i) for i in g.index],
        colorscale="Viridis", showscale=True,
    )
    fig.update_layout(template="wall")
    fig.update_annotations(font_size=10)
    return fig


def _b_contour(df, m):
    g = _pivot(df, m, "y", "x", "z")
    return go.Figure(
        go.Contour(z=g.values, x=[str(c) for c in g.columns], y=[str(i) for i in g.index],
                   colorscale="Viridis",
                   contours=dict(showlabels=True, labelfont=dict(size=9, color=INK)))
    )


def _b_contour_constraint(df, m):
    g = _pivot(df, m, "y", "x", "z")
    z = g.values
    lo, hi = float(np.nanpercentile(z, 35)), float(np.nanpercentile(z, 75))
    return go.Figure(
        [
            go.Contour(z=z, contours=dict(type="constraint", operation="[]", value=[lo, hi]),
                       fillcolor="rgba(90,169,255,0.35)", line=dict(color=CATS[0]),
                       name=f"between {lo:,.1f} and {hi:,.1f}", showlegend=True),
            go.Contour(z=z, contours=dict(type="constraint", operation="<", value=lo),
                       fillcolor="rgba(255,123,156,0.35)", line=dict(color=CATS[3]),
                       name=f"below {lo:,.1f}", showlegend=True),
        ]
    )


def _b_dumbbell(df, m):
    d = _tail(df, 40)
    fig = go.Figure()
    for lab, x0, x1 in zip(d[m["label"]], d[m["start"]], d[m["end"]]):
        fig.add_shape(type="line", x0=x0, x1=x1, y0=lab, y1=lab,
                      line=dict(color=MUTED, width=3), layer="below")
    fig.add_trace(go.Scatter(x=d[m["start"]], y=d[m["label"]], mode="markers",
                             name=m["start"], marker=dict(size=13, color=CATS[0])))
    fig.add_trace(go.Scatter(x=d[m["end"]], y=d[m["label"]], mode="markers",
                             name=m["end"], marker=dict(size=13, color=CATS[1])))
    return fig


def _b_lollipop(df, m):
    d = _tail(df, 60).sort_values(m["value"])
    fig = go.Figure()
    for lab, x in zip(d[m["label"]], d[m["value"]]):
        fig.add_shape(type="line", x0=0, x1=x, y0=lab, y1=lab,
                      line=dict(color=MUTED, width=2))
    fig.add_trace(go.Scatter(x=d[m["value"]], y=d[m["label"]], mode="markers",
                             marker=dict(size=15, color=CATS[0]), name=m["value"]))
    return fig


def _b_cleveland(df, m):
    d = _tail(df, 40)
    fig = go.Figure()
    for i, col in enumerate(m["values"]):
        fig.add_trace(go.Scatter(x=d[col], y=d[m["label"]], mode="markers", name=col,
                                 marker=dict(size=12, color=CATS[i % len(CATS)])))
    return fig


def _b_marimekko(df, m):
    # Bar WIDTH is how big the category is; bar HEIGHT is its share. That pair
    # is the whole point - a 100% stacked bar makes a tiny category shout.
    d = _tail(df, 24)
    # Width is a physical size, so it cannot be negative. A change column can
    # be, so take the magnitude - "how big", not "which way".
    w = np.abs(d[m["width"]].to_numpy(dtype=float))
    w[w == 0] = w[w > 0].min() if (w > 0).any() else 1.0
    centres = np.cumsum(w) - w / 2
    v = d[m["height"]].to_numpy(dtype=float)
    labels = d[m["label"]].astype(str).to_list()
    top = v / v.max() * 100 if v.max() else v
    fig = go.Figure(
        [
            go.Bar(x=centres, y=top, width=w, offset=0, name=m["height"],
                   marker_color=CATS[0], customdata=labels,
                   hovertemplate="%{customdata}<br>%{y:.0f}<extra></extra>"),
            go.Bar(x=centres, y=100 - top, width=w, offset=0, name="rest",
                   marker_color=CATS[1], customdata=labels,
                   hovertemplate="%{customdata}<br>%{y:.0f}<extra></extra>"),
        ]
    )
    return fig.update_layout(
        barmode="stack", bargap=0,
        xaxis=dict(tickvals=centres, ticktext=labels,
                   title=f"{m['label']} (width = {m['width']})"),
        yaxis_title="share (%)",
    )


def _b_multicategory(df, m):
    d = _tail(df, 60)
    return go.Figure(
        go.Bar(x=[d[m["outer"]].astype(str).to_list(), d[m["inner"]].astype(str).to_list()],
               y=d[m["y"]], marker_color=CATS[0])
    ).update_layout(xaxis=dict(dividercolor=GRID, dividerwidth=2))


def _b_facets(df, m):
    d = _few(df, m["facet_col"], 9)
    fig = px.histogram(d, x=m["x"], facet_col=m["facet_col"], facet_col_wrap=3,
                       color=m["facet_col"], nbins=30)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig.update_layout(showlegend=False)


def _b_facet_grid_ff(df, m):
    d = _tail(_few(df, m["facet_col"], 6), 2000)
    fig = ff.create_facet_grid(d, x=m["x"], y=m["y"], facet_col=m["facet_col"],
                               marker=dict(size=4, opacity=0.6))
    fig.update_layout(template="wall", showlegend=False)
    return fig


def _b_table(df, m):
    d = _tail(df[m["columns"]], 200)
    return go.Figure(
        go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in d.columns], fill_color="#1b2230",
                        font=dict(color=INK), align="left", height=30),
            cells=dict(values=[d[c] for c in d.columns],  # column-major, always
                       fill_color=[["#12171f", "#161c26"] * (len(d) // 2 + 1)],
                       font=dict(color=INK), align="left", height=26),
        )
    )


def _b_table_ff(df, m):
    fig = ff.create_table(_tail(df[m["columns"]], 25).round(2),
                          colorscale=[[0, "#1b2230"], [0.5, "#161c26"], [1, "#12171f"]],
                          font_colors=[INK, INK, INK])
    fig.update_layout(template="wall", margin=dict(l=8, r=8, t=8, b=8))
    return fig


# =====================================================================
# BUILDERS - DISTRIBUTE
# =====================================================================


def _b_histogram(df, m):
    return px.histogram(df, x=m["x"], color=m["color"], nbins=50,
                        marginal="box").update_layout(bargap=0.02)


def _b_histogram_cum(df, m):
    return px.histogram(df, x=m["x"], color=m["color"], nbins=60, histnorm="percent",
                        cumulative=True, opacity=0.6).update_layout(barmode="overlay",
                                                                    bargap=0)


def _b_ecdf_ccdf(df, m):
    d = df[df[m["x"]] > 0]
    return px.ecdf(d, x=m["x"], ecdfmode="complementary", log_x=True, log_y=True)


def _b_box_precomputed(df, m):
    # Five numbers per group instead of ten million rows. ATLAS measures it at
    # 6,760 bytes against 2,728,215 for the same picture.
    d = _tail(df, 200)
    kw = dict(x=d[m["label"]], q1=d[m["q1"]], median=d[m["median"]], q3=d[m["q3"]],
              marker_color=CATS[0], name="summary")
    if m["lowerfence"]:
        kw["lowerfence"] = d[m["lowerfence"]]
    if m["upperfence"]:
        kw["upperfence"] = d[m["upperfence"]]
    if m["mean"]:
        kw["mean"] = d[m["mean"]]
    return go.Figure(go.Box(**kw))


def _b_violin_split(df, m):
    sides = _groups(df, m["split"], cap=2)
    fig = go.Figure()
    for (side, colour), val in zip((("negative", CATS[0]), ("positive", CATS[1])), sides):
        sub = df[df[m["split"]] == val]
        fig.add_trace(go.Violin(x=sub[m["x"]], y=sub[m["y"]], side=side, name=str(val),
                                line_color=colour, fillcolor=colour, opacity=0.6,
                                points=False, scalemode="count"))
    return fig.update_layout(violinmode="overlay", violingap=0.15, yaxis_title=m["y"])


def _b_ridgeline(df, m):
    # violingap=0 is the load-bearing trick: it fuses the ridges into one
    # landscape instead of 40 separate violins.
    fig = go.Figure()
    for i, g in enumerate(_groups(df, m["category"], cap=40)):
        vals = df.loc[df[m["category"]] == g, m["value"]]
        fig.add_trace(
            go.Violin(x=vals, name=str(g), side="positive", orientation="h", width=3,
                      points=False, line_color=CATS[i % len(CATS)],
                      fillcolor=CATS[i % len(CATS)], opacity=0.6)
        )
    return fig.update_layout(violingap=0, violingroupgap=0, showlegend=False,
                             xaxis_title=m["value"])


def _b_beeswarm(df, m):
    v = _tail(df, 4000)[m["value"]].to_numpy(dtype=float)
    rng = np.random.default_rng(7)
    return go.Figure(
        go.Scatter(x=v, y=rng.normal(0, 0.09, v.size), mode="markers",
                   marker=dict(size=5, opacity=0.55, color=CATS[0]))
    ).update_layout(yaxis=dict(visible=False), xaxis_title=m["value"])


def _b_raincloud(df, m):
    v = _tail(df, 2000)[m["value"]].to_numpy(dtype=float)
    rng = np.random.default_rng(3)
    return go.Figure(
        [
            go.Violin(x=v, side="positive", points=False, width=1.4, y0=0.45,
                      line_color=CATS[0], fillcolor=CATS[0], opacity=0.5, name="shape"),
            go.Box(x=v, y=["summary"] * v.size, boxpoints=False, width=0.22,
                   marker_color=CATS[1], name="summary"),
            go.Scatter(x=v, y=rng.normal(-0.35, 0.05, v.size), mode="markers",
                       marker=dict(size=4, opacity=0.45, color=CATS[2]), name="rows"),
        ]
    ).update_layout(yaxis=dict(visible=False), xaxis_title=m["value"], showlegend=False)


def _b_density_heatmap(df, m):
    fig = px.density_heatmap(df, x=m["x"], y=m["y"], nbinsx=40, nbinsy=40,
                             marginal_x="histogram", marginal_y="histogram")
    # Set the scale after the fact: handing color_continuous_scale in alongside
    # marginals tries to give the scale name to the marginal markers.
    return fig.update_coloraxes(colorscale="Viridis")


def _b_density_2d_ff(df, m):
    d = _tail(df, 3000)
    fig = ff.create_2d_density(d[m["x"]], d[m["y"]], colorscale="Viridis", point_size=3)
    fig.update_layout(template="wall", showlegend=False)
    return fig


def _b_isosurface(df, m):
    d = _tail(df, 8000)
    v = d[m["value"]]
    return go.Figure(
        go.Isosurface(x=d[m["x"]], y=d[m["y"]], z=d[m["z"]], value=v,
                      isomin=float(v.quantile(0.35)), isomax=float(v.quantile(0.85)),
                      surface_count=3, opacity=0.5, colorscale="Viridis",
                      caps=dict(x_show=False, y_show=False, z_show=False))
    )


def _b_volume(df, m):
    d = _tail(df, 8000)
    v = d[m["value"]]
    return go.Figure(
        go.Volume(x=d[m["x"]], y=d[m["y"]], z=d[m["z"]], value=v,
                  isomin=float(v.min()), isomax=float(v.max()), opacity=0.12,
                  surface_count=16, colorscale="Viridis")
    )


# =====================================================================
# BUILDERS - RELATE
# =====================================================================


def _b_scatter_trend(df, m):
    d = _tail(df, 5000).sort_values(m["x"])
    return px.scatter(d, x=m["x"], y=m["y"], trendline="rolling",
                      trendline_options=dict(window=max(5, len(d) // 12)),
                      trendline_color_override=CATS[3], opacity=0.45)


def _b_scattergl(df, m):
    d = df.astype({m["x"]: "float32", m["y"]: "float32"})
    return px.scatter(d, x=m["x"], y=m["y"], render_mode="webgl",
                      opacity=0.25).update_traces(marker=dict(size=3))


def _b_quadrant(df, m):
    mx, my = df[m["x"]].median(), df[m["y"]].median()
    fig = px.scatter(df, x=m["x"], y=m["y"], opacity=0.55)
    fig.add_hline(y=my, line_dash="dot", line_color=MUTED)
    fig.add_vline(x=mx, line_dash="dot", line_color=MUTED)
    fig.add_annotation(x=df[m["x"]].max(), y=df[m["y"]].max(), text="high / high",
                       showarrow=False, xanchor="right", font=dict(color=CATS[3]))
    fig.add_annotation(x=df[m["x"]].min(), y=df[m["y"]].max(), text="low x / high y",
                       showarrow=False, xanchor="left", font=dict(color=CATS[1]))
    return fig


def _b_splom(df, m):
    return px.scatter_matrix(df, dimensions=m["dimensions"], color=m["color"],
                             opacity=0.5).update_traces(diagonal_visible=False,
                                                        showupperhalf=False,
                                                        marker_size=4)


def _b_splom_ff(df, m):
    fig = ff.create_scatterplotmatrix(_tail(df[m["dimensions"]], 800), diag="histogram",
                                      height=420, width=None)
    fig.update_layout(template="wall", showlegend=False)
    return fig


def _b_parcoords_constrained(df, m):
    d = _tail(df, 5000)
    dims = []
    for i, col in enumerate(m["dimensions"]):
        dim = dict(label=col, values=d[col])
        if i == 0:  # open the page already filtered on the first axis
            lo, hi = d[col].quantile(0.55), d[col].max()
            dim["constraintrange"] = [float(lo), float(hi)]
        dims.append(dim)
    colour = d[m["color"]] if m["color"] else d[m["dimensions"][0]]
    return go.Figure(
        go.Parcoords(line=dict(color=colour, colorscale="Viridis", showscale=True),
                     dimensions=dims)
    )


def _b_scatter3d_ribbon(df, m):
    # surfaceaxis is the only thing separating a 3D line from a 3D ribbon.
    fig = go.Figure()
    for i, g in enumerate(_groups(df, m["color"], cap=6)):
        sub = df if g is None else df[df[m["color"]] == g]
        sub = _tail(sub.sort_values(m["x"]), 400)
        fig.add_trace(
            go.Scatter3d(x=sub[m["x"]], y=sub[m["y"]], z=sub[m["z"]], mode="lines",
                         surfaceaxis=1, surfacecolor=CATS[i % len(CATS)],
                         line=dict(color=CATS[i % len(CATS)], width=4),
                         name=str(g) if g is not None else m["z"])
        )
    return fig


def _b_surface(df, m):
    g = _pivot(df, m, "y", "x", "z")
    return go.Figure(
        go.Surface(z=g.values, x=[str(c) for c in g.columns], y=[str(i) for i in g.index],
                   colorscale="Viridis",
                   contours=dict(z=dict(show=True, usecolormap=True, project_z=True)))
    )


def _b_mesh3d(df, m):
    d = _tail(df, 3000)
    return go.Figure(
        go.Mesh3d(x=d[m["x"]], y=d[m["y"]], z=d[m["z"]], alphahull=3, opacity=0.75,
                  colorscale="Viridis", intensity=d[m["z"]], flatshading=False)
    )


def _b_radar(df, m):
    # Repeat the first point at the end so the loop closes.
    axes = list(m["values"])
    fig = go.Figure()
    for i, (_, row) in enumerate(_tail(df, 3).iterrows()):
        vals = [float(row[c]) for c in axes]
        fig.add_trace(go.Scatterpolar(r=vals + vals[:1], theta=axes + axes[:1],
                                      fill="toself", name=str(row[m["entity"]]),
                                      line_color=CATS[i % len(CATS)], opacity=0.75))
    return fig.update_layout(polar=dict(gridshape="linear"))


def _b_secondary_y(df, m):
    d = _tail(df.sort_values(m["x"]), 2000)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=d[m["x"]], y=d[m["y1"]], name=m["y1"], marker_color=CATS[0],
                         opacity=0.6), secondary_y=False)
    fig.add_trace(go.Scatter(x=d[m["x"]], y=d[m["y2"]], name=m["y2"],
                             line=dict(color=CATS[1], width=2)), secondary_y=True)
    fig.update_yaxes(title_text=m["y1"], secondary_y=False)
    fig.update_yaxes(title_text=m["y2"], secondary_y=True, showgrid=False)
    return fig


def _b_polar(df, m):
    # render_mode='svg' on purpose: past 1,000 points px silently switches to
    # scatterpolargl, and the WebGL line object has no `shape`, so line_close
    # blows up. Cheaper to cap the rows than to lose the closed loop.
    d = _tail(df, 800)
    return px.line_polar(d, r=m["r"], theta=m["theta"], color=m["color"],
                         line_close=True, markers=True, render_mode="svg")


def _b_scattersmith(df, m):
    d = _tail(df, 2000)
    return go.Figure(
        go.Scattersmith(real=d[m["real"]], imag=d[m["imag"]], mode="markers",
                        marker=dict(size=7, color=CATS[0]))
    )


def _b_carpet(df, m):
    d = _tail(df, 400)
    return go.Figure(
        go.Carpet(a=d[m["a"]], b=d[m["b"]], x=d[m["x"]], y=d[m["y"]], carpet="grid1",
                  aaxis=dict(gridcolor=GRID, title=m["a"]),
                  baxis=dict(gridcolor=GRID, title=m["b"]))
    )


def _b_scattercarpet(df, m):
    d = _tail(df, 400)
    return go.Figure(
        [
            go.Carpet(a=d[m["a"]], b=d[m["b"]], x=d[m["x"]], y=d[m["y"]], carpet="c1",
                      aaxis=dict(gridcolor=GRID), baxis=dict(gridcolor=GRID)),
            go.Scattercarpet(a=d[m["a"]].head(8), b=d[m["b"]].head(8), carpet="c1",
                             mode="markers+lines", marker=dict(size=10, color=CATS[1]),
                             line=dict(color=CATS[1]), name="run 1"),
        ]
    )


def _b_contourcarpet(df, m):
    d = _tail(df, 400)
    return go.Figure(
        [
            go.Carpet(a=d[m["a"]], b=d[m["b"]], x=d[m["x"]], y=d[m["y"]], carpet="c1",
                      aaxis=dict(gridcolor=GRID), baxis=dict(gridcolor=GRID)),
            go.Contourcarpet(a=d[m["a"]], b=d[m["b"]], z=d[m["z"]], carpet="c1",
                             colorscale="Viridis", contours=dict(showlines=True)),
        ]
    )


# =====================================================================
# BUILDERS - COMPOSE
# =====================================================================


def _b_bar_barnorm(df, m):
    return px.bar(df, x=m["x"], y=m["y"], color=m["color"]).update_layout(
        barnorm="percent", yaxis_title=f"share of {m['x']} (%)"
    )


def _b_streamgraph(df, m):
    d = df.sort_values(m["x"])
    fig = go.Figure()
    for i, g in enumerate(_groups(d, m["color"], cap=12)):
        s = d if g is None else d[d[m["color"]] == g]
        fig.add_trace(go.Scatter(x=s[m["x"]], y=s[m["y"]], stackgroup="one", mode="none",
                                 name=str(g), fillcolor=CATS[i % len(CATS)],
                                 hoverinfo="x+y+name"))
    return fig.update_layout(yaxis=dict(visible=False))


def _b_flamegraph(df, m):
    # Same hierarchy as an icicle, flipped so the root sits at the BOTTOM -
    # the profiler's view, and the actual reason to pick icicle over treemap.
    return px.icicle(df, path=m["path"], values=m["values"], color=m["values"],
                     color_continuous_scale="Viridis").update_traces(
        tiling=dict(orientation="v", flip="y")
    )


def _b_waffle(df, m):
    # One square is one percent, so 37% is 37 squares a reader can count.
    d = _tail(df, 8)
    share = d[m["share"]].to_numpy(dtype=float)
    share = np.round(share / share.sum() * 100).astype(int)
    names = d[m["label"]].astype(str).to_list()
    g, start = np.zeros(100), 0
    for i, s in enumerate(share):
        g[start:start + s] = i
        start += s
    n = max(len(share) - 1, 1)
    return go.Figure(
        go.Heatmap(z=g.reshape(10, 10), xgap=4, ygap=4, showscale=False,
                   colorscale=[[i / n, CATS[i % len(CATS)]] for i in range(len(share))],
                   hovertemplate="%{z}<extra></extra>")
    ).update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"),
                    title=" / ".join(f"{a} {b}%" for a, b in zip(names, share)))


def _b_pyramid(df, m):
    d = _tail(df, 30)
    left = d[m["left"]].to_numpy(dtype=float)
    return go.Figure(
        [
            go.Bar(y=d[m["band"]].astype(str), x=-left, orientation="h", name=m["left"],
                   customdata=left.round(1),
                   hovertemplate="%{y}: %{customdata}<extra></extra>",
                   marker_color=CATS[0]),
            go.Bar(y=d[m["band"]].astype(str), x=d[m["right"]], orientation="h",
                   name=m["right"], marker_color=CATS[1],
                   hovertemplate="%{y}: %{x:.1f}<extra></extra>"),
        ]
    ).update_layout(barmode="relative", bargap=0.08, xaxis=dict(tickformat="~s"))


# =====================================================================
# BUILDERS - FLOW
# =====================================================================


def _b_sankey(df, m):
    d = _tail(df, 400)
    names, src, tgt = _sankey_index(d, m["source"], m["target"])
    return go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(label=names, pad=18, thickness=16,
                      line=dict(color=GRID, width=1),
                      color=[CATS[i % len(CATS)] for i in range(len(names))]),
            link=dict(source=src, target=tgt, value=d[m["value"]],
                      color="rgba(90,169,255,0.22)",
                      hovertemplate="%{source.label} to %{target.label}"
                                    "<br>%{value}<extra></extra>"),
        )
    ).update_layout(margin=dict(l=8, r=8, t=8, b=8))


def _b_sankey_grouped(df, m):
    d = _tail(df, 400)
    names, src, tgt = _sankey_index(d, m["source"], m["target"])
    groups = [[len(names) - 2, len(names) - 1]] if len(names) >= 2 else []
    return go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(label=names, pad=18, thickness=16, align="left", groups=groups,
                      color=[CATS[i % len(CATS)] for i in range(len(names))]),
            link=dict(source=src, target=tgt, value=d[m["value"]], arrowlen=14,
                      color="rgba(78,203,141,0.22)"),
        )
    ).update_layout(margin=dict(l=8, r=8, t=8, b=8))


def _b_parcats(df, m):
    d = _tail(df, 5000)
    colour = d[m["color"]] if m["color"] else None
    return px.parallel_categories(d, dimensions=m["dimensions"], color=colour,
                                  color_continuous_scale="Viridis")


def _b_funnel(df, m):
    return px.funnel(df, x=m["x"], y=m["y"]).update_traces(
        textinfo="value+percent previous", marker_color=CATS[0]
    )


def _b_cone(df, m):
    d = _tail(df, 3000)
    return go.Figure(
        go.Cone(x=d[m["x"]], y=d[m["y"]], z=d[m["z"]], u=d[m["u"]], v=d[m["v"]],
                w=d[m["w"]], colorscale="Viridis", sizemode="scaled", sizeref=0.5,
                showscale=False)
    )


def _b_streamtube(df, m):
    d = _tail(df, 3000)
    return go.Figure(
        go.Streamtube(x=d[m["x"]], y=d[m["y"]], z=d[m["z"]], u=d[m["u"]], v=d[m["v"]],
                      w=d[m["w"]], colorscale="Viridis", sizeref=0.4, showscale=False)
    )


def _b_quiver_ff(df, m):
    d = _tail(df, 600)
    fig = ff.create_quiver(d[m["x"]], d[m["y"]], d[m["u"]], d[m["v"]],
                           scale=1.0, arrow_scale=0.35,
                           line=dict(width=1.2, color=CATS[0]))
    fig.update_layout(template="wall")
    return fig


# =====================================================================
# BUILDERS - RANK
# =====================================================================


def _b_rank_bar(df, m):
    d = _tail(df.sort_values(m["value"]), 40)
    return px.bar(d, x=m["value"], y=m["label"], orientation="h", color=m["label"],
                  text_auto=".1f").update_layout(showlegend=False)


def _b_bump(df, m):
    # The whole trick is autorange='reversed' so rank 1 sits at the top.
    return px.line(df.sort_values(m["x"]), x=m["x"], y=m["rank"], color=m["entity"],
                   markers=True).update_yaxes(autorange="reversed", dtick=1, title="rank")


def _b_slope(df, m):
    ends = df[df[m["x"]].isin([df[m["x"]].min(), df[m["x"]].max()])].copy()
    ends[m["x"]] = ends[m["x"]].astype(str)
    fig = px.line(ends, x=m["x"], y=m["y"], color=m["entity"], markers=True)
    return fig.update_layout(xaxis=dict(type="category"), margin=dict(r=90))


def _b_pareto(df, m):
    d = df.groupby(m["label"], as_index=False)[m["value"]].sum().sort_values(
        m["value"], ascending=False
    ).head(30)
    cum = d[m["value"]].cumsum() / d[m["value"]].sum() * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=d[m["label"]].astype(str), y=d[m["value"]],
                         marker_color=CATS[0], name="total"), secondary_y=False)
    fig.add_trace(go.Scatter(x=d[m["label"]].astype(str), y=cum, mode="lines+markers",
                             name="cumulative %", line=dict(color=CATS[1], width=2)),
                  secondary_y=True)
    fig.add_hline(y=80, line_dash="dot", line_color=MUTED, secondary_y=True,
                  annotation_text="80%", annotation_position="top left")
    fig.update_yaxes(title_text=m["value"], secondary_y=False)
    fig.update_yaxes(title_text="cumulative %", range=[0, 105], secondary_y=True,
                     showgrid=False)
    return fig


def _b_rank_heatmap(df, m):
    g = df.pivot_table(index=m["entity"], columns=m["period"], values=m["value"],
                       aggfunc="mean")
    return go.Figure(
        go.Heatmap(z=g.values, x=[str(c) for c in g.columns], y=[str(i) for i in g.index],
                   xgap=2, ygap=2, colorscale="Viridis_r",
                   colorbar=dict(title=m["value"]),
                   texttemplate="%{z:.0f}", textfont=dict(size=10))
    )


def _b_legend_isolate(df, m):
    fig = px.line(df.sort_values(m["x"]), x=m["x"], y=m["y"], color=m["color"])
    for tr in fig.data[2:]:  # start with the top two showing, rest one click away
        tr.visible = "legendonly"
    return fig.update_layout(
        legend=dict(itemclick="toggleothers", itemdoubleclick="toggle",
                    orientation="h", y=1.08, x=0, title_text="click to isolate  ")
    )


# =====================================================================
# BUILDERS - LOCATE
# =====================================================================


def _b_choropleth_facet(df, m):
    # Only the outline (_geo) family facets at all - the tile-map family cannot.
    d = _few(df, m["facet_col"], 6)
    fig = px.choropleth(d, locations=m["locations"], locationmode="USA-states",
                        color=m["color"], scope="usa", facet_col=m["facet_col"],
                        color_continuous_scale="Viridis")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig


def _b_geo_subplots(df, m):
    cols = m["values"]
    fig = make_subplots(rows=1, cols=len(cols), specs=[[{"type": "geo"}] * len(cols)],
                        subplot_titles=tuple(cols))
    for i, col in enumerate(cols, start=1):
        fig.add_trace(
            go.Choropleth(locations=df[m["locations"]], locationmode="USA-states",
                          z=df[col], colorscale="Viridis", showscale=False),
            row=1, col=i,
        )
    fig.update_geos(scope="usa", bgcolor=PANEL, lakecolor=PANEL, landcolor="#1b2230",
                    subunitcolor=GRID)
    return fig


def _b_mapbox_deprecated(df, m):
    df, m = _magnitude(df, m)          # a negative radius is a ValueError, not a chart
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return px.scatter_mapbox(df, lat=m["lat"], lon=m["lon"], size=m["size"],
                                 color=m["color"], zoom=3, mapbox_style="white-bg",
                                 color_continuous_scale="Viridis", size_max=14,
                                 opacity=0.6)


def _b_hexbin_ff(df, m):
    d = _tail(df, 20000)
    fig = ff.create_hexbin_map(lat=d[m["lat"]].to_list(), lon=d[m["lon"]].to_list(),
                               nx_hexagon=18, opacity=0.7,
                               color_continuous_scale="Viridis", min_count=1)
    fig.update_layout(template="wall", map_style="white-bg",
                      margin=dict(l=0, r=0, t=0, b=0))
    return fig


def _b_hexbin_mapbox_ff(df, m):
    d = _tail(df, 20000)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = ff.create_hexbin_mapbox(lat=d[m["lat"]].to_list(), lon=d[m["lon"]].to_list(),
                                      nx_hexagon=14, opacity=0.7, min_count=1,
                                      color_continuous_scale="Plasma")
    fig.update_layout(template="wall", map_style="white-bg",
                      margin=dict(l=0, r=0, t=0, b=0))
    return fig


# =====================================================================
# BUILDERS - CHANGE
# =====================================================================


def _b_line(df, m):
    # Sort first. px.line draws rows in dataframe order, so unsorted input
    # gives you spaghetti.
    return px.line(df.sort_values(m["x"]), x=m["x"], y=m["y"],
                   color=m["color"]).update_layout(hovermode="x unified")


def _b_line_step(df, m):
    return px.line(df.sort_values(m["x"]), x=m["x"], y=m["y"], color=m["color"],
                   line_shape="hv", markers=True)


def _b_band(df, m):
    # One closed polygon: x forwards then backwards, high then low reversed.
    d = df.sort_values(m["x"])
    x, lo, hi = d[m["x"]], d[m["low"]], d[m["high"]]
    return go.Figure(
        [
            go.Scatter(x=np.r_[x, x[::-1]], y=np.r_[hi, lo[::-1]], fill="toself",
                       fillcolor="rgba(90,169,255,0.18)", line=dict(width=0),
                       hoverinfo="skip", name="band"),
            go.Scatter(x=x, y=d[m["y"]], mode="lines", line=dict(color=CATS[0], width=2),
                       name=m["y"]),
        ]
    ).update_layout(hovermode="x unified")


def _b_events(df, m):
    # There is no "event" column in a generic result, so this shades the middle
    # third of the x range as a worked example. Swap the two dates for your own.
    d = df.sort_values(m["x"])
    fig = px.line(d, x=m["x"], y=m["y"], color=m["color"])
    x0, x1, xv = d[m["x"]].quantile(0.35), d[m["x"]].quantile(0.6), d[m["x"]].quantile(0.8)
    fig.add_vrect(x0=x0, x1=x1, fillcolor=CATS[1], opacity=0.12, line_width=0,
                  layer="below", annotation_text="example band",
                  annotation_position="top left",
                  annotation_font=dict(color=CATS[1], size=11))
    fig.add_vline(x=xv, line_dash="dash", line_color=CATS[3],
                  annotation_text="example event", annotation_position="top right",
                  annotation_font=dict(color=CATS[3], size=11))
    return fig


def _b_rangeslider(df, m):
    fig = px.line(df.sort_values(m["x"]), x=m["x"], y=m["y"], color=m["color"])
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            bgcolor="#1b2230", activecolor=CATS[0], font=dict(color=INK),
            buttons=[
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all", label="All"),
            ],
        ),
    )
    return fig


def _b_rangebreaks(df, m):
    fig = px.line(df.sort_values(m["x"]), x=m["x"], y=m["y"], color=m["color"])
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    return fig


def _b_tickformatstops(df, m):
    # dtickrange is in MILLISECONDS. 86400000 is one day.
    fig = px.line(df.sort_values(m["x"]), x=m["x"], y=m["y"], color=m["color"])
    fig.update_xaxes(tickformatstops=[
        dict(dtickrange=[None, 3_600_000], value="%H:%M"),
        dict(dtickrange=[3_600_000, 86_400_000], value="%e %b %H:%M"),
        dict(dtickrange=[86_400_000, 604_800_000], value="%e %b"),
        dict(dtickrange=[604_800_000, None], value="%b %Y"),
    ])
    return fig


def _b_bar_time(df, m):
    keys = [pd.Grouper(key=m["x"], freq="MS")] + ([m["color"]] if m["color"] else [])
    d = df.groupby(keys, as_index=False)[m["y"]].sum()
    return px.bar(d, x=m["x"], y=m["y"], color=m["color"])


def _b_timeline(df, m):
    return px.timeline(df, x_start=m["x_start"], x_end=m["x_end"], y=m["y"],
                       color=m["color"]).update_yaxes(autorange="reversed")


def _b_gantt_ff(df, m):
    d = _tail(df, 60)
    rows = [dict(Task=str(t), Start=str(pd.Timestamp(s).date()),
                 Finish=str(pd.Timestamp(f).date()),
                 Resource=str(r) if m["color"] else "task")
            for t, s, f, r in zip(d[m["y"]], d[m["x_start"]], d[m["x_end"]],
                                  d[m["color"]] if m["color"] else d[m["y"]])]
    fig = ff.create_gantt(rows, index_col="Resource", show_colorbar=True,
                          group_tasks=True, bar_width=0.3, colors=CATS[:8])
    fig.update_layout(template="wall")
    return fig


def _b_waterfall(df, m):
    # measure tags each bar absolute / relative / total. Without it you have
    # drawn a bar chart with extra steps.
    d = _tail(df, 30)
    measure = d[m["measure"]].astype(str).to_list() if m["measure"] else \
        ["relative"] * len(d)
    return go.Figure(
        go.Waterfall(
            measure=measure, x=d[m["label"]].astype(str), y=d[m["delta"]],
            connector=dict(line=dict(color=MUTED, dash="dot")),
            increasing=dict(marker_color=CATS[2]),
            decreasing=dict(marker_color=CATS[3]),
            totals=dict(marker_color=CATS[0]),
            textposition="outside", texttemplate="%{delta:+,.0f}",
        )
    ).update_layout(yaxis_title=m["delta"], margin=dict(t=44))


def _b_candlestick(df, m):
    d = df.sort_values(m["x"])
    return go.Figure(
        go.Candlestick(x=d[m["x"]], open=d[m["open"]], high=d[m["high"]],
                       low=d[m["low"]], close=d[m["close"]],
                       increasing=dict(line=dict(color=CATS[2])),
                       decreasing=dict(line=dict(color=CATS[3])))
    ).update_layout(xaxis_rangeslider_visible=False)


def _b_ohlc(df, m):
    d = df.sort_values(m["x"])
    return go.Figure(
        go.Ohlc(x=d[m["x"]], open=d[m["open"]], high=d[m["high"]], low=d[m["low"]],
                close=d[m["close"]],
                increasing=dict(line=dict(color=CATS[2])),
                decreasing=dict(line=dict(color=CATS[3])))
    ).update_layout(xaxis_rangeslider_visible=False)


_OHLC_ORDER = (
    "These four columns are not in open / high / low / close order - the "
    "factory checks that every high is the biggest of the four and every low "
    "the smallest, and refuses if not. Re-pick the four slots. go.Candlestick "
    "does NOT check, which is why the plain version draws and this one does not."
)


def _b_candlestick_ff(df, m):
    d = _tail(df.sort_values(m["x"]), 120)
    try:
        fig = ff.create_candlestick(d[m["open"]], d[m["high"]], d[m["low"]],
                                    d[m["close"]], dates=d[m["x"]])
    except Exception:  # noqa: BLE001 - a mis-picked mapping is a message
        return _message_figure("Candlestick (figure factory)", _OHLC_ORDER)
    fig.update_layout(template="wall", xaxis_rangeslider_visible=False)
    return fig


def _b_ohlc_ff(df, m):
    d = _tail(df.sort_values(m["x"]), 120)
    try:
        fig = ff.create_ohlc(d[m["open"]], d[m["high"]], d[m["low"]], d[m["close"]],
                             dates=d[m["x"]])
    except Exception:  # noqa: BLE001
        return _message_figure("OHLC (figure factory)", _OHLC_ORDER)
    fig.update_layout(template="wall", xaxis_rangeslider_visible=False)
    return fig


def _b_calendar_heatmap(df, m):
    # No calendar-heatmap trace exists. You reshape to weekday x ISO week.
    d = df[[m["date"], m["value"]]].copy()
    d[m["date"]] = pd.to_datetime(d[m["date"]])
    d["week"] = d[m["date"]].dt.isocalendar().week.astype(int)
    d["dow"] = d[m["date"]].dt.dayofweek
    g = d.pivot_table(index="dow", columns="week", values=m["value"], aggfunc="sum")
    g = g.reindex(range(7))
    return go.Figure(
        go.Heatmap(z=g.values, x=[str(c) for c in g.columns],
                   y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                   xgap=2, ygap=2, colorscale="Viridis",
                   colorbar=dict(title=m["value"]))
    ).update_layout(xaxis_title="ISO week", yaxis_autorange="reversed")


def _b_entity_period_heatmap(df, m):
    g = df.pivot_table(index=m["entity"], columns=m["period"], values=m["value"],
                       aggfunc="mean")
    return go.Figure(
        go.Heatmap(z=g.values, x=[str(c) for c in g.columns],
                   y=[str(i) for i in g.index], xgap=1, ygap=1,
                   colorscale="RdBu", zmid=0, colorbar=dict(title=m["value"]))
    )


def _b_animation(df, m):
    # Two non-negotiables: fixed ranges, or the axes rescale every frame and
    # nothing appears to move; and animation_group, or dots teleport.
    df, m = _magnitude(df, m)          # a negative radius is a ValueError, not a chart
    d = df.copy()
    d[m["frame"]] = d[m["frame"]].astype(str)
    pad = lambda s: [float(s.min()) * 0.9, float(s.max()) * 1.1]  # noqa: E731
    return px.scatter(d.sort_values(m["frame"]), x=m["x"], y=m["y"], size=m["size"],
                      color=m["entity"], animation_frame=m["frame"],
                      animation_group=m["entity"], hover_name=m["entity"],
                      range_x=pad(d[m["x"]]), range_y=pad(d[m["y"]]), size_max=45)


# =====================================================================
# BUILDERS - CONNECT
# =====================================================================


def _circle_positions(names: list[str]) -> np.ndarray:
    """Lay nodes out on a circle. networkx is not installed, so we do it here."""
    ang = np.linspace(0, 2 * np.pi, len(names), endpoint=False)
    return np.c_[np.cos(ang), np.sin(ang)]


def _b_network(df, m):
    # All the edges live in ONE trace with a None between each pair. That is
    # the difference between a chart that renders and a page that hangs.
    d = _tail(df, 2000)
    names = list(dict.fromkeys(list(d[m["source"]].astype(str)) +
                               list(d[m["target"]].astype(str))))[:200]
    pos = _circle_positions(names)
    idx = {n: i for i, n in enumerate(names)}
    ex, ey, deg = [], [], np.zeros(len(names))
    for a, b in zip(d[m["source"]].astype(str), d[m["target"]].astype(str)):
        if a not in idx or b not in idx:
            continue
        ex += [pos[idx[a], 0], pos[idx[b], 0], None]
        ey += [pos[idx[a], 1], pos[idx[b], 1], None]
        deg[idx[a]] += 1
        deg[idx[b]] += 1
    return go.Figure(
        [
            go.Scatter(x=ex, y=ey, mode="lines", line=dict(width=0.8, color=GRID),
                       hoverinfo="skip", showlegend=False),
            go.Scatter(x=pos[:, 0], y=pos[:, 1], mode="markers+text", text=names,
                       textposition="top center", textfont=dict(size=9, color=MUTED),
                       marker=dict(size=8 + deg * 2.2, color=deg, colorscale="Viridis",
                                   line=dict(width=1, color=PANEL),
                                   colorbar=dict(title="links")),
                       hovertemplate="%{text}<br>%{marker.color} links<extra></extra>",
                       showlegend=False),
        ]
    ).update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"))


def _b_arc_diagram(df, m):
    d = _tail(df, 1000)
    names = list(dict.fromkeys(list(d[m["source"]].astype(str)) +
                               list(d[m["target"]].astype(str))))[:80]
    idx = {n: i for i, n in enumerate(names)}
    ax, ay = [], []
    for a, b in zip(d[m["source"]].astype(str), d[m["target"]].astype(str)):
        if a not in idx or b not in idx or a == b:
            continue
        i, j = idx[a], idx[b]
        c, rad = (i + j) / 2, abs(j - i) / 2
        t = np.linspace(0, np.pi, 30)
        ax += list(c + rad * np.cos(t)) + [None]
        ay += list(rad * np.sin(t)) + [None]
    return go.Figure(
        [
            go.Scatter(x=ax, y=ay, mode="lines", line=dict(width=1, color=CATS[0]),
                       opacity=0.5, hoverinfo="skip"),
            go.Scatter(x=list(range(len(names))), y=np.zeros(len(names)), mode="markers",
                       text=names, marker=dict(size=9, color=CATS[1]),
                       hovertemplate="%{text}<extra></extra>"),
        ]
    ).update_layout(showlegend=False, yaxis=dict(visible=False),
                    xaxis=dict(title="node, in order", showgrid=False))


def _b_overlap_matrix(df, m):
    g = _pivot(df, m, "y", "x", "z")
    return px.imshow(g, text_auto=True, aspect="auto", color_continuous_scale="Viridis",
                     labels=dict(color=m["z"]))


def _b_upset_bar(df, m):
    # Plotly has no Venn and no UpSet. Count the combinations, plot the bar.
    cols = m["sets"]
    truth = df[cols].apply(lambda s: s.astype(str).str.lower().isin(
        {"1", "true", "t", "yes", "y"}) if s.dtype == object else s.astype(bool))
    combos = truth.apply(lambda row: "+".join([c for c in cols if row[c]]) or "(none)",
                         axis=1)
    d = combos.value_counts().head(12).reset_index()
    d.columns = ["combination", "entities"]
    return px.bar(d.sort_values("entities"), x="entities", y="combination",
                  orientation="h", color="entities",
                  color_continuous_scale="Viridis").update_layout(coloraxis_showscale=False)


# =====================================================================
# BUILDERS - SINGLE VALUE
# =====================================================================


def _last_and_first(df, m):
    """The KPI pair: the newest value, and something to compare it against."""
    v = float(df[m["value"]].iloc[-1])
    ref = float(df[m["reference"]].iloc[-1]) if m.get("reference") else \
        float(df[m["value"]].iloc[0])
    return v, ref


def _b_indicator(df, m):
    v, ref = _last_and_first(df, m)
    return go.Figure(
        go.Indicator(mode="number+delta", value=v,
                     number=dict(valueformat=",.4~g", font=dict(size=54)),
                     delta=dict(reference=ref, relative=True, valueformat=".1%",
                                increasing=dict(color=CATS[2]),
                                decreasing=dict(color=CATS[3])),
                     title=dict(text=m["value"], font=dict(size=13, color=MUTED)))
    ).update_layout(margin=dict(l=10, r=10, t=30, b=10))


def _b_indicator_gauge(df, m):
    v, ref = _last_and_first(df, m)
    top = float(max(df[m["value"]].max(), v)) * 1.25 or 1.0
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta", value=v, delta=dict(reference=ref),
            title=dict(text=m["value"], font=dict(size=13, color=MUTED)),
            gauge=dict(
                shape="angular", axis=dict(range=[0, top], tickcolor=MUTED),
                bar=dict(color=CATS[0]), bgcolor=PANEL, borderwidth=0,
                steps=[dict(range=[0, top / 3], color="#1b2230"),
                       dict(range=[top / 3, top * 2 / 3], color="#232b38"),
                       dict(range=[top * 2 / 3, top], color="#2c3546")],
                threshold=dict(line=dict(color=CATS[3], width=3), thickness=0.85,
                               value=ref),
            ),
        )
    ).update_layout(margin=dict(l=24, r=24, t=40, b=10))


def _b_indicator_bullet(df, m):
    d = _tail(df, 4)
    n = len(d)
    fig = go.Figure()
    for i, (_, row) in enumerate(d.iterrows()):
        val = float(row[m["value"]])
        ref = float(row[m["target"]]) if m["target"] else val
        mx = max(val, ref) * 1.4 or 1.0
        fig.add_trace(
            go.Indicator(
                mode="number+gauge+delta", value=val, delta=dict(reference=ref),
                title=dict(text=str(row[m["label"]]), font=dict(size=11, color=MUTED)),
                domain=dict(x=[0.32, 1], y=[i / n + 0.04, (i + 1) / n - 0.04]),
                gauge=dict(shape="bullet", axis=dict(range=[0, mx]),
                           bar=dict(color=CATS[i % len(CATS)], thickness=0.55),
                           bgcolor=PANEL, borderwidth=0,
                           steps=[dict(range=[0, mx * 0.5], color="#1b2230"),
                                  dict(range=[mx * 0.5, mx], color="#232b38")],
                           threshold=dict(line=dict(color=CATS[3], width=2),
                                          thickness=0.8, value=ref)),
            )
        )
    return fig.update_layout(margin=dict(l=8, r=18, t=12, b=12))


def _b_kpi_row(df, m):
    # Indicator is a DOMAIN trace: the cell must be declared type='indicator'
    # or the trace silently refuses to land.
    d = _tail(df, 4)
    n = len(d)
    fig = make_subplots(rows=1, cols=n, specs=[[{"type": "indicator"}] * n])
    for i, (_, row) in enumerate(d.iterrows(), start=1):
        ref = float(row[m["reference"]]) if m["reference"] else float(row[m["value"]])
        fig.add_trace(
            go.Indicator(mode="number+delta", value=float(row[m["value"]]),
                         number=dict(valueformat=",.4~g", font=dict(size=30)),
                         delta=dict(reference=ref, increasing=dict(color=CATS[2]),
                                    decreasing=dict(color=CATS[3])),
                         title=dict(text=str(row[m["label"]]),
                                    font=dict(size=11, color=MUTED))),
            row=1, col=i,
        )
    return fig.update_layout(margin=dict(l=8, r=8, t=30, b=8))


def _b_bullet_ff(df, m):
    d = _tail(df, 5)
    rows = []
    for _, row in d.iterrows():
        val, tgt = float(row[m["value"]]), float(row[m["target"]])
        top = max(val, tgt) * 1.3 or 1.0
        rows.append(dict(label=str(row[m["label"]]), range=[top / 2, top],
                         performance=[val, tgt], point=[tgt]))
    fig = ff.create_bullet(pd.DataFrame(rows), markers="point", measures="performance",
                           ranges="range", titles="label", title="",
                           measure_colors=[CATS[0], CATS[4]],
                           range_colors=["#1b2230", "#2c3546"])
    fig.update_layout(template="wall", margin=dict(l=110, r=18, t=8, b=12))
    fig.update_annotations(font=dict(color=INK, size=11))
    return fig


def _b_sparkline_kpi(df, m):
    y = _tail(df, 400)[m["value"]].to_numpy(dtype=float)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y, mode="lines", fill="tozeroy",
                             line=dict(color=CATS[0], width=2),
                             fillcolor="rgba(90,169,255,0.15)", hoverinfo="skip"))
    fig.add_trace(
        go.Indicator(mode="number+delta", value=float(y[-1]),
                     number=dict(valueformat=",.4~g", font=dict(size=40)),
                     delta=dict(reference=float(y[max(0, len(y) - 8)])),
                     title=dict(text=m["value"], font=dict(size=12, color=MUTED)),
                     domain=dict(x=[0.02, 0.45], y=[0.35, 1.0]))
    )
    return fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False),
                             showlegend=False, margin=dict(l=8, r=8, t=8, b=8))


def _b_kpi_table(df, m):
    # A big number alone is not information. Sometimes the honest KPI tile is
    # a four-row table.
    d = _tail(df[m["columns"]], 6)
    return go.Figure(
        go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in d.columns], fill_color="#1b2230",
                        font=dict(color=INK), align="left", height=30),
            cells=dict(values=[d[c] for c in d.columns],
                       fill_color=[["#161c26", "#12171f"] * (len(d) // 2 + 1)],
                       font=dict(color=INK), align="left", height=28),
        )
    ).update_layout(margin=dict(l=6, r=6, t=6, b=6))


# =====================================================================
# THE TABLE OF 145
# ---------------------------------------------------------------------
# Metadata is looked up in wall.py by name, never retyped. If a name in
# wall.py changes, this module raises at import instead of drifting.
# =====================================================================

_LEFT = {c.name: c for c in wall.CHARTS}
TEMPLATES: list[ChartTemplate] = []


def _add(key, wall_name, trace_type, *, required=(), optional=(), build=None,
         demo_only=False, demo_why=""):
    """Register one template against its wall.py entry."""
    src = _LEFT.pop(wall_name, None)
    if src is None:
        raise KeyError(
            f"registry.py expects a chart named {wall_name!r} in bench/wall.py "
            f"and did not find one. Either wall.py was renamed or this key is stale."
        )
    if key in {t.key for t in TEMPLATES}:
        raise KeyError(f"duplicate registry key: {key!r}")
    TEMPLATES.append(
        ChartTemplate(
            key=key, name=src.name, section=src.section, call=src.call, shape=src.shape,
            use_when=src.use_when, note=src.note, trace_type=trace_type,
            required=tuple(required), optional=tuple(optional),
            build=build, wall_fn=src.fn, demo_only=demo_only, demo_why=demo_why,
            blocked=src.blocked, height=src.height,
        )
    )


# -- slot shorthands, so the table below reads like English ------------
S_X_CAT = Slot("x", CAT, "a label column")
S_Y_NUM = Slot("y", NUM, "a number to measure")
S_COLOR = Slot("color", CAT, "a column to colour by")


# ---------------------------------------------------------------- COMPARE
_add("bar", "Bar chart", "bar",
     required=[S_X_CAT, S_Y_NUM], optional=[S_COLOR],
     build=_px("bar"))

_add("bar_horizontal", "Horizontal bar (ranked)", "bar",
     required=[Slot("x", NUM, "a number to measure"),
               Slot("y", CAT, "a label column")],
     optional=[S_COLOR], build=_b_bar_h)

_add("bar_grouped", "Grouped bar", "bar",
     required=[S_X_CAT, S_Y_NUM, Slot("color", CAT, "a second label column to split by")],
     build=_px("bar", barmode="group"))

_add("bar_sorted", "Sorted bar via categoryorder", "bar",
     required=[S_X_CAT, S_Y_NUM], optional=[S_COLOR], build=_b_bar_sorted)

_add("histogram_groupby", "Histogram as GROUP BY", "histogram",
     required=[S_X_CAT, Slot("y", NUM, "a number to total up")], optional=[S_COLOR],
     build=_px("histogram", histfunc="sum"))

_add("box_compare", "Box plot (compare groups)", "box",
     required=[S_X_CAT, Slot("y", NUM, "a number with many rows per group")],
     optional=[S_COLOR], build=_px("box", points="outliers"))

_add("imshow_pivot", "Heatmap of a pivot table", "heatmap",
     required=[Slot("x", CAT, "a column label"), Slot("y", CAT, "a row label"),
               Slot("z", NUM, "a number for each pair")],
     build=_b_imshow_pivot)

_add("corr_matrix", "Correlation matrix", "heatmap",
     required=[Slot("values", NUM, "two or more number columns", many=True, min_n=2)],
     build=_b_corr)

_add("heatmap", "Heatmap (go.Heatmap, long form)", "heatmap",
     required=[Slot("x", CAT, "a column label"), Slot("y", CAT, "a row label"),
               Slot("z", NUM, "a number for each pair")],
     build=_b_heatmap)

_add("annotated_heatmap", "Annotated heatmap", "heatmap",
     required=[Slot("x", CAT, "a column label"), Slot("y", CAT, "a row label"),
               Slot("z", NUM, "a number for each pair")],
     build=_b_annotated_heatmap)

_add("contour_grid", "Contour of a computed grid", "contour",
     required=[Slot("x", CAT, "a grid-column label"),
               Slot("y", CAT, "a grid-row label"),
               Slot("z", NUM, "the value computed at each pair")],
     build=_b_contour)

_add("contour_constraint", "Constraint contour (feasible region)", "contour",
     required=[Slot("x", CAT, "a grid-column label"),
               Slot("y", CAT, "a grid-row label"),
               Slot("z", NUM, "the value computed at each pair")],
     build=_b_contour_constraint)

_add("bar_polar", "Wind rose (polar bar)", "barpolar",
     required=[Slot("theta", CAT, "a wrap-around category such as a compass point or an hour"),
               Slot("r", NUM, "a number for each one")],
     optional=[Slot("color", NUM, "a number to colour by")],
     build=_px("bar_polar", color_continuous_scale="Viridis"))

_add("dumbbell", "Dumbbell chart", "scatter",
     required=[Slot("label", CAT, "an entity column"),
               Slot("start", NUM, "the before number"),
               Slot("end", NUM, "the after number")],
     build=_b_dumbbell)

_add("lollipop", "Lollipop chart", "scatter",
     required=[Slot("label", CAT, "a label column"), Slot("value", NUM, "one number")],
     build=_b_lollipop)

_add("cleveland", "Cleveland dot plot", "scatter",
     required=[Slot("label", CAT, "an entity column"),
               Slot("values", NUM, "two or more comparable numbers", many=True, min_n=2)],
     build=_b_cleveland)

_add("marimekko", "Marimekko / mosaic", "bar",
     required=[Slot("label", CAT, "a category column"),
               Slot("height", NUM, "the number that sets bar height"),
               Slot("width", NUM, "a second number for how big the category is")],
     build=_b_marimekko)

_add("multicategory", "Two-level category axis", "bar",
     required=[Slot("outer", CAT, "the outer grouping column"),
               Slot("inner", CAT, "the inner grouping column"),
               Slot("y", NUM, "a number for each pair")],
     build=_b_multicategory)

_add("facets", "Small multiples (facets)", "histogram",
     required=[Slot("x", NUM, "a number to spread out"),
               Slot("facet_col", CAT, "a low-cardinality column to split panels by")],
     build=_b_facets)

_add("facet_grid_ff", "Facet grid (figure factory)", "scatter",
     required=[Slot("x", NUM, "a number for the x axis"),
               Slot("y", NUM, "a second number for the y axis"),
               Slot("facet_col", CAT, "a column to split panels by")],
     build=_b_facet_grid_ff)

_add("table", "Table", "table",
     required=[Slot("columns", ANY, "at least one column of any kind", many=True, min_n=1)],
     build=_b_table)

_add("table_ff", "Table (figure factory)", "heatmap",
     required=[Slot("columns", ANY, "at least one column of any kind", many=True, min_n=1)],
     build=_b_table_ff)

# ------------------------------------------------------------- DISTRIBUTE
_add("histogram", "Histogram", "histogram",
     required=[Slot("x", NUM, "one number column with many rows")],
     optional=[S_COLOR], build=_b_histogram)

_add("histogram_cumulative", "Histogram, normalised and cumulative", "histogram",
     required=[Slot("x", NUM, "one number column with many rows")],
     optional=[S_COLOR], build=_b_histogram_cum)

_add("ecdf", "ECDF - the share below any value", "scatter",
     required=[Slot("x", NUM, "one number column")], optional=[S_COLOR],
     build=_px("ecdf", ecdfnorm="percent"))

_add("ecdf_ccdf", "ECDF, complementary, log-log", "scatter",
     required=[Slot("x", NUM, "one money-shaped number column")], build=_b_ecdf_ccdf)

_add("ecdf_weighted", "ECDF weighted by a count column", "scatter",
     required=[Slot("x", NUM, "the value column"),
               Slot("y", NUM, "a count column to weight each row by")],
     build=_px("ecdf", ecdfnorm="percent"))

_add("box", "Box plot", "box",
     required=[Slot("y", NUM, "one number column")],
     optional=[Slot("x", CAT, "a column to split the boxes by"), S_COLOR],
     build=_px("box", notched=True, points="suspectedoutliers"))

_add("box_precomputed", "Box from pre-computed quartiles", "box",
     required=[Slot("label", CAT, "a group column"),
               Slot("q1", NUM, "a pre-computed 25th-percentile column"),
               Slot("median", NUM, "a pre-computed median column"),
               Slot("q3", NUM, "a pre-computed 75th-percentile column")],
     optional=[Slot("lowerfence", NUM, "a low-whisker column"),
               Slot("upperfence", NUM, "a high-whisker column"),
               Slot("mean", NUM, "a mean column")],
     build=_b_box_precomputed)

_add("violin", "Violin", "violin",
     required=[Slot("y", NUM, "one number column")],
     optional=[Slot("x", CAT, "a column to split by"), S_COLOR],
     build=_px("violin", box=True, points=False))

_add("violin_split", "Split violin (back to back)", "violin",
     required=[Slot("x", CAT, "a grouping column"),
               Slot("y", NUM, "the number to compare"),
               Slot("split", CAT, "a two-value column for the two sides")],
     build=_b_violin_split)

_add("ridgeline", "Ridgeline", "violin",
     required=[Slot("category", CAT, "a category with 5 to 40 levels"),
               Slot("value", NUM, "the number whose shape you want")],
     build=_b_ridgeline)

_add("strip", "Strip plot - every single row", "box",
     required=[Slot("y", NUM, "one number column")],
     optional=[Slot("x", CAT, "a column to split by"), S_COLOR],
     build=_px("strip"))

_add("beeswarm", "Beeswarm", "scatter",
     required=[Slot("value", NUM, "one number column")], build=_b_beeswarm)

_add("raincloud", "Raincloud", "violin",
     required=[Slot("value", NUM, "one number column")], build=_b_raincloud)

_add("density_heatmap", "2D density heatmap", "histogram2d",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     build=_b_density_heatmap)

_add("density_contour", "2D density contour", "histogram2dcontour",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     optional=[S_COLOR], build=_px("density_contour"))

_add("density_2d_ff", "2D density (figure factory)", "histogram2dcontour",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     build=_b_density_2d_ff)

_add("isosurface", "Isosurface - the 3D threshold shell", "isosurface",
     required=[Slot("x", NUM, "an x position column"),
               Slot("y", NUM, "a y position column"),
               Slot("z", NUM, "a z position column"),
               Slot("value", NUM, "the value measured at each point")],
     build=_b_isosurface)

_add("volume", "Volume - the whole 3D cloud", "volume",
     required=[Slot("x", NUM, "an x position column"),
               Slot("y", NUM, "a y position column"),
               Slot("z", NUM, "a z position column"),
               Slot("value", NUM, "the value measured at each point")],
     build=_b_volume)

_add("distplot_blocked", "Distplot (histogram + smooth curve + rug)", "histogram")
_add("violin_ff_blocked", "Violin with smoothed curve (figure factory)", "violin")

# ----------------------------------------------------------------- RELATE
_add("scatter", "Scatter plot", "scatter",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     optional=[S_COLOR], build=_px("scatter", opacity=0.7))

_add("scatter_marginal", "Scatter with edge distributions", "scatter",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     build=_px("scatter", marginal_x="histogram", marginal_y="violin", opacity=0.55))

_add("scatter_trend", "Scatter with a trend line", "scatter",
     required=[Slot("x", NUM, "the number that orders the cloud"),
               Slot("y", NUM, "the number you think follows it")],
     build=_b_scatter_trend)

_add("bubble", "Bubble chart", "scatter",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column"),
               Slot("size", NUM, "a third number for dot size")],
     optional=[Slot("color", NUM, "a fourth number for dot colour")],
     build=_px("scatter", size_max=34, color_continuous_scale="Viridis", opacity=0.7))

_add("scattergl", "WebGL scatter (huge point counts)", "scattergl",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     build=_b_scattergl)

_add("quadrant", "Quadrant scatter", "scatter",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column")],
     build=_b_quadrant)

_add("splom", "Scatter plot matrix (splom)", "splom",
     required=[Slot("dimensions", NUM, "three or more number columns", many=True, min_n=3)],
     optional=[S_COLOR], build=_b_splom)

_add("splom_ff", "Scatterplot matrix (figure factory)", "scatter",
     required=[Slot("dimensions", NUM, "two or more number columns", many=True, min_n=2)],
     build=_b_splom_ff)

_add("parcoords", "Parallel coordinates", "parcoords",
     required=[Slot("dimensions", NUM, "three or more number columns", many=True, min_n=3)],
     optional=[Slot("color", NUM, "a number to colour the lines by")],
     build=_px("parallel_coordinates", color_continuous_scale="Viridis"))

_add("parcoords_constrained", "Parallel coordinates with a locked filter", "parcoords",
     required=[Slot("dimensions", NUM, "three or more number columns", many=True, min_n=3)],
     optional=[Slot("color", NUM, "a number to colour the lines by")],
     build=_b_parcoords_constrained)

_add("scatter3d", "3D scatter", "scatter3d",
     required=[Slot("x", NUM, "one number column"), Slot("y", NUM, "a second number"),
               Slot("z", NUM, "a third number")],
     optional=[Slot("color", NUM, "a number to colour by")],
     build=_px("scatter_3d", color_continuous_scale="Viridis", opacity=0.7))

_add("line3d", "3D line", "scatter3d",
     required=[Slot("x", NUM, "one number column"), Slot("y", NUM, "a second number"),
               Slot("z", NUM, "a third number")],
     optional=[S_COLOR], build=_px("line_3d"))

_add("scatter3d_ribbon", "3D ribbon (filled 3D line)", "scatter3d",
     required=[Slot("x", NUM, "one number column"), Slot("y", NUM, "a second number"),
               Slot("z", NUM, "a third number")],
     optional=[Slot("color", CAT, "a column to make one ribbon per group")],
     build=_b_scatter3d_ribbon)

_add("surface", "Surface", "surface",
     required=[Slot("x", CAT, "a grid-column label"),
               Slot("y", CAT, "a grid-row label"),
               Slot("z", NUM, "the value at each pair")],
     build=_b_surface)

_add("mesh3d", "Mesh3d - a solid from a point cloud", "mesh3d",
     required=[Slot("x", NUM, "one number column"), Slot("y", NUM, "a second number"),
               Slot("z", NUM, "a third number")],
     build=_b_mesh3d)

_add("trisurf_ff", "Trisurf (figure factory)", "mesh3d", demo_only=True,
     demo_why="it needs an explicit list of which three points make each triangle, "
              "which no SQL result carries.")

_add("radar", "Radar / spider chart", "scatterpolar",
     required=[Slot("entity", CAT, "an entity column"),
               Slot("values", NUM, "three or more comparable score columns",
                    many=True, min_n=3)],
     build=_b_radar)

_add("polar", "Polar scatter / line", "scatterpolar",
     required=[Slot("theta", CAT, "a cyclical category such as an hour or a month"),
               Slot("r", NUM, "a number for each one")],
     optional=[S_COLOR], build=_b_polar)

_add("scatterpolargl", "Polar scatter, WebGL", "scatterpolargl",
     required=[Slot("theta", NUM, "an angle column, 0 to 360"),
               Slot("r", NUM, "a radius column")],
     build=_px("scatter_polar", render_mode="webgl", opacity=0.3))

_add("secondary_y", "Two units on one x axis (secondary y)", "scatter",
     required=[Slot("x", ANY, "a shared x column"),
               Slot("y1", NUM, "the number on the left axis"),
               Slot("y2", NUM, "a second number in different units")],
     build=_b_secondary_y)

_add("scattersmith", "Smith chart", "scattersmith",
     required=[Slot("real", NUM, "the real part of an impedance"),
               Slot("imag", NUM, "the imaginary part")],
     build=_b_scattersmith)

_add("carpet", "Carpet - the graph paper itself", "carpet",
     required=[Slot("a", NUM, "the a coordinate"), Slot("b", NUM, "the b coordinate"),
               Slot("x", NUM, "where that node lands on x"),
               Slot("y", NUM, "where it lands on y")],
     build=_b_carpet)

_add("scattercarpet", "Scattercarpet - points on a warped grid", "scattercarpet",
     required=[Slot("a", NUM, "the a coordinate"), Slot("b", NUM, "the b coordinate"),
               Slot("x", NUM, "where that node lands on x"),
               Slot("y", NUM, "where it lands on y")],
     build=_b_scattercarpet)

_add("contourcarpet", "Contourcarpet - contours on a warped grid", "contourcarpet",
     required=[Slot("a", NUM, "the a coordinate"), Slot("b", NUM, "the b coordinate"),
               Slot("x", NUM, "where that node lands on x"),
               Slot("y", NUM, "where it lands on y"),
               Slot("z", NUM, "the value measured there")],
     build=_b_contourcarpet)

_add("ols_trend_blocked", "Ordinary-least-squares / lowess trend line", "scatter")
_add("dendrogram_blocked", "Dendrogram (clustering tree)", "scatter")

# ---------------------------------------------------------------- COMPOSE
_add("pie", "Pie / donut", "pie",
     required=[Slot("names", CAT, "a category column with six or fewer values"),
               Slot("values", NUM, "a number that sums to a real whole")],
     build=_px("pie", hole=0.45))

_add("bar_stacked", "Stacked bar", "bar",
     required=[S_X_CAT, S_Y_NUM, Slot("color", CAT, "a subcategory column")],
     build=_px("bar"))

_add("bar_barnorm", "100% stacked bar", "bar",
     required=[S_X_CAT, S_Y_NUM, Slot("color", CAT, "a subcategory column")],
     build=_b_bar_barnorm)

_add("area", "Area chart", "scatter",
     required=[Slot("x", DATE, "a date column"), S_Y_NUM],
     optional=[S_COLOR], build=_px("area"))

_add("area_norm", "100% stacked area", "scatter",
     required=[Slot("x", DATE, "a date column"), S_Y_NUM,
               Slot("color", CAT, "a category column to split the mix by")],
     build=_px("area", groupnorm="fraction"))

_add("streamgraph", "Streamgraph", "scatter",
     required=[Slot("x", DATE, "a date column"), S_Y_NUM,
               Slot("color", CAT, "a category column, one band each")],
     build=_b_streamgraph)

_add("treemap", "Treemap", "treemap",
     required=[Slot("path", CAT, "one or more nesting columns, broad to narrow",
                    many=True, min_n=1),
               Slot("values", NUM, "a number to size the boxes by")],
     build=_px("treemap", color_continuous_scale="Viridis"))

_add("sunburst", "Sunburst", "sunburst",
     required=[Slot("path", CAT, "one or more nesting columns, broad to narrow",
                    many=True, min_n=1),
               Slot("values", NUM, "a number to size the rings by")],
     build=_px("sunburst", color_continuous_scale="Viridis"))

_add("icicle", "Icicle", "icicle",
     required=[Slot("path", CAT, "one or more nesting columns, broad to narrow",
                    many=True, min_n=1),
               Slot("values", NUM, "a number to size the bars by")],
     build=_px("icicle", color_continuous_scale="Viridis"))

_add("flamegraph", "Flame graph", "icicle",
     required=[Slot("path", CAT, "one or more nesting columns, broad to narrow",
                    many=True, min_n=1),
               Slot("values", NUM, "a number to size the bars by")],
     build=_b_flamegraph)

_add("funnelarea", "Funnel area", "funnelarea",
     required=[Slot("names", CAT, "an ordered stage column"),
               Slot("values", NUM, "a count that shrinks")],
     build=_px("funnel_area"))

_add("ternary", "Ternary scatter", "scatterternary",
     required=[Slot("a", NUM, "the first part"), Slot("b", NUM, "the second part"),
               Slot("c", NUM, "the third part")],
     optional=[S_COLOR], build=_px("scatter_ternary", opacity=0.7))

_add("line_ternary", "Ternary line", "scatterternary",
     required=[Slot("a", NUM, "the first part"), Slot("b", NUM, "the second part"),
               Slot("c", NUM, "the third part")],
     optional=[S_COLOR], build=_px("line_ternary", markers=True))

_add("waffle", "Waffle / unit chart", "heatmap",
     required=[Slot("label", CAT, "a category column"),
               Slot("share", NUM, "a number that is a share of the whole")],
     build=_b_waffle)

_add("pyramid", "Population pyramid", "bar",
     required=[Slot("band", CAT, "an ordered band column, e.g. an age group"),
               Slot("left", NUM, "the left-hand count"),
               Slot("right", NUM, "the right-hand count")],
     build=_b_pyramid)

_add("ternary_contour_blocked", "Ternary contour", "scatterternary")

# ------------------------------------------------------------------- FLOW
_add("sankey", "Sankey diagram", "sankey",
     required=[Slot("source", CAT, "a source column"),
               Slot("target", CAT, "a target column"),
               Slot("value", NUM, "a value column")],
     build=_b_sankey)

_add("sankey_grouped", "Sankey with grouped nodes and arrow links", "sankey",
     required=[Slot("source", CAT, "a source column"),
               Slot("target", CAT, "a target column"),
               Slot("value", NUM, "a value column")],
     build=_b_sankey_grouped)

_add("parcats", "Parallel categories", "parcats",
     required=[Slot("dimensions", CAT, "three or more category columns",
                    many=True, min_n=3)],
     optional=[Slot("color", NUM, "a number to colour the ribbons by")],
     build=_b_parcats)

_add("funnel", "Funnel", "funnel",
     required=[Slot("y", CAT, "an ordered stage column"),
               Slot("x", NUM, "a count that shrinks at each stage")],
     build=_b_funnel)

_add("funnel_grouped", "Grouped funnel", "funnel",
     required=[Slot("y", CAT, "an ordered stage column"),
               Slot("x", NUM, "a count that shrinks"),
               Slot("color", CAT, "a column naming which pipeline each row is")],
     build=_px("funnel"))

_add("cone", "Cone - a 3D vector field", "cone",
     required=[Slot("x", NUM, "an x position"), Slot("y", NUM, "a y position"),
               Slot("z", NUM, "a z position"), Slot("u", NUM, "an x direction"),
               Slot("v", NUM, "a y direction"), Slot("w", NUM, "a z direction")],
     build=_b_cone)

_add("streamtube", "Streamtube - the paths through a field", "streamtube",
     required=[Slot("x", NUM, "an x position"), Slot("y", NUM, "a y position"),
               Slot("z", NUM, "a z position"), Slot("u", NUM, "an x direction"),
               Slot("v", NUM, "a y direction"), Slot("w", NUM, "a z direction")],
     build=_b_streamtube)

_add("quiver_ff", "Quiver plot (2D arrows)", "scatter",
     required=[Slot("x", NUM, "an x position"), Slot("y", NUM, "a y position"),
               Slot("u", NUM, "an x direction"), Slot("v", NUM, "a y direction")],
     build=_b_quiver_ff)

_add("streamline_ff", "Streamlines (2D)", "scatter", demo_only=True,
     demo_why="it needs a regular grid of directions, not a flat list of rows.")

# ------------------------------------------------------------------- RANK
_add("rank_bar", "Ranked horizontal bar", "bar",
     required=[Slot("label", CAT, "an entity column"), Slot("value", NUM, "one number")],
     build=_b_rank_bar)

_add("bump", "Bump chart", "scatter",
     required=[Slot("x", ANY, "a period column"),
               Slot("rank", NUM, "a rank column, 1 for the top"),
               Slot("entity", CAT, "an entity column")],
     build=_b_bump)

_add("slope", "Slope chart", "scatter",
     required=[Slot("x", ANY, "a period column with at least two values"),
               Slot("y", NUM, "the number that moved"),
               Slot("entity", CAT, "an entity column")],
     build=_b_slope)

_add("pareto", "Pareto chart", "bar",
     required=[Slot("label", CAT, "an entity column"),
               Slot("value", NUM, "the number to accumulate")],
     build=_b_pareto)

_add("rank_heatmap", "Rank as a heatmap", "heatmap",
     required=[Slot("entity", CAT, "an entity column"),
               Slot("period", ANY, "a period column"),
               Slot("value", NUM, "a rank or a value for each pair")],
     build=_b_rank_heatmap)

_add("legend_isolate", "Legend as an isolate control", "scatter",
     required=[Slot("x", ANY, "an ordered column"), Slot("y", NUM, "one number"),
               Slot("color", CAT, "a column with several series in it")],
     build=_b_legend_isolate)

# ----------------------------------------------------------------- LOCATE
_add("choropleth", "Choropleth (built-in outlines)", "choropleth",
     required=[Slot("locations", GEO, "a place-code column such as a state code or an ISO country"),
               Slot("color", NUM, "a number for each place")],
     build=_px("choropleth", locationmode="USA-states", scope="usa",
               color_continuous_scale="Viridis"))

_add("choropleth_diverging", "Diverging choropleth", "choropleth",
     required=[Slot("locations", GEO, "a place-code column"),
               Slot("color", NUM, "a number that can sit either side of zero")],
     build=_px("choropleth", locationmode="USA-states", scope="usa",
               color_continuous_scale="RdBu", color_continuous_midpoint=0))

_add("choropleth_facet", "Small-multiple maps (facets)", "choropleth",
     required=[Slot("locations", GEO, "a place-code column"),
               Slot("color", NUM, "a number for each place"),
               Slot("facet_col", CAT, "one more low-cardinality column, e.g. year")],
     build=_b_choropleth_facet)

_add("scatter_geo", "Geo scatter (bubble map)", "scattergeo",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     optional=[Slot("size", NUM, "a number for circle size"),
               Slot("color", NUM, "a number for circle colour")],
     build=_px("scatter_geo", scope="usa", color_continuous_scale="Viridis",
               size_max=18, opacity=0.65))

_add("line_geo", "Geo connection map", "scattergeo",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column"),
               Slot("color", CAT, "a route column so each journey is one line")],
     build=_px("line_geo", scope="usa", markers=True))

_add("geo_projection", "Orthographic globe", "scattergeo",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     optional=[Slot("color", NUM, "a number to colour by")],
     build=_px("scatter_geo", projection="orthographic",
               color_continuous_scale="Viridis", opacity=0.7))

_add("scatter_map", "Tile-map scatter", "scattermap",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     optional=[Slot("size", NUM, "a number for circle size"),
               Slot("color", NUM, "a number for circle colour")],
     build=_px("scatter_map", zoom=3, map_style="white-bg",
               color_continuous_scale="Viridis", size_max=16, opacity=0.7))

_add("density_map", "Tile-map density (hotspot blur)", "densitymap",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     optional=[Slot("z", NUM, "a weight column")],
     build=_px("density_map", radius=22, zoom=3, map_style="white-bg",
               color_continuous_scale="Viridis"))

_add("choropleth_map", "Tile-map choropleth (your own boundaries)", "choroplethmap",
     demo_only=True,
     demo_why="it needs a GeoJSON of your own boundaries, and a SQL result cannot "
              "carry polygons.")

_add("line_map", "Line map (tile)", "scattermap",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column"),
               Slot("color", CAT, "a route column so each journey is one line")],
     build=_px("line_map", zoom=4, map_style="white-bg"))

_add("hexbin_ff", "Hexbin map", "choroplethmap",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     build=_b_hexbin_ff)

_add("geo_subplots", "Geo subplot grid", "choropleth",
     required=[Slot("locations", GEO, "a place-code column"),
               Slot("values", NUM, "one or more numbers, one map each",
                    many=True, min_n=1)],
     build=_b_geo_subplots)

_add("image", "Image as a plot layer", "image", demo_only=True,
     demo_why="it draws actual pixels - a scan, a floor plan, a screenshot - not rows.")

_add("mapbox_deprecated", "Deprecated mapbox family", "scattermapbox",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     optional=[Slot("size", NUM, "a number for circle size"),
               Slot("color", NUM, "a number for circle colour")],
     build=_b_mapbox_deprecated)

_add("mapbox_deprecated_family", "Deprecated mapbox: density, choropleth and line",
     "densitymapbox", demo_only=True,
     demo_why="it is three different deprecated maps in one figure, shown together so "
              "none of them is hidden from you.")

_add("hexbin_mapbox_ff", "Hexbin map (deprecated mapbox twin)", "choroplethmap",
     required=[Slot("lat", LAT, "a latitude column"), Slot("lon", LON, "a longitude column")],
     build=_b_hexbin_mapbox_ff)

_add("county_choropleth_blocked", "US county choropleth by FIPS", "choropleth")

# ----------------------------------------------------------------- CHANGE
_add("line", "Line chart", "scatter",
     required=[Slot("x", DATE, "a date column"), S_Y_NUM],
     optional=[S_COLOR], build=_b_line)

_add("line_step", "Step line", "scatter",
     required=[Slot("x", DATE, "a date column"),
               Slot("y", NUM, "a number that holds then jumps")],
     optional=[S_COLOR], build=_b_line_step)

_add("band", "Line with a confidence band", "scatter",
     required=[Slot("x", DATE, "a date column"),
               Slot("y", NUM, "the central estimate"),
               Slot("low", NUM, "the lower bound"),
               Slot("high", NUM, "the upper bound")],
     build=_b_band)

_add("events", "Event markers on a time series", "scatter",
     required=[Slot("x", DATE, "a date column"), S_Y_NUM],
     optional=[S_COLOR], build=_b_events)

_add("rangeslider", "Range slider + range selector", "scatter",
     required=[Slot("x", DATE, "a long date column"), S_Y_NUM],
     optional=[S_COLOR], build=_b_rangeslider)

_add("rangebreaks", "Rangebreaks - delete the dead time", "scatter",
     required=[Slot("x", DATE, "a date column with weekend gaps"), S_Y_NUM],
     optional=[S_COLOR], build=_b_rangebreaks)

_add("tickformatstops", "Zoom-aware date labels", "scatter",
     required=[Slot("x", DATE, "a date column"), S_Y_NUM],
     optional=[S_COLOR], build=_b_tickformatstops)

_add("bar_time", "Bars over periods", "bar",
     required=[Slot("x", DATE, "a date column"), Slot("y", NUM, "a number to total")],
     optional=[S_COLOR], build=_b_bar_time)

_add("timeline", "Gantt / timeline", "bar",
     required=[Slot("x_start", DATE, "a start-date column"),
               Slot("x_end", DATE, "an end-date column"),
               Slot("y", CAT, "the thing each row is about")],
     optional=[S_COLOR], build=_b_timeline)

_add("gantt_ff", "Gantt (figure factory)", "scatter",
     required=[Slot("x_start", DATE, "a start-date column"),
               Slot("x_end", DATE, "an end-date column"),
               Slot("y", CAT, "a task column")],
     optional=[S_COLOR], build=_b_gantt_ff)

_add("waterfall", "Waterfall", "waterfall",
     required=[Slot("label", CAT, "a step-label column"),
               Slot("delta", NUM, "the signed change at each step")],
     optional=[Slot("measure", CAT, "a column tagging each step relative / total / absolute")],
     build=_b_waterfall)

_add("candlestick", "Candlestick", "candlestick",
     required=[Slot("x", DATE, "a date column"), Slot("open", NUM, "an open column"),
               Slot("high", NUM, "a high column"), Slot("low", NUM, "a low column"),
               Slot("close", NUM, "a close column")],
     build=_b_candlestick)

_add("ohlc", "OHLC bars", "ohlc",
     required=[Slot("x", DATE, "a date column"), Slot("open", NUM, "an open column"),
               Slot("high", NUM, "a high column"), Slot("low", NUM, "a low column"),
               Slot("close", NUM, "a close column")],
     build=_b_ohlc)

_add("candlestick_ff", "Candlestick (figure factory)", "box",
     required=[Slot("x", DATE, "a date column"), Slot("open", NUM, "an open column"),
               Slot("high", NUM, "a high column"), Slot("low", NUM, "a low column"),
               Slot("close", NUM, "a close column")],
     build=_b_candlestick_ff)

_add("ohlc_ff", "OHLC (figure factory)", "scatter",
     required=[Slot("x", DATE, "a date column"), Slot("open", NUM, "an open column"),
               Slot("high", NUM, "a high column"), Slot("low", NUM, "a low column"),
               Slot("close", NUM, "a close column")],
     build=_b_ohlc_ff)

_add("calendar_heatmap", "Calendar heatmap", "heatmap",
     required=[Slot("date", DATE, "a date column"), Slot("value", NUM, "a count")],
     build=_b_calendar_heatmap)

_add("entity_period_heatmap", "Entity x period heatmap", "heatmap",
     required=[Slot("entity", CAT, "an entity column"),
               Slot("period", ANY, "a period column"),
               Slot("value", NUM, "a number that can straddle zero")],
     build=_b_entity_period_heatmap)

_add("animation", "Animation over time", "scatter",
     required=[Slot("x", NUM, "one number column"),
               Slot("y", NUM, "a second number column"),
               Slot("entity", CAT, "an entity column, so a dot glides not teleports"),
               Slot("frame", ANY, "a time column, one frame each")],
     optional=[Slot("size", NUM, "a number for dot size")],
     build=_b_animation)

# ---------------------------------------------------------------- CONNECT
_add("network", "Node-link network", "scatter",
     required=[Slot("source", CAT, "a from column"), Slot("target", CAT, "a to column")],
     build=_b_network)

_add("arc_diagram", "Arc diagram", "scatter",
     required=[Slot("source", CAT, "a from column"), Slot("target", CAT, "a to column")],
     build=_b_arc_diagram)

_add("overlap_matrix", "Overlap matrix", "heatmap",
     required=[Slot("x", CAT, "one side of the pair"),
               Slot("y", CAT, "the other side of the pair"),
               Slot("z", NUM, "how much they share")],
     build=_b_overlap_matrix)

_add("upset_bar", "Set-combination bar (UpSet's top half)", "bar",
     required=[Slot("sets", CAT, "two or more yes/no membership columns",
                    many=True, min_n=2)],
     build=_b_upset_bar)

# ----------------------------------------------------------- SINGLE VALUE
_add("indicator", "Indicator - number and delta", "indicator",
     required=[Slot("value", NUM, "one number column")],
     optional=[Slot("reference", NUM, "a prior value to compare against")],
     build=_b_indicator)

_add("indicator_gauge", "Indicator - gauge dial", "indicator",
     required=[Slot("value", NUM, "one number column")],
     optional=[Slot("reference", NUM, "a target to draw the threshold at")],
     build=_b_indicator_gauge)

_add("indicator_bullet", "Indicator - bullet bar", "indicator",
     required=[Slot("label", CAT, "a label column"), Slot("value", NUM, "one number")],
     optional=[Slot("target", NUM, "the target for each row")],
     build=_b_indicator_bullet)

_add("kpi_row", "KPI row", "indicator",
     required=[Slot("label", CAT, "a label column"),
               Slot("value", NUM, "the number on each tile")],
     optional=[Slot("reference", NUM, "the prior value on each tile")],
     build=_b_kpi_row)

_add("bullet_ff", "Bullet chart (figure factory)", "bar",
     required=[Slot("label", CAT, "a label column"), Slot("value", NUM, "the actual"),
               Slot("target", NUM, "the target")],
     build=_b_bullet_ff)

_add("sparkline_kpi", "Number with a sparkline behind it", "indicator",
     required=[Slot("value", NUM, "one number column with a few rows of history")],
     build=_b_sparkline_kpi)

_add("kpi_table", "One number with its context rows", "table",
     required=[Slot("columns", ANY, "one or more columns of any kind",
                    many=True, min_n=1)],
     build=_b_kpi_table)


# -- integrity checks, run at import ----------------------------------
if _LEFT:
    raise RuntimeError(
        "bench/wall.py has charts registry.py never registered: "
        + ", ".join(sorted(_LEFT))
    )

for _t in TEMPLATES:
    if not _t.blocked and not _t.demo_only and _t.build is None:
        raise RuntimeError(f"{_t.key}: no builder")
    if _t.trace_type not in TRACE_CLASSES:
        raise RuntimeError(
            f"{_t.key}: {_t.trace_type!r} is not one of Plotly's trace types"
        )

CHARTS: dict[str, ChartTemplate] = {t.key: t for t in TEMPLATES}
SECTIONS: list[tuple[str, str]] = list(wall.SECTIONS)
BY_SECTION: dict[str, list[ChartTemplate]] = {
    name: [t for t in TEMPLATES if t.section == name] for name, _ in SECTIONS
}

# The keys whose whole chart really is one Plotly Express call with nothing
# but the mapping in it. codegen.py can print those as `px.<key>(df, ...)`.
# Everything else has styling baked into its builder, so its honest code line
# is `bench.registry.build("<key>", df, ...)`.
PX_PURE: frozenset[str] = frozenset(
    t.key for t in TEMPLATES
    if getattr(t.build, "px_pure", None) == t.key
)

# A pure-px chart prints in the code panel as a bare `px.thing(df, ...)`, which
# is only true if its builder hands the frame to px untouched. `_px` DOES touch
# it when a size slot holds negative numbers (see `_magnitude`), so a pure-px
# chart may never declare a size slot. Checked at import, not assumed.
for _t in TEMPLATES:
    if _t.key in PX_PURE and _t.slot("size") is not None:
        raise RuntimeError(
            f"{_t.key} is printed as a bare px call but declares a size slot, "
            "which _magnitude may rewrite. Give it a named builder instead."
        )


# =====================================================================
# THE SEAMS - what the other Bench modules call
# =====================================================================


def trace_type(key: str) -> str | None:
    """
    Which trace does this chart draw? `knobs.trace_type_for` asks this first.

    Returns Plotly's own spelling ("bar", "sankey", "scattermap"), or None for
    a key this registry does not know - knobs.py then falls back to reading the
    key as a trace name itself.
    """
    t = CHARTS.get((key or "").strip())
    return t.trace_type if t else None


def build(key: str, df: pd.DataFrame, **mapping) -> go.Figure:
    """
    Draw a chart by key. This is the function codegen.py writes into the
    generated code for every chart with no Plotly Express front door:

        fig = bench.registry.build("sankey", df, source="SRC", target="TGT",
                                   value="AMOUNT")

    Knobs are deliberately NOT applied here - the generated code sets those on
    the next lines with `fig.update_traces(...)` / `fig.update_layout(...)`,
    which is what makes the code panel readable.
    """
    if key not in CHARTS:
        raise KeyError(
            f"no chart called {key!r}. Try one of: "
            + ", ".join(sorted(CHARTS)[:8]) + ", ..."
        )
    return CHARTS[key].builder(df, mapping, None)


# =====================================================================
# SELF TEST - run `python bench/registry.py`
# =====================================================================


def _demo_frames() -> dict[str, pd.DataFrame]:
    """The demo shapes from wall.py, as the frames a warehouse might return."""
    return {
        "category (label + number)": wall.d_category(),
        "long (category + many rows)": wall.d_long(),
        "scatter (numbers + a group)": wall.d_scatter(400),
        "timeseries (date + cat + num)": wall.d_timeseries(200),
        "flow (source/target/amount)": wall.d_flow(),
        "geo points (lat/lon/amount)": wall.d_geo_points(300),
        "states (place code + 2 nums)": wall.d_states(),
        "ohlc (date + 4 prices)": wall.d_ohlc(60),
        "hierarchy (3 levels + num)": wall.d_hierarchy(),
        "numeric block (5 numbers)": wall.d_numeric_block(200),
        "stages (stage + count)": wall.d_stages(),
        "rank over time": wall.d_rank_over_time(),
    }


def _self_test() -> int:
    import traceback

    print(f"templates          : {len(TEMPLATES)}")
    print(f"  with a builder   : {sum(1 for t in TEMPLATES if t.build)}")
    print(f"  demo-only        : {sum(1 for t in TEMPLATES if t.demo_only)}")
    print(f"  blocked here     : {sum(1 for t in TEMPLATES if t.blocked)}")
    print(f"  pure-px keys     : {len(PX_PURE)}  ({', '.join(sorted(PX_PURE))})")
    assert len(CHARTS) == len(TEMPLATES), "duplicate keys"
    for t in TEMPLATES:
        assert t.key and t.key.islower() and "-" not in t.key, t.key
        assert t.trace_type in TRACE_CLASSES, t.key
        assert hasattr(go, t.trace_class), t.key
        assert trace_type(t.key) == t.trace_type, t.key
        assert t.blocked or t.demo_only or t.build, t.key
        assert t.blocked or t.demo_only or t.required, f"{t.key} has no mapping slots"
    print("keys unique, trace types real, slots present : OK")

    bad = 0
    for label, df in _demo_frames().items():
        r = roles(df)
        ok = [t for t in TEMPLATES if drawable(r, t)[0]]
        drew = 0
        for t in ok:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fig = t.builder(df, auto_map(r, t), {"layout.title.text": t.name})
                assert isinstance(fig, go.Figure)
                drew += 1
            except Exception as exc:  # noqa: BLE001
                bad += 1
                print(f"    FAIL {t.key}: {type(exc).__name__}: {exc}")
                traceback.print_exc(limit=2)
        print(f"{label:32s} {len(ok):3d} drawable, {drew:3d} built  ({describe(r)})")

    print("\nsample reasons on a two-column frame:")
    tiny = pd.DataFrame({"agency": ["a", "b"], "spend": [1.0, 2.0]})
    rt = roles(tiny)
    for key in ("sankey", "candlestick", "scatter_geo", "corr_matrix", "bar",
                "treemap", "distplot_blocked", "image"):
        ok, why = drawable(rt, CHARTS[key])
        print(f"  [{'yes' if ok else 'no ':3s}] {why}")

    print(f"\nbuild failures: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(_self_test())
