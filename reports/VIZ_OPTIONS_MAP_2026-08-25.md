# Warehouse Metrics → Visualization Options Map

**Dated 2026-08-25.** A menu, not a decision. Nothing here is a recommendation
and there is no shortlist at the end — that's on purpose. The pick is Chris's.

---

## Plain-English intro

You have a pile of numbers about your own data warehouse — how big it is, how
much of it is connected, how much of it is junk, and how much of what looks
connected is actually fake. This document lists **every sensible way to draw
those numbers on a website**, and every tool that could draw them.

Two separate choices hide inside "how should I visualize this":

1. **The picture** — is this a bar chart, a flowing river, a grid of dots, a
   drawing of a building? That's the *concept*.
2. **The tool** — what software draws it? That's the *library*.

Most people collapse those two into one and end up with whatever their tool
draws by default. This document keeps them apart. Section by section it gives
**9 metric groups × 6-7 different picture ideas each (60 concepts total)**,
scores each one on nine practical dimensions, and then — separately — lists
**30 tools** with what each can and can't do.

**Direction of the scores:** more dots = better on that dimension, always.
Page weight and effort are shown as real numbers (KB, hours) instead of dots,
because a dot rating there hides the thing you'd actually want to know.

---

## What's already built (so nothing here is presented as new when it isn't)

You already have a body of visual work in this repo. Verified on disk this
session, not remembered:

| Existing page | What it already does |
|---|---|
| the scale gallery (10 scenes) | counting-problem clock, one-pixel-per-entity field, printed-tower metaphor, source skyline, domain treemap, ripple, powers-of-ten, build-over-time, human-scale arithmetic, map-lighting-up |
| the chart vocabulary field guide | a catalogue of chart forms already drawn once |
| the infographic layout systems survey | page-composition patterns |
| the warehouse biome page | mart row counts as a biome |
| the spine tree page | spine axis → table membership as a tree |
| ten data pages (rate map, pill rivers, heartbeat, denial gap, waiting room, detention rivers, own clock, pulse grid, bank deserts, money shape) | the existing house style: dark "night water" palette, hand-rolled HTML + canvas, data baked in at build time |

**Where that matters below:** concepts that already exist in some form are
marked **[BUILT]**, concepts that are a variation on something built are
marked **[NEAR-BUILT]**. Everything else is new to this repo. This is context,
not a ceiling — several new concepts below deliberately overlap the same
metric a built page covers, because a second, better picture of the same
number is a real option.

---

## What's actually installed on this Mac (verified this session)

This changes the effort numbers a lot, so it's stated up front rather than
assumed.

**Present:** Python 3.9 with plotly 6.6.0, altair 5.5.0, pandas 2.3.3,
numpy 2.0.2, networkx 3.2.1, pydeck 0.9.2, dash 4.4.1, Pillow 11.3.0,
duckdb 1.4.5. **Node v22.23.2 is installed** (via nvm). Chrome is installed
(used for headless screenshotting).

**Absent:** matplotlib, seaborn, plotnine, datashader, bokeh, holoviews,
hvplot, pyecharts, kaleido, vl-convert-python, geopandas, graphviz, scipy.

