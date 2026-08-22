
---

# Biggest Opportunities

The five places where the warehouse is closest to Ready but isn't yet — ranked
by *capability unlocked per unit of effort*, not by what should be built first.
That call isn't made here.

---

### 1. One small model turns every ZIP-to-ZIP flow into a drawable arc

**Currently:** 🟡 Flow maps · **Effort:** hours, one dbt model, no ingest

ZIP is the warehouse's dominant geography — in finished marts it beats real
coordinates roughly three to one. And the two pieces needed to put a ZIP on a
map are both already sitting in the core schema: a 46,960-row ZIP-to-county
crosswalk, and a 3,222-row county table carrying population-weighted centroid
coordinates as real numbers. ZIP → county → centroid is a two-hop join.

**The one step:** write `DIM_ZIP_POINT` — every ZIP joined to its dominant
county's centroid, with a tie-break for the ZIPs that straddle a county line.

**What it lights up:** the 178.6M-row opioid distributor-to-pharmacy flow and
the 3.08M-row disaster-displacement flow immediately, plus ZIP-grain rates,
ZIP-grain heat surfaces and ZIP-grain hotspot testing across the biggest tables
in the building — which today can be *counted* by ZIP and never *mapped* by it.
It is also the missing denominator under the single most-parked question in the
whole census grid ("per person served," parked 1,426 times).

**Optional day two:** derive true per-ZIP centroids by averaging the coordinates
on the ~12.9M already-geocoded, ZIP-stamped facility and bank-branch rows.
Finer, but facility-weighted rather than population-weighted, and full of holes
where no regulated site exists.

---

### 2. One copy-pasted date conversion makes the ripple animation real

**Currently:** 🟡 Ripples · **Effort:** hours, one cast in an existing model

The blocker was stated as "no edge anywhere carries a world clock," and half of
that is wrong. The corporate-ownership relationship table already carries three
properly typed date columns, rated high-confidence — so a crude dated ownership
animation runs *today*. What is still text is the pair of columns that say when
each ownership link switched on and off, and the exact conversion needed is
already written a few lines above them in the same model file.

**The one step:** apply the guarded date conversion already used in that model
to the relationship start and end columns — filtering to the right period type
first, because the five period slots are a flattened repeating group and slot
one does not mean the same thing on every row.

**What it lights up:** this is the only dated relationship source whose
identifier travels — it reaches 5.3M geocoded facilities through a pre-built
corporate crosswalk, the SEC filing family, and roughly 40M federal award rows.
It is the one edge set that can carry a ripple *out* of its own source.

**Watch out:** the clock index measures that period range as running from 1832 to
2035, so junk and future dates are in there and need filtering.

---

### 3. Registering one already-built bridge fuses the biggest island into the spine

**Currently:** 🟡 Connectome mapping · **Effort:** days — the cost is a spine
rebuild, not the SQL

The scoring said "build one crosswalk per island." One of those crosswalks is
already built and nothing referenced it: a 5.3-million-row table — exactly one
row per EPA-regulated facility — carrying the facility's registry id alongside a
matched corporate identifier, an ultimate-parent identifier, an SEC filer id and
a federal-contractor id. There is live proof the chain traverses end to end: a
findings view already joins facility violations to federal award dollars on the
corporate parent key.

**The one step:** register that crosswalk as an edge source in the spine's key
families, so the connection layer sees facility-to-corporate-parent as edges
instead of the join living only inside one hand-written view.

**What it lights up:** the whole corporate island — 3.4M legal entities, 484k
ownership edges, 5.3M facilities, ~40M federal award rows and the SEC family —
becomes one connected component you can run centrality *across* rather than
*inside*.

**Cost and honesty:** prior sessions measured a full spine rebuild at roughly
4.5 hours and $10–15 on the small warehouse, and flipping the registration flag
freezes incremental updates until that rebuild finishes. The crosswalk's own
columns mark it as a fuzzy name match, and what share of the 5.3M rows carry a
populated corporate identifier **cannot be read from metadata — check the fill
rate before trusting it.**

---

### 4. Flattening one array could grow the money-to-votes graph tenfold

