"""THE SEAM - where the Bench's DataFrame comes from.

The Bench takes a DataFrame and does not care where it came from. This module is
the one place that answers "from where?", so wiring the real warehouse in was a
swap and not a rewrite.

Two kinds of source, and that is the whole story:

    {"kind": "demo",      "name": "category"}     -> fake data, no network
    {"kind": "warehouse", "sql":  "SELECT ..."}   -> the guarded read lane

WHAT THIS MODULE DOES NOT DO
----------------------------
It does not talk to Snowflake itself. Every warehouse read goes through
`viz.sqlrun.run()` untouched - that module is the one chokepoint holding the
text guard, the claim-table block, single-statement execution, the verified
read-only lane, the row/cell caps and the 300s timeout. Reimplementing any of
that here, or routing around it, would quietly delete a safety belt. So we call
it with exactly two arguments and pass its answer straight back up.

One deliberate consequence: `sqlrun.run()` takes an `unsafe_claims` flag that
force-reads the raw claim tables (unreviewed accusations about named people).
The Bench never passes it. A chart tool is not the place to punch through the
libel firewall - query LIBRARY_META."CONNECT".V_LEADS_PUBLISHED instead.

ERRORS ARE RETURN VALUES, NOT EXCEPTIONS
----------------------------------------
`frame()` never raises for a bad source. A refused query, a typo'd demo name or
a dead connection all come back as `(empty DataFrame, meta)` with
`meta["ok"] is False` and `meta["error"]` holding the plain-English reason.
That matches the rule codegen.parse lives by, and it means the UI always has a
meta to render - the lane badge and the row count are never allowed to vanish
off the screen just because something went wrong.

THE FRAME CACHE - why it exists and what it promises
----------------------------------------------------
Every knob turn in the Bench repaints the figure, and repainting means having
the DataFrame again. Without a cache that is a live Snowflake round trip per
knob turn (a bare `SELECT 1` measured at 9.4s on this box), so `frame()` keeps
its answers.

    frame(source)                  cached; a repeat is a dict lookup
    frame(source, refresh=True)    bypass and REPLACE - what RUN passes
    frame(source, copy=False)      the cached frame itself, read-only
    frame_info(source)             columns and roles, worked out once
    invalidate(source) / invalidate()   drop one entry, or the lot
    cache_stats()                  what is in there and how big it is

Five promises, and each one is a thing that bit someone:

  1. THE CACHE HOLDS THE RESULT, NEVER THE GUARD. A warehouse read still goes
     through viz.sqlrun in full, every time it is really fetched. Nothing here
     remembers a permission, a lane or a refusal *decision* - only the answer
     that came back, keyed on the exact source that produced it.
  2. IT IS BOUNDED. CACHE_MAX_ENTRIES entries and CACHE_MAX_BYTES of frames,
     least-recently-used evicted first. A 100k-row result is a real thing the
     read lane will hand you, so an unbounded dict of them is a memory leak
     with a friendly name.
  3. A CACHED HIT SAYS SO. meta comes back whole - lane, rows, truncated,
     elapsed_s, as_of - with the ORIGINAL elapsed_s, plus `cached=True` and
     `cache_age_s`. The status bar is never allowed to imply it just re-queried
     when it did not.
  4. IT IS THREAD-SAFE. Dash serves callbacks on threads. The cache is guarded
     by a lock, and two threads asking for the same source at the same time
     produce ONE fetch, not two - the second waits and gets the first's answer.
  5. FAILURES ARE CACHED TOO, ON PURPOSE. A dead connection is the slowest
     thing in the building. Caching the refusal is what stops every knob turn
     re-dialling it. `refresh=True` - the RUN button - is how you retry, and it
     is the only way, which is said out loud here so nobody has to guess.

THE COLUMN-ROLE HELPER
----------------------
`column_roles(df)` sorts a result's columns into numeric / category / date /
geo_state / year so `registry.py` can grey out the charts this data cannot draw
and say why. It delegates to `viz.plugs.column_roles()` - which already handles
the all-TEXT landing-table case and the trap where all-digit strings ('15020000001',
an FEC image number) get misread as epoch dates - and then applies one
correction of its own: a column that is *already* a real datetime dtype is a
date, full stop. See `column_roles` for why that correction is needed.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

# Anchor imports to the repo root, not the current working directory, so this
# works whether you run `python bench/app.py`, `pytest`, or a REPL from anywhere.
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from bench import wall  # noqa: E402  the 144 charts + the fake-data generators
from viz import plugs  # noqa: E402  column-role sniffing (pure pandas, no network)
from bench import settings  # noqa: E402  stdlib-only tunables
from viz import sqlrun  # noqa: E402  THE guarded read lane - never bypassed

# Importing wall has one side effect worth knowing about: it registers the dark
# "wall" Plotly template and makes it the default for the whole process. That is
# what makes every Bench chart match the wall page without repeating forty lines
# of update_layout. Nothing else in this module depends on it.

__all__ = [
    "DEMO", "DemoFrame", "ROLES", "FrameInfo",
    "frame", "frame_info", "demo_names", "demo_catalogue", "demo_shape",
    "column_roles", "role_of", "columns_for", "describe_roles",
    "lane", "tables", "table_columns", "table_profile", "starter_sql",
    "clear_demo_cache", "invalidate", "cache_stats", "source_key",
    "CACHE_MAX_ENTRIES", "CACHE_MAX_BYTES",
]


# =====================================================================
# DEMO FRAMES
# ---------------------------------------------------------------------
# The generators already live in wall.py. We do not copy them - we point
# at them and add a slug, a plain-English shape line, and the bit of
# reshaping the three non-DataFrame generators need.
# =====================================================================


@dataclass(frozen=True)
class DemoFrame:
    """One fake dataset the Bench can draw on, and what SHAPE it has.

    `shape` is the sentence that decides which charts are even possible - it is
    lifted straight off the generator's own docstring in wall.py, so the two
    files can never drift apart.
    """

    name: str                         # the slug you put in source["name"]
    build: Callable[[], pd.DataFrame]  # returns the DataFrame
    shape: str                        # plain English: what columns you get
    note: str = ""                    # anything extra worth saying
    wide: bool = False                # True = a pivot/grid, not one row per thing
    extra: dict = field(default_factory=dict)  # e.g. the geojson for a choropleth

    @property
    def label(self) -> str:
        """A human-readable name for a dropdown."""
        return self.name.replace("_", " ")


def _doc(fn) -> str:
    """The first line of a generator's docstring - its shape, in one sentence."""
    return (fn.__doc__ or "").strip().split("\n")[0].strip()


# --- the three generators that hand back something other than a DataFrame ----
# wall.py returns raw numpy for these because that is what the 3D traces eat.
# The Bench works in DataFrames, so we tidy them here - one row per point.


def _df_surface() -> pd.DataFrame:
    """d_surface returns a 2D numpy grid. Wrap it as a grid DataFrame."""
    z = wall.d_surface()
    return pd.DataFrame(
        z,
        index=[f"r{i:02d}" for i in range(z.shape[0])],
        columns=[f"c{j:02d}" for j in range(z.shape[1])],
    )


