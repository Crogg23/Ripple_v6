# Lens-to-schema mapping matrix — 2026-09-07

Desk review only. Sources: `reports/warehouse_topo_map_2026-09-05.md`,
`reports/detective_toolkit_warehouse_map_2026-09-07.md`,
`reports/investigation_catalog_2026-09-07.md`, `.claude/traps.md`.
No live queries run. No table/column names invented beyond what the topo map
documents. "Strong fit" = the schema's known shape (money fields, timestamps,
identity keys, addresses, text fields, network tables) plausibly supports the
lens — not a claim the lens has been tested there.

---

## HEALTH — 98 tables, 363.2M rows
Best-fit lenses:
- **Benford's law / digit variance** — CMS Open Payments and Part D carry real dollar amounts (`TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `Tot_Drug_Cst`).
- **Power law tail / Pareto 80/20** — provider- and manufacturer-level payment concentration is a natural shape for NPI-anchored money.
- **Network science (betweenness, community detection)** — NPI is the widest identity bridge (59 wired tables), a real relationship graph.
- **Homophily / herding** — shared-rep prescribing patterns (diffusion lens) fits Part D prescriber data.
- **Missingness pattern** — heavy documented suppression (`GE65_Sprsn_Flag`, LEIE blanks) makes this schema a natural missingness testbed.
Posture: **Follow one entity** — pull one NPI across NPPES, Open Payments, Part D, LEIE.
Trap warning: LEIE NPI join only covers 10.6% of rows (floor, not full ban list); NPPES EIN/TIN columns are `<UNAVAIL>` on every row — never build an EIN edge from NPPES; Open Payments manufacturer ID is a 12-digit numeric ID, not a payment amount, despite the column name.

## FINANCE — 56 tables, 102.1M rows
Best-fit lenses:
- **Benford's law / digit variance** — FEC individual contributions and USAspending awards are the canonical worked examples in the toolkit itself.
- **Round-number clustering / regression discontinuity** — contribution limits ($200, $2,500) are documented thresholds.
- **Power law / Zipf / Pareto** — donor and committee-level concentration.
- **Betweenness / community detection** — committee-to-committee transfer graph (FEC_CMTE_ID, 45k tables reach).
- **Address reuse / fingerprint match** — straw-donor patterns via shared address/name.
Posture: **Reverse the question** — start from a spend spike, walk back to donors.
Trap warning: FEC committees reuse IDs across cycles with no cycle column (join the DIM table, not raw); Schedule E carries prank filings worth tens of billions; committee-to-committee is 93% earmark memos needing `MEMO_CD <> 'X'` filter; independent-expenditure mart totals read ~20x the real FEC figure.

## POLITICS — 79 tables, 21.0M rows
Best-fit lenses:
- **Signaling / Nash tell** — lobbying-then-legislation timing chains.
- **Change-point detection / Granger causality** — lobbying filing vs. bill/contract timing.
- **Stylometry / N-gram fingerprint** — boilerplate phrasing across filings (LDA, FARA).
- **Cui bono** — committee membership vs. money flow.
Posture: **Cross-domain collision** — join lobbying/committee data against FINANCE money with no built relation.
Trap warning: committee membership has no cycle-aware dedupe (5.7x fan-out joining to money); PARTY column holds 'majority'/'minority', not D/R; no congressional-district geometry exists at all; EDUCATION schema (not POLITICS) actually holds lobbying/Fed-rate tables mislabeled by folder name — check tables, not schema names.

## JUSTICE — 65 tables, 57.9M rows
Best-fit lenses:
- **Small-world network / betweenness** — DOCKET key reaches 17 tables, a real case-linkage graph.
- **Duplicate near-miss / Levenshtein** — litigant/party name collisions are heavily documented.
- **Survivorship bias** — active-only exclusion/case snapshots.
- **Time of death window** — docket filing gaps.
Posture: **Absence hunting** — missing rosters (e.g., judges who resigned mid-term) are a documented gap type here.
Trap warning: common-surname case names ("SMITH V. UNITED STATES") are noise unless distinctive; financial disclosure YEAR is column-shifted text on over half of rows; judge district codes need `ASSIGNED_TO_ID`, not `FILEJUDG`.

## ENVIRONMENT — 75 tables, 107.7M rows
Best-fit lenses:
- **Spatial clustering / hot-spot mapping** — EPA facility and emissions data is inherently geospatial.
- **Entropy measure** — self-reported emissions sequences, explicitly a toolkit example.
- **Distance decay** — facility-to-community effects.
- **Bridge/cut vertex** — FRS_ID is the environmental identity bridge (20 wired tables).
Posture: **Cross-domain collision** — FRS facility identity joined against FINANCE or JUSTICE enforcement.
Trap warning: a junk-hub geometry (`INTL_FR_DATA_GOUV_FULL.SPATIAL_GEOM`) contains every US point and fakes centrality; lat/lon in TRI_FACILITY are packed DDMMSS with swapped pairs.

