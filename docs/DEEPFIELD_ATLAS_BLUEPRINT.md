# DEEPFIELD — The Ripple Atlas Blueprint

*The master design spec for visualizing the Library: 1,043 tables,
2,694 verified connections, and the 85% that is still dark.*

*Direction set 2026-08-02. The working build is [`deepfield.html`](deepfield.html) —
a standalone, self-contained file: open it by double-clicking, no server, no
network, no dependencies. Rebuild its data with `python -m viz.compile_atlas --inline`.
This file is the spec; `deepfield.html` is the instrument.*

*House rule, inherited from [`RIPPLE.md`](RIPPLE.md): **never trust a number
typed in prose.** Every count below is dated 2026-08-02 and read live from
`outputs/connect_graph.json`. Re-read the file, don't quote this one.*

---

## Contents

1. [The spine — the lensing method](#1-the-spine)
2. [What the data already decided](#2-what-the-data-decided)
3. [The visual & structural engine](#3-the-engine)
4. [The interaction paradigm](#4-the-interaction-paradigm)
5. [The tech stack](#5-the-stack)
6. [The build path](#6-the-build-path)
7. [Open calls for Chris](#7-open-calls)

---

## 1. The spine — the lensing method {#1-the-spine}

**This is not a diagramming tool. It is an instrument for finding things that
aren't there.**

Chris's framing, which is now the constitution's §1.1: *"we think something is
out there, and we're going to look based on what we see it affecting."*

That is gravitational lensing. Astronomers cannot see dark matter. They find it
by watching light bend around a mass that appears on no chart, and they point
the next telescope at the bend. Ripple's method is structurally identical:

| Astronomy | Ripple | Share of the Library |
|---|---|---:|
| Ordinary matter — the part that shines | Tables with a verified connection | **155 · 14.9%** |
| Dark matter — invisible, but you see it bend things | Tables carrying a real, populated key that *still* connect to nothing | **82 · 7.9%** |
| Nothing to measure with | Tables with no populated identity column at all | **131 · 12.6%** |
| Dark energy — the unexplained majority | Tables never admitted to the graph (the parked `PORTAL_*` crawl) | **675 · 64.7%** |
| Lensing — light bending around it | Two datasets that should overlap and measurably don't (`hunch_absence_verdicts`) | — |
| Pointing the next telescope at the bend | The absence queue: verified gaps become the ranked hunt list | — |

The proportions are not a stretched analogy. Real cosmology runs roughly 5%
ordinary matter, 27% dark matter, 68% dark energy. The Library runs 14.9% lit,
20.5% dark-but-charted, 64.7% never looked at. **Both are mostly the thing you
can't see.**

**Design consequence, and it is the whole point:** absence is not a toggle, an
overlay, or a filter. It is a **first-class layer with its own ink, on by
default**, sitting under the verified mesh the way a gravity map sits under a
star chart. You read the field as *bright things = what we can see*,
*distortions = where something is hiding.*

Every other decision in this document serves that.

---

## 2. What the data already decided {#2-what-the-data-decided}

The layout was not chosen aesthetically. It was read out of the graph. Three
facts from `outputs/connect_graph.json` (2026-08-02) dictate the design:

**2.1 There are four states, not two.** Every off-the-shelf tool sorts tables
into "connected" and "not connected." That collapse destroys the only
distinction that tells you what to do next. Measured live:

| State | Count | What it means | What it demands |
|---|---:|---|---|
| **LIT** | 155 | Has ≥1 verified edge | nothing — it works |
| **DARK** | 82 | Carries a real, populated key and *still* matches nothing | **the hunt list** — measured absence is evidence |
| **KEYLESS** | 131 | No populated identity column at all | an *acquisition* problem — go get better columns |
| **UNCHARTED** | 675 | Never entered edge discovery | a parked *decision* — 668 are `PORTAL_*`, excluded on purpose |

Three completely different jobs. The map draws them three different ways, and
**82 is the number that matters** — it is small enough for a human to actually
work through, which is the entire point of separating it from the other two.

A note on the 675: they are excluded by an explicit, documented decision in
`connect/discover.py` (`EDGE_UNIVERSE_EXCLUDE_PREFIXES`), pending the open
"finish or prune the portal crawl" question from the 2026-07-27 inventory audit.
Verified 2026-08-02: **672 of those 675 carry at least one populated,
non-probabilistic key.** They are not technically blocked. They are waiting on a
ruling — which makes that ruling the single biggest lever on how dark the map
looks.

**2.2 The edges speak named languages.** Every one of the 2,694 verified
connections travels over an identity system, and the distribution is lopsided
enough to be structural:

| Key family | Edges | Reads as |
|---|---:|---|
| `NAME@ZIP` | 1,242 | the name bridge |
| `CCN~NPI` | 318 | health, bridged |
| `NPI` | 258 | health / providers |
| `EIN` | 201 | money / employers |
| `FIPS` | 190 | land / place |
| `CIK` | 94 | markets / filings |
| `FRS_ID` | 91 | environment |
| `CCN` | 78 | facilities |
| `ZIP` | 50 | place, coarse |
| `PWSID` | 36 | water systems |
| `CIK~EIN` | 36 | markets, bridged |

*(Full tail continues: `COUNTRY` 16, `EIN~UEI` 16, `FEC_CAND_ID` 15, `GEO_IN` 15, …)*

These families are the real geography of the Library. Tables that speak `NPI`
belong together regardless of which agency published them. **The organizing
force is already in the data — the job is to draw it, not invent one.**

**2.3 Darkness is the signal.** 888 of 1,043 tables — **85.1%** — have no
verified connection. Those tables hold 429 million rows, roughly half the
Library's total mass, entirely unweighed. A conventional tool hides them as
clutter. Per §1, they are the mission.

Proof-tier distribution, which becomes the line grammar:

| Tier | Count | What it means |
|---|---:|---|
| CORROBORATED | 1,246 | proven over softer evidence |
| STEEL | 806 | exact ID match, measured |
| BRIDGE | 370 | reached via a crosswalk, not direct |
| GEO | 271 | same place, not same entity |
| STRONG | 1 | domain ID, the odd duck |

Scale note for the compiler: the connect engine tested **2,664,155 pairs** to
find 2,694 edges. The expensive thinking is already done and already on disk.

---

## 3. The visual & structural engine {#3-the-engine}

### 3.1 The metaphor: identity gravity

The field is a dark chart. **22 anchor wells** — one per key family, listed in
`viz/compile_atlas.py`'s `WELLS` — sit at fixed positions, like capital cities.
**They never move.** Their order in that list sets their angular position, so
reordering it rotates the whole map and burns everyone's spatial memory. Don't.

Every table is placed at the **weighted barycenter of the key families it
actually carries**, with weights from `outputs/connect_fingerprints.json`:
fill rate × distinct-value ratio (see the honesty note in §3.4). A light
collision-relaxation pass separates overlapping neighbors. The consequences
fall out for free:

- **Monolingual tables orbit tight.** The CMS pile that only speaks `NPI`
  forms a dense constellation hugging the NPI well. Instant visual module, no
  clustering algorithm, no tuning.
- **Polyglot tables drift into the straits.** `FED_EPA_FRS_FULL` (104 edges),
  the corporate crosswalks, CMS enrollments — anything speaking three languages
  physically sits in the interstitial territory between wells. **The bridges of
  the Library become literal geography.** You find crosswalks by looking at the
  channels between territories.
- **The layout is deterministic.** Fixed seed, same inputs → same map, every
  session, forever. Position becomes memory: "OSHA lives southwest of the EIN
  well" stays true next month. New tables fade in at their charted position;
  nothing else moves.

Top hubs as of 2026-08-02, which will be the visually dominant bodies:
`FED_CMS_MEDICARE_PROVIDER` (105 edges), `FED_EPA_FRS_FULL` (104),
`FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER` (102),
`FED_CMS_PART_D_PRESCRIBERS` (89), `FED_OSHA_ITA_300A_SUMMARY_2025` (89).

### 3.2 What a table looks like

Four honest channels, no decoration:

- **Luminosity / size** = log(row count) plus degree. A 100-row lookup glimmers;
  a 20M-row hub burns.
- **Hue** = dominant key family. A glance reads "that region is money, that one
  is health, that one is land."
- **Form encodes state**, and this is the load-bearing choice — the four states
  are not four shades of grey, they are four different *shapes*:

  | State | Mark | Why that mark |
  |---|---|---|
  | LIT | filled core + glow | it shines; it is connected |
  | DARK | **hollow ring, no fill** | a hole where mass should be — placed *in* lit territory, beside the well it speaks, with no corridor reaching it |
  | KEYLESS | a bare tick | nothing to hold; it has no handle to join by |
  | UNCHARTED | a faint dot on the outer ring | genuinely off the map, because nobody looked |

- **Halo** = best proof tier present, so well-proven territory visibly glows
  harder than tentative territory.

The DARK ring is the single most important mark in the system. It is *not*
banished to a margin — banishing it would hide the very thing we are hunting.
It sits exactly where its keys say it belongs, and the missing corridor is
visible as a shape.

### 3.3 Edges as corridors, proof as line-weight

2,694 straight lines is a hairball. Edges sharing a key family are drawn
**bundled along that family's corridor** (force-directed edge bundling, computed
once at build time), so the macro view shows a dozen luminous arteries instead
of three thousand hairs. Hover the EIN well → its 201 edges ignite as one river.

The five tiers map to line grammar. **The chart never draws a connection as more
certain than the engine proved it** — this is the [`RIPPLE_DESIGN_BRIEF.md`](RIPPLE_DESIGN_BRIEF.md)
confidence-ladder rule, inherited and non-negotiable:

| Tier | Ink |
|---|---|
| **STEEL** | Solid, full brightness, heaviest weight. The load-bearing iron. |
| **CORROBORATED** | Solid, half weight. The bulk of the mesh. |
| **GEO** | Dashed. "Same place" — real, but place-grade, not entity-grade. Reads looser at a glance, on purpose. |
| **BRIDGE** | Dotted arcs routed *visibly through* the crosswalk node that enables them. A bridged claim never disguises itself as direct. |
| **STRONG** | Thin solid. Keeps its own honest weight. |

### 3.4 Spectral barcodes — every table's fingerprint is its face

Inside a source, each table gets a machine-generated visual identity from
`connect_fingerprints.json`: one vertical stripe per ID column, where

- stripe **hue** = key family,
- stripe **brightness** = fill rate,
- stripe **solidity** = distinct-value ratio.

This encodes the platform's hardest-won lesson — the NPPES `EIN` and NOAA_AIS
`imo_number` burns, per constitution §7 — directly into the visual language.
A column that is 100% "populated" but sentinel-masked renders as a **bright
stripe with a hollow, hatched core**. The trap that fooled a null-check twice
cannot fool an eyeball once.

### 3.5 The unlit census

The census panel is permanent HUD furniture, not a stat you go looking for.
Every session opens with the four counts and one line in the accent colour:
**"85.1% of the Library is unconnected."** Each row is also a filter, so the
gauge and the control are the same object.

The 675 uncharted tables render as a **dim ring at the periphery** — present,
counted, deliberately outside the lit territory, because "we never looked" is a
different claim from "we looked and found nothing" and the map must not blur
them.

When the connect engine verifies a new edge, that table **physically migrates**
into the field, pulled to its barycenter over a ~2s glide. That animation is the
platform's heartbeat made visible, and it is the single most motivating pixel in
the design.

### 3.6 The lensing layer

Per §1, this is first-class and default-on. `hunch_absence_verdicts.json`
renders as thin **hairline arcs in a reserved color used for nothing else**,
connecting pairs that should overlap and measurably don't. They sit *beneath*
the verified mesh — a gravity map under a star chart.

**And they are clickable into a queue.** The absence layer has a companion
panel: the ranked hunt list, sorted by how big the gap is versus expectation.
Drawing it is half the job; handing Chris the list is the other half.

### 3.7 The second projection: the Foundry

Structure is half the brief; **sequential interaction** is the other half.
Rather than a separate diagram, Deepfield holds **two projections of the same
nodes**. Toggle to *Foundry view* and every glyph keeps its identity, hue, and
label, but the field reorganizes into a left-to-right process cartogram:

```
LANDING → CONNECT engine → HUNCH lattice → HYPOTHESIS_CATALOG → Pattern Desk → Reading Room (human sign-off)
```

The morph is one staged ~900ms transition — nodes stream to their swimlane like
iron filings snapping to a new magnet. Because identity persists across the
morph, you never lose the thing you were studying. One dataset, two truths:
*where things live*, and *how things flow*.

The Reading Room lane terminating the flow is not decorative — it draws
constitution §7 (human sign-off on every finding, auto-publish blocked) into the
picture of the machine.

---

## 4. The interaction paradigm {#4-the-interaction-paradigm}

### 4.1 Semantic zoom — four registers

Zoom is **disclosure**, not magnification. Hard thresholds, crossfaded handoffs,
never a moment of soup.

| Band | Name | Shows | Question it answers |
|---|---|---|---|
| **Z0** | The Field | 1,043 glyphs, anchor wells, bundled corridors, unlit ring, lensing arcs. Labels on wells + top hubs only. | What territories exist and what binds them? |
| **Z1** | The Precinct | One well's territory, 20–80 tables. Bundles relax into individual tier-weighted edges. Everything labeled. | Who speaks this language, and how well proven is each link? |
| **Z2** | The Station | One source unfolds into a shallow isometric platform: each table a slab, height = row count, face = its spectral barcode. Edges dock into the specific slab and column they touch. | What's inside, and which table carries each connection? |
| **Z3** | The Schema | Full column list with fill/distinct microbars, lifecycle status from `CATALOG`, every edge endpoint with matched counts and sample values. | Can I trust this key, right now, with numbers? |

### 4.2 The camera

- **2.5D orthographic dolly.** The chart is a plane the camera flies over.
  Subtle parallax between edge / node / label layers gives depth without the
  disorientation of free 3D. Scroll = altitude, drag = pan, both with short
  critically-damped inertia. **No roll, no tumble** — north stays north, because
  cartographic permanence is the entire point.
- **Focus dive.** Double-click a glyph: camera dollies in on an eased curve
  while the rest of the field dims and desaturates. Band transitions fire
  mid-flight, so the source unfolds *as you arrive*.
- **The flight recorder.** Every dive appends to a breadcrumb strip on the
  bottom edge — a literal recorded flight path. `Esc` flies back out along it.
  You can always answer "where am I and how did I get here," which is the
  question that kills every other large-graph tool.
- **The compass rose.** A small fixed radar showing the anchor wells and your
  viewport as a bright rectangle. Hover any family on the rose → its corridors
  ignite across the whole field. One gesture answers "show me everything money
  touches."
- **Search is teleport with a contrail.** Type `osha`, enter, camera flies
  (~500ms, one smooth arc, never a hard cut), leaving a fading contrail so the
  spatial model survives the jump.
- **The URL is the state.** Camera, band, projection, pins, highlights all
  serialize. A pasted link reproduces the exact view. Views become shareable
  receipts.

### 4.3 Interrogation, not just navigation

- **The receipt panel.** Click any edge → exactly what the engine measured: key,
  tier, matched count, match rate, distinct counts both sides, and real sample
  values. Every line on the map produces its evidence on demand. Non-negotiable
  for a platform whose product is proof.
- **Trace mode.** Pick two tables; pathfind over the verified mesh; light every
  route, ranked by weakest-tier link. *"Can I get from FEC money to OSHA
  injuries, and which hop is shakiest?"* becomes a ten-second visual answer.
- **The absence queue.** Per §3.6 — the lensing layer's ranked hunt list, which
  is the method from §1 made operable.
- **Pins.** Right-click drops a survey pin; pinned glyphs stay lit at full
  saturation through any dimming, band change, or projection morph. Your working
  set never sinks back into the dark.

### 4.4 The scope law, enforced by the camera

Every dive ends in receipts; every `Esc` ends back at the whole field. The
instrument's resting state is the full map. **The UI physically resists
collapsing into "one nice little story"** — it always pulls back to the census.
That is constitution §1's scope law implemented as interaction design.

---

## 5. The tech stack {#5-the-stack}

**The law: heavy thinking at build time, dumb speed at runtime** — the same rule
the warehouse already lives by (constitution §7: AI is a build-time tool, not a
runtime dependency).

Nothing structural is computed in the browser. Nothing numerous is a DOM element.

### 5.1 The build-time compiler

`viz/compile_atlas.py` — a sibling of `connect/` — eats the four JSON outputs and
emits one static `atlas.json`:

- Barycentric layout + collision relaxation, **fixed seed**, deterministic by
  construction. Stable across sessions, and *diffable across weeks* — this
  month's atlas vs. last month's is itself an artifact: watch the unlit ring
  shrink.
- Edge bundling (FDEB) baked into precomputed polyline ribbons. The most
  expensive computation in the system, done once, never in the client.
- Per-band label priority lists, barcode textures, LOD cut lists.

Runtime needs no AI, no warehouse, no cost — it renders a file. Snowflake is
touched only by live-receipt panels, and those read registry tables
(`SOURCE_REGISTRY`, `CATALOG`, `CONNECT_EDGES`, `COLUMN_CATALOG`), never data.

### 5.2 The renderer

| Layer | Choice | Why |
|---|---|---|
| Canvas | **WebGL2 / Three.js**, orthographic camera | Boring, bulletproof, hiring-proof. WebGPU isn't worth its portability tax at 3k edges. *Pragmatic alternative: deck.gl buys picking + LOD free, at some aesthetic ceiling cost.* |
| Nodes | One instanced quad mesh + SDF shader | All 1,043 glyphs (and every column slab at Z2) in one draw call. Glow, tier halo, dim, hue = per-instance attributes; hover costs a uniform update, not a re-render. |
| Edges | One prebaked triangle-strip VBO | All bundled ribbons in a single buffer; tier (solid/dash/dot) and corridor hue in vertex attributes; dash animation and corridor-ignite are a shader time uniform. Zero per-frame geometry work. |
| Labels | SDF glyph atlas (troika-three-text) | **Text is the real performance boss at this scale, not lines.** Stays crisp through the whole zoom range; per-band priority lists cap live labels at ~120. |
| Picking | GPU color-pick buffer | Pixel-exact hover on nodes *and* curved ribbons at zero CPU cost. No quadtree drift on bundles. |
| UI chrome | HTML/CSS over the canvas | Receipt panels, flight recorder, compass, search — real accessible DOM where counts are small and text should be selectable. |
| State | zustand + URL serialization | One store: camera, band, projection, pins, highlights. The URL *is* the state. |
| Morphs | Dual position attributes + shader `mix()` | Field→Foundry is `mix(posA, posB, t)` per instance on the GPU. A thousand nodes reprojecting at 120fps costs one eased scalar. |

### 5.3 The frame budget, honestly

Per frame: one edge draw, one node draw, one label pass, one pick pass — ~4 draw
calls, under 200k triangles. **Single-digit milliseconds on integrated
graphics**; a phone holds 60fps.

The engineering risk at this scale was never triangle count. It's label
legibility, transition choreography, and layout stability — which is exactly
where this blueprint spends its effort. The ceiling is real: the same
architecture holds past 10,000 tables without redesign, because instancing and
baked ribbons scale linearly and semantic-zoom bands cap what's ever on screen.

---

## 6. The build path {#6-the-build-path}

Three phases. Each ships a usable instrument. Ordered because each feeds the next.

### Phase I — The Chart ✅ SHIPPED 2026-08-02
*compiler + static field*

`viz/compile_atlas.py` → `outputs/atlas.json` → [`docs/deepfield.html`](deepfield.html).
Identity-gravity layout, the four states, the census HUD, hover and click
inspection with per-table detail, search, lensing isolation, pan/zoom/keyboard.

Reads only `outputs/*.json`. **Zero Snowflake cost.** Standalone: no server, no
network, no dependencies — it opens by double-click and works offline. This
alone replaces every ERD conversation permanently.

Rebuild after the connect engine runs:

```bash
python -m viz.compile_atlas --inline
```

Verified at ship: layout is byte-identical across runs (md5-checked), the
inline step is idempotent, and the first frame costs 20 edge strokes and 6
gradient allocations rather than 2,694 and ~180.

### Phase II — The Dive
*semantic zoom + interiors*

Z1–Z3: precincts, stations, spectral barcodes, flight recorder, compass rose,
pins, trace mode, and the exportable hunt list. Tables unfold into isometric
column platforms. This is where all 1,043 tables become individually reachable
without the map ever showing more than a few hundred things at once.

### Phase III — The Machine
*projections + live feeds*

The Field↔Foundry reprojection; the absence queue wired to real ranking; and
"atlas over time" — watch tables migrate out of the dark as the connect
engine earns edges. Once `HYPOTHESIS_CATALOG` exists (pending
`infra/ddl/07_hypothesis_catalog.sql` in Snowsight), its surprise scores plug in
as a heat channel on the same glyphs.

---

## 7. Open calls for Chris {#7-open-calls}

Red-lane, per constitution §4. Phase I shipped without needing any of these,
but they shape Phases II and III.

**Surfaced by building the map — these are the new ones:**

1. **The portal crawl is 65% of the Library and has never been ruled on.**
   668 `PORTAL_*` tables sit outside edge discovery by a parked decision, and
   672 of the 675 uncharted tables carry a real key. Finish the crawl, prune it,
   or admit a sample of it to the graph — any of the three is defensible, but
   the current state means two thirds of the map is dark because nobody chose,
   not because anything failed. **This is the biggest single lever on the
   platform's coverage story.**
2. **131 tables hold 219M rows and cannot join anything.** No populated identity
   column at all. That's an acquisition backlog, not a matching problem. Worth
   deciding whether to re-ingest with better columns, or formally retire them.

**Carried from the original spec:**

3. **How loud is the lensing layer at rest?** Default-on is decided (§1). But
   *how* loud — a whisper under the mesh, or bright enough to compete with
   verified edges? The difference between "a map that notes gaps" and "a map
   about gaps."
4. **Does the absence queue ever auto-rank?** The engine can sort gaps by size
   versus expectation. Whether that ranking is presented as a priority order —
   the machine suggesting where to point the light — is a taste call with
   mission weight.
5. **Is the atlas ever public?** The design brief's Phase 1 says private
   workbench. A Deepfield showing the shape of the public record, carrying no
   findings, is arguably publishable and arguably the best single explanation of
   Ripple that exists. Not the same question as publishing a finding.

---

*Lineage: this blueprint absorbed and supersedes the visualization direction in
`lattice-map.html` (2026-08-01). Prior concepts survive as organs, not costumes —
the octopus became bundled corridors, the star map became the deep field, the
isometric platforms became station interiors, the manufacturing schematic became
the Foundry, the fractal tree became the four zoom registers. The spine is none
of them: it is a layout dictated by the Library's own measured identity systems,
so the beauty and the truth are the same object.*