**Currently:** ✅ Circulation overall, but the politics lane inside it is
effectively unwired · **Effort:** hours, one flatten and four re-pointed models

Prior sessions recorded that politics rides zero verified cross-family joins.
The identifier Rosetta stone that fixes it already exists and no technique
mentioned it: a 12,794-row member crosswalk carrying fifteen parallel identifier
systems side by side, plus a campaign-finance id array. The evidence it isn't
being used: the downstream money and voting tables hold between 1,050 and 1,715
rows each — about a tenth of the members the crosswalk covers.

**The one step:** flatten the campaign-finance id array into one row per member
per committee id, then re-point the four starved money tables at it.

**What it lights up:** wires 84.2M individual contributions to 945k roll-call
votes and 368k bill cosponsorships through a single bridge.

**Measure first:** how many of the 12,794 rows actually have that array
populated is **not readable from metadata**. If it's as thin as the table it
replaces, the ceiling doesn't move.

---

### 5. One public boundary download turns five techniques from dots into maps

**Currently:** 🟡 Sample or tier by zoom · **Effort:** one to two days —
a routine ingest plus a type conversion and a join test

Every rung of the zoom ladder is already there: 56 states, 3,222 counties,
85,391 tracts and a 46,960-row ZIP crosswalk, all keyed on the codes a boundary
file joins to, and counties and tracts even carry their own population. The only
missing piece is the shapes themselves — confirmed absent two ways: a full type
census of all 162,750 columns returns two geospatial columns (both the same
point column) and zero polygon columns, and a name sweep for every boundary-file
synonym returns two tiny site-specific tables and nothing national.

**The one step:** ingest the public Census cartographic boundary files for
state, county, tract and ZIP — roughly 89,000 polygon rows across all four rungs
— keyed on codes the core dimension tables already carry.

**What it lights up:** zoom tiering (its literal blocker), Voronoi's drawn cells,
choropleth for the aggregate-first family, and the map surface underneath mass,
kernel density, hotspot analysis and spatial autocorrelation. Five techniques
currently scored Ready are Ready *on the statistics* and degraded *on the
picture* purely because of this gap.

**Ranked last only because it is the single item on this entire map that needs a
file from outside the warehouse.** It has by far the widest blast radius.

---

# What the Laboratory doesn't have — and the warehouse does

A completeness pass went the other way: which shapes exist at real scale that
**no technique in the catalog claims**. These are capabilities sitting unused,
not gaps in the data.

### Seven technique families the catalog never lists

| family | why it belongs | substrate already measured |
|---|---|---|
| **Survival / time-to-event** (how long until something happens, and to whom) | The catalog has no duration technique at all. "How long does a water system stay in violation before anyone acts" is the mission's own question. | 56 span tables and 70 reporting-lag tables **already scored** on disk for censoring, backwards dates and cohort comparability. Biggest: 14.4M violation spans, 2.57M detention stints with real book-in and book-out times, 565k inspection-to-action lags. |
| **Group-disparity testing** (rate ratios between demographic groups, with a denominator per group) | The most direct possible answer to "who gets hurt, and does the data show it." Absent from all five sections. | 19.1M mortgage applications carrying race, ethnicity, sex, income, denial reason **and their own tract-level population and minority-population denominators on the same row**. Plus an existing 128,507-row disparity mart that already computes per-race rates, ratios and gaps. |
| **Text analytics** (topic maps, phrase shift over time, near-duplicate detection) | ~29 million rows of people describing what happened to them, and not one technique touches text. It is the closest thing in the warehouse to a human voice. | 17.2M consumer complaint narratives, 9.79M emergency-room injury narratives, 2.74M device adverse events, 1.15M rail casualties, 1.58M workplace incident descriptions, 274k mine accidents — every one already carrying a place and a clock. |
| **Changepoint detection** (when did this line break) | The catalog's only time technique is "what moves together." It has nothing for "when did it snap." | A prebuilt 1.16M-row table of source × clock × grain × day × row-count across 403 sources — the exact input, already assembled. |
| **Funnel plots / uncertainty-aware benchmarking** | The standard fix for the failure mode this mission most invites: naming a tiny facility "worst in America" because it had two bad months. | 6,103 hospitals × 107 measures; 44,429 facilities × 204 measures; 398,620 workplaces carrying hours-worked as a true exposure denominator. One county health table already ships a confidence interval. |
| **Sankey / alluvial / chord** (flow *without* geography) | Flow maps got downgraded purely for want of coordinates. A Sankey needs none — so every one of those flows is drawable today. | 178.6M shipments with business-activity tiers on both ends; 3.08M displacement moves with dollar amounts; 6.3M criminal cases with an origin and a transfer district (court districts have no geography anywhere, which kills the map and not the Sankey). |
| **Compositional / mix-shift** (what share each category holds, and which shares moved) | Entropy measures how *spread* a distribution is, never *which parts* moved. | 687 table-column mix rulings **already computed**, complete with snapshot-risk and survivorship-risk flags. |

