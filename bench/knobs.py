#!/usr/bin/env python
"""
KNOBS - turn Plotly's own validators into a tiered panel of controls.

Nobody hand-writes 2,488 controls. Plotly already describes every setting it
has, in machine-readable form, and this module reads that description and
hands back a tree the UI can render.

WHAT IT DOES, IN ONE BREATH
---------------------------
Give it a chart key and the column names in your dataframe. It walks the
chart's trace object and `go.Layout`, asks Plotly what each property accepts,
picks the right control for it, files it in one of the six ATLAS buckets, and
sorts it into three tiers so the twenty settings you actually use sit on top.

    from bench import knobs
    t = knobs.tree("bar", ["STATE", "TOTAL"])
    t["FRAME"][0]          # -> the Tier 0 FRAME knobs, ATLAS order

THE THREE WORDS YOU NEED
------------------------
    validator   Plotly's own gatekeeper object for one property. It knows the
                legal values, the min and the max. `go.Bar()._get_validator("orientation")`
                hands you one; its class name tells you what control to draw.
    bucket      Which of the six ATLAS families a setting belongs to -
                DATA, MARK, SCALE, FRAME, INTERACTION, MOTION.
    tier        How buried it is. Tier 0 = the twenty you touch constantly.
                Tier 1 = shallow. Tier 2 = deep. See SPEC section 4.3.

WHAT THIS MODULE MUST NOT DO
----------------------------
No dash. No snowflake. No network. It is pure introspection over the plotly
package that is installed on this machine, and it is safe to import from a
test with nothing else running.

TWO HONEST LIMITS, STATED UP FRONT
----------------------------------
1. **Plotly's real defaults are not in Python.** They live in plotly.js. A
   freshly built `go.Bar()` reports `None` for nearly every property, so
   `default()` returns `None` almost always. That is not a bug in this module -
   it is why SPEC section 3 says the state object stores only the knobs you
   actually changed. "At default" means "absent from SPEC['knobs']".
2. **The walk stops at depth 4.** Some Plotly objects nest deeper than that
   (and `layout.template` nests forever). Everything cut is recorded, not
   silently dropped - see `cut_at_depth()`.
"""

from __future__ import annotations

import ast
import fnmatch
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import plotly.colors as pcolors
import plotly.graph_objects as go
import plotly.io as pio

log = logging.getLogger(__name__)


# =====================================================================
# THE SIX BUCKETS
# ---------------------------------------------------------------------
# ATLAS section 1.1. Fixed order - the UI renders them top to bottom in
# this order and codegen writes its sections in this order too.
# =====================================================================

DATA = "DATA"
MARK = "MARK"
SCALE = "SCALE"
FRAME = "FRAME"
INTERACTION = "INTERACTION"
MOTION = "MOTION"

BUCKETS: tuple[str, ...] = (DATA, MARK, SCALE, FRAME, INTERACTION, MOTION)

TIERS: tuple[int, ...] = (0, 1, 2)

# How many segments deep the walk goes past the `layout.` / `trace.` prefix.
# `layout.xaxis.title.font.size` is depth 4 and is the deepest thing we keep.
MAX_DEPTH = 4


# =====================================================================
# VALIDATOR -> CONTROL
# ---------------------------------------------------------------------
# SPEC section 4.1. The class name of the validator is the whole decision.
# Every class name below was read off this install by walking all 49
# registered trace types plus go.Layout - there are no guesses here.
# =====================================================================

# Three validator classes are noise and never become a control.
#   SrcValidator       - the `*src` twins. ATLAS 5.3: 18% of the library,
#                        only meaningful inside Chart Studio's grid.
#   LiteralValidator   - read-only, e.g. `type` on a trace. You cannot set it.
#   SubplotidValidator - which axis a trace binds to. Subplots are out of
#                        scope for v1 (SPEC section 9), not a knob.
SKIP_VALIDATORS: frozenset[str] = frozenset(
    {"SrcValidator", "LiteralValidator", "SubplotidValidator"}
)

# Validators that want a LIST and get handed a string, because controls.py has
# no list widget and draws them as a text box. `validate` reads the string as a
# list before it goes near Plotly - see `_read_list` for why four of ATLAS's
# twenty were unusable without this.
#
# DataArrayValidator is deliberately NOT here: it is the mapping bucket, where
# the value is a column NAME and reading "a,b" as a list would be wrong.
LIST_VALIDATORS: frozenset[str] = frozenset(
    {"InfoArrayValidator", "ColorlistValidator", "ColorscaleValidator",
     "CompoundArrayValidator"}
)

# Validators that hold a child object we walk into.
RECURSE_VALIDATORS: frozenset[str] = frozenset({"CompoundValidator", "TitleValidator"})

# Validators that hold children we deliberately do NOT walk into.
#   CompoundArrayValidator - a LIST of objects (annotations, shapes, sliders).
#                            A list needs an add/remove repeater, not a tree.
#   BaseTemplateValidator  - `layout.template` contains a whole Layout and a
#                            whole set of traces. Walking it never ends.
NO_RECURSE_VALIDATORS: frozenset[str] = frozenset(
    {"CompoundArrayValidator", "BaseTemplateValidator"}
)

