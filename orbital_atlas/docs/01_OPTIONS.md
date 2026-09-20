# 01 — Options

Ten open questions. Three or more real options each. A recommendation only where the tradeoffs make it obvious, and marked as such.

**How to read this:** each section opens with a one-line summary, then a table. Depth sits under "More" and can be skipped.

**A note on outside tools:** every library, package, and host limit named below is from memory. None was checked in this session. That covers sizes, and also whether the thing still exists and behaves as described. Treat each as "might" and check before committing.

---

## 1. Rendering technology

**Summary:** Canvas draws pixels fast. SVG draws real shapes the browser knows about. WebGL uses the graphics card. They differ most on print, on hover cost, and on how many maps fit on one page.

| | Canvas 2D | SVG | WebGL | Hybrid: canvas map + SVG export |
|---|---|---|---|---|
| 3,142 shapes | easy | fine | easy | easy |
| 10,000+ shapes | fine with caching | sluggish; every shape is a page element | easy | fine |
| Hover hit-testing | hidden colour-coded canvas, as v1 does | free, the browser does it | colour-coded buffer, same idea | as canvas |
| Print / PDF | image only; must re-render at high resolution | **vector, sharp at any size** | image only, and awkward to capture | vector, via the export path |
| Accessibility | nothing built in; needs a parallel table and a live text readout | shapes can carry labels, but 3,142 tab stops help nobody | nothing built in | as canvas |
| Lighting, texture, grain | good: blend modes, gradients, blur | limited: filters are slow at this scale | best: real shaders, real hillshade | good |
| Extrusion, true 3D | no | no | **only option** | no |
| Many maps on one page | unlimited | unlimited but heavy | **browsers cap live WebGL contexts, roughly 8 to 16 per page** | unlimited |
| Unknown host | safest; works everywhere | safe; host CSS can leak in unless isolated | can be blocked or lose its context in embedded frames | safe |
| Code you write | moderate | least | most, unless you adopt a library | moderate plus a second drawing backend |

**Leaning, close to obvious:** canvas for the live map, with drawing routed through a small "draw list" so a second backend can emit SVG for export. It keeps v1's speed, keeps print sharp, and keeps small multiples possible. WebGL is only forced if extrusion or 50,000+ shapes become real needs. That is decisions 1, 2, and 3 in `06`.

### More
- **Draw list** means: the engine first decides "fill this shape this colour, stroke this line", as plain data. A canvas painter or an SVG writer then carries it out. Same picture, two outputs.
- Canvas blur via `ctx.filter` needs a Safari check. If it fails, glow and atmosphere need a fallback such as pre-blurred sprites.
- Canvas size limits are around 16,000 pixels a side in most browsers. A 4× export of a 975-wide map is well inside that.
- Canvas can run in a background thread via `OffscreenCanvas`. Useful later, not needed now.

---

## 2. Application structure

**Summary:** the real question is what the host has to know. The less it has to know, the later the host can be chosen.

| | A. Plain library, no framework | B. Light reactive layer | C. Full framework | D. Web component shell |
|---|---|---|---|---|
| What it is | `createAtlas(element, {view, theme, data})` in plain TypeScript or JavaScript | Same, with a small state library such as signals, Lit, or compiled Svelte for the panel parts | A React or Vue app | A custom HTML tag, `<orbital-atlas>`, that wraps A or B |
| Static site | script tag | script tag | needs a build | one tag |
| Webflow | works, script must be hosted elsewhere and linked | same | awkward | **best fit: paste one tag** |
| Streamlit-style data app | wrapped in a custom component | same | natural if the component template is React | wrapped the same way |
| Desktop wrapper | works | works | works | works |
| Survives a host change | **yes** | yes | UI code is married to the framework | **yes** |
| Code you write | most: you hand-write UI updates | less | least for UI | a thin layer on top |
| Dependency cost | near zero | roughly 3 to 15 KB | roughly 40 KB and up, plus build tooling | zero; it is a browser built-in |

**These are not exclusive.** The common shape is A at the core with D as the shell, and optional thin wrappers for any framework host. B only matters for whichever pieces have lots of UI state: the readout panel, the slicers.

**Host gotchas worth knowing now:**
- **Webflow** custom-code embeds have a character limit. The engine must load from a hosted script URL, not be pasted inline.
- **Streamlit inside Snowflake** has historically restricted custom components and outside scripts. Not checked in this session. If that host matters, check before choosing.
- **Shadow DOM**, the isolation a web component can use, blocks host CSS from leaking in. It also means webfonts must be declared on the outer page, not inside the component. Known trap.

---

## 3. Configuration storage and schema

**Summary:** configs are JSON either way. The choice is what checks them and what keeps old ones working.

| | A. JSON + JSON Schema | B. TypeScript types + a runtime validator such as zod | C. Hand-written checks |
|---|---|---|---|
| Source of truth | a `.schema.json` file | TypeScript code; JSON Schema generated from it | code |
| Editor help when hand-writing configs | **yes, in any editor, via `$schema`** | yes, after generation | no |
| Error messages | decent, can be cryptic | good | as good as you write them |
| Runtime cost | a validator library, roughly 40 KB; or **zero if validators are compiled at build time** | roughly 13 KB | zero |
| Readable by non-JS tools, such as Python in a data app | **yes** | only the generated schema | no |
| Drift risk | types and schema can disagree unless one is generated from the other | low | high |

