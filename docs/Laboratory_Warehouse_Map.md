# The Laboratory ↔ Warehouse Map

*What every visualization technique in `docs/The_Laboratory.md` would need, what
the warehouse actually holds, and how far each one is from being tryable today.*

**Built 2026-08-22. Metadata only — `INFORMATION_SCHEMA` across all five
databases, plus the wiring tables in LIBRARY_META and the audit reports already
on disk. Zero data SELECTs, zero profiling queries, zero sampling.**

This is a menu, not a plan. It deliberately does **not** say what to build
first.

---

## The one-screen picture

**23 techniques scored. 18 ready to try today, 5 partial, none dead.**

But that headline is misleading on its own, and the three sentences under it are
the actual finding:

1. **The warehouse is 91.6% text strings.** 149,003 of 162,750 columns are TEXT.
   Only 122 tables store map coordinates as real numbers even though 801 have
   columns named for them; 322 of 948 money tables have a real numeric amount;
   1,058 of 3,517 date-ish tables have a real typed date. Every technique that
   needs a number is really a technique that needs a cast first. **The cheapest
   unlock in this warehouse is almost always "add a guarded cast to a dbt model
   that already exists" — the canonical clock did exactly that for time, for 403
   tables, last week.**

2. **Nothing in the warehouse knows the shape of a county.** Exactly 2 of
   162,750 columns are a real geospatial type, and both are the same ship-position
   point column. Zero polygon columns exist anywhere. Five of the geographic
   techniques are scored Ready because the *statistics* work off centroids — but
   their *drawn output* is dots and heat surfaces, never a filled-in map. One
   public boundary-file download fixes all five at once, and it is the only item
   on the whole map that needs something from outside.

3. **The best connection maps in the building are not in the connection layer.**
   The official map holds 4,910 table-to-table links, of which roughly a
   quarter are hard-identifier matches and the rest are name-and-address
   guesses. Meanwhile several source tables carry clean, hard-identifier,
   directed, *dated* edge lists on their own — opioid shipments (178.6M),
   offshore-leaks relationships (3.3M), doctor-to-facility affiliation (2.3M),
   corporate ownership with switch-on and switch-off dates (484k). Three
   separate techniques were scored on the assumption that the graph lives in the
   connection layer; it mostly does not.

> **The single widest constraint:** value is present, type is wrong. The single
> widest *unlock* is one boundary-file ingest. Everything else on this map is a
> cast or a join over tables that already exist.

---

## How to read a technique entry

- **Needs** — the shape of data the technique requires, in plain words.
- **What exists** — what was actually found, with counts and named tables.
- **Readiness** — ✅ Ready · 🟡 Partial · 🔴 Needs new data · 🛠️ Needs cleanup.
- **The gap / Distance to ready** — for anything not Ready, the exact named
  blocker and the single step that would clear it.
- **Candidate tables** — the 1–3 strongest places to prototype against.
- The line in a **blockquote** at the end of each entry is the one thing worth
  remembering about it.

Every table named in this document was checked against the live metadata dump
this session. Backup, restore and retired schemas were excluded by rule.

---

## Method, and what it cannot tell you

Each of the five Laboratory categories was scored by one pass, then handed to a
second pass told to **refute** it — check that every cited table exists with
those exact columns and row counts, hunt for tier inflation, hunt for tier
deflation, and catch anywhere a column *name* had been trusted as proof of a
column's *contents*. Two more passes then swept the finished set for
contradictions, oversold claims and warehouse shapes that no technique had
claimed. Four tier calls changed as a result and every change is shown in place.

**The hard limit of a metadata-only sweep:** a column name and a data type tell
you the shape, never the contents. A numeric latitude column can still be 40%
null. A hard-identifier column can still be sentinel-masked — that exact trap
has bitten this platform twice. Nothing in this document has been value-checked,
and several entries say so explicitly where it matters most.

---

## Corrections this sweep made to things already written down

Four claims that were on the record turned out to be wrong, and they are
corrected here rather than left to be rediscovered.

| what was written | what is actually true |
|---|---|
| The Laboratory: "~12.88M entities across the 31 spine tables" | The resolved-entity tables hold **33,312,349**; the index and node tables hold **84,382,504**. The number is roughly a quarter of current scale. |
| Two scoring passes disagreed on whether a polygon layer exists | It does not. The one column *named* geometry is typed TEXT. A full type census returns 2 geospatial columns warehouse-wide, both the same point column, and zero polygon columns. |
| "Nothing in the warehouse can place a ZIP on a map," used to block flow maps | ZIP → county → population-weighted centroid is a two-hop join over two tables that both exist today. Flows are drawable at county resolution with no new data at all. |
| Two techniques were caveated on county/FIPS columns being broken by a bad numeric cast | That defect was **repaired on 2026-08-10** — the repair note says so in the same words, and the live metadata agrees the columns are TEXT today, leading zeros intact. The warning was stale. |

One more, in the other direction: a mid-sweep claim that the opioid shipment
table's county and date columns were bad casts turned out to have been read off
the **backup copy** of that table, not the live one. The live table's date column
is rated the cleanest big event clock in its batch.

---

## Summary table

Sorted so everything ready to try today is visible at a glance.