# The control the UI should draw. `controls.py` maps these names to Dash
# components; this module never imports Dash and never builds a component.
CONTROL_BY_VALIDATOR: dict[str, str] = {
    # --- SPEC section 4.1, verbatim -----------------------------------
    "EnumeratedValidator": "dropdown",
    "BooleanValidator": "toggle",
    "ColorValidator": "color",  # colour picker AND a hex box, always
    "NumberValidator": "number",  # upgraded to "slider" when min and max are real
    "IntegerValidator": "integer",
    "StringValidator": "text",  # upgraded to "dropdown" when it carries values
    "AngleValidator": "angle",
    "FlaglistValidator": "multiselect",
    "CompoundValidator": "section",  # expandable sub-section, we recurse in
    "DataArrayValidator": "column",  # dropdown of the current df's columns
    "AnyValidator": "text",  # last resort
    # --- classes the spec table does not name, but this install has ----
    # Found by walking every trace type and layout. Each one is real.
    "TitleValidator": "section",  # a Title object; behaves like a compound
    "CompoundArrayValidator": "list",  # annotations, shapes, sliders, buttons
    "BaseTemplateValidator": "dropdown",  # options are the registered templates
    "ColorscaleValidator": "colorscale",  # 94 named ramps on this install
    "ColorlistValidator": "colorlist",  # an ordered list of colours (colorway)
    "DashValidator": "dropdown",  # solid/dot/dash/... plus a regex we drop
    "InfoArrayValidator": "list",  # a fixed-length list, e.g. range=[0, 100]
    "ImageUriValidator": "text",  # a URL or a data: URI
}


# =====================================================================
# BUCKET ASSIGNMENT
# ---------------------------------------------------------------------
# SPEC section 4.2. Table-driven, first match wins, evaluated top to
# bottom. Patterns are fnmatch globs anchored to the whole dotted path,
# so `layout.click*` catches `layout.clickmode` but never
# `layout.legend.groupclick`.
#
# The one rule that is not a pattern sits between rows 2 and 3: any
# DataArrayValidator that has not already matched is DATA. That is what
# puts sankey's `trace.link.source` in the mapping bucket where it
# belongs, while `trace.marker.colors` stays in MARK because the explicit
# MARK pattern above it already claimed it.
# =====================================================================

BUCKET_RULES: tuple[tuple[str, str], ...] = (
    # 1. The named data channels. Exact paths - `trace.text` is DATA but
    #    `trace.textposition` is MARK, so these must be matched exactly.
    (DATA, "trace.x"),
    (DATA, "trace.y"),
    (DATA, "trace.z"),
    (DATA, "trace.color"),
    (DATA, "trace.values"),
    (DATA, "trace.labels"),
    (DATA, "trace.parents"),
    (DATA, "trace.text"),
    # 2. What the drawn thing looks like.
    (MARK, "trace.marker"),
    (MARK, "trace.marker.*"),
    (MARK, "trace.line"),
    (MARK, "trace.line.*"),
    (MARK, "trace.fill*"),
    (MARK, "trace.opacity"),
    (MARK, "trace.textposition"),
    (MARK, "trace.orientation"),
    # 3. (the DataArrayValidator -> DATA rule fires here, in code)
    # 4. Everything else trace-side is MARK.
    (MARK, "trace.*"),
    # 5. How numbers and categories become position and colour.
    (SCALE, "layout.xaxis"),
    (SCALE, "layout.xaxis.*"),
    (SCALE, "layout.yaxis"),
    (SCALE, "layout.yaxis.*"),
    (SCALE, "layout.coloraxis*"),
    (SCALE, "layout.colorscale"),
    (SCALE, "layout.colorscale.*"),
    (SCALE, "layout.*colorway"),
    (SCALE, "layout.polar*"),
    (SCALE, "layout.geo*"),
    (SCALE, "layout.scene*"),
    (SCALE, "layout.ternary*"),
    (SCALE, "layout.map*"),
    (SCALE, "layout.smith*"),
    # 6. What happens when a human touches it.
    (INTERACTION, "layout.hover*"),
    (INTERACTION, "layout.click*"),
    (INTERACTION, "layout.drag*"),
    (INTERACTION, "layout.select*"),
    (INTERACTION, "layout.modebar*"),
    (INTERACTION, "layout.updatemenu*"),
    (INTERACTION, "layout.slider*"),
    (INTERACTION, "layout.spikedistance"),
    (INTERACTION, "layout.newshape*"),
    # 7. Animation.
    (MOTION, "layout.transition*"),
    # 8. Everything around and behind the data.
    (FRAME, "layout.title*"),
    (FRAME, "layout.legend*"),
    (FRAME, "layout.margin*"),
    (FRAME, "layout.font*"),
    (FRAME, "layout.annotation*"),
    (FRAME, "layout.shape*"),
    (FRAME, "layout.image*"),
    (FRAME, "layout.paper_bgcolor"),
    (FRAME, "layout.plot_bgcolor"),
    (FRAME, "layout.width"),
    (FRAME, "layout.height"),
    (FRAME, "layout.template*"),
    (FRAME, "layout.showlegend"),
    (FRAME, "layout.grid*"),
    (FRAME, "layout.uniformtext*"),
)

# Anything that matched nothing lands in FRAME and its path is remembered
# here, so a gap in the table above surfaces instead of being swallowed.
_UNMATCHED: set[str] = set()

# Anything the depth cap cut off. Same idea: recorded, not silently lost.
_CUT_DEPTH: set[str] = set()

# Anything the loop guard stopped. Measured on this install: empty, because
# the only two loop-makers in Plotly (`layout.template`, which contains a
# whole Layout, and the compound arrays) are already excluded from the walk.
# The guard stays as belt-and-braces, not because it fires today.
_CUT_CYCLE: set[str] = set()


# =====================================================================
# TIER 0 - THE TWENTY
# ---------------------------------------------------------------------
# ATLAS section 4.1. The half-sentences below are lifted straight out of
# that table; the only edit is stripping markdown backticks and asterisks
# so they read cleanly in a tooltip. No wording was changed and nothing
# was written fresh.
#
# The key is the rank in the ATLAS table, which is also the order Tier 0
# renders in. Several ATLAS rows name more than one property; each one
# gets its own entry with the same sentence, because that is what the
# ATLAS row says about it.
# =====================================================================

