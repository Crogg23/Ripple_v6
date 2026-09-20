# GO BILLS — Orbital Atlas v2 handoff

Paste this whole file as the opening prompt of a new Claude Code session, started in the Ripple_v6 repo. Written 2026-09-19.

---

## The goal, in Chris's words (2026-09-19) — read this before anything else

> "above all else I need things to be functional and demonstrate a knack for communicating large and complex data into simple, conversational terms"

He called the first demo "an excel hack from the mid 2000's". Six art-directed poster plates followed; he said they "lost sight of the goal". What landed was the map TALKING: a headline sentence generated from the numbers, bullets that light up their places, a hover sentence per place. Beauty serves that, never leads. **The front door is now `demo/story.html`.** `demo/index.html` is the old control-panel bench, `demo/plate.html` is the six posters.

## Your role

You are the builder on Orbital Atlas v2. The recon phase is finished, the decisions are made, and four of eight build slices are done and verified. **Your next job is slice 4.** Do not reopen decisions unless Chris asks.

Read these three files before anything else, in this order:

1. `orbital_atlas/docs/07_BUILD_SPEC.md` — the plan, the slices, the standing rules
2. `orbital_atlas/docs/06_DECISIONS_NEEDED.md` — all twelve answers, with who made each
3. `orbital_atlas/docs/03_CONFIG_SCHEMA.md` — the view and theme schemas, now implemented

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
| **2. Honest colour** | done, verified 2026-09-19 | Eight scale types, ties share a colour, legend generated from the scale, readout with value, base, ratio, n, tier, rank. Geometric hover. Refusals in plain words. |
| **3. Configs** | done, verified 2026-09-19 | Ten row files load and render. Config checks in plain words. Theme `base` chains. Roles: highlight by eight rules, low confidence, no data. Hillshade, glow, texture, radial light. Schema files generated from the engine. |
| 4. Hands on | **next** | — |
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
  src/engine/drawlist.js    buildDrawList(topology, theme, {fills, marks}); ops ground land places glow hatch mesh outlines dots light texture
                            buildOverlay(theme, {hover}): ops painted over the cached map
  src/engine/frame.js       fit(bbox, W, H, pad), project()
  src/engine/defaults.js    DEFAULT_THEME with four palette families, DEFAULT_VIEW with measure, scale, readout; overlay()
  src/engine/measure.js     measureValues(cols, which, header, report); ratioOf(); the only place a rate is divided
  src/engine/scale.js       buildScale(values, cfg) -> position per place, zero mask, category index, palette-free legend model
  src/engine/color.js       hex, Oklab blending, ramp(), familyRamp(palettes, family)
  src/engine/format.js      makeFormatter("$,.3s"): hand-written d3-format subset [$][,][.p][f|d|%|s]; refuses the rest
  src/engine/colorize.js    colorize({layer, view, theme, topology}) -> {fills, legend, model}; the one pipe the shell calls
  src/engine/readout.js     rankAll(), buildReadout(idx, model) -> plain data
  src/engine/config.js      WORDS: every enum, single source; checkView(), checkTheme(), resolveTheme(raw, library)
  src/engine/roles.js       pickHighlight(): eight rules, ties flagged together; pickLowConfidence()
  src/engine/light.js       hillshade(topology, height): shading from scale position only
  src/engine/hit.js         hitTest(topology, x, y) by geometry, unproject(); no pixels read
  src/painter/canvas.js     CanvasPainter: setTopology, resize, paint(drawList, transform, overlay); keeps the finished map on a hidden canvas
  src/loader/parse.js       text -> rows; delimiter sniffing, header detection, paste shorthand, NUMBER regex
  src/loader/load.js        loadRows(rows, {topology, header, onDuplicate, knownGeoTypes}) -> {header, table, report}; resolvePeriod()
  src/loader/report.js      describeReport(report) -> [{level, text}]
  src/adapters/sources.js   sources.paste / file / url / rows
  src/element/orbital-atlas.js   the tag: theme, view, ready, load(), clear(), legend, readout(geoId); legend and readout DOM;
                                 events atlas-ready / atlas-load / atlas-error / place-hover
  src/vendor/topojson-client.js  the only outside code, 7 KB, fetched from jsdelivr, makes no network calls
  configs/index.json        the rows: each is one view file plus one theme file
  configs/views/            01_money .. 08_land_area, 07b_absence, empty
  configs/themes/           ledger is the base; restraint, alarm, paper, washed, lean, relief build on it
  configs/schema/           orbital.view.1.json, orbital.theme.1.json; GENERATED, never hand-edit
  tools/make_schemas.js     node tools/make_schemas.js   rewrites the schema files from src/engine/config.js
  demo/layers.js            seeded made-up tables per layer id; land_area is measured from the shapes. Host-side, not engine.
  topologies/registry.json, topologies/us_counties_2018.topo.json
  demo/index.html           paste box, samples, view controls, report panel
                            URL: ?sample=ct|messy|full|minimal|ties|all &measure= &scale= &bins= &zero=1 &invert=1 &spread=1 &hover=<geo_id>
                            URL: ?row=1..9|7b &theme=<id> &hover=<geo_id>
  test/slice0..3.test.js
