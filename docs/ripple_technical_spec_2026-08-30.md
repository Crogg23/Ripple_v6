# Ripple — Technical Spec Sheet

*Pulled live from the warehouse 2026-08-30. No spec sheet existed before this —
built fresh from `LIBRARY_META.REGISTRY.CATALOG`, `LIBRARY_META.CONNECT.CONNECT_EDGES`,
`LIBRARY_META.CONNECT.CONNECT_EDGES_INC`, and `LIBRARY_META.CONNECT.LEADS`.
Numbers here will drift — re-run the queries below to refresh, don't hand-edit.*

---

## 1. Scale, top line

| Metric | Value |
|---|---|
| Landing rows (raw, all sources) | 1,250,067,942 |
| Landing tables | 2,208 |
| Sources registered (all lifecycle stages) | 3,283 |
| Sources actually landed/modeled (usable now) | ~589 |
| Entities resolved (people/orgs, deduped) | 33,312,349 |
| Connection edges (cross-source ID matches) | 4,512 (main) + 3,182 (incremental/probabilistic) |
| Leads (flagged contradictions, pending human review) | 17,256 |

---

## 2. Source pipeline — where everything sits in the funnel

Every source moves through: `scouted → queued → sampled → landed → modeled`
(or `stale` / `empty` / `failed` if something's wrong). Counts by domain:

| Domain | scouted | sampled | landed | modeled | other |
|---|--:|--:|--:|--:|--:|
| open_data_portal | 234 | 1,158 | — | 11 | 1 empty |
| health_medicine | 27 | 66 | 1 | 39 | 3 stale |
| housing_social | 13 | 83 | — | 5 | — |
| education | 9 | 75 | — | 1 | 1 empty |
| economy_labor_trade | 26 | 67 | 1 | 12 | 1 empty, 1 failed |
| science_research | 66 | — | — | 7 | — |
| justice_courts | 52 | — | — | 15 | 2 empty |
| corporate_entities | 55 | 17 | 1 | 14 | 2 empty |
| transport_movement | 32 | 51 | — | 6 | 1 stale, 1 empty |
| government_power | 40 | 1 | — | 21 | 3 queued, 1 stale, 1 failed |
| money_in_politics | 39 | 1 | — | 16 | 3 queued |
| history_culture | 29 | — | — | 8 | — |
| procurement_intl | 27 | — | — | 1 | — |
| spending_budget | 28 | 7 | — | 13 | 1 failed, 1 queued |
| energy_environment | 24 | 24 | — | 13 | — |
| geo_demographics | 20 | 1 | — | 7 | — |
| money_finance | 18 | — | — | 11 | 1 stale |
| crime_security | 4 | 13 | — | 16 | — |
| sanctions_enforcement | 1 | — | 1 | 9 | — |
| immigration_migration | 1 | — | — | 9 | — |
| elections_voting | 4 | 1 | — | 4 | — |
| targeted_investigation | — | — | — | 3 | — |
| unclassified/uncategorized | — | 2 | 40 | 354 | 43 stale/empty/failed |

**Reading this:** ~1,400 sources are still `scouted` or `sampled` — found and
previewed, not yet built into a queryable table. The 589-table "shelf" is what's
`landed`/`modeled` today. The pipeline is the backlog; the spec below is what's live.

---

## 3. The 40 largest live tables (by row count)

| Table | Domain | Rows | Join-key tier |
|---|---|--:|---|
| DEA ARCOS (controlled-substance transactions) | health_medicine | 178,598,026 | STEEL |
| SEC 13F Holdings | — | 101,261,252 | STEEL |
| USASpending Prime Contract Awards (full re-pull) | — | 93,153,424 | STEEL |
| FEC Individual Contributions (itemized) | money_in_politics | 84,172,112 | STEEL |
| CourtListener Dockets | — | 71,677,647 | STRONG |
| NOAA AIS (vessel transponders) | transport_movement | 58,106,517 | STEEL |
| CFPB Consumer Complaints | money_finance | 34,348,075 | GEO |
| CMS Facility-Level Minimum Data Set Frequency | — | 31,403,215 | STEEL |
| FEMA Individual Assistance Housing Registrations | — | 26,250,920 | — |
| CMS Part D Prescribers (by Provider & Drug, DY2022) | health_medicine | 25,869,521 | STEEL |
| FDA FAERS (adverse-event drugs) | — | 20,914,284 | STEEL |
| FDA FAERS (adverse-event reactions) | — | 20,621,386 | STEEL |
| USASpending Contract Awards (FY07–26) | spending_budget | 20,000,000 | STEEL |
| USASpending Assistance Awards (FY07–26) | spending_budget | 19,902,879 | STEEL |
| CFPB HMDA Historic (mortgage applications) | — | 19,136,434 | — |
| CourtListener Citations | — | 18,123,788 | — |
| UK Companies House — Persons of Significant Control | — | 15,804,611 | — |
| EPA SDWA Violations & Enforcement | — | 15,432,737 | STEEL |
| CMS Open Payments — General Payments (PY2024) | health_medicine | 15,385,047 | STEEL |
| CMS Open Payments (PY2023) | health_medicine | 14,700,786 | STEEL |
| CMS Open Payments (PY2022) | health_medicine | 13,306,564 | STEEL |
| Canada Elections Contributions | — | 12,646,465 | — |
| EOIR Immigration Court Case Data | immigration_migration | 12,631,225 | NONE |
| CMS Medicare Dialysis Facilities | — | 12,456,456 | STEEL |
| FJC Integrated Database — Civil | — | 10,857,396 | — |
| EPA Air Emissions (combined) | — | 10,411,826 | STEEL |
| CourtListener × FJC IDB (linked) | — | 10,323,280 | — |
| CourtListener Opinion Clusters | — | 10,070,727 | — |
| FDA FAERS (indications) | — | 9,833,260 | STEEL |
| CPSC NEISS (consumer product injuries) | — | 9,794,977 | STEEL |
| CMS Medicare Physician/Other Practitioners (by Provider & Service) | — | 9,781,673 | STEEL |
| NPPES (National Provider registry) | health_medicine | 9,606,683 | STEEL |
| EPA NPDES Water Discharge Violation History | — | 7,951,656 | STEEL |
| FracFocus Registry | — | 7,200,550 | — |
| FJC Integrated Database — Bankruptcy | — | 6,965,441 | — |
| USGS Water Data APIs | energy_environment | 6,694,816 | GEO |
| CourtListener Parentheticals | — | 6,408,887 | — |
| USASpending Prime Contract Awards | spending_budget | 6,325,622 | STEEL |
| GLEIF Repex (global legal-entity relationships) | — | 6,313,372 | STEEL |

*(Note: a handful of sources appear twice under different names — a legacy
`FED_*` internal id and a human-readable registry name pointing at the same
physical table. Not double-counted in the 1.25B total; it's the registry
carrying two labels for one source, a known cleanup item.)*

Full 589-table list: `SELECT * FROM LIBRARY_META.REGISTRY.CATALOG WHERE LIFECYCLE IN ('modeled','landed')`.

---

## 4. The connection layer — what's actually wired together

Two separate edge tables, different confidence classes:

### `CONNECT_EDGES` — 4,512 edges (the trusted layer)

| Tier | Edges | What it means |
|---|--:|---|
| CORROBORATED | 2,513 | Name + ZIP agreement — softer than a hard ID, still structured, not free-text fuzzy match |
| STEEL | 1,345 | Exact match on a government-issued ID (NPI, EIN, CIK, CCN, FRS_ID, FEC IDs, PWSID, NPDES_ID, LEI, UEI, DUNS, etc.) — zero false-merge by design |
| BRIDGE | 512 | Crosswalk join across two different ID systems (CCN↔NPI, CIK↔EIN, EIN↔UEI) |
| GEO | 140 | Geographic key join (FIPS, ZIP) |
| STRONG | 2 | Near-STEEL, one step short of full ID confidence |

Top individual key types by edge count: `NAME@ZIP` (2,512), `CCN~NPI` bridge (373),
`EIN` (366), `NPI` (364), `FRS_ID` (136), `CIK` (128).

**429 distinct sources** currently touch at least one edge — meaning roughly
three-quarters of the 589 live tables aren't wired into the connection graph yet.
That's the real ceiling on cross-domain queries today.

### `CONNECT_EDGES_INC` — 3,182 edges (the exploratory/probabilistic layer)

Runs on-land immediately after a new source is loaded — mostly `NAME`-based
probabilistic matching (confidence-scored, e.g. `0.108`–`0.999`), used to surface
*candidate* crosswalks before a human decides whether to promote one to a real
`STEEL`/`BRIDGE` key. Not used for findings on its own.

---

## 5. Entity resolution

- **33,312,349 entities** resolved — one row per real-world person/org/vessel/facility,
  built by clustering on hard IDs — no name matching in the identity layer. Name+geo composites live only in the discover edge lane (CORROBORATED tier), never in ENTITY_MAP.
- Zero false-merge rule: two records only collapse into one entity if they share
  a government-issued identifier. Name-based candidates stay in the probabilistic
  layer (`CONNECT_EDGES_INC`) until a human promotes them.

---

## 6. Detection layer — the 8 live rules

| Rule | Active leads | Class |
|---|--:|---|
| osha_cohort_outlier_2024 | 16,215 | Statistical peer-cohort outlier scan |
| banned_but_paid | 773 | Hard-ID intersection (NPI) |
| debarred_but_funded | 344 | Hard-ID intersection (UEI/EIN) |
| excluded_but_billing | 236 | Hard-ID intersection (NPI) |
| sanctioned_vessel_broadcasting_v2 | 12 | Hard-ID intersection (IMO) |
| banned_but_operating | 11 | Hard-ID intersection |
| sanctioned_vessel_broadcasting (v1) | 4 | Hard-ID intersection (IMO), superseded by v2 |
| sec_filer_in_irs_bmf | 3 | Hard-ID intersection (CIK/EIN) |
| **Total** | **17,256** | — |

Everything here is pre-publish. `decisions.total = 0` — no human review has been
recorded yet in this warehouse snapshot; auto-publish is structurally blocked.

---

## 7. Stack

| Layer | Tech |
|---|---|
| Warehouse | Snowflake, 4 databases (raw landing / metadata-registry / staging / marts), X-Small auto-suspend warehouses |
| Transform | dbt — 1,378 models (975 staging, 399 marts, 4 intermediate) |
| Loading | Custom Python framework — checksummed, deduped, atomic, resumable |
| Portal discovery | Custom crawler/indexer — 3,283 sources registered, cataloged by ID type carried |
| Entity resolution | Custom graph-matching engine on normalized government IDs |
| Detection | 8 SQL rule sets, threshold-gated |
| Human review | Reading Room — 254 views recorded, gates every publish |

---

## 8. Known gaps (as of this pull)

- 429 of 589 live sources are wired into the edge graph — the rest need join-key
  work before they can be cross-referenced.
- `debarred_but_funded` jumped from 2 (pitch-deck era) to 344 active leads —
  worth a methodology check before quoting externally; could be a real
  detector improvement or a widened/loosened match.
- Two catalog entries can point at one physical table under different names
  (see §3 note) — cosmetic, not a row-count error, but worth a registry cleanup.
- `marts.stale_vs_landing: 36` — 36 mart tables are behind their landing source
  and due for a rebuild.

---

*Refresh command:*
```python
import connect.db as db
conn = db.connect()
db.rows(conn, "SELECT * FROM LIBRARY_META.REGISTRY.V_STATE")
```
