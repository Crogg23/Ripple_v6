# THE BENCH — build spec

**Status:** design locked 2026-08-04. Skeleton in progress.
**Read [ATLAS.md](ATLAS.md) first** — it is the map this app is a UI for.

---

## 0. What it is, in one paragraph

A local Dash app with three panes. **Left:** all 144 chart types from
[wall.py](wall.py), grouped by the question they answer. **Middle:** your chart,
live, off real warehouse data. **Right:** every knob Plotly exposes for *that*
chart type, auto-generated from Plotly's own validators, grouped into the six
buckets from ATLAS §1.1, tiered so the 20 you actually use are on top.
**Bottom:** the Python that produced the chart — and it is **two-way**. Turn a
knob, the line appears in the code. Edit the code, the knob moves.

Power BI's visualization pane + format pane, with the code never hidden.

---

## 1. Why two-way, and where it honestly breaks

**Why:** a one-way clicky panel is a black box. The whole point is that Chris
learns Plotly by watching the code change under his hands. Read-only code
teaches half as much.

**Where it breaks — say this out loud, don't paper over it.**
Parsing arbitrary Python back into knob state is not solvable in general. So:

- The code panel is always **rendered in a canonical form** (§5).
- Editing is parsed with `ast` against that canonical form.
- If the edit still parses → knobs update, sync holds.
- If the edit does NOT parse into canonical form → the app enters
  **CUSTOM mode**: the chart still renders (we exec the code), the knob panel
  greys out with a one-line banner *"custom code — knobs are read-only until you
  Reset"*, and a Reset button returns to canonical.

CUSTOM mode is a feature, not a failure. It is the escape hatch that means the
UI can never become a ceiling.

---

## 2. Module map

Each module is independently testable. `app.py` is the only one that imports Dash.

| Module | Owns | Must not import |
|---|---|---|
| `bench/knobs.py` | introspect Plotly → a typed, tiered knob tree | dash, snowflake |
| `bench/controls.py` | knob → Dash control component | snowflake |
| `bench/codegen.py` | spec dict ⇄ canonical Python source | dash, snowflake, plotly |
| `bench/data.py` | where the DataFrame comes from (demo or warehouse) | dash |
| `bench/registry.py` | the 144 chart templates, selectable | dash, snowflake |
| `bench/app.py` | the three panes, callbacks, wiring | — |

---

## 3. The one state object

Everything is derived from this. It is JSON-serialisable so it can live in a
`dcc.Store`, be saved to disk, and be diffed.

```python
SPEC = {
    "chart":  "bar",                 # registry key (§6)
    "source": {                      # §7
        "kind": "warehouse",         # "demo" | "warehouse"
        "sql":  "SELECT ...",        # when kind == "warehouse"
        "name": "entity_count",      # when kind == "demo"
    },
    "mapping": {                     # bucket 1 — DATA. column names.
        "x": "STATE", "y": "TOTAL", "color": None, ...
    },
    "knobs": {                       # buckets 2-6. dotted paths -> values.
        "layout.barmode": "group",
        "layout.xaxis.categoryorder": "total descending",
        "trace.marker.opacity": 0.8,
    },
    "custom_code": None,             # str when in CUSTOM mode, else None
}
```

Rules:
- `knobs` holds **only non-default values.** A knob at its default is absent.
  This is what keeps the generated code short and readable.
- Paths are prefixed `layout.` or `trace.` — nothing else.
- `mapping` is separate from `knobs` because it is the one bucket whose legal
  values come from *the data*, not from Plotly.

---

## 4. `knobs.py` — the generator

**The core idea: nobody hand-writes 2,488 controls. Plotly describes itself.**

Confirmed working on plotly 6.9.0 (this install):

```python
go.Bar()._valid_props                      # -> set of property names
go.Bar()._get_validator("orientation")     # -> EnumeratedValidator
validator.values                           # -> ['v', 'h']   (enums only)
type(validator).__name__                   # -> the control to render
```

### 4.1 Validator → control type

