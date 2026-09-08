# Lens-first index — 2026-09-07

Inverted view of `reports/lens_schema_mapping_2026-09-07.md`: for each of the
52 lenses in `reports/detective_toolkit_warehouse_map_2026-09-07.md`, which
of the 20 warehouse schemas were flagged as a best fit, and the one-line
reason already given there. No new analysis — pure re-sort. Where a lens
bullet in the source combined two or three lens names (e.g. "Betweenness /
community detection"), the same reason is re-attributed under each lens it
names. Reasons are otherwise quoted/paraphrased directly from the source.

Lenses with no schema flagged are marked "no schema flagged yet in the desk
review."

---

## Math laws

**Zipf's law**
- FINANCE — donor- and committee-level concentration (grouped as "Power law / Zipf / Pareto").

**Benford's law**
- HEALTH — CMS Open Payments and Part D carry real dollar amounts (`TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `Tot_Drug_Cst`).
- FINANCE — FEC individual contributions and USAspending awards are the canonical worked examples in the toolkit itself.
- ECONOMICS — SEC 13F holdings, CFPB HMDA dollar fields.

**Power law tail**
- HEALTH — provider- and manufacturer-level payment concentration is a natural shape for NPI-anchored money.
- FINANCE — donor and committee-level concentration (grouped as "Power law / Zipf / Pareto").
- ECONOMICS — 13F filer concentration is the toolkit's own worked example (grouped as "Pareto 80/20 / power law").

**Pareto 80/20**
- HEALTH — provider- and manufacturer-level payment concentration is a natural shape for NPI-anchored money.
- FINANCE — donor and committee-level concentration.
- ECONOMICS — 13F filer concentration is the toolkit's own worked example.

**Small-world network**
- JUSTICE — DOCKET key reaches 17 tables, a real case-linkage graph (grouped as "Small-world network / betweenness").

**Preferential attachment**
- no schema flagged yet in the desk review.

**Log-normal**
- ECONOMICS — filing interval and timing patterns (grouped as "Log-normal / Poisson clustering").

**Poisson clustering**
- ECONOMICS — filing interval and timing patterns (grouped as "Log-normal / Poisson clustering").

---

## Forensic tricks

**Time of death window**
- JUSTICE — docket filing gaps.
- IMMIGRATION — case-processing gaps.

**Fingerprint match**
- FINANCE — straw-donor patterns via shared address/name (grouped as "Address reuse / fingerprint match").

**Trace evidence**
- CORPORATE_REGISTRY — shared registered agent across "unrelated" filings, a toolkit worked example.

**Alibi check**
- no schema flagged yet in the desk review.

**Staging vs real**
- no schema flagged yet in the desk review.

**Chain of custody**
- no schema flagged yet in the desk review.

**Behavioral profiling**
- no schema flagged yet in the desk review.

---

## Cheap tells

**Round-number clustering**
- FINANCE — contribution limits ($200, $2,500) are documented thresholds (grouped as "Round-number clustering / regression discontinuity").

**Address reuse**
- FINANCE — straw-donor patterns via shared address/name.

**Timing tics**
- no schema flagged yet in the desk review.

---

## Network science

**Betweenness centrality**
- HEALTH — NPI is the widest identity bridge (59 wired tables), a real relationship graph (grouped as "Network science (betweenness, community detection)").
- FINANCE — committee-to-committee transfer graph (FEC_CMTE_ID, 45k tables reach), grouped as "Betweenness / community detection".
- JUSTICE — DOCKET key reaches 17 tables, a real case-linkage graph (grouped as "Small-world network / betweenness").

**Community detection**
- HEALTH — NPI is the widest identity bridge (59 wired tables), a real relationship graph.
- FINANCE — committee-to-committee transfer graph (FEC_CMTE_ID, 45k tables reach).

**Bridge/cut vertex**
- ENVIRONMENT — FRS_ID is the environmental identity bridge (20 wired tables).
- CORPORATE_REGISTRY — UK PSC ownership chains, single shell company as chokepoint.

**Homophily check**
- HEALTH — shared-rep prescribing patterns fit Part D prescriber data (grouped as "Homophily / herding").

---

## Stats of fraud

**Chi-square uniformity**
- CONSUMER_PROTECTION — complaint category distribution.
- LABOR — DOL OLMS shows this failure mode (shifted-year columns), grouped as "Chi-square uniformity / column-shift detection."

**Digit variance test**
- HEALTH — CMS Open Payments and Part D carry real dollar amounts (grouped as "Benford's law / digit variance").

**Regression discontinuity**
- FINANCE — contribution limits ($200, $2,500) are documented thresholds (grouped as "Round-number clustering / regression discontinuity").
- HOUSING — HMDA lending-denial trend by lender size is a toolkit-adjacent shape (grouped as "Regression discontinuity / Simpson's paradox").
- LABOR — wage/threshold rules.

**Cui bono**
- POLITICS — committee membership vs. money flow.

---

## Anomaly hunting

**Isolation forest logic**
- no schema flagged yet in the desk review.

**Z-score sweep**
- no schema flagged yet in the desk review.

**Missingness pattern**
- HEALTH — heavy documented suppression (`GE65_Sprsn_Flag`, LEIE blanks) makes this schema a natural missingness testbed.
- IMMIGRATION — structurally broken parallel tables are a direct missingness signal.
- CONSUMER_SAFETY — NHTSA complaints documented as headerless/positional.
- REFERENCE — reference/lookup tables are where mislabeling is most consequential (grouped as "Missingness pattern / provenance skepticism").
- LABOR — LDA lobbying coverage gaps (1999-2010, 2020-2021 only, per traps).
- TRANSPORT — mangled-header table is a direct example.
- OPEN_DATA — PORTAL_CKA structure is column-partial by construction (grouped as "Missingness pattern / provenance skepticism").

**Duplicate near-miss**
- JUSTICE — litigant/party name collisions are heavily documented (grouped as "Duplicate near-miss / Levenshtein").
- REFERENCE — code/lookup table redundancy.
- OPEN_DATA — ROWID collisions across monthly resources.

---

## Physics and biology analogies

**Entropy measure**
- ENVIRONMENT — self-reported emissions sequences, explicitly a toolkit example.
- SCIENCE_RESEARCH — measurement/research data noise characteristics.

**Diffusion/spread rate**
- HEALTH — shared-rep prescribing patterns fit Part D prescriber data (noted as "diffusion lens" within the "Homophily / herding" bullet).
- MARITIME — vessel-route pattern propagation.

**Herding/flocking**
- HEALTH — shared-rep prescribing patterns fit Part D prescriber data (grouped as "Homophily / herding").

---

## Game theory

**Nash tell**
- POLITICS — lobbying-then-legislation timing chains (grouped as "Signaling / Nash tell").

**Signaling**
- POLITICS — lobbying-then-legislation timing chains (grouped as "Signaling / Nash tell").

---

## Text and language

**Stylometry**
- POLITICS — boilerplate phrasing across filings (LDA, FARA), grouped as "Stylometry / N-gram fingerprint".
- CONSUMER_PROTECTION — CFPB complaints are narrative text, a natural fit (grouped as "Text/language (stylometry, n-gram)").

**N-gram fingerprint**
- POLITICS — boilerplate phrasing across filings (LDA, FARA).
- CORPORATE_REGISTRY — boilerplate clauses across filing purposes.
- CONSUMER_PROTECTION — CFPB complaints are narrative text, a natural fit.

**Levenshtein distance**
- JUSTICE — litigant/party name collisions are heavily documented (grouped as "Duplicate near-miss / Levenshtein").

---

## Time series

**Autocorrelation**
- MARITIME — AIS vessel-position time series (grouped as "Autocorrelation / seasonality").
- CONSUMER_PROTECTION — complaint volume over time (grouped as "Time series (seasonality, autocorrelation)").
- TIMELINE — this schema's entire purpose is time-indexed rollups (grouped as "Change-point detection / autocorrelation").

**Change-point detection**
- POLITICS — lobbying filing vs. bill/contract timing (grouped as "Change-point detection / Granger causality").
- IMMIGRATION — case volume/backlog shifts.
- CONSUMER_SAFETY — recall/complaint volume shifts.
- TIMELINE — this schema's entire purpose is time-indexed rollups.
- ENERGY — EPA CAMPD daily emissions, EIA plant/utility data (grouped as "Time series (seasonality, change-point)").

**Seasonality check**
- MARITIME — AIS vessel-position time series (grouped as "Autocorrelation / seasonality").
- CONSUMER_PROTECTION — complaint volume over time.
- TIMELINE — built for exactly this.
- ENERGY — EPA CAMPD daily emissions, EIA plant/utility data.

**Granger causality**
- POLITICS — lobbying filing vs. bill/contract timing (grouped as "Change-point detection / Granger causality").

---

## Geospatial

**Spatial clustering**
- ENVIRONMENT — EPA facility and emissions data is inherently geospatial (grouped as "Spatial clustering / hot-spot mapping").
- HOUSING — HOLC redlining polygons, FEMA registrations (grouped as "Spatial clustering / hot-spot mapping").
- MARITIME — vessel movement/port clustering.
- CONSUMER_SAFETY — complaint geography if present.
- TRANSPORT — airport/facility geography.
- ENERGY — plant-level geography.

**Distance decay**
- ENVIRONMENT — facility-to-community effects.

**Hot-spot mapping**
- ENVIRONMENT — EPA facility and emissions data is inherently geospatial (grouped as "Spatial clustering / hot-spot mapping").
- HOUSING — HOLC redlining polygons, FEMA registrations.

---

## Causal and bias traps

**Survivorship bias**
- JUSTICE — active-only exclusion/case snapshots.
- HOUSING — HMDA originations-only file (zero denials documented separately).
- CORPORATE_REGISTRY — active-companies-only visibility, explicit toolkit example for this schema.

**Simpson's paradox**
- HOUSING — HMDA lending-denial trend by lender size is a toolkit-adjacent shape (grouped as "Regression discontinuity / Simpson's paradox").

**Regression to the mean**
- no schema flagged yet in the desk review.

**Confounding variable**
- no schema flagged yet in the desk review.

---

## Epidemiology

**Contact tracing logic**
- no schema flagged yet in the desk review.

**R-naught style spread**
- no schema flagged yet in the desk review.

---

## Info theory

**Compressibility test**
- SCIENCE_RESEARCH — synthetic-vs-measured data detection.

**Mutual information**
- ECONOMICS — contract size vs. lobbying spend (cross-schema but economics-anchored).

---

## Notes on non-lens bullets encountered in the source

Two schemas (EDUCATION, and part of OPEN_DATA/REFERENCE/LABOR) listed
best-fit items that are investigation **postures** or verification habits
from the source file rather than named entries in the 52-lens toolkit:
"Cross-domain collision," "Provenance skepticism," "Column-shift detection."
These are not double-counted above as lens hits since they aren't among the
52 canonical lens names; they're preserved here for completeness rather than
silently dropped.

## Coverage gap summary

Of the 52 lenses, the following had zero schema hits in the source desk
review: Preferential attachment, Alibi check, Staging vs real, Chain of
custody, Behavioral profiling, Timing tics, Isolation forest logic, Z-score
sweep, Regression to the mean, Confounding variable, Contact tracing logic,
R-naught style spread — **12 lenses** with no schema flagged yet.