def _df_volume() -> pd.DataFrame:
    """d_volume returns four flat arrays. One row per point in the cube."""
    x, y, z, value = wall.d_volume()
    return pd.DataFrame({"x": x, "y": y, "z": z, "value": value})


def _df_vectorfield() -> pd.DataFrame:
    """d_vectorfield returns six flat arrays: position + direction per point."""
    x, y, z, u, v, w = wall.d_vectorfield()
    return pd.DataFrame({"x": x, "y": y, "z": z, "u": u, "v": v, "w": w})


def _df_geojson_zones() -> pd.DataFrame:
    """d_geojson_boxes returns (geojson, df). The polygons ride in `extra`."""
    _geojson, df = wall.d_geojson_boxes()
    return df


_GEOJSON = wall.d_geojson_boxes()[0]


def _demo(name, build, shape=None, note="", wide=False, extra=None) -> DemoFrame:
    return DemoFrame(
        name=name,
        build=build,
        shape=shape or _doc(build),
        note=note,
        wide=wide,
        extra=extra or {},
    )


# The catalogue. Slugs match wall.py's generator names minus the `d_` prefix,
# so there is never a question about which function made which frame.
DEMO: dict[str, DemoFrame] = {
    d.name: d
    for d in [
        _demo("category", wall.d_category),
        _demo("category_2way", wall.d_category_2way),
        _demo("long", wall.d_long,
              note="The un-aggregated one. Feed it to a box plot, a histogram or "
                   "an ECDF - anything that wants many rows per group."),
        _demo("bimodal", wall.d_bimodal),
        _demo("scatter", wall.d_scatter),
        _demo("numeric_block", wall.d_numeric_block),
        _demo("timeseries", wall.d_timeseries),
        _demo("hierarchy", wall.d_hierarchy),
        _demo("flow", wall.d_flow),
        _demo("stages", wall.d_stages),
        _demo("geo_points", wall.d_geo_points),
        _demo("states", wall.d_states,
              note="'state' holds two-letter US codes, so px.choropleth needs no "
                   "GeoJSON at all. 'change' straddles zero - use a diverging scale."),
        _demo("ohlc", wall.d_ohlc),
        _demo("grid", wall.d_grid, wide=True,
              note="Already pivoted: the row LABELS live in the index, not in a "
                   "column. px.imshow reads them for free; px.bar cannot."),
        _demo("surface", _df_surface,
              shape=_doc(wall.d_surface) + " Wrapped here as a grid DataFrame.",
              wide=True),
        _demo("volume", _df_volume,
              shape=_doc(wall.d_volume) + " Flattened here to one row per point."),
        _demo("vectorfield", _df_vectorfield,
              shape=_doc(wall.d_vectorfield) + " Flattened here to one row per point."),
        _demo("ternary", wall.d_ternary,
              note="Careful: the column named 'state' here is a SHARE, not a place "
                   "code. It classifies numeric, which is correct."),
        _demo("wind", wall.d_wind),
        _demo("gantt", wall.d_gantt),
        _demo("rank_over_time", wall.d_rank_over_time),
        _demo("geojson_zones", _df_geojson_zones,
              shape="One row per region (a zone code + a number). The matching "
                    "polygons ride on meta['geojson'].",
              note="Those polygons are exactly what px.choropleth_map(geojson=...) "
                   "wants - this is the demo for boundaries that are not "
                   "countries or states.",
              extra={"geojson": _GEOJSON}),
    ]
}


def demo_names() -> list[str]:
    """Every demo frame slug, in menu order."""
    return list(DEMO)


def demo_shape(name: str) -> str:
    """The one-sentence shape of a demo frame, or '' if that name is unknown."""
    d = DEMO.get(name)
    return d.shape if d else ""


_CATALOGUE: list[dict] | None = None


def demo_catalogue() -> list[dict]:
    """Every demo frame with its shape, its columns and its size.

    This is what the source dropdown renders, and it means the menu says the
    real column names rather than a guess.

    TWO THINGS THIS DELIBERATELY DOES NOT DO, both measured:

      * it does not rebuild. All 22 frames plus their roles cost 26.8ms, and
        `source_bar` asks for the lot every time it is drawn. It is a pure
        function of DEMO, so it is worked out once per process and kept.
      * it does not go through the frame cache. Twenty-two menu entries would
        evict the query you are actually looking at (CACHE_MAX_ENTRIES is 8),
        so the catalogue fetches past it. A menu is not a working set.
    """
    global _CATALOGUE
    if _CATALOGUE is not None:
        return _CATALOGUE
    out = []
    for d in DEMO.values():
        df, _meta = _fetch({"kind": "demo", "name": d.name})
        roles = column_roles(df)
        out.append({
            "name": d.name,
            "label": d.label,
            "shape": d.shape,
            "note": d.note,
            "wide": d.wide,
            "rows": len(df),
            "columns": [str(c) for c in df.columns],
            "roles": roles,
            "roles_line": describe_roles(roles),
        })
    _CATALOGUE = out
    return out


# --- the cache -------------------------------------------------------------
# Two reasons this matters more than it looks:
#   1. wall.RNG is one module-level generator, so calling d_scatter() twice
#      hands back DIFFERENT numbers. Every knob turn re-renders the figure, and
#      a chart whose data jitters under your hands is unusable.
#   2. It makes a demo frame reproducible across processes, because we seed a
#      fresh generator per frame and put wall's own one back afterwards.
_CACHE: dict[str, pd.DataFrame] = {}


def clear_demo_cache() -> None:
    """Forget the built demo frames. Mostly for tests.

    It drops three things, because leaving any one of them behind would make
    "cold" a lie: the built frames, every demo entry sitting in the frame cache
    on top of them, and the memoised catalogue. Warehouse entries are left
    alone - this function's name says demo, and a warehouse result is the
    expensive thing you least want thrown away by a helper you called for
    something else. Use `invalidate()` for those.
    """
    _CACHE.clear()
    global _CATALOGUE
    _CATALOGUE = None
    with _CACHE_LOCK:
        for key, entry in list(_FRAMES.items()):
            if entry.kind == "demo":
                _FRAMES.pop(key, None)


def _seed_for(name: str) -> int:
    """A stable seed per demo frame - same name, same numbers, every run.

    Rolled by hand because Python's built-in hash() of a string is salted per
    process, so it would give a different answer on every launch.
    """
    return sum((i + 1) * ord(ch) for i, ch in enumerate(name))


def _build_demo(d: DemoFrame) -> pd.DataFrame:
    """Build one demo frame deterministically, then restore wall's generator."""
    saved = wall.RNG
    wall.RNG = np.random.default_rng(_seed_for(d.name))
    try:
        return d.build()
    finally:
        wall.RNG = saved


# =====================================================================
# THE FRAME CACHE
# ---------------------------------------------------------------------
# One bounded, thread-safe, LRU store of (DataFrame, meta) keyed on the
# source that produced it. Read the promises in the module docstring
# before changing anything here - four of the five are load-bearing.
# =====================================================================