## HOUSING — 18 tables, 45.8M rows
Best-fit lenses:
- **Regression discontinuity / Simpson's paradox** — HMDA lending-denial trend by lender size is a toolkit-adjacent shape.
- **Spatial clustering / hot-spot mapping** — HOLC redlining polygons, FEMA registrations.
- **Survivorship bias** — HMDA originations-only file (zero denials documented separately).
Posture: **Absence hunting** — HMDA has originations but no denials; a real, documented gap.
Trap warning: `HOUSING__FED_MAPPING_INEQUALITY` mart is 1,155 rows vs 10,154 in landing (89% loss); HOLC_ID is not an id; FEMA IA FIPS is unpadded text creating false distinct-state collisions.

## MARITIME — 1 table, 58.1M rows
Best-fit lenses:
- **Autocorrelation / seasonality** — AIS vessel-position time series.
- **Spatial clustering** — vessel movement/port clustering.
- **Diffusion/spread rate** — vessel-route pattern propagation.
Posture: **Chase a random row** — follow one IMO-keyed vessel across its position history (single-table schema, so this is close to the only posture available).
Trap warning: none documented specifically for NOAA_AIS in traps.md; note IMO reach is only 9 tables — a single-table schema has essentially no cross-table verification available in-schema.

## ECONOMICS — 44 tables, 43.1M rows
Best-fit lenses:
- **Benford's law / digit variance** — SEC 13F holdings, CFPB HMDA dollar fields.
- **Pareto 80/20 / power law** — 13F filer concentration is the toolkit's own worked example.
- **Log-normal / Poisson clustering** — filing interval and timing patterns.
- **Mutual information** — contract size vs. lobbying spend (cross-schema but economics-anchored).
Posture: **Assume guilt first** — take top-10 13F filers, try to prove clean.
Trap warning: no traps.md entries specific to SEC 13F located in this pass; general "everything is TEXT" cast trap applies warehouse-wide.

## CORPORATE_REGISTRY — 11 tables, 29.7M rows
Best-fit lenses:
- **Trace evidence** — shared registered agent across "unrelated" filings, a toolkit worked example.
- **Bridge/cut vertex** — UK PSC ownership chains, single shell company as chokepoint.
- **Survivorship bias** — active-companies-only visibility, explicit toolkit example for this schema.
- **N-gram fingerprint** — boilerplate clauses across filing purposes.
Posture: **Follow one entity** — walk a COMPANY_NO/LEI through PSC ownership layers.
Trap warning: `UK_COMPANIES_HOUSE_PSC` stopped mid-load, ~7M of an expected 10M+ rows — any count is a floor.

## IMMIGRATION — 15 tables, 19.9M rows
Best-fit lenses:
- **Time of death window** — case-processing gaps.
- **Missingness pattern** — structurally broken parallel tables are a direct missingness signal.
- **Change-point detection** — case volume/backlog shifts.
Posture: **Absence hunting** — the working case table vs. the broken parallel load is itself the finding.
Trap warning: `IMMIGRATION__FED_EOIR_CASE_DATA` is a broken one-column parallel load (same row count as the real `FED_EOIR_CASES`) — use the latter; also note 12 tables mislabeled "immigration" in the registry domain column are not actually immigration data (CMS/EPA) — verify by table, not domain tag.

## CONSUMER_PROTECTION — 1 table, 17.2M rows
Best-fit lenses:
- **Text/language (stylometry, n-gram)** — CFPB complaints are narrative text, a natural fit.
- **Time series (seasonality, autocorrelation)** — complaint volume over time.
- **Chi-square uniformity** — complaint category distribution.
Posture: **Outsider's question** — what would a consumer-rights lawyer ask first of a complaints table.
Trap warning: none specific to CFPB complaints found in this pass; single-table schema limits cross-verification (external baseline needed).

## CONSUMER_SAFETY — 4 tables, 12.4M rows
Best-fit lenses:
- **Change-point detection** — recall/complaint volume shifts.
- **Spatial clustering** — complaint geography if present.
- **Missingness pattern** — NHTSA complaints documented as headerless/positional.
Posture: **Absence hunting** — headerless columns mean most fields are effectively unusable/missing by structure.
Trap warning: `FED_NHTSA_COMPLAINTS` is headerless `C1..C54`; only C3/C4/C5/C6/C8/C12 are known-usable, and 110k rows have a blank date.

## REFERENCE — 34 tables, 8.4M rows
Best-fit lenses:
- **Missingness pattern / provenance skepticism** — reference/lookup tables are where mislabeling is most consequential.
- **Duplicate near-miss** — code/lookup table redundancy.
Posture: **Verification-layer support role** — reference tables mainly serve other schemas' joins, not lenses of their own.
Trap warning: none specific found; treat as low-signal for most of the 52 lenses given its lookup-table nature.

