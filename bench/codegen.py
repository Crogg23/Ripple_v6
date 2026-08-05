#!/usr/bin/env python
"""
CODEGEN - the two-way bridge between the knob panel and the code panel.

Two functions, and they are each other's mirror:

    render(spec) -> str          the SPEC dict, written out as Python
    parse(src)   -> spec | None  that Python, read back into a SPEC dict

The contract the whole Bench rests on:

    parse(render(spec)) == spec        exactly, for every canonical spec

"Exactly" means the values come back as the same Python objects they went in
as - a string is still that string, 0.8 is still the float 0.8, False is still
False and not 0, None is still None, and a list is still that list.

WHY THIS MODULE IS PURE PYTHON
------------------------------
It imports `ast` and `math` and nothing else. No dash, no plotly, no
snowflake. That is deliberate: this is the one piece of the Bench that has to
be provably right, and a module with no dependencies is a module you can test
in a millisecond and reason about on paper.

The cost of that purity is two small tables of measured facts (UNDERSCORE_NAMES
and PX_CHARTS). Both were read straight out of plotly 6.9.0 - the numbers are
in the comments beside them - and tests/test_bench_codegen.py re-measures them
against the live library so they cannot silently drift.

WHAT "CANONICAL FORM" LOOKS LIKE
--------------------------------
    # --- data ---------------------------------------------------------
    df = bench.data.frame({"kind": "demo", "name": "entity_count"})

    # --- chart --------------------------------------------------------
    fig = px.bar(df, x="STATE", y="TOTAL")

    # --- MARK ---------------------------------------------------------
    fig.update_traces(marker_opacity=0.8)

    # --- SCALE --------------------------------------------------------
    fig.update_layout(xaxis_categoryorder="total descending")

    fig.show()

One call per bucket, buckets always in the order MARK, SCALE, FRAME,
INTERACTION, MOTION. A bucket with nothing in it emits nothing at all - no
empty call, no lonely comment. Every section carries its bucket name, because
that comment is the reader's map back to ATLAS section 1.1.

WHERE IT HONESTLY BREAKS
------------------------
`parse` accepts the shape above and very little else. Anything it does not
recognise comes back as `None`, which is the app's signal to drop into CUSTOM
mode: the chart still draws, the knobs go read-only, a Reset button brings you
home. That is a feature. It is the escape hatch that stops the knob panel from
ever becoming a ceiling.

`parse` NEVER raises. A broken edit is a return value, not an exception.
"""

from __future__ import annotations

import ast
import math
import warnings
from typing import Any, Iterable

# =====================================================================
# MEASURED FACTS
# ---------------------------------------------------------------------
# Two tables. Both were counted by walking plotly 6.9.0 itself, not
# remembered. tests/test_bench_codegen.py re-counts them.
# =====================================================================

# Plotly's "magic underscore" writes a nested path as one keyword:
# layout.xaxis.categoryorder becomes xaxis_categoryorder. To read that back
# we have to know which property NAMES carry an underscore of their own -
# paper_bgcolor is ONE name, not paper -> bgcolor.
#
# Measured on plotly 6.9.0 by walking layout + all 49 registered trace types
# + go.Frame to the bottom (1,062 distinct classes, 882 distinct property
# names): exactly SEVEN names contain an underscore, and not one of their
# leading words ("copy", "error", "paper", "plot") is a property name
# anywhere else in the library. That is what makes the split unambiguous.
UNDERSCORE_NAMES: frozenset[str] = frozenset({
    "copy_ystyle",
    "copy_zstyle",
    "error_x",
    "error_y",
    "error_z",
    "paper_bgcolor",
    "plot_bgcolor",
})

# The registry keys that are also real Plotly Express functions, so the chart
# line can read `px.bar(df, ...)` instead of going through the registry.
# Measured on plotly 6.9.0: 39 functions that take a `data_frame` argument,
# plus `imshow`, which takes pixels or a grid instead. 40 in total.
#
# registry.py may add to or subtract from this set at import time. Doing so
# changes how the chart line READS; it cannot break the round trip, because
# `parse` recovers the same key from either form.
PX_CHARTS: set[str] = {
    "area", "bar", "bar_polar", "box", "choropleth", "choropleth_map",
    "choropleth_mapbox", "density_contour", "density_heatmap", "density_map",
    "density_mapbox", "ecdf", "funnel", "funnel_area", "histogram", "icicle",
    "imshow", "line", "line_3d", "line_geo", "line_map", "line_mapbox",
    "line_polar", "line_ternary", "parallel_categories",
    "parallel_coordinates", "pie", "scatter", "scatter_3d", "scatter_geo",
    "scatter_map", "scatter_mapbox", "scatter_matrix", "scatter_polar",
    "scatter_ternary", "strip", "sunburst", "timeline", "treemap", "violin",
}