| Validator | Control | Notes |
|---|---|---|
| `EnumeratedValidator` | dropdown | options come from `.values`; drop non-str/bool oddities |
| `BooleanValidator` | toggle | |
| `ColorValidator` | color picker + hex text box | both, always — hex is how you learn |
| `NumberValidator` | slider **or** number box | slider when `.min`/`.max` both present, else box |
| `IntegerValidator` | number box, step 1 | |
| `StringValidator` | text box | |
| `AngleValidator` | number box, -180..180 | |
| `FlaglistValidator` | multi-select | `.flags` gives the options |
| `CompoundValidator` | **expandable sub-section** | recurse into it |
| `DataArrayValidator` | dropdown of **the current df's columns** | this is the `mapping` bucket |
| `AnyValidator` | text box | last resort |
| `LiteralValidator` | **skip** | read-only, e.g. `type` |
| `SrcValidator` | **skip** | ATLAS §5.3 — 18% pure noise |
| `SubplotidValidator` | **skip** | subplots are §9, not a knob |

### 4.2 Bucket assignment

Every knob path maps to exactly one of the six ATLAS buckets. Assignment is by
path prefix, table-driven, in `knobs.BUCKETS`:

- **DATA** — `trace.x`, `trace.y`, `trace.z`, `trace.color`, `trace.values`,
  `trace.labels`, `trace.parents`, `trace.text`, any `DataArrayValidator`
- **MARK** — `trace.marker.*`, `trace.line.*`, `trace.fill*`, `trace.opacity`,
  `trace.textposition`, `trace.orientation`, everything else trace-side
- **SCALE** — `layout.{x,y}axis.*`, `layout.coloraxis*`, `layout.*colorway`,
  `layout.polar/geo/scene/ternary/map/smith`
- **FRAME** — `layout.title*`, `.legend*`, `.margin*`, `.font*`, `.annotations`,
  `.shapes`, `.images`, `.paper_bgcolor`, `.plot_bgcolor`, `.width`, `.height`,
  `.template`, `.showlegend`, `.grid`, `.uniformtext`
- **INTERACTION** — `layout.hover*`, `.click*`, `.drag*`, `.select*`,
  `.modebar`, `.updatemenus`, `.sliders`, `.spikedistance`, `.newshape`
- **MOTION** — `layout.transition*`, frames

Anything unmatched falls to FRAME and is **logged**, so gaps get found instead
of silently swallowed.

### 4.3 Tiers

- **Tier 0** — the 20 named in ATLAS §4.1, verbatim, plus the chart type's own
  DATA knobs. **Always visible, always expanded.**
- **Tier 1** — depth ≤ 2. Behind "show more" per bucket.
- **Tier 2** — depth ≥ 3. Behind "show everything".
- A **search box** over all knob paths + descriptions cuts every tier. This is
  the real answer to "I know there's a setting for X."

### 4.4 Descriptions

Plotly's own `validator.description()` is useless prose
(*"The 'hovertemplate' property is a string and must be specified as..."*).
So:

1. Tier 0 uses the **hand-written half-sentences already in ATLAS §4.1** —
   import them, don't retype them.
2. Everything else falls back to a **cleaned** `description()`: strip the
   boilerplate prefix, keep the legal-values list, cap at ~160 chars.
3. A knob with no usable description shows its path only. Never invent text.

### 4.5 Public API

```python
knobs.tree(chart_key: str, columns: list[str]) -> KnobTree
# KnobTree: {bucket: {tier: [Knob]}}
# Knob: path, label, control, options, min, max, default, description, depth

knobs.default(path: str) -> Any      # for "is this knob at default?"
knobs.validate(path, value) -> (ok, coerced_or_error)
```

---

## 5. `codegen.py` — canonical form

Given a SPEC, emit exactly this shape. Deterministic, stable ordering, no
cleverness — the whole two-way contract rests on it being predictable.

```python
# --- data ---------------------------------------------------------
df = bench.data.frame(...)          # the source line, from SPEC["source"]

# --- chart --------------------------------------------------------
fig = px.bar(df, x="STATE", y="TOTAL")      # mapping only

# --- MARK ---------------------------------------------------------
fig.update_traces(marker_opacity=0.8)

# --- SCALE --------------------------------------------------------
fig.update_layout(xaxis_categoryorder="total descending")

# --- FRAME --------------------------------------------------------
fig.update_layout(barmode="group", template="plotly_dark")

fig.show()
```