## LABOR — 12 tables, 7.2M rows
Best-fit lenses:
- **Chi-square uniformity / column-shift detection** — DOL OLMS shows exactly this failure mode (shifted-year columns).
- **Missingness pattern** — LDA lobbying coverage gaps (1999-2010, 2020-2021 only, per traps).
- **Regression discontinuity** — wage/threshold rules.
Posture: **Red-team your own pipeline** — the OLMS shortage-amount trap is a pipeline artifact, not a real signal, and is the textbook case for this verification check.
Trap warning: `FED_DOL_OLMS SHORTAGE_AMOUNT` non-zero rows are all column-shifted junk — there are no real shortage dollars in that column.

## EDUCATION — 17 tables, 4.6M rows
Best-fit lenses:
- **Cross-domain collision** — this schema is explicitly a grab-bag (CFTC, Fed rates, political ads, Senate lobbying), so accidental cross-domain joins are already latent here.
- **Provenance skepticism** — given the mislabeling, source-checking every table is mandatory.
Posture: **Outsider's question** — "wait, why is this in EDUCATION?" is literally the finding.
Trap warning: **explicit trap** — EDUCATION schema holds non-education tables (CFTC futures, Fed interest rates/flow-of-funds, Google political ads, Senate lobbying filings); schema name is not a content guarantee.

## SCIENCE_RESEARCH — 6 tables, 2.5M rows
Best-fit lenses:
- **Entropy measure** — measurement/research data noise characteristics.
- **Compressibility test** — synthetic-vs-measured data detection.
Posture: **Chase a random row** — small schema, best explored table-by-table.
Trap warning: none documented; smallest, least-verified schema in this pass — treat any finding as needing external baseline before trusting.

## TRANSPORT — 12 tables, 2.2M rows
Best-fit lenses:
- **Missingness pattern** — mangled-header table is a direct example.
- **Spatial clustering** — airport/facility geography.
Posture: **Red-team your own pipeline** — the ADIP header trap is a load bug, not a data finding.
Trap warning: `TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS` loaded with mangled headers (`UNNAMED_1..5`); unusable until reloaded.

## OPEN_DATA — 12 tables, 1.7M rows
Best-fit lenses:
- **Missingness pattern / provenance skepticism** — PORTAL_CKA structure is column-partial by construction (different resources, different headers).
- **Duplicate near-miss** — ROWID collisions across monthly resources.
Posture: **Red-team your own pipeline** — this schema's shape is dominated by loader artifacts, not underlying signal.
Trap warning: portal tables are folders of resources with non-shared headers — up to 71 of 105 columns partially filled on one table; ROWID is not a primary key and silently props up dedupe; MERCHANT strings are terminal strings, not merchant identity.

## TIMELINE — 32 tables + 403 views, 1.2M rows
Best-fit lenses:
- **Change-point detection / autocorrelation** — this schema's entire purpose is time-indexed rollups.
- **Seasonality check** — built for exactly this.
Posture: **Absence hunting** — stale materialized rollups behind "green" guards are the documented failure mode.
Trap warning: `_INDEX` rollup tables are materialized and can go stale silently (no builder existed for them); view column lists freeze at create time and break silently on upstream schema changes; SNAPSHOT_DATE reflects when a snapshot was read, not when an event happened — don't treat it as event time.

## ENERGY — 29 tables, 0.5M rows
Best-fit lenses:
- **Time series (seasonality, change-point)** — EPA CAMPD daily emissions, EIA plant/utility data.
- **Spatial clustering** — plant-level geography.
Posture: **Chase a random row** — smallest schema by rows among the 20, best walked entity-first.
Trap warning: `_INGESTED_AT` on EPA CAMPD reads as epoch-microseconds-as-seconds on at least 7 tables — never trust it as a date without a range check first.

---

## Coverage gaps

Thin-coverage schemas — metadata doesn't obviously support many of the 52 lenses:

- **MARITIME** (1 table) and **CONSUMER_PROTECTION** (1 table) — single-table schemas have no internal cross-table lens (no betweenness, no community detection, no trace evidence) and weak in-schema replication/verification; findings there lean entirely on external baseline.
- **REFERENCE** (34 tables but lookup-shaped) — mostly code/lookup tables with no money, no timestamps, no network structure documented; low fit for math-laws, forensic, and network lenses alike.
- **SCIENCE_RESEARCH** (6 tables, 2.5M rows) — smallest documented footprint, no traps recorded at all, meaning no one has stress-tested it; treat any lens result here as unverified until a first pass exists.
- **ENERGY, TRANSPORT, OPEN_DATA** — small row counts and (per traps.md) load-artifact-dominated shapes; several of their strongest "findings" are already known to be pipeline bugs (mangled headers, partial-column portals), so lens results there need the pipeline-first check before anything else.
- Schemas with declared money fields and identity-key reach (HEALTH, FINANCE, ECONOMICS, ENVIRONMENT, CORPORATE_REGISTRY) carry the deepest lens coverage because they anchor the warehouse's four real identity bridges (NPI, EIN, FRS_ID, CCN/UEI); everything else inherits network lenses only secondhand, through those bridges.
