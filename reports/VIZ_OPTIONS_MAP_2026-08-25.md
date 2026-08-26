# Warehouse Metrics → Visualization Options Map

**Dated 2026-08-25.** A menu, not a decision. No recommendation, no shortlist —
on purpose. The pick is Chris's. *(Optimized + Round 2 + polish pass, all
2026-08-25. Every concept now ends with a **Lift** — the single conceptual
design decision that would make that piece beautiful, not just correct. Facts
and scores unchanged; original archived in session scratchpad.)*

---

## How to use this

Two separate choices hide inside "how should I visualize this":

1. **The picture** — bar chart, river, dot grid, drawing? That's the *concept*.
2. **The tool** — what software draws it? That's the *library*.

Most people collapse the two and get their tool's default. This document keeps
them apart: **9 metric groups × 6-7 picture ideas each (60 concepts, plus 24
more + 3 more wild in Round 2 near the end — 93 total)**, each scored on nine
dimensions, then **30 tools** listed separately.

**Score direction:** more dots = better, always. Page weight and effort are
real numbers (KB, hours) because dots would hide what you'd want to know.

**The Lift lines:** each concept's *Lift* is the detail that separates a
portfolio piece from a dashboard widget — one decision, stated so it can be
kept or discarded deliberately. Lifts are design intent, not extra features;
none changes the effort or score estimates materially unless it says so.

**Static-first ruling (Chris, 2026-08-25): minimal moving parts or animation.**
The default for every piece is fully still. Lifts that added motion to
otherwise-static concepts have been rewritten static. Concepts that *cannot
exist* without continuous motion stay on the menu but are tagged and sit
outside the default — see the static-first note in the cross-cutting section.

---

## Already built (verified on disk this session)

| Existing page | What it does |
|---|---|
| scale gallery (10 scenes) | counting clock, pixel-per-entity field, printed tower, source skyline, domain treemap, ripple, powers-of-ten, build-over-time, human-scale arithmetic, map lighting up |
| chart vocabulary field guide | catalogue of chart forms, drawn once |
| infographic layout survey | page-composition patterns |
| warehouse biome page | mart row counts as a biome |
| spine tree page | spine axis → table membership as a tree |
| ten data pages (rate map, pill rivers, heartbeat, denial gap, waiting room, detention rivers, own clock, pulse grid, bank deserts, money shape) | the house style: dark "night water" palette, hand-rolled HTML + canvas, data baked in at build |

**[BUILT]** = exists in some form. **[NEAR-BUILT]** = variation on something
built. Context, not a ceiling — a second, better picture of a covered number is
a real option.

---

## Installed on this Mac (verified this session)

**Present:** Python 3.9 with plotly 6.6.0, altair 5.5.0, pandas 2.3.3,
numpy 2.0.2, networkx 3.2.1, pydeck 0.9.2, dash 4.4.1, Pillow 11.3.0,
duckdb 1.4.5. **Node v22.23.2** (via nvm — corrects the old "no Node" memory
note). Chrome (headless screenshotting).