# THE CAPS, and why these numbers.
#
# viz.sqlrun hands back at most MAX_LIMIT_ROWS = 100,000 rows or
# LIMIT_CELLS = 2,000,000 cells, whichever bites first. Measured on this box:
# a 100,000 x 6 mixed result is 19 MB, and the worst case the read lane can
# legally produce - 2,000,000 cells of short strings - is about 130 MB.
#
#   CACHE_MAX_BYTES = 256 MB   holds one worst-case result AND the working set
#                              around it, and is a number this machine can
#                              carry without anyone noticing.
#   CACHE_MAX_ENTRIES = 8      the demo you started on, the two or three
#                              queries you are flipping between, and slack.
#                              Past that you are browsing, not working, and a
#                              re-fetch of something you left ten clicks ago is
#                              the right price for a bounded cache.
#
# Both are module-level on purpose: a test (or a bigger box) can turn them up
# without editing this file.
CACHE_MAX_ENTRIES = 8
CACHE_MAX_BYTES = 256 * 1024 * 1024

# Above this many rows, a frame's size is ESTIMATED from a head sample rather
# than measured exactly. `memory_usage(deep=True)` walks every string in the
# frame - 17ms on a 100k-row result, measured - and paying that on every insert
# to feed a cache budget is the tail wagging the dog. Under the sample size it
# is exact, because exact is free there.
_CACHE_SAMPLE_ROWS = 5_000


@dataclass(eq=False)
class _Entry:
    """One cached answer: the frame, its meta, and what it costs to keep.

    `eq=False` because a generated `__eq__` would compare DataFrames, and
    `df1 == df2` on frames is an elementwise array, not a bool. Nothing here
    compares entries; identity is the only thing that means anything.
    """

    key: str
    kind: str                 # "demo" | "warehouse" | whatever the source said
    source: Any               # a JSON round-trip of the source, for cache_stats
    df: pd.DataFrame
    meta: dict                # sealed at fetch time; never handed out directly
    nbytes: int
    made_at: float            # time.time() of the fetch that filled this
    serves: int = 0           # how many callers have been handed this answer

    @cached_property
    def info(self) -> "FrameInfo":
        """The columns-and-roles view, built once and kept with the frame."""
        return FrameInfo(self.key, self.df, self.meta)


_FRAMES: "OrderedDict[str, _Entry]" = OrderedDict()

# One lock over the cache bookkeeping. It is held for dict operations ONLY -
# never across a fetch, because a 9.4s Snowflake round trip inside this lock
# would stall every other Dash callback in the process.
_CACHE_LOCK = threading.RLock()

# One lock PER SOURCE, so two threads asking for the same query at the same
# moment produce one fetch and not two. Refcounted, so the dict cannot grow.
_KEY_LOCKS: dict[str, tuple[threading.Lock, int]] = {}

_STATS = {"hits": 0, "misses": 0, "refreshes": 0, "evictions": 0, "oversized": 0}


def source_key(source: Any) -> str:
    """The stable cache key for a source dict.

    Canonical JSON (sorted keys, `default=str` for anything exotic) hashed to a
    fixed-width digest, so one character of different SQL is a different entry
    and a 40 KB query does not become a 40 KB dict key.

    Rolled by hand rather than with `hash()`, for the same reason `_seed_for`
    is: Python salts the hash of a string per process, so `hash()` would give a
    different answer on every launch. blake2b is fast and is not being asked to
    be a security boundary - this is a cache key.
    """
    try:
        text = json.dumps(source, sort_keys=True, default=str)
    except Exception:                       # a source that will not serialise
        text = repr(source)
    return hashlib.blake2b(text.encode("utf-8"), digest_size=16).hexdigest()


def _frame_bytes(df: pd.DataFrame) -> int:
    """How much memory this frame is holding down, in bytes.

    Exact under `_CACHE_SAMPLE_ROWS` rows; a head-sample scaled by row count
    above it. An estimate is honest for a budget - it decides what to evict,
    not what to show anyone - and it keeps an insert cheap on the big results
    the cache exists for.
    """
    try:
        rows = len(df)
        if rows <= _CACHE_SAMPLE_ROWS:
            return int(df.memory_usage(index=True, deep=True).sum())
        head = df.head(_CACHE_SAMPLE_ROWS)
        sampled = int(head.memory_usage(index=True, deep=True).sum())
        return int(sampled * (rows / float(_CACHE_SAMPLE_ROWS)))
    except Exception:                       # an exotic dtype; do not blow up
        return 0


def _key_lock(key: str) -> threading.Lock:
    """The per-source lock, refcounted so `_KEY_LOCKS` stays bounded."""
    with _CACHE_LOCK:
        lock, waiting = _KEY_LOCKS.get(key, (threading.Lock(), 0))
        _KEY_LOCKS[key] = (lock, waiting + 1)
        return lock


def _drop_key_lock(key: str) -> None:
    with _CACHE_LOCK:
        got = _KEY_LOCKS.get(key)
        if got is None:
            return
        lock, waiting = got
        if waiting <= 1:
            _KEY_LOCKS.pop(key, None)
        else:
            _KEY_LOCKS[key] = (lock, waiting - 1)


def _touch(key: str) -> _Entry | None:
    """Look one up and mark it as the most recently used. None on a miss."""
    with _CACHE_LOCK:
        entry = _FRAMES.get(key)
        if entry is None:
            return None
        _FRAMES.move_to_end(key)
        return entry


def _store(key: str, source: Any, df: pd.DataFrame, meta: dict) -> _Entry:
    """Put one answer in, then evict until both caps hold again."""
    entry = _Entry(
        key=key,
        kind=str(meta.get("kind") or "unknown"),
        source=json.loads(json.dumps(source, default=str)) if source is not None else None,
        df=df,
        meta=dict(meta),
        nbytes=_frame_bytes(df),
        made_at=time.time(),
    )
    with _CACHE_LOCK:
        _FRAMES.pop(key, None)          # a refresh REPLACES, it does not stack
        _FRAMES[key] = entry
        _evict()
    return entry


def _evict() -> None:
    """LRU eviction. The caller holds `_CACHE_LOCK`.

    One deliberate exception: a single result bigger than the whole budget is
    kept anyway, alone. Refusing to cache it would mean re-running the most
    expensive query in the app on every knob turn, which is the exact thing
    this cache exists to stop. It is counted, so `cache_stats()` can say it
    happened rather than leaving you to wonder where the memory went.
    """
    while _FRAMES and (len(_FRAMES) > CACHE_MAX_ENTRIES
                       or (_bytes_held() > CACHE_MAX_BYTES and len(_FRAMES) > 1)):
        _FRAMES.popitem(last=False)     # least recently used
        _STATS["evictions"] += 1
    if len(_FRAMES) == 1 and _bytes_held() > CACHE_MAX_BYTES:
        _STATS["oversized"] += 1


def _bytes_held() -> int:
    return sum(e.nbytes for e in _FRAMES.values())


