# GO BILLS — Orbital Atlas v2 handoff

Paste this whole file as the opening prompt of a new Claude Code session, started in the Ripple_v6 repo. Written 2026-09-19.

---

## Your role

You are the builder on Orbital Atlas v2. The recon phase is finished, the decisions are made, and two of eight build slices are done and verified. **Your next job is slice 2.** Do not reopen decisions unless Chris asks.

Read these three files before anything else, in this order:

1. `orbital_atlas/docs/07_BUILD_SPEC.md` — the plan, the slices, the standing rules
2. `orbital_atlas/docs/06_DECISIONS_NEEDED.md` — all twelve answers, with who made each
3. `orbital_atlas/docs/03_CONFIG_SCHEMA.md` — the view and theme schemas slice 2 and 3 implement

Then run the checks in "Prove it still works" below. If they do not pass, fix that first.

## What this is

One rendering engine that shows any place-keyed table as a map, where every "version" of the map is a row of JSON config, not a code change. Counties today, census tracts per state on drill-down, a warehouse feeding it later. The original brief is `orbital_atlas/CLAUDE_CODE_PROMPT.md`. Its non-negotiables still bind:

- **The data contract:** one flat table, seven columns — `geo_id, geo_type, period, value, denominator, n, tier`. The source never sends a rate. The engine divides.
- **Three concerns, never mixed:** engine, view, theme. View says what the map means. Theme says how it looks. Both are plain JSON.
- **Motion:** nothing moves on its own. Only in response to a user action, once, fast, no loops.
- **Honesty by default:** raw and normalized always reachable; low-confidence places markable; the legend generated from the real scale, never typed by hand.

## Decisions, all closed

| # | Decision | Answer | Who |
|---|---|---|---|
| 1 | Print | none; a saved image is enough | Chris |
| 2 | Smallest shapes | counties nationally; tracts per state on drill-down; about 9,000 shapes on screen at most | Chris |
| 3 | 3D | someday, not now; keep the painter swappable | Chris |
| 4 | Framework | none | Chris |
| 5 | Language | plain JavaScript, ES modules, type notes in comments, no build step | Claude |
| 6 | Configs | JSON files now, flat enough to be warehouse rows later | Claude |
| 7 | Layer header | yes: label, units, format strings travel with the table | Claude |
| 8 | Duplicate rows | reject and report by default; `sum` and `last` per load | Claude |
| 9 | County vintage | current-year file as default, 2018 kept, alias table for CT and AK | Claude |
| 10 | Encoding | lives in the theme; engine refuses size encodings on rates | Claude |
| 11 | Slicers | `setView` call first, optional control component second | Claude |
| 12 | Architecture | A: plain core + `<orbital-atlas>` web component | follows from 4 |

"Claude" rows can be flipped by Chris before their slice starts.

## The one hard wall

```
rows + header -> LOADER -> clean table + load report
                               |
view.json  ->  ENGINE: scale, roles, frame, legend, readout, events
theme.json ->      |
topology   ->   draw list (plain data)  ->  PAINTER  ->  canvas
```

**Only `src/painter/` touches a canvas.** The engine emits a draw list: plain JSON-safe data saying what to fill and stroke. That wall is what makes a 3D painter a swap later. A test enforces it.

## What is built

| Slice | State | What exists |
|---|---|---|
| **0. Bones** | done, verified | `<orbital-atlas>` tag, topology registry, draw list, canvas painter, empty state. 3,142 counties render with the measured bounding box, so the Aleutians are in frame. |
| **1. Data in** | done, verified | Forgiving parser, strict loader, layer header, four adapters behind one interface, load report in plain words, demo page with paste box and four samples. Places with a value are lit; no colour scale yet. |
| 2. Honest colour | **next** | — |
| 3. Configs | not started | — |
| 4. Hands on | not started | — |
| 5. Drill-down | not started | — |
| 6. Around the map | not started | — |
| 7. Out | not started | — |

