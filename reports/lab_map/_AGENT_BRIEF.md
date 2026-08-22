# Agent brief — Laboratory ↔ Warehouse metadata mapping (2026-08-22)

**Everything below was measured live from Snowflake INFORMATION_SCHEMA today.
No data SELECTs were run. Do not run any either.**

## Where the evidence lives (all local CSV, read with grep/head/awk — do NOT query Snowflake)

| file | what it holds |
|---|---|
| `reports/lab_map/ALL_TABLES.csv` | every table/view in all 5 DBs: db, schema, table, type, row_count, bytes, created, last_altered, comment |
| `reports/lab_map/ALL_COLUMNS.csv` | all 162,750 columns: db, schema, table, column, ordinal, dtype, charlen, numprec, numscale, nullable, comment |
| `reports/lab_map/TABLE_SHAPES.csv` | one row per table, sorted biggest-first: n_cols, n_numeric, n_date, n_text, n_variant, and a `signals` field listing which shape-signals its column names matched |
| `reports/lab_map/signals/SIG_<name>.csv` | every column that matched one shape signal (lat, lon, geom, zip, fips, county, state, city, country, address, origin, dest, amount, count_meas, rate_meas, severity, entity_id, name_id, person, naics_sic, date_col, outcome, flag_bool, seq_order) |
| `reports/lab_map/signals/COMBO_<name>.csv` | tables satisfying a combined shape (e.g. POINT_GEO_latlon, OD_flow_origin_dest, MULTIVAR_numeric_ge20, GEO_plus_TIME), sorted by row count |
| `reports/lab_map/SHAPE_SUMMARY.json` | the counts for every signal and combo |

## Warehouse facts measured today

- **4,847 objects total** — 3,033 base tables + 1,814 views.
- By database: LIBRARY_RAW 2,218 · LIBRARY_STAGING 1,373 · LIBRARY_MARTS 1,123 · LIBRARY_META 133 · **LIBRARY_TOOLS is EMPTY (0 objects)**.
- Biggest schemas: `LIBRARY_RAW.LANDING` (2,212), `LIBRARY_STAGING.DBT_CROGERS` (1,350), `LIBRARY_MARTS.TIMELINE` (436 views — the canonical-clock layer built 2026-08-21).
- Domain marts: HEALTH 97, POLITICS 79, ENVIRONMENT 70, JUSTICE 65, FINANCE 57, ECONOMICS 41, REFERENCE 31, ENERGY 29, HOUSING 17, EDUCATION 17, IMMIGRATION 15, PUBLIC 14, FINDINGS 13, TRANSPORT 12, OPEN_DATA 12, LABOR 12, CORPORATE_REGISTRY 11, plus ~20 singleton schemas.
- **Duplicate/backup schemas exist and must never be cited as candidates**: `LIBRARY_META.CONNECT_BAK_20260730`, `LIBRARY_META.CONNECT_PRESPINE_20260730`, `LIBRARY_MARTS._RESTORE_20260731`, `LIBRARY_MARTS._RESTORE_20260701`, `LIBRARY_MARTS.UNCATEGORIZED`, `LIBRARY_META.REGISTRY.SOURCE_REGISTRY_BAK_20260729`.

## The graph layer (LIBRARY_META.CONNECT) — exact columns and row counts