# =====================================================================
# SHAPE CONSTANTS
# ---------------------------------------------------------------------
# The literal text of the canonical form. Change one of these and every
# rendered snippet changes with it - which is the point, there is exactly
# one place that decides what the code panel looks like.
# =====================================================================

SOURCE_CALL = "bench.data.frame"      # where the DataFrame comes from (SPEC 7)
REGISTRY_CALL = "bench.registry.build"  # the fallback chart builder (SPEC 6)
PX_NAMESPACE = "px"                   # how plotly.express is imported up top

HEADER_WIDTH = 68   # "# --- MARK ---...---" is padded out to this many chars
WRAP_AT = 88        # a call longer than this gets one argument per line
MAX_DEPTH = 20      # how deep a nested list/dict value may go before we quit

# The five buckets that emit code, in the order they emit it. DATA is absent
# on purpose: DATA is the `mapping` dict, and it rides on the chart line.
BUCKET_ORDER: tuple[str, ...] = ("MARK", "SCALE", "FRAME", "INTERACTION", "MOTION")

# Which Plotly call each bucket writes into. MARK is trace-side; the other
# four are layout-side. That is ATLAS section 1.1, and it is also how `parse`
# knows whether a keyword it just read is a `trace.` path or a `layout.` one.
BUCKET_CALL: dict[str, str] = {
    "MARK": "update_traces",
    "SCALE": "update_layout",
    "FRAME": "update_layout",
    "INTERACTION": "update_layout",
    "MOTION": "update_layout",
}

# The mapping slots, in the order they read best on the chart line. Anything
# not named here sorts alphabetically after these. Order is cosmetic only -
# two dicts with the same pairs are equal whatever order they were built in -
# but "px.bar(df, x=..., y=..., color=...)" reads like the docs and
# "px.bar(df, color=..., x=..., y=...)" does not.
MAPPING_ORDER: tuple[str, ...] = (
    "x", "y", "z",
    "x_start", "x_end",
    "lat", "lon", "locations", "geojson", "featureidkey",
    "a", "b", "c", "r", "theta", "real", "imag",
    "open", "high", "low", "close",
    "labels", "parents", "values", "names", "path", "dimensions",
    "source", "target", "value",
    "color", "size", "symbol", "pattern_shape", "line_dash",
    "text", "hover_name", "hover_data",
    "facet_row", "facet_col",
    "animation_frame", "animation_group",
)


# =====================================================================
# BUCKETS - which of the six a dotted path belongs to
# ---------------------------------------------------------------------
# SPEC 4.2, spelled out as a table. First match wins.
#
# One honest gap, called out rather than hidden: this module cannot run a
# Plotly validator, so it cannot see the "any DataArrayValidator" half of the
# DATA rule. It matches the eight names SPEC 4.2 lists by hand. knobs.py,
# which CAN run a validator, is welcome to widen DATA_NAMES at import time.
# It makes no difference to the generated code either way - see _emit_bucket.
# =====================================================================

DATA_NAMES: set[str] = {
    "x", "y", "z", "color", "values", "labels", "parents", "text",
}

