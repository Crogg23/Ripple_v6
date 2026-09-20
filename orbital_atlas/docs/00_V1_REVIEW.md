# 00 — v1 Review

Read 2026-09-19. Source: `reference/orbital-atlas-v1-source.html`, 545 lines. The first 140 are font declarations. The rest is about 100 lines of markup and 300 of script.

## The short version

- **v1 proves the look.** Dark surface, rank-based colour, serif readout. Keep the direction.
- **v1 is one class that does everything.** Data, ranking, colour, drawing, mouse, and panel text all live in one `Component`. Nothing can be swapped without touching the rest.
- **v1 breaks three of the new non-negotiables today.** The legend lies about the scale. Ties get different colours. Glow is decoration, not signal.
- **Nothing in v1 is config.** Palettes, layers, and number formats are JavaScript, not data.
- **Verdict: keep the ideas, leave the code.** About six techniques are worth carrying over. Listed at the bottom.

---

## What the files actually contain

Checked by script, not read off the brief.

| Thing | Found |
|---|---|
| County shapes | 3,142, all with a 5-digit id and a name |
| State shapes | 51, the 50 states plus DC |
| Nation shape | 1 |
| Line segments in the file | 9,462 arcs, 37,858 points. Small. |
| Bounding box | x from -57.7 to 957.5, y from 13.0 to 606.6 |
| Puerto Rico and territories | not present |

**Two traps in the topology:**

- **The box is not 0 to 975.** The Aleutian chain in Alaska runs to x = -57. v1 fits the view to a hardcoded 0–975 box, so the far Aleutians sit outside the fitted frame.
- **It is a 2018 county list.** Connecticut has its 8 old counties; the 9 planning regions that replaced them in 2022 are not there. Alaska has `02261` Valdez-Cordova; its 2019 replacements `02063` and `02066` are not there. Any dataset newer than 2019 will have rows that match nothing, and v1 would not tell you.

---

## What v1 does well

| Strength | How it does it | Why it matters for v2 |
|---|---|---|
| Fast hover on 3,142 shapes | A hidden second canvas paints each county in a unique colour. Reading one pixel under the mouse gives the county. | Cost does not grow with shape count. Works at 10,000+. |
| Cheap redraws | The full map is drawn once to an offscreen canvas. Hover only repaints the highlight on top. | Hover never redraws 3,142 fills. |
| Shapes built once | Each county becomes a `Path2D` object at load. Zoom is a canvas transform, not a re-projection. | Zoom and focus are nearly free. |
| Colour by rank | Counties are sorted and coloured by position in the sort, not raw value. | Skewed data such as population still uses the whole palette. |
| Rank in the readout | Hover shows value and "#12 of 3,142". | Already halfway to the honesty rule. |
| State focus panel | Click dims other states, zooms in, shows a 14-bar histogram against the national range. | Good pattern: local detail, national context. |
| Motion mostly obeys the rule | No idle animation. No loops. The starfield is seeded, so it is static. | Little to unlearn. |
| Forgiving paste box | Accepts comma, tab, or semicolon. Pads short FIPS. Header row names the layer. Reports "N of 3,142 matched". | The tone of the loader is right. |
| Borders drawn as shared lines | Uses the topology's mesh, so a border between two counties is stroked once. | Cleaner lines, fewer draw calls. |

---

## What v1's structure makes hard

### It breaks the honesty rule in three places

| Problem | Where | What a reader sees |
|---|---|---|
| **Legend implies linear, colours are by rank** | `legendLo`/`legendHi` are min and max value on a smooth gradient. Colour comes from `c.r`, the rank position. | The midpoint colour looks like "halfway between min and max". It is actually the median county. For land area those are wildly different numbers. |
| **Ties get different colours** | `rankMetric` sorts, then assigns `i/(n-1)`. Equal values get consecutive positions. | The Neighbours layer is small whole numbers, so nearly every county is in a tie. Counties with the same count show as a smooth gradient of different colours. The order inside a tie is just file order. |
| **Glow is not tied to anything statistical** | `makeGlow` lights every county above the 72nd percentile. | 28% of the country glows on every layer. Glow reads as "special" and means "upper-ish". |

### Engine, view, and theme are fused

- **Layers are code.** Each metric is an object holding JavaScript functions for formatting. A function cannot be saved as JSON.
- **Palettes are code.** A `PALETTES` constant. Adding one is an edit.
- **The only real config is three runtime props**: palette name, atmosphere strength, county lines on or off. That is the seed of a theme schema, and it only exists because the host runtime asked for it.
- **Lighting, stars, vignette, and atmosphere are hardwired into `drawScene`.** A flat, light-background, or print theme means rewriting the draw function.
- **`renderVals` builds every string the panel shows.** The panel cannot exist without the class, and the class cannot exist without the panel.