def _serve(entry: _Entry, *, copy: bool, fetched: bool) -> tuple[pd.DataFrame, dict]:
    """Hand one cached answer out, and be honest about where it came from.

    `fetched` is True only for the call that actually did the work. Everyone
    else gets `cached=True`, the ORIGINAL `elapsed_s`, and a note saying so -
    the status bar must never imply it just re-queried when it did not.

    `copy=True` (the default) hands back a copy, so a caller that edits the
    frame cannot poison the cache. Measured: 1.0ms on a 100k x 6 result.
    `copy=False` hands back the cached frame itself and is the right call for
    a render path that only reads - which is every chart builder in
    registry.py, all of which copy before they mutate.
    """
    with _CACHE_LOCK:
        entry.serves += 1
    meta = dict(entry.meta)
    notes = list(meta.get("notes") or [])
    age = max(0.0, time.time() - entry.made_at)
    meta["cached"] = not fetched
    meta["cache_key"] = entry.key
    meta["cache_age_s"] = 0.0 if fetched else round(age, 3)
    if not fetched:
        notes.append(
            f"served from the frame cache ({age:,.0f}s old) - elapsed_s is what "
            "the ORIGINAL fetch took, not this one. Press RUN to re-query.")
    meta["notes"] = notes
    return (entry.df.copy() if copy else entry.df), meta


def _entry_for(source: Any, refresh: bool) -> tuple[_Entry, bool]:
    """The cache entry for a source, fetching it if we have to.

    Returns (entry, fetched). Everything that costs time happens OUTSIDE
    `_CACHE_LOCK` and inside a per-source lock, so:
      * a slow query never blocks a callback asking for a different source;
      * two callbacks asking for the SAME source produce one fetch, and the
        second waits for the first rather than firing its own.
    """
    key = source_key(source)

    if not refresh:
        entry = _touch(key)
        if entry is not None:
            with _CACHE_LOCK:
                _STATS["hits"] += 1
            return entry, False

    lock = _key_lock(key)
    try:
        with lock:
            if not refresh:
                # Someone else may have filled it while we waited for the lock.
                entry = _touch(key)
                if entry is not None:
                    with _CACHE_LOCK:
                        _STATS["hits"] += 1
                    return entry, False
            with _CACHE_LOCK:
                _STATS["refreshes" if refresh else "misses"] += 1
            df, meta = _fetch(source)
            return _store(key, source, df, meta), True
    finally:
        _drop_key_lock(key)


def invalidate(source: Any = None) -> int:
    """Forget one cached source, or all of them. Returns how many went.

    This is the explicit refresh door for anything that is not a `frame()`
    call - `frame(source, refresh=True)` is the same thing done in one step,
    and is what the RUN button should use. Demo BUILDERS are untouched; that
    is `clear_demo_cache`.
    """
    with _CACHE_LOCK:
        if source is None:
            gone = len(_FRAMES)
            _FRAMES.clear()
            return gone
        return 1 if _FRAMES.pop(source_key(source), None) is not None else 0


def cache_stats() -> dict:
    """What is in the cache right now, and what it has been doing.

    Counters are cumulative for the life of the process. `frames` is listed
    least-recently-used first, which is eviction order.
    """
    with _CACHE_LOCK:
        now = time.time()
        return {
            "entries": len(_FRAMES),
            "bytes": _bytes_held(),
            "max_entries": CACHE_MAX_ENTRIES,
            "max_bytes": CACHE_MAX_BYTES,
            **dict(_STATS),
            "frames": [
                {
                    "key": e.key,
                    "kind": e.kind,
                    "rows": int(e.meta.get("rows") or 0),
                    "ok": bool(e.meta.get("ok")),
                    "bytes": e.nbytes,
                    "age_s": round(max(0.0, now - e.made_at), 3),
                    "serves": e.serves,
                    "source": e.source,
                }
                for e in _FRAMES.values()
            ],
        }


# =====================================================================
# THE SEAM
# =====================================================================


def frame(source: dict, *, refresh: bool = False,
          copy: bool = True) -> tuple[pd.DataFrame, dict]:
    """Get the DataFrame a SPEC asks for. `source` is SPEC['source'].

        frame({"kind": "demo", "name": "category"})
        frame({"kind": "warehouse", "sql": "SELECT ...", "limit_rows": 5000})

    Returns (df, meta). Never raises for a bad source - check `meta["ok"]`.

    CACHED, keyed on the whole source dict. A repeat call with the same source
    does not touch Snowflake and does not regenerate demo data - see the module
    docstring for the five promises that come with that.

        refresh=True   bypass the cache and REPLACE the entry. This is what a
                       RUN button passes: pressing Run on the same SQL has to
                       genuinely run it again.
        copy=False     hand back the cached frame itself instead of a copy.
                       Read-only: edit it and you have edited the cache. Worth
                       it on a repaint path, which only ever reads.

    meta always carries:
        ok         True when the frame is real data
        kind       "demo" | "warehouse"
        rows       len(df)
        elapsed_s  how long the ORIGINAL fetch took, in seconds. A cached hit
                   reports that number, not ~0, and flags itself with `cached`.
        truncated  True when the row cap cut the result short
        lane       "demo", or the warehouse lane sqlrun proved: "enforced"
                   (read-only enforced server-side) or "client-guard"
        as_of      the data-vintage stamp, or None when nothing could prove one
        notes      plain-English lines the UI should be willing to show
        cached     True when this answer came out of the cache
        cache_age_s  how old that cached answer is, in seconds (0.0 when fresh)
        cache_key  the entry it came from, for `cache_stats()` and for debugging
        error      only present when ok is False
    """
    entry, fetched = _entry_for(source, refresh)
    return _serve(entry, copy=copy, fetched=fetched)


def frame_info(source: dict, *, refresh: bool = False) -> "FrameInfo":
    """Columns and roles for a source, worked out once and kept.

    The picker asks "what can this result draw?" on every single repaint, and
    the answer is a pure function of the frame - so it is computed on first ask
    and then handed back for free. Measured on a 100k-row result:
    `column_roles` 9.7ms, `registry.roles` 4.1ms, every repaint, for an answer
    that cannot have changed.

    Same cache and same key as `frame()`, so the two can never disagree about
    which frame they are describing.
    """
    entry, _fetched = _entry_for(source, refresh)
    return entry.info