Two corrections worth noting: an older note in memory says there is **no Node
on this Mac** — there is, v22.23.2. And **matplotlib is not installed**, which
matters because five of the Python options below (seaborn, plotnine, PyWaffle,
Datashader's mpl path, and matplotlib itself) all sit on top of it.

---

## The numbers being visualized (pulled from the audit, not re-derived)

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

# How to read the score tables

Every concept below gets scored on all nine dimensions. Same nine, every time,
no weighting — the weighting is yours.

| Column | Means | Scale |
|---|---|---|
| **Weight** | what the visitor's browser downloads for this one graphic | real KB estimate |
| **Effort** | rough hours: first working draft → portfolio-polished | real hours |
| **Interact** | does clicking/hovering/zooming add real meaning here, or is it decoration? | ●○○○○ decoration → ●●●●● interaction *is* the point |
| **Design** | how good this can look with real design effort applied (not the default theme) | ●○○○○ stuck ugly → ●●●●● magazine-grade |
| **Scale** | does it survive the actual row counts without sampling? | ●○○○○ needs aggregation → ●●●●● handles it natively |
| **A11y** | colorblind-safe + screen-reader/alt-text feasible | ●○○○○ canvas blob, no text layer → ●●●●● real text/SVG, describable |
| **Theme** | works in both your light and dark site themes | ●○○○○ one theme only → ●●●●● token-driven, flips free |
| **Regen** | can it rebuild itself next time the audit runs? | ●○○○○ hand-tuned art → ●●●●● one script, zero hand-touching |
| **Wow** | how differentiated vs. a generic dashboard chart | ●○○○○ seen it → ●●●●● nobody has one of these |

**One honesty note applied throughout:** any concept scoring ●●●●● on Wow and
●○○○○ on Regen is *art*, not a chart — beautiful once, stale the moment the
numbers change. That trade-off is real and is never smoothed over below.

---

# A. Warehouse scale — the headline number

**What this section shows:** the one number that says "this is big" — 4.97
billion rows, 185.4GB, 5,436 objects across 7 databases. The problem with a
headline number is that a human can't feel a billion. Every concept here is a
different answer to *how do you make 4.97B mean something.*

### A1. Big-type stat block **[BUILT]**
Four or five enormous numerals in your serif face, with a one-line plain
sentence under each. No chart at all — typography carrying the whole load. The
existing gallery header already does this.

### A2. The counting clock **[BUILT]**
"Read one row per second, no sleep." 4.97B seconds = ~158 years. An animated
counter that visibly can't finish, with the elapsed-years figure ticking beside
it. Already built as scene 1.

### A3. One-pixel-per-entity field **[BUILT]**
A canvas where each dot is one entity, filling the screen until it's texture
rather than dots. Works because the eye reads density directly. Already built.

### A4. Powers-of-ten ladder **[BUILT]**
Ten steps from one readable record to the full warehouse, each ×10, each
annotated with a real-world comparison at that size. Already built as scene 7.

### A5. Nested-square area nest (new)
One square = 4.97B rows. Inside it, a square for the largest database, inside
that the largest schema, then the largest table — four true-to-area nestings
that show, in one static image, how much of "everything" one table actually is.
Different from a treemap: it's a *zoom*, not a partition.

### A6. Physical-object scale stack (new)
Render the warehouse as a to-scale physical object next to a known reference —
185.4GB as a stack of 1.44MB floppy disks (~125,700 of them; at 3.2mm each
that's ~402m / ~1,320 ft, taller than the Empire State Building's 1,250 ft
roof), beside a drawn building for reference. Static illustration, numbers
computed, drawing hand-composed.

### A7. Scrolling odometer strip (new)
A single horizontal band that scrolls the digits of 4,974,176,335 past as the
visitor scrolls the page, with tick labels marking where each database's
contribution ends. The number becomes a *distance* you travel through.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| A1 big type | ~2 KB | 1→4 | ●○○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| A2 counting clock | ~4 KB | 2→6 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |
| A3 pixel field | ~15 KB | 3→10 | ●●○○○ | ●●●●○ | ●●●○○ | ●●○○○ | ●●●○○ | ●●●●○ | ●●●●○ |
| A4 powers of ten | ~8 KB | 4→12 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●●○ | ●●●○○ |
| A5 nested squares | ~6 KB | 3→9 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |
| A6 physical stack | ~180 KB* | 8→30 | ●○○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●○○○ | ●○○○○ | ●●●●● |
| A7 odometer strip | ~5 KB | 4→14 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●● | ●●●●○ | ●●●●○ |

\* A6's weight is an embedded illustration; as inline SVG instead it drops to
~30 KB but the drawing effort roughly doubles.

**Tools that can draw these:** A1/A5/A7 are plain HTML+CSS+SVG, no library.
A2/A3 are canvas + ~40 lines of JS. A4 is either. A6 is Pillow (installed) or
hand-drawn SVG, or a generative pass in p5.js. Nothing in this group needs a
charting library at all — worth knowing, because a charting library is the
default assumption and it buys you nothing here.

---

# B. Per-database breakdown — seven wildly different things

**What this section shows:** the warehouse isn't one database, it's seven, and
they're not comparable. Three hold ~1.3B rows each. One holds 135,812. Two hold
literally zero. Any chart that puts all seven on one linear axis makes four of
them invisible — that's the whole design problem here.

### B1. Log-scale horizontal bars (the honest default)
Seven bars on a log axis, each labeled with its real number in plain digits so
the log distortion can't mislead. The two zero-row databases get an explicit
"zero — not a short bar" treatment, since log scales cannot draw zero.

### B2. Small-multiple cards
Seven identical cards, one per database, each with its own tiny bar showing
rows / tables / views / GB — comparison happens by scanning cards, not by
sharing an axis. Sidesteps the scale problem entirely by refusing to share a
scale.

### B3. Treemap by database → schema **[NEAR-BUILT]**
Area = rows. Seven top blocks subdivided into their schemas (the mart side has
~40). Shows both "which database is biggest" and "which schema inside it
dominates" in one shape. The biome page does a version of this for marts only.

### B4. Stacked ribbon / horizon strip
One horizontal band per database, height ∝ log(rows), colored by layer role
(landing / staging / marts / metadata / backup / dead). The strip reads as a
cross-section of the warehouse, like geological strata.

### B5. Dot-matrix waffle grid
One square = 10M rows. 497 squares total, grouped and colored by database. The
zero-row databases appear as labeled empty outlines — the only form in this
group where "nothing" is visually as loud as "something."

### B6. Bubble-in-a-box packing
Seven circles, area ∝ rows, packed inside one frame. Fast to read the ranking;
weak at exact comparison. Handles the two zero cases badly (a zero circle is a
dot) — flagged as a real weakness, not a nitpick.

### B7. Two-axis scatter: tables vs. rows
X = table count, Y = row count, both log. Instantly exposes the shape story
that a bar chart hides: RAW has 2,212 tables holding 1.27B rows while META has
108 tables holding *more* (1.50B). That "few tables, enormous rows" outlier is
the actual finding, and only this form shows it.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| B1 log bars | ~3 KB | 1→4 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| B2 small multiples | ~6 KB | 2→7 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| B3 treemap | ~25 KB | 3→10 | ●●●●○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ |
| B4 strata ribbon | ~7 KB | 4→12 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| B5 waffle grid | ~10 KB | 3→9 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |
| B6 bubble pack | ~20 KB | 2→7 | ●●●○○ | ●●●○○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●○○○ |
| B7 tables-vs-rows scatter | ~4 KB | 2→6 | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |

**Tools:** all seven are trivially drawable in Vega-Lite/Altair (installed),
Plotly (installed), ECharts/pyecharts (not installed, MIT + Apache-2.0), or
hand-rolled SVG. B3 specifically: `d3-hierarchy` gives squarified treemap
layout and is the algorithm most other libraries wrap; ECharts and Plotly both
ship treemaps natively. B5 in Python is PyWaffle (MIT) — but PyWaffle sits on
matplotlib, which is **not installed here**.

---

# C. The registration gap and its correction — 847 → 178 → 267

**What this section shows:** the most interesting story in the whole audit, and
the one a bar chart would actively ruin. The morning number said 847 tables had
real keys but only 178 were registered — a 669-table backlog. By evening that
was mostly wrong: 289 were duplicate mirrors, 37 were already registered but
mis-flagged, 14 weren't sources at all. The real backlog was 183 tables, of
which 90 got wired that day. **The shape here is "a number that corrected
itself," which is a before/after, not a quantity.**

### C1. Waterfall / bridge chart
Start at 847, step down through each deduction (−289 mirrors, −37 mis-flagged,
−14 derived, −20 mart-only, −135 docket parked), land at 183 real backlog, then
step to 90 wired / 93 gaps. The single most literal form for "how a big number
became a small one," and the steps are self-labeling.

### C2. Side-by-side before/after with a connecting flow
Left column: the 847 as one block. Right column: the corrected buckets. Curved
ribbons connect left to right, width ∝ tables. The ribbons carry the
"where did they go" information a waterfall states but doesn't show.

### C3. Sankey of the full reconciliation
847 splits into 7 destination buckets, and the portal and federal buckets split
again into wired vs. gap. Two levels of branching, ~11 terminal nodes. Denser
than C2 and shows the second-level split the waterfall flattens.

### C4. Sieve / filter-stack illustration
Draw it as a physical sieve stack: 847 tables poured in the top, each mesh
layer catching one category (mirrors, mis-flags, derived, parked), 183 falling
through to the bottom. Static illustration, honest to the mechanism, and it
makes "de-duplication" legible to someone with no data background.

### C5. Two-state toggle **[interactive only]**
One chart, one button: "as first counted" / "after checking." The bars
physically re-arrange between states. The correction becomes something the
visitor *does*, which is a much stronger honesty signal than describing it.

### C6. Annotated number line with a strike-through
A horizontal line from 0 to 847, with 847 struck through and re-marked at 183,
each deduction annotated as a labeled bracket beneath. Deliberately plain — the
"editorial correction" look, like a printed erratum.

### C7. Unit grid of 847 squares, recolored
847 tiny squares in a grid. Color-code every one by its fate. You see the real
backlog as the small colored minority it turned out to be, and — unlike every
other form here — you can see that the mirrors bucket alone is a third of the
whole picture.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| C1 waterfall | ~4 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| C2 before/after ribbons | ~10 KB | 4→14 | ●●●○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| C3 Sankey | ~30 KB | 3→10 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●○○ |
| C4 sieve illustration | ~120 KB | 8→26 | ●○○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●○○○ | ●○○○○ | ●●●●● |
| C5 two-state toggle | ~8 KB | 5→16 | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| C6 struck number line | ~3 KB | 2→8 | ●○○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ |
| C7 847-square grid | ~12 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |

**Tools:** C1 is native in ECharts and Plotly; in Vega-Lite it's a hand-built
stacked bar with transparent bases (doable, ~30 lines). C3 Sankey is native in
Plotly, ECharts, and `d3-sankey`. C2/C6/C7 are SVG by hand. C5 needs any JS —
no library required if the chart is SVG.

---

# D. Entity graph scale — six orders of magnitude in one pipeline

**What this section shows:** the pipeline's stage counts, which span from 181
million down to 4,910 — a factor of ~37,000 — in one sequence. And there's a
trap: the sequence is **not** a shrinking funnel. It goes 33.3M golden entities
→ 84.4M keyset nodes → 181M match pairs → 4,910 edges → 17,598 leads. It grows
twice, collapses hard, then grows again. **A standard funnel chart drawn on
these numbers tells a lie**, because funnel charts assume each stage is a
subset of the last. Every concept below has to state how it handles that.

*(Why the numbers grow: one real-world company can have five different ID
types, so 33.3M entities produce 84.4M key nodes; and pairs of nodes are
combinatorial, so 84.4M nodes produce 181M candidate pairs. Then scoring throws
almost all of them away.)*

### D1. Log-scale stage strip (the honest baseline)
Five bars on a log axis, left to right in pipeline order, each labeled with its
real number and a plain sentence. Log scale is the only linear form where 4,910
and 181M are both visible. Non-monotonic movement shows correctly because
nothing about a bar chart implies subsetting.

### D2. Sankey with explicit expansion and collapse
Flows sized by count, with the expansion steps drawn as *fan-outs* (one node
splitting into several) and the collapse drawn as a hard narrowing. Solves the
funnel lie by using a grammar that permits growth. Cost: at true scale the
4,910 edge is a hairline — needs a log-width or a break-out inset.

### D3. Nested rings, each ring ÷10
Concentric circles, one per power of ten from 10⁰ to 10⁹, with each pipeline
stage plotted as a marker at its true radius. Reads as a zoom, and the
non-monotonic order shows as markers that jump inward and outward — which is
exactly the truth.

### D4. Two-panel "grows then collapses"
Split the story into two charts side by side, because it's honestly two
stories. Panel 1: entities → nodes → pairs (expansion, linear axis works).
Panel 2: pairs → edges → leads (collapse, log axis). Refuses to force one
grammar onto two different behaviors.

### D5. Animated scrubber **[interactive only]**
A slider or scroll-driven walk through the five stages, one at a time, with a
count-up and a one-sentence explanation per stage, and a persistent
mini-timeline showing where you are. The expansion/collapse is felt as motion
rather than argued in a caption.

### D6. Sand-through-a-funnel physical metaphor
Static art: five vessels, sized to true scale under a log transform, with the
grain volume in each vessel drawn to match. The middle vessel visibly overflows
the one before it — which is the point, and is much easier to accept as
"correct" in a physical metaphor than in a funnel chart.

### D7. Hundred-thousand-dot field with a survivor highlight
Render a sampled field of match-pairs as dots, then highlight the 4,910 that
survived scoring — visually, a near-empty scattering in a dense fog. The best
form for the emotional truth ("almost nothing survives"), the worst for exact
reading. Needs explicit "this is a 1-in-N sample" labeling or it's dishonest.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| D1 log strip | ~4 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| D2 Sankey | ~30 KB | 4→14 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●○○ |
| D3 nested rings | ~7 KB | 4→12 | ●●●○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| D4 two-panel | ~6 KB | 3→9 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| D5 scrubber | ~14 KB | 6→20 | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| D6 sand funnel | ~140 KB | 10→30 | ●○○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●○○○ | ●○○○○ | ●●●●● |
| D7 survivor field | ~60 KB | 5→16 | ●●●○○ | ●●●●○ | ●●○○○ | ●●○○○ | ●●●○○ | ●●●○○ | ●●●●● |

**Tools:** D7 is the one place in this whole document where **Datashader**
earns its keep — it's built to rasterize hundreds of millions of points into a
fixed-size image server-side, so the browser only ever downloads a PNG. Its
docs claim billion-point rendering and it's at v0.19.1; it is **not installed
here** and it needs matplotlib/Numba, so budget install time. The alternative
is doing the aggregation in DuckDB (installed) and drawing the resulting grid
in plain canvas — fewer dependencies, more hand-written code.

---

# E. Overlap coverage — 24,011 measured table pairs

**What this section shows:** how much of the warehouse has actually been
checked for connections, and by which kind of ID. 24,011 pairs measured;
11,839 confirm what the platform already found, 12,172 are new. Split across
25 key types that range from DOCKET's 6,560 pairs down to MMSI's 3.

### E1. Stacked bars by key type, split confirmed/new
25 rows, each bar split into confirmed vs. new. Sorted by total. The long tail
(DEA_NO 4, MMSI 3) either gets a "+19 more" rollup or its own zoomed inset.

### E2. Slope chart: confirmed vs. new per key type
Two vertical axes, a line per key type. The lines that slope steeply upward
(DOCKET: 386 confirmed → 6,174 new) are visually the story: which key types
this audit opened up that the platform had barely touched.

### E3. Key-type matrix heatmap
Rows = key types, columns = coverage buckets, cell shading = pair count. The
grid form makes 25 categories scannable where 25 bars start to feel like a list.

### E4. The actual network, aggregated
Draw the 816 keyed tables as nodes and the 24,011 overlaps as edges — but
aggregated: bundle edges by schema pair so it renders as ~40 fat bundles rather
than 24,011 hairlines. This is the only concept in the group that shows the
*shape* of the connection map rather than its counts.

### E5. Chord diagram by domain
Collapse tables to their domain (HEALTH, FINANCE, JUSTICE…) and draw arcs
between domains, thickness ∝ number of measured overlaps. Answers a question no
bar chart in this group answers: **which subject areas actually touch each
other.** ECharts 6 shipped a native chord series (verified this session).

### E6. Coverage-percentage histogram
For each pair, coverage_a_pct is already computed. Plot the distribution: a
huge spike near 100% (mirrors — same table twice) and a huge spike near 0%
(coincidence). The bimodal shape *is* the finding, and it's invisible in every
count-based form above.

### E7. Interactive filterable pair explorer **[interactive only]**
A searchable, sortable table/scatter hybrid — pick a key type, see every pair
plotted by (distinct_a, overlap), click one to read its numbers. Portfolio
value: proves the underlying data is real and browsable, not a claim.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| E1 stacked bars | ~8 KB | 2→7 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| E2 slope chart | ~6 KB | 3→9 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●○○ |
| E3 matrix heatmap | ~10 KB | 3→9 | ●●●○○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ | ●●●●● | ●●○○○ |
| E4 bundled network | ~90 KB | 8→26 | ●●●●○ | ●●●●● | ●●●○○ | ●○○○○ | ●●●○○ | ●●●○○ | ●●●●● |
| E5 chord by domain | ~40 KB | 4→14 | ●●●●○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| E6 coverage histogram | ~5 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| E7 pair explorer | ~120 KB | 10→30 | ●●●●● | ●●●○○ | ●●●○○ | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ |

**Tools:** E4's edge bundling is `d3-hierarchy` + hierarchical edge bundling,
or — if you want it live and draggable — cosmos.gl (MIT, WebGL2, v3.0, claims
hundreds of thousands of points/links) or sigma.js v3 on graphology. **Caution
on licensing:** cosmos.gl the engine is MIT, but *Cosmograph*, the friendlier
wrapper product built on it, is **CC-BY-NC-4.0 — non-commercial only**. A
portfolio site is a gray area there; the MIT engine isn't. E5 chord is native
in ECharts 6 and in `d3-chord`.

---

# F. The DOCKET trust breakdown — the honesty centerpiece

**What this section shows:** of 6,560 docket-number overlaps, 45 are
trustworthy, 2,909 were *actively downgraded* mid-audit after a claim turned
out to be wrong, and ~6,475 are noise or unverified. Two things make this the
most visually interesting metric you have: the trustworthy share is **0.7%**,
and one pair overlaps at **99.98% purely by coincidence.**

**A note that governs this whole group:** a bar chart with a 6,475 bar and a 45
bar renders the 45 as a hairline — which undersells the finding. "We found 45
real ones" is the *good news*; the form has to let it be seen.

### F1. Icon array / dot grid, 6,560 dots
6,560 dots, 45 of them lit. The single most literal answer to "how rare is
rare," and the one form where 0.7% is felt rather than read. At a 100×66 grid
each dot is ~6px on a 700px-wide figure — legible.

### F2. Three-tier confidence stack with a visible correction mark
A vertical stack: TRUST / RECLASSIFIED / DON'T TRUST, sized to count, with the
2,909 band drawn with a strike-through or "was: trusted" ghost above it. Puts
the mid-audit correction *into* the chart instead of a footnote.

### F3. Coverage-vs-plausibility scatter with a labeled trap
Plot every docket pair: X = overlap coverage %, Y = shared value count (log).
The federal-courts cluster sits high-right. The FDIC/CourtListener pair sits at
99.98% coverage on ~11,800 values and is labeled *"coincidence — small ID
space landing inside a huge one."* One annotated dot carries the entire
argument for why coincidence-scoring exists.

### F4. The 47% short-string histogram
Distribution of shared-value counts across the ~3,600 cross-agency pairs, with
the ≤5-values region shaded. 47% of the mass sits in a band that means "these
tables share four numbers, by chance." Blunt, cheap, devastating.

### F5. Before/after reclassification flow
A small Sankey or ribbon: the original three buckets on the left, the corrected
three on the right, with the 2,909 visibly moving from "trust narrowly" to
"unverified." The chart's subject is *the audit correcting itself*, which is a
different subject than the docket data.

### F6. The 45, named
Skip aggregate visualization entirely. List all 45 trustworthy pairs as a
designed table — publisher, publisher, coverage %, shared case count. On a
portfolio site, "here are the 45, by name" is a stronger credibility signal
than any chart of 6,560.

### F7. Two-color skyline of all 6,560, sorted by coverage
Every pair as a 1px vertical line, sorted left-to-right by coverage %, colored
by trust tier. Produces a distinctive ragged silhouette where the trustworthy
sliver is visible as a colored band at one end. Dense, printable, unusual.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| F1 icon array | ~20 KB | 3→10 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ |
| F2 tier stack + strike | ~5 KB | 3→10 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●●●○ |
| F3 annotated scatter | ~35 KB | 4→14 | ●●●●○ | ●●●●● | ●●●●○ | ●●●○○ | ●●●●● | ●●●●○ | ●●●●● |
| F4 short-string histogram | ~5 KB | 2→6 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| F5 correction flow | ~25 KB | 3→10 | ●●●○○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●○ | ●●●●○ |
| F6 the 45, named | ~8 KB | 2→8 | ●●●○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ |
| F7 6,560-line skyline | ~30 KB | 4→12 | ●●○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●●● |

**Tools:** F1 is hand-rolled SVG (6,560 `<rect>`s ≈ 200-300 KB of markup —
better as a single canvas draw or a CSS grid of divs) or PyWaffle for a static
PNG (MIT, but needs matplotlib, absent here). F3/F4 are Vega-Lite or Plotly,
both installed. F7 is one canvas loop, no library.

---

# G. Dead weight — the waste story

**What this section shows:** roughly a third of the warehouse is doing no work.
One whole database is 254 empty views. Another is a frozen backup with 894
million rows and 34.4GB. Two spine backups hold 272,607,989 rows *each*. And
one landing table is stuck at exactly 20,000,000 rows — a loader cap masquerading
as a row count.

**The framing choice here is a taste call in itself**, and it changes the
picture: is this a *waste* story (money and space wasted), a *rigor* story (we
found it and named it), or a *housekeeping* story (here's the cleanup list)?
The concepts below split roughly along those three framings.

### G1. Live vs. dead donut, stated in GB
185.4GB total; ~59GB of it is backups, legacy, and junk schemas. One ring, two
colors, the number in the middle. Simplest possible version of the waste
framing.

### G2. Warehouse floorplan with the dead rooms greyed
Draw the seven databases as rooms sized by storage, grey out the dead ones,
label each with what it is and why it's dead. Turns an abstract "33% waste" into
something spatial and immediately readable by a non-technical visitor.

### G3. The truncation trap, magnified
A single chart about the 20,000,000-row table: a bar at exactly 20.0M sitting
next to the re-pull's 63.7M, with the round number circled and the caption
"round numbers in data are almost always a cap, not a count." One graphic that
teaches a transferable idea rather than reporting a local fact.

### G4. Duplicate-pair strip
Every table that exists more than once (mart mirror, TIMELINE copy, restore
schema) drawn as a paired mark, sorted by size. Makes the 289-mirror finding
and the storage duplication visible as a repeated visual rhythm.

### G5. The empty-shelf illustration
THE_LIBRARY as a drawn library: 254 shelf slots, 26 labeled sections, every
shelf empty. Literal, memorable, and the one concept where "zero" gets to be
the subject of the picture instead of an absence in it.

### G6. Cost-framed bar
Convert dead storage to a monthly dollar figure and show that instead of GB.
**Blocked today**: there is no billing visibility on this account, so this
concept cannot be built honestly without a price per GB — listed because it's a
real option, flagged because it currently has no verified input.

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

**What this section shows:** how the machine works, in four steps, with live
counts attached: SCOUT (catalogs portals, tags key types before loading) →
COLLECT (2,212 landing tables, 1.27B rows) → CONNECT (267 registered tables,
84.4M key nodes, 4,910 edges) → DETECT (17,598 leads in the review queue).

**This is the one graphic a portfolio visitor most needs**, because every other
number on the page is meaningless without it. It's also the one where a generic
four-box-and-arrows diagram would be the biggest missed opportunity.

### H1. Four boxes, arrows, live counts
The baseline. Clean typography, four labeled stages, a count under each, one
plain sentence each. Boring is not automatically wrong — this is the version
that definitely communicates.

### H2. Widening-then-narrowing pipe
Draw the pipeline as an actual pipe whose diameter tracks the volume at each
stage — wide through COLLECT, narrow at CONNECT's edge count, with a small
outlet at DETECT. The shape carries the "we throw almost everything away"
message without a word of caption.

### H3. Layered stack with drill-downs **[interactive]**
Four horizontal bands; clicking one expands it to reveal its internals (COLLECT
expands into its source families; CONNECT expands into the trust tiers). One
diagram that serves both the five-second visitor and the five-minute one.

### H4. Assembly-line / factory illustration
An isometric drawing: raw material in at one end, four machines, a small tray of
finished leads at the other. The most "designed" option and the most likely to
be screenshotted by someone else.

### H5. Annotated timeline of a single record
Follow ONE real row from a government file all the way to a lead, with each of
the four verbs shown acting on it. Narrative, not aggregate — the form that
teaches best and shows scale worst.

### H6. Live status version
The same four boxes, but each carries a freshness state pulled from the source
freshness table — so the diagram doubles as a system-health readout. Highest
maintenance burden of the group, and the only one where the picture keeps
changing after you ship it.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| H1 four boxes | ~4 KB | 1→5 | ●○○○○ | ●●●●○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●○○○○ |
| H2 widening pipe | ~8 KB | 3→12 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●●○ |
| H3 layered drill-down | ~15 KB | 6→20 | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●● | ●●●●○ | ●●●○○ |
| H4 factory isometric | ~150 KB | 12→36 | ●○○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●○○○ | ●○○○○ | ●●●●● |
| H5 one record's journey | ~10 KB | 5→18 | ●●●○○ | ●●●●● | ●○○○○ | ●●●●● | ●●●●● | ●●○○○ | ●●●●○ |
| H6 live status boxes | ~12 KB | 6→18 | ●●●○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●●○ |

**Tools:** H1/H2 are hand SVG. Graphviz (not installed) auto-lays-out H1-style
diagrams but its default aesthetic is academic and hard to design past. H4 needs
an illustrator or a generative pass — not a chart library.

---

# I. Key trust tiers — what counts as proof

**What this section shows:** the four-tier vocabulary that governs everything
(STEEL = hard government ID, STRONG = narrower code, GEO = location,
PROBABILISTIC = a name), with the real column counts behind it: of 3,619
verified key columns, **2,368 are GEO, 1,025 are STEEL, 226 are STRONG**. And
underneath, what those keys identify: 2,368 places, 434 organizations, 285
facilities, 226 cases, 176 providers, 93 people, 23 assets, 14 vessels.

**The finding hiding in these counts:** the most common key type in the
warehouse (location) is also the weakest one. Most concepts below are built to
make that visible rather than to just tabulate the tiers.

### I1. Tier ladder with counts
Four rungs, STEEL at top, PROBABILISTIC at bottom, each with its count and a
one-line definition in plain words. Vertical position encodes trust; bar length
encodes quantity. The inversion (biggest bar on the weakest rung) is the payload.

### I2. Quantity-vs-trust quadrant
X = how many columns carry it, Y = how much it proves. GEO lands bottom-right
(everywhere, proves little); STEEL lands top-left (rarer, proves a lot). The
one form that states the trade-off as a position rather than a caption.

### I3. Entity-grain sunburst
Inner ring = tier, outer ring = what it identifies (place / organization /
facility / case / provider / person / asset / vessel). Two questions answered in
one shape.

### I4. The proof gradient
A continuous horizontal gradient from "fact" to "hint," with each key type
placed along it as a labeled marker sized by count. Rejects the four-bucket
framing in favor of the continuum the buckets approximate — arguably more honest,
definitely less standard.

### I5. Side-by-side evidence cards
Four cards, each showing a *real example value* from the warehouse: an actual
EIN, an actual ZIP, an actual name — with "what this proves" under each. Teaches
the vocabulary by showing the thing rather than counting it.

### I6. Vessel/person/facility pictogram row
The eight entity grains as icon rows, each icon = 10 columns. Vessels (14) and
assets (23) show as one-or-two-icon slivers next to place's 237 icons. Makes the
rare, exotic entity types visible as rare rather than invisible.

| Concept | Weight | Effort | Interact | Design | Scale | A11y | Theme | Regen | Wow |
|---|---|---|---|---|---|---|---|---|---|
| I1 tier ladder | ~4 KB | 2→6 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●○○ |
| I2 quadrant | ~5 KB | 3→10 | ●●●○○ | ●●●●● | ●●●●● | ●●●●○ | ●●●●● | ●●●○○ | ●●●●○ |
| I3 sunburst | ~30 KB | 3→10 | ●●●●○ | ●●●●○ | ●●●●● | ●●○○○ | ●●●●○ | ●●●●● | ●●●○○ |
| I4 proof gradient | ~5 KB | 4→14 | ●●○○○ | ●●●●● | ●●●●● | ●●●○○ | ●●●●○ | ●●●●○ | ●●●●● |
| I5 evidence cards | ~6 KB | 2→8 | ●●○○○ | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●●●○ | ●●●●○ |
| I6 pictogram rows | ~12 KB | 3→10 | ●●○○○ | ●●●●○ | ●●●●● | ●●●●○ | ●●●●● | ●●●●● | ●●●●○ |

**One caution on I5:** showing real example values on a public site means
publishing real identifiers. EINs and ZIPs of organizations are public record;
anything person-grade is not the same call. That's a RED-lane decision, flagged
here, not made.

---

# The library capability matrix

**What this table is for:** picking a *tool* is a separate decision from picking
a *picture*. This is every tool worth considering, what it can actually do, and
whether it's already on this machine.

**Verification rule applied:** every version number and license marked ✅ was
checked against current documentation or the local install **this session**.
Anything marked ⚠️ is from general knowledge and has NOT been re-verified — do
not treat those as facts.

## Python, static-image output

| Tool | Version / license | Installed here? | Interactive | Scale ceiling | Static export | Web embed | Honest note |
|---|---|---|---|---|---|---|---|
| **matplotlib** | 3.11.1, Jul 2026 ✅ / BSD ⚠️ | ❌ no | none | ~100k points before it crawls | PNG/SVG/PDF — best in class | as an image | 3.11 overhauled text/font handling (HarfBuzz, full internationalization) ✅. Total control, ugly defaults, real design work possible via stylesheets. Five other options below depend on it. |
| **seaborn** | ⚠️ not verified / BSD ⚠️ | ❌ no | none | inherits matplotlib | via matplotlib | as an image | Statistical convenience layer. Buys you little here — these are counts, not distributions (except F4/E6). |
| **plotnine** | 0.15.7, Jun 2026 ✅ / MIT ⚠️ | ❌ no | none | inherits matplotlib | via matplotlib | as an image | Grammar-of-graphics (ggplot2 grammar in Python). If you think in "map this column to this channel," this is the most fluent Python option. |
| **Datashader** | 0.19.1 ✅ / BSD ⚠️ | ❌ no | none alone | **claims billions of points** ✅ | PNG | as an image | The only Python tool built for your 181M/84M numbers. Rasterizes server-side so the browser downloads a picture, not data. Needs Numba; pairs with HoloViews for interactivity. |
| **PyWaffle** | ⚠️ not verified / MIT ✅ | ❌ no | none | thousands of icons | via matplotlib | as an image | Icon arrays / pictograms — directly relevant to F1 and I6. Font Awesome icon support. Requires matplotlib. |
| **NetworkX** | 3.2.1 ✅ / BSD ⚠️ | ✅ **yes** | none | layout gets slow past ~10k nodes | via matplotlib | as an image | Graph *algorithms* more than graph drawing. Use it to compute the layout, draw it elsewhere. |
| **Graphviz / PyGraphviz** | ⚠️ not verified / EPL ⚠️ | ❌ no | none | thousands of nodes | SVG/PNG | SVG embeds fine | Best automatic layout for H1-style system diagrams. Distinctive academic look that is genuinely hard to design past. |
| **Pillow** | 11.3.0 ✅ / MIT-CMU ⚠️ | ✅ **yes** | none | pixel-bound | PNG/JPG | as an image | Not a chart library — a pixel canvas. This is what you'd drive for A6/D6/G5-style hand-built metaphor art from Python. |

## Python → interactive web output

| Tool | Version / license | Installed here? | Interactive | Scale ceiling | Static export | Web embed | Honest note |
|---|---|---|---|---|---|---|---|
| **Plotly (py)** | 6.6.0 local ✅ / MIT ⚠️ | ✅ **yes** | strong, built-in | ~50-100k SVG points; WebGL traces go higher | needs kaleido (**not installed**) | writes standalone HTML | Fastest path from a dataframe to a working interactive chart on this machine right now. Its default look is recognizably "a Plotly chart" — polish takes real theming work. |
| **plotly.js** | bundle: full 3.3MB raw / 1.2MB min / ~391KB gzipped; "basic" partial ~318KB gzipped ✅ | (bundled) | strong | as above | — | script tag | **The page-weight problem in this whole document.** ~318KB gzipped minimum is more than every hand-rolled option in this map combined. Partial bundles help; they don't make it small. |
| **Altair / Vega-Lite** | altair 5.5.0 local ✅ (6.x exists ✅) / BSD ⚠️ | ✅ **yes** | good (Vega signals) | tens of thousands of marks | via **vl-convert-python** — self-contained, **no Node or browser needed** ✅ (not installed) | JSON spec + vega-embed | Declarative: you describe the chart, not the drawing. Best "regenerate automatically" story of any option here — the chart is a JSON file your audit script can emit. |
| **Bokeh** | ⚠️ not verified / BSD ⚠️ | ❌ no | strong | good; server-callback model for big data | PNG via headless browser ⚠️ | standalone HTML | Sits between Plotly and D3. Its real edge is the server-side callback model, which you don't need for a static portfolio page. |
| **HoloViews / hvPlot** | holoviews 1.23.x ✅ (doc title) / BSD ⚠️ | ❌ no | strong | **inherits Datashader's scale** ✅ | via backend | Bokeh/Plotly HTML | The reason to care: HoloViews + Datashader is the documented path to *interactive* views of hundreds of millions of points. That combination is unique in Python. |
| **pyecharts** | 2.1.0, Feb 2026 ✅ / MIT ✅ | ❌ no | strong | ECharts handles ~100k+ via canvas | — | standalone HTML | Python wrapper over Apache ECharts. Matters because ECharts has the best "editorial/graphic-design" default look of the mainstream libraries and ships forms the others don't. |
| **Apache ECharts (js)** | 6.1.0 ✅ / Apache-2.0 ✅ | (CDN/inline) | strong | canvas-based, good | SVG or canvas render modes | script tag | v6 added a **native chord series** and a **matrix coordinate system** ✅ — directly relevant to E5 and E3. Also has treemap, sunburst, sankey, graph, and themeable rivers built in. |
| **pydeck / deck.gl** | pydeck 0.9.2 local ✅ / deck.gl v9, WebGL2 via luma.gl v9 ✅ / MIT ⚠️ | ✅ **pydeck yes** | strong, GPU | **millions of points** | — | HTML/JS | Built for geographic layers but the layer model works for abstract point clouds too. WebGPU is in progress, **not enabled in 9.0** ✅ — so WebGL2 is what you'd ship. |
| **Panel / Dash** | dash 4.4.1 local ✅ / MIT ⚠️ | ✅ dash yes, ❌ panel no | full app | depends on backing chart | — | needs a running server | **Both need a live Python server.** For a static portfolio site that is a hosting commitment, not a chart. Listed for completeness; the mismatch is structural. |

## JavaScript, for the site itself

| Tool | Version / license | Interactive | Scale ceiling | Static export | Honest note |
|---|---|---|---|---|---|
| **D3.js** | 7.9.0 is latest on npm; **no v8** ✅ / ISC ⚠️ | anything you write | SVG: ~10k marks; canvas: millions | render to SVG string | Not a chart library — a set of tools for building one. Beats every Python option on total control and design ceiling. Costs hand-written code for every element. Its sub-modules (`d3-hierarchy`, `d3-sankey`, `d3-chord`, `d3-scale`) are usable **without** the rest of D3, which is how you keep the page light. |
| **Observable Plot** | ⚠️ current version not verified / ISC ⚠️ | good | thousands of marks | **SSR via JSDOM works** ✅ — but docs warn it's "only practical for simple plots of small data" ✅ | The concise middle ground: D3's grammar with far less code. Stylesheet is now inlined into the generated SVG ✅, which makes single-file embedding clean. |
| **Observable Framework** | 1.13.4 ✅ / open source, exact license not verified ⚠️ | full | data loaders precompute static snapshots ✅ | it *is* a static site generator | If the portfolio page becomes a whole data site rather than a few graphics, this is the purpose-built option: your Python audit script becomes a data loader, the site builds static. |
| **cosmos.gl** | v3.0 ✅ / **MIT** ✅ / npm `@cosmos.gl/graph` ✅ | GPU force-graph, live | claims "hundreds of thousands of points and links" ✅ | canvas snapshot only | OpenJS Foundation incubating project ✅, rendering ported from regl to luma.gl in v3 ✅. The serious option for E4 as a *live* graph. |
| **Cosmograph** | **CC-BY-NC-4.0 — non-commercial only; commercial use requires contacting them** ✅ | as above, friendlier API | as above | — | ⚠️ **Licensing flag.** A portfolio site is a gray zone. The underlying MIT engine above has no such restriction. |
| **sigma.js + graphology** | v3 ✅ / license **not verified this session** ⚠️ | strong, WebGL | "thousands of nodes and edges" ✅ | — | The established WebGL graph option. graphology handles the data structure and layout algorithms separately from rendering, which is a cleaner split than most. |
| **three.js** | ⚠️ not verified / MIT ⚠️ | full 3D | GPU-bound, very high | — | For genuinely 3D or heavily animated pieces. Big bundle, big effort, big differentiation. Overkill for any bar chart in this document; correct for two of the wild ideas below. |
| **regl** | ⚠️ not verified / MIT ⚠️ | low-level WebGL | millions of points | — | Thin functional layer over WebGL. What you'd use for a custom million-dot field where you want no framework at all. |
| **p5.js** | ⚠️ not verified / LGPL ⚠️ | creative-coding loop | canvas-bound | canvas snapshot | The creative-coding option: generative, sketch-like, made for visual metaphor rather than charts. Relevant to A6/D6/G5. |
| **rough.js / roughViz** | rough.js <9kB gzipped ✅; roughViz 2.0.5 ✅, built on D3v5 ✅ / MIT ⚠️ | basic | small data only | SVG | Hand-drawn sketchy aesthetic. Its own docs say to use it where the goal is *intent or generality, not absolute precision* ✅ — which is a real argument against using it for audit numbers, and a real argument for it on a concept diagram. |
| **Chart.js / Recharts / Nivo** | ⚠️ none verified this session | standard | thousands | varies | The "web dev default" tier. Fast, fine, and visually identical to every dashboard on the internet — which is the opposite of what a portfolio piece is for. |
| **LayerCake (Svelte)** | ⚠️ not verified / MIT ⚠️ | full | your call | SSR-able | If the site is Svelte, this gives D3-level control with component structure. Only relevant if the site's framework is already chosen. |
| **DuckDB-WASM** | duckdb 1.4.5 locally ✅; WASM build ⚠️ not verified | queries in the browser | millions of rows client-side | — | Not a chart library — the thing that would let a visitor *query* the audit data live in their browser. Relevant to E7 and to wild idea 4. |
| **Highcharts / Flourish / Datawrapper** | ⚠️ none verified / **commercial licensing** | strong | varies | yes | The paid tier. Datawrapper and Flourish produce genuinely good-looking editorial charts with near-zero code. **Cost and licensing not verified this session** — and per the money rule, any of these needs a price tag before it's a real option. |

---

# Cross-cutting notes

These apply to almost every row above and are easy to discover too late.

### Page weight, ranked honestly
- **Hand-rolled SVG/CSS:** 2-15 KB. Nothing beats it.
- **Static PNG from Python:** 30-200 KB, zero JavaScript, works with JS
  disabled, and can be `loading="lazy"`.
- **Vega-Lite embed:** the spec is ~2-10 KB but vega + vega-lite + vega-embed
  runtime is a few hundred KB ⚠️ (not measured this session).
- **plotly.js:** ~318 KB gzipped minimum, verified ✅. That's the single
  heaviest common choice in this document.
- **WebGL (deck.gl / cosmos.gl / three.js):** hundreds of KB to megabytes, plus
  it will not render at all on a device without working WebGL.

**The hybrid that most editorial sites use:** ship a static image, and only
load the interactive version when the visitor clicks "explore this." You get a
fast page and a deep option. Worth knowing this exists before choosing between
"static" and "interactive" as if they were exclusive.

### Where interactivity genuinely earns its place — and where it doesn't
- **Earns it:** E7 (browsing 24,011 real pairs), H3 (one diagram for two
  audiences), C5 (the correction as an action the visitor performs), D5 (walking
  the pipeline stages).
- **Decoration:** hovering a 7-bar chart to see the number that could have been
  printed on the bar. Most tooltips on most of these charts are in this
  category. A number label costs 0 KB and works on touchscreens.

### Accessibility, by rendering technology
- **SVG/HTML:** every element is a real DOM node — `aria-label`, `<title>`, and
  a text alternative all work. Best case.
- **Static image:** one `alt` attribute carries everything. Limited but honest,
  and it never breaks.
- **Canvas / WebGL:** a screen reader sees one empty box. **Any canvas concept
  in this document (A2, A3, D7, F1-as-canvas, F7, E4, and all the WebGL options)
  needs a parallel text or table description written by hand** — that's real
  work, not a checkbox, and it's not in the effort estimates above.
- **Color:** every concept that encodes trust tiers by color needs a
  colorblind-safe ramp plus a second channel (shape, position, or label).
  Trust tiers are exactly the kind of ordered category where color-alone fails.

### Light/dark theme
Anything drawn from CSS variables flips themes for free. Anything baked into a
PNG needs **two exports**, one per theme — which doubles the regeneration step
for every static-image option. Your existing pages are committed dark-only,
which sidesteps this entirely; adopting a light theme later reopens it for
every static image ever exported.

### Regeneration — the question that decides whether this ages
There's a clean split in this document:
- **Regenerates itself:** anything where the audit script emits data and a
  template renders it (all the chart-grammar options, all the hand-rolled SVG
  built from a JSON file).
- **Doesn't:** every illustration and metaphor concept (A6, C4, D6, G2, G5, H4).
  Those are drawings with numbers in them, and when the numbers change, someone
  redraws them. That's not a flaw — it's the price of the highest Wow scores in
  this document, and it should be paid knowingly.

The pattern already in this repo handles the first case: extract to JSON,
template with a placeholder, string-replace at build. That's a durable
regeneration path and it exists today.

---

# The wildest ideas

**Kept in deliberately, including the impractical ones.** Each is labeled with
what could go wrong. None of these is being suggested — they're here because a
menu that only contains safe options isn't a menu.

### W1. The warehouse as a walkable city
An isometric or first-person 3D scene where every table is a building: height ∝
rows, district = schema, materials = layer (landing / mart / metadata). The two
dead databases are an unlit district with 254 empty storefronts. The visitor
moves through it. Every number in this entire document has a physical address.

- **Tool:** three.js, or deck.gl's polygon layers for a flatter isometric version.
- **Risk:** very high. 15-60+ hours, megabytes of bundle, unusable on low-end
  phones, needs a full accessible text alternative, and it can very easily read
  as a tech demo rather than as evidence. It is also the single most
  differentiated thing on this list — nobody's data portfolio has this.

### W2. Sonification — the warehouse as sound
Each database is an instrument, pitch by row count, density by table count. The
DOCKET noise story becomes literal noise; the 45 trustworthy pairs become 45
clean bell strikes over it. A 40-second audio piece plus a visual score.

- **Tool:** Web Audio API, no library needed. Optionally Tone.js ⚠️ (not verified).
- **Risk:** high, and it's *taste*, not engineering — sonification either lands
  as striking or as gimmick, with little middle ground. Genuine upside: it's the
  only concept in this document that's fully accessible to a blind visitor by
  design rather than by retrofit.

### W3. The broadsheet — the audit as a printed front page
Set the whole thing as a newspaper page: masthead, headline number, columns of
text, small precise charts inline in the text column, and — bottom right, boxed
— a **CORRECTION** notice carrying the 2,909 reclassification and the 847→183
re-count, in the exact register a newspaper uses to correct itself.

- **Tool:** pure HTML/CSS with a real editorial typeface; charts as inline SVG.
- **Risk:** low technically, high on execution — bad newspaper pastiche looks
  cheap instantly. The conceptual payoff is unusually strong: it makes "we
  correct ourselves in public" the *form* of the page, not a claim inside it.

### W4. Don't trust me — run it yourself
Embed a real query engine in the page with the audit's CSVs loaded. A visitor
types SQL, gets the same numbers the page claims, in their own browser. Ship
four or five pre-written queries as buttons ("count the trustworthy docket
pairs yourself").

- **Tool:** DuckDB-WASM (DuckDB 1.4.5 is installed locally ✅; the WASM build's
  current size and version were **not verified this session** ⚠️).
- **Risk:** medium-high. Several MB of WASM, and it invites scrutiny of the data
  — which is either the whole point or a liability, depending on how ready the
  numbers are. That readiness call is not a design question.

### W5. The coincidence machine
A small interactive toy: two sliders set two ID ranges (say "a small bank ID
space" and "a huge court docket space"). The visitor watches the false-overlap
percentage climb toward 100% without a single real connection existing. Then
one button: "this is the FDIC/CourtListener pair — 99.98%."

- **Tool:** ~150 lines of vanilla JS and an SVG. Genuinely small.
- **Risk:** low technically. The real risk is that it teaches the visitor to
  distrust overlap numbers — including your own. That's either the most
  credible thing on the site or a self-inflicted wound, and which one it is
  isn't a technical judgment.

### W6. The entity constellation, as a physical print
33.3M golden entities as a generated star field, clustered by entity type,
rendered at poster resolution — a one-off piece of art with a legend, designed
to be printed at A1 and also shown on the site as a deep-zoomable image.

- **Tool:** Pillow (installed) or Datashader for the render; a tiling zoom
  viewer for the web version.
- **Risk:** medium. It regenerates badly (it's art), and a star field is a
  well-worn visual. Its strength is that it's the only concept here that exists
  off the screen.

---

# End of options

No recommendation, no shortlist, no "if I had to pick" — by design. What's
above is **60 picture concepts across 9 metric groups, plus 6 wild ones, plus
30 tools**, each scored on the same nine dimensions so they can be compared
without being ranked for you.

Two things worth knowing before you weigh them, stated as facts rather than
advice:

1. **The single biggest fork isn't which library — it's static vs. interactive
   vs. illustrated.** Static regenerates itself and loads instantly. Interactive
   earns its keep on roughly four of the 60 concepts. Illustrated wins every Wow
   score and every one of them goes stale when the numbers change.
2. **Six of the nine metric groups need no charting library at all.** Groups A,
   C, F, G, H, and I are mostly typography, SVG, and one canvas loop. The
   library question only really bites on the graph-scale concepts (D7, E4) and
   the exploratory ones (E7).

---

# Appendix: what was verified this session, and where

Checked against live documentation or the local machine on 2026-08-25:

- **Datashader** v0.19.1; billion-point claim; Python 3.10-3.14 —
  [datashader.org](https://datashader.org/releases.html),
  [github.com/holoviz/datashader](https://github.com/holoviz/datashader)
- **pyecharts** 2.1.0 (Feb 10 2026), MIT —
  [PyPI](https://pypi.org/project/pyecharts/),
  [GitHub](https://github.com/pyecharts/pyecharts)
- **Apache ECharts** 6.1.0, Apache-2.0, new chord series + matrix coordinate
  system in v6 —
  [ECharts 6 features](https://echarts.apache.org/handbook/en/basics/release-note/v6-feature/),
  [npm](https://www.npmjs.com/package/echarts)
- **Observable Plot** server-side rendering via JSDOM, and its own warning that
  SSR suits only simple/small plots; stylesheet now inlined in the SVG —
  [Plot docs](https://observablehq.com/plot/features/plots),
  [GitHub](https://github.com/observablehq/plot)
- **cosmos.gl** MIT, v3.0, WebGL2 via luma.gl, `@cosmos.gl/graph`, OpenJS
  incubating — [GitHub](https://github.com/cosmosgl/graph),
  [OpenJS announcement](https://openjsf.org/blog/introducing-cosmos-gl)
- **Cosmograph** CC-BY-NC-4.0, commercial use requires contacting them —
  [Cosmograph docs](https://cosmograph.app/docs-general/)
- **deck.gl** v9, WebGL2 via luma.gl v9, WebGPU not enabled in 9.0 —
  [deck.gl what's new](https://deck.gl/docs/whats-new),
  [WebGPU doc](https://deck.gl/docs/developer-guide/webgpu)
- **plotly.js** bundle sizes (full 3.3MB raw / 1.2MB min / ~391KB gzipped;
  basic partial ~318KB gzipped) —
  [plotly.js dist README](https://github.com/plotly/plotly.js/blob/master/dist/README.md)
- **vl-convert-python** self-contained static export, no Node or browser
  needed — [GitHub](https://github.com/vega/vl-convert),
  [PyPI](https://pypi.org/project/vl-convert-python)
- **D3** latest published is 7.9.0; no v8 — [npm](https://www.npmjs.com/package/d3?activeTab=versions)
- **sigma.js** v3 on graphology, WebGL — [sigmajs.org](https://www.sigmajs.org/docs/)
  *(license not verified)*
- **PyWaffle** MIT, Font Awesome icon support, matplotlib-based —
  [GitHub](https://github.com/gyli/PyWaffle)
- **rough.js** <9kB gzipped; **roughViz** 2.0.5, built on D3v5, explicitly for
  "intent or generality, not absolute precision" —
  [roughjs.com](https://roughjs.com/), [roughViz](https://github.com/jwilber/roughViz)
- **Observable Framework** 1.13.4, static site generator with data loaders —
  [GitHub](https://github.com/observablehq/framework)
- **matplotlib** 3.11.1 (3.11.0 released Jun 11 2026), text/font overhaul —
  [release notes](https://matplotlib.org/stable/release/release_notes.html)
- **plotnine** 0.15.7 (Jun 13 2026) — [changelog](https://plotnine.org/changelog.html)
- **Local machine** (checked directly): plotly 6.6.0, altair 5.5.0, pandas
  2.3.3, numpy 2.0.2, networkx 3.2.1, pydeck 0.9.2, dash 4.4.1, Pillow 11.3.0,
  duckdb 1.4.5, Node v22.23.2, Chrome present. **Absent:** matplotlib, seaborn,
  plotnine, datashader, bokeh, holoviews, hvplot, pyecharts, kaleido,
  vl-convert-python, graphviz, scipy, geopandas.

**Not verified this session** (do not treat as fact): Bokeh, Panel, three.js,
regl, p5.js, Chart.js, Recharts, Nivo, LayerCake, DuckDB-WASM, Graphviz, and
all Highcharts / Flourish / Datawrapper pricing and licensing. Every license
marked ⚠️ above is from general knowledge only.
