# 🧪 The Laboratory
*A running catalog of visualization techniques for massive/dense datasets — collected during Ripple idea war room sessions. Pure exploration mode: nothing here is committed to, some of it may be duds, that's fine.*

---

## 📊 Making Massive Scatter Plots Readable
*(the foundational problem — too many points to plot individually)*

- **Aggregate first** — histograms, heatmaps, hexbins. Plot summaries of groups, not every point.
- **Encode density, not position** — use color/opacity to show *how many* records overlap in a spot, instead of one dot per record.
- **Dimension reduction** — PCA, t-SNE. Squashes too many *variables* per point down into 2D so it can be plotted at all.
- **Sample or tier by zoom** — show a smart subset at first glance, reveal more as someone zooms in (how maps handle "don't render every blade of grass until zoomed in").

*Status: tabled mid-session, not yet explored deeply.*

---

## 🫀 The Organism Metaphor
*(mass / distance / circulation / ripples — mapped onto the actual Ripple warehouse)*

| Concept | Visualization Family | What It Answers | Ripple Equivalent |
|---|---|---|---|
| ⚖️ **Mass** | Density / heatmaps, bubble size, contour maps | "Where is there a lot?" | The 96.4M keys in DISPLAY_KEYSET_LIVE, 290M in KEYSET_LIVE *(spine wording retired 2026-09-01)* |
| 📏 **Distance** | Clustering, dimension reduction | "What's similar to what?" | Join-key relatedness logic in LIBRARY_META |
| 🩸 **Circulation** | Network / force-directed graphs | "What connects to what?" | The Catalog layer — CONNECT_EDGES / ENTITY_INDEX |
| 🌊 **Ripples** | Diffusion / propagation animation | "What happens if this changes?" | "Reverse peel" made visual — watching a mechanism propagate across the spine |

**Core sentence:** Mass and distance describe the organism's *anatomy*. Circulation and ripples describe its *physiology* — how it actually lives.

**Style notes for ripple animation (if built):**
- Easing, not snapping — things fade/grow gradually
- Muted palette + soft glow, not neon
- Only the ripple moves — the underlying map stays still

---

## 🔬 Physics-Derived Techniques
*(finding hidden structure, not just displaying known structure)*

- **Topological Data Analysis (TDA)** — finds shapes, loops, and voids in a data cloud that normal stats miss entirely.
- **Percolation theory** — from materials physics ("when does this become a conductor?"). Finds the *tipping point* where loosely-connected clusters suddenly become one giant connected system.
- **Network centrality** — calculates which nodes are secretly most important, even if they don't look busy (a 2-connection bridge node can matter more than a 50-connection node).
- **Entropy / information density** — measures how "surprising" or disordered a region is. Sudden drops in entropy can flag where a pattern just snapped into order.

---

## 🗺️ GIS / Geographic Techniques

