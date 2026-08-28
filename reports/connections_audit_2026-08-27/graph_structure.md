# Graph Structure Audit — 2026-08-27

Read-only audit of the entity graph in `LIBRARY_META."CONNECT"`. All SQL via the guarded read lane (`viz.sqlrun`). Snapshot: 35,951,018 entities (ENTITY_GOLDEN / ENTITY_MAP), 90,004,885 entity-index rows (ENTITY_INDEX = one row per entity x source table x key).

## 1. Schema / how the graph is structured

- **Entities** are hard-key spine entities: one entity per (KEY_TYPE, KEY_VALUE) — EIN, NPI, FRS_ID, LEI, CCN, UEI, CIK, COMPANY_NO, etc. Spine v1 never fuses across different key TYPES (per `connect/entity_index_specs.py` / `spine.py` docstrings), so an entity can never blob across ID systems by construction.
- **ENTITY_INDEX** (90.0M rows): entity_id, entity_type, key_type, key_value, source_table, display_label, display_norm, row_count, preview. Rows-per-entity = number of source tables the key appears in (one index row per source table, not per raw record — ROW_COUNT carries the raw record count).
- **Edges** live at the *table-pair family* level in **CONNECT_EDGES** (4,910 families; columns A, B, KEY, TIER, MATCHED, A_DISTINCT, B_DISTINCT, MATCH_RATE, CONFIDENCE, SAMPLE) plus **CONNECT_EDGES_INC** (3,182 incremental families, which also has a PROBABILISTIC tier). Row-level fuzzy identity links: **ENTITY_LINKS** (2,324). Tiers computed in `connect/keys.py` / `discover.py` (strongest-first; STEEL keys must be globally-unique IDs; false-STRONG gate documented in source ~"70% of the headline graph was false STRONG edges" before the collision-model gate).

## 2. Blob check — VERDICT: CLEAN

Rows per entity (ENTITY_INDEX rows = distinct source tables per entity):

| bucket | entities | index rows |
|---|---|---|
| 1 | 15,863,520 | 15,863,520 |
| 2–5 | 17,152,163 | 46,607,502 |
| 6–20 | 2,935,335 | 27,533,863 |
| 21–100 | 0 | 0 |
| 100+ | 0 | 0 |

**The largest entity in the whole graph spans 20 source tables.** No mega-blobs exist structurally — an entity is one hard key value, and the ceiling (20) is simply the number of spine tables carrying that key type.

Top 20 largest: #1 Caterpillar Inc (EIN, 20 tables, 3 name variants), #2 Target (EIN, 19 tables, 4 name variants), then 18 individual NPI providers in 18–19 tables each, all with consistent names (2–3 case-variant spellings only). **No false merges visible in the top 20.**

Placeholder-key trap (the CVS+SK-Telecom class): checked NULL/blank/'nan'/'none'/'n/a'/'unknown'/all-zeros/all-nines key values across all 90M index rows. Total hits: **23 rows**, all CL_PERSON_ID / ICPSR values like '9', '99', '999', '9999', '000' (court/legislator sequence IDs where small integers may be legitimate but 999-style values are suspect — worst case glues 2 names into one entity, 5 rows). No placeholder EINs, NPIs, UEIs, or LEIs survive in the index. The prior placeholder-EIN bug does not reproduce in the current build.

## 3. Singleton rate

**15,863,520 / 35,951,018 = 44.1% of entities appear in exactly one source table** (unconnected within their key axis). By type/key (top axes):

| type | key | entities | % singleton |
|---|---|---|---|
| organization | COMPANY_NO | 10.98M | 49.1 |
| provider | NPI | 9.61M | 66.6 |
| facility | FRS_ID | 5.40M | 36.6 |
| organization | EIN | 3.41M | 6.1 |
| organization | LEI | 3.41M | 7.8 |
| facility | NPDES_ID | 1.21M | 35.6 |
| organization | UEI | 0.83M | 88.5 |
| facility | PWSID | 0.43M | 0.0 |
| organization | CIK | 0.18M | 91.7 |
| organization | DEA_NO | 0.15M | **100.0** |
| facility | MINE_ID | 92k | 65.8 |
| facility | CCN | 82k | 27.8 |
| person | ICPSR | 12.7k | 95.0 |
| vessel | IMO | 9.0k | 96.6 |