### The engine knows things it should not know

| Hardcoded knowledge | Line of evidence | What it blocks |
|---|---|---|
| The map box is 975 × 610 | atmosphere, glow, and `baseT` all use these numbers | Any other topology |
| A county belongs to the state named by its first two digits | `c.st = c.fips.slice(0,2)` | Districts, hospital regions, user polygons |
| Texas is 695,662 km² and Alaska is drawn at 0.35 scale | used to turn pixels into km² | Anything that is not this exact file |
| Room must be left for a side panel | `fit()` reserves 350 px of width; the panel itself is 316 | Any host that lays things out differently |
| Click means "focus the state" | `onClick` | Compare, select, brush, or host-defined clicks |
| Ids are 1 to 5 digits | the paste regex | Non-numeric ids such as district codes |

### The data path is too narrow for the contract

- Takes `fips,value` only. No `denominator`, `n`, `period`, `tier`, or `geo_type`.
- **One custom layer at a time.** A second paste overwrites the first.
- **Duplicate rows: last one wins, silently.**
- **Reports matches, not misses.** It says how many counties got a value. It never says how many pasted rows matched nothing. With the 2018 county list, that is exactly the number you need.
- Values are stored on the shape objects themselves, as `c.v.custom`. Data and geometry are one object. Two maps cannot share one topology with different data.

### Tied to its host

- Depends on `DCLogic`, `sc-for`, `sc-if`, and `{{ }}` templating. None of that exists outside the document runtime.
- Pulls in React through that runtime, plus d3 and topojson as globals it polls for every 30 ms.
- All styling is inline on each element. No theme can reach it.
- Two webfonts loaded from the bundle: IBM Plex Mono and Instrument Serif.

### Smaller things worth knowing

| Issue | Detail |
|---|---|
| Edge pixels can pick the wrong county | The hidden pick canvas is antialiased. On a border, two id-colours blend into a third colour, which decodes to some unrelated county. Shows up as a flicker when crossing borders. |
| Hover is dead during zoom | `pickAt` returns nothing while the animation runs. |
| Zoom runs 0.7 to 1.5 seconds | User-triggered and runs once, so it is legal. It is not "finishes fast". |
| Zoom redraws every county every frame | The offscreen cache is bypassed during animation. Fine at 3,142. Not fine at 10,000+. |
| Two giant hidden canvases | Glow and atmosphere are each about 3,000 × 2,000 pixels. The glow one is rebuilt, with a blur, on every layer change. |
| Blur uses `ctx.filter` | Safari support for this has been patchy. Not checked in this session. |
| No keyboard access | Esc is the only key. The canvas has no text alternative. A screen reader sees nothing. |
| No export, no shareable state | No PNG, no PDF, no URL that reopens the same view. |
| Pixel density capped at 2× | Good for speed. Rules out print-quality output from the same path. |

---

## Keep / leave

| Keep | Leave |
|---|---|
| The visual direction: dark ground, restrained type, serif place names | The `DCLogic` runtime and its templating |
| Pixel-colour hit testing, with antialiasing fixed | One class owning data, draw, and UI |
| Offscreen scene cache plus a thin overlay for hover | Layers and formatters written as functions |
| Shapes built once, zoom by transform | Values stored on the shape objects |
| Rank-based colour, **with ties sharing a colour and a legend that says "percentile"** | Min–max legend on a rank scale |
| Rank shown beside value in the readout | Glow by fixed percentile cutoff |
| State focus with histogram against national range, generalised to "any parent region" | First-two-digits parent lookup |
| Shared-border mesh strokes | Hardcoded 975 × 610, Texas calibration, 350 px panel |
| The forgiving paste parser and its plain-spoken messages | Silent last-wins on duplicates; no unmatched-row count |
| The three props as the seed of a theme schema | Inline styles everywhere |

## Findings that feed later docs

- **→ 02_CONTRACT:** unknown `geo_id` must be counted and listed. The 2018 vintage guarantees it will happen with Connecticut and Alaska.
- **→ 02_CONTRACT:** duplicates need a stated rule, not last-wins.
- **→ 03_CONFIG_SCHEMA:** number formats must be expressible as data, such as a format string plus a unit, because functions cannot be saved.
- **→ 03_CONFIG_SCHEMA:** scale logic needs a tie rule and the legend must be generated from the scale, never written separately.
- **→ 01_OPTIONS, topology:** each topology needs to declare its own box, its parent lookup, and its vintage year.
- **→ 01_OPTIONS, rendering:** the pick-canvas trick is the strongest argument for staying on canvas. SVG gets hit testing free but pays at 10,000 shapes.