```

### The table shape the colour pipe reads

`loadRows` returns `table.byPeriod[period]` holding columns aligned to `topology.places` order:

- `has` Uint8Array — a row exists
- `value`, `denominator`, `n` Float64Array — `NaN` means no data, which is **not** zero
- `tier` Array of string or null

`resolvePeriod(table, 'latest')` gives the last period in sort order. `table.setAside` holds rows for other known geo_types, kept for drill-down.

## Prove it still works

```
cd orbital_atlas
node --test test/*.test.js                 # expect 75 pass, 0 fail
python -m http.server 8765                 # then open http://localhost:8765/demo/index.html
```

Headless check, no clicking needed:

```
# This machine is Windows, run from Git Bash. On a Mac the binary is "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome".
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --virtual-time-budget=8000 --dump-dom "http://localhost:8765/demo/index.html?sample=messy" | grep -o "<title>[^<]*"
# the title starts:  LOADED kept=2 unmatched=1 dupkeys=1 rejected=2   then  | legend: ...
# ?sample=ct                       starts  LOADED kept=2 unmatched=5 dupkeys=0 rejected=0
# ?sample=minimal&measure=ratio    ends    refused: This layer has no denominator, so "ratio" cannot be drawn. ...
# ?sample=all&scale=log            ends    refused: A log scale cannot show zero or negative values, and 930 places have them. ...
# ?sample=all&measure=ratio&bins=4&zero=1&hover=48201   ends with Harris: value, denominator, ratio, n, and rank
# ?row=1                contains  row 1 theme=restraint | highlight=accent_fill:top 10%:315
# ?row=1&theme=paper    contains  row 1 theme=paper | highlight=outline:top 10%:315        same 315, different look
# ?row=5                contains  low_confidence=desaturate:low confidence: people under 5,000:806
# ?row=9                is        EMPTY | row 9 theme=ledger
```

ES modules and `fetch` do not work from `file://`. A local server is required for development.

## Slice 2 — how it works, for whoever builds on it

```
cols -> measureValues -> buildScale -> positions 0..1, zero mask, legend model with no colours
                                          |
theme.palettes -> familyRamp ------------> colorize -> fills + finished legend + readout model
```

- **Ties share by construction.** Every position is a function of the value alone. `ties: "spread"` is opt-in, and the legend then carries a warning line.
- **Smooth quantile:** each tied group takes its middle rank; the lowest group is stretched to 0 and the highest to 1. Legend ticks sit at the real colour position of the values at percentiles 0, 10, 50, 90, 100, so skew and ties show up as uneven spacing.
- **Binned quantile:** cut values that repeat are merged, and the legend says "5 classes became 3".
- **`invert`** flips colours at lookup time only, so legends still read low to high.
- **Palette family:** categorical, binary, diverging by scale type; `zero_class` switches a sequential scale onto the binary family; otherwise sequential. The zero colour must not equal the no-data colour; a test pins that for the default theme.
- **Refusals** throw plain-word errors from the engine. The shell catches them, shows them in red, fires `atlas-error`, and paints no colour.
- **Hover** is a geometric hit test, not a pick canvas. It reads no pixels, so v1's blended-edge trap cannot happen. Slice 4 can keep it; 3,142 box checks per pointer move is cheap.

## Slice 3 — how it works, for whoever builds on it

- **A row is two file names.** `configs/index.json` pairs a view with a theme. The demo loads the theme, loads the layer the view names, then sets the view. Nothing else changes between versions of the map.
- **The view says who, the theme says how.** `colorize` returns `marks: { highlight, low_confidence }` as place indexes. Fill-type styles change the fills. Line-type styles become draw-list ops. Swapping a theme cannot change `marks`, the legend words, the ticks, or the ranks; a test pins that for rows 1 and 4.
- **Paint order for one place:** scale colour, hillshade, highlight fill, low-confidence wash. The wash goes last so a shaky place still looks shaky when it is also called out.
- **Refusals come in two layers.** `checkView` and `checkTheme` run in the shell before anything draws. `colorize` refuses what needs the data: wrong layer id, wrong map, no tier column, size encoding on a rate, encodings not built.
- **"Flagging all is flagging none."** Percentile and top-n rules flag nobody when the cut would take every place.
- **Hover is an overlay.** The painter keeps the finished map on a hidden canvas and adds one outline per move.
- **Schema files are generated.** Change a word list in `src/engine/config.js`, run `node tools/make_schemas.js`, or a test fails.

## After slice 3 — the talking layer and the looks (2026-09-19 and 20, skeptic-passed after fixes)

```
src/engine/narrate.js    narrate(model, marks) -> { headline, evidence, lines:[{kind,text,places}], caveats }; describePlace(idx, model)
                         kinds: typical, standout, overall, concentration, where, region, zeros. Every line carries the places it is about.
src/engine/stipple.js    dot-density ink, seeded per place
src/engine/field.js      places melted into one smooth surface: contours(), ridges(), currents()
src/engine/hit.js        hitTest now uses a bucket grid; same answers as brute force
colorize()               also returns story, ink, labels, legend.spread (distribution bars in the map's own colours), model.order
drawlist                 new ops: stipple, strokes, ridges, callouts, veil; land shadow; buildOverlay takes hover, pinned, spotlight
shell                    el.story, el.spotlight(places), el.pin(geoId), rebuild_ms; events view-change, place-click; canvas aria-label = headline
configs/themes           nightfall, pressroom, survey, topograph, transmission, undertow   ·   configs/views/plate_*.json
demo/story.html          URL: ?data= &measure=value|ratio &call=none|top|out &look= &place=<geo_id> &light=<bullet index> &paste=<csv>
test/story.test.js       16 tests; 5 of them are sentences the skeptic proved false, now pinned
```

**The narrator's one law: a sentence only says what was counted.** The first version said "Eight in ten fall between X and Y" from percentiles; with ties at zero it was really nine in ten. It said "half above, half below" with 70 of 100 tied at the median. It called one place of one "spread out". It named a top tenth when every value was equal. All read well and all were false. Now each share is counted before it is worded, ties are said out loud, and equal data gets one sentence and stops. When you add a sentence, add the test that recomputes it from the table.

Words come from the data's own labels: nouns from `topologies/registry.json` (`"noun": ["county", "counties"]`), labels and formats from the layer header. A header may add `one` for the singular. Compact formats like `$,.3s` print `$4.1M` on a legend and "$4.1 million" in a sentence.

Open after this pass: the demo tables are still made up (only `land_area` is real). Real data is the next lever, and it needs the warehouse's Python door and a price first. The narrator reads one layer and one period; it has no change-over-time sentences yet.

## Slice 4 — what to build

From the spec: **pick canvas with the edge-pixel fix, hover, focus parent, `setView`, events, keyboard walk by neighbour.** Done means hover across a border never flashes a wrong place, arrow keys walk the map, zoom is user-triggered, runs once, 250 ms or less.

Already in hand from slices 2 and 3: geometric hover, readout, `place-hover` event, hover outline, cached base paint. Still to build: `place-click` and `view-change` events, `setView(patch)`, `frame` types and the zoom, `focus_dim` veil, `on_click`, keyboard walk using `place.neighbors`, and the first pixel test of the painter. The zoom needs a second animation-frame call site or a reworked one; the motion test pins the count at one, so argue the change there.

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
| **v1's ties** | Equal values got different colours, ordered by file position. | `ties: "share"` is the default. A test runs the tie case under every scale type. |
| **v1's pick canvas** | Antialiased edges blend two id-colours into a third county's id. | Slice 2 hovers by geometry, so no pixels are read. If slice 4 adds a pick canvas anyway, fix this there. |
| **Path filters on Windows** | The wall test skipped files by `'/painter/'`. Windows paths use backslashes, so the painter was scanned and the test failed; the vendor skip was dead too. | `jsFiles()` normalises separators. Any new path filter in a test must do the same. |
| **Zero looked like no data** | First zero colour was one shade off the no-data colour; on the map they read as the same. | Zero colour is now a distinct slate. Look at a screenshot before trusting two hex codes to differ. |
| **Resize wiped the map for a frame** | Setting a canvas width clears it, and the repaint waited for the next frame. A headless screenshot caught row 4 fully blank. | `_resize` paints at once, inside the same frame. |
| **A number borrowed the wrong format** | The low-confidence floor printed as "5,000.0" because it used the rate's format string. | Every number is formatted by the header part it belongs to, never by the driving measure. |
| **null blocks crashed the checker** | `"highlight": null` threw a programmer error instead of a plain refusal. The skeptic found it. | `brokenBlocks()` runs first and names the block in words. |
| **Legend labels printed over each other** | Percentile 90 and the maximum sit a tenth apart on the ramp. | Tick labels alternate between two rows. |

## Known gaps, honest

- Encodings other than `fill` are refused as not built. `focus_dim`, `frame`, `on_click`, `labels.top`, `layer_b` are checked and carried, and do nothing yet.
- The engine runs no JSON Schema validator. Its checks are hand-written; a test pins the schema files to the same word lists.
- Glow uses canvas shadow blur. Safari is still unchecked.
- Money over a billion prints as `$1.10G`, the d3 way, not `B`.
- All demo layers are made up and say so on the page. Only `land_area` is real, measured from the shapes.
- A categorical layer with more codes than the theme has swatches reuses colours. The legend still lists every code.
- The log scale ignores `bins`.
- The number formatter is hand-written, not d3-format. It covers `[$][,][.p][f|d|%|s]` and refuses anything else.
- Legend and readout are placed bottom-left and top-left inside the tag, and the legend can sit over the far south-west of the map. Placement belongs to slice 6.
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

**First message to Chris in the new session:** confirm the 75 tests pass and `demo/story.html` loads, then ask what he wants next. Do not assume slice 4.
