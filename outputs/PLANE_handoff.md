# HANDOFF — Build "The Plane" (a Google-Earth-style explorer for the Ripple data WAREHOUSE)

*Paste this into a fresh Claude Code session in the Ripple_v6 repo. Self-contained — you shouldn't need the
conversation that produced it. Read `CLAUDE.md` and `build-state.md` first for repo norms + state.*

---

## WHAT THIS IS (and what it is NOT)

**This is a tool for Chris to EXPLORE HIS OWN DATA WAREHOUSE** — to *see what he has and how it connects*,
at a glance and in detail. The Google-Earth metaphor: his whole library as one map he flies through.

> "My warehouse as a map I fly through — zoom out and I see all my domains and which datasets are big and
> real; zoom in and I see how any dataset connects to the rest and which keys bridge them; click one and I
> see its full profile."

**Explicitly OUT OF SCOPE (this is the "product"/publishing layer — Chris is deliberately waiting on it):**
- ❌ NO entity/person corkboards (one banned doctor + their pharma checks).
- ❌ NO leads as glowing hotspots, NO "fly to a named person," NO investigation drill-down.
- ❌ NO web app / server. This is a self-contained file Chris opens to understand his data.

The unit of everything here is a **DATASET** (a landed table / source), never an entity. That keeps the
whole thing **static, offline, and simple** — 720 datasets, not 10.7M entities. Build it as a
self-contained `fig.write_html`.

**Foreman model:** Chris approves, doesn't do manual work. Build **v0 first, then checkpoint with him.**
Casual tone, full code blocks, map-not-essay. Stack is FIXED: Python + Plotly + Snowflake.

---

## START HERE — the map already exists as data

**Do NOT compute a new layout.** `outputs/connect_graph.json` already holds the navigable surface:
- **720 nodes** = his datasets, `{id, rows, domain, keys[], x, y}` — x/y are cached spring positions (from
  `connect/cache_layout.py`). These ARE the map.
- **20,696 edges** = how datasets connect, `{a, b, key, tier, via, hop, confidence, match_rate, sample[]}`.
  An edge means "these two datasets share a join key" (e.g. both carry NPI).
- Tiers (connection strength): STEEL 350 / STRONG 9,396 / GEO 5,633 / CORROBORATED 769 / BRIDGE 133 /
  PROBABILISTIC 4,415. 638 connected / **82 isolated** (datasets that connect to nothing — itself a finding).

⚠️ **Per-node attributes you need are NOT in the JSON — compute them once at build:** `degree`,
`max_tier` (strongest tier on any incident edge), `rows`, and the join keys it carries (`keys[]` is there).
Degree loop is in `explore.py`.

---

## THE DESIGN

The plane answers three questions at increasing zoom: **what do I have → how does it connect → tell me
everything about this one dataset.**

### Altitude ladder — one fixed coordinate space; the axis-range SPAN is the altimeter

⚠️ **The real bbox is x[-6.74, 7.82], y[-7.43, 5.47] → extent ≈ 14.5, NOT [-1,1].** Compute
`EXT = max(xspan, yspan)` at build and make **every breakpoint a fraction of EXT.** Hardcoded literals
dump you straight into the deepest level on load.

| Altitude | Span (frac of EXT≈14.5) | What you SEE | Labeled | Deeper |
|---|---|---|---|---|
| **0 · ORBIT** (the whole warehouse) | `> 0.55·EXT` (~8) | Only the **~80 hub datasets** (degree ≥ 50). The shape of the warehouse + where the mass is. Size=`14+6·log10(deg)`. | Top ~12 hubs ("CMS POS · 302 links") | Zoom in, or click a hub → fly to its neighborhood |
| **1 · REGION** (all the datasets) | `0.55 → 0.12·EXT` | All **638 connected datasets** fade in (Scattergl). The STEEL+STRONG **join-key backbone** lights up (9,746 edges). Islands sit in a gutter. | degree ≥ 25 (~top 30) | Click a dataset → tighten to its 1-hop neighborhood |
| **2 · STREET** (one dataset + its links) | `0.12 → 0.03·EXT` | In-viewport datasets + **all 6 tiers of edges, culled to viewport**, hover shows the join key. | every in-frame dataset (`_short()`) | Click a dataset → its **profile card** |
| **3 · CARD** (one dataset, full detail) | on click (NOT zoom-triggered) | A panel/board for ONE dataset: name, domain, **lifecycle (landed/modeled/empty/stub)**, row count, the **join keys it carries**, and **every dataset it connects to + on which key + at which tier.** | everything | Close → back to the map |