# Each rule is (pattern, bucket). A pattern ending in "*" is a startswith
# test on the FIRST segment after the "layout." prefix; a pattern starting
# with "*" is an endswith test; anything else is an exact match.
_LAYOUT_RULES: tuple[tuple[str, str], ...] = (
    # SCALE - how numbers and categories become position and colour
    ("xaxis*", "SCALE"), ("yaxis*", "SCALE"),
    ("coloraxis*", "SCALE"), ("*colorway", "SCALE"),
    ("polar*", "SCALE"), ("geo*", "SCALE"), ("scene*", "SCALE"),
    ("ternary*", "SCALE"), ("map*", "SCALE"), ("smith*", "SCALE"),
    # FRAME - everything around and behind the data
    ("title*", "FRAME"), ("legend*", "FRAME"), ("margin*", "FRAME"),
    ("font*", "FRAME"), ("annotations", "FRAME"), ("shapes", "FRAME"),
    ("images", "FRAME"), ("paper_bgcolor", "FRAME"), ("plot_bgcolor", "FRAME"),
    ("width", "FRAME"), ("height", "FRAME"), ("template", "FRAME"),
    ("showlegend", "FRAME"), ("grid", "FRAME"), ("uniformtext", "FRAME"),
    # INTERACTION - what happens when a human touches it
    ("hover*", "INTERACTION"), ("click*", "INTERACTION"),
    ("drag*", "INTERACTION"), ("select*", "INTERACTION"),
    ("modebar", "INTERACTION"), ("updatemenus", "INTERACTION"),
    ("sliders", "INTERACTION"), ("spikedistance", "INTERACTION"),
    ("newshape", "INTERACTION"),
    # MOTION - animation
    ("transition*", "MOTION"),
)


def bucket_for(path: str) -> str:
    """Which of the six ATLAS buckets does this dotted path live in?

    `path` is prefixed `trace.` or `layout.` and nothing else (SPEC 3).

        >>> bucket_for("layout.xaxis.categoryorder")
        'SCALE'
        >>> bucket_for("trace.marker.opacity")
        'MARK'
        >>> bucket_for("trace.x")
        'DATA'

    Anything on the layout side that matches no rule falls to FRAME. That is
    SPEC 4.2's deliberate catch-all: a gap should show up as a knob in the
    wrong drawer, which somebody notices, rather than vanishing.
    """
    prefix, _, rest = path.partition(".")
    head = rest.partition(".")[0]

    if prefix == "trace":
        # Trace-side: the named data channels are DATA, everything else is MARK.
        return "DATA" if head in DATA_NAMES else "MARK"

    if prefix != "layout":
        raise ValueError(
            f"knob paths must start with 'trace.' or 'layout.', got {path!r}")

    for pattern, bucket in _LAYOUT_RULES:
        if pattern.endswith("*"):
            if head.startswith(pattern[:-1]):
                return bucket
        elif pattern.startswith("*"):
            if head.endswith(pattern[1:]):
                return bucket
        elif head == pattern:
            return bucket
    return "FRAME"


def _emit_bucket(path: str) -> str:
    """Which SECTION of the generated code does this path get written into?

    Same answer as `bucket_for`, with one adjustment: a DATA-classified path
    sitting in `knobs` still has to be written somewhere, and it is trace-side,
    so it goes out with MARK through `update_traces`. In normal use this never
    fires - data channels live in `mapping`, not `knobs` - but a knob that
    quietly disappeared would break the round trip, and nothing here is
    allowed to quietly disappear.
    """
    bucket = bucket_for(path)
    return "MARK" if bucket == "DATA" else bucket


# =====================================================================
# PATHS <-> KEYWORDS
# ---------------------------------------------------------------------
# "layout.xaxis.categoryorder"  <->  "xaxis_categoryorder"
# =====================================================================


def _flatten(path: str) -> str:
    """Drop the trace./layout. prefix and join what's left with underscores."""
    return "_".join(path.split(".")[1:])


def _segments(keyword: str) -> list[str]:
    """Split a magic-underscore keyword back into its property names.

    Greedy, longest match first, using UNDERSCORE_NAMES. Because none of the
    seven underscore-carrying names starts with a word that is itself a
    property name, greedy is not a heuristic here - it is the only possible
    answer.

        _segments("xaxis_categoryorder") -> ["xaxis", "categoryorder"]
        _segments("paper_bgcolor")       -> ["paper_bgcolor"]
        _segments("error_y_visible")     -> ["error_y", "visible"]
    """
    words = keyword.split("_")
    out: list[str] = []
    i = 0
    while i < len(words):
        take = 1
        # Longest run of words starting here that is a known single name.
        for j in range(len(words), i + 1, -1):
            if "_".join(words[i:j]) in UNDERSCORE_NAMES:
                take = j - i
                break
        out.append("_".join(words[i:i + take]))
        i += take
    return out