**Absent:** matplotlib, seaborn, plotnine, datashader, bokeh, holoviews,
hvplot, pyecharts, kaleido, vl-convert-python, geopandas, graphviz, scipy.
**matplotlib being absent blocks five options below** (seaborn, plotnine,
PyWaffle, Datashader's mpl path, matplotlib itself).

---

## The numbers (from the audit, not re-derived)

| # | Metric group | The numbers |
|---|---|---|
| A | Warehouse scale | 7 databases · 5,436 objects · 3,350 tables · 2,086 views · 4,974,176,335 rows · 185.4GB |
| B | Per-database split | RAW 1.27B rows/2,212 tables · MARTS 1.31B/701 · META 1.50B/108 · PREDBT 894M/318 · STAGING 135,812/11 · THE_LIBRARY 0/0 (254 views) · TOOLS 0/0 |
| C | Registration gap + correction | 847 detected → 178 registered → corrected to 267 (via 289 mirrors, 37 mis-flagged, 14 derived, ~20 mart-only, 135 docket, 153 portal → 79 wired / 74 gaps, 30 federal → 11 wired / 19 gaps) |
| D | Entity graph scale | 33,312,349 golden entities · 84,382,504 keyset nodes · 181,002,484 match pairs · 176,983,257 working keysets · 4,910 edges · 17,598 leads |
| E | Overlap coverage | 24,011 measured pairs = 11,839 confirmed + 12,172 new; by key: DOCKET 6,560 (6,174 new), EIN 5,777 (1,790), NPI 3,711 (1,457), CCN 1,827 (853), CIK 1,649 (481), FRS_ID 1,217 (271), + 19 smaller key types down to MMSI (3) |
| F | DOCKET trust tiers | 45 trustworthy (federal courts) · 2,909 reclassified from "trust narrowly" to unverified · ~6,475 noise/unverified · 47% of cross-agency pairs share ≤5 values · one pair at 99.98% overlap that is pure coincidence |
| G | Dead weight | THE_LIBRARY 254 views / 0 rows · PREDBT 318 tables / 894,348,890 rows / 34.4GB · 2 spine backups at 272,607,989 rows each · one landing table stuck at exactly 20,000,000 rows (a cap, not a count) |
| H | The four-verb pipeline | SCOUT → COLLECT (2,212 landing tables, 1.27B rows) → CONNECT (267 registered, 84.4M nodes, 4,910 edges) → DETECT (17,598 leads) |
| I | Key trust tiers | Of 3,619 verified key columns: GEO 2,368 · STEEL 1,025 · STRONG 226. By what they identify: place 2,368 · organization 434 · facility 285 · case 226 · provider 176 · person 93 · asset 23 · vessel 14 |

---

# Reading the score tables

Same nine dimensions every time, no weighting — the weighting is yours.

| Column | Means |
|---|---|
| **Weight** | browser download for this one graphic (real KB) |
| **Effort** | hours: first working draft → portfolio-polished |
| **Interact** | does clicking/hovering add meaning? ●○○○○ decoration → ●●●●● interaction *is* the point |
| **Design** | ceiling with real design effort. ●○○○○ stuck ugly → ●●●●● magazine-grade |
| **Scale** | survives the real row counts without sampling? |
| **A11y** | colorblind-safe + screen-reader feasible. ●○○○○ canvas blob → ●●●●● real text/SVG |
| **Theme** | works in light and dark. ●○○○○ one theme → ●●●●● token-driven |
| **Regen** | rebuilds itself when the audit re-runs? ●○○○○ hand-tuned art → ●●●●● one script |
| **Wow** | differentiation vs. a generic dashboard chart |

**Standing honesty note:** ●●●●● Wow + ●○○○○ Regen = *art*, not a chart —
beautiful once, stale the moment the numbers change. That trade-off is real
everywhere below.

---

# A. Warehouse scale — the headline number

4.97B rows, 185.4GB, 5,436 objects, 7 databases. A human can't feel a billion —
every concept here is a different answer to *making 4.97B mean something.*

- **A1. Big-type stat block [BUILT]** — enormous numerals, one plain sentence
  each; typography carries it all. The gallery header already does this.
  *Lift:* never round — set all ten digits of 4,974,176,335 at poster scale,
  with "counted 2026-08-24" in small type beneath. The unrounded figure plus
  its exact date does the "still counting" work — completely still.
- **A2. Counting clock [BUILT]** — "one row per second" = ~158 years; an
  animated counter that visibly can't finish. Built as scene 1.
  *Lift:* the clock never resets — it remembers each visitor's position and
  resumes counting where they left off. Coming back a week later and finding
  it barely moved is the exhibit.
- **A3. One-pixel-per-entity field [BUILT]** — dots fill the screen into
  texture; the eye reads density directly.
  *Lift:* light exactly one pixel and caption it — "this one is a real
  hospital in Ohio." One named dot turns 33 million pixels of texture into
  33 million somebodies.
- **A4. Powers-of-ten ladder [BUILT]** — ten ×10 steps from one record to the
  warehouse, real-world comparison at each. Built as scene 7.
  *Lift:* at every step, keep the previous step visible as a tiny glowing
  square in the corner — a breadcrumb trail of scale, so the visitor never
  loses the thread of how far they've zoomed.
- **A5. Nested-square area nest (new)** — true-to-area squares nested four
  deep: warehouse → biggest database → schema → table. A *zoom*, not a treemap
  partition.
  *Lift:* draw it honestly enough that the innermost square nearly vanishes —
  then label the vanishing: "this table holds 63 million rows and you can
  barely see it." The chart's failure to show it IS the message.
- **A6. Physical-object scale stack (new)** — 185.4GB as ~125,700 floppy disks
  = a ~402m / ~1,320ft stack, taller than the Empire State roof (1,250ft),
  drawn beside a building. Static illustration, hand-composed.
  *Lift:* draw it in strict two-tone blueprint convention — elevation drawing,
  dimension lines, title block — and put a tiny aircraft-warning light on top
  of the disk stack. One deadpan joke that states the altitude.
- **A7. Scrolling odometer strip (new)** — the digits of 4,974,176,335 scroll
  past as the visitor scrolls, ticks marking each database's share. The number
  becomes a distance.
  *Lift:* mile-marker signage at each database boundary, and when the visitor
  inevitably stops scrolling, print where they gave up: "you made it to row
  212,004,318 — 4.3% of the way." Their surrender is the data point.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| A1 big type | ~2 KB | 1→4 | ●○○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| A2 counting clock | ~4 KB | 2→6 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |
| A3 pixel field | ~15 KB | 3→10 | ●●○○○ | ●●●●○ | ●●●○○ | ●●○○○ | ●●●○○ | ●●●●○ | ●●●●○ |
| A4 powers of ten | ~8 KB | 4→12 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●●○ | ●●●○○ |
| A5 nested squares | ~6 KB | 3→9 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |
| A6 physical stack | ~180 KB* | 8→30 | ●○○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●○○○ | ●○○○○ | ●●●●● |
| A7 odometer strip | ~5 KB | 4→14 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●● | ●●●●○ | ●●●●○ |

\* A6 as inline SVG drops to ~30 KB but drawing effort roughly doubles.

**Tools:** A1/A5/A7 plain HTML+CSS+SVG; A2/A3 canvas + ~40 lines JS; A4
either; A6 Pillow (installed), hand SVG, or p5.js. **No charting library needed
anywhere in this group.**

---

# B. Per-database breakdown — seven wildly different things

Three databases hold ~1.3B rows each, one holds 135,812, two hold zero. One
linear axis makes four of the seven invisible — that's the design problem.

- **B1. Log-scale horizontal bars (the honest default)** — real numbers printed
  on each bar so the log distortion can't mislead; the two zeros get an
  explicit "zero — not a short bar" treatment (log can't draw zero).
  *Lift:* draw each zero as a dotted outline of the bar it doesn't have, with
  a two-word verdict inside: "empty on purpose" vs. "empty by accident." The
  chart distinguishes intent — most charts can't.
- **B2. Small-multiple cards** — seven cards, each with its own tiny bars
  (rows/tables/views/GB); refuses to share an axis, so no scale problem.
  *Lift:* give every card a one-word character title over its stats — The
  Landing Zone, The Showroom, The Ledger, The Frozen Backup, The Workbench,
  The Empty Library, The Toolshed. The taxonomy becomes the design, and a
  visitor remembers seven characters where they'd forget seven bar charts.
- **B3. Treemap by database → schema [NEAR-BUILT]** — area = rows, two levels;
  the biome page does a marts-only version.
  *Lift:* in the night-water palette, map depth to darkness — descending from
  database to schema literally descends into deeper water. The hierarchy
  becomes a dive, not an outline.
- **B4. Stacked ribbon / horizon strip** — one band per database, height ∝
  log(rows), colored by layer role; reads like geological strata.
  *Lift:* commit fully to the core-sample: label the layers like a field
  geologist — bedrock (raw), sediment (marts), fossil layer (backups) — with
  a depth scale in rows down the side. Metaphor held with a straight face.
- **B5. Dot-matrix waffle grid** — 1 square = 10M rows, 497 squares grouped by
  database; the only form where the zero databases are as loud as the full ones.
  *Lift:* the two empty databases get full-size empty grids with their names
  set inside the blank space — silence given equal floor area, which no other
  chart form grants it.
- **B6. Bubble-in-a-box packing** — area ∝ rows; fast ranking, weak exact
  comparison, handles the zeros badly (a zero circle is a dot) — real weakness.
  *Lift:* if built anyway, draw the zeros as burst-bubble rings — a thin
  circle with a break in it. Absence rendered as a pop, not a dot.
- **B7. Tables-vs-rows scatter (both log)** — exposes what bars hide: RAW =
  2,212 tables / 1.27B rows, META = 108 tables / *more* (1.50B). Only this form
  shows that outlier.
  *Lift:* add faint diagonal guide lines of constant rows-per-table, so the
  eye reads "average table size" as position without doing math — and the
  metadata outlier sits visibly on the wrong diagonal, annotated in-plot.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| B1 log bars | ~3 KB | 1→4 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| B2 small multiples | ~6 KB | 2→7 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| B3 treemap | ~25 KB | 3→10 | ●●●●○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ |
| B4 strata ribbon | ~7 KB | 4→12 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| B5 waffle grid | ~10 KB | 3→9 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |
| B6 bubble pack | ~20 KB | 2→7 | ●●●○○ | ●●●○○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●○○○ |
| B7 tables-vs-rows scatter | ~4 KB | 2→6 | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |

**Tools:** all seven trivial in Vega-Lite/Altair (installed), Plotly
(installed), ECharts/pyecharts (not installed), or hand SVG. B3: `d3-hierarchy`
is the squarified-treemap algorithm most libraries wrap; ECharts and Plotly
ship treemaps natively. B5 in Python = PyWaffle (MIT) — but it sits on
matplotlib, **not installed here**.

---

# C. The registration gap and its correction — 847 → 178 → 267

The best story in the audit and the one a bar chart would ruin. Morning: 847
keyed tables, only 178 registered — a 669 backlog. Evening: mostly wrong — 289
mirrors, 37 mis-flagged, 14 not sources. Real backlog 183, of which 90 wired
that day. **The shape is "a number that corrected itself" — a before/after,
not a quantity.**

- **C1. Waterfall / bridge** — 847 stepping down through each deduction (−289,
  −37, −14, −20, −135) to 183, then to 90 wired / 93 gaps. The most literal
  form for "how a big number became small," self-labeling steps.
  *Lift:* color each falling step by the *kind of check that caught it* —
  automated dedup vs. a human actually reading the table. The waterfall stops
  being arithmetic and becomes a portrait of the checking itself.
- **C2. Before/after with connecting ribbons** — 847 block on the left,
  corrected buckets on the right, ribbon width ∝ tables; shows the "where did
  they go" a waterfall only states.
  *Lift:* draw the mirrors ribbon as two identical halves folding onto each
  other mid-flight — the form physically enacts "this was the same thing
  counted twice."
- **C3. Sankey of the full reconciliation** — 847 → 7 buckets, portal and
  federal splitting again into wired/gap; ~11 terminal nodes. Denser than C2,
  keeps the second-level split.
  *Lift:* order the terminal nodes resolved→unresolved top to bottom, so the
  reader's eye lands last on the 93 gaps. The honest residue is the final
  thing read — composition doing the disclosure.
- **C4. Sieve / filter-stack illustration** — 847 poured in the top, each mesh
  catching one category, 183 falling through. Static art; makes de-duplication
  legible to a non-data visitor.
  *Lift:* etch each mesh with the actual question that layer asked — "is this
  the same file twice?", "was this already registered?" — so the illustration
  documents the method, not just the outcome.
- **C5. Two-state toggle [interactive only]** — one button: "as first counted"
  / "after checking"; the bars re-arrange. The correction becomes something the
  visitor *does* — a strong honesty signal.
  *Lift:* label the two states with times, not words — "the 8am count" / "the
  10pm count." The toggle becomes a day you can flip back and forth, and the
  work it took lives in the gap between the labels.
- **C6. Struck-through number line** — 0→847 line, 847 struck and re-marked at
  183, deductions as labeled brackets. The printed-erratum look, deliberately
  plain.
  *Lift:* typeset it exactly like a book's errata page — the old value struck
  in red-pencil style, the correction in a marginal annotation hand. Borrow
  the full visual grammar of print correction, not just the strikethrough.
- **C7. Unit grid of 847 squares** — every table colored by its fate; the real
  backlog reads as a small minority, and the mirrors bucket is visibly a third
  of the whole.
  *Lift:* print a small ghost of the uniform morning grid beside the
  recolored evening grid — before/after as two stills, no animation. The
  visitor performs the blink comparison with their own eyes.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| C1 waterfall | ~4 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| C2 before/after ribbons | ~10 KB | 4→14 | ●●●○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| C3 Sankey | ~30 KB | 3→10 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●○○ |
| C4 sieve illustration | ~120 KB | 8→26 | ●○○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●○○○ | ●○○○○ | ●●●●● |
| C5 two-state toggle | ~8 KB | 5→16 | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| C6 struck number line | ~3 KB | 2→8 | ●○○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ |
| C7 847-square grid | ~12 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |

**Tools:** C1 native in ECharts and Plotly; in Vega-Lite it's a hand-built
stacked bar with transparent bases (~30 lines). C3 native in Plotly, ECharts,
`d3-sankey`. C2/C6/C7 hand SVG. C5 needs only vanilla JS over SVG.

---

# D. Entity graph scale — six orders of magnitude

Stage counts span 181M down to 4,910 (~37,000×), and the sequence is **not a
funnel**: 33.3M entities → 84.4M nodes → 181M pairs → 4,910 edges → 17,598
leads. It grows twice, collapses hard, grows again. **A funnel chart on these
numbers lies** (funnels assume each stage subsets the last); every concept must
handle that. *(It grows because one company can carry five ID types, and pairs
are combinatorial; scoring then discards almost everything.)*

- **D1. Log-scale stage strip (honest baseline)** — five bars, pipeline order,
  real number + one sentence each. Log is the only linear form where 4,910 and
  181M are both visible; bars don't imply subsetting, so the growth is honest.
  *Lift:* caption each bar with one verb — GATHER, SPLIT, PAIR, JUDGE, KEEP —
  so the axis reads as a sentence. Five bars become grammar.
- **D2. Sankey with expansion and collapse** — expansions drawn as fan-outs,
  the collapse as hard narrowing. A grammar that permits growth. Cost: the
  4,910 flow is a hairline at true scale — needs log-width or an inset.
  *Lift:* let the discarded flow fade to transparent instead of routing to a
  "rejected" node — 181 million candidates dissolving into the background,
  which is what rejection actually looks like. The survivors' thread stays
  crisp all the way across.
- **D3. Nested rings (÷10 per ring)** — ten concentric powers of ten, stages
  plotted at true radius; markers jumping in and out *is* the truth.
  *Lift:* style it as sonar — a slow sweep line, stages as pings that glow
  when swept, depth rings labeled in powers of ten. The pipeline becomes
  something being *searched*, which it is.
- **D4. Two-panel "grows then collapses"** — panel 1: expansion (linear axis);
  panel 2: collapse (log). Refuses to force one grammar onto two behaviors.
  *Lift:* title the panels like chapters — "The explosion" / "The verdict."
  Two named acts admit the story has two natures instead of apologizing for
  the split.
- **D5. Animated scrubber [interactive only]** — scroll/slider walk through the
  five stages, count-up + one sentence each, persistent mini-timeline. The
  expansion/collapse is felt as motion.
  *Lift:* tune the easing so the count races through the millions and then
  *brakes* — decelerating hard into 4,910 and stopping dead. The deceleration
  is the judgment; the visitor feels the cull in their scroll finger.
- **D6. Sand-through-a-funnel art** — five vessels, log-scaled, the middle one
  visibly overflowing its predecessor; a physical metaphor accepts "it grew"
  more easily than a funnel chart does.
  *Lift:* make it an hourglass, not a funnel — implying the process takes time
  and can be turned over and run again. The sand shifts color at the trust
  boundary: everything below the neck is a different, cleaner grain.
- **D7. Dot field with survivor highlight** — sampled match-pair fog with the
  4,910 survivors lit. Best for the emotional truth ("almost nothing
  survives"), worst for exact reading; needs explicit "1-in-N sample" labeling
  or it's dishonest.
  *Lift:* pin one survivor with a real annotation — the actual two datasets
  it connects, in plain words. One receipt pinned to the fog keeps the
  emotional picture attached to something checkable.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| D1 log strip | ~4 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| D2 Sankey | ~30 KB | 4→14 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●○○ |
| D3 nested rings | ~7 KB | 4→12 | ●●●○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| D4 two-panel | ~6 KB | 3→9 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| D5 scrubber | ~14 KB | 6→20 | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| D6 sand funnel | ~140 KB | 10→30 | ●○○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●○○○ | ●○○○○ | ●●●●● |
| D7 survivor field | ~60 KB | 5→16 | ●●●○○ | ●●●●○ | ●●○○○ | ●●○○○ | ●●●○○ | ●●●○○ | ●●●●● |

**Tools:** D7 is the one place **Datashader** earns its keep — server-side
rasterization of hundreds of millions of points into a PNG (docs claim
billions; v0.19.1; **not installed**, needs matplotlib/Numba). Alternative:
aggregate in DuckDB (installed), draw the grid in plain canvas — fewer deps,
more hand code.

---

# E. Overlap coverage — 24,011 measured table pairs

How much of the warehouse has been checked for connections, by ID type. 24,011
pairs: 11,839 confirm known links, 12,172 are new; 25 key types from DOCKET
(6,560) down to MMSI (3).

- **E1. Stacked bars by key type (confirmed/new)** — 25 rows sorted by total;
  the tail (DEA_NO 4, MMSI 3) gets a "+19 more" rollup or a zoomed inset.
  *Lift:* set "confirmed" in quiet gray and "new" in the accent color — the
  chart's color budget spent entirely on *what this audit added*. The gray
  is the platform; the color is the news.
- **E2. Slope chart, confirmed → new** — a line per key type; the steep risers
  (DOCKET 386 → 6,174) are the story: what this audit opened up.
  *Lift:* gray every line except the risers past a stated threshold, and
  annotate the steepest with its multiple ("×16") right on the line. A
  spaghetti chart becomes three colored lines and a crowd of context.
- **E3. Key-type matrix heatmap** — key types × coverage buckets, shading =
  pair count; a grid scans where 25 bars read as a list.
  *Lift:* put the real numbers *in* the cells and demote the shading to a
  whisper behind them — a designed numeric table where color assists reading
  instead of replacing it. More honest, and it prints.
- **E4. The actual network, aggregated** — 816 keyed tables as nodes, the
  24,011 overlaps bundled by schema pair into ~40 fat bundles. The only concept
  showing the *shape* of the map, not its counts.
  *Lift:* fix the layout by hand once, like a cartographer — domains in stable
  positions, labels placed with care — instead of letting a physics simulation
  land wherever it lands. The difference between a map and a hairball is that
  someone *drew* the map.
- **E5. Chord diagram by domain** — HEALTH/FINANCE/JUSTICE… arcs, thickness ∝
  overlaps. Answers what nothing else here does: **which subject areas touch.**
  ECharts 6 ships a native chord series (verified).
  *Lift:* dim the expected arcs (health↔health) and light the surprising ones
  (health↔justice) — the diagram points at its own discoveries instead of
  making the visitor hunt for them.
- **E6. Coverage-percentage histogram** — coverage_a_pct is already computed;
  the distribution is bimodal (spike near 100% = mirrors, spike near 0% =
  coincidence). That shape *is* the finding, invisible in every count form.
  *Lift:* label the two spikes in plain words directly on the chart — "same
  table, counted twice" over one, "strangers sharing a zip code" over the
  other. The annotations do the teaching; no caption needed.
- **E7. Filterable pair explorer [interactive only]** — pick a key type, see
  every pair plotted, click for its numbers. Proves the data is real and
  browsable, not a claim.
  *Lift:* never open on an empty search box — open mid-story, on one curated
  pair with its numbers already unpacked. The visitor arrives inside the
  evidence and works outward, instead of facing a blank tool.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| E1 stacked bars | ~8 KB | 2→7 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| E2 slope chart | ~6 KB | 3→9 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |
| E3 matrix heatmap | ~10 KB | 3→9 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ | ●●●●● | ●●○○○ |
| E4 bundled network | ~90 KB | 8→26 | ●●●●○ | ●●●●● | ●●●○○ | ●○○○○ | ●●●○○ | ●●●○○ | ●●●●● |
| E5 chord by domain | ~40 KB | 4→14 | ●●●●○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| E6 coverage histogram | ~5 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| E7 pair explorer | ~120 KB | 10→30 | ●●●●● | ●●●○○ | ●●●○○ | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ |

**Tools:** E4 = `d3-hierarchy` + hierarchical edge bundling, or live/draggable
via cosmos.gl (MIT, WebGL2, v3.0) or sigma.js v3 on graphology. **Licensing
caution:** cosmos.gl the engine is MIT, but *Cosmograph*, the friendly wrapper
on it, is **CC-BY-NC-4.0 — non-commercial only**; a portfolio site is a gray
area there, the MIT engine isn't. E5 chord native in ECharts 6 and `d3-chord`.

---

# F. The DOCKET trust breakdown — the honesty centerpiece

Of 6,560 docket overlaps: 45 trustworthy, 2,909 *actively downgraded*
mid-audit, ~6,475 noise/unverified. The trustworthy share is **0.7%**, and one
pair overlaps at **99.98% purely by coincidence** — the two most visually
interesting facts you have.

**Governing note:** a bar chart renders the 45 as a hairline next to 6,475 —
underselling the finding. "We found 45 real ones" is the *good news*; the form
has to let it be seen.

- **F1. Icon array, 6,560 dots, 45 lit** — the literal answer to "how rare is
  rare"; 0.7% is felt, not read. 100×66 grid → ~6px dots at 700px wide, legible.
  *Lift:* compose it as stars over night water — 6,515 dots barely brighter
  than the dark, 45 in warm gold. Under it, one line: "…and that's all of
  them." The house palette was built for exactly this picture.
- **F2. Three-tier stack with a correction mark** — TRUST / RECLASSIFIED /
  DON'T TRUST sized to count, the 2,909 band carrying a "was: trusted" ghost.
  *Lift:* render the ghost as a true afterimage — the band's former position
  faintly visible above where it now sits, like a shape that moved and left
  its light behind. The correction becomes physics, not a footnote.
- **F3. Coverage-vs-plausibility scatter with a labeled trap** — X = coverage
  %, Y = shared values (log). Federal courts cluster high-right; the
  FDIC/CourtListener dot sits at 99.98% labeled *"coincidence — small ID space
  inside a huge one."* One dot carries the whole argument for
  coincidence-scoring.
  *Lift:* title the piece **"The pair that lied"** and give the coincidence
  dot a museum-plaque caption. One villain, named and framed, teaches
  coincidence-scoring better than any legend.
- **F4. The 47% short-string histogram** — shared-value counts across ~3,600
  cross-agency pairs, ≤5-value region shaded; 47% of the mass means "these
  tables share four numbers, by chance." Blunt, cheap, devastating.
  *Lift:* render the bars in the ≤5 zone with a crumbling dither texture —
  visibly disintegrating — against solid bars beyond it. Statistical dust,
  drawn as dust.
- **F5. Reclassification flow** — small Sankey, the 2,909 visibly moving from
  "trust narrowly" to "unverified." Subject: *the audit correcting itself.*
  *Lift:* stamp the moving band with the date and the plain sentence that
  triggered it ("same-agency pairs had been counted as cross-checks"). A
  correction with a timestamp and a cause reads as integrity; one without
  reads as noise.
- **F6. The 45, named** — no chart; a designed table of all 45 trustworthy
  pairs (publishers, coverage %, shared cases). "Here are the 45, by name"
  beats any chart of 6,560 for credibility.
  *Lift:* typeset it as a formal register — numbered 01–45, rule lines,
  small-caps headings, the register of record for the whole platform. The
  formality *is* the design; it should look like something you'd swear on.
- **F7. Two-color skyline of all 6,560** — 1px line per pair, sorted by
  coverage, colored by tier; the trustworthy sliver shows as a band at one end.
  Dense, printable, unusual.
  *Lift:* title it **"The silhouette of noise,"** and in the print version,
  foot it with all 45 trustworthy pairs named in fine type — the skyline
  above, its only real citizens listed below.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| F1 icon array | ~20 KB | 3→10 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |
| F2 tier stack + strike | ~5 KB | 3→10 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●●●○ |
| F3 annotated scatter | ~35 KB | 4→14 | ●●●●○ | ●●●●● | ●●●●○ | ●●●○○ | ●●●●● | ●●●●○ | ●●●●● |
| F4 short-string histogram | ~5 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| F5 correction flow | ~25 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| F6 the 45, named | ~8 KB | 2→8 | ●●●○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ |
| F7 6,560-line skyline | ~30 KB | 4→12 | ●●○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● |

**Tools:** F1 as SVG is 6,560 `<rect>`s ≈ 200-300 KB of markup — better as one
canvas draw or a CSS grid of divs; PyWaffle does it as a PNG (MIT, needs
matplotlib, absent). F3/F4: Vega-Lite or Plotly, both installed. F7: one
canvas loop, no library.

---

# G. Dead weight — the waste story

Roughly a third of the warehouse does no work: one database is 254 empty
views; another is a frozen 894M-row / 34.4GB backup; two spine backups hold
272,607,989 rows *each*; one landing table sits at exactly 20,000,000 rows — a
loader cap masquerading as a count.

**The framing is itself a taste call:** *waste* story (money/space), *rigor*
story (we found and named it), or *housekeeping* story (cleanup list). The
concepts split along those framings.

- **G1. Live vs. dead donut in GB** — 185.4GB total, ~59GB dead; one ring, two
  colors, number in the middle. Simplest waste framing.
  *Lift:* give the dead arc a flat, desaturated tone that visibly does not
  belong to the site's palette — dead even in color. The living arc gets the
  night-water blues; the dead arc gets cardboard.
- **G2. Floorplan with dead rooms greyed** — seven rooms sized by storage,
  dead ones grey with a why-label. Makes "33% waste" spatial and
  non-technical-readable.
  *Lift:* full architectural convention — wall lines, door swings, a title
  block — with the dead rooms diagonal-hatched and door-tagged CONDEMNED:
  followed by the reason. Building-inspector deadpan, held throughout.
- **G3. The truncation trap, magnified** — one chart: the 20.0M bar beside the
  re-pull's 63.7M, round number circled, caption "round numbers are almost
  always a cap, not a count." Teaches a transferable idea.
  *Lift:* typeset 20,000,000 with the seven zeros at display size — the
  roundness itself is the exhibit. The caption is phrased as a rule the
  visitor can steal and use on their own data tomorrow.
- **G4. Duplicate-pair strip** — every twice-existing table as a paired mark,
  sorted by size; the 289-mirror finding as a repeated visual rhythm.
  *Lift:* draw each pair as a reflection across a horizontal waterline — the
  original above, its copy mirrored below, slightly dimmed. The mirror
  finding drawn as an actual mirror, in the house's water idiom.
- **G5. The empty-shelf illustration** — the empty database drawn as a library:
  254 shelf slots, 26 labeled sections, all bare. The one concept where "zero"
  is the subject, not an absence.
  *Lift:* one shelf holds a single yellowed card: "reserved." 254 empty slots
  and one small joke — restraint everywhere, wit in exactly one place.
- **G6. Cost-framed bar** — dead storage as monthly dollars. **Blocked today:
  no billing visibility on this account**, so no honest price per GB exists.
  Listed as real, flagged as unbuildable now.
  *Lift:* if ever built before billing access lands, design it as a price tag
  with the amount blank and "pending" stamped across it — the blocker itself
  drawn as the graphic, which is more honest than an estimate.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| G1 live/dead donut | ~4 KB | 1→4 | ●●○○○ | ●●●○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| G2 floorplan | ~40 KB | 6→20 | ●●●○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●○○ | ●●●●● |
| G3 truncation trap | ~3 KB | 1→5 | ●○○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ |
| G4 duplicate strip | ~10 KB | 4→12 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |
| G5 empty shelves | ~90 KB | 6→20 | ●○○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●○○○ | ●○○○○ | ●●●●● |
| G6 cost bar | ~3 KB | 1→4 | ●○○○○ | ●●●○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●○○○ |

---

# H. The four-verb pipeline — the system diagram

SCOUT (catalogs portals, tags key types) → COLLECT (2,212 landing tables,
1.27B rows) → CONNECT (267 registered, 84.4M nodes, 4,910 edges) → DETECT
(17,598 leads). **The one graphic a visitor most needs** — every other number
is meaningless without it — and the one where a generic four-box diagram is the
biggest missed opportunity.

- **H1. Four boxes, arrows, live counts** — the baseline; clean typography, a
  count and one sentence per stage. Boring but it definitely communicates.
  *Lift:* set the four verbs in stenciled crate lettering with the counts as
  manifest lines beneath — industrial shipping-label typography. Utilitarian
  on purpose, and suddenly the boring version has a voice.
- **H2. Widening-then-narrowing pipe** — pipe diameter tracks volume per stage;
  the "we throw almost everything away" message with zero caption.
  *Lift:* end the pipe at a small tap over a waiting dish — 17,598 leads as
  the distillate of 1.27 billion rows. The dish is the whole point of the
  machine, drawn at its true, humble size.
- **H3. Layered stack with drill-downs [interactive]** — click a band to expand
  its internals (COLLECT → source families; CONNECT → trust tiers). One diagram
  for the five-second and the five-minute visitor.
  *Lift:* two registers, one component: closed bands speak in single plain
  sentences, opened bands swap prose for pure numbers. The click changes not
  just what you see but what language the diagram speaks.
- **H4. Assembly-line / factory illustration** — isometric: raw material in,
  four machines, a small tray of leads out. Most designed, most screenshotable.
  *Lift:* light it as the night shift — four machines glowing in a dark
  warehouse. "Shining a light on hidden harm" is the mission sentence; this
  is the one graphic that can draw it literally without saying it.
- **H5. One record's journey** — follow ONE real row from government file to
  lead, each verb acting on it. Teaches best, shows scale worst.
  *Lift:* format it as a chain-of-custody document — the record as an
  evidence item, each verb a dated stamp and initials. The pipeline becomes
  a custody chain, which for a trust-obsessed platform is the perfect frame.
- **H6. Live status version** — the four boxes carrying freshness states from
  the source-freshness table; diagram doubles as a health readout. Highest
  maintenance; the picture keeps changing after you ship it.
  *Lift:* express freshness as weather — clear, overcast, storm — one glyph
  per box. It borrows the platform's own internal weather vocabulary, so the
  public diagram and the internal language become the same picture.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| H1 four boxes | ~4 KB | 1→5 | ●○○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| H2 widening pipe | ~8 KB | 3→12 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| H3 layered drill-down | ~15 KB | 6→20 | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●○○ |
| H4 factory isometric | ~150 KB | 12→36 | ●○○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●○○○ | ●○○○○ | ●●●●● |
| H5 one record's journey | ~10 KB | 5→18 | ●●●○○ | ●●●●● | ●○○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ |
| H6 live status boxes | ~12 KB | 6→18 | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●●○ |

**Tools:** H1/H2 hand SVG. Graphviz (not installed) auto-lays-out H1-style
diagrams but its academic default look is hard to design past. H4 needs an
illustrator or generative pass — not a chart library.

---

# I. Key trust tiers — what counts as proof

The four-tier vocabulary (STEEL = hard government ID, STRONG = narrower code,
GEO = location, PROBABILISTIC = a name) with real counts: of 3,619 verified key
columns — GEO 2,368, STEEL 1,025, STRONG 226. By what they identify: place
2,368, organization 434, facility 285, case 226, provider 176, person 93,
asset 23, vessel 14. **The hidden finding: the most common key type (location)
is the weakest.** Most concepts below exist to make that visible.

- **I1. Tier ladder** — STEEL top, PROBABILISTIC bottom; position = trust, bar
  length = quantity. The inversion (biggest bar, weakest rung) is the payload.
  *Lift:* draw the rungs in their actual materials — a steel bar, cut timber,
  a chalk line, a pencil stroke. Material = trust, felt before it's read; the
  huge bar resting on the chalk rung makes the inversion physical.
- **I2. Quantity-vs-trust quadrant** — X = how many columns, Y = how much it
  proves; GEO bottom-right, STEEL top-left. The trade-off as a position.
  *Lift:* write plain verdicts into the corners — "everywhere, proves little"
  / "rare, proves a lot" — so the plot reads like an editorial with no
  caption. The corners do the arguing.
- **I3. Entity-grain sunburst** — inner ring = tier, outer = what it
  identifies. Two questions in one shape.
  *Lift:* outline the person-grade segments in the warning color — the one
  place the ethics question is drawn *into* the chart rather than footnoted
  under it.
- **I4. The proof gradient** — a continuous "fact → hint" gradient with key
  types placed along it, sized by count. Rejects the four-bucket framing for
  the continuum it approximates — arguably more honest, less standard.
  *Lift:* print the four bucket names as fading tick labels *underneath* the
  continuum — the buckets visibly admitting they're approximations of the
  smooth truth above them. A chart that shows its own simplification.
- **I5. Evidence cards** — four cards, each a *real example value* (an actual
  EIN, ZIP, name) with "what this proves." Teaches by showing.
  *Lift:* design them as literal evidence bags — translucent sleeve, item
  tag, case number. The courtroom metaphor made physical, which is exactly
  the register the trust doctrine speaks in.
- **I6. Pictogram rows** — eight entity grains as icon rows, 1 icon = 10
  columns; vessels (14) and assets (23) as slivers beside place's 237 icons.
  Makes the rare types visible as rare.
  *Lift:* use each entity's own silhouette — ships for vessels, buildings for
  facilities, figures for people. The 14 vessels become a tiny flotilla of
  one-and-a-half ships; rarity rendered as charm instead of as a short bar.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| I1 tier ladder | ~4 KB | 2→6 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| I2 quadrant | ~5 KB | 3→10 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ |
| I3 sunburst | ~30 KB | 3→10 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●○○ |
| I4 proof gradient | ~5 KB | 4→14 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●●○ | ●●●●● |
| I5 evidence cards | ~6 KB | 2→8 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●●●○ |
| I6 pictogram rows | ~12 KB | 3→10 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●●○ |

**Caution on I5:** real example values on a public site = publishing real
identifiers. Org EINs/ZIPs are public record; anything person-grade is not the
same call. **RED-lane decision — flagged, not made.**

---

# The library capability matrix

Picking a *tool* is separate from picking a *picture*. **Verification rule:**
✅ = checked against current docs or the local install this session; ⚠️ = from
general knowledge, NOT re-verified — do not treat as fact.

## Python, static-image output

| Tool | Version / license | Installed? | Interactive | Scale ceiling | Static export | Note |
|---|---|---|---|---|---|---|
| **matplotlib** | 3.11.1, Jul 2026 ✅ / BSD ⚠️ | ❌ | none | ~100k points | PNG/SVG/PDF, best in class | 3.11 overhauled text/fonts (HarfBuzz) ✅. Total control, ugly defaults, real design possible via stylesheets. Five options below depend on it. |
| **seaborn** | ⚠️ / BSD ⚠️ | ❌ | none | inherits mpl | via mpl | Statistical layer; buys little here — these are counts, not distributions (except F4/E6). |
| **plotnine** | 0.15.7, Jun 2026 ✅ / MIT ⚠️ | ❌ | none | inherits mpl | via mpl | ggplot2 grammar in Python; most fluent if you think in channel mappings. |
| **Datashader** | 0.19.1 ✅ / BSD ⚠️ | ❌ | none alone | **billions of points** ✅ | PNG | The only Python tool built for the 181M/84M numbers; browser downloads a picture, not data. Needs Numba; pairs with HoloViews for interactivity. |
| **PyWaffle** | ⚠️ / MIT ✅ | ❌ | none | thousands of icons | via mpl | Icon arrays — relevant to F1/I6. Requires matplotlib. |
| **NetworkX** | 3.2.1 ✅ / BSD ⚠️ | ✅ | none | slow past ~10k nodes | via mpl | Graph *algorithms*, not drawing — compute the layout, draw elsewhere. |
| **Graphviz / PyGraphviz** | ⚠️ / EPL ⚠️ | ❌ | none | thousands of nodes | SVG/PNG | Best auto-layout for H1-style diagrams; academic look, hard to design past. |
| **Pillow** | 11.3.0 ✅ / MIT-CMU ⚠️ | ✅ | none | pixel-bound | PNG/JPG | A pixel canvas, not a chart library — the Python route to A6/D6/G5 metaphor art. |

## Python → interactive web output

| Tool | Version / license | Installed? | Interactive | Scale ceiling | Static export | Note |
|---|---|---|---|---|---|---|
| **Plotly (py)** | 6.6.0 ✅ / MIT ⚠️ | ✅ | strong | ~50-100k SVG pts; WebGL higher | needs kaleido (**not installed**) | Fastest dataframe→interactive path on this machine; default look is recognizably "Plotly," polish takes real theming. Writes standalone HTML. |
| **plotly.js** | full 3.3MB raw / 1.2MB min / ~391KB gz; "basic" ~318KB gz ✅ | (bundled) | strong | as above | — | **The page-weight problem of this document** — ~318KB gz minimum, more than every hand-rolled option combined. |
| **Altair / Vega-Lite** | altair 5.5.0 ✅ (6.x exists ✅) / BSD ⚠️ | ✅ | good (signals) | tens of thousands of marks | via **vl-convert-python** — no Node/browser ✅ (not installed) | Declarative JSON spec = **best regeneration story here**; the audit script can emit the chart. |
| **Bokeh** | ⚠️ / BSD ⚠️ | ❌ | strong | good | headless-browser PNG ⚠️ | Real edge is server callbacks — which a static portfolio page doesn't need. |
| **HoloViews / hvPlot** | 1.23.x ✅ / BSD ⚠️ | ❌ | strong | **inherits Datashader** ✅ | via backend | The documented path to *interactive* views of hundreds of millions of points — unique in Python. |
| **pyecharts** | 2.1.0, Feb 2026 ✅ / MIT ✅ | ❌ | strong | ~100k+ via canvas | — | Wrapper over ECharts, which has the best editorial default look of the mainstream libraries. Standalone HTML. |
| **Apache ECharts (js)** | 6.1.0 ✅ / Apache-2.0 ✅ | (CDN/inline) | strong | canvas, good | SVG or canvas | v6 added **native chord + matrix coordinate system** ✅ (→ E5, E3); treemap, sunburst, sankey, graph, rivers built in. |
| **pydeck / deck.gl** | pydeck 0.9.2 ✅ / deck.gl v9, WebGL2 ✅ / MIT ⚠️ | ✅ pydeck | strong, GPU | **millions of points** | — | Geo-first but works for abstract point clouds. WebGPU not enabled in 9.0 ✅ — WebGL2 is what ships. |
| **Panel / Dash** | dash 4.4.1 ✅ / MIT ⚠️ | ✅ dash, ❌ panel | full app | per backing chart | — | **Both need a live Python server** — a hosting commitment, not a chart. Structural mismatch with a static site. |

## JavaScript, for the site itself

| Tool | Version / license | Interactive | Scale ceiling | Static export | Note |
|---|---|---|---|---|---|
| **D3.js** | 7.9.0 latest, **no v8** ✅ / ISC ⚠️ | anything you write | SVG ~10k marks; canvas millions | SVG string | Toolkit, not chart library. Highest control and design ceiling; costs hand code. Sub-modules (`d3-hierarchy`, `d3-sankey`, `d3-chord`, `d3-scale`) work **without** the rest — that's how the page stays light. |
| **Observable Plot** | version ⚠️ / ISC ⚠️ | good | thousands of marks | SSR via JSDOM ✅, but docs: "only practical for simple plots of small data" ✅ | D3's grammar, far less code; stylesheet now inlined in the SVG ✅ — clean single-file embeds. |
| **Observable Framework** | 1.13.4 ✅ / open source, exact license ⚠️ | full | data loaders precompute ✅ | it *is* a static site generator | If this becomes a whole data site: the audit script becomes a data loader, site builds static. |
| **cosmos.gl** | v3.0 ✅ / **MIT** ✅ / `@cosmos.gl/graph` ✅ | GPU force-graph | "hundreds of thousands of points/links" ✅ | canvas snapshot | OpenJS incubating ✅; luma.gl rendering since v3 ✅. The serious option for a *live* E4. |
| **Cosmograph** | **CC-BY-NC-4.0 — non-commercial only** ✅ | as above, friendlier | as above | — | ⚠️ Licensing flag: portfolio = gray zone. The MIT engine above has no restriction. |
| **sigma.js + graphology** | v3 ✅ / license ⚠️ | strong, WebGL | "thousands of nodes/edges" ✅ | — | Established WebGL graph option; graphology cleanly splits data/layout from rendering. |
| **three.js** | ⚠️ / MIT ⚠️ | full 3D | GPU-bound, very high | — | Big bundle, big effort, big differentiation. Overkill for charts; correct for two wild ideas below. |
| **regl** | ⚠️ / MIT ⚠️ | low-level WebGL | millions of points | — | Thin WebGL layer for a custom million-dot field with no framework. |
| **p5.js** | ⚠️ / LGPL ⚠️ | creative-coding | canvas-bound | canvas snapshot | Generative/sketch route for metaphor art (A6/D6/G5). |
| **rough.js / roughViz** | rough.js <9kB gz ✅; roughViz 2.0.5, D3v5 ✅ / MIT ⚠️ | basic | small data | SVG | Sketchy aesthetic; its own docs say "intent or generality, not absolute precision" ✅ — an argument against it for audit numbers, for it on concept diagrams. |
| **Chart.js / Recharts / Nivo** | ⚠️ none verified | standard | thousands | varies | The web-dev default tier — visually identical to every dashboard, the opposite of a portfolio piece. |
| **LayerCake (Svelte)** | ⚠️ / MIT ⚠️ | full | your call | SSR-able | Only relevant if the site is already Svelte. |
| **DuckDB-WASM** | duckdb 1.4.5 local ✅; WASM build ⚠️ | in-browser SQL | millions of rows client-side | — | Lets a visitor *query* the audit data live. Relevant to E7 and wild idea W4. |
| **Highcharts / Flourish / Datawrapper** | ⚠️ / **commercial** | strong | varies | yes | Paid tier; genuinely good editorial output near-zero code. **Cost/licensing not verified — needs a price tag before it's a real option.** |

---

# Cross-cutting notes

### Page weight, ranked
- **Hand SVG/CSS:** 2-15 KB — nothing beats it.
- **Static PNG from Python:** 30-200 KB, zero JS, works with JS off, lazy-loads.
- **Vega-Lite embed:** spec ~2-10 KB, but the runtime is a few hundred KB ⚠️ (not measured).
- **plotly.js:** ~318 KB gz minimum ✅ — the heaviest common choice here.
- **WebGL:** hundreds of KB to MBs, and renders nothing without working WebGL.

**The editorial hybrid:** ship a static image, load the interactive version
only on "explore this" click. Fast page *and* deep option — static vs.
interactive isn't actually an exclusive choice.

### Where interactivity earns its place
- **Earns it:** E7 (browsing 24,011 pairs), H3 (two audiences, one diagram),
  C5 (the correction as an action), D5 (walking the stages).
- **Decoration:** hover-tooltips on a 7-bar chart. A printed number label costs
  0 KB and works on touchscreens.

### Static-first — the ruling, applied to all 93 (Chris, 2026-08-25)

The menu now sorts into three motion classes. This is the standing default,
not a per-piece suggestion:

- **Fully still (the default — ~75 of 93):** everything not listed below.
  Type, SVG, printed numbers, illustrations. No animation, no state.
- **Light interaction, no continuous motion (acceptable):** one click or
  scroll and it's still again — C5 (one toggle), H3 (click to expand), E7
  (filterable explorer), A7/A11 (scroll-driven, moves only when the visitor
  scrolls), F8 (a drawn lens, zero motion despite looking dynamic), W4 (type
  a query), W5 (two sliders).
- **Continuous motion is the concept (outside the default):** A2 (counting
  clock — already built, grandfathered), C9 (digit morph), D5 (animated
  scrubber), H6 (live-updating status), W1 (walkable 3D city), W2 (audio),
  W9 (timelapse). These stay on the menu because a menu keeps its options,
  but they now carry this ruling against them.

### Accessibility, by technology
- **SVG/HTML:** real DOM nodes — aria-labels and text alternatives work. Best case.
- **Static image:** one `alt` attribute. Limited but honest, never breaks.
- **Canvas/WebGL:** a screen reader sees an empty box. **Every canvas concept
  (A2, A3, D7, F1-as-canvas, F7, E4, all WebGL) needs a hand-written parallel
  text/table** — real work NOT included in the effort estimates above.
- **Color:** trust tiers encoded by color need a colorblind-safe ramp PLUS a
  second channel (shape/position/label) — ordered categories are exactly where
  color-alone fails.
- **Motion:** under the static-first ruling, only the inherently-motion
  concepts animate at all — and any that gets built needs a
  `prefers-reduced-motion` static fallback, planned up front.

### Light/dark theme
CSS-variable graphics flip free. PNGs need **two exports per theme change** —
doubling regeneration for every static image. Existing pages are dark-only,
which sidesteps this; adopting a light theme later reopens it for every static
image ever exported.

### Regeneration — what decides whether this ages
- **Regenerates itself:** anything where the audit emits data and a template
  renders it (chart grammars, hand SVG from JSON).
- **Doesn't:** every illustration/metaphor concept (A6, C4, D6, G2, G5, H4) —
  drawings with numbers in them; when the numbers change, someone redraws.
  That's the price of the highest Wow scores, paid knowingly.

The repo's existing pattern (extract to JSON → template placeholder →
string-replace at build) already covers the first case.

---

# The wildest ideas

Kept in deliberately, including the impractical. None is being suggested — a
menu of only safe options isn't a menu.

- **W1. The warehouse as a walkable city** — every table a building (height ∝
  rows, district = schema, materials = layer); the dead databases an unlit
  district of 254 empty storefronts. *Tool:* three.js, or deck.gl polygons for
  flat isometric. *Risk:* very high — 15-60+ hours, MBs of bundle, dead on
  low-end phones, needs a full text alternative, can read as tech demo. Also
  the single most differentiated thing on this list.
  *Lift:* spawn the visitor at the city's most-connected intersection — the
  single best-linked table — with the skyline receding in every direction.
  First impression: you are somewhere specific in something vast.
- **W2. Sonification** — each database an instrument; the docket noise becomes
  literal noise, the 45 trustworthy pairs 45 clean bell strikes. ~40s audio +
  visual score. *Tool:* Web Audio API; optionally Tone.js ⚠️. *Risk:* high and
  pure taste — striking or gimmick, little middle. Upside: the only concept
  fully accessible to a blind visitor *by design*.
  *Lift:* end the piece with ten seconds of only the 45 bells, the noise floor
  cut dead. Trust, rendered as the silence after the static.
- **W3. The broadsheet** — the audit set as a newspaper front page, with a
  boxed **CORRECTION** notice carrying the 2,909 reclassification and 847→183
  re-count in genuine erratum register. *Tool:* HTML/CSS + editorial typeface,
  inline SVG charts. *Risk:* low technically, high on execution — bad pastiche
  looks cheap instantly. Payoff: "we correct ourselves in public" becomes the
  *form* of the page.
  *Lift:* date the masthead with the audit date and mark it "SECOND EDITION" —
  corrections as editions. Re-running the audit prints the next edition, which
  quietly gives this art concept a regeneration story.
- **W4. Don't trust me — run it yourself** — an embedded query engine with the
  audit CSVs; visitors type SQL and get the page's numbers themselves, plus
  preset query buttons. *Tool:* DuckDB-WASM (local DuckDB 1.4.5 ✅; WASM size/
  version ⚠️). *Risk:* medium-high — several MB of WASM, and it invites
  scrutiny; whether that's the point or a liability isn't a design question.
  *Lift:* pre-fill the query box with the query that would *disprove the
  page's biggest number if it were wrong*. Opening on the hardest question
  you could be asked is the strongest trust gesture available.
- **W5. The coincidence machine** — two sliders set two ID ranges; the visitor
  watches false overlap climb toward 100% with zero real connections, then one
  button: "this is the 99.98% pair." *Tool:* ~150 lines vanilla JS + SVG.
  *Risk:* low technically; it teaches distrust of overlap numbers — including
  yours. Most credible thing on the site or a self-inflicted wound; not a
  technical judgment.
  *Lift:* start the sliders already set to the real pair's actual ranges — the
  visitor's first act is *discovering* the trap is real, not building a toy
  version of it.
- **W6. The entity constellation, printed** — 33.3M entities as a generated
  star field at poster resolution, A1 print + deep-zoom web image. *Tool:*
  Pillow (installed) or Datashader; tiling zoom viewer. *Risk:* medium —
  regenerates badly (it's art) and star fields are well-worn; its strength is
  existing off the screen.
  *Lift:* name the clusters like constellations — The Providers, The Vessels,
  The Facilities — with a proper astronomical legend. A star chart, not a
  scatter plot; the legend is what makes it a map of something.

---

# ROUND 2 — 24 more concepts + 3 more wild ideas

**Added later on 2026-08-25, second brainstorm pass.** Same groups, same nine
scoring dimensions, deliberately different angles from Round 1: derived ratios,
editorial formats, matrix forms, and comparisons to things people already know.
**Not yet in the interactive options board.** Data-availability flags are
honest: anything needing numbers not already in the audit CSVs says so.

---

## A. Warehouse scale — four more

- **A8. Famous-dataset ranking shelf** — one bar chart placing the warehouse
  among datasets people have heard of (all English Wikipedia, a national
  census file, a music-service catalog). "You are here" among the known.
  ⚠️ Comparison figures are general knowledge, unverified — each needs a
  sourced number before publishing.
  *Lift:* set it as a museum wall label — small type, generous margins, the
  warehouse's entry in bold among its peers. "You are here" delivered in the
  visual language of an institution.
- **A9. The Excel wall** — Excel maxes out at 1,048,576 rows per sheet; the
  warehouse is **~4,744 completely maxed-out spreadsheets**. Draw the wall of
  spreadsheet icons. Instantly meaningful to anyone who's ever hit that limit.
  *Lift:* draw one spreadsheet open, scrolled to row 1,048,576 — the exact
  wall every analyst has hit — and behind it, the other 4,743 as spines on a
  shelf. The known frustration in front, the unthinkable quantity behind.
- **A10. The download clock** — how long to download 185.4GB: ~4.1 hours at
  100 Mbps, ~25 minutes at gigabit. The size stated as *your time*.
  *Lift:* render it as the download dialog everyone has stared at — progress
  bar, "3.1 hours remaining" — frozen at 25%. Instant recognition, mild
  dread, message delivered.
- **A11. The bottomless scrollbar [interactive]** — a page whose scrollbar
  represents every row; the thumb is sub-pixel and the bottom is unreachable.
  One control everyone already understands, repurposed as the exhibit.
  *Lift:* add a magnifier callout showing the scrollbar thumb at true scale —
  a sliver thinner than one pixel — beside the enlarged version you can
  actually grab. The interface element itself becomes the scale comparison.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| A8 ranking shelf | ~4 KB | 2→7 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●○○ | ●●●○○ |
| A9 Excel wall | ~8 KB | 2→8 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●●○ |
| A10 download clock | ~3 KB | 1→4 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| A11 bottomless scrollbar | ~6 KB | 4→14 | ●●●●● | ●●●○○ | ●●●●● | ●●○○○ | ●●●●● | ●●●●● | ●●●●● |

## B. Per-database breakdown — three more

- **B8. Parallel-coordinates profile lines** — four vertical axes (rows,
  tables, views, GB), one line per database. The *shape* of each line is its
  personality: the metadata database spikes on rows while staying low on
  tables; the landing database does the reverse. Round 1 had no
  multi-metric form at all.
  *Lift:* present each line as that database's *signature* — seven scrawls,
  one per database, with the axes faded back. You learn to recognize them by
  handwriting, which is exactly what a profile line is.
- **B9. Marimekko / mosaic** — column width = table count, height = average
  rows per table, so area = total rows. Tall-and-thin vs. short-and-wide is
  the story bars can't tell.
  *Lift:* annotate directly inside the extreme columns — "few tables, enormous
  ones" written vertically up the tall thin column. The shapes get to explain
  themselves in their own space.
- **B10. Average-table-size bars** — a derived ratio Round 1 never plotted:
  rows per table. META ~13.9M avg · PREDBT ~2.8M · MARTS ~1.9M · RAW ~574k ·
  STAGING ~12k. Flips the intuition — the "biggest" database has the
  *smallest* average tables.
  *Lift:* frame it as "average serving size" — plates of proportional size at
  the end of each bar. The kitchen metaphor makes the inversion (most tables,
  smallest servings) land for a visitor who will never read "rows per table."

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| B8 parallel coordinates | ~6 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |
| B9 Marimekko | ~7 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ |
| B10 avg-table-size bars | ~3 KB | 1→4 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |

## C. The registration correction — three more

- **C8. The receipt** — the correction typeset as a store receipt: 847 at the
  top, each deduction a line item, SUBTOTAL 183, "PAID: 90 wired," balance 93.
  Everyone reads receipts; nobody misreads one. Pure HTML/CSS.
  *Lift:* full thermal-paper commitment — monospace face, faint print
  banding, a slight scan skew, and a real barcode that encodes the audit
  date. An artifact you'd believe fell out of a pocket, carrying true numbers.
- **C9. The digit morph [interactive]** — scroll-driven: the numeral 847
  physically breaks apart, pieces flying into labeled bins (mirrors,
  mis-flags…), the remainder reassembling as 183. The recount as motion.
  *Lift:* every fragment keeps its bin's color from the moment it splits, so
  a viewer can visually trace *which part of 847* went where. The animation
  becomes auditable — rewatch it and follow one shard.
- **C10. One day of checking, as a timeline** — the correction plotted against
  the actual hours of 08-24: morning count, each bucket discovered through the
  day, evening total. Frames it as *work*, not magic. ⚠️ Needs per-correction
  timestamps — not confirmed the audit logged them.
  *Lift:* draw it as a workday — hour ticks, a lunch gap if the record shows
  one, the evening total in heavier weight. The chart's subject becomes the
  labor, and the number's credibility rides on the visible effort.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| C8 the receipt | ~4 KB | 2→8 | ●○○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●●●● |
| C9 digit morph | ~10 KB | 6→20 | ●●●●○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●● | ●●●○○ | ●●●●● |
| C10 correction timeline | ~5 KB | 3→10 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●○○ |

## D. Entity graph scale — two more

- **D8. The multiplier staircase** — plot the *ratios between stages*, not the
  counts: ×2.5 (entities→nodes), ×2.1 (nodes→pairs), **÷36,864**
  (pairs→edges), ×3.6 (edges→leads). Four numbers instead of five huge ones;
  the ÷36,864 step is the whole story and finally gets to be the biggest thing
  on screen.
  *Lift:* draw the three gentle multipliers as stairs and the ÷36,864 as a
  sheer cliff face — one break in the drawing's own grammar, carrying the
  entire finding. The eye falls off the edge exactly where the data does.
- **D9. The odds ladder** — "a candidate pair's chance of becoming a real
  edge: 1 in 36,864," placed on a ladder of familiar odds. ⚠️ The familiar
  odds are general knowledge — each rung needs a sourced figure before
  publishing.
  *Lift:* space the rungs *logarithmically true*, so the empty stretch of
  ladder between the last familiar odd and yours is drawn at honest length.
  The gap — not the rungs — is the exhibit.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| D8 multiplier staircase | ~4 KB | 2→8 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ |
| D9 odds ladder | ~4 KB | 2→8 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ |

## E. Overlap coverage — three more

- **E8. Arc diagram** — tables (or schemas) on one horizontal line, overlaps
  as arcs above it. The printable, orderly cousin of the E4 network: same
  connections, readable left-to-right, real SVG text throughout.
  *Lift:* order the line to minimize crossings and color arcs by key type —
  at which point it reads as a musical score: connections as phrases, key
  types as voices. Print it wide and it's a frieze.
- **E9. Schema-adjacency matrix** — schemas × schemas grid, cell shade = pair
  count between them. The classic answer to "node-link diagrams stop working";
  scales cleanly, screen-reader-friendly, and distinct from E3 (that was key
  type × coverage bucket).
  *Lift:* visibly mask the diagonal — self-pairs and mirrors crossed out with
  a printed "we don't count these." The chart refusing to flatter itself is
  the most on-brand pixel in the whole group.
- **E10. Twenty-five constellation stamps** — one tiny network per key type,
  small-multiple grid. Shows at a glance which key types form dense hubs
  (EIN, NPI) and which are two dots and a line (MMSI). No single-network
  hairball, same insight.
  *Lift:* uniform frames like a stamp album — each key type a stamp, its pair
  count as the denomination in the corner. Collectible, scannable, and the
  three-pair stamp is exactly as dignified as the six-thousand-pair one.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| E8 arc diagram | ~15 KB | 4→12 | ●●●○○ | ●●●●● | ●●●●○ | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| E9 adjacency matrix | ~12 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●○ | ●●●●● | ●●●○○ |
| E10 constellation stamps | ~25 KB | 5→16 | ●●○○○ | ●●●●● | ●●●●○ | ●●○○○ | ●●●●○ | ●●●●○ | ●●●●● |

## F. DOCKET trust — two more

- **F8. The magnifier inset** — the full 6,560-dot field with a drawn lens
  pulled out to one corner, enlarging the region holding the 45. The
  needle-in-a-haystack composition, literal. Half chart, half illustration.
  *Lift:* render the lens with real optics — edge distortion, a faint glass
  highlight — so the enlargement reads as *looking closer*, not as a zoomed
  crop. Craft in the lens is what signals care about what's under it.
- **F9. Looks-real vs. is-real 2×2** — a quadrant chart of the whole trust
  problem: high-overlap-and-real (the 45), high-overlap-but-fake (the 99.98%
  pair), low-and-noise (the thousands), low-but-real (rare). Teaches *false
  positive* without ever saying it. The one form here about the logic, not
  the counts.
  *Lift:* name the quadrants like a field guide — **True friends · Impostors
  · Static · The overlooked** — with the impostor quadrant holding exactly one
  labeled specimen: the 99.98% pair. A memorable taxonomy outlives any chart.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| F8 magnifier inset | ~30 KB | 5→16 | ●●○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ | ●●●○○ | ●●●●● |
| F9 real-vs-looks 2×2 | ~5 KB | 2→8 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●●●○ |

## G. Dead weight — three more

- **G7. Before/after cleanup bars** — the warehouse today (185.4GB) beside the
  warehouse after deleting the dead weight (~126GB). The only concept that
  shows the *payoff* of cleanup rather than the existence of waste.
  *Lift:* draw the "after" bar with a clean dotted cut line, the freed ~59GB
  drifting off it as pale, dissolving blocks. Deletion drawn as release, not
  as absence — the picture argues for the cleanup without a word.
- **G8. The graveyard timeline** — every dead object plotted by when it was
  last touched. Shows the dead weight isn't one accident, it accumulated.
  ⚠️ Needs last-touched dates per object — in the warehouse's metadata in
  principle, not confirmed pulled into the audit CSVs.
  *Lift:* restraint plus one cue — plain tick marks along the time axis, but
  each tick shaped as the smallest possible headstone. One illustration
  decision, held at whisper volume, and the axis becomes a burial record.
- **G9. Cause-of-death cards** — each class of dead weight as a labeled card:
  MIRROR · BACKUP · CAP · EMPTY, with its count and one plain sentence.
  The housekeeping framing at its most scannable.
  *Lift:* design them as archive toe-tags — string hole, stamped
  classification, deadpan cause line ("died of being counted twice"). Dark
  humor at exactly the volume a cleanup list can carry.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| G7 before/after bars | ~3 KB | 1→4 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| G8 graveyard timeline | ~8 KB | 4→12 | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ |
| G9 cause-of-death cards | ~5 KB | 2→7 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |

## H. The four-verb pipeline — two more

- **H7. The subway map** — the four verbs as stations on a transit line;
  source families are colored lines converging into COLLECT, one line exiting
  to DETECT. A visual language everyone can already read, and it extends
  naturally as sources grow.
  *Lift:* obey real transit-map discipline — 45° angles only, even station
  spacing, an official-looking legend — and make CONNECT the grand
  interchange where every line meets. That's not decoration; the interchange
  *is* the platform's thesis, drawn in a grammar everyone reads fluently.
- **H8. Four-panel storyboard** — the pipeline as a comic strip: one drawn
  panel per verb, one caption each. The friendliest possible entry for a
  visitor who will not read a diagram.
  *Lift:* make it a silent comic — no dialogue, no captions, only the counts
  appearing as the panels' sole text. The numbers become the punchlines, and
  the strip works in any language.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| H7 subway map | ~10 KB | 5→16 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● |
| H8 storyboard | ~120 KB | 8→24 | ●○○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●○○○ | ●○○○○ | ●●●●○ |

## I. Key trust tiers — two more

- **I7. The plain 100% bar** — one horizontal bar, 3,619 columns split
  GEO / STEEL / STRONG. Round 1 skipped the simplest form in the entire
  vocabulary; it belongs on the menu, and the GEO share doing most of the bar
  *is* the finding.
  *Lift:* give the hairline STRONG segment a long callout leader and the
  loudest label on the chart — the smallest slice gets the biggest voice.
  Inverting the visual hierarchy once, deliberately, is the design.
- **I8. Tier × entity-grain matrix** — which trust tiers identify which kinds
  of thing: rows = tier, columns = place/org/facility/…, cell = column count.
  Would show whether people are only ever identified by weak keys — a real
  question. ⚠️ Needs the cross-tab; the audit CSVs have each axis separately,
  the combination not confirmed.
  *Lift:* border the *person* column so the ethics question is visible as a
  highlighted column before a single number is read. The chart declares what
  it's really asking.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| I7 plain 100% bar | ~2 KB | 1→3 | ●○○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| I8 tier×grain matrix | ~8 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ |

## Three more wild ideas

- **W7. The map room** — all nine metric groups composed onto ONE giant
  deep-zoomable poster: scale in the center, pipeline as the spine, trust
  tiers as the legend, dead weight as greyed territory. One artifact instead
  of nine graphics; also printable at A0. *Risk:* very high effort (30-60+
  hours), and one bad composition decision sinks the whole thing instead of
  one chart.
  *Lift:* commit to full cartographic convention — compass rose, a scale bar
  denominated in rows, marginalia, "surveyed 2026-08-24" in the corner. Not
  a dashboard that looks like a map; a survey document of a territory that
  happens to be data.
- **W8. The data fingerprint** — a generative mark seeded deterministically by
  the audit's numbers: every audit run produces a unique visual signature, and
  the mark *changing* between runs is itself the message ("the warehouse
  moved"). The one art concept that regenerates *by design* — it dodges the
  standing art-vs-regen trade-off instead of paying it. *Risk:* abstract; it
  proves nothing on its own and needs the real charts next to it.
  *Lift:* make it the site's actual mark — favicon, masthead, page footer —
  so the identity of the whole site is a hash of the current audit. When the
  numbers change, the site visibly changes its face. Show last audit's mark
  faintly beside it: the drift between the two IS the changelog.
- **W9. The audit timelapse** — the warehouse growing across audit runs as an
  animation: databases inflating, connections lighting up, dead weight
  accumulating. *Risk:* ⚠️ needs historical audit snapshots — only the
  2026-08-24 audit is confirmed to exist in this form, so this one starts
  paying off on audit #3, not today.
  *Lift:* include a "play it backwards" control — the warehouse un-growing to
  nothing. Watching it rewind to zero is the cleanest possible statement of
  how much got built; the empty first frame is the origin story.

---

# End of options

No recommendation, no shortlist, no "if I had to pick" — by design. **60
concepts across 9 groups + 6 wild ones + 30 tools in Round 1, plus 24 concepts
and 3 wild ones in Round 2 — 93 total**, all scored the same way so they
compare without being ranked for you. Every concept carries a **Lift** — keep
it or drop it per piece; they're intent, not requirements.

Two facts (not advice) worth holding while weighing:

1. **The biggest fork isn't the library — it's static vs. interactive vs.
   illustrated.** Static regenerates and loads instantly; interactive earns its
   keep on ~4 of 60 concepts; illustrated wins every Wow score and every one
   goes stale when the numbers change.
2. **Six of nine groups need no charting library at all** (A, C, F, G, H, I —
   typography, SVG, one canvas loop). The library question only bites on the
   graph-scale concepts (D7, E4) and the exploratory one (E7).

---

# Appendix: verified this session (2026-08-25)

Checked against live documentation or the local machine:

- **Datashader** 0.19.1; billion-point claim; Py 3.10-3.14 — [datashader.org](https://datashader.org/releases.html), [GitHub](https://github.com/holoviz/datashader)
- **pyecharts** 2.1.0 (Feb 10 2026), MIT — [PyPI](https://pypi.org/project/pyecharts/), [GitHub](https://github.com/pyecharts/pyecharts)
- **Apache ECharts** 6.1.0, Apache-2.0, chord + matrix coords new in v6 — [handbook](https://echarts.apache.org/handbook/en/basics/release-note/v6-feature/), [npm](https://www.npmjs.com/package/echarts)
- **Observable Plot** SSR via JSDOM + its "simple plots of small data" warning; stylesheet inlined — [docs](https://observablehq.com/plot/features/plots), [GitHub](https://github.com/observablehq/plot)
- **cosmos.gl** MIT, v3.0, WebGL2/luma.gl, `@cosmos.gl/graph`, OpenJS incubating — [GitHub](https://github.com/cosmosgl/graph), [OpenJS](https://openjsf.org/blog/introducing-cosmos-gl)
- **Cosmograph** CC-BY-NC-4.0, commercial use by contact — [docs](https://cosmograph.app/docs-general/)
- **deck.gl** v9, WebGL2 via luma.gl v9, WebGPU not enabled in 9.0 — [what's new](https://deck.gl/docs/whats-new), [WebGPU](https://deck.gl/docs/developer-guide/webgpu)
- **plotly.js** bundle sizes (3.3MB raw / 1.2MB min / ~391KB gz; basic ~318KB gz) — [dist README](https://github.com/plotly/plotly.js/blob/master/dist/README.md)
- **vl-convert-python** self-contained export, no Node/browser — [GitHub](https://github.com/vega/vl-convert), [PyPI](https://pypi.org/project/vl-convert-python)
- **D3** 7.9.0 latest, no v8 — [npm](https://www.npmjs.com/package/d3?activeTab=versions)
- **sigma.js** v3 on graphology, WebGL — [sigmajs.org](https://www.sigmajs.org/docs/) *(license not verified)*
- **PyWaffle** MIT, Font Awesome icons, matplotlib-based — [GitHub](https://github.com/gyli/PyWaffle)
- **rough.js** <9kB gz; **roughViz** 2.0.5 on D3v5, "intent or generality, not absolute precision" — [roughjs.com](https://roughjs.com/), [roughViz](https://github.com/jwilber/roughViz)
- **Observable Framework** 1.13.4, static site generator with data loaders — [GitHub](https://github.com/observablehq/framework)
- **matplotlib** 3.11.1 (3.11.0 Jun 11 2026), text/font overhaul — [release notes](https://matplotlib.org/stable/release/release_notes.html)
- **plotnine** 0.15.7 (Jun 13 2026) — [changelog](https://plotnine.org/changelog.html)
- **Local machine** (checked directly): plotly 6.6.0, altair 5.5.0, pandas 2.3.3, numpy 2.0.2, networkx 3.2.1, pydeck 0.9.2, dash 4.4.1, Pillow 11.3.0, duckdb 1.4.5, Node v22.23.2, Chrome present. **Absent:** matplotlib, seaborn, plotnine, datashader, bokeh, holoviews, hvplot, pyecharts, kaleido, vl-convert-python, graphviz, scipy, geopandas.

**Not verified this session** (do not treat as fact): Bokeh, Panel, three.js,
regl, p5.js, Chart.js, Recharts, Nivo, LayerCake, DuckDB-WASM, Graphviz, and
all Highcharts / Flourish / Datawrapper pricing and licensing. Every ⚠️ license
above is general knowledge only.
