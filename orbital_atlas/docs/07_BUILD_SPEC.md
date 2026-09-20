# 07 — Build Spec

Written 2026-09-19 from the answers in `06`. This is the clean starting point for the build phase. Nothing here is built yet.

## What was decided

| # | Decision | Answer | Who |
|---|---|---|---|
| 1 | Print | none; saved image only | Chris |
| 2 | Smallest shapes | counties nationally, tracts per state on drill-down | Chris |
| 3 | 3D | someday, not now; keep the painter swappable | Chris |
| 4 | Framework | none | Chris |
| 5 | Language | plain JavaScript, type notes in comments | Claude, follows from 4 |
| 6 | Configs | JSON files now, flat enough to be warehouse rows later | Claude |
| 7 | Layer header | yes | Claude |
| 8 | Duplicate rows | reject and report by default; per-load override | Claude, follows from the honesty rule |
| 9 | County vintage | current-year default, 2018 kept, alias table | Claude, follows from 2 |
| 10 | Encoding | theme; engine refuses size on rates | Claude |
| 11 | Slicers | `setView` first, control component second | Claude |
| 12 | Architecture | A: plain core + web component | follows from 4 |

Any "Claude" row can be flipped before its slice starts, at no cost.

---

## The shape of the thing

```
rows + header ──▶ LOADER ──▶ clean table + load report
                                  │
view.json  ──▶ ┌──────────────────▼─────────────────┐
theme.json ──▶ │  ENGINE   scale · roles · frame     │──▶ draw list ──▶ PAINTER ──▶ canvas
topology   ──▶ │           legend · readout · events │                  (canvas today,
               └──────────────────┬─────────────────┘                   3D someday)
                                  │
              setView(patch) ◀────┴────▶ events: place-hover, place-click, view-change
```

**The one hard wall:** only the painter touches the canvas. The engine produces a **draw list**, which is plain data: "fill shape 1043 with this colour, stroke this mesh at this width". That wall is what makes 3D someday a painter swap and not a rewrite.

## Files

```
orbital_atlas/
  src/
    loader/       parse, clean ids, validate, dedupe, load report
    adapters/     paste, file, url, host-rows
    topology/     registry, decode, adjacency, parent and children links
    engine/       scale, roles, legend model, readout model, frame, draw list
    painter/      canvas painter, pick canvas
    interact/     hover, click, focus, keyboard walk, events
    element/      <orbital-atlas>, <atlas-controls>, <atlas-table>
    vendor/       topojson-client, a number formatter; single files, no install at runtime
  configs/
    views/        the nine illustration rows, as JSON
    themes/
    schema/       JSON Schema files, for editor autocomplete
  topologies/     counties current, counties 2018, tracts per state, registry.json
  tools/          one-time scripts that make the topology files
  demo/           index.html
  docs/
```

## Outside code

| Piece | Why | Cost |
|---|---|---|
| topojson-client | decodes the topology files, finds neighbours, builds border meshes | one small vendored file |
| a number formatter, such as d3-format | format strings like `$,.3s` live in configs | one small vendored file; size not checked this session |
| mapshaper or similar | **tool only**, run once to make tract files in the same projection as counties | never shipped to the browser |

Everything else is hand-written: colour blending, scales, shape paths, zoom maths.

**Correction to something said in chat:** "open the file in a browser and it just runs" was too strong. Browsers block a local page from loading its own map files. Development needs a one-line local server, such as `python3 -m http.server`. Once hosted anywhere, no server logic is needed.

---

## Build order

Each slice ends with something visible and a check that could prove it wrong.

| Slice | What gets built | Done means |
|---|---|---|
| **0. Bones** | folder, demo page, `<orbital-atlas>` tag, topology registry, draw list, canvas painter, flat fill | 3,142 counties appear. Shape count asserted in a test. Real bounding box used, so the Aleutians are in frame. |
| **1. Data in** | loader, paste adapter, layer header, load report shown in words | Paste the three examples from `02`. A paste with Connecticut planning-region ids reports them as unmatched by id. A duplicate key is rejected and listed. |
| **2. Honest colour** | scales with ties sharing, generated legend, readout with value, denominator, ratio, rank | The Neighbours-style tie case: equal values get one colour. A quantile legend prints "percentile" and real cut values. |
| **3. Configs** | view and theme loading, schema files, cross-checks, roles: highlight, low-confidence, no-data | **All nine illustration rows load from JSON and render.** This is the acceptance test for the view/theme split. Swapping themes between rows 1 and 4 changes look, not meaning. |
| **4. Hands on** | pick canvas with the edge-pixel fix, hover, focus parent, `setView`, events, keyboard walk by neighbour | Hover across a border never flashes a wrong county. Arrow keys walk the map. Zoom is user-triggered, runs once, 250 ms or less. |
| **5. Drill-down** | tract files per state via `tools/`, `children` link in the registry, scale scope setting | Click Texas: tracts load and draw aligned to the county borders. Legend says "ranked within Texas" or "ranked nationally". |
| **6. Around the map** | `<atlas-controls>` bound to view fields, `<atlas-table>` sortable and linked to hover | A dropdown changes the period with no code. The table and the map highlight the same place. |
| **7. Out** | save as image, share link carrying view and theme, `.atlas.json` bundle carrying data too | A share link reopens the exact view. |

### Parked for after slice 7
Cartograms · side-by-side, swipe, small multiples · difference and ratio maps · auto-labels and callouts · stipple, hatch, dots · grain and paper textures · non-map views beyond the table · the 3D painter · the warehouse adapter.

None of these change the structure above. `04_RENDER_MODES` is the menu.

---

## Rules carried into every slice

- **Motion:** only `motion.zoom_ms`, capped at 400. No timers, no loops, no idle animation anywhere in the code. A test greps for `setInterval` and looping animation frames.
- **Honesty:** the legend is generated from the scale, never typed. Raw, base, and ratio are always reachable when a denominator exists. Low-confidence gets a legend entry whenever it is switched on.
- **Domain-free engine:** no place names, no state codes, no units in `src/`. They live in topologies, headers, and configs.
- **Nothing silent:** every dropped, repaired, or unmatched row appears in the load report.
- **Configs outlive code:** every config carries its schema version. Fields are added freely, renamed only with an upgrade function.

## Open items that do not block slice 0

| Item | When it matters |
|---|---|
| Does canvas blur work in Safari? | before any glow theme, slice 3 |
| Where tract boundary files come from, and their year | slice 5 |
| Does the project stay inside the Ripple repo? | before the first commit |
