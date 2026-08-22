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
| ⚖️ **Mass** | Density / heatmaps, bubble size, contour maps | "Where is there a lot?" | The ~12.88M entities across the 31 spine tables |
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

*Last updated: 2026-08-22 — Idea War Room session*