- **Hotspot analysis (Getis-Ord Gi*)** — statistically confirms a cluster is *significantly* denser than random chance, not just visually dense.
- **Kernel Density Estimation (KDE)** — turns scattered points into a smooth "heat surface," like a weather map.
- **Spatial autocorrelation (Moran's I)** — checks if nearby things behave similarly (clustering) or oppositely (dispersion). Works on non-geographic "similarity distance" too.
- **Voronoi diagrams** — divides space into zones of influence around each point. *(Possible dud — cool visually, hard to make meaningful without genuine "ownership" logic in the data.)*
- **Flow maps** — shows movement *between* places (migration/trade origin). Could map how entities move between domains over time.

---

## 🧬 Other Domains Raided for Ideas

- **Epidemiology → contact tracing graphs**: built to answer "who touched whom, and how far did it spread."
- **Astronomy → sky surveys / N-body simulations**: handle billions of points using gravity-like attraction models to cluster related objects. Force-directed graphs' big sibling.
- **Neuroscience → connectome mapping**: maps millions of neurons and connections — nearly identical problem shape to the Catalog (huge number of connections, need to find the important circuits).
- **Ecology → food web / trophic cascade models**: models what happens when *removing* one species cascades through an ecosystem. Possibly the *best* template for "ripples" — built around removal and cascading effect, not just spread.
- **Music/Audio → spectrograms**: turns sound into a compact visual over time. Could solve the "ripple" problem as a *static image* instead of requiring animation. *(Possible dud — clever idea, probably a stretch to force onto tabular investigative data.)*
- **Finance → correlation matrices / heatmap clustering**: finds which things "move together." Same math as the distance/similarity problem, different label.

---

## 📌 Open / Tabled Questions
- Does the ripple animation live in the **Catalog** (technical, for Chris) or **Publishing** (for readers)?
- Deep dive on scatter-plot readability techniques — not yet explored beyond the initial list.
- Which 2–3 techniques across all categories are worth actually prototyping first?

---



---

## 🔎 How to Find Things — the method, 2026-09-05
*(from the "metric ton of data, now what" session. This is the part that turns the catalog above into findings.)*

**The one-liner:** don't look for things. Look for weird, then read the weird.

### The atom is an entity, not a question
| step | do | example |
|---|---|---|
| 1 | pick a key | NPI |
| 2 | pick the busiest value on it | the NPI in the most tables |
| 3 | pull every row about it | its dossier, ~10 tables |
| 4 | read it like a story, find the odd | paid $200k, wrote $3M scripts |
| 5 | count how many others do that | 2,431 more |

Questions are the wrong start. You need to know the answer to ask a good one.
The joins already did the work: they built the dossier. Step 4 is reading, not querying.

### The five weirdness passes — generic SQL, run over everything
| pass | question asked of every table / entity | output |
|---|---|---|
| 1 shape | what does normal look like, per column | distribution per column |
| 2 outlier | who sits far from normal, within their group | ranked list, top 50 |
| 3 coverage | who is in way more tables than peers | ranked list |
| 4 residual | who should join but doesn't, or double-joins | orphans, collisions |
| 5 change | where does a time series break | dates, per entity |

- Same SQL, 2,000 tables, no thinking per table. The computer does breadth, you do depth.
- Read only the top 50 of each list. Five passes, one evening.
- Most hits are data bugs. Fine. Those are traps to save.
- The residual pass is the sneaky one: a nonprofit with 40 UEIs is a bug or a story.
- Rank tables by leverage first: rows × keys × clock. Top 30 tables carry most of the surprise.
- **Product idea: a weirdness score per entity.** That is the whole thing.

### The slot machine
Random entity button → full dossier → weirdness score → next.
Find the story by playing, not by planning. Built for one player: Chris.

---

## 🔗 What the joins already allow — live counts, 2026-09-04
*(from CONNECT_EDGES, 4,512 proven pairs, and KEYSET_LIVE)*

| key family | tables | edges | matched rows | quality |
|---|---|---|---|---|
| NPI | 34 | 364 | 117M | steel |
| EIN | 34 | 366 | 10.4M | steel |
| FRS_ID / NPDES / PWSID | 37 | 226 | 67.8M | steel |
| CIK | 19 | 128 | 0.4M | steel |
| FIPS county | 15 | 78 | 0.2M | 73–100% |
| FEC cmte / cand | 19 | 81 | 0.5M | 72–100% |
| UEI / DUNS | 14 | 21 | 0.1M | thin |
| LEI / COMPANY_NO | 9 | 22 | 8.8M | steel |
| Courts, Congress | 13 | 47 | 0.2M | steel |
| NAME@ZIP | 122 | 2,512 | 38M | fuzzy |

In the keyset but no edges built yet: EIA plants, PECOS, AWARD_KEY, CUSIP, FDIC/RSSD, CAGE, IMO/MMSI, NAICS, SIC.
Bridge rule in code: hard keys cross, code keys never do. NAICS/SIC/FIPS/ZIP only group.
Full 62-shape catalog: `reports/viz_join_catalog_2026-09-04.md`.

### Five cross-layer hunts that are wired today
| hunt | chain | status |
|---|---|---|
| contractors with high injury rates | OSHA →EIN→ FAC →UEI→ USAspending | 441 employers match |
| PAC money → committee seat → bills | FEC →FEC_IDS→ Congress → GovInfo | column exists, no edge yet |
| opioid scripts vs county deaths | Part D →zip→ county ←FIPS CDC | wired |
| water violators vs who drinks it | SDWA →PWSID→ ECHO →FIPS→ county | wired |
| polluter parents | ECHO →FRS→ crosswalk →LEI→ GLEIF | 22,743 LEIs |

### Tried 2026-09-04, and what the skeptic said
- Open Payments × Part D on NPI: paid $10k+ prescribers cost 1.6x to 7x more per claim within specialty. Skeptic: drug mix, not behaviour; ProPublica did this join years ago.
- SAM exclusions × USAspending on UEI: 22 firms, $1.86M while debarred. Skeptic: UEI predates 2022 only via unvalidated backfill; mods on old awards are lawful.
- IRS auto-revocations × FAC × assistance: **trap.** Tribes, transit agencies, housing authorities auto-revoke because they never file. $13.4B of nothing.
- SAM NPI × Part D: zero excluded prescribers in Part D 2024. Either CMS works or the NPI column is empty-shaped. Unchecked.
Receipts: `reports/join_proof_2026-09-04.md`.

---

## ⏱ Time series shapes — what ticks, 2026-09-04
*(from LIBRARY_MARTS.TIMELINE.RIPPLE_TIME_REGISTRY, 643 sources classified)*

| clock | grain | sources | rows |
|---|---|---|---|
| happened | day | 123 | 598M |
| happened | year | 102 | 72M |
| reported | day | 81 | 64M |
| reported | quarter | 6 | 54M |
| decided | day | 29 | 17M |
| none | — | 241 | 83M |

Heaviest day-grain streams: ARCOS 179M, FEC individual contributions 84M, CourtListener dockets 72M, AIS 58M.

| shape | example |
|---|---|
| one line over time | ARCOS pills per day 2006–2019; CFPB complaints per week |
| two lines, one axis | pharma payments per month vs Part D scripts |
| before and after a date | MSHA violations 12 months either side of an accident |
| same entity, many years | one water system, 20 years, one sparkline |
| reported vs happened | FAERS carries both clocks; the lag is the chart |

Before-and-after is the cleanest visual there is. Build it first.

---

## 🪤 Traps met this week
- Registry VOLUME is prose, not a count. Quote `"CONNECT"` as a schema name.
- USAspending assistance columns are lowercase; quote them.
- GEO_IN edges to INTL_FR_DATA_GOUV_FULL match 100% on 22 tables. Fake.
- Government units in IRS auto-revocation lists are noise, not findings.

---

*Last updated: 2026-09-05 — method, joins, time series, traps folded in from the 09-04/05 sessions*