**Versioning, same for all three:**
- Every config carries `"schema": "orbital.view/1"`. The number is the major version.
- The engine ships small upgrade functions: 1→2, 2→3. Old configs are upgraded on load, in memory.
- Unknown fields are kept and warned about, never silently dropped. A config written by a newer engine still loads in an older one.
- **Rule that makes this work:** fields are added freely; renamed or removed only with a major bump and an upgrade function.

**Where configs live:** plain `.json` files in a folder; one row per view or theme in a table; or embedded in a share link. All three are the same JSON. The engine takes an object and does not care where it came from.

---

## 4. Topology handling

**Summary:** "pre-projected" means the curved-earth maths was done ahead of time and the file holds flat x,y. Runtime projection means the browser does that maths on load.

| | A. Pre-project at build time | B. Project at runtime | C. Support both |
|---|---|---|---|
| Load speed | fastest | slower; a few hundred ms for counties | depends on the file |
| Engine size | smallest; no projection code | adds roughly 30 KB of d3-geo | adds it, loadable on demand |
| Alaska and Hawaii insets | baked in | needs the composite Albers USA projection | either |
| User drops in arbitrary GeoJSON | **no**, they must run a build step | **yes** | yes |
| Consistency | every topology looks deliberate | easy to get odd framing | mixed |
| Build tooling | needs a small script, such as mapshaper or `geoproject` | none | both |

**Whichever is chosen, each topology needs a registry entry. v1's hardcoding shows exactly what must go in it:**

```
id            "us_counties_2018"
geo_type      "county"
vintage       2018
url / object  where the file is, which object inside it
projected     true | false
bbox          real bounds, measured, not assumed
id_rule       how to clean ids, e.g. pad left to 5 with "0"
name_field    which property holds the display name
parent        how a place finds its parent: prefix of 2, a property, or a lookup table
aliases       optional: retired or renamed ids, e.g. CT and AK changes
layouts       optional: precomputed cartogram positions
```

**Where topologies come from:** Census cartographic boundary files for counties, states, districts, tracts. The `us-atlas` package republishes some of those pre-projected. Hospital regions come from the Dartmouth Atlas, as shapefiles; check they are still published. User polygons arrive as GeoJSON.

**Adjacency**, which places touch, is computed at load from the topology. It is cheap and v1 already does it.

---

## 5. Cartograms

**Summary:** a cartogram trades true shape for some other fairness. The three kinds differ in whether the layout depends on the data.

| | Tile | Dorling | Continuous |
|---|---|---|---|
| What it is | every place an equal square or hexagon | every place a circle sized by value, pushed apart until none overlap | real shapes stretched so area equals value |
| Layout depends on the data? | **no**, only on the topology | yes, sizes change per layer | yes |
| Can be precomputed per topology? | **yes, fully** | start positions only | no |
| Quality at 3,142 units | poor to fair: the dense East scrambles; neighbours drift apart. States tile beautifully, counties do not. | **good**: recognisable country, honest sizes | fair: needs many passes, shapes get ugly, slow |
| Compute cost | offline, an assignment problem solved once | roughly 1 to 3 seconds of force simulation in the browser | 10+ seconds, best done offline |
| Hover, focus, borders | simple | simple | works, borders distort |

**Where to compute:**

| | Precomputed per topology | At load, main thread | In a background worker |
|---|---|---|---|
| Works for | tile only | Dorling, freezes the page briefly | Dorling and continuous |
| Cost | a build script and a stored layout | none | a little plumbing |
| Motion rule | n/a | n/a | the switch to the new layout is a single user-triggered move, which is legal |

**Honest take:** tile at state level and Dorling at county level are the two that earn their keep. Continuous at county level is a research project.

---

## 6. Interaction model

**Summary:** the engine should own anything that needs to know about geometry. The host should own what a click means.

| Interaction | Needs geometry? | Natural owner |
|---|---|---|
| Hover and readout | yes | engine |
| Click | hit test yes, meaning no | engine finds the place, **host or view decides the meaning** |
| Focus: zoom to a region | yes | engine |
| Select and pin: hold place A while hovering B | yes | engine keeps the set, host may read it |
| Brush: drag a box or lasso to pick many | yes | engine |
| Compare: two places side by side in the readout | no | readout component |
| Keyboard | yes | engine |

**Three ways to split it:**

| | A. Engine decides everything | B. Engine only emits events | C. Defaults in the view, events always emitted |
|---|---|---|---|
| Example | click always focuses the parent region | click fires `place-click`, nothing else happens | view says `"on_click": "focus_parent"`, and the event fires too |
| Works with zero host code | yes | **no** | yes |
| Host can override | no | yes | yes |
| Risk | v1's trap again | every host rebuilds the basics | slightly more config surface |