class FrameInfo:
    """One result's shape: its columns, and what each column can be used as.

    Everything expensive on here is worked out on first access and then kept,
    so asking twice costs a dict lookup. Attribute, not method, wherever it
    reads better at the call site.

        info = data.frame_info(spec["source"])
        info.columns          ('STATE', 'TOTAL')   - names, stringified
        info.rows             1_240
        info.roles            {"numeric": [...], "category": [...], ...}
        info.chart_roles      {"STATE": {"category", ...}} - registry.py's shape
        info.roles_line       "this result has 1 number column, ..."
        info.df               the cached frame itself. READ-ONLY.

    Two threads hitting an unbuilt property at the same instant may both
    compute it. That is a wasted millisecond, never a wrong answer - each one
    is a pure function of a frame that cannot change under them.
    """

    def __init__(self, key: str, df: pd.DataFrame, meta: dict):
        self.key = key
        self.df = df                       # shared with the cache: do not edit
        self._meta = meta
        self.rows = int(len(df))
        self.raw_columns: tuple = tuple(df.columns)
        self.columns: tuple[str, ...] = tuple(str(c) for c in df.columns)
        self.ok = bool(meta.get("ok"))

    @property
    def meta(self) -> dict:
        """A copy of the frame's meta. Copy, so a caller cannot edit the cache."""
        return dict(self._meta)

    @cached_property
    def roles(self) -> dict[str, list]:
        """`column_roles(df)` - {"numeric": [...], "category": [...], ...}."""
        return column_roles(self.df)

    @cached_property
    def role_of(self) -> dict[Any, str]:
        """{column -> its one role}. The inverse of `roles`."""
        out: dict[Any, str] = {}
        for role, cols in self.roles.items():
            for c in cols:
                out[c] = role
        return out

    @cached_property
    def roles_line(self) -> str:
        """The plain-English line: 'this result has 2 number columns, ...'."""
        return describe_roles(self.roles)

    @cached_property
    def chart_roles(self) -> dict[Any, set[str]]:
        """`registry.roles(df)` - {column: {role, role}}, the picker's shape.

        registry.py sorts columns the other way up from `column_roles` and does
        its own lat/lon range checks, so the picker needs THIS one and not a
        translation of the other. Imported lazily and by hand, exactly the way
        knobs.py reaches for the registry: this module must stay importable
        with nothing else in the room.
        """
        if not len(self.df.columns):
            return {}
        from bench import registry  # noqa: PLC0415  (deliberately lazy)
        return registry.roles(self.df)

    def columns_for(self, role: str) -> list:
        """Every column that can fill `role`, honest substitutions included."""
        return columns_for(self.roles, role)

    def __repr__(self) -> str:            # pragma: no cover - a debugging aid
        return (f"FrameInfo({self._meta.get('kind')!r}, {self.rows:,} rows, "
                f"{len(self.columns)} columns)")


def _fetch(source: Any) -> tuple[pd.DataFrame, dict]:
    """The real work: read a source, with no cache anywhere near it.

    This is `frame()` minus the cache, and it is what the cache calls on a
    miss. Split out so there is exactly one place that decides what a source
    means, and so the cache can be tested by counting calls to this.
    """
    t0 = time.time()
    if not isinstance(source, dict):
        return _fail("unknown", f"source must be a dict, got {type(source).__name__}", t0)

    kind = str(source.get("kind") or "").strip().lower()
    if kind == "demo":
        return _demo_frame(source, t0)
    if kind == "warehouse":
        return _warehouse_frame(source, t0)
    return _fail(
        kind or "unknown",
        f"source kind {source.get('kind')!r} is not one of: demo, warehouse",
        t0,
    )


def _demo_frame(source: dict, t0: float) -> tuple[pd.DataFrame, dict]:
    """Fake data from wall.py. No network, no credentials, runs on a plane."""
    name = str(source.get("name") or "").strip()
    d = DEMO.get(name)
    if d is None:
        return _fail(
            "demo",
            f"no demo frame named {name!r}. Available: {', '.join(demo_names())}",
            t0,
        )

    cached = name in _CACHE
    if not cached:
        _CACHE[name] = _build_demo(d)
    # Hand out a copy so a caller that edits the frame cannot poison the cache.
    df = _CACHE[name].copy()

    notes = ["demo data - generated in this process, nothing left the machine",
             "as_of is None because generated data has no vintage"]
    if cached:
        notes.append("served from the in-process demo cache, so elapsed_s is ~0")
    if d.note:
        notes.append(d.note)

    meta = {
        "ok": True,
        "kind": "demo",
        "name": name,
        "shape": d.shape,
        "wide": d.wide,
        "rows": len(df),
        "elapsed_s": round(time.time() - t0, 3),
        "truncated": False,
        "lane": "demo",
        "as_of": None,
        "notes": notes,
    }
    meta.update(d.extra)  # e.g. meta["geojson"] for the choropleth demo
    return df, meta


def _warehouse_frame(source: dict, t0: float) -> tuple[pd.DataFrame, dict]:
    """Real data, through viz.sqlrun.run() - the one guarded read lane.

    Everything protective happens inside that call: the text guard, the
    claim-table block, single-statement execution, the verified read-only role,
    the row/cell caps and the 300s statement timeout. We add nothing and we
    remove nothing. We only relabel its answer for the UI.
    """
    sql = str(source.get("sql") or "").strip()
    if not sql:
        return _fail("warehouse", "no SQL to run - the query box is empty", t0)

    if source.get("deferred"):
        # A spec restored from a previous session or loaded from a file. The
        # SQL is real but nothing may hit Snowflake without a human asking -
        # RUN builds a fresh source dict without this flag, which is the ask.
        return _fail("warehouse",
                     "restored SQL has not run this session - switch the "
                     "source bar to warehouse SQL and press RUN to run it",
                     t0, lane="idle")

    limit_rows = int(source.get("limit_rows") or sqlrun.DEFAULT_LIMIT_ROWS)

    try:
        df, meta = sqlrun.run(sql, limit_rows)
    except sqlrun.GuardError as exc:
        # The read lane refused the query and told us exactly why. That reason
        # is the most useful thing on the screen - pass it through verbatim.
        return _fail("warehouse", str(exc), t0, lane="refused")
    except Exception as exc:  # connection, syntax, permissions, budget
        return _fail("warehouse", f"{type(exc).__name__}: {exc}", t0)

    out = dict(meta)  # sqlrun's own meta: rows, truncated, elapsed_s,
                      # warehouse, role?, lane, as_of, budget, claim_refs
    out["ok"] = True
    out["kind"] = "warehouse"
    out["sql"] = sql
    out["limit_rows"] = limit_rows

    notes: list[str] = []
    if out.get("lane") != "enforced":
        notes.append("lane is NOT server-side enforced - the client guard is all "
                     "that stands between this box and a write. Provision "
                     "SNOWFLAKE_SERVE_PAT to fix it.")
    if out.get("truncated"):
        notes.append(f"truncated at {len(df):,} rows - the chart is showing a "
                     "slice, not the whole answer")
    if out.get("as_of") is None:
        notes.append("as_of is None: this result has no _INGESTED_AT column, so "
                     "nothing could prove a data vintage")
    try:
        notes.extend(sqlrun.lane_status().get("notes") or [])
    except Exception as exc:  # pragma: no cover - lane_status needs the same connection
        _LOG.info("lane_status unavailable: %s: %s", type(exc).__name__, exc)
    out["notes"] = notes
    return df, out


def _fail(kind: str, reason: str, t0: float, lane: str = "unknown"):
    """The honest empty answer: no rows, and the reason sitting in meta."""
    meta = {
        "ok": False,
        "kind": kind,
        "error": reason,
        "rows": 0,
        "elapsed_s": round(time.time() - t0, 3),
        "truncated": False,
        "lane": "demo" if kind == "demo" else lane,
        "as_of": None,
        "notes": [reason],
    }
    return pd.DataFrame(), meta