Rules:
- One `update_traces` / `update_layout` call **per bucket**, in fixed bucket
  order (MARK, SCALE, FRAME, INTERACTION, MOTION). A bucket with no non-default
  knobs emits nothing — not an empty call, not a comment.
- Use **underscore flattening** (`xaxis_categoryorder=`), not nested dicts.
  Shorter, and it is what Plotly's own docs use.
- Every emitted section carries its bucket name as a comment. That comment is
  the reader's map back to ATLAS.

### 5.1 Parsing back

```python
codegen.render(spec) -> str
codegen.parse(src)   -> spec | None     # None => CUSTOM mode
```

`parse` walks the `ast`. It accepts exactly the canonical shape above.
Anything else returns `None` and the app goes to CUSTOM. **`parse` must never
raise** — a malformed edit is a return value, not an exception.

---

## 6. `registry.py` — the 144 templates

Do not re-derive the chart list. [wall.py](wall.py) already holds all 144 with
`section / name / call / shape / use_when` metadata on a `Chart` dataclass.

`registry.py` imports that metadata and adds, per chart:

- `key` — stable slug (`sankey`, `ridgeline`, `bump_chart`)
- `builder(df, mapping, knobs) -> go.Figure` — the actual construction
- `required` / `optional` mapping slots, with the column **role** each needs
  (numeric / category / date / geo) so the picker can grey out charts that
  can't be drawn from the current df — and say *why*
- `trace_type` — which `go.<Trace>` to introspect for the MARK bucket

**Grey-out-with-a-reason is required.** "Sankey needs a source column, a target
column, and a value column — this result has no second category column" teaches
more than a disabled button.

---

## 7. `data.py` — the seam

The Bench takes a DataFrame. It does not care where it came from. This is the
single function that makes the skeleton complete on fake data and the warehouse
wiring a swap, not a rewrite.

```python
def frame(source: dict, *, refresh: bool = False,
          copy: bool = True) -> tuple[pd.DataFrame, dict]:
    """source == SPEC['source']. Returns (df, meta)."""
```

- `kind == "demo"` → the generators already in [wall.py](wall.py). No network.
- `kind == "warehouse"` → **`viz.sqlrun.run(sql, limit_rows)`**, unchanged.
  That module is the guarded read lane: text guard, claim-table block,
  single-statement execution, verified read-only lane, row/cell caps, 300s
  timeout, SERVE_WH → COMPUTE_WH. It is plumbing, not a viz tool. **Do not
  reimplement it and do not route around it.**
- `meta` carries `rows`, `elapsed_s`, `truncated`, `lane`, `as_of`. The lane and
  the "data as of" stamp are **shown in the UI**, always.

Table/column discovery for the SQL box reuses `viz/catalog.py` rather than a
hardcoded list — since 2026-08, through a disk snapshot (`bench_catalog.json`,
written by `catalog.snapshot_write`), so browsing costs zero warehouse queries.
Exactly three catalog actions touch Snowflake, each behind its own labelled
button: `refresh catalog` (two live queries), picking a row (`DESCRIBE`,
metadata only), and `draft starter SQL` (the 10k-row profile, cached 7 days —
it used to run silently on every pick; it does not any more).

### 7.1 The frame cache

Every knob turn repaints the figure, and repainting needs the frame again.
Un-cached that is a live Snowflake round trip per knob turn — a bare `SELECT 1`
measured at 9.4s on this box. So `frame()` keeps its answers, keyed on a hash of
the whole source dict.

```python
frame(source)                    # cached; a repeat is a dict lookup
frame(source, refresh=True)      # bypass and REPLACE — what RUN passes
frame(source, copy=False)        # the cached frame itself. read-only
frame_info(source) -> FrameInfo  # .columns .rows .roles .chart_roles .roles_line
invalidate(source) / invalidate()
cache_stats()
```

Rules, all of them measured or load-bearing:

- **The result is cached, never the guard.** A real fetch always goes through
  `viz.sqlrun` in full. Nothing remembers a lane, a permission or a refusal
  *decision* — only the answer, against the exact source that produced it.
- **Bounded, LRU:** `CACHE_MAX_ENTRIES = 8`, `CACHE_MAX_BYTES = 256 MB`. A
  100k-row result is a real thing the read lane will hand you.