### Six shapes nobody claimed

- **Denominators that aren't 2020 resident population.** Every technique reached
  for the same county population snapshot. Better ones exist: a county-by-year
  population with an age-adjusted death rate, hours-worked as a workplace
  exposure denominator, population-served on 434,040 water systems, and
  population density on the compliance table itself.
- **Industry as an axis.** 916 tables carry an industry classification code and
  no technique uses it — even though it is the natural peer group for "is this
  employer unusually bad compared with others doing the same work." Gap worth
  knowing: no lookup table anywhere decodes those codes or nests them up to
  sector, so the hierarchy has to be built or the inline description columns
  trusted.
- **The shape of money itself.** 656 numerically typed amount columns exist in
  the finished marts. Every technique uses them as a weight to add up; nothing
  looks at their *distribution* — digit tests, round-number bunching,
  just-under-a-threshold clustering, concentration curves. The July sweep found
  one of these by hand ("a tiny donor cluster generates a fifth of all rows at
  $23 each") with no technique behind it.
- **A 6.5-million-row labelled training set**, sitting unused: name-match pairs
  with a human-or-rule verdict and a score. Nothing in the catalog is
  supervised — and this is the substrate for a learned record-linkage model,
  which is the thing that would start dissolving the island problem two
  techniques call a blocker.
- **A full calendar dimension** — 155,593 rows carrying federal fiscal year,
  election cycle, congress number and weekend/month-end flags. Bolted onto the
  403 tables now on a shared clock, that is calendar-effect analysis for free:
  the September fiscal-year-end contract dump, money timed to election cycles,
  weekday-only reporting artifacts. No technique in the catalog names
  seasonality at all.
- **Bipartite two-mode structure.** 33.3M entities each carrying the list of
  source files they appear in. Two techniques dip into it; nobody claims the
  shape. Project it one way and you get an honest map of which sources really
  describe the same population — the version the 0.1%-sampled schema graph only
  gestures at. Project it the other way and you get a visibility-anomaly
  detector: which things show up in an unusual combination of files. Neither
  projection needs anything built or ingested.

---

# Caveats

Stated once, at the end, where they belong for an exploratory pass.

- **Metadata cannot see contents.** A numeric coordinate column can still be
  mostly null; a hard-identifier column can still be sentinel-masked, which has
  bitten this platform twice. Nothing here was value-checked.
- **Documented defects still stand** where cited: a destroyed workplace-inspection
  table, three-quarters of a 62M-row drug-safety corpus column-shifted, an
  environmental penalty column stamping one settlement onto hundreds of
  facilities, a federal debarment list under 9% loaded with fabricated status
  flags, and 18 tables whose suspiciously round row counts are confirmed load
  caps.
- **The trend sweep's warning applies to every time-based technique here:** most
  of the movement in this warehouse is about how the data was *collected*, not
  what happened in the world. Anything built on a changing line needs its
  denominator settled first.
- **Row counts are Snowflake's own metadata** and are exact for base tables and
  absent for views.

---

*Evidence: `reports/lab_map/` — the full metadata dump, the shape index, the
per-signal candidate lists, and the verified-facts file every number here was
checked against.*