### File map

```
orbital_atlas/
  GO_BILLS.md               this file
  CLAUDE_CODE_PROMPT.md     the original brief
  docs/00..07               review, options, contract, schemas, render modes, candidates, decisions, build spec
  docs/img/                 slice screenshots
  reference/                v1 source and the 2018 topology, untouched
  src/topology/registry.js  decode a TopoJSON file using its registry entry; ids, parents, adjacency, meshes, measured bbox
  src/engine/drawlist.js    buildDrawList(topology, theme, {fills})
  src/engine/frame.js       fit(bbox, W, H, pad), project()
  src/engine/defaults.js    DEFAULT_THEME, DEFAULT_VIEW, overlay() for partial configs
  src/painter/canvas.js     CanvasPainter: setTopology, resize, paint(drawList, transform)
  src/loader/parse.js       text -> rows; delimiter sniffing, header detection, paste shorthand, NUMBER regex
  src/loader/load.js        loadRows(rows, {topology, header, onDuplicate, knownGeoTypes}) -> {header, table, report}; resolvePeriod()
  src/loader/report.js      describeReport(report) -> [{level, text}]
  src/adapters/sources.js   sources.paste / file / url / rows
  src/element/orbital-atlas.js   the tag: theme, view, ready, load(), clear(), events atlas-ready / atlas-load / atlas-error
  src/vendor/topojson-client.js  the only outside code, 7 KB, fetched from jsdelivr, makes no network calls
  configs/themes/ledger.json, configs/views/empty.json
  topologies/registry.json, topologies/us_counties_2018.topo.json
  demo/index.html           paste box, samples, duplicate policy dropdown, report panel; ?sample=ct|messy|full|minimal auto-loads
  test/slice0.test.js, test/slice1.test.js
```

### The table shape slice 2 will read

`loadRows` returns `table.byPeriod[period]` holding columns aligned to `topology.places` order:

- `has` Uint8Array — a row exists
- `value`, `denominator`, `n` Float64Array — `NaN` means no data, which is **not** zero
- `tier` Array of string or null

`resolvePeriod(table, 'latest')` gives the last period in sort order. `table.setAside` holds rows for other known geo_types, kept for drill-down.

## Prove it still works

```
cd orbital_atlas
node --test test/*.test.js                 # expect 26 pass, 0 fail
python3 -m http.server 8765                # then open http://localhost:8765/demo/index.html
```

Headless check, no clicking needed:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --virtual-time-budget=8000 --dump-dom "http://localhost:8765/demo/index.html?sample=messy" | grep -o "<title>[^<]*"
# expect: LOADED kept=2 unmatched=1 dupkeys=1 rejected=2
# ?sample=ct expects: LOADED kept=2 unmatched=5 dupkeys=0 rejected=0
```

ES modules and `fetch` do not work from `file://`. A local server is required for development.

## Slice 2 — what to build

From the spec: **scales with ties sharing a colour, a legend generated from the scale, a readout with value, denominator, ratio, and rank.**

Done means:
- Equal values get one colour. v1 spread ties across the palette in file order; that is the bug to not repeat.
- A quantile legend prints the word "percentile" and shows real cut values, with uneven spacing so it cannot be read as linear.
- When a denominator exists, value, denominator, and ratio are all reachable from the readout.
- Zero denominator shows the rate as no data. Never infinity, never zero.

Suggested shape, not binding:
- `src/engine/measure.js` — turn a period's columns plus `view.measure` into one Float64Array: `value`, `ratio` using `header.ratio.per`, `denominator`, `n`, `presence`.
- `src/engine/scale.js` — `linear`, `log`, `quantile`, `quantize`, `threshold`, `diverging`, `binary`, `categorical`; `ties: "share"`; `zero_class`; `invert`. Output: a position in 0..1 per place, plus a **legend model** as plain data.
- `src/engine/color.js` — hand-written palette interpolation, in a perceptual space if cheap.
- `src/engine/readout.js` — a readout model as plain data for one place: label, formatted numbers, rank "of N".
- Number formats are strings in the layer header. A small formatter needs vendoring or writing; d3-format was the candidate, size not yet checked.
- The legend and readout are DOM, drawn by the shell or a small component. They are not painter work.
- Replace `_fills()` in the shell, which today only lights places that have a value.