TIER0: dict[str, tuple[int, str]] = {
    "layout.title.text": (
        1,
        "Says what the reader is looking at, before they read a single axis.",
    ),
    "layout.xaxis.title.text": (
        2,
        '"Which is biggest?" is unanswerable if you never said biggest what.',
    ),
    "layout.yaxis.title.text": (
        2,
        '"Which is biggest?" is unanswerable if you never said biggest what.',
    ),
    "layout.xaxis.categoryorder": (
        3,
        "Sorts a category axis — 18 values, and 'total descending' turns an "
        "alphabetical bar chart into an actual answer.",
    ),
    "layout.barmode": (
        4,
        "'group' to compare side by side, 'stack' to add up, 'relative' when there "
        "are negatives, 'overlay' for two histograms.",
    ),
    "layout.yaxis.tickformat": (
        5,
        "A d3 format string; stops 1.2e+06 appearing on a chart a human has to read.",
    ),
    "layout.yaxis.range": (
        6,
        "Forces the window — the only way two charts side by side are honestly "
        "comparable.",
    ),
    "layout.xaxis.type": (
        7,
        "'log' when values span orders of magnitude; 'date' / 'category' when Plotly "
        "guessed wrong. Six values.",
    ),
    "layout.hovermode": (
        8,
        "'x unified' gives one tooltip listing every series at that x. The single "
        "biggest usability win in Plotly, and it is off by default.",
    ),
    "layout.showlegend": (
        9,
        "One series → off, it's noise. Twelve → on.",
    ),
    "layout.legend.orientation": (
        10,
        "'h' across the top of a wide chart hands ~15% of the width back to the data.",
    ),
    "layout.legend.x": (
        11,
        "x=1.02 parks the legend outside the plot instead of on top of your data.",
    ),
    "layout.legend.y": (
        11,
        "x=1.02 parks the legend outside the plot instead of on top of your data.",
    ),
    "layout.margin.l": (
        12,
        "The fix for clipped category labels, and for a 200px KPI tile losing 40% of "
        "itself to default padding.",
    ),
    "layout.margin.r": (
        12,
        "The fix for clipped category labels, and for a 200px KPI tile losing 40% of "
        "itself to default padding.",
    ),
    "layout.margin.t": (
        12,
        "The fix for clipped category labels, and for a 200px KPI tile losing 40% of "
        "itself to default padding.",
    ),
    "layout.margin.b": (
        12,
        "The fix for clipped category labels, and for a 200px KPI tile losing 40% of "
        "itself to default padding.",
    ),
    "layout.width": (
        13,
        'Both default to None, which means "fill the container" — only set them '
        "when exporting at a fixed size.",
    ),
    "layout.height": (
        13,
        'Both default to None, which means "fill the container" — only set them '
        "when exporting at a fixed size.",
    ),
    "layout.template": (
        14,
        "First line of any styling work; 11 built-ins, 'plotly_white' or "
        "'simple_white' instantly stops a chart looking like a demo.",
    ),
    "layout.paper_bgcolor": (
        15,
        "Two backgrounds and everyone forgets there are two: paper is the whole "
        "image, plot is just the data rectangle.",
    ),
    "layout.plot_bgcolor": (
        15,
        "Two backgrounds and everyone forgets there are two: paper is the whole "
        "image, plot is just the data rectangle.",
    ),
    "layout.font.family": (
        16,
        "One place to set the typeface, instead of the 37 separate font objects "
        "underneath.",
    ),
    "layout.font.size": (
        16,
        "One place to set the typeface, instead of the 37 separate font objects "
        "underneath.",
    ),
    "layout.font.color": (
        16,
        "One place to set the typeface, instead of the 37 separate font objects "
        "underneath.",
    ),
    "layout.colorway": (
        17,
        "The ordered list of colours handed to series one by one — where your "
        "brand palette goes.",
    ),
    "layout.yaxis.showgrid": (
        18,
        "Grid on and faint when reading exact values matters; off when the shape is "
        "the point.",
    ),
    "layout.yaxis.gridcolor": (
        18,
        "Grid on and faint when reading exact values matters; off when the shape is "
        "the point.",
    ),
    "layout.annotations": (
        19,
        '"This spike is the March outage." A labelled chart needs no caption. The '
        "most under-used property in Plotly.",
    ),
    "layout.shapes": (
        20,
        "Target lines, thresholds, shaded bands — add_hline / add_vrect are the "
        "easy front doors.",
    ),
}


# =====================================================================
# THE KNOB
# =====================================================================


@dataclass(frozen=True)
class Knob:
    """One row in the knob panel: one Plotly setting, ready to render.

    Fields are exactly the ones SPEC section 4.5 names, plus three the UI
    needs to file the row (`bucket`, `tier`) and to debug it (`validator`).

    path        dotted, always starting `layout.` or `trace.` - the key used
                in SPEC["knobs"]
    label       the path with that prefix stripped, e.g. "xaxis.categoryorder"
    control     which widget to draw; see CONTROL_BY_VALIDATOR
    options     legal values for a dropdown/multiselect, or the dataframe's
                column names when control == "column". None when free-form.
    min / max   the numeric bounds Plotly enforces, when it enforces any
    default     what a freshly built Plotly object reports. Almost always
                None - see the module docstring.
    description a half-sentence. ATLAS wording for Tier 0, a cleaned-up
                version of Plotly's own for everything else.
    depth       how many segments past the prefix, so 1 = top level
    bucket      one of BUCKETS
    tier        0, 1 or 2
    validator   the Plotly validator class name this came from
    """

    path: str
    label: str
    control: str
    options: tuple[Any, ...] | None
    min: float | None
    max: float | None
    default: Any
    description: str
    depth: int
    bucket: str
    tier: int
    validator: str

    def as_dict(self) -> dict[str, Any]:
        """A plain dict, safe to hand to Dash or json.dumps."""
        return {
            "path": self.path,
            "label": self.label,
            "control": self.control,
            "options": list(self.options) if self.options is not None else None,
            "min": self.min,
            "max": self.max,
            "default": self.default,
            "description": self.description,
            "depth": self.depth,
            "bucket": self.bucket,
            "tier": self.tier,
            "validator": self.validator,
        }