| table | rows | columns |
|---|---:|---|
| `MATCH_PAIRS` | 181,002,484 | KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B, RUN_ID, BUILT_AT |
| `KEYSET_LIVE` | 176,983,257 | TABLE_NAME, KEY, VAL |
| `CONNECT_NODES` | 84,382,504 | NODE_ID, KEY_TYPE, KEY_VALUE, TABLE_NAME, RUN_ID, BUILT_AT |
| `ENTITY_INDEX` | 84,382,504 | ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, SOURCE_TABLE, DOMAIN, DISPLAY_LABEL, ROW_COUNT, PREVIEW(OBJECT), DISPLAY_NORM |
| `SPINE_KEYSET` / `SPINE_KEYSET_LIVE` | 84,382,504 | TABLE_NAME, KEY_TYPE, VAL |
| `ENTITY_GOLDEN` | 33,312,349 | ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, CANONICAL_NAME, NAME_NORM, CANONICAL_ADDR, NAME_SOURCE, RUN_ID, BUILT_AT |
| `ENTITY_MAP` | 33,312,349 | ENTITY_ID, KEY_TYPE, KEY_VALUE, ENTITY_TYPE, **MEMBER_TABLES(ARRAY)**, **SOURCE_COUNT(NUMBER)**, RUN_ID, BUILT_AT |
| `GOLD_PAIRS` | 6,538,936 | NPI, L_LAST, L_FIRST, R_LAST, R_FIRST, PLACE, LABEL(BOOLEAN), SCORE — a *labelled training set* for name matching, not a general edge list |
| `CROSSWALK_SCRATCH` | 2,692,258 | KEY_A, KEY_B, VAL_A, VAL_B, SRC |
| `ENTITY_XREF` | 2,672,384 | KEY_A, VALUE_A, KEY_B, VALUE_B, SOURCE_TABLE, **RELATION**, **FANOUT**, RUN_ID, BUILT_AT |
| `LEADS` | 17,598 | LEAD_ID, RULE_NAME, LEFT_ENTITY_ID, RIGHT_ENTITY_ID, LEFT_KEY_TYPE/VALUE, RIGHT_KEY_TYPE/VALUE, TITLE, SCORE, EVIDENCE(VARIANT), EVIDENCE_COUNT, FIRST_SEEN, LAST_SEEN, RUN_ID, STATUS, COMPILED_SQL, SQL_SHA256, AS_OF_DATE, SOURCE_SNAPSHOTS |
| `CONNECT_EDGES` | 4,910 | A, B, KEY, **TIER**, A_COL, B_COL, MATCHED, A_DISTINCT, B_DISTINCT, MATCH_RATE, CONFIDENCE, SAMPLE(VARIANT), RUN_ID, BUILT_AT — **this is a TABLE-to-TABLE edge list (a schema graph), not an entity-to-entity graph** |
| `CONNECT_EDGES_INC` | 3,182 | same shape, incremental |
| `ENTITY_LINKS` | 2,324 | LEFT_REF, RIGHT_REF, LEFT_SRC, RIGHT_SRC, METHOD, SCORE, BAND, NPI_MATCH, EVIDENCE, CREATED_AT |
| `CONNECT_WATERMARK` | 2,110 | (incremental bookkeeping) |
| `NICKNAME_MAP` | 102 | name-variant dictionary |
| `SOURCE_OVERLAP_MATRIX` | 36 | SOURCE_A, SOURCE_B, ENTITY_TYPE, KEY_TYPE, SHARED_ENTITIES |
| `CLUSTER_ASSIGNMENTS` | 23 | SOURCE_TABLE, CLUSTER_ID, CLUSTER_LABEL, DOMAIN |
| `DOMAIN_OVERLAP_MATRIX` | 7 | DOMAIN_A, DOMAIN_B, ENTITY_TYPE, TOTAL_SHARED_ENTITIES, SOURCE_PAIRS, MAX_PAIR_OVERLAP |
| `BRIDGE_ENTITIES` | **0 — empty** | |

`CONNECT_EDGES.TIER` values are documented in the table comment as
STEEL / STRONG (hard identifier) and GEO / CORROBORATED / PROBABILISTIC (softer).
Views `V_CONNECTIONS`, `V_CONNECTIONS_CORE`, `V_CONNECTION_SUMMARY`,
`V_LEADS_PUBLISHED` sit on top.

## Shape-signal counts measured today (number of distinct tables/views hit)

lat 805 · lon 810 · **lat AND lon together 801** · geom-ish name 1,212 · zip 1,303 ·
fips/tract/cbsa 742 · county 768 · state 1,583 · city 1,447 · country 522 ·
address 1,622 · amount 948 · count-measure 2,125 · rate-measure 1,108 ·
severity/grade/class 3,341 · hard entity id 1,393 · org name 2,833 · person 387 ·
naics/sic 916 · date-ish 3,517 · harm/outcome 504 · boolean flag 562 ·
sequence/order 490.

