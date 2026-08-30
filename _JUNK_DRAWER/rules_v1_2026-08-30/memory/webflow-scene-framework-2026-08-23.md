---
name: webflow-scene-framework-2026-08-23
description: "The composition-scene framework Chris means by 'the flow framework' — 21 named scenes with dense/quiet rhythm and one sun per page — and how it is built in Webflow"
metadata:
  type: project
---

**"The framework we have been talking about" = the composition-scene system**,
not a component swatch page. Getting this wrong cost a full build on
2026-08-23 (five components in a strip at the bottom of a scratch page —
Chris: "i thought you were building out the flow framework - part of the
actual site").

**What the framework is** (from the music/infographic rules Chris pasted
2026-08-23 plus the Board Segments generator in `reports/viz/board_segments.html`):

- **21 named composition scenes** — circle, fullbleed, starburst, tallcolumn,
  densefield, offcenter, diagonal, flatgrid, circlemirror, fullbleedstack,
  starbursteven, tallcolumnreversed, densefieldgrid, diagonalsteep,
  circletwoscales, staircase, nestedframe, splitspine, orbitring, anchorrail,
  terrace.
- Each is tagged **dense** or **quiet**; the sequencing rule is **a dense scene
  is never followed by another dense scene** (Chris's "tension, release").
- **One zone per page is the "sun"** — the melody, the one big idea. Rust border.
- Zones are sized **L / M / S**: L = lead chart / the big proof, M = a chart, a
  map, a paragraph, S = a stat, a quote, a caption.
- A page is a sequence of **five to seven scenes**.

**Built in Webflow 2026-08-23** on the site in
[[board-segments-webflow-2026-08-23]] (scratch Home wiped first, with Chris's
explicit go-ahead — "It was a scratchpad. Get rid of the shit"):

- Scenes are a **12-column CSS grid**, not the absolute-positioned 820px
  geometry of the sketch generator — `scene` + `zone` classes with `c1`-`c12`
  span combos, `st2`-`st10` start offsets, `h-s/h-m/h-l/h-xl` heights, and
  shape modifiers (`is-circle`, `is-ring`, `is-cut-l/r`, `is-texture`,
  `is-flat`, `is-sun`, `is-guide`). All colors/fonts/spacing bound to the 23
  existing Variables.
- Pages: **Home** (portfolio front), **Framework** (the 21-scene library, zones
  carry `is-guide` so the shapes are visible), **Investigation** (a worked page).
- `Site Nav` and `Site Footer` are components; the earlier five tile components
  survive as the visual kit.

**Webflow API traps hit** (save the next session the same detours):
- `data_element_builder` `set_text` **does not work** on TextBlock — those come
  back as plain Blocks holding a default string. Set text on the inner **String
  node** instead (`set_text` on the block itself errors "doesn't support text").
- **`data_whtml_builder` is the fast path**: it reuses existing global classes
  by exact name (no duplicates created) AND sets text correctly. Build markup
  with class attributes rather than assembling element trees.
- `FormBlockLabel`/`FormTextInput` are rejected outside a Form — use a `DOM`
  element with `dom_tag: "input"`.
- Attribute values **cannot be bound to component props** through this API
  ("value must be a string or a binding") — placeholders stay static.
- The **Body element cannot take a style** via the API; put background/type on
  a `page` wrapper div instead.

**Added later the same day (three learning-curve flatteners Chris picked):**
1. **Ten chart bricks** as components (group "Bricks") — the 108 chart types from
   `reports/viz/chart_vocabulary_field_guide.html` collapsed into: Ranked Bars,
   Trend Line, Distribution, Scatter, Map, Network, Flow, Range, Testimony,
   Stacked Share. Plots are inline SVG (confirmed to survive whtml insertion,
   including `currentColor`, which is how the mark color stays token-bound);
   secondary accent colors inside SVG are hardcoded hex — the one place the
   palette is not variable-driven.
2. **Deadspace notes** on all 21 scene headers, lifted verbatim-in-substance from
   `reports/viz/deadspace_and_counterweight.html` (8 shapes) and
   `board_segments_sketchbook.html` (13) — the picker's if-then logic delivered in
   Designer instead of a separate tool.
3. **Navigator names** on every scene and zone across Framework, Investigation and
   Home ("Scene 05 · dense field · dense", "Zone L · SUN · the proof"). The Bricks
   page was left unnamed — its zones hold already-named component instances.

**THE COMBO-CHAIN TRAP (cost a rebuild on 2026-08-23 — do not repeat):**
Webflow combo classes are CHAINS, not independent CSS modifiers. An element with
`zone col-4 h-l al-top` makes Webflow create a NEW EMPTY class at every level
past the first combo (`.zone.col-4.h-l`, `.zone.col-4.h-l.al-top`). The styled
combo `.zone.h-l` still applies — but only because the element's class *name*
matches.

So: **renaming a modifier combo silently unstyles every page using it.** Renaming
`h-l` → `tall` left every element still carrying `h-l`, matching nothing. Heights,
alignments, shapes, textures and the sun borders all went dead across six pages
with no error anywhere. Fixed by renaming all 18 modifiers back to their original
names.

Only the FIRST combo after the base class is the real style object, which is why
the `c1..c11` → `col-1..col-11` rename survived (width sits first in the chain)
while everything after it broke.

Practical rules: put the width class first; never rename a modifier combo after
pages exist; and when a rename is genuinely needed, rebuild the pages instead.