# =====================================================================
# TRACE TYPE LOOKUP
# ---------------------------------------------------------------------
# `tree()` takes a registry key, e.g. "bump_chart". registry.py owns the
# mapping from key to trace type. This module asks it if it is there and
# falls back to treating the key as a trace type name, so knobs.py is
# testable on its own before registry.py exists.
# =====================================================================

# The 49 names Plotly registers, read off the install, mapped to class names.
TRACE_CLASS_NAMES: dict[str, str] = dict(go.Figure()._data_validator.class_strs_map)

# The three deprecated mapbox traces. ATLAS section 3.1: prop-for-prop twins
# of the current ones. Anything asking for a mapbox trace gets the live one.
DEPRECATED_TRACES: dict[str, str] = {
    "scattermapbox": "scattermap",
    "densitymapbox": "densitymap",
    "choroplethmapbox": "choroplethmap",
}


def trace_type_for(chart_key: str) -> str:
    """Which go.<Trace> to introspect for a registry key.

    Tries `registry.py` first (it owns the 144 templates and their
    `trace_type` field). Falls back to reading the key as a trace type
    name, which is what makes `tree("sankey", [...])` work with no
    registry present.

    Raises ValueError with the full legal list if the key is neither.
    """
    key = (chart_key or "").strip()

    # Ask the registry, if it is importable. Wrapped because registry.py
    # may not exist yet, and because it must never be a hard dependency.
    try:
        from bench import registry  # noqa: PLC0415  (deliberately lazy)
    except Exception:
        registry = None
    if registry is not None:
        getter = getattr(registry, "trace_type", None)
        if callable(getter):
            try:
                found = getter(key)
            except Exception:
                found = None
            if found:
                return DEPRECATED_TRACES.get(found, found)

    if key in DEPRECATED_TRACES:
        return DEPRECATED_TRACES[key]
    if key in TRACE_CLASS_NAMES:
        return key

    raise ValueError(
        f"knobs: don't know which trace type {chart_key!r} draws. "
        f"Either registry.trace_type() has to answer for it, or the key has "
        f"to be one of: {', '.join(sorted(TRACE_CLASS_NAMES))}"
    )


def _trace_object(trace_type: str) -> go.BaseTraceType:
    """A blank instance of the trace, which is what carries the validators."""
    return getattr(go, TRACE_CLASS_NAMES[trace_type])()


# =====================================================================
# READING ONE VALIDATOR
# =====================================================================

_DESC_PREFIX = re.compile(r"^The '[^']+' property ")
_DESC_CAP = 160


def clean_description(raw: str | None) -> str:
    """Plotly's own description, with the boilerplate lopped off.

    Plotly writes every description the same way:

        "The 'hovermode' property is an enumeration that may be specified
         as: - One of the following enumeration values: ['x', 'y', ...]"

    The first six words are the same on all 2,488 of them, so they carry no
    information. This collapses the whitespace, drops that prefix, and caps
    the result at about 160 characters on a word boundary.

    Nothing is ever invented. If there is no usable text, this returns "" and
    the UI shows the path alone (SPEC section 4.4, rule 3).
    """
    if not raw:
        return ""
    text = " ".join(str(raw).split())
    text = _DESC_PREFIX.sub("", text)
    text = text.strip()
    if not text:
        return ""
    if len(text) <= _DESC_CAP:
        return text
    cut = text[:_DESC_CAP]
    space = cut.rfind(" ")
    if space > 60:
        cut = cut[:space]
    return cut.rstrip(" ,;:-") + "..."


def _is_regex(value: Any) -> bool:
    """Is this `values` entry a plotly.js regex rather than a choice?

    They arrive slash-wrapped, e.g. '/^x([2-9]|[1-9][0-9]+)?( domain)?$/' on
    `xaxis.matches`. A regex is never a value you can pick - Plotly refuses it
    on the way back in - so it can never be an option.
    """
    return isinstance(value, str) and value.startswith("/") and value.endswith("/")


def _enum_options(values: Any) -> tuple[Any, ...] | None:
    """The legal values for a dropdown, with the oddities dropped.

    Plotly's `values` lists are written for plotly.js and carry three kinds
    of entry a human should never see in a dropdown:

      - integer codes and their string twins. `marker.symbol` lists
        0, '0', 'circle', 100, '100', 'circle-open', ... The names are the
        useful half.
      - regexes, e.g. the dash-length pattern on `line.dash`, which arrives
        as the string '/^\\d+(\\.\\d+)?(px|%)?.../'.
      - nothing else. Booleans stay: `hovermode` legitimately accepts False.

    If the cleaning empties the list the raw list comes back instead - an
    empty dropdown is worse than a messy one, and `geo.resolution` really does
    only accept the two integers 110 and 50.

    THE ONE THING THAT NEVER COMES BACK IS A REGEX. Measured on plotly 6.9.0:
    two paths - `layout.xaxis.matches` and `layout.yaxis.matches` - list
    nothing BUT regexes, so the rescue above used to hand them straight to the
    dropdown, and both options were refused the moment you picked one. A
    dropdown you cannot pick from is worse than no dropdown, so those return
    None and `_control_for` turns them into a text box you can type "x2" into.
    """
    if not values:
        return None
    usable = [v for v in values if not _is_regex(v)]
    if not usable:
        return None
    kept: list[Any] = []
    for v in usable:
        if isinstance(v, bool):
            kept.append(v)
            continue
        if isinstance(v, (int, float)):
            continue  # the numeric twin of a name we are already keeping
        if not isinstance(v, str):
            continue
        if v.isdigit():
            continue  # the string twin of an integer code
        kept.append(v)
    if not kept:
        return tuple(usable)
    return tuple(kept)