Combos: GEO+TIME 685 · GEO+MONEY 154 · GEO+OUTCOME 100 · ZIP+TIME 1,032 ·
ZIP+OUTCOME 148 · COUNTY+TIME 645 · ENTITY+TIME 1,152 · ENTITY+MONEY 357 ·
ENTITY+GEO 745 · ENTITY+OUTCOME 206 · origin&dest-ish 558 ·
≥8 numeric cols 261 · ≥20 numeric 81 · ≥50 numeric 30 · ≥50 cols 726 ·
≥150 cols 108 · ≥1M rows 252 · ≥10M rows 79.

**Caveat you must respect:** these are *column-name* matches only. The `origin`
signal is deliberately loose (it catches SOURCE_, PARENT_, PRIOR_) and
over-counts badly. `severity` is also loose. Treat any signal count as an upper
bound, and say so when it matters.

## Known audit findings you may cite (already documented in this repo — do not re-verify)

From `reports/pattern_sweep_2026-07-27.md`:
1. FEC contributions: a tiny donor cluster generates ~1/5 of all rows at $23 each.
2. **The OSHA inspection table was destroyed by a load and logged as success** — its staging view is broken because the raw table vanished (probable re-pull under a new name).
3. MSHA marts silently report zero mine deaths and zero serious violations.
4. EPA penalty column stamps one settlement onto hundreds of facilities — $2.3B of phantom fines.
5. SEC 13F mixes two currency scales in one column — off by ~1000x across eras.
6. **Three-quarters of the 62M-row FAERS drug-safety corpus is column-shifted with its join key destroyed.**
7. Federal debarment list is ≤9% loaded and its status flags are fabricated.
13. NHTSA investigations mart throws away 80% of raw records on a wrong dedup grain.
15. Six "included" sources are actually API sample stubs.

From `reports/mart_defect_verdicts_2026-08-10.md`: text-cast-to-number confirmed
and bigger than reported; positional column names confirmed for FEC; 18
suspected page caps confirmed as round numbers; 49 tables whose row counts
disagree with themselves.

From memory / prior sessions (treat as documented, flag as prior-session
findings not re-verified today): NPPES `EIN` and NOAA_AIS `imo_number` looked
fully populated but were sentinel-masked blanks; loaders wrote the string
`'nan'` instead of NULL into ~4.2M cells including a branch id and coordinates;
FAERS ~76% duplicated; contract tables carry epoch-date corruption from
`TRY_TO_DATE('YYYYMMDD')`.

## Census-grid facts (from `reports/census_grid_2026-08-12/SUMMARY.md`, built 2026-08-12, filled 2026-08-17)

- 1,765 modeled tables described as noun / event / link / code.
- 38 families, 278 distinct things, 52,235 grid cells; 30,509 fillable, 21,726 structural holes.
- Top families by model count: place 453 · unresolved 235 · facility 142 · organization 131 · measurement 82 · filing 73 · aggregate 56 · code 47 · case 44 · provider 40.
- Parking-lot tally (the ranked build roadmap): per person served 1,426 · inspection-first lineage 658 · harm join 658 · trend over time 616 · join to the entity spine 615 · assessed vs collected 160 · events per noun via hard ID 110.
- 674 models have no declared grain.

## Time layer facts (from `reports/time_index/`, built 2026-08-20/21)

- 482 tables classified for clocks; 2,089 column-level rulings in `clock_index.csv`.
- 46 tables have no clock at all; 74 have a reporting lag; 75 have a span (start+end).
- A canonical row clock is rolled out across **403 tables** as views — `LIBRARY_MARTS.TIMELINE` holds 436 views.
- `planned` (future-dated) timestamps are now separated out — 633 rows across ~20 tables.

## The Laboratory's own stale number

The Laboratory says "~12.88M entities across the 31 spine tables". Measured
today: `ENTITY_GOLDEN`/`ENTITY_MAP` hold **33,312,349** entities and
`ENTITY_INDEX`/`CONNECT_NODES` hold **84,382,504** rows. Say so.