- **A cached hit says so.** `meta` survives whole — `lane`, `rows`, `truncated`,
  `as_of`, and the **original** `elapsed_s` — plus `cached=True`,
  `cache_age_s` and a note. The status bar never implies a query it did not run.
- **Thread-safe.** Two callbacks asking for one source at the same moment
  produce one fetch, not two; the cache lock is never held across a fetch.
- **Failures are cached too**, so a dead connection is not re-dialled on every
  knob turn. `refresh=True` — the RUN button — is the way back.

`frame_info` exists because the picker re-derives column roles on every single
repaint: 9.7ms (`column_roles`) + 4.1ms (`registry.roles`) on a 100k-row result,
for an answer that cannot have changed. It is derived once per frame and kept
with it.

---

## 8. `app.py` — layout and callbacks

```
┌──────────────┬──────────────────────────┬──────────────────┐
│ PICKER       │ CHART                    │ KNOBS            │
│ search box   │ [ live figure ]          │ search box       │
│ ▸ COMPARE    │                          │ ▾ DATA (open)    │
│ ▸ DISTRIBUTE │                          │ ▸ MARK           │
│ ▾ FLOW       │                          │ ▸ SCALE          │
│    sankey ◀  │                          │ ▸ FRAME          │
│ ... 144      │                          │ ▸ INTERACTION    │
│              ├──────────────────────────┤ ▸ MOTION         │
│              │ CODE (editable)  [Reset] │  [show more]     │
└──────────────┴──────────────────────────┴──────────────────┘
   source bar: [demo ▾ | SQL...]     lane: enforced   data as of: ...
```

Callback graph — one direction of truth at a time, guarded by
`dash.callback_context` so the two-way sync cannot loop:

1. picker click → SPEC.chart → re-render knob panel + code + figure
2. knob change → SPEC.knobs → re-render code + figure (**not** the knob panel)
3. code edit (debounced ~600ms) → `codegen.parse` → SPEC or CUSTOM → figure
4. source change → new df → re-render everything (mapping revalidated against
   new columns; invalid mapping slots clear and say so)

### 8.1 One writer, three readers

`sync_spec` is the only callback that writes `SPEC`. Everything on screen is
derived from it by **three** render callbacks, split by what they cost:

| lane | owns | measured — rebuilding / guarded |
|---|---|---|
| `render_chart` | figure, code box, status bar, build message, code mode | 1.4–10.3 ms, 5.8–38.6 KB — always runs |
| `render_knobs` | the right-hand pane | 6.1 ms, 78 KB lazy / 0.01 ms, 0 KB |
| `render_picker` | the 145 chart buttons | 3.9 ms, 133.6 KB / 0.01 ms, 0 KB |

It was one callback with eight Outputs. Dash returns a callback's outputs
together, so the figure — 1.3 ms to build, 2.5 KB on the wire — could not
appear until the knob pane had finished: **268 ms and 4,128 KB for a chart
click, 94% of it the pane.** Splitting is the fix. Nothing else changes: the
three lanes read the store and never write it, so there is no cycle at all.

**The gesture, end to end, over HTTP** — `bench/e2e.py` starts a real server
and times from the click leaving to the figure being read back, with the three
lanes fired together on separate sockets the way a browser fires them. Median
of 31, against the old shape rebuilt around today's builders:

| gesture | before | after |
|---|---|---|
| click a chart | **331 ms** (668 KB up, 4,129 KB down) | **16 ms** (24 KB up, 6 KB down) |
| turn a knob | **63 ms** (668 KB up, 310 KB down) | **26 ms** (24 KB up, 6 KB down) |

The fan-out costs two more round trips and they do **not** land on the critical
path: the figure is back 3–9 ms after `sync_spec` answers, while the pane and
the picker are still in flight. What is left of a knob turn is 6.5 ms of
`plotly.express` building the figure and the dev server's own 0–15.6 ms
Windows scheduler tick — neither of which is this app's wiring.

The echo (rule 2 of the no-loop contract) is **two stores**, one per writer —
`bench-echo` holds the code text, `bench-knob-echo` holds the widget values.
Two callbacks firing from one Input at the same instant cannot clobber each
other's record of the screen if they do not share one.