def _bounds(validator: Any) -> tuple[float | None, float | None]:
    """The numeric floor and ceiling, when Plotly enforces one.

    NOTE ON THE SPEC: SPEC section 4.1 calls these `.min` and `.max`. On
    plotly 6.9.0 the real attribute names are `min_val`, `max_val` and
    `has_min_max`. The spec's shorthand is stale; these are the names that
    exist, checked by reading a live validator.

    An infinite bound is returned as None, because "between 10 and infinity"
    is a number box, not a slider.
    """
    if not getattr(validator, "has_min_max", False):
        return None, None
    lo = getattr(validator, "min_val", None)
    hi = getattr(validator, "max_val", None)
    if lo is not None and lo in (float("-inf"), float("inf")):
        lo = None
    if hi is not None and hi in (float("-inf"), float("inf")):
        hi = None
    return lo, hi


def _control_for(validator: Any, cls_name: str) -> str:
    """Which widget draws this property.

    Straight table lookup from CONTROL_BY_VALIDATOR, with three upgrades:

      - a NumberValidator with both bounds real becomes a slider instead of
        a number box (SPEC section 4.1)
      - a StringValidator that carries a `values` list is really a dropdown
        wearing a string's clothes
      - an EnumeratedValidator with no PICKABLE value becomes a text box.
        `xaxis.matches` is the case: its whole `values` list is two regexes,
        and Plotly refuses a regex handed back to it. A text box takes the
        "x2" the regex was describing; a dropdown of two poison options does
        not.
    """
    control = CONTROL_BY_VALIDATOR.get(cls_name)
    if control is None:
        # An unknown validator class. Not fatal - a text box takes anything -
        # but say so, because it means this install has something the table
        # has not met.
        log.warning("knobs: no control mapped for validator %s, using a text box", cls_name)
        return "text"
    if control == "number":
        lo, hi = _bounds(validator)
        if lo is not None and hi is not None:
            return "slider"
    if control == "text" and cls_name == "StringValidator":
        if _enum_options(getattr(validator, "values", None)):
            return "dropdown"
    if cls_name == "EnumeratedValidator" and not _enum_options(
            getattr(validator, "values", None)):
        return "text"
    return control


def _options_for(validator: Any, cls_name: str, control: str) -> tuple[Any, ...] | None:
    """The choice list for a dropdown or multi-select, if there is one."""
    if cls_name == "FlaglistValidator":
        flags = list(getattr(validator, "flags", None) or [])
        extras = list(getattr(validator, "extras", None) or [])
        return tuple(flags + extras) or None
    if cls_name == "BaseTemplateValidator":
        # The templates actually registered in this process, not a guess.
        return tuple(sorted(str(t) for t in pio.templates))
    if cls_name == "ColorscaleValidator":
        return tuple(pcolors.named_colorscales())
    if control in ("dropdown", "multiselect"):
        return _enum_options(getattr(validator, "values", None))
    return None


# =====================================================================
# BUCKETING
# =====================================================================


def bucket_for(path: str, validator_class: str) -> str:
    """Which of the six buckets a knob path belongs to.

    Walks BUCKET_RULES top to bottom, first match wins, with the one
    in-code rule described above the table: an unclaimed DataArrayValidator
    is DATA no matter how deep it sits.

    Anything that matches nothing falls to FRAME and its path is remembered
    in `unmatched()`, so the gap gets found instead of swallowed.
    """
    for bucket, pattern in BUCKET_RULES:
        # Rule 3 sits between the explicit MARK patterns and the `trace.*`
        # catch-all, so it is checked just before that catch-all is tried.
        # This is what puts sankey's `trace.link.source` and table's
        # `trace.cells.values` in DATA where they belong.
        if pattern == "trace.*" and validator_class == "DataArrayValidator":
            if path.startswith("trace."):
                return DATA
        if fnmatch.fnmatchcase(path, pattern):
            return bucket
    if path not in _UNMATCHED:
        _UNMATCHED.add(path)
        log.debug("knobs: no bucket rule for %s (%s) - filed under FRAME", path, validator_class)
    return FRAME


def unmatched() -> tuple[str, ...]:
    """Every path that fell through BUCKET_RULES into FRAME, sorted.

    Read this after building a few trees. A long list means the table in
    SPEC section 4.2 has a hole in it.
    """
    return tuple(sorted(_UNMATCHED))


def cut_at_depth() -> tuple[str, ...]:
    """Every compound object the depth cap stopped us walking into, sorted.

    These are real settings that exist and are not in the tree. If a knob
    someone wants is missing, look here first. Raising MAX_DEPTH is the fix.
    """
    return tuple(sorted(_CUT_DEPTH))


def cut_as_cycle() -> tuple[str, ...]:
    """Every compound object the loop guard refused to re-enter, sorted.

    Empty on plotly 6.9.0 - checked by walking layout to depth 12 with the
    guard instrumented. Kept because a future Plotly could add a loop and
    an infinite walk is a hang, not an error message.
    """
    return tuple(sorted(_CUT_CYCLE))


# =====================================================================
# THE WALK
# ---------------------------------------------------------------------
# Recursive, depth-capped, cycle-guarded. It produces plain dicts rather
# than Knob objects because the result is cached per trace type and the
# column-dependent bits get filled in afterwards.
# =====================================================================


@dataclass
class _Raw:
    """One property found during the walk, before columns are known."""

    path: str
    depth: int
    validator_class: str
    control: str
    options: tuple[Any, ...] | None
    min: float | None
    max: float | None
    description: str
    default: Any = None
    bucket: str = ""


def _unset_value(obj: Any, name: str) -> Any:
    """What one property reads as on a Plotly object nobody has touched.

    Almost always None, because Plotly's real defaults are in JavaScript.
    The honest exceptions are the list-valued properties - `layout.shapes`
    on a blank Layout reads as an empty tuple, not None - so those come back
    as `[]`, which is both true and JSON-safe.

    A compound container (`layout.title`, `trace.marker`) is not a value at
    all, so it reports None.
    """
    try:
        value = getattr(obj, name)
    except Exception:
        return None
    if value is None:
        return None
    if hasattr(value, "_valid_props"):
        return None  # a sub-object, not a setting
    if isinstance(value, tuple):
        return [v for v in value if not hasattr(v, "_valid_props")]
    return value


