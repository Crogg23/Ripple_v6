---
name: bench-plotly-workbench
description: "2026-08-04 — the Bench shipped (bench/), replacing four forgotten viz tools; why it exists and what's left"
metadata: 
  node_type: memory
  type: project
  originSessionId: b318dc10-f1b8-4525-aa1f-73cd98243cfc
  modified: 2026-08-05T05:14:00.920Z
---

Built 2026-08-04. `bench/` is Chris's Plotly workbench — a Dash app at
http://127.0.0.1:8051 (`python bench/app.py`, port 8051 not 8050).

**Why it exists.** The repo already had four viz surfaces (`ripple chart` CLI,
`viz/plugs.py`, `playground/workbench.ipynb`, the Playground Dash app). Chris had
forgotten all of them existed — every card under `investigations/` was made on a
single day, 2026-07-03. He retired them all. The real problem was never "can't
write Plotly," it was **"I don't know what I don't know"** — `plugs.py` capped him
at 10 chart types out of ~139 Plotly can make. See [[connection-lenses]] for what
the charts are ultimately for.

**The organizing idea that made it tractable:** it is not 45 charts × 2,488
options. Every Plotly setting falls in one of six buckets — DATA, MARK, SCALE,
FRAME, INTERACTION, MOTION — and four of the six live on `layout`, identical
across every chart type. Learn ~200 once, then a new chart costs ~60. The knob
panel is **generated** from Plotly's own validators (`_valid_props` /
`_get_validator`), never hand-written, so it can't go stale.

**Design calls Chris made (don't relitigate):**
- Two-way code sync, not a clicky black box — matches [[user-hybrid-learning-preference]].
- Wired to the real warehouse, not demo-only.
- `viz/sqlrun.py` is plumbing, not one of the retired viz tools — reused, never
  routed around. Verified live: lane `enforced`, role RIPPLE_READER, DROP refused.

**Artifacts:** `bench/SPEC.md` (the build spec — read before changing anything),
`bench/ATLAS.md` (the Plotly map), `bench/wall.py` (139 charts on one page; needs
`--offline` or it pulls plotly.js from CDN).

**Open:** `wall.py` has no test — its build prints "failures: none" while
proving only that figure objects got constructed, not that any draw.
Warehouse wiring beyond the smoke test is unexercised. `pip install scipy
statsmodels scikit-image plotly-geo` unblocks 6 charts (PNG export no longer
needs kaleido — browser modebar does it at 2x).

**Perf sweep (2026-08-04, same day, later session).** `bench/perf.py` and
`bench/e2e.py` are the two benchmarking tools (not tests — safe to edit).
A prior pass had already split the render callbacks into fast/slow lanes and
made the knob pane lazy (see `perf-baseline.json` vs `perf-after.json`). A
follow-up independent sweep found `knobs.tree()` was rebuilding ~2,000 Knob
objects from scratch on every call even though its own `_raw_tree` helper was
already cached — fixed by adding a correctly-designed cache layer underneath
(Knob is `@dataclass(frozen=True)`, so sharing objects across calls is safe;
the outer dict/list containers are still rebuilt fresh every call, since
`app.py`'s `knob_tree()` mutates them in place). Also removed a
threading-lock dance in `app.py`'s `render_code()` (replaced with a plain
keyword arg to `codegen.render`). Result: all three `e2e.py` gestures ~30%
faster, `knobs.tree()` warm calls ~100-300x faster, 1891 tests still pass.
Two proposed wins were investigated and rejected as unsafe without editing
tests — see [[feedback-verify-agent-research-against-tests]] for the general
lesson from that.

**UI restyle (2026-08-04, after Chris said "everything's the same color").**
Five commits (bc38df0f..c392a556): BG_0..BG_3 elevation scale in controls.py
(SURFACE/PANEL/PANEL_2 are now aliases), `controls.css_vars()` generates a
`:root{--bench-*}` block inlined via index_string, and `bench/assets/bench.css`
holds every selector in var() form — colours live ONLY in controls.py. Six
bucket hues (validated with the dataviz skill's validator) paint each bucket's
stripe/dot via `bench-bucket--<name>` classNames; save/RUN are filled accent
primaries; chips get tinted backgrounds; chart card = BG_1. **Key trap fixed:
Dash 4.4.1 dropdowns render `.dash-dropdown` markup, not react-select
`.Select-*` — the old PANEL_CSS silently no-op'd and every open dropdown menu
was a white box.** Restarting the 8051 server needs a verified kill
(Stop-Process on the port owner, confirm nothing still listens) — a failed
silent restart left a stale server serving old wall.py during verification.

**Catalog overhaul (2026-08-04, Chris: "free text to search a billion tables?
are you kidding?").** Commit 456b17d1. The term-box/look-up/bare-FQN picker is
gone. Replaced with a browse-first drawer served from a disk snapshot
(`outputs/bench_catalog.json`, `catalog.snapshot_write/read` in viz/catalog.py):
domain shelves with table counts + row volumes, filter-within, rich rows
(friendly name, one-liner, FQN, row count, lifecycle/SAMPLE badges). Browsing
never touches Snowflake. Exactly three labelled warehouse actions: `refresh
catalog` (2 queries), row pick (DESCRIBE, metadata-only — works even with the
warehouse suspended), `draft starter SQL` (the 10k-row profile that used to run
SILENTLY on every pick — now explicit, shows the budget line after). Every
warehouse touch writes a ⚡ activity line to bench-src-note. Current snapshot is
seeded from outputs/thelibrary_inventory.json (428 tables, honest 2026-07-29
built_at) because a live rebuild was blocked — see the SERVE_MON note below.
Callback count is now 11 server + 2 clientside; tests/test_viz_catalog_snapshot.py
guards snapshot purity (read never connects, write is atomic).

**BLOCKER (2026-08-04 evening): SERVE_MON resource monitor exceeded its quota —
SERVE_WH refuses to resume.** All bench RUN / refresh / profile paths are dead
until the monitor resets or Chris raises the quota (his call — real money).
Metadata ops (DESCRIBE) still work. Also: tests/test_connect_incremental.py::
test_incremental_state_matches_full_rebuild_backstop fails on clean main
(keyset drift a-b=80397, b-a=56451856) — pre-existing, unrelated to the bench.

**Improvement sweep (2026-08-04, Chris approved all four packages).** Six
commits, ~1,950 bench tests green, perf flat vs baseline. Shipped: (1)
`codegen.parse_why` — bad code edits name their line in the CUSTOM banner;
copy button, .py/HTML/spec-.json export, 2x PNG via modebar; (2) catalog
`LAST_CATALOG_ERROR` (offline vs broken), ast-gated custom-code tracer
(straight-line code skips settrace), `bench/settings.py` (BENCH_* env vars,
BENCH_DEBUG=1 = hot reload), oldshape.py deleted; (3) undo/redo (cap 50) +
save/load + localStorage restore on F5 — restored warehouse SQL is marked
`deferred`, answers "press RUN" in a new "idle" lane, never auto-queries
Snowflake; picker clicks carry over knobs instead of nuking (layout knobs
are universal, trace knobs drop with a message); Ctrl+Z/Y/S, Ctrl+Enter=RUN;
(4) real add/remove editor for layout.annotations/shapes (indexed knob paths
fold into a plain list — codegen untouched). SPEC.md §11 documents the new
contracts. sync_spec now has 5 outputs / more inputs — perf.py and every
test harness that fakes it were updated to match.