| # | Technique | Category | Tier | The one-line reason |
|---|---|---|---|---|
| 1 | Hotspot analysis (Getis-Ord Gi*) | GIS | ✅ Ready | county and tract centroids plus population give both the neighbour rule and the rate denominator |
| 2 | Kernel Density Estimation (KDE) | GIS | ✅ Ready | the only technique here that needs nothing built first — check row grain before plotting |
| 3 | Spatial autocorrelation (Moran's I) | GIS | ✅ Ready | distance-band weights from existing centroids; the shuffle-test code is already running elsewhere |
| 4 | Voronoi diagrams | GIS | ✅ Ready | not the dud the catalog assumes — bank branches and water systems genuinely own their ground |
| 5 | Aggregate first (histograms/heatmaps/hexbins) | Scatter readability | ✅ Ready | 252 tables over 1M rows with real groupers and real numeric measures; 14 rollups already exist |
| 6 | Encode density not position | Scatter readability | ✅ Ready | 122 tables have genuinely numeric coordinates; the biggest is 58.1M points |
| 7 | Dimension reduction (PCA/t-SNE) | Scatter readability | ✅ Ready | 10 tables carry a 20+ measure vector on 50k+ rows — but watch the exact duplicate twin |
| 8 | Epidemiology → contact tracing graphs | Raided | ✅ Ready | one table already IS contact tracing — 2.57M person-stints with book-in and book-out times |
| 9 | Astronomy → sky surveys / N-body clustering | Raided | ✅ Ready | 58M-point cloud is real, but it is one week of pings — a photograph, not a survey |
| 10 | Ecology → food web / trophic cascade | Raided | ✅ Ready | directed multi-hop chains exist in one ID namespace — shipments, ownership, mine controllers |
| 11 | Music/Audio → spectrograms | Raided | ✅ Ready | one pharmacy, drugs down the side, 84 months across the bottom — straight out of one table |
| 12 | Finance → correlation matrices / heatmap clustering | Raided | ✅ Ready | 403 sources already counted per day on one shared axis; the matrix input is prebuilt |
| 13 | Topological Data Analysis (TDA) | Physics | ✅ Ready | dense numeric point clouds exist; the distance rule is arithmetic you write, not a table you need |
| 14 | Network centrality | Physics | ✅ Ready | real entity-to-entity edge lists exist, and degree is already computed for 33.3M entities |
| 15 | Entropy / information density | Physics | ✅ Ready | 403 tables now share one clock column, so one query shape runs warehouse-wide |
| 16 | Mass (density/heatmaps/bubble/contour) | Organism | ✅ Ready | coordinates, place codes and 2020 population denominators all present at county and tract |
| 17 | Distance (clustering, dimension reduction over join-key relatedness) | Organism | ✅ Ready | cluster on the source registry's own feature columns, not on the 0.1%-sampled edge map |
| 18 | Circulation (network / force-directed graphs) | Organism | ✅ Ready | several real edge lists — but the two biggest are sealed islands with no way out |
| 19 | Flow maps | GIS | 🟡 Partial | drawable today at county resolution; ZIP resolution needs one small model, no new data |
| 20 | Sample or tier by zoom | Scatter readability | 🟡 Partial | every rung of the ladder exists, but no boundary shape exists, so zoom gives bigger dots not filled areas |
| 21 | Neuroscience → connectome mapping | Raided | 🟡 Partial | runs inside the opioid network today; cannot run across the warehouse, the islands don't touch |
| 22 | Percolation theory | Physics | 🟡 Partial | valid on the opioid shipment network; on the connection map it would measure the sampler |
| 23 | Ripples (diffusion/propagation animation) | Organism | 🟡 Partial | no spine edge carries a world clock; the dated graphs that exist are mostly sealed |

**18 ready · 5 partial · 0 needing new data · 0 needing cleanup.** Nothing in The Laboratory is dead against this warehouse.

---

## Making Massive Scatter Plots Readable

### Aggregate first (histograms/heatmaps/hexbins)

**Readiness:** ✅ **Ready**

**Needs.** A table big enough that drawing every row breaks a browser, plus something to group rows by (a place, a category, or a date bucket) and something to count or add up inside each group. No coordinates needed for the histogram/heatmap version.

**What exists.** Verified: 252 objects carry 1M+ rows and 79 carry 10M+. The flagship LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS really does hold 178,598,026 rows, and I read all 33 of its columns (the first pass said 31): QUANTITY, DOSAGE_UNITS, BASE_WEIGHT_GRAMS and TOTAL_MME are all typed FLOAT, TRANSACTION_DATE is a real DATE, and BUYER_COUNTY/CITY/STATE/ZIP are there to group on. FINANCE__FED_FEC_INDIV_CONTRIBUTIONS is 84,172,112 rows with TRANSACTION_AMT as FLOAT, ZIP_CODE/CITY/STATE, and a typed TRANSACTION_DATE. The rollup habit already exists: LIBRARY_MARTS.PUBLIC holds exactly 14 hand-made aggregate tables. The first pass said all 14 stop at the state line — two of them are not state rollups at all (one is by manufacturer and payment nature, one by agency and NAICS). The true and stronger statement, which I checked column-by-column: not one of the 14 carries a county, zip, tract, FIPS, or lat/lon column, so none goes below state. For a genuine map hexbin, MARITIME__FED_NOAA_AIS gives 58,104,610 rows with LATITUDE/LONGITUDE typed FLOAT. Rate denominators are real: LIBRARY_MARTS.CORE.DIM_COUNTY (3,222 rows) and DIM_TRACT (85,391) both carry POPULATION_2020. One correction that matters for rates: ARCOS carries no FIPS code anywhere in its 33 columns, so a per-person county rate on the flagship is a county-NAME match. If you want a code-clean county join at scale, HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY has 31,403,215 rows and a real FIPS_COUNTY_CODE.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. BUYER_COUNTY/CITY/STATE/ZIP to group by, TOTAL_MME and DOSAGE_UNITS typed FLOAT to sum, TRANSACTION_DATE a real DATE for time buckets — all confirmed in the column list
- `LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS` — 58,104,610 rows. LATITUDE and LONGITUDE typed FLOAT plus the warehouse's only real GEOGRAPHY column, so a map hexbin needs no join
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY` — 31,403,215 rows. 31.4M rows with a real FIPS_COUNTY_CODE — the biggest fact table that joins to the county rung by code instead of by name

> The rollups already exist — 14 of them — and every single one is blind below the state line.

### Encode density not position

**Readiness:** ✅ **Ready**

**Needs.** Lots of records piling onto the same or nearly the same spot, so you colour the spot by how many landed there instead of drawing a dot per record. Needs a real coordinate pair (or any two real number columns) on a table big enough to overplot.

**What exists.** 801 objects carry both a latitude-ish and a longitude-ish column name; 799 of those sit outside the backup schemas, and 24 (not the 23 claimed) have 1M+ rows. But the first pass leaned on the name match and then hung the caveat on the wrong hook. The real caveat, measured: of those 801 tables, only 122 have a latitude column with a numeric dtype — 686 store latitude as TEXT. The documented 'nan'-string corruption lives in those TEXT columns, not in the numeric ones, so the tables worth using are the small numeric-typed set, and every table I recommend is in it. MARITIME__FED_NOAA_AIS at 58,104,610 rows has LATITUDE/LONGITUDE as FLOAT plus POSITION_GEOGRAPHY typed GEOGRAPHY — and I confirmed that is one of exactly two GEOGRAPHY/GEOMETRY columns in all 162,750 columns (the other is the same column on its TIMELINE view). Behind it, twelve non-backup mart tables above 500k rows have a numerically typed latitude, more than the three offered: FRACFOCUS 7,200,550; USGS_WATER 6,694,816; EPA_FRS_FACILITIES 5,300,149 (which also carries a real FIPS_CODE); EPA_FRS_FRS_FACILITIES 3,277,557; EPA_ECHO 3,135,554; FDIC_SOD_BRANCH_DEPOSITS 2,823,000; NOAA_STORM_EVENTS 1,780,730; EPA_RCRA_FACILITIES 1,613,224; EPA_NPDES_ICIS_FACILITIES 1,213,737; FRA_CASUALTIES 1,150,788. The non-map version (density across two measure axes) is served by HEALTH__FED_CMS_MEDICARE_PROVIDER, 1,296,739 rows and 49 numeric columns of which 48 are genuine measures.

**Candidate tables.**

- `LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS` — 58,104,610 rows. 58.1M position pings, LATITUDE/LONGITUDE typed FLOAT, plus the warehouse's only real GEOGRAPHY column so Snowflake bins server-side
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` — 5,300,149 rows. 5.3M regulated facilities, LATITUDE/LONGITUDE both FLOAT, and a real FIPS_CODE plus POSTAL_CODE so the density surface can also roll up by county
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER` — 6,694,816 rows. 6.7M water records with LATITUDE typed FLOAT — a second big numerically-typed coordinate table the first pass missed

> Eight hundred tables look like they have coordinates; only 122 store latitude as an actual number — the rest are text, and that is where the 'nan' corruption lives.

### Dimension reduction (PCA/t-SNE)

**Readiness:** ✅ **Ready**

**Needs.** One row equals one thing, with many real number columns sitting side by side on that same row — twenty-plus measurements per subject. Counts and dollars and percentages, not ID numbers that merely happen to be digits.

**What exists.** The bleak headline numbers all check out: of 4,847 objects, 3,076 (63%) have zero numeric columns, only 261 have 8+, 81 have 20+, and 30 have 50+ (29 outside the backup schemas). Among the 252 tables with 1M+ rows, zero have 50+ numeric and 110 have none at all. But the first pass said 'exactly one table is both wide and big' and called the technique PARTIAL on that basis, and that claim is false. Ten non-backup base tables carry 20+ numeric columns on 50,000+ rows, and three of them are large with genuine measure vectors I read column by column: HEALTH__FED_CMS_MEDICARE_PROVIDER (1,296,739 rows, 49 numeric, 48 real — payments, beneficiary age and race counts, ~35 chronic-condition percentages, one row per provider); HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE (503,917 rows, 62 numeric); and HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER (381,228 rows, 52 numeric — I read all of them and 51 are real measures, same payment/age/race/condition family). Below those: IMMIGRATION__FED_DOL_OFLC 664,616 rows and 22 numeric, JUSTICE__FED_SCDB 83,644 and 47, HEALTH__FED_CMS_POS_OTHER 44,429 and 204. That is a menu, not a single table. Two caveats I verified rather than assumed. First, the duplicate twin is real and exact: HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER has the same 1,296,739 rows and the same 81 column names except NPI where the other says RNDRNG_NPI — though it was created three seconds EARLIER, not later as claimed. Pick one or you double every point. Second, the 62 numeric columns on the quality-payment table are roughly half positional MEASURE_ID_1..28 slots rather than measures, so its usable vector is nearer 30. FEMA IA housing registrations does carry 31 real measure columns on 3,080,000 rows, but that count is a suspiciously round number against a 21,730,000-row raw table — about 14% of source.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER` — 1,296,739 rows. 49 numeric columns verified as real measures — payments, beneficiary age and race counts, ~35 chronic-condition percentages — one row per provider
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER` — 381,228 rows. 381k rows and 52 numeric columns, 51 of them genuine measures — a second big-and-wide table the first pass missed entirely
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE` — 503,917 rows. 503,917 rows with 62 numeric columns, though about half are positional MEASURE_ID slots so the usable vector is nearer 30

> Raised from Partial on review: ten tables carry a 20-plus measure vector on 50,000-plus rows, and three of them are large — but the top one has an exact duplicate twin, so pick a side before you reduce or you double every point.

### Sample or tier by zoom

**Readiness:** 🟡 **Partial**

**Needs.** A nesting ladder — state to county to tract to individual point — so the wide view draws a few thousand shapes and only fetches the millions of underlying records when someone zooms in. Each rung needs a place to draw and a number to show.

**What exists.** The ladder is real and I confirmed every rung: LIBRARY_MARTS.CORE holds DIM_STATE (56 rows), DIM_COUNTY (3,222), DIM_TRACT (85,391) and XWALK_ZCTA_COUNTY (46,960) bridging ZIP to county. DIM_COUNTY and DIM_TRACT both carry POP_CENTER_LAT, POP_CENTER_LON and POPULATION_2020, so those two rungs have a dot to draw and a per-person denominator. One correction: DIM_STATE has neither — no population, no centroid, just FIPS, USPS, name and a territory flag — so the top rung's denominator has to be summed up from counties. The time-zoom ladder is genuinely built: LIBRARY_MARTS.TIMELINE holds exactly 436 views, including ones over ARCOS, FEC individual contributions, NOAA AIS, EPA ECHO, FEMA housing and all four HMDA tables. The tract rung is where the first pass went wrong twice. It said only 90 tables carry a tract or block-group column; I measure 136 non-backup objects with a tract, GEOID or block-group column name. And it named HMDA_LAR as a main tract source — that table holds 17,474 rows, and HOUSING__FED_CFPB_HMDA and _DC_ONLY hold 28,301 each. They are stubs. The one substantial national tract-level table is HOUSING__FED_CFPB_HMDA_HISTORIC at 19,136,434 rows, and it carries STATE_CODE, COUNTY_CODE and CENSUS_TRACT_NUMBER — a complete code-keyed ladder on one table. FEMA IA housing registrations adds CENSUS_GEOID on 3,080,000 rows. The boundary gap the first pass flagged is real and I re-measured it: of 2,346 columns whose names look geometric, 2,331 are dtype TEXT and exactly two are real GEOGRAPHY (both the same NOAA AIS column). Every table with a GEOMETRY, SHAPE_WKT or THE_GEOM column is a city ArcGIS portal pull sitting in LIBRARY_RAW.LANDING — Harris County and its peers — not a national boundary file.

**The gap.** There is no boundary-shape table anywhere in the warehouse, and the technique silently needs one. Exactly two columns out of 162,750 carry a real GEOGRAPHY type and both are the same ship-position point column; the 1,212 tables the geometry signal flagged are name-only TEXT leftovers from city portal crawls, with no national state, county, tract or ZCTA polygon among them. So a zoom that fills in areas has nothing to fill — you get sized dots on centroids. Second, smaller gap: the biggest fact table, ARCOS, has no FIPS code in any of its 33 columns, so tiering it to the county rung is a county-NAME match rather than a code match.

**Distance to ready.** Pull one boundary source — Census TIGER state, county, tract and ZCTA polygons — keyed on the FIPS codes DIM_STATE, DIM_COUNTY and DIM_TRACT already carry. That single ingest lights all four rungs at once; everything else is already sitting in LIBRARY_MARTS.CORE.

**Candidate tables.**

- `LIBRARY_MARTS.CORE.DIM_COUNTY` — 3,222 rows. the middle rung — COUNTY_FIPS and STATE_FIPS keys, POP_CENTER_LAT/LON to draw on, POPULATION_2020 as a ready-made rate denominator
- `LIBRARY_MARTS.CORE.DIM_TRACT` — 85,391 rows. the fine rung — TRACT_GEOID nesting up through COUNTY_FIPS and STATE_FIPS, with its own centroid and 2020 population
- `LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC` — 19,136,434 rows. the only large national table carrying the whole ladder by code on one row — STATE_CODE, COUNTY_CODE and CENSUS_TRACT_NUMBER across 19.1M loan records; the HMDA tables the first pass named insteadd hold 17k-28k rows

> Every rung of the zoom ladder exists and county and tract even carry population — but nothing in this warehouse knows the shape of a county, so zoom gives you bigger dots, never filled-in areas.

---

## The Organism Metaphor (Mass / Distance / Circulation / Ripples)

### Mass (density/heatmaps/bubble/contour)

**Readiness:** ✅ **Ready**

**Needs.** Something to count, and somewhere to put it — either a real coordinate pair, or a place code (ZIP, county, state, census tract) you can pin to a map. Plus a population number underneath so you can show a rate per person instead of a raw pile that just tracks where people live.

**What exists.** Real supply, but the headline counts were inflated about 8x and I am cutting them. The 801 lat+lon tables, 1,303 ZIP, 768 county and 1,583 state are counts of OBJECTS, and the same source is counted three times as it flows raw to staging to finished. Deduped to the finished mart layer it is 91 point-geo tables, 279 with a ZIP, 174 with a county, 80 pairing place with a clock and 27 pairing place with a harm column. Quality is also thinner than the count suggests: of 805 tables carrying a latitude, 683 store it as text, not a number. The big finished point-geo tables are real and clean though — MARITIME__FED_NOAA_AIS (58,104,610), ENVIRONMENT__FED_FRACFOCUS_REGISTRY (7,200,550), ENVIRONMENT__FED_EPA_FRS_FACILITIES (5,300,149, latitude and longitude both FLOAT), ENVIRONMENT__FED_EPA_ECHO (3,135,554). Denominators exist at county and tract only: LIBRARY_MARTS.CORE.DIM_COUNTY (3,222, POPULATION_2020 + POP_CENTER_LAT/LON), DIM_TRACT (85,391, same shape), DIM_STATE (56). Confirming the first pass's correction of The Laboratory's stale number: the doc says '~12.88M entities across 31 spine tables'; ENTITY_GOLDEN and ENTITY_MAP each hold 33,312,349 and ENTITY_INDEX and CONNECT_NODES each hold 84,382,504.

**Candidate tables.**

- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` — 5,300,149 rows. REGISTRY_ID plus numeric LATITUDE/LONGITUDE plus COUNTY, FIPS_CODE, STATE_CODE and POSTAL_CODE — the widest clean census of regulated sites
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO` — 3,135,554 rows. lat/lon, inspection and penalty dates, and compliance flags on one row — but its money column is the documented phantom-fines defect, so map counts, not dollars
- `LIBRARY_MARTS.CORE.DIM_COUNTY` — 3,222 rows. POPULATION_2020 plus population-weighted centroid lat/lon, the denominator that turns a pile into a rate

> The denominator stops at county and tract — no table anywhere carries population by ZIP, and XWALK_ZCTA_COUNTY (46,960 rows) has no population column, so the warehouse's single most common geography cannot be turned into a per-person rate without a many-to-many ZIP-to-county allocation you would have to build.

### Distance (clustering, dimension reduction over join-key relatedness)

**Readiness:** ✅ **Ready**

**Needs.** A number saying how close any two things are — either a measured overlap score between a pair of tables, or a row of features per source you can cluster on. Then something to squash it into two dimensions so it can be looked at.

**What exists.** Both routes named in the needs exist, so I am raising this from PARTIAL to READY. The feature route is complete: LIBRARY_META.REGISTRY.SOURCE_REGISTRY holds 2,778 rows with five ARRAY columns (DOMAIN_SECONDARY, ENTITY_TYPES, JOIN_KEYS_STD, THEMES, NATURAL_KEY) plus GRAIN, SPINE_ENTITY, JOIN_KEY_TIER, HAS_EVENTS, SOURCE_ROLE and DOMAIN_PRIMARY — every column verified present. That is a full feature matrix you can cluster and project today with nothing new built. The measured-overlap route also exists: LIBRARY_META.CONNECT.CONNECT_EDGES (4,910 rows) carries A, B, KEY, TIER, MATCHED, A_DISTINCT, B_DISTINCT, MATCH_RATE and CONFIDENCE — all verified. ENTITY_MAP (33,312,349) carries MEMBER_TABLES(ARRAY) and SOURCE_COUNT. The previous analyst called this PARTIAL because SOURCE_OVERLAP_MATRIX is 36 rows, DOMAIN_OVERLAP_MATRIX 7, CLUSTER_ASSIGNMENTS 23 and BRIDGE_ENTITIES 0 — I confirmed all four counts, but those are pre-chewed answer tables, not inputs the technique requires. Having to run the clustering yourself is not a missing-data blocker.

**Candidate tables.**

- `LIBRARY_META.REGISTRY.SOURCE_REGISTRY` — 2,778 rows. five ARRAY feature columns plus GRAIN, SPINE_ENTITY, JOIN_KEY_TIER and HAS_EVENTS give every source a vector, no join needed
- `LIBRARY_META.CONNECT.CONNECT_EDGES` — 4,910 rows. MATCH_RATE and CONFIDENCE banded by TIER on measured table pairs is a ready-made similarity score
- `LIBRARY_META.CONNECT.ENTITY_MAP` — 33,312,349 rows. MEMBER_TABLES plus SOURCE_COUNT is entity-level co-occurrence, the finest-grain relatedness available

> Cluster off the registry's feature columns, not off CONNECT_EDGES: 4,910 measured pairs is a sliver of the possible pairs, and a missing pair there means 'never measured,' not 'no overlap' — treating missing as zero would make the warehouse look far more disconnected than it is.

### Circulation (network / force-directed graphs)

**Readiness:** ✅ **Ready**

**Needs.** An edge list: two named endpoints on every row, ideally with a label saying what the link is and a weight saying how strong. Plus a node list so the dots have names.

**What exists.** Confirmed READY, and every column claim checked out. Two different graphs live here. The warehouse-wiring graph is CONNECT_EDGES (4,910 rows, A and B hold table names) with MATCH_PAIRS (181,002,484) underneath and ENTITY_INDEX (84,382,504) as a node list, not an edge list. The real-world graphs sit in the marts: HEALTH__FED_DEA_ARCOS (178,598,026) has REPORTER_DEA_NO to BUYER_DEA_NO with QUANTITY, TOTAL_MME and a DATE-typed TRANSACTION_DATE, plus reporter and buyer names inline. ICIJ OFFSHORELEAKS_RELATIONSHIPS (3,339,267) has NODE_ID_START, NODE_ID_END and REL_TYPE — and there are FIVE matching node tables, not four as previously stated: ENTITIES 814,344, OFFICERS 771,315, ADDRESSES 402,246, INTERMEDIARIES 26,768 and OTHERS 2,989, so leaving OTHERS out orphans edges. UK_COMPANIES_HOUSE_PSC (7,000,000) links COMPANY_NUMBER to a named person with NATURES_OF_CONTROL. ECONOMICS__INTL_GLEIF_RELATIONSHIPS (484,142) is parent/child ownership against a 3,382,301-row LEI entity table. HEALTH__FED_CMS_FACILITY_AFFILIATION (2,260,193) has NPI and CCN. On the spine side ENTITY_XREF (2,672,384) is the one genuine key-to-key crosswalk, with RELATION and FANOUT.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. REPORTER_DEA_NO to BUYER_DEA_NO with quantity, opioid dose weight and a real date — the biggest directed weighted dated flow network in the building
- `LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS` — 3,339,267 rows. start/end node ids plus a relation type, with five node tables supplying names, addresses and jurisdictions
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS` — 484,142 rows. the only relationship graph whose node identifier reaches outside its own source — LEI also appears in nine other mart tables across four domains
- `LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK` — 12,794 rows. found by the completeness critic — the identifier Rosetta stone for the one domain prior sessions recorded as having zero verified cross-family joins. Carries fifteen parallel member identifiers plus a campaign-finance id array. The tables that should consume it are starved at roughly a tenth of its coverage.

> The two biggest graphs are sealed islands: I checked every mart column and REPORTER_DEA_NO / BUYER_DEA_NO exist nowhere except ARCOS, ICIJ's NODE_ID nowhere except the ICIJ tables, and COMPANY_NUMBER nowhere except the two UK tables — so ARCOS and ICIJ draw beautiful pictures that cannot be linked to anything else, while the much smaller GLEIF graph is the only one that can.

### Ripples (diffusion/propagation animation)

**Readiness:** 🟡 **Partial**

**Needs.** Edges plus a clock on the edges. You have to know when each link switched on or fired, or at least have an ordered sequence, or nothing can move and there is nothing to animate.

**What exists.** Dated edges exist inside single sources and nowhere across them. ARCOS (178,598,026) has a DATE-typed TRANSACTION_DATE with weights — fully animatable today within itself. ICIJ RELATIONSHIPS (3,339,267) has START_DATE and END_DATE as real DATE columns on the edges. Companies House PSC has NOTIFIED_ON and CEASED_ON as real DATE columns, but its row count is exactly 7,000,000 — a hard round number matching the documented load-cap defect pattern, and its sibling UK company table sits at an unrounded 5,734,780, so the PSC edge set is almost certainly truncated. GLEIF RELATIONSHIPS carries five period start/end pairs but all ten are TEXT, the exact cast that has produced epoch-date corruption in this warehouse. Every spine edge table is clockless in the way that matters: CONNECT_EDGES, CONNECT_EDGES_INC, MATCH_PAIRS, ENTITY_XREF, ENTITY_MAP, ENTITY_GOLDEN and CONNECT_NODES carry only BUILT_AT and RUN_ID, and ENTITY_LINKS only CREATED_AT. The TIMELINE layer is real — 436 views, 403 carrying RIPPLE_TS, and all four relationship sources have one — but I confirmed exactly 66 of the 436 carry a hard entity id (EIN, NPI, CIK, CCN, UEI, LEI, DUNS or COMPANY_NUMBER), so the canonical clock cannot be joined onto most of the graph.

**The gap.** Two things, not one. First, no spine edge table has a world clock — CONNECT_EDGES, MATCH_PAIRS, ENTITY_XREF and ENTITY_MAP carry only BUILT_AT and RUN_ID, a pipeline timestamp. Second, and more binding: the three source graphs that DO have dated edges are sealed — ARCOS's DEA numbers, ICIJ's NODE_IDs and Companies House's COMPANY_NUMBERs appear in no other mart table in the warehouse, so a ripple can be animated inside one source and has nowhere to propagate to.

**Distance to ready.** Cast GLEIF RELATIONSHIPS' five TEXT period start/end pairs to real dates. GLEIF is the only dated relationship source whose node identifier (LEI) also appears in nine other mart tables across finance, housing and environment, so this is the one edge set that could actually carry a ripple out of its own source. The fix suggested on the first pass — copying RIPPLE_TS into ENTITY_XREF and MATCH_PAIRS — does not work: those rows are key-value matches, and one key value appears on many source rows with many different dates, so there is no single timestamp to copy.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. dated, weighted, directed shipments — propagation works today, but only inside this one source
- `LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS` — 3,339,267 rows. START_DATE and END_DATE as real DATE columns sitting directly on 3.3M edges
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS` — 484,142 rows. dated ownership links on an identifier nine other mart tables also carry — small, but the only one that can cross a source boundary
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK` — 5,300,149 rows. found by the completeness critic — a pre-built bridge from the corporate-identifier namespace onto 5.3M geocoded, FIPS-stamped facilities, and onward to the SEC family and to 40M federal award rows. It breaks the "nowhere to propagate to" half of the blocker. Marked as a fuzzy name match by its own confidence and review columns — check the fill rate before trusting it.

> Do not build on Companies House PSC without checking it first — it sits at exactly 7,000,000 rows in both raw and mart, the same round-number signature as the 5,000-row subawards stub, so the ownership timeline you would animate is probably a truncated slice of the real one.

---

## Physics-Derived Techniques

### Topological Data Analysis (TDA)

**Readiness:** ✅ **Ready**

**Needs.** A pile of points where every point is one real thing — a hospital, a plant, a water system — and each point carries a bunch of comparable numbers as its coordinates. The math then hunts for loops, holes and clumps in that pile that ordinary averages never show. The 'how far apart are two points' rule is arithmetic you write at run time, not a column you have to find.

**What exists.** Every number the original scoring gave checks out exactly. The warehouse is overwhelmingly text: of 162,750 columns, 149,003 are TEXT against 7,558 NUMBER and 2,064 FLOAT. Filtering the 20-plus-numeric-column list to real base tables outside the backup/restore schemas gives exactly 34 tables; 13 of those have 50 or more numeric columns; 9 of the 34 also carry 100k or more rows. The named clouds are real and the row and column counts are exact: HCRIS 6,103 rows by 107 numeric of 125 columns, POS_OTHER 44,429 by 204 of 473, QUALITY_PAYMENT_PROGRAM_EXPERIENCE 503,917 by 62 of 212, MEDICARE_PROVIDER 1,296,739 by 49, NURSING_HOME 14,700 by 61 with lat/lon. Two corrections. First, the claim that MEDICARE_PROVIDER is 'the only million-row cloud with real depth' is false: HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER is the identical file loaded twice — same 1,296,739 rows, same 81 columns, the only difference in the whole column list being NPI versus RNDRNG_NPI. Anyone running on both double-counts. Second, the substrate is wider than 34 tables, because a two-column cloud is still a cloud: 801 tables carry lat and lon together, and persistent homology on spatial points is the oldest use of this technique. The distance-column grep was honest — 45 hits, every one a TEXT column named DISTANCE in ATF, portal and DPRK-missile tables, plus no DEGREE/CENTRALITY/PAGERANK/COMPONENT_ID column anywhere. But that absence is not a data gap, which is why the tier moved.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS` — 6,103 rows. 107 typed-numeric columns on 6,103 hospitals — the densest per-row cloud in the warehouse and small enough to run in seconds
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER` — 44,429 rows. 204 typed-numeric columns on 44,429 Medicare facilities — the widest numeric table anywhere, no duplicate twin
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE` — 503,917 rows. 62 typed-numeric columns over half a million providers — the biggest genuinely wide cloud with no known duplicate

> This was under-called on the first pass: the missing piece was a distance calculation, which is arithmetic you write, not a table you need — the clouds exist today, and the real trap is that the 1.3M-row Medicare table is loaded twice under two names.

### Percolation theory

**Readiness:** 🟡 **Partial**  *(changed from ✅ Ready during the completeness review — reason below)*

**Needs.** A network whose links each carry a strength score, so you can turn a dial from 'only rock-solid links count' down to 'count everything' and watch the moment scattered islands snap into one giant blob. The dial setting where the snap happens is the finding.

**What exists.** Verified line by line and it holds. CONNECT_EDGES exists in LIBRARY_META.CONNECT at exactly 4,910 rows and its column list is confirmed: A, B, KEY, TIER (TEXT), A_COL, B_COL, MATCHED (NUMBER), A_DISTINCT (NUMBER), B_DISTINCT (NUMBER), MATCH_RATE (FLOAT), CONFIDENCE (FLOAT), SAMPLE, RUN_ID, BUILT_AT — three independent threshold dials plus three weight columns on every edge. V_CONNECTIONS, V_CONNECTIONS_CORE and V_CONNECTION_SUMMARY all exist as views in the same schema. MATCH_PAIRS is confirmed at 181,002,484 rows with KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B. ARCOS checks out completely: LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS at 178,598,026 rows with REPORTER_DEA_NO and BUYER_DEA_NO both TEXT, TRANSACTION_DATE a real DATE, and QUANTITY, DOSAGE_UNITS, BASE_WEIGHT_GRAMS, DOSAGE_STRENGTH and TOTAL_MME all real FLOATs. Two things to sharpen. The node-count ceiling was stated as ~3,033 tables, but edges can reference views as well, so the honest ceiling is the 4,847 objects in the warehouse — still trivially small. And CONNECT_EDGES_INC sits alongside at 3,182 rows, so the edge set has an incremental sibling; which of the two is current was not checkable from metadata alone.

**The gap.** Downgraded after review. The threshold dial on the connection map is measuring the sampler, not the warehouse: 4,910 measured table pairs out of roughly 4.6 million possible pairs across 3,033 base tables is about 0.1% coverage, and a missing pair there means "never measured", not "no overlap". Percolation's entire output is the threshold where islands snap into one blob — on a 0.1% sample that number is an artifact. `MATCH_PAIRS` does not rescue it either: a row says one key value appeared in two TABLES, not that two entities are linked.

**Distance to ready.** Run it on a real physical network instead of on the warehouse's own wiring. The opioid shipment table is a genuine directed weighted network with 178.6M edges in one identifier namespace and a FLOAT quantity to threshold on — percolation there is valid today with no repair. To make the connection-map lane valid you would have to measure a far larger share of table pairs first.

**Candidate tables.**

- `LIBRARY_META.CONNECT.CONNECT_EDGES` — 4,910 rows. TIER, MATCH_RATE and CONFIDENCE confirmed on every edge — three ready-made threshold dials on a graph small enough to sweep instantly
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. REPORTER_DEA_NO to BUYER_DEA_NO with FLOAT quantities and a real DATE — a genuine physical shipment network you can threshold on volume
- `LIBRARY_META.CONNECT.MATCH_PAIRS` — 181,002,484 rows. KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B gives per-value witnesses, so edges can be weighted by real shared values instead of a tier label

> Valid today on the opioid shipment network; invalid on the connection map, because 0.1% of the possible table pairs have ever been measured.

### Network centrality

**Readiness:** ✅ **Ready**

**Needs.** A list of links where both ends are the actual things you care about — this person to that company, this doctor to that hospital — so 'who is quietly the bridge everything runs through' says something about the world instead of about the database.

**What exists.** The core reading survives verification. ICIJ is real and exact: CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS at 3,339,267 rows with NODE_ID_START, NODE_ID_END, REL_TYPE, LINK, STATUS and real DATE columns START_DATE and END_DATE, over node tables that all carry a NODE_ID column — ENTITIES 814,344, OFFICERS 771,315, ADDRESSES 402,246, INTERMEDIARIES 26,768, OTHERS 2,989 (2,017,662 nodes, so '~2.01M' was right). FACILITY_AFFILIATION is exact at 2,260,193 rows with NPI and CCN both present. GLEIF relationships is exact at 484,142, though the columns are named RELATIONSHIP_STARTNODE_NODEID / RELATIONSHIP_ENDNODE_NODEID with a separate NODEIDTYPE column rather than anything literally called LEI. ENTITY_MAP is confirmed at 33,312,349 rows carrying MEMBER_TABLES (ARRAY) and SOURCE_COUNT (NUMBER), BRIDGE_ENTITIES is confirmed empty at 0 rows, and a sweep for DEGREE, CENTRALITY, BETWEENNESS, PAGERANK or COMPONENT_ID turns up nothing but academic degrees on judges and MSHA injury-severity codes — so no graph metric is precomputed, which is fine because these are all computed at run time. The court-citation trap is worse than described and worth stating plainly: the citation table's columns really are ID/VOLUME/REPORTER/PAGE/CLUSTER_ID, and the table that would hold citing-to-cited edges, FED_COURTLISTENER_CITATION_MAP, exists but holds 0 rows. The Laboratory's '~12.88M entities across 31 spine tables' is stale — 33,312,349 in ENTITY_GOLDEN/ENTITY_MAP, 84,382,504 in ENTITY_INDEX/CONNECT_NODES.

**Candidate tables.**

- `LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS` — 3,339,267 rows. NODE_ID_START to NODE_ID_END with a relation type and real start/end dates — a true directed typed edge list over ~2M named nodes
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION` — 2,260,193 rows. NPI to CCN, hard federal identifiers on both ends — a clean doctor-to-facility graph
- `LIBRARY_META.CONNECT.ENTITY_MAP` — 33,312,349 rows. SOURCE_COUNT is bipartite degree already computed for 33.3M entities, with MEMBER_TABLES giving the neighbour list for free

> The spine links things to files, not to each other — so the honest people-to-people graphs are ICIJ, ARCOS and CMS affiliation, and the court-citation network is a dead end because the table that would hold those edges is sitting there empty.

### Entropy / information density

**Readiness:** ✅ **Ready**

**Needs.** Counts spread across buckets — categories, months, or places — so you can measure whether they are spread evenly or piled into one corner, and catch the moment the spread collapses into a pattern.

**What exists.** Every count was re-measured and every one is exact. LIBRARY_MARTS.TIMELINE holds exactly 436 views; 435 carry RIPPLE_SOURCE, RIPPLE_GRAIN and RIPPLE_CLOCK; 403 carry RIPPLE_TS. The 32 views without RIPPLE_TS are not failures — they are the per-domain index roll-ups (TIMELINE__HEALTH_INDEX and friends) plus a warehouse-wide one, so the clock rollout is cleaner than the raw gap suggests. Of the 436, exactly 312 match a severity/category signal and 81 match an outcome signal. CFPB complaints verified in full at 17,168,287 rows with PRODUCT, SUB_PRODUCT, ISSUE, SUB_ISSUE, COMPANY_RESPONSE, SUBMITTED_VIA and TAGS as text categories, STATE and ZIP_CODE for place, DATE_RECEIVED and DATE_SENT_TO_COMPANY as real DATEs, and IS_TIMELY, HAS_NARRATIVE, IS_CLOSED as real BOOLEANs. EPA SDWA violations verified at 15,432,737 rows with VIOLATION_CODE, VIOLATION_CATEGORY_CODE, CONTAMINANT_CODE and IS_HEALTH_BASED_IND — but it has 13 real DATE columns, not the four claimed, which makes it better than described. Two corrections on HMDA_HISTORIC (19,136,434 rows, correct): it has no DATE or TIMESTAMP column at all — its only clock is AS_OF_YEAR stored as TEXT, so any time entropy on it is year-grain and no finer; and it has no FIPS column, only STATE_CODE plus COUNTY_CODE plus CENSUS_TRACT_NUMBER, which you compose yourself. Finally, the 312 and 81 signal counts are column-NAME matches from the same loose severity and outcome rules the brief warns over-count badly, so treat them as upper bounds exactly like the 3,341.

**Candidate tables.**

- `LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS` — 17,168,287 rows. seven text category columns plus state, zip, two real DATEs and three BOOLEANs — textbook category-by-place-by-time entropy, all columns confirmed
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT` — 15,432,737 rows. violation, category and contaminant codes with a health-based flag and 13 real DATE columns for time-sliced distributions
- `LIBRARY_META.CONNECT.ENTITY_MAP` — 33,312,349 rows. MEMBER_TABLES gives each of 33.3M entities a distribution over source files, so entropy of that mix measures directly whether a thing is visible everywhere or hiding in one place

> Four hundred tables all got the same clock column last week, so one query shape runs across the whole warehouse — just know that the biggest mortgage table's clock is a year stored as text, so it can never be sliced finer than annually.

---

## GIS / Geographic Techniques

### Hotspot analysis (Getis-Ord Gi*)

**Readiness:** ✅ **Ready**

**Needs.** A number attached to a place (facilities per county, deposits per county, denials per tract), plus a rule for which places count as next-door to which. The rule can be "within so many miles" — it does not have to be a shared border.

**What exists.** Both halves are here today. LIBRARY_MARTS.CORE.DIM_COUNTY (3,222 rows) carries POP_CENTER_LAT and POP_CENTER_LON as real FLOATs plus POPULATION_2020, which gives you a distance-band neighbour rule and the per-person denominator out of the same table; LIBRARY_MARTS.CORE.DIM_TRACT does the same for 85,391 tracts. A distance band is Getis and Ord's own original form of the test, so the missing border-adjacency list the first pass treated as a blocker is not actually required. Clean county-keyed values exist to feed it: LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES (5,300,149 rows) has FIPS_CODE, and the 2026-08-10 defect review flagged only its COUNTY_NAME and COUNTRY_NAME, not FIPS_CODE; LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS (2,823,000) came back a clean OK with BRANCH_COUNTY_FIPS, BRANCH_DEPOSITS_THOUSANDS and an annual SURVEY_YEAR. The real hazard is the join key, not the neighbour rule: 88 of the 610 mart models in that review push a county or FIPS column through try_to_number (29 times on COUNTY, 16 on COUNTY_NAME, 12 on COUNTY_CODE, 6 on COUNTY_FIPS), which wipes leading zeros off FIPS codes and nulls county names outright — and only 9 of the 318 defect-clean models carry a county-FIPS column at all.

**Candidate tables.**

- `LIBRARY_MARTS.CORE.DIM_COUNTY` — 3,222 rows. POP_CENTER_LAT and POP_CENTER_LON as FLOAT plus POPULATION_2020 — the neighbour rule and the rate denominator come out of one 3,222-row table
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` — 5,300,149 rows. FIPS_CODE survived the Aug-10 review unflagged (only COUNTY_NAME and COUNTRY_NAME were bad-cast), so 5.3M regulated facilities roll up to clean county counts
- `LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS` — 2,823,000 rows. verdict OK in the defect review, with BRANCH_COUNTY_FIPS, BRANCH_DEPOSITS_THOUSANDS and SURVEY_YEAR — a clean value per county per year

> The blocker is not the missing border list — it is that 88 mart models ran their county and FIPS columns through a number cast, so the key you would join on is the thing most likely to be broken.

### Kernel Density Estimation (KDE)

**Readiness:** ✅ **Ready**

**Needs.** Dots on a map — a latitude and a longitude per row that are actually numbers, not text. Optionally a weight so a big facility counts more than a small one.

**What exists.** 801 objects have columns NAMED latitude and longitude, but only 120 have both stored as real numbers — the other 679 keep coordinates as text, which is the actual reason the headline number collapses (the 608 hash-named city-portal crawl objects are a subset of that, not the whole story). Of the 120, 54 sit in LIBRARY_MARTS domain schemas and 21 carry 100,000 rows or more; the rest are TIMELINE views and staging copies of the same sources. The big ones are real: LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS at 58,104,610 vessel pings (LATITUDE/LONGITUDE FLOAT plus POSITION_GEOGRAPHY, the only true GEOGRAPHY column in all 162,750 columns, exposed twice), LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES at 5,300,149, and LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO at 3,135,554 which also carries POPULATION_DENSITY as a FLOAT. Two corrections to the first pass: FRS has no NAICS column at all (its NAICS codes live in a separate 2,179,702-row table whose own header count disagrees at 500,000), and LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY's 7,200,550 rows are ingredient-disclosure records keyed by INGREDIENT_RECORD_ID, not 7.2M wells — plotting them raw would make a chemically talkative operator look like a drilling hotspot.

**Candidate tables.**

- `LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS` — 58,104,610 rows. LATITUDE and LONGITUDE as FLOAT, a genuine GEOGRAPHY column and a DATE — the densest point cloud in the warehouse, and its Aug-10 verdict is OK
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` — 5,300,149 rows. LATITUDE/LONGITUDE FLOAT on every EPA-regulated facility, with ADDRESS, COUNTY, FIPS_CODE and POSTAL_CODE to slice by — but no NAICS on this table
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO` — 3,135,554 rows. LATITUDE/LONGITUDE FLOAT plus POPULATION_DENSITY on the same row — the heat surface and the people underneath it come from one table

> The only technique here that needs nothing built first, but check row grain before you plot: FracFocus's 7.2M rows are chemical ingredients, not wells, and a prior session found loaders writing the text 'nan' into coordinate cells.

### Spatial autocorrelation (Moran's I)

**Readiness:** ✅ **Ready**

**Needs.** A value per place, a rule for which places are near which, and a shuffle test — reshuffle the values across places a few hundred times to see whether the real clustering beats random.

**What exists.** All three are available. The neighbour rule comes from the same centroids as hotspot analysis (DIM_COUNTY 3,222 and DIM_TRACT 85,391, both with POP_CENTER_LAT/LON as FLOAT and POPULATION_2020), so no border-adjacency table is needed. The shuffle machinery is already written and running: reports/ripples_neighbor_rule_2026-08-21.md documents a 20-draw random control group across three domains — its neighbour key is corporate ownership rather than geography, so swapping in distance is the only change. On values, the first pass picked LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS (165,531 rows) for its county FIPS, but that is exactly the wrong column to lean on — all of its county and FIPS columns are among its 7 bad casts in the Aug-10 review; what saves it is that the same table carries LATITUDE and LONGITUDE as FLOAT alongside HPSA_SCORE and HPSA_ESTIMATED_UNDERSERVED_POPULATION, so it works as points and never touches the broken key. One absolute claim from the first pass is also wrong: a polygon layer does exist — LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY carries a GEOMETRY column with HOLC_GRADE, FIPS and LAT/LON — though the mart holds only 1,155 rows against 10,154 in raw landing, so it is a redlining sample, not a national layer.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS` — 165,531 rows. HPSA_SCORE and HPSA_ESTIMATED_UNDERSERVED_POPULATION as FLOAT sitting on LATITUDE/LONGITUDE FLOAT — use the coordinates, not its seven bad-cast county and FIPS columns
- `LIBRARY_MARTS.CORE.DIM_TRACT` — 85,391 rows. 85,391 tract centroids with POPULATION_2020 — the finest grain at which a distance-band neighbour rule can be built, and the denominator for any rate
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` — 5,300,149 rows. FIPS_CODE is one of the few county keys the defect review left unflagged, so 5.3M facilities give a clean value per county to test for clustering

> The random-shuffle code this test needs is already built and running on corporate ownership — pointing it at distance instead of ownership is the whole job.

### Voronoi diagrams

**Readiness:** ✅ **Ready**

**Needs.** Points, plus a genuine reason each point owns the ground around it — a branch that takes deposits, a water system that serves households. Without that ownership meaning it is decoration.

**What exists.** The Laboratory calls this a probable dud; the warehouse disagrees in one strong lane and one broken one. LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS (2,823,000 rows) came back a clean OK in the Aug-10 defect review and carries SIMS_LATITUDE and SIMS_LONGITUDE as FLOAT, BRANCH_DEPOSITS_THOUSANDS as a NUMBER, BRANCH_COUNTY_FIPS and an annual SURVEY_YEAR — a real dollar amount owned by each individual point. Assigning LIBRARY_MARTS.CORE.DIM_TRACT's 85,391 population-weighted centroids to their nearest branch turns the whole tessellation into a plain nearest-point join with no geometry engine, and POPULATION_2020 gives people-per-catchment immediately, so nothing is missing to get the numbers. The water lane is weaker than the first pass claimed: LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS (434,040) genuinely has POPULATION_SERVED_COUNT and SERVICE_CONNECTIONS_COUNT but no coordinates (correct), and its partner LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS (578,198) has COUNTY_SERVED flagged as a bad cast and a row disagreement against a 500,000 header, so the declared territory is itself defect-flagged. A table literally named SDWA_SERVICE_AREAS does exist (422,464 rows, verdict OK, misfiled under the IMMIGRATION schema) but holds only a service-area type code, not any geography.

**Candidate tables.**

- `LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS` — 2,823,000 rows. SIMS_LATITUDE/SIMS_LONGITUDE FLOAT plus BRANCH_DEPOSITS_THOUSANDS and SURVEY_YEAR, and a clean defect verdict — each point genuinely owns a measurable amount
- `LIBRARY_MARTS.CORE.DIM_TRACT` — 85,391 rows. 85,391 centroids with POPULATION_2020 turn the tessellation into a nearest-point join and hand you people-per-catchment in the same step
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS` — 578,198 rows. CITY_SERVED and ZIP_CODE_SERVED per water system are usable as a declared-territory check, but COUNTY_SERVED is a flagged bad cast and the row count disagrees with its header

> Not the dud the catalog assumes — people-per-bank-branch works as a plain join today; only the drawn picture is blocked, because there is no outline anywhere to clip the cells against.

### Flow maps

**Readiness:** 🟡 **Partial**  *(tier held, but the stated gap was corrected during the completeness review — see below)*

**Needs.** One row saying a thing went from here to there — a start place and an end place side by side, ideally with an amount and a date — plus coordinates for both ends so the arc can be drawn.

**What exists.** The shape index's 558 origin-and-destination tables is close to worthless and the review debunked it: the top "origin" column names are loader bookkeeping — SOURCE_RUN_ID (1,884), _SOURCE_URL (1,100), _SOURCE_RUN_ID (948) — and only 32 columns in the whole warehouse are literally named ORIGIN. About six genuine same-row flow families survive, and they are strong on the from-and-to and weak on the coordinates.

`LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` carries reporter city/state/zip to buyer city/state/zip across 178,598,026 shipment rows with DOSAGE_UNITS and TOTAL_MME as FLOAT. **A mid-sweep claim that its date and county columns are bad casts was read off the backup copy of the table, not the live one** — in the live mart BUYER_COUNTY is TEXT and the clock index rates TRANSACTION_DATE as happened / day / high confidence, calling it the cleanest big event clock in its batch. The real limit on it is span: coverage is 2006–2012, not 2006–2026.

`LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS` genuinely pairs damaged ZIP/city/state with rental-resource ZIP/city/state plus a rental assistance amount — and its origin end needs no crosswalk at all, because it carries a census tract id that joins straight to the tract centroid table. Its 3,080,000 rows is an exactly round count, the shape confirmed as a load cap in 18 other tables.

`LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL` holds recipient county FIPS and place-of-performance county FIPS on the same row across 19,902,879 rows — the only county-to-county lane there is. **The bad-cast warning previously attached to those two columns is stale**: that defect was repaired on 2026-08-10 and both columns land as TEXT today, leading zeros intact. The real problem with that table is different and worse — all 112 of its columns are TEXT, including every obligation amount and the action date, so a weighted or dated flow needs a cast first. Its contracts twin has the identically-named money columns as FLOAT, so this is a per-table modelling miss, not a source limitation.

`LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL` already holds district and transfer-district on the same row across 6.3M cases — but court districts have no geography anywhere in the warehouse, which kills the map and not the flow. The transport equivalent is a confirmed 21-row stub.

**The gap.** Corrected after review — the original blocker ("nothing can place a ZIP on a map") was wrong. ZIP → county → centroid is a two-hop join over two tables that both exist today: `LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY` (46,960 rows) maps every ZIP to a county, and `LIBRARY_MARTS.CORE.DIM_COUNTY` (3,222) carries POP_CENTER_LAT/LON as FLOAT. So flows are drawable **today at county resolution with no ingest**. What is genuinely missing is a ZIP-level centroid, so the flagship ZIP-to-ZIP flows collapse from roughly 33,000 endpoints to 3,222 — a real loss of resolution, not a blocked technique. Separately: the recipient and place-of-performance county FIPS columns on the USAspending assistance table land as TEXT in the mart, so the leading zeros are probably intact — unverified, check the values before trusting them.

**Distance to ready.** One dbt model, hours not days: DIM_ZIP_POINT — ZCTA5 from XWALK_ZCTA_COUNTY joined to DIM_COUNTY's population-weighted centroid, with a tie-break for the ZIPs that span counties (46,960 rows cover roughly 33,000 ZIPs, so some span). Optional follow-on of about a day for true per-ZIP centroids: average the coordinates on the ~12.9M already-geocoded ZIP-stamped facility and branch rows — finer, but facility-weighted and with holes where no regulated site exists.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. reporter city/state/zip to buyer city/state/zip on 178.6M rows with DOSAGE_UNITS and TOTAL_MME as FLOAT and the cleanest big event clock in the warehouse — the ZIP ends are clean and drawable at county resolution today; coverage stops at 2012
- `LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS` — 3,080,000 rows. DAMAGED_ZIP_CODE/CITY/STATE to RENTAL_RESOURCE_ZIP_CODE/CITY/STATE with RENTAL_ASSISTANCE_AMOUNT — household-grain displacement, though the round row count fits the confirmed load-cap pattern
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL` — 19,902,879 rows. place-of-performance and recipient county FIPS on the same row — the only county-to-county lane, and the FIPS columns are TEXT and intact after the August repair. Every amount and date on this table is TEXT though, so weighting a flow needs a cast

> Not blocked — just coarse. Every ZIP-to-ZIP flow in the building can be drawn today at county resolution; one small model takes it down to ZIP.

---

## Other Domains Raided for Ideas

### Epidemiology → contact tracing graphs

**Readiness:** ✅ **Ready**

**Needs.** Records that put two parties in the same place at the same time — same building, same prescriber, same employer, same address — with a stable ID for each party and a start and end time. Without the clock you get a crowd, not a contact.

**What exists.** One table is literally contact tracing: LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS, 2,571,975 rows carrying PERSON_HASH, DETENTION_FACILITY plus its code, and BOOK_IN_AT / BOOK_OUT_AT as real TIMESTAMP_NTZ columns — verified in the column list. CORRECTION to the first pass: the time index does NOT rate that clock CLEAN. Its ruling file says the primary clock is STAY_BOOK_OUT_DATE at confidence MEDIUM (2022-10-01 to 2026-03-11, populated on 2,397,989 of 2,571,975 rows), and states in writing that the four cast book-in/book-out timestamps 'never reached the candidate list' — so the exact columns this technique needs are typed but unrated. It also warns some book-outs are future-dated scheduled releases (max 2027-02-01), which would stretch stays and inflate overlaps. The table additionally ships DUPLICATE_LIKELY, DUPLICATE_LIKELY_SAMEDAY, DUPLICATE_LIKELY_BOND and DUPLICATE_DROP_ROW columns — the mart flags its own suspected duplicate rows, and unfiltered those double-count co-presence. Behind it: LIBRARY_META.CONNECT.ENTITY_XREF holds 2,672,384 rows with RELATION and FANOUT; LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION adds 2,260,193 NPI↔CCN rows and has ZERO date columns of any type and zero entries in the clock index — genuinely undated, verified. Shared-address tracing is column-name surface only: 1,622 tables match an address-ish name (513 plain ADDRESS), which proves nothing about population. Person keys are thin: the person signal covers 387 tables but is dominated by LAST_NAME (80) and FIRST_NAME (68); PERSON_ID appears in 14 tables and PERSON_HASH in exactly two marts, both ICE.

**Candidate tables.**

- `LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS` — 2,571,975 rows. PERSON_HASH + DETENTION_FACILITY + BOOK_IN_AT/BOOK_OUT_AT as TIMESTAMP_NTZ — same place, same time, per person, no join
- `LIBRARY_META.CONNECT.ENTITY_XREF` — 2,672,384 rows. KEY_A/VALUE_A to KEY_B/VALUE_B with RELATION and FANOUT — a typed shared-key link with a hub-size counter to cap noise
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION` — 2,260,193 rows. NPI↔CCN bipartite co-affiliation — the doctor-shares-a-building edge, with no date column at all

> One table already IS contact tracing — but its book-in/book-out clock was never rated, some book-outs are future-dated scheduled releases, and the table flags its own duplicate rows, so filter those three things before you count a single overlap.

### Astronomy → sky surveys / N-body clustering

**Readiness:** ✅ **Ready**

**Needs.** A very large cloud of points — millions, not thousands — plus some measure that pulls related points together, so you can cluster and render density instead of drawing every dot. Distance on a map counts as that measure.

**What exists.** The point cloud is real and verified: LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS holds 58,104,610 ship positions with LATITUDE and LONGITUDE as FLOAT plus POSITION_GEOGRAPHY typed GEOGRAPHY — and a dtype sweep of all 162,750 columns finds only TWO GEOGRAPHY columns in the entire warehouse, so that native spatial type is nearly unique to this table. 801 tables carry a lat AND a lon together. CORRECTION to the first pass's ranking: the next-densest point clouds after AIS are ENVIRONMENT__FED_FRACFOCUS_REGISTRY at 7,200,550, then ENVIRONMENT__FED_USGS_WATER at 6,694,816 (which the prior list skipped entirely), then ENVIRONMENT__FED_EPA_FRS_FACILITIES at 5,300,149. SECOND CORRECTION: LIBRARY_META.CONNECT.MATCH_PAIRS was cited as '181M shared-key pairs, the attraction measure for clustering entities' — its columns are KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B, so a row says one key value appeared in two TABLES, not that entity A attracts entity B. That is the same defect the first pass correctly called out under connectome mapping and then relied on here, so it is dropped as a candidate. What genuinely does not exist: a stored similarity of any kind. The full column-type census returns zero VECTOR-typed columns, and a name sweep for EMBED / VECTOR / COSINE / SIMILARITY returns only physical distance fields and false hits like 'GRANTSANDSIMILARAMOUNTSPAIDAMT'. Any similarity has to be computed, never read. Two hard limits: the AIS clock is verified CLEAN but spans only 2024-01-01 to 2024-01-08, and IMO_NUMBER was found sentinel-masked in a prior session, so vessel identity should come off MMSI or IMO_NORMALIZED, both of which exist in the column list.

**Candidate tables.**

- `LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS` — 58,104,610 rows. 58.1M lat/lon points plus POSITION_GEOGRAPHY — one of only two GEOGRAPHY columns in the warehouse, and the densest single cloud by 8x
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY` — 7,200,550 rows. 7.2M frack jobs with LATITUDE/LONGITUDE, API_NUMBER as the well id and JOB_START_DATE/JOB_END_DATE — the true second-densest cloud, and a dated one
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` — 5,300,149 rows. 5.3M mapped facilities with LATITUDE, LONGITUDE, ADDRESS and REGISTRY_ID — the point cloud you can actually label once clustered

> 58 million ship pings is a real star field, but it is one week of January 2024 — a photograph, not a survey — and there is no stored similarity anywhere in the warehouse, so every distance you cluster on has to be computed from scratch.

### Neuroscience → connectome mapping

**Readiness:** 🟡 **Partial**

**Needs.** A huge list of connections between individual things — not between tables — plus enough of them joined into one structure that you can ask which few nodes hold the whole thing together. Millions of edges, one connected map.

**What exists.** The headline number is misleading and the first pass was right to say so. LIBRARY_META.CONNECT.MATCH_PAIRS has 181,002,484 rows but its columns are KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B — one entity showed up in two TABLES, not entity A links to entity B. LIBRARY_META.CONNECT.CONNECT_EDGES is 4,910 rows and is a table-to-table schema graph by the brief's own statement. The genuine thing-to-thing edge lists, all verified in the column file: LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS at 3,339,267 (NODE_ID_START, NODE_ID_END, REL_TYPE), LIBRARY_META.CONNECT.ENTITY_XREF at 2,672,384, and HEALTH__FED_CMS_FACILITY_AFFILIATION at 2,260,193 — 8,271,844 typed edges — plus transaction tables that collapse into edges (ARCOS 178,598,026, FEC contributions 84,172,112). ADDED FACT the first pass missed: the ICIJ edges DO carry START_DATE and END_DATE as real DATE columns, but only 704,064 of 3,339,267 rows have a start date (21%) and 238,130 an end date, over a range of 1759 to 2029 — so that edge list is mostly undated and partly junk-dated. Nothing precomputes importance: CONNECT.BRIDGE_ENTITIES is confirmed EMPTY at 0 rows, CLUSTER_ASSIGNMENTS holds 23 source-level rows, SOURCE_OVERLAP_MATRIX 36, DOMAIN_OVERLAP_MATRIX 7. The 2026-08-12 question ladder names the wiring hole: DEA ARCOS, ICIJ, ICE detention, sanctions, NPDB and the courts have zero verified connections into the entity graph.

**The gap.** The pieces never join into one circuit map: the two biggest edge lists are documented graph dark matter — ARCOS (178,598,026 rows) and ICIJ Offshore Leaks (3,339,267) have zero verified connections into the entity spine — and BRIDGE_ENTITIES, the table meant to hold the hub nodes, is confirmed empty at 0 rows while the only warehouse-wide 'edge' table (MATCH_PAIRS, 181,002,484) links TABLE_A to TABLE_B, not entity to entity.

**Distance to ready.** Build one crosswalk per island — a DEA-number-to-registry bridge for ARCOS is the single highest-yield one — and the largest island fuses into the spine, at which point centrality can be run across it rather than inside it.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. REPORTER_DEA_NO and BUYER_DEA_NO are the same kind of ID, so 178.6M shipments collapse into one self-contained connected circuit you can run centrality on today
- `LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS` — 3,339,267 rows. NODE_ID_START to NODE_ID_END with REL_TYPE — the biggest true entity-to-entity typed edge list, though only 21% carry a start date
- `LIBRARY_META.CONNECT.ENTITY_XREF` — 2,672,384 rows. 2.7M bridge edges carrying a RELATION type and a FANOUT count, so noisy hub nodes can be capped before layout
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK` — 5,300,149 rows. found by the completeness critic — one of the "build a crosswalk per island" bridges is already built. There is live proof the chain traverses: a FINDINGS view already joins EPA facility violations to federal award dollars on the corporate parent key.

> You can run a real connectome inside the opioid shipment table today — 178.6M edges, one ID namespace, no join needed — what you cannot do is run one across the warehouse, because the islands do not touch and the table meant to hold the hub nodes is empty.

### Ecology → food web / trophic cascade

**Readiness:** ✅ **Ready**

**Needs.** Arrows, not lines. A depends on B, so knocking out B has to visibly hurt A — money flowing payer to payee, an owner over its facilities, a prime contractor over its subs. Then a second hop, so the shock can travel.

**What exists.** TIER RAISED from PARTIAL to READY, because the second hop already exists inside single tables and needs no missing table to reach it. LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS is a genuine multi-tier supply chain: 178,598,026 rows of REPORTER_DEA_NO to BUYER_DEA_NO with DRUG_NAME, QUANTITY, TOTAL_MME and TRANSACTION_DATE (verified happened/day, HIGH confidence, 2006-01-01 to 2012-12-31, 178,598,021 of 178,598,026 populated). Both endpoints are DEA registrant numbers in one namespace, so a buyer on one row is a reporter on another — the chain walks manufacturer to distributor to pharmacy in-table, and REPORTER_BUSINESS_ACTIVITY versus BUYER_BUSINESS_ACTIVITY labels the tier. LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS holds 484,142 directed LEI-to-LEI ownership edges (RELATIONSHIP_STARTNODE_NODEID to RELATIONSHIP_ENDNODE_NODEID) with a relationship type and a QUANTIFIERAMOUNT ownership share as FLOAT — recursive, so ownership trees walk several levels. CORRECTION: the first pass called GLEIF's clock CLEAN. It is not. Every period start/end column is TEXT, not DATE; the clock index rates them MEDIUM and records an explicit trap — the period slots are a flattened repeating group, so slot 1 is not the same KIND of period on every row and you must filter RELATIONSHIP_PERIOD_1_PERIODTYPE = 'RELATIONSHIP_PERIOD' first; the measured span runs 1832 to 2035, so future-dated junk is present. SECOND CORRECTION: direction is real in more than three places. Beyond ARCOS, GLEIF and the controller keys (LABOR__FED_MSHA_MINES.CURRENT_CONTROLLER_ID, MSHA_VIOLATIONS and MSHA_ACCIDENTS.CONTROLLER_ID, HEALTH__FED_CMS_NURSING_HOME.CHAIN_ID with NUMBER_OF_FACILITIES_IN_CHAIN), ICIJ Offshore Leaks is a fourth directed list at 3,339,267 typed start-to-end edges, and ECONOMICS__FED_USASPENDING_CONTRACTS_FULL carries PARENT_AWARD_ID_PIID — a contract-action to parent-award hop — though its raw table sits at exactly 20,000,000 rows, itself a round-number cap. THIRD CORRECTION: PROCUREMENT__FED_USASPENDING_SUBAWARDS is confirmed at exactly 5,000 rows (a page cap), and its typed columns carry no prime-award key, but it does hold a RECORD_JSON VARIANT column whose contents are unverified from metadata — the prime link may be inside it. The genuinely directionless part is the warehouse's own graph layer: ENTITY_XREF's RELATION values are affiliation and same-row, which have no arrow.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. reporter-to-buyer in one DEA namespace with quantity, MME and a HIGH-confidence day clock, plus a business-activity code on each side — the chain has real tiers and walks without a join
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS` — 484,142 rows. LEI-to-LEI ownership with a relationship type and a QUANTIFIERAMOUNT share — recursive, so knocking out a parent cascades down several levels
- `LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES` — 91,906 rows. CURRENT_CONTROLLER_ID and CURRENT_CONTROLLER_NAME point an owner down to each mine, and the same controller key repeats on MSHA_VIOLATIONS and MSHA_ACCIDENTS so the shock has somewhere to land

> Raised to Ready on review: the opioid shipment table and the corporate ownership table each carry both endpoints in one ID namespace, so a cascade walks two or more hops inside a single table — the capped 5,000-row subaward file blocks one lane of federal money, not the technique.

### Music/Audio → spectrograms

**Readiness:** ✅ **Ready**

**Needs.** One thing's activity chopped into a dense grid — categories down the side, time buckets across the bottom, intensity in each cell. Needs many time buckets per thing and many categories per thing, in the same table.

**What exists.** The best-supplied technique in the category, and it holds up. LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS delivers it with no join: 178,598,026 rows of BUYER_DEA_NO by DRUG_NAME by TRANSACTION_DATE with QUANTITY and TOTAL_MME, verified at day grain, HIGH confidence, 2006-01-01 to 2012-12-31 — 84 monthly columns for any one pharmacy. LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY adds 31,403,215 rows of CCN by MDS_ITEM_QUESTION_DESCRIPTION by REPORT_DATE with OVERALL_PERCENT, SHORT_STAY_PERCENT and LONG_STAY_PERCENT as intensity — CORRECTION: REPORT_DATE is a real DATE column but the clock index rates it clock=reported, grain=QUARTER, confidence MEDIUM, noting CMS publishes the file quarterly, so it is roughly 4 buckets a year, not daily. LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS gives 10,411,826 rows of REGISTRY_ID by POLLUTANT_NAME by REPORTING_YEAR, verified 2008 to 2024 at MEDIUM confidence — CORRECTION: both ANNUAL_EMISSION and REPORTING_YEAR are stored as TEXT, so the axis needs casting as well as the value. Underneath, 1,152 tables match the entity-plus-time combo and LIBRARY_MARTS.TIMELINE holds 436 views putting one canonical clock on 403 sources. The load-stamp trap the first pass flagged is confirmed: HEALTH__FED_CMS_PARTD_PRESCRIBERS looks perfect at 25,869,521 rows of NPI by drug, but the clock index states its only timestamp is _LOADED_AT and that it holds one single value (2026-07-23 22:44:38) across all 25.9M rows — no time axis at all.

**Candidate tables.**

- `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` — 178,598,026 rows. buyer by drug by day with QUANTITY and TOTAL_MME on a HIGH-confidence 2006-2012 clock — a drug-versus-month heat grid per pharmacy, 84 months deep, no join
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY` — 31,403,215 rows. CCN by quality measure by REPORT_DATE with three percentage columns as cell intensity, at quarterly resolution
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS` — 10,411,826 rows. facility by pollutant by year, 2008-2024 — a pollution fingerprint per site, once the TEXT year and TEXT emission are both cast

> One pharmacy, drugs down the side, months across the bottom, colour is pills — the opioid shipment table hands you that straight out, 84 months deep; the nursing-home and pollution grids are quarterly and yearly, so their bars are far wider than they look.

### Finance → correlation matrices / heatmap clustering

**Readiness:** ✅ **Ready**

**Needs.** Lots of separate lines measured on the same clock at the same grain, long enough to be worth comparing — dozens of time buckets each. Then you score every pair against every other pair and reorder the grid so the ones that move together clump.

**What exists.** The shared axis is live and verified. LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE holds 1,161,122 rows whose columns are exactly RIPPLE_SOURCE, RIPPLE_CLOCK, RIPPLE_GRAIN, RIPPLE_DAY and N_ROWS — one row per source, clock, grain and day with a count — beside 31 domain rollups (ENVIRONMENT_INDEX 274,313, JUSTICE_INDEX 236,956, HEALTH_INDEX 131,105) and RIPPLE_TIME_REGISTRY at 647 rows naming the chosen clock per live table. The series are pulled and scored: 371 measured, 307 scored, 136 carrying 100,000-plus rows, with 953 table-and-column series listed with grain and confidence. HARD CORRECTION: the first pass's clean-panel candidate, ECONOMICS__FED_BLS_QCEW, does not work. Its 3,619,437 rows all carry YEAR = 2022 — the measured span is 2022 to 2022 at HIGH confidence — and the clock index rules QUARTER 'not_a_date... a bare 1-4 ordinal with no year in it', so the table yields at most four time buckets against a technique that needs dozens. It is replaced by CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS: 17,168,287 rows, COMPANY by PRODUCT by ISSUE, DATE_RECEIVED verified 100% populated at day grain HIGH confidence from 2011-12-01 to 2026-07-23, with RECEIVED_MONTH already precomputed — roughly 175 monthly buckets across thousands of company series in one table. SECOND CORRECTION: HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE was called 'the widest such table live' at 62 numeric columns; it is the biggest of the wide tables by ROW count, but HEALTH__FED_CMS_POS_OTHER is far wider at 204 numeric columns of 473 (44,429 rows). 81 tables carry 20-plus numeric columns and 30 carry 50-plus. Two limits to respect: the 2026-08-20 trend sweep's own headline is that most strangeness it found is about how data was COLLECTED, not what happened, naming crawl schedules, partial-year files and bulk backfills — so a warehouse-wide matrix surfaces publication twins first; and the shared clock is uneven, with several domain rollups nearly empty (CRIMINAL_JUSTICE 1 row, HISTORY 2, MONEY_FINANCE 7, MARITIME 8, INVESTIGATIONS 16, JUDICIARY 21).

**Candidate tables.**

- `LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE` — 1,161,122 rows. RIPPLE_SOURCE by RIPPLE_CLOCK by RIPPLE_GRAIN by RIPPLE_DAY with N_ROWS — 403 sources already counted per day on one shared axis, the matrix input prebuilt
- `LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS` — 17,168,287 rows. COMPANY by PRODUCT by ISSUE with a fully populated day clock 2011-12 to 2026-07 and a prebuilt RECEIVED_MONTH — thousands of parallel monthly series, ~175 buckets deep, one table
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER` — 44,429 rows. 204 numeric columns on one row — the genuine widest within-record correlation form in the warehouse, not the 62-column table cited before

> The shared clock is built and 403 sources sit on it, but the county-employment panel the first pass leaned on holds only the year 2022 — and the trend sweep warned that things moving together here usually means they were downloaded together, not that the world moved together.

---

## Biggest Opportunities

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

## What the Laboratory doesn't have — and the warehouse does

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

## Caveats

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