**Keyboard for 3,142 shapes.** Tabbing through them is useless. Options that work together:
- **One tab stop** for the whole map. Arrow keys then walk to the neighbour in that direction, using adjacency plus compass bearing between centres.
- **A search box**: type a place name, jump to it.
- **The sortable table view** as the true accessible equivalent. Same data, same selection.
- A live text region that speaks the readout, so screen readers hear what sighted users see.

---

## 7. Data ingestion at runtime

**Summary:** every source should end at the same doorway: a table in the contract shape, plus a load report. What varies is who fetches.

| | A. Adapters return row objects | B. Adapters return columns as typed arrays | C. Adapters return raw text; one shared parser does the rest |
|---|---|---|---|
| Simplicity | **simplest** | more plumbing | simple for text sources only |
| Speed at 3,142 × 20 periods | fine | fastest | fine |
| Speed at 1M rows | slow | **fine** | slow |
| Warehouse results, which arrive as JSON or Arrow | natural | natural | awkward |
| One place for validation | yes, after the adapter | yes | **yes, strongest** |

**The interface, in plain words:**

```
source.load(request)  ->  { header, table, report }

request   which layer, which periods
header    label, unit, formats; see 02_CONTRACT
table     rows in the contract shape
report    rows in, rows kept, unmatched ids, duplicates, gaps
```

Paste, file drop, URL fetch, and "the host handed me rows" are four small adapters behind that.

**The warehouse adapter is not what it sounds like.** A browser cannot safely hold warehouse credentials. So the future plug is one of two things: the host queries and hands rows in, as a data app would; or a small web service sits in between and the engine fetches a URL. Both are already covered by "host rows" and "URL". **That means the warehouse adapter is a plug by construction.**

**File formats:** CSV, TSV, and JSON rows cost nothing. Parquet needs a reader library; small pure-JavaScript ones might exist, check size before adding.

---

## 8. Export

| Output | Options | Tradeoff |
|---|---|---|
| **PNG** | re-render the canvas at 2× to 4× and save | trivial; texture and lighting come through exactly |
| **SVG** | second drawing backend, from the draw list in question 1 | moderate; sharp; blur and blend effects need simplified stand-ins |
| **PDF** | a. browser print of the SVG with a print stylesheet | zero dependencies; user sees a print dialog |
| | b. a PDF library in the browser | roughly 300 KB and up; one-click; font embedding is fiddly |
| | c. a headless browser on a server | best fidelity; needs a server, which fights "host decided later" |
| **Share this view** | a. config squeezed into the URL after `#` | no server; works for view + theme; **cannot carry pasted data beyond a few KB** |
| | b. a single `.atlas.json` file holding view, theme, and data | carries everything; it is a file, not a link |
| | c. a short link backed by storage | nicest; needs a server |

**Print-safe grayscale** is a theme, not an export feature. Export just renders whatever theme is active.

---

## 9. Multiple views at once

**Summary:** first separate two things that look alike. A **difference map** or **ratio map** is one map with arithmetic on two layers. That is a view feature. **Side-by-side, swipe, and small multiples** are several maps arranged. Only the second group is a layout question.

| | A. Engine draws one map; host arranges | B. Engine owns multi-map layouts | C. One-map core plus an optional compare module |
|---|---|---|---|
| Core stays small | **yes** | no | yes |
| Linked hover and shared colour scale | host must wire it, or a `link(a, b)` helper does | built in | built in, inside the module |
| Swipe, which needs two maps pixel-aligned | hard for a host | easy | easy |
| Small multiples in a host's own grid | **natural** | fights the host's layout | either |
| Shares one loaded topology across maps | needs a shared cache | yes | yes |

**Two technical notes:**
- A shared colour scale across small multiples is an honesty issue, not a convenience. Twelve maps each with their own scale cannot be compared. The default should be shared.
- This is where WebGL's context cap bites. Twelve small multiples is twelve contexts.

---

## 10. Dashboard-style controls

**Summary:** a slicer is just a widget that changes one field of the view config. So the foundation is one call, `atlas.setView({period: "2023"})`, and the three options are who draws the widget.

| | A. Inside the engine | B. A separate control component | C. Host-provided |
|---|---|---|---|
| Example | the map has its own side panel, as v1 | `<atlas-controls for="map1">` reads a small controls config | a Streamlit dropdown calls `setView` |
| Webflow / static site | works | **works, and can be placed anywhere on the page** | you would have to build widgets |
| Data-app host | clashes with the host's own widgets | optional | **natural** |
| Engine stays domain-free | no, it grows a UI | yes | yes |
| Looks native to the host | no | themeable | yes |

**How binding works in B and C:** a controls config lists which view fields are exposed.

```json
{ "controls": [
  { "bind": "view.layer",   "type": "select", "options": "auto" },
  { "bind": "view.measure", "type": "toggle", "options": ["value", "ratio"] },
  { "bind": "view.period",  "type": "select", "options": "auto" },
  { "bind": "theme",        "type": "select", "options": ["ledger", "nightlights"] }
]}
```

`"auto"` means the engine fills the choices from what is loaded.

**Close to obvious:** build the `setView` call first, since B and C both sit on it. Ship B as an optional extra. Avoid A; it is how v1 got stuck.