## Standing rules, each enforced by a test today

| Rule | Test |
|---|---|
| Only the painter touches canvas | greps every non-painter file for `getContext`, `Path2D`, `ctx` |
| No timers, no CSS animation, one animation-frame call site in the codebase | pinned by count; a new one must be argued for in the test |
| Engine is domain-free: no place names, state codes, or map-box numbers in `src/` | regex over `src/` |
| Draw list is plain data | must survive a JSON round trip |
| Every input row lands in exactly one report bucket | checked under `reject`, `sum`, and `last` |

Add to these as slices land. Do not weaken them.

## Traps already hit — do not repeat

| Trap | What happened | Rule now |
|---|---|---|
| **Decimal comma** | `48201;12,5` loaded as 125 and the report said all was well. My 24 tests passed; the skeptic found it. | A comma is only a thousands separator in groups of three. Anything else is refused and reported. |
| **2018 county list** | Connecticut planning regions `09110`–`09190` and Alaska `02063`, `02066` are not in the file. | The report lists unmatched ids and names the vintage. Alias table and a current-year file arrive in slice 5. |
| **The file's own bbox is loose** | TopoJSON `bbox` was off by about half a unit from the shapes. | Measure from the decoded shapes. Never trust a declared box, never assume 0 to 975. |
| **Row counts under `sum`** | `rows_kept` double-counted merged duplicates. | `rows_used` counts input rows that reached the table; `rows_kept` counts cells; `duplicates.dropped` counts rows lost. |
| **v1's ties** | Equal values got different colours, ordered by file position. | `ties: "share"` is the default in slice 2. |
| **v1's pick canvas** | Antialiased edges blend two id-colours into a third county's id. | Fix when the pick canvas is built in slice 4. |

## Known gaps, honest

- **No automated test looks at pixels.** The painter is proven by screenshots only. A pixel test lands with slice 4, when hover needs one anyway.
- Canvas blur in Safari is unchecked. It matters before any glow theme, slice 3.
- Source and year of tract boundary files are undecided. Slice 5.
- Library names and sizes in docs 01 and 05 are from memory, never checked.
- The demo page's side panel is host-side scaffolding, not part of the engine.

## How to work with Chris

The repo's `CLAUDE.md` and the scannable output style govern every message. The short version:

- Lead with the answer. Headline as a fact, a fenced numbers block, three to five capped bullets, one bold arrow line. One screen.
- Plain words, short lines, no parentheses in chat. Explain it like telling a sharp friend at a bar.
- **One question at a time.** If he says "idk", explain it in everyday terms and recommend one option with the reason.
- He directs, you figure it out. Make mechanical calls silently and say which you made. Do not lecture on method.
- Say "done" only after running the thing that could prove it wrong. **Every done gets a fresh-context skeptic pass** with his words verbatim. If the skeptic disagrees, show him both verdicts.
- Before code: one line naming the adjacent thing it can break, or "nothing adjacent."
- Commit or push only when he asks. Nothing gets published without his explicit yes.
- Answers go in chat. Receipts and long tables go in a file, with one link.

## Housekeeping

- The project lives inside the Ripple_v6 repo as `orbital_atlas/`. Whether it moves to its own repo is open and blocks nothing.
- A dev server may still be running on port 8765 from the last session.
- The Snowflake chat plug-in door failed login on 2026-09-19. Out of scope for the atlas; the engine must work with pasted data alone.

**First message to Chris in the new session:** confirm the 26 tests pass and the demo loads, then say you are starting slice 2.