Notable: **DEA_NO is 100% singleton** (a whole key axis wired but connecting nothing — ARCOS-only), CIK 91.7%, UEI 88.5%, IMO 96.6%, ICPSR 95.0% are near-dead axes for cross-source connection; EIN/LEI (6–8%) are the workhorses.

## 4. Edge tiers — reconciliation

TIER labels live on **table-pair families**, not row edges. Family counts match the expected figures exactly; row-level edges = SUM(MATCHED):

| tier | families | row-level matched | meaning |
|---|---|---|---|
| STEEL | 1,386 | 206,719,075 | shared globally-unique hard ID (EIN 366 fams, NPI 358, FRS_ID 154, CIK 128, CCN 78, FEC ids 103, ...) |
| CORROBORATED | 2,670 | 39,525,705 | NAME@ZIP (2,666) / NAME@FIPS (4) — normalized name + geo cell |
| BRIDGE | 496 | 6,086,950 | cross-key crosswalks: CCN~NPI 357, CIK~EIN 85, EIN~UEI 52, DUNS~UEI 2 |
| GEO | 353 | 577,626 | shared FIPS (275) / GEO_IN point-in-polygon (52) / COUNTRY (18) / ZIP (8) |
| STRONG | 5 | 9,227 | DOCKET only |

CONNECT_EDGES_INC (incremental) adds a PROBABILISTIC tier: 545 families / 2.67M matched, plus its own STEEL 333 / CORROBORATED 1,162 / GEO 1,118 / STRONG 24.

## 5. Tier precision sample (25 families per tier, RANDOM(42), names pulled via ENTITY_INDEX where the key is a spine key, sample match values eyeballed otherwise)

### STEEL — measured precision ~95–100% (13 yes / 3 unsure / 0 no on name-comparable pairs)
Both-side name lookups for one sampled key value per family. Every comparable pair agreed (TAYLOR BRIAN=TAYLOR BRIAN, NEW MOUNTAIN FINANCE=same, FOXX Virginia=same, NEOSKYE INC=same, Evergreen Presbyterian=same, UGALDE DAMARA=same, Bel-Air Manor CCN=same, etc.). Unsure cases, all defensible:
- FRS 110001950470: "AMERICAN PRIDE SEAFOOD" vs "AMERICAN SEAFOODS INTERNATIONAL L.L.C." — same facility, related-but-renamed operator.
- EIN 140689340: "Metem, A GE Vernova Business" vs "GENERAL ELECTRIC CO" — same EIN, subsidiary-vs-parent filer. Correct as a taxpayer entity; watch this class if EIN edges are read as "same operating company."
- EIN 410706143: "FIRST CARE MEDICAL SERVICES" (IRS 990) vs "Essentia Health" (OSHA) — plausibly an affiliate filing under the shared EIN; unsure.
No outright false STEEL edge found in the sample.

### CORROBORATED (NAME@ZIP) — measured precision ~75–85% at match-value level
Most sampled values are multi-token org names + ZIP and clearly correct (MASSACHUSETTS EYE EAR INFIRMARY|02114, TENNESSEE VALLEY AUTHORITY|37402, TYSON FOODS|30040, FRESENIUS KIDNEY CARE SARALAND|36571 — yes). Clear failure classes in the sample:
- **Bare surnames + ZIP**: Part-D prescribers "EATON|42101", "KELLER|84106", "FREEMAN|40391" matched to EPA facility names — a person's surname colliding with a company name in the same ZIP. Judged NO.
- **Place-names-as-org-names**: HUD projects "ROCK SPRINGS|82901", "ALAMOSA|81101", "PUEBLO|81001" vs OSHA establishments — different entities that share a town name. Judged NO.
- Single-token generics ("HUFFMAN|22902", "CORNING|14831") — unsure-to-no.
Of 25 families, ~19 yes, ~3 clearly polluted, ~3 mixed/unsure. The name-normalizer's token-sorting also produces scrambled labels ("CENTER EYE MEDICAL SLEEPY" = Sleepy Eye Medical Center) — cosmetic, not a match error.