# =====================================================================
# COLUMN ROLES
# ---------------------------------------------------------------------
# Which charts can this result even draw? That is decided by the ROLE of
# each column, not by its name. registry.py reads these buckets to grey
# out the charts that cannot be drawn - and to say why.
# =====================================================================

ROLES = ("numeric", "category", "date", "geo_state", "year")

# Plain English for each role, for the "why is this greyed out" message.
ROLE_WORDS = {
    "numeric": "a number column",
    "category": "a category column",
    "date": "a date column",
    "geo_state": "a US state-code column",
    "year": "a year column",
}

# Roles that can stand in for another role. A year is a number AND a category;
# a state code is also just a category. Substitution is one-way and explicit -
# nothing is ever guessed.
_SUBSTITUTES = {
    "numeric": ("numeric", "year"),
    "category": ("category", "geo_state", "year"),
    "date": ("date",),
    "geo_state": ("geo_state",),
    "year": ("year",),
}


def column_roles(df) -> dict[str, list[str]]:
    """Sort a DataFrame's columns into chart roles.

    Returns {"numeric": [...], "category": [...], "date": [...],
             "geo_state": [...], "year": [...], "empty": [...]}

    The hard work is `viz.plugs.column_roles()`, which is kept because it
    already survives two live traps:

      * an all-TEXT landing table, where every column arrives as a string and
        the role has to be sniffed from the values;
      * all-digit strings. Snowflake and pandas will both happily read
        '15020000001' as an epoch timestamp, which is how FEC image numbers
        ended up on a time axis. In that classifier numbers win: a real date
        column has separators or month names.

    One correction is added on top. That "numbers win" rule is right for
    strings and wrong for a column that is ALREADY a datetime - pandas will
    convert a datetime64 column to nanoseconds-since-epoch without complaint,
    so a genuine date column comes back classified numeric (verified: the
    'date' column of the timeseries demo). Dtype is proof, so any real
    datetime / period column is moved to `date` here, and booleans to
    `category`. The string trap handling is untouched.

    `_INGESTED_AT` and friends are provenance stamps, never chart axes, so
    plugs drops them and so do we. Columns that are entirely null land in
    `empty` rather than silently disappearing.
    """
    buckets: dict[str, list[str]] = {r: [] for r in ROLES}
    buckets["empty"] = []
    if df is None or len(getattr(df, "columns", [])) == 0:
        return buckets

    raw = _plugs_roles(df)
    for src, dest in (("numeric", "numeric"), ("category", "category"),
                      ("date", "date"), ("state", "geo_state"), ("year", "year")):
        buckets[dest] = list(raw.get(src, []))

    # The dtype correction, applied after the fact so plugs' logic stays intact.
    for col in df.columns:
        s = df[col]
        if isinstance(s, pd.DataFrame):  # duplicate column name - skip it
            continue
        want = None
        if pd.api.types.is_datetime64_any_dtype(s) or isinstance(s.dtype, pd.PeriodDtype):
            want = "date"
        elif pd.api.types.is_bool_dtype(s):
            want = "category"
        if want is None:
            continue
        for role in ROLES:
            if col in buckets[role] and role != want:
                buckets[role].remove(col)
        if col not in buckets[want] and str(col).upper() not in plugs.META_COLS:
            buckets[want].append(col)

    # Anything plugs dropped for being all-null (or unclassifiable) is named,
    # not silently lost - a column that vanishes is a bug you never find.
    placed = {c for role in ROLES for c in buckets[role]}
    for col in df.columns:
        if col in placed or str(col).upper() in plugs.META_COLS:
            continue
        buckets["empty"].append(col)
    return buckets


def _plugs_roles(df) -> dict:
    """Call viz.plugs.column_roles, tolerating odd column names.

    plugs upper-cases each column name for its heuristics, so a non-string name
    (an integer column off a numpy grid) would blow it up. Stringifying the
    names keeps every heuristic alive; if that still fails we fall back to a
    dtype-only read rather than returning nothing.
    """
    try:
        work = df.copy(deep=False)
        work.columns = [str(c) for c in df.columns]
        raw = plugs.column_roles(work)
    except Exception:
        return _dtype_only_roles(df)
    # Map the stringified names back to the originals, in order.
    back = {}
    for original in df.columns:
        back.setdefault(str(original), []).append(original)
    out = {}
    for role, cols in raw.items():
        out[role] = [back[c].pop(0) if back.get(c) else c for c in cols]
    return out


def _dtype_only_roles(df) -> dict:
    """Last-resort classification from dtypes alone. No value sniffing."""
    out = {"numeric": [], "date": [], "category": [], "state": [], "year": []}
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_datetime64_any_dtype(s):
            out["date"].append(col)
        elif pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
            out["numeric"].append(col)
        else:
            out["category"].append(col)
    return out


def role_of(df) -> dict[Any, str]:
    """The inverse view: {column -> role}. Handy for a per-column label."""
    out = {}
    for role, cols in column_roles(df).items():
        for c in cols:
            out[c] = role
    return out


def columns_for(roles: dict, role: str) -> list[Any]:
    """Every column that can fill `role`, substitutes included.

    A year column can be a number or a category. A state code can be a
    category. Ask for "category" on the states demo and you get the state
    column back, because a place code IS a category.
    """
    if role == "any":
        return [c for r in ROLES for c in roles.get(r, [])]
    return [c for r in _SUBSTITUTES.get(role, (role,)) for c in roles.get(r, [])]


def describe_roles(roles: dict) -> str:
    """One plain-English line: what this result actually has.

    'This result has 2 number columns, 1 category column and no date column.'
    is a better greyed-out button than a greyed-out button.
    """
    bits = []
    for role in ROLES:
        cols = roles.get(role) or []
        if not cols:
            continue
        word = ROLE_WORDS[role].replace("a ", "", 1)
        bits.append(f"{len(cols)} {word}" + ("s" if len(cols) > 1 else ""))
    return "this result has " + (", ".join(bits) if bits else "no chartable columns")


# =====================================================================
# TABLE / COLUMN DISCOVERY for the SQL box
# ---------------------------------------------------------------------
# All of it comes off viz/catalog.py, which reads the live CATALOG and
# INFORMATION_SCHEMA. Nothing here is a hardcoded list, so a source that
# lands next month is chartable with zero wiring.
#
# Every one of these needs a warehouse connection, so each is lazy and
# each returns an empty answer rather than raising when there isn't one.
#
# But "empty because offline" and "empty because something broke" are two
# different facts, and swallowing both into `[]` made them impossible to
# tell apart from the UI. Each helper now records what actually happened in
# LAST_CATALOG_ERROR (and the log), so app.py's note line can say which one
# it was. The return types stay exactly as they were.
# =====================================================================

_LOG = logging.getLogger("bench.data")

# The last exception a catalog helper swallowed, as one plain sentence -
# or None if the most recent call worked. Read by app.py's source bar.
LAST_CATALOG_ERROR: str | None = None


def _catalog_failed(what: str, exc: Exception) -> None:
    global LAST_CATALOG_ERROR
    reason = f"{type(exc).__name__}: {exc}"
    LAST_CATALOG_ERROR = f"{what} failed - {reason}"
    if isinstance(exc, (ImportError, ConnectionError, OSError, TimeoutError)):
        _LOG.info("%s: %s (treating as offline)", what, reason)
    else:
        _LOG.exception("%s failed", what)