Felt experience: Orbit shows the **CMS gravity well** (POS_OTHER 302, HOSPITAL_GENERAL 279, HCRIS 252,
DIALYSIS 234) wired in gold to OIG_LEIE (230) — instantly "the health data is the dense core." Fly in →
638 datasets resolve, the hard-ID backbone appears → street level, hover an edge to see "joined on NPI" →
click NPPES → its card: *9.6M rows, modeled, carries NPI+CCN, connects to 21 datasets.* That's the loop.

### The core mechanism — fake semantic zoom with ONE relayout listener

Plotly has **no native semantic zoom.** A single `plotly_relayout` listener reads the live axis range,
buckets it into a band, and swaps level-of-detail via `Plotly.restyle`. **All four fixes are mandatory:**

```js
const EXT = 14.5;                                 // measured at build, injected
const ENTER = [0.55*EXT, 0.12*EXT, 0.03*EXT];
const EXIT  = [0.60*EXT, 0.14*EXT, 0.045*EXT];    // asymmetric → kills seam-flapping
let curBand = -1, t = null;
gd.on('plotly_relayout', (ev) => {
  if (ev['xaxis.autorange']) return runBand(0);    // reset path carries no range
  const x0 = ev['xaxis.range[0]'] ?? gd._fullLayout.xaxis.range[0];
  const x1 = ev['xaxis.range[1]'] ?? gd._fullLayout.xaxis.range[1];
  const b = bandFor(curBand, x1 - x0);             // hysteresis: enter/exit asymmetric
  if (b === curBand) return;                        // restyle ONLY on band change
  clearTimeout(t); t = setTimeout(() => { curBand = b; applyBand(b); }, 70);  // debounce
});
runBand(0);   // MUST run once on load — autorange leaves range undefined otherwise
```

### Trace architecture (stress-mandated)
- **Two node traces, not one:** `go.Scattergl` for marker dots (WebGL, needed for 638+ points) **+ a
  separate SVG `go.Scatter` text-only trace** (or `layout.annotations`) for labels. **NEVER
  `mode='markers+text'` on the Scattergl trace** — WebGL text is buggy/GPU-dependent.
- **Edges:** `go.Scatter` lines **pre-bucketed by tier** at build + **pre-indexed by node id**
  (`{nodeId:[edgeIdx]}`) so the Street viewport cull is O(visible nodes), not O(20,696) per relayout.

### The visual encoding — built to answer "what do I have, what's real, how connected"
Domain color is **dead today** (660/720 nodes are domain `"other"` until a backfill runs), so:
| Channel | Encodes | |
|---|---|---|
| **Color = trust tier** (`explore.TIER_STYLE`, gold=STEEL) | "how hard-joinable is this?" | the one honest encoding today; make `color_of(node)` a **swappable function** |
| **Size = degree** (`14+6·log10(deg)`), NOT rows | "is this a connective hub?" | rows-sizing = the 56px-blob hairball lesson |
| **Opacity / fill = is it REAL** | landed/modeled solid; empty/stub/sampled faded or hollow | ties straight to the trust-gate work — "see what's actually real at a glance" |

> The lifecycle channel needs `CATALOG.lifecycle` per source (landed/modeled/empty/stub). That's a **v1
> build-time enrichment** (one query) — keep **v0 graph-only/offline** (color by tier, opacity by rows).

### The dataset CARD (deepest level) — the payload
On clicking a dataset at Street level, show its profile. Source = `connect_graph.json` for connections +
(v1) one build-time `CATALOG` pull for the metadata. Fields:
- `source_id`, friendly name, `domain_primary`, **`lifecycle`**, **row count**, the **join keys it carries**.
- **Its connections:** for each neighbor — neighbor name, the join key they share, the tier, match rate.
- Render as a side panel (HTML div) or a small second Plotly figure (a mini hub-and-spoke of just this
  dataset + its direct neighbors, edges labeled by key). Either is fine; the side panel is simpler for v1.

### Wayfinding — how the map tells you where to go (all dataset-level, no people)
- **Filter by join key:** "show me every dataset carrying NPI / EIN / UEI / IMO / FIPS" → matching datasets
  light up, the rest dim. (This surfaces real findings: e.g. EIN-carriers are mostly islands.)
- **Filter by lifecycle / domain:** "show only what's real (landed+modeled)" / "show only the health cluster."
- **Search a dataset** → camera flies to its x/y (`Plotly.relayout` animating the axis range).
- **Islands gutter:** the 82 disconnected datasets parked in a labeled strip outside the bbox — seeing what
  *doesn't* connect is part of "what do I have."
- **Orientation:** corner minimap (2nd tiny Plotly div, viewport rectangle driven by the same listener).

---