### 8.2 The knob pane is lazy

`controls.accordion(..., lazy=True, opened=...)`. A first paint materialises
Tier 0 and nothing else: 39 knob rows and 87 KB instead of 1,895 rows and
3,808 KB. Tier 1 and Tier 2 are not hidden behind a shut `<details>` — they
do not exist as components, which is the only thing that stops them being
serialised into the layout, into every repaint, and into every
pattern-matching Input payload (668 KB of request body per knob turn).

`bench-open` holds the open tokens plus the pane they belong to; `grow_open`
is its only writer, and a token set stamped with a different chart reads as
empty rather than being reset by a second writer that could race the first.
**Search ignores it entirely** — it reads the tree, so every knob in every
tier is one box away.

### 8.3 A click on a row is not a click on a bucket

`html.Details` renders `<details onClick={n_clicks + 1}>` and React's onClick
bubbles, so opening the `mapping.x` dropdown fires `n_clicks` on the bucket
wrapped around it. At `grow_open` that is indistinguishable from clicking the
bucket header, and acting on it rebuilds the pane — replacing the dropdown
whose menu just opened. **Measured: 314 components and 81.6 KB in, the same
314 and 81.6 KB out. The menu shut, the click did nothing, the second click
worked.** That is exactly what "you can't tell if it's broken" feels like.

Two guards, and each is a statement about the code rather than a heuristic:

- `app.materialisable(spec)` names the bucket tiers that hold knobs, so a
  token for an empty one is dropped. That is DATA, always — `knob_tree`
  replaces Plotly's DATA bucket with the chart's own mapping slots at Tier 0
  and nothing behind them — and DATA is the one bucket open on a first paint.
  Cached per chart, because which tier a knob lands in is decided by path,
  bucket and depth and by nothing about the data.
- **While a search is on, `grow_open` returns `no_update` and `render_knobs`
  leaves `opened` out of its signature.** A search draws no tier expanders at
  all, so every bucket id on screen under one is a `<details>` a row click
  bubbled to, and `controls.accordion` cannot read `opened` during a search
  anyway.

### 8.4 An error must not be sticky

Both slow lanes skip their work when the state matches the signature of what
they last drew. On the error path they must **clear** that signature, not leave
it — `render_knobs` writes `{"knobs": {}, "sig": None, "vals": None}` and
`render_picker` writes `None`. Keeping it meant the red box was a trap: come
back to the state that drew fine, it matched, nothing was rebuilt, and the
error sat where the knobs should be with a working chart beside it.

Non-negotiable UI rules:
- The lane badge (`enforced` / `client-guard`) is **always on screen.**
- Row count + truncation warning always on screen.
- A knob at its default renders greyed; changed knobs render highlighted. You
  should be able to see at a glance what you have actually touched.
- **Slow must read as working, never as broken.** `dcc.Loading` wraps the
  figure and the knob pane and shows at 250 ms; the RUN button disables itself
  and says `RUNNING SQL…` for as long as the query is in flight.
- **An error is on the screen.** Every render lane catches, prints the full
  traceback to the terminal and puts one readable line in its own pane. A
  blank pane with the reason only in a server log is the failure this app was
  reported for. And you can get back OUT of it — §8.4.
- **A click never gets eaten.** No gesture may rebuild a pane into the same
  pane. A rebuild replaces the widget under the cursor, so a rebuild that
  changes nothing is worse than no rebuild at all — §8.3.

---

## 9. Explicitly out of scope for v1

Named so they are decisions, not omissions:

- subplots / `make_subplots` (ATLAS §6.1)
- animation frames (ATLAS §6.3)
- multiple traces on one figure
- ~~saving/loading specs to disk~~ *(shipped in the 2026-08 sweep — §11)*
- ~~PNG export~~ *(shipped: browser-side via the modebar camera at 2x; kaleido
  is still not installed and still not needed — §11)*

Each is additive later. None changes the state object.

---

## 10. Done means