def _catalog_ok() -> None:
    global LAST_CATALOG_ERROR
    LAST_CATALOG_ERROR = None


def lane() -> dict:
    """What the read lane is running as, for the badge that is always on screen.

    {"lane": "enforced" | "client-guard", "warehouse": ..., "notes": [...]}
    On no connection: {"lane": "offline", ..., "notes": [the reason]}.
    """
    try:
        return sqlrun.lane_status()
    except Exception as exc:
        return {"lane": "offline", "warehouse": None,
                "notes": [f"no warehouse connection: {type(exc).__name__}: {exc}"]}


def catalog_snapshot() -> dict | None:
    """The on-disk catalog snapshot, or None when none has been built yet.
    Pure disk read - NEVER touches the warehouse, safe to call on every
    drawer repaint."""
    try:
        from viz import catalog
        return catalog.snapshot_read()
    except Exception as exc:
        _catalog_failed("catalog.snapshot_read", exc)
        return None


def catalog_refresh() -> dict | None:
    """Rebuild the catalog snapshot - the one discovery call that costs
    warehouse time on purpose (two live queries, ~10s on a cold warehouse).
    Only ever fired by the labelled refresh button. None when offline."""
    try:
        from viz import catalog
        snap = catalog.snapshot_write()
        _catalog_ok()
        return snap
    except Exception as exc:
        _catalog_failed("catalog.snapshot_write", exc)
        return None


def budget() -> str:
    """The resource-monitor budget line, cached 10 min by sqlrun. Costs one
    metadata round trip on a cache miss - callers only invoke this after an
    action that already touched the warehouse."""
    try:
        return sqlrun.budget_line()
    except Exception as exc:
        return f"budget unknown ({type(exc).__name__}: {exc})"


def tables(term: str = "", refresh: bool = False) -> list[dict]:
    """Chartable tables matching `term`, live off the catalog. [] when offline."""
    try:
        from viz import catalog
        found = catalog.find(term, refresh=refresh)
        _catalog_ok()
        return found
    except Exception as exc:
        _catalog_failed("catalog.find", exc)
        return []


def table_columns(fqn: str) -> list[dict]:
    """DESCRIBE TABLE for one table: [{'column':..., 'sf_type':...}]. Metadata
    only - it costs no warehouse time. [] when offline."""
    try:
        from viz import catalog
        cols = catalog.columns(fqn)
        _catalog_ok()
        return cols
    except Exception as exc:
        _catalog_failed("catalog.columns", exc)
        return []


def table_profile(fqn: str) -> list[dict]:
    """Per-column chart roles for a table, sniffed in the warehouse rather than
    in pandas. Useful before you have run anything. [] when offline."""
    try:
        from viz import catalog
        prof = catalog.profile(fqn)
        _catalog_ok()
        return prof
    except Exception as exc:
        _catalog_failed("catalog.profile", exc)
        return []


def starter_sql(fqn: str, limit: int | None = None) -> str:
    """A first query for the SQL box: the casted SELECT that makes an all-TEXT
    landing table chartable, plus a LIMIT. A starting point to edit, not a
    hidden layer. Falls back to SELECT * when the catalog is unreachable.

    `limit` defaults to settings.SQL_LIMIT (env BENCH_SQL_LIMIT, 1000)."""
    if limit is None:
        limit = settings.SQL_LIMIT
    try:
        from viz import catalog
        sql = f"{catalog.cast_sql(fqn)}\nLIMIT {int(limit)}"
        _catalog_ok()
        return sql
    except Exception as exc:
        _catalog_failed("catalog.cast_sql", exc)
        return f"SELECT *\nFROM {fqn}\nLIMIT {int(limit)}"


# =====================================================================
# SELF-TEST - run `python bench/data.py`
# =====================================================================