def _walk(obj: Any, prefix: str, depth: int, seen: frozenset[type], out: list[_Raw]) -> None:
    """Read every property off one Plotly object, then step into its children.

    `seen` holds the classes already open further up this path. Plotly has
    genuine loops in it - a Template holds a Layout which holds a Template -
    so a class that is already open is never re-entered.
    """
    try:
        props = sorted(obj._valid_props)
    except Exception as exc:  # pragma: no cover - would mean a broken install
        log.warning("knobs: cannot read properties of %s: %s", type(obj).__name__, exc)
        return

    for name in props:
        try:
            validator = obj._get_validator(name)
        except Exception as exc:
            log.debug("knobs: no validator for %s.%s: %s", prefix, name, exc)
            continue

        cls_name = type(validator).__name__
        if cls_name in SKIP_VALIDATORS:
            continue

        path = f"{prefix}.{name}"
        control = _control_for(validator, cls_name)
        lo, hi = _bounds(validator)
        raw = _Raw(
            path=path,
            depth=depth,
            validator_class=cls_name,
            control=control,
            options=_options_for(validator, cls_name, control),
            min=lo,
            max=hi,
            description=clean_description(
                validator.description() if hasattr(validator, "description") else None
            ),
            # Read the default off the object we already have, rather than
            # re-walking from the root. Almost always None - see the module
            # docstring - but list-valued properties honestly read as [].
            default=_unset_value(obj, name),
        )
        raw.bucket = bucket_for(path, cls_name)
        out.append(raw)

        if cls_name not in RECURSE_VALIDATORS:
            continue

        data_class = getattr(validator, "data_class", None)
        if data_class is None:
            continue
        if data_class in seen:
            _CUT_CYCLE.add(path)  # a loop; never seen on plotly 6.9.0
            continue
        if depth >= MAX_DEPTH:
            _CUT_DEPTH.add(path)  # deeper than the cap; recorded, not lost
            continue
        try:
            child = data_class()
        except Exception as exc:  # pragma: no cover
            log.debug("knobs: cannot open %s: %s", path, exc)
            continue
        _walk(child, path, depth + 1, seen | {data_class}, out)


@lru_cache(maxsize=64)
def _raw_tree(trace_type: str) -> tuple[_Raw, ...]:
    """Every knob for one trace type plus the whole shared layout, cached.

    Cached because this is roughly 2,000 properties per chart and the UI
    rebuilds the panel every time you click a different chart. The result
    does not depend on the dataframe, so caching it is free.
    """
    out: list[_Raw] = []
    trace = _trace_object(trace_type)
    _walk(trace, "trace", 1, frozenset({type(trace)}), out)
    _walk(go.Layout(), "layout", 1, frozenset({go.Layout}), out)
    return tuple(out)


# =====================================================================
# TIERING
# =====================================================================


def tier_for(path: str, bucket: str, depth: int) -> int:
    """How buried a knob is. SPEC section 4.3.

    Tier 0  the twenty ATLAS names, plus every DATA knob for this chart -
            always visible, always expanded
    Tier 1  depth 1 or 2 - behind "show more"
    Tier 2  depth 3 and below - behind "show everything"
    """
    if path in TIER0:
        return 0
    if bucket == DATA:
        return 0  # you cannot draw the chart without these
    if depth <= 2:
        return 1
    return 2


def _tier0_rank(path: str) -> int:
    """Where a Tier 0 knob sits in the ATLAS table. Non-ATLAS knobs go last."""
    entry = TIER0.get(path)
    return entry[0] if entry else 99


# =====================================================================
# PUBLIC API  (SPEC section 4.5)
# =====================================================================


def tree(chart_key: str, columns: list[str] | None = None) -> dict[str, dict[int, list[Knob]]]:
    """Every knob for one chart, filed by bucket then tier.

    Args:
        chart_key: a registry key (`"sankey"`, `"bump_chart"`) or, when
            registry.py cannot answer, a raw Plotly trace type name.
        columns: the column names in the dataframe on screen. These become
            the options on every DATA knob, which is the one bucket whose
            legal values come from the data instead of from Plotly.

    Returns:
        `{bucket: {tier: [Knob, ...]}}` - every bucket in BUCKETS is present
        and every tier in TIERS is present, so the UI can render the six
        headers without checking for holes. Lists may be empty.

    Ordering inside a list is fixed and stable: Tier 0 runs in ATLAS
    section 4.1 order, everything else runs alphabetically by path.
    """
    cols = tuple(columns or ())
    trace_type = trace_type_for(chart_key)

    out: dict[str, dict[int, list[Knob]]] = {b: {t: [] for t in TIERS} for b in BUCKETS}

    for raw in _raw_tree(trace_type):
        tier = tier_for(raw.path, raw.bucket, raw.depth)
        # DATA is the mapping bucket: its choices are your columns, not
        # anything Plotly knows. A container that somehow lands here keeps
        # its own control - you cannot bind a column to a sub-object.
        if raw.bucket == DATA and raw.control not in ("section", "list"):
            control = "column"
            options: tuple[Any, ...] | None = cols or None
        elif raw.validator_class == "BaseTemplateValidator":
            # The one option list in the whole tree that is a fact about this
            # PROCESS rather than about Plotly's schema, so it cannot be cached
            # with the rest. `_raw_tree` is memoised, and a template registered
            # after the first tree was built used to be missing from the
            # dropdown forever - reproduced: build a tree, register a template,
            # build again, and it is still not there. Anything that imports
            # Plotly can add one (importing streamlit adds "streamlit";
            # importing bench.wall adds "wall"), so it is read fresh here.
            control = raw.control
            options = tuple(sorted(str(t) for t in pio.templates))
        else:
            control = raw.control
            options = raw.options
        entry = TIER0.get(raw.path)
        description = entry[1] if entry else raw.description
        out[raw.bucket][tier].append(
            Knob(
                path=raw.path,
                label=raw.path.split(".", 1)[1],
                control=control,
                options=options,
                min=raw.min,
                max=raw.max,
                default=raw.default,
                description=description,
                depth=raw.depth,
                bucket=raw.bucket,
                tier=tier,
                validator=raw.validator_class,
            )
        )

    for bucket in BUCKETS:
        out[bucket][0].sort(key=lambda k: (_tier0_rank(k.path), k.path))
        out[bucket][1].sort(key=lambda k: k.path)
        out[bucket][2].sort(key=lambda k: k.path)
    return out