1. `python bench/app.py` opens the three panes.
2. Pick any of the 144 → it renders on demo data or says exactly why it can't.
3. The knob panel is generated, never hand-written, and tiered.
4. Turning a knob updates chart **and** code.
5. Editing the code updates chart **and** knobs — or drops to CUSTOM cleanly.
6. Warehouse mode runs real SQL through `viz.sqlrun` with the lane badge visible.
7. Tests cover: knob generation for ≥20 trace types, codegen round-trip
   (`parse(render(spec)) == spec`) over a spec battery, and CUSTOM-mode fallback
   on deliberately malformed code.


---

## 11. The 2026-08 improvement sweep (addendum)

Everything below was added after v1 shipped. The v1 contracts above all still
hold — one spec writer, the echo rules, the codegen shape, `viz.sqlrun` as the
only warehouse door. New contracts:

**`codegen.parse_why(src) -> (spec | None, reason)`.** `parse` is unchanged
(never raises, `None` means CUSTOM). `parse_why` is the same walk but a failure
carries a sentence naming the line that broke canonicality ("line 4: only
fig.update_traces / fig.update_layout / fig.show() are canonical"). The CUSTOM
banner prints it.

**Export.** The code-panel header has copy (dcc.Clipboard), `.py` (the panel
text as a runnable file), `html` (`fig.to_html`, standalone interactive page)
and `save` (the SPEC as `.json`). PNG is the modebar camera at scale 2 —
browser-side, no kaleido. All downloads share one `dcc.Download` behind the
`export_chart` callback.

**History and persistence — still one writer.** `sync_spec` gained two more
Outputs: `bench-history` ({"past": [...], "future": [...]}, cap 50) and
`bench-persist` (`storage_type="local"`, a mirror of every spec write). Undo /
redo / load (dcc.Upload of a saved .json) / the restore request are four more
Inputs on `sync_spec`; nothing else writes the spec, the history, or the
mirror. On page load a clientside callback copies `bench-persist` into
`bench-restore-req` exactly once (a window flag makes later mirror writes
inert), and `sync_spec` validates it through the same gate as a file load: the
chart must be in the registry and a canonical spec must survive `render_code`.

**Deferred warehouse sources.** A restored or file-loaded spec whose source is
warehouse SQL gets `source["deferred"] = True`. `bench.data` answers that with
a refusal in the new `"idle"` lane ("restored SQL has not run this session —
press RUN") instead of touching Snowflake. RUN builds a fresh source dict
without the flag, which is the human asking.

**A picker click no longer nukes the knobs.** Knobs the new chart also has
(checked with `knobs.validator_for`) carry over; the rest are dropped and
named in the message line. Layout knobs are universal — `go.Layout` is one
class shared by every trace — so they always carry.

**The compound editor.** `layout.annotations` and `layout.shapes` (and only
those — `knobs.COMPOUND_EDITOR_PATHS`) render as controls' `"compound"`
editor: one bordered group per row with the fields that matter, plus add /
per-row remove buttons (`{"bench": "knobrow", ...}` ids, their own Input
pattern on `sync_spec`, because a button has no `value` prop). Row field
widgets use indexed knob paths — `layout.annotations[0].text` — and
`_apply_knobs` folds them back into the parent list. The SPEC value stays a
plain list of dicts, so codegen and the figure builder needed no changes. New
rows default to paper refs so they draw on any chart immediately.

**Keyboard.** Ctrl+Z / Ctrl+Y undo/redo (only outside text boxes — native
undo stays native), Ctrl+S saves the spec, Ctrl+Enter in the SQL box is RUN.
Synthesised clicks on the real buttons; no second server surface.

**`bench/settings.py`.** Every tunable number, env-overridable:
BENCH_DEBOUNCE_MS, BENCH_SPINNER_MS, BENCH_CUSTOM_TIMEOUT_S, BENCH_PORT,
BENCH_SQL_LIMIT, BENCH_TABLE_CAP, BENCH_DEBUG (=1 turns on Dash hot reload).
Stdlib-only, importable without Dash.

**Error visibility.** The catalog helpers in `data.py` record
`LAST_CATALOG_ERROR` (and log) instead of silently returning `[]`, so the
source bar can say *offline* vs *broken*. The custom-code deadline tracer is
ast-gated: straight-line code skips `sys.settrace` entirely; anything with a
loop / comprehension / def keeps the 5s guard (known gap: loop-free recursion
built via exec-inside-exec escapes it; CPython's recursion limit catches the
plain kind).