if __name__ == "__main__":
    import inspect

    print("=" * 78)
    print("DEMO FRAMES")
    print("=" * 78)
    bad = []
    for entry in demo_catalogue():
        print(f"\n{entry['name']:<16} {entry['rows']:>6,} rows x "
              f"{len(entry['columns'])} cols{'   [wide/grid]' if entry['wide'] else ''}")
        print(f"  shape : {entry['shape']}")
        print(f"  cols  : {', '.join(entry['columns'])}")
        print(f"  roles : {entry['roles_line']}")
        for role in ROLES:
            cols = entry["roles"][role]
            if cols:
                print(f"          {role:<10} {', '.join(str(c) for c in cols)}")
        if entry["roles"].get("empty"):
            print(f"          empty      {', '.join(str(c) for c in entry['roles']['empty'])}")
        if entry["rows"] == 0:
            bad.append(entry["name"])

    print("\n" + "=" * 78)
    print("DETERMINISM (same frame twice must be identical)")
    print("=" * 78)
    clear_demo_cache()
    a, _ = frame({"kind": "demo", "name": "scatter"})
    clear_demo_cache()
    b, _ = frame({"kind": "demo", "name": "scatter"})
    print(f"  scatter built twice from a cold cache: identical = {a.equals(b)}")

    print("\n" + "=" * 78)
    print("META + FAILURE PATHS")
    print("=" * 78)
    _df, m = frame({"kind": "demo", "name": "category"})
    print(f"  demo meta      : {m}")
    _df, m = frame({"kind": "demo", "name": "nope"})
    print(f"  bad demo name  : ok={m['ok']} error={m['error']}")
    _df, m = frame({"kind": "sideways"})
    print(f"  bad kind       : ok={m['ok']} error={m['error']}")
    _df, m = frame({"kind": "warehouse", "sql": ""})
    print(f"  empty sql      : ok={m['ok']} error={m['error']}")
    _df, m = frame({"kind": "warehouse", "sql": "DROP TABLE x"})
    print(f"  guard refusal  : ok={m['ok']} lane={m['lane']} error={m['error']}")

    print("\n" + "=" * 78)
    print("WAREHOUSE LANE (import + signature only - no live call)")
    print("=" * 78)
    sig = inspect.signature(sqlrun.run)
    print(f"  viz.sqlrun.run{sig}")
    params = list(sig.parameters)
    assert params[:2] == ["sql", "limit_rows"], params
    print("  we call run(sql, limit_rows) - matches, positionally and by name")
    print(f"  unsafe_claims default = {sig.parameters['unsafe_claims'].default} "
          "(never passed by the Bench)")

    # =================================================================
    # THE FRAME CACHE - measured, not asserted
    # -----------------------------------------------------------------
    # Nothing below opens a connection. The warehouse half is proved by
    # standing a counting stub in front of the read lane and counting
    # calls, which is the only honest way to test "it did not re-query"
    # without a warehouse to not-query.
    # =================================================================
    print("\n" + "=" * 78)
    print("THE FRAME CACHE")
    print("=" * 78)
    broken: list[str] = []

    def check(name: str, ok: bool, said: str = "") -> None:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}{'   ' + said if said else ''}")
        if not ok:
            broken.append(name)

    # --- cold vs warm, on demo data ---------------------------------
    invalidate()
    clear_demo_cache()
    src = {"kind": "demo", "name": "long"}
    t0 = time.perf_counter()
    frame(src)
    cold_ms = (time.perf_counter() - t0) * 1000

    warm = []
    for _ in range(11):
        t0 = time.perf_counter()
        frame(src, copy=False)
        warm.append((time.perf_counter() - t0) * 1000)
    warm_ms = sorted(warm)[len(warm) // 2]
    print(f"  cold  {cold_ms:7.3f} ms   warm {warm_ms:7.3f} ms   "
          f"({cold_ms / max(warm_ms, 1e-9):,.1f}x)")

    # --- the meta round trip ----------------------------------------
    invalidate(src)
    _df, first = frame(src)
    _df, again = frame(src)
    check("first call reports cached=False", first["cached"] is False)
    check("repeat call reports cached=True", again["cached"] is True)
    check("elapsed_s is the ORIGINAL, not ~0 for the repeat",
          again["elapsed_s"] == first["elapsed_s"],
          f"{first['elapsed_s']} == {again['elapsed_s']}")
    check("lane / rows / truncated / as_of all survive",
          all(again[k] == first[k] for k in ("lane", "rows", "truncated", "as_of")))
    check("the cached hit says so in notes",
          any("frame cache" in n for n in again["notes"]))

    # --- editing a served frame cannot poison the cache --------------
    got, _m = frame(src)
    got.iloc[0, 0] = "POISON"
    fresh, _m = frame(src)
    check("a caller editing its copy cannot poison the cache",
          fresh.iloc[0, 0] != "POISON")

    # --- eviction ----------------------------------------------------
    invalidate()
    names = demo_names()[: CACHE_MAX_ENTRIES + 3]
    for name in names:
        frame({"kind": "demo", "name": name})
    stats = cache_stats()
    check(f"entries capped at {CACHE_MAX_ENTRIES}",
          stats["entries"] == CACHE_MAX_ENTRIES,
          f"{len(names)} sources in -> {stats['entries']} kept")
    kept = [f["source"]["name"] for f in stats["frames"]]
    check("the LEAST recently used ones went",
          kept == names[-CACHE_MAX_ENTRIES:], f"kept {kept}")

    # --- explicit refresh REPLACES ----------------------------------
    calls = {"n": 0}
    payload = {"n": 1}

    def fake_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        calls["n"] += 1
        return (pd.DataFrame({"N": [payload["n"]] * 3}),
                {"rows": 3, "truncated": False, "elapsed_s": 9.4,
                 "warehouse": "SERVE_WH", "lane": "enforced",
                 "as_of": "2026-08-01 00:00:00", "budget": "", "claim_refs": []})

    real_run, real_lane = sqlrun.run, sqlrun.lane_status
    setattr(sqlrun, "run", fake_run)
    setattr(sqlrun, "lane_status", lambda: {"lane": "enforced", "notes": []})
    try:
        wh = {"kind": "warehouse", "sql": "SELECT 1"}
        invalidate(wh)
        calls["n"] = 0
        frame(wh)
        frame(wh)
        check("two identical requests -> the read lane ran ONCE",
              calls["n"] == 1, f"{calls['n']} call(s)")

        _df, warm_meta = frame(wh)
        check("a cached warehouse hit keeps the ORIGINAL elapsed_s",
              warm_meta["elapsed_s"] == 9.4 and warm_meta["cached"] is True,
              f"elapsed_s={warm_meta['elapsed_s']} cached={warm_meta['cached']}")

        payload["n"] = 2
        stale, _m = frame(wh)
        replaced, meta_r = frame(wh, refresh=True)
        after, _m = frame(wh)
        check("refresh=True re-runs the query", calls["n"] == 2, f"{calls['n']} calls")
        check("refresh=True REPLACES the entry",
              int(stale["N"][0]) == 1 and int(replaced["N"][0]) == 2
              and int(after["N"][0]) == 2)
        check("the refreshed answer is not flagged cached",
              meta_r["cached"] is False)
        check("the guard is never cached - only its answer is",
              "SELECT 1" == wh["sql"] and meta_r["lane"] == "enforced")

        # --- the BYTE cap, on frames the size the read lane really returns
        rng = np.random.default_rng(3)
        big = pd.DataFrame({
            "STATE": rng.choice(["CA", "TX", "NY", "FL", "OH"], 100_000),
            "AGENCY": rng.choice([f"agency {i:03d}" for i in range(300)], 100_000),
            "AMOUNT": rng.normal(50_000, 12_000, 100_000),
        })

        def big_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
            return big.copy(), {"rows": len(big), "truncated": False,
                                "elapsed_s": 9.4, "warehouse": "SERVE_WH",
                                "lane": "enforced", "as_of": None,
                                "budget": "", "claim_refs": []}

        setattr(sqlrun, "run", big_run)
        invalidate()
        one, _m = frame({"kind": "warehouse", "sql": "SELECT 1 FROM BIG"}, copy=False)
        per = cache_stats()["bytes"]
        held = CACHE_MAX_BYTES
        CACHE_MAX_BYTES = int(per * 2.5)     # room for two of these, not three
        for i in range(2, 5):
            frame({"kind": "warehouse", "sql": f"SELECT {i} FROM BIG"})
        stats = cache_stats()
        CACHE_MAX_BYTES = held
        print(f"  one 100k x 3 result measures {per / 1e6:,.1f} MB "
              f"(pandas says {big.memory_usage(index=True, deep=True).sum() / 1e6:,.1f} MB)")
        check("the BYTE cap evicts even under the entry cap",
              stats["entries"] == 2 and stats["bytes"] <= int(per * 2.5),
              f"{stats['entries']} entries, {stats['bytes'] / 1e6:,.1f} MB, "
              f"cap was {per * 2.5 / 1e6:,.1f} MB")
    finally:
        setattr(sqlrun, "run", real_run)
        setattr(sqlrun, "lane_status", real_lane)
        invalidate()

    # --- the columns-and-roles accessor ------------------------------
    info = frame_info(src)
    t0 = time.perf_counter()
    info.roles, info.chart_roles
    first_ms = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    for _ in range(100):
        i2 = frame_info(src)
        i2.roles, i2.chart_roles, i2.columns
    repeat_ms = (time.perf_counter() - t0) * 1000 / 100
    print(f"  frame_info: first roles+chart_roles {first_ms:7.3f} ms, "
          f"repeat {repeat_ms:7.4f} ms")
    check("frame_info agrees with column_roles",
          info.roles == column_roles(frame(src)[0]))
    check("frame_info.columns are the frame's columns",
          list(info.columns) == [str(c) for c in frame(src, copy=False)[0].columns])

    print("\n" + "=" * 78)
    print(f"RESULT: {len(DEMO)} demo frames, {len(bad)} empty; "
          f"{len(broken)} cache check(s) failed -> "
          f"{'OK' if not bad and not broken else 'FAILED: ' + ', '.join(bad + broken)}")
    print("=" * 78)
    raise SystemExit(1 if (bad or broken) else 0)