def _unflatten(prefix: str, keyword: str) -> str:
    """The inverse of _flatten. `prefix` is "trace" or "layout"."""
    return ".".join([prefix, *_segments(keyword)])


def _real_path(prefix: str, keyword: str) -> str:
    """`_unflatten`, but it refuses to invent a knob that cannot exist.

    Every segment of a knob path is a Plotly property name, so every segment
    has to be a real identifier. Three keywords a human can type break that,
    and all three used to sail straight into SPEC["knobs"]:

        fig.update_layout(_=1)       -> "layout.."       (two empty segments)
        fig.update_layout(title_=1)  -> "layout.title."  (a trailing empty one)
        fig.update_layout(_title=1)  -> "layout..title"

    The first of those then took the whole app down: `render` refuses to write
    a path it cannot read back, so the next repaint raised out of the callback
    that draws the figure, the code box, the knob pane AND the picker, and the
    screen froze with the error only in the server log.

    A keyword that does not name a knob is not the canonical form, so it goes
    to CUSTOM mode - which is exactly what SPEC section 1 says CUSTOM is for.
    """
    parts = _segments(keyword)
    if not parts or not all(p.isidentifier() for p in parts):
        raise _NotCanonical(f"{keyword!r} does not name a knob")
    return ".".join([prefix, *parts])


# =====================================================================
# WRITING VALUES
# ---------------------------------------------------------------------
# Only the JSON types, because SPEC 3 says the state object has to survive a
# dcc.Store. Anything else is a bug upstream and gets a loud error, not a
# quiet coercion.
# =====================================================================