def flat(chart_key: str, columns: list[str] | None = None) -> list[Knob]:
    """The same knobs as `tree()`, as one flat list. Handy for a search box."""
    built = tree(chart_key, columns)
    return [k for b in BUCKETS for t in TIERS for k in built[b][t]]


@lru_cache(maxsize=4096)
def default(path: str, chart_key: str | None = None) -> Any:
    """What a freshly built Plotly object reports for this knob.

    Read the module docstring before you trust this: Plotly's real defaults
    live in plotly.js, not in Python, so this returns None for essentially
    every knob. That is the honest answer, and it is why SPEC section 3
    defines "at default" as "absent from SPEC['knobs']".

    It is implemented by actually reading the object rather than returning a
    hardcoded None, so that if Plotly ever does set something at construction
    time, this reports the truth.

    `chart_key` is only needed for `trace.` paths - `layout.` paths are the
    same for every chart, which is the whole point of ATLAS section 1.1.
    """
    try:
        obj, rest = _root_object(path, chart_key)
    except ValueError:
        return None
    if not rest:
        return None
    for segment in rest[:-1]:
        try:
            obj = getattr(obj, segment)
        except Exception:
            return None
        if obj is None or not hasattr(obj, "_valid_props"):
            return None
    if rest[-1] not in getattr(obj, "_valid_props", ()):
        return None
    return _unset_value(obj, rest[-1])


def validate(path: str, value: Any, chart_key: str | None = None) -> tuple[bool, Any]:
    """Run a value past Plotly's own gatekeeper for this knob.

    Returns `(True, coerced)` when Plotly accepts it, `(False, message)`
    when it does not. Never raises - a bad value from a text box is an
    answer, not an accident.

    Four conveniences on top of raw Plotly:

      - `None` or an empty string means "clear this knob", and comes back as
        `(True, None)`. That is how the UI removes a knob from SPEC["knobs"].
      - a numeric knob given the string "0.5" gets one attempt at float()
        first, because a Dash text box hands you strings and Plotly does not
        coerce them.
      - a LIST knob given the string "[0, 100]" gets one attempt at reading it
        as a list, for the same reason. See `_read_list`.
      - the answer is always a JSON value. See `_json_safe` below for the one
        knob on this install where Plotly's own answer is not.

    `chart_key` is only needed for `trace.` paths.
    """
    if _is_blank(value):
        return True, None

    try:
        validator = validator_for(path, chart_key)
    except ValueError as exc:
        return False, str(exc)
    if validator is None:
        return False, f"knobs: no such knob {path!r}"

    cls_name = type(validator).__name__
    candidate = value
    if isinstance(value, str) and cls_name in ("NumberValidator", "AngleValidator", "IntegerValidator"):
        try:
            candidate = int(value) if cls_name == "IntegerValidator" else float(value)
        except ValueError:
            candidate = value
    elif isinstance(value, str) and cls_name in LIST_VALIDATORS:
        candidate = _read_list(value)
        if _is_blank(candidate):
            # "[]" typed into a list knob means the same as an empty box.
            # This matters more than it looks: `layout.shapes` on a blank
            # Layout honestly reads as `[]`, so controls.py DISPLAYS "[]" in
            # its text box, and without this the displayed default would come
            # straight back as a setting you never chose. SPEC section 3: a
            # knob at its default is absent, not present-and-empty.
            return True, None

    try:
        coerced = validator.validate_coerce(candidate)
    except Exception as exc:
        # Plotly's error is a wall of text; the first real line is the useful bit.
        lines = [ln.strip() for ln in str(exc).splitlines() if ln.strip()]
        return False, lines[0] if lines else f"invalid value for {path}"

    # Plotly said yes - but a coerced value still has to be something SPEC
    # section 3 can hold. See `_json_safe`.
    if not _json_safe(coerced) and _json_safe(candidate):
        return True, candidate
    return True, coerced


def _is_blank(value: Any) -> bool:
    """Does this value mean "nothing set"?

    None, an empty box, and an empty list all mean the same thing to SPEC
    section 3: the knob is at its default, so it is absent from SPEC["knobs"].
    """
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, tuple)):
        return len(value) == 0
    return False


def _read_list(text: str) -> Any:
    """A text box's string, read as the list it is obviously trying to be.

    WHY THIS EXISTS. Four of ATLAS section 4.1's twenty - `yaxis.range` (#6),
    `colorway` (#17), `annotations` (#19) and `shapes` (#20) - are list-shaped
    properties that `controls.py` has no list widget for, so they render as a
    plain text box. A text box hands back a string. Plotly refuses a string for
    every one of them. Measured before this existed: there was NO value you
    could type into `layout.yaxis.range` that the panel would accept. Four of
    the twenty knobs the whole tiering exists to promote were dead.

        "[0, 100]"              -> [0, 100]
        "0, 100"               -> [0, 100]
        "red, blue"            -> ["red", "blue"]
        "#ff0000,#00ff00"      -> ["#ff0000", "#00ff00"]
        '[{"text": "spike"}]'  -> [{"text": "spike"}]
        "Viridis"              -> "Viridis"   (unchanged - a colorscale NAME)

    Anything that is not obviously a list comes back untouched, which is what
    keeps a colorscale name reaching Plotly as a name. `ast.literal_eval` and
    not `eval`: it reads literals and nothing else, so a text box can never
    become a way to run code.
    """
    stripped = text.strip()
    try:
        got = ast.literal_eval(stripped)
    except Exception:
        got = None
    if isinstance(got, (list, tuple)):
        return list(got)
    if "," not in stripped:
        return text
    out: list[Any] = []
    for part in stripped.split(","):
        part = part.strip()
        try:
            out.append(ast.literal_eval(part))
        except Exception:
            out.append(part)          # a bare colour name, say
    return out