## REUSE (import, don't rebuild)
| File | Becomes | Honesty |
|---|---|---|
| `connect/cache_layout.py` | the map surface — 638 cached x/y | verbatim; the x/y ARE the map |
| `connect/explore.py` | `TIER_STYLE`, `_short`, the invisible-midpoint **edge-hover trick**, the degree loop | import these; **node trace is NOT reusable** (it's SVG — write Scattergl fresh) |
| `outputs/connect_graph.json` | nodes (datasets) + edges (connections) | the whole map, already on disk |
| `LIBRARY_META.REGISTRY.CATALOG` | v1 card enrichment: `lifecycle`, `domain_primary`, `join_keys_std`, row count per `source_id` | one build-time query; keep v0 graph-only |
| `connect/__main__.py` | copy the `explore` subparser branch → a `plane` verb | pattern |

**New code is small:** one `connect/plane.py` (~150–200 lines) + the relayout JS block. **No `dossier.py`,
no `leads.py`, no server** — those belong to the deferred investigative layer.

---

## LANDMINES (read before coding — hard-won)
1. **bbox is ~14.5 wide, not [-1,1].** All zoom thresholds = fractions of measured `EXT`.
2. **WebGL text is buggy** → labels in a separate SVG trace, never `markers+text` on Scattergl.
3. **relayout handler:** debounce 70ms + asymmetric hysteresis + `runBand(0)` once on load (autorange
   carries no range in its payload).
4. **Domain color is a lie today** (660/720 = "other"). Color by **tier** (and lifecycle in v1); make
   `color_of(node)` swappable for a one-line flip when the domain backfill lands. Legend must tell the truth NOW.
5. **82 isolated datasets have no x/y.** Park them in a labeled gutter OUTSIDE the bbox, hidden at Orbit,
   shown at Region/Street. (Don't let them collapse to (0,0) and pile up.)
6. **Edges restyle is per-trace, not per-point.** Pre-bucket edges into per-tier traces at build; at Street,
   toggle tier visibility + viewport-cull via the node index.
7. **File size / offline:** vendor `plotly.min.js` locally (`include_plotlyjs='directory'`), trim edge
   `sample[]` arrays, round x/y to 5 decimals. Re-measure **< 4MB** before claiming "offline double-click."
8. **Keep v0 zero-Snowflake** — everything it needs is in `connect_graph.json`. The CATALOG enrichment
   (lifecycle/real-domain) is a v1 build-time pull, not a runtime dependency.

---

## PHASED BUILD

### v0 — "the warehouse zooms" (one session, ZERO Snowflake) ← start here
- **Files:** new `connect/plane.py`; 3-line subparser in `connect/__main__.py`.
- **Deliverable:** `outputs/plane.html` — opens at Orbit (~80 hub datasets), zoom in → Region (638 datasets
  fade in + the join-key backbone) → Street (all edges + hover showing the join key). Color by tier, size by
  degree, opacity by rows. Two clean LOD transitions, hover works, fully offline.
- **First step:** in `plane.py`, load `connect_graph.json`, compute `EXT = max(xspan, yspan)`, precompute
  per-node `[degree, max_tier, rows, keys]`.
- **Acceptance:** file < 4MB, two LOD transitions, `runBand(0)` on load, double-click works offline.
- **Then checkpoint with Chris.**

### v1 — "click a dataset = its full profile"
- Click a dataset at Street → side-panel card: lifecycle, row count, domain, join keys, and its connections
  (neighbor + shared key + tier). One build-time `CATALOG` pull enriches the metadata; color/opacity now
  reflect **lifecycle** (real vs empty/stub — the trust-gate made this honest).
- **Acceptance:** clicking NPPES shows "9.6M rows · modeled · NPI,CCN · connects to N datasets," and an
  empty/stub dataset (e.g. FJC_IDB) visibly reads as NOT real.

### v2 — "find anything, see the structure"
- Filter-by-join-key (NPI/EIN/UEI/IMO/FIPS), filter-by-lifecycle, filter-by-domain; dataset search box with
  fly-to; the islands gutter; the corner minimap.
- **Acceptance:** "show me everything carrying EIN" lights up the EIN-carriers and makes their island-ness
  visible.

### DEFERRED — the investigative layer (do NOT build yet; Chris is waiting on it)
Entity corkboards (one person + their records), lead hotspots, fly-to-a-named-person, the `/dossier` server
route. The hooks exist (`dossier.py`, `leads.py`, the 353 safety-gated leads) and can ride on top of this
plane later — but that's the "product" direction, intentionally out of scope here.

---

**In one breath:** Chris's whole warehouse as one fixed plane, four faked altitudes via a single relayout
listener, honest tier/degree/lifecycle encoding (so "what's real" reads at a glance), the deepest level a
**dataset's profile card** (not a person's corkboard). All static, offline, no server. v0 ships in a session
over data already on disk.