def _pystr(text: str) -> str:
    """A double-quoted Python string literal that reads back as this string.

    Written by hand rather than with repr() so the quote style is always the
    same one, which keeps the output stable enough to diff.
    """
    out = ['"']
    for ch in text:
        code = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif code < 0x20 or code == 0x7F:
            out.append(f"\\x{code:02x}")
        elif 0xD800 <= code <= 0xDFFF:
            # A lone surrogate. Legal in a Python str, not writable as raw
            # UTF-8, so spell it out as an escape and it still reads back.
            out.append(f"\\u{code:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _literal(value: Any, where: str, depth: int = 0) -> str:
    """One SPEC value, written as a Python literal.

    `where` only ever appears in error messages - it says which knob or
    mapping slot the bad value came from, so you are not left hunting.
    """
    if depth > MAX_DEPTH:
        raise ValueError(f"{where}: value nests more than {MAX_DEPTH} deep")

    if value is None:
        return "None"
    if isinstance(value, bool):          # before int - a bool IS an int
        return "True" if value else "False"
    if isinstance(value, int):
        return repr(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(
                f"{where}: {value!r} cannot be written as a literal "
                "(inf and nan are not JSON either)")
        return repr(value)
    if isinstance(value, str):
        return _pystr(value)
    if isinstance(value, list):
        return "[" + ", ".join(
            _literal(v, where, depth + 1) for v in value) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise TypeError(f"{where}: dict keys must be strings, got {key!r}")
        return "{" + ", ".join(
            f"{_pystr(k)}: {_literal(value[k], where, depth + 1)}"
            for k in sorted(value)) + "}"
    raise TypeError(
        f"{where}: {type(value).__name__} is not a JSON value "
        "(allowed: str, int, float, bool, None, list, dict)")


def _call(head: str, parts: list[str], close: str = ")") -> str:
    """One call, on one line if it fits, otherwise one argument per line.

    `head.rstrip()` matters: the chart line's head ends "px.bar(df, " so the
    single-line form reads right, and stripping that space keeps the wrapped
    form free of trailing whitespace.
    """
    single = head + ", ".join(parts) + close
    if len(single) <= WRAP_AT or not parts:
        return single
    body = "".join(f"    {p},\n" for p in parts)
    return f"{head.rstrip()}\n{body}{close}"


def _header(label: str) -> str:
    """`# --- MARK -----------------------------------------------------`"""
    start = f"# --- {label} "
    return start + "-" * max(3, HEADER_WIDTH - len(start))


# =====================================================================
# RENDER
# =====================================================================


def render(spec: dict, *, px_charts: Iterable[str] | None = None) -> str:
    """Write a SPEC dict out as canonical Python.

    `px_charts` overrides which chart keys print as `px.<name>(df, ...)`
    instead of `bench.registry.build(<name>, df, ...)`, for one call only -
    with no read of or write to the module-level PX_CHARTS. app.py's
    render_code() uses this instead of mutating the shared set under a lock,
    since a parameter can't leak between callers the way shared state can.

    Deterministic: the same spec always produces the same characters. That is
    the whole basis of the two-way sync - if rendering wobbled, the code panel
    would fight the person typing in it.

        >>> print(render({
        ...     "chart": "bar",
        ...     "source": {"kind": "demo", "name": "entity_count"},
        ...     "mapping": {"x": "STATE", "y": "TOTAL"},
        ...     "knobs": {"layout.barmode": "group"},
        ...     "custom_code": None,
        ... }))                                       # doctest: +ELLIPSIS
        # --- data ...

    If `spec["custom_code"]` holds a string, the app is in CUSTOM mode and
    that string IS the code panel, so it comes back untouched. Round-tripping
    a CUSTOM spec is not promised and cannot be: custom code is by definition
    the code that did not parse.

    Raises ValueError / TypeError on a spec that could never be valid - a knob
    path with no trace./layout. prefix, a value that is not JSON, a float that
    is inf. Those are bugs in the caller, and a loud one is cheaper to fix
    than a silently dropped knob.
    """
    custom = spec.get("custom_code")
    if isinstance(custom, str):
        return custom

    chunks: list[str] = []

    # --- data ---------------------------------------------------------
    source = spec.get("source") or {}
    if not isinstance(source, dict):
        raise TypeError(f"spec['source'] must be a dict, got {type(source).__name__}")
    pairs = [f"{_pystr(k)}: {_literal(source[k], f'source[{k!r}]')}"
             for k in sorted(source)]
    chunks.append(_header("data") + "\n"
                  + _call(f"df = {SOURCE_CALL}({{", pairs, "})"))

    # --- chart --------------------------------------------------------
    chart = spec.get("chart")
    if not isinstance(chart, str) or not chart:
        raise ValueError(f"spec['chart'] must be a non-empty string, got {chart!r}")
    mapping = spec.get("mapping") or {}
    if not isinstance(mapping, dict):
        raise TypeError(f"spec['mapping'] must be a dict, got {type(mapping).__name__}")

    args = [f"{slot}={_literal(mapping[slot], f'mapping[{slot!r}]')}"
            for slot in _ordered_mapping(mapping)]
    charts = PX_CHARTS if px_charts is None else px_charts
    if chart.isidentifier() and chart in charts:
        head = f"fig = {PX_NAMESPACE}.{chart}(df"
    else:
        head = f"fig = {REGISTRY_CALL}({_pystr(chart)}, df"
    head = head + ", " if args else head
    chunks.append(_header("chart") + "\n" + _call(head, args))

    # --- one section per bucket that has anything in it ----------------
    knobs = spec.get("knobs") or {}
    if not isinstance(knobs, dict):
        raise TypeError(f"spec['knobs'] must be a dict, got {type(knobs).__name__}")

    by_bucket: dict[str, list[str]] = {b: [] for b in BUCKET_ORDER}
    for path in sorted(knobs):
        if not isinstance(path, str):
            raise TypeError(f"knob paths must be strings, got {path!r}")
        keyword = _flatten(path)
        prefix = path.partition(".")[0]
        if not keyword or not keyword.replace("_", "").isidentifier():
            raise ValueError(f"{path!r} does not flatten to a Python keyword")
        # Prove the inverse before writing it. A path we cannot read back is
        # a path we refuse to write - a silent round-trip break is the one
        # failure this module exists to prevent.
        if _unflatten(prefix, keyword) != path:
            raise ValueError(
                f"{path!r} is not round-trip safe: it flattens to "
                f"{keyword!r}, which reads back as "
                f"{_unflatten(prefix, keyword)!r}")
        by_bucket[_emit_bucket(path)].append(
            f"{keyword}={_literal(knobs[path], f'knobs[{path!r}]')}")

    for bucket in BUCKET_ORDER:
        parts = by_bucket[bucket]
        if not parts:
            continue          # empty bucket emits NOTHING - SPEC 5, rule 1
        chunks.append(_header(bucket) + "\n"
                      + _call(f"fig.{BUCKET_CALL[bucket]}(", parts))

    return "\n\n".join(chunks) + "\n\nfig.show()\n"


def _ordered_mapping(mapping: dict) -> list[str]:
    """Mapping slots in reading order: the known channels first, then A-Z."""
    known = [s for s in MAPPING_ORDER if s in mapping]
    rest = sorted(s for s in mapping if s not in MAPPING_ORDER)
    return known + rest


# =====================================================================
# PARSE
# ---------------------------------------------------------------------
# Everything below walks the `ast`. Nothing below ever executes the source.
# =====================================================================


class _NotCanonical(Exception):
    """Internal: this source is not the canonical shape. Becomes a None."""


def parse(src: str) -> dict | None:
    """Read canonical Python back into a SPEC dict, or return None.

    None means "this is not the canonical shape" - the app's cue to enter
    CUSTOM mode. That covers a syntax error, an import, a loop, an f-string,
    a lambda, an extra call it does not know, or just an empty box.

    This function never raises. Not for malformed input, not for hostile
    input, not for the empty string, not for None. A broken edit is a return
    value.

    Comments are invisible here - `ast` throws them away - so the `# --- MARK`
    headers are for the human reading the panel, and you can rewrite or delete
    them without upsetting anything.

    Two places it is deliberately more forgiving than `render` is tidy:
      * the bucket calls may appear in any order and any number, and they get
        merged left to right (a later keyword wins);
      * a tuple is read as a list.
    Neither can affect the round trip, because `render` never emits either.
    """
    try:
        # Half-typed code makes the compiler grumble (SyntaxWarning: invalid
        # decimal literal, and friends). This runs on every keystroke, so
        # swallow the noise - the answer is the return value, not the log.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return _parse(src)
    except Exception:       # noqa: BLE001 - "never raises" is the contract
        return None


def _parse(src: str) -> dict | None:
    tree = ast.parse(src)
    body = list(tree.body)
    if len(body) < 2:
        return None

    source = _read_source_line(body[0])
    chart, mapping = _read_chart_line(body[1])

    knobs: dict[str, Any] = {}
    seen_show = False
    for node in body[2:]:
        if seen_show:
            return None                      # nothing may follow fig.show()
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            return None
        call = node.value
        func = call.func
        if not (isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "fig"):
            return None

        if func.attr == "show":
            if call.args or call.keywords:
                return None
            seen_show = True
            continue

        if func.attr not in ("update_traces", "update_layout"):
            return None
        if call.args:
            return None                      # canonical form is keywords only
        prefix = "trace" if func.attr == "update_traces" else "layout"
        for kw in call.keywords:
            if kw.arg is None:               # **something
                return None
            knobs[_real_path(prefix, kw.arg)] = _read_value(kw.value)

    return {
        "chart": chart,
        "source": source,
        "mapping": mapping,
        "knobs": knobs,
        "custom_code": None,
    }


def _read_source_line(node: ast.stmt) -> dict:
    """`df = bench.data.frame({...})` -> the source dict."""
    if not (isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "df"
            and isinstance(node.value, ast.Call)):
        raise _NotCanonical("first statement is not `df = ...`")
    call = node.value
    if _dotted(call.func) != SOURCE_CALL:
        raise _NotCanonical(f"first statement does not call {SOURCE_CALL}")
    if len(call.args) != 1 or call.keywords:
        raise _NotCanonical(f"{SOURCE_CALL} takes exactly one dict")
    value = _read_value(call.args[0])
    if not isinstance(value, dict):
        raise _NotCanonical(f"{SOURCE_CALL} was not handed a dict")
    return value


def _read_chart_line(node: ast.stmt) -> tuple[str, dict]:
    """`fig = px.bar(df, x="A")` -> ("bar", {"x": "A"}).

    Also accepts the registry form, which is what charts with no Plotly
    Express front door get: `fig = bench.registry.build("sankey", df, ...)`.
    """
    if not (isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "fig"
            and isinstance(node.value, ast.Call)):
        raise _NotCanonical("second statement is not `fig = ...`")
    call = node.value
    name = _dotted(call.func)
    if name is None or "." not in name:
        raise _NotCanonical("the chart call is not a dotted name")

    if name == REGISTRY_CALL:
        if len(call.args) != 2:
            raise _NotCanonical(f"{REGISTRY_CALL} takes a key and df")
        key = call.args[0]
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            raise _NotCanonical("the registry key is not a string literal")
        chart = key.value
        df_arg = call.args[1]
    else:
        if len(call.args) != 1:
            raise _NotCanonical("the chart call takes df and then keywords")
        chart = name.rsplit(".", 1)[-1]
        df_arg = call.args[0]

    if not (isinstance(df_arg, ast.Name) and df_arg.id == "df"):
        raise _NotCanonical("the chart call was not handed df")
    if not chart:
        raise _NotCanonical("empty chart key")

    mapping: dict[str, Any] = {}
    for kw in call.keywords:
        if kw.arg is None:
            raise _NotCanonical("**kwargs on the chart call")
        mapping[kw.arg] = _read_value(kw.value)
    return chart, mapping


def _dotted(node: ast.expr) -> str | None:
    """`px.bar` -> "px.bar". Anything that is not a plain dotted name -> None."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return None
    parts.append(node.id)
    return ".".join(reversed(parts))


def _read_value(node: ast.expr, depth: int = 0) -> Any:
    """One literal out of the tree, as the Python object it stands for.

    Deliberately narrower than `ast.literal_eval`: no complex numbers, no
    bytes, no Ellipsis, no arithmetic. Only the JSON types, because those are
    the only ones a SPEC is allowed to hold.

    "The JSON types" includes the small print: `inf` and `nan` are NOT JSON,
    and `_literal` refuses to write either. So `parse` must refuse to read
    either, or the two stop being mirrors - and `fig.update_layout(width=1e400)`
    is six characters that used to put an `inf` in the SPEC and then raise out
    of the repaint callback, taking the whole screen with it.
    """
    if depth > MAX_DEPTH:
        raise _NotCanonical("value nests too deep")

    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, float) and not math.isfinite(value):
            raise _NotCanonical(f"{value!r} is not a JSON number")
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        raise _NotCanonical(f"{type(value).__name__} is not a SPEC value")

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        inner = _read_value(node.operand, depth + 1)
        if isinstance(inner, bool) or not isinstance(inner, (int, float)):
            raise _NotCanonical("sign applied to something that is not a number")
        return -inner if isinstance(node.op, ast.USub) else inner

    if isinstance(node, (ast.List, ast.Tuple)):
        return [_read_value(el, depth + 1) for el in node.elts]

    if isinstance(node, ast.Dict):
        out: dict[str, Any] = {}
        for key, val in zip(node.keys, node.values):
            if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                raise _NotCanonical("dict keys must be string literals")
            out[key.value] = _read_value(val, depth + 1)
        return out

    raise _NotCanonical(f"{type(node).__name__} is not a literal")


# =====================================================================
# SELF TEST
# ---------------------------------------------------------------------
# `python bench/codegen.py` runs a quick smoke test. The full battery -
# 30-plus specs and a pile of hostile input - is in
# tests/test_bench_codegen.py.
# =====================================================================


def _smoke() -> int:
    spec = {
        "chart": "bar",
        "source": {"kind": "demo", "name": "entity_count"},
        "mapping": {"x": "STATE", "y": "TOTAL", "color": None},
        "knobs": {
            "layout.barmode": "group",
            "layout.template": "plotly_dark",
            "layout.xaxis.categoryorder": "total descending",
            "trace.marker.opacity": 0.8,
        },
        "custom_code": None,
    }
    code = render(spec)
    print(code)
    back = parse(code)
    ok = back == spec
    print("round trip:", "OK" if ok else "FAILED")
    if not ok:
        print("  wanted:", spec)
        print("  got   :", back)
    hostile = ["", "import os", "for i in x: pass", "def f(): pass", "1 +",
               "lambda: 1", "(x := 1)", 'f"{x}"', "df = evil()"]
    bad = [h for h in hostile if parse(h) is not None]
    print("hostile input all rejected:", "OK" if not bad else f"FAILED {bad}")
    return 0 if ok and not bad else 1


if __name__ == "__main__":
    raise SystemExit(_smoke())