### BRIDGE — not same-entity edges by design; ~100% correct AS RELATIONSHIPS, ~0% as identity for CCN~NPI (357/496 families)
CCN~NPI links a facility to affiliated practitioners — match rates run 100–475% (fan-out, one CCN to many NPIs). These are affiliation edges, and correct as such. CIK~EIN and EIN~UEI families (139 fams) ARE identity crosswalks and the sampled values look sane (SEC DERA carries both IDs on one filing; NIH Reporter EIN→UEI). Verdict: precision question is category-dependent — do not count CCN~NPI in identity precision.

### GEO — never identity; and much of it is near-vacuous
FIPS families frequently match on **2-digit state codes** ("18","25","54") or COUNTRY codes ("GB","MX") — "Medicare DME referrers ↔ NOAA storm events share state 54" carries no entity meaning. FIPS values also mix formats within one key ("39083" vs "TX273" vs "18"). GEO_IN point-in-polygon (redlining-map overlays, WAPO fatal-force points) is genuinely useful spatial context. Same-real-world-entity precision: ~0% by construction; usefulness-as-context: FIPS-county/GEO_IN ok, state/COUNTRY-level families are noise.

### STRONG — 5 families, 3 of 5 are FALSE edge families (~40% family precision)
The entire STRONG tier is the DOCKET key:
- FED_FDIC_BANK_DATA ↔ FED_FDIC_SOD_BRANCH_DEPOSITS (7,905 matched, 73.2%): FDIC cert numbers, legitimate.
- FED_OYEZ ↔ FED_SCDB (22 matched): Supreme Court dockets, legitimate.
- **FED_FDIC_BANK_DATA ↔ FED_SCDB (820 matched), FED_FDIC_SOD_BRANCH_DEPOSITS ↔ FED_SCDB (476), FED_FDIC_BANK_DATA ↔ FED_OYEZ (4): FDIC certificate numbers colliding with Supreme Court docket numbers — pure numeric collision, FALSE.** ~1,300 of the tier's 9,227 row edges are garbage. DOCKET is not a globally unique key across issuers; it needs an issuer namespace. (3 DOCKET families also sit inside STEEL — same concern applies there.)

## 6. Ranked worst suspected false merges / false edges

1. **STRONG/DOCKET cross-domain collisions** — FDIC cert# ↔ SCOTUS docket, 3 families, ~1,300 row edges, confirmed false. Fix: namespace DOCKET per issuer or demote to same-source-family only.
2. **CORROBORATED bare-surname matches** — person-source names (Part-D prescribers) vs org names sharing a ZIP; systematic false class inside otherwise-good NAME@ZIP.
3. **CORROBORATED place-name orgs** — HUD/city-named establishments gluing to unrelated establishments in the same town.
4. **GEO state/COUNTRY-level families** — not false exactly, but meaningless edges inflating the family count (≥18 COUNTRY + many 2-digit-FIPS families).
5. **CL_PERSON_ID/ICPSR '999'-style values** — 23 index rows, tiny, worst case merges 2 names; worth a filter but not urgent.
6. **EIN parent/subsidiary conflation** — correct as tax entities, misleading if read as "same operating company" (GE Vernova↔GE class).

## 7. Bottom line

- **Blob verdict: clean.** Hard-key spine architecture makes CVS-class mega-merges structurally impossible; max entity = 20 sources; placeholder-key gluing reduced to 23 trivial rows.
- **Singleton rate: 44.1%** overall; DEA_NO (100%), IMO (96.6%), ICPSR (95%), CIK (91.7%), UEI (88.5%) are near-dead connection axes.
- **Tier precision (sampled): STEEL ~95–100%, CORROBORATED ~75–85%, BRIDGE = relationship edges (CCN~NPI) + good crosswalks (CIK~EIN/EIN~UEI), GEO = context not identity (with state/country noise), STRONG ~40% at family level (DOCKET collisions).**