def _json_safe(value: Any) -> bool:
    """Can this value live in SPEC["knobs"]?

    SPEC section 3 says the state object is JSON-serialisable, because it has
    to survive a `dcc.Store`, a save to disk and a diff - and because
    `codegen.render` will only write the JSON types.

    Nearly every Plotly validator hands back exactly what you gave it, or a
    plain list. One does not, and it is a knob people actually reach for:

        knobs.validate("layout.template", "plotly_dark")

    `BaseTemplateValidator` answers with the whole expanded `layout.Template`
    object - 13,670 characters of it on plotly 6.9.0, measured. Stored, that
    turns into a 14 KB code panel, and pushing it back at a figure fails
    outright ("Invalid value of type 'builtins.str'"), so the chart quietly
    keeps the template it already had.

    Swept on this install: of 1,015 legal values across every knob in the
    `bar` tree, `layout.template` is the only one that comes back as a graph
    object. When it happens `validate` keeps the value you handed in, because
    Plotly has already confirmed the name is real and
    `fig.update_layout(template="plotly_dark")` is both what works and what
    the code panel should be printing.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return True
    if isinstance(value, (list, tuple)):
        return all(_json_safe(v) for v in value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and _json_safe(v) for k, v in value.items())
    return False


def validator_for(path: str, chart_key: str | None = None) -> Any:
    """The live Plotly validator object behind a dotted knob path.

    Exposed because `codegen.py` and the tests both want to ask Plotly
    directly rather than trusting a copy of the answer.
    """
    obj, rest = _root_object(path, chart_key)
    if not rest:
        raise ValueError(f"knobs: {path!r} names no property")
    for segment in rest[:-1]:
        try:
            child_validator = obj._get_validator(segment)
        except Exception:
            return None
        data_class = getattr(child_validator, "data_class", None)
        if data_class is None:
            return None
        obj = data_class()
    try:
        return obj._get_validator(rest[-1])
    except Exception:
        return None


def _root_object(path: str, chart_key: str | None) -> tuple[Any, list[str]]:
    """Split `layout.xaxis.title.text` into (a blank Layout, [xaxis, title, text])."""
    head, _, rest = (path or "").partition(".")
    segments = [s for s in rest.split(".") if s]
    if head == "layout":
        return go.Layout(), segments
    if head == "trace":
        if chart_key is None:
            raise ValueError(
                f"knobs: {path!r} is a trace path, so it needs a chart_key - "
                "trace properties differ per chart type"
            )
        return _trace_object(trace_type_for(chart_key)), segments
    raise ValueError(f"knobs: path must start with 'layout.' or 'trace.', got {path!r}")


# =====================================================================
# SELF-TEST
# ---------------------------------------------------------------------
# `python bench/knobs.py` builds the tree for twenty-odd trace types and
# prints the real counts. No arguments, no network, no database.
# =====================================================================

# The twenty-one this module is checked against. Deliberately spread across
# all ten ATLAS questions and both extremes of size (box has 88 properties,
# indicator has 24).
SELFTEST_TRACES: tuple[str, ...] = (
    "bar", "scatter", "sankey", "sunburst", "violin", "box", "heatmap",
    "choropleth", "indicator", "treemap", "waterfall", "funnel",
    "candlestick", "parcoords", "parcats", "densitymap", "scatter3d",
    "surface", "table", "icicle", "pie",
)

DEMO_COLUMNS = ["agency", "region", "spend", "date"]


def _selftest() -> int:
    """Build every tree in SELFTEST_TRACES and print the counts. Returns exit code."""
    import sys

    # The Windows console is cp1252 and the ATLAS sentences carry em dashes.
    # Replace what it cannot draw rather than crashing the report.
    def say(text: str = "") -> None:
        sys.stdout.write(
            text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(
                sys.stdout.encoding or "utf-8", errors="replace"
            )
            + "\n"
        )

    failures: list[str] = []
    say(f"{'trace':<15} {'total':>6} " + " ".join(f"{b[:5]:>6}" for b in BUCKETS) + "   T0    T1    T2")
    say("-" * 92)

    for name in SELFTEST_TRACES:
        try:
            built = tree(name, DEMO_COLUMNS)
        except Exception as exc:
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
            say(f"{name:<15} FAILED - {type(exc).__name__}: {exc}")
            continue
        per_bucket = [sum(len(built[b][t]) for t in TIERS) for b in BUCKETS]
        per_tier = [sum(len(built[b][t]) for b in BUCKETS) for t in TIERS]
        total = sum(per_bucket)
        say(
            f"{name:<15} {total:>6} "
            + " ".join(f"{n:>6}" for n in per_bucket)
            + "  "
            + " ".join(f"{n:>5}" for n in per_tier)
        )

    say()
    bar = tree("bar", DEMO_COLUMNS)
    say("Tier 0 for bar, in ATLAS order:")
    for bucket in BUCKETS:
        for knob in bar[bucket][0]:
            say(f"  {bucket:<12} {knob.label:<28} {knob.control:<11} {knob.description[:60]}")

    say()
    say(f"depth cap = {MAX_DEPTH}; compound objects cut by it: {len(cut_at_depth())}")
    for path in cut_at_depth():
        say(f"  cut: {path}")
    say(f"compound objects cut by the loop guard: {len(cut_as_cycle())}")
    for path in cut_as_cycle():
        say(f"  loop: {path}")
    say(f"paths with no bucket rule (filed under FRAME): {len(unmatched())}")
    for path in unmatched():
        say(f"  unmatched: {path}")

    say()
    if failures:
        say(f"FAILURES: {len(failures)}")
        for f in failures:
            say("  " + f)
        return 1
    say(f"OK - {len(SELFTEST_TRACES)} trace types built, none failed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
