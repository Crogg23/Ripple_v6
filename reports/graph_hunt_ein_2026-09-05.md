# Graph hunt — heaviest entity intersections, 2026-09-05

Three queries requested by the lead investigator. All run through the Python
door, `connect/db.py`. Scripts: `scratchpad/hunt1.py` … `hunt4.py`.

**Headline: the ranking the investigator asked for is an artifact, twice over.
The top EINs are not the most-connected entities. They are the entities whose
source agency splits its files the most ways.**

---

## Q1. The graph schema

The requested query cannot run as written:

```sql
SELECT * FROM LIBRARY_META."CONNECT" LIMIT 5;   -- fails
```

`"CONNECT"` is a **schema**, not a table. It holds 27 base tables. The one that
answers "which entity touches which table" is `ENTITY_INDEX`, 96,399,174 rows.

### `ENTITY_INDEX` columns

| Column | Type | What it holds |
|---|---|---|
| `ENTITY_ID` | TEXT | `ENT_` + 16 hex, the resolved entity |
| `ENTITY_TYPE` | TEXT | organization, provider, facility, person, vessel |
| `KEY_TYPE` | TEXT | EIN, NPI, CCN, FRS_ID and the rest |
| `KEY_VALUE` | TEXT | the identifier itself |
| `SOURCE_TABLE` | TEXT | the landing table this sighting came from |
| `DOMAIN` | TEXT | subject bucket |
| `DISPLAY_LABEL` | TEXT | the name as that table spelled it |
| `ROW_COUNT` | NUMBER | rows behind this sighting |
| `PREVIEW` | OBJECT | small JSON, usually `{"place": ...}` |
| `DISPLAY_NORM` | TEXT | normalized name for matching |

### A sample row

```
ENTITY_ID      ENT_3ec465dff7945629
ENTITY_TYPE    provider
KEY_TYPE       NPI
KEY_VALUE      1881791945
SOURCE_TABLE   FED_CMS_NPPES
DOMAIN         health
DISPLAY_LABEL  STRELCHECK CHIROPRACTIC CLINIC LTD
ROW_COUNT      1
PREVIEW        { "place": "CRYSTAL LAKE IL 600144139" }
DISPLAY_NORM   STRELCHECK CHIROPRACTIC CLINIC LTD
```

### This is a node table, not an edge table

Each row is **one entity seen in one table**. There is no from/to. An "edge" in
the investigator's sense is two rows sharing an `ENTITY_ID`.

Table-to-table edges live separately in `CONNECT_EDGES`, 4,512 rows:

| Column | Holds |
|---|---|
| `A`, `B` | the two table names |
| `KEY` | the key type joining them |
| `A_COL`, `B_COL` | the actual column on each side |
| `TIER` | STEEL and other confidence tiers |
| `MATCHED` | rows that matched |
| `A_DISTINCT`, `B_DISTINCT` | distinct key values each side |
| `MATCH_RATE`, `CONFIDENCE` | measured overlap |
| `SAMPLE` | VARIANT, four sample key values |

A real edge row:

```
A            FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT
B            FED_CMS_NPPES
KEY          NPI
A_COL / B_COL  NPI / NPI
TIER         STEEL
MATCHED      2,540,936
A_DISTINCT   2,541,258
B_DISTINCT   9,606,683
MATCH_RATE   100.0
CONFIDENCE   1.0
```

Read that as: **every one of the 2.54M enrolled providers resolves in NPPES.**
The 9.6M denominator is NPPES holding providers who never enrolled in Medicare.

---

## Q2. Heaviest entities, as asked — the raw ranking

`group by ENTITY_ID, KEY_TYPE`, `count(distinct SOURCE_TABLE)`, over 96.4M rows.

| Entity | Key | Value | Tables | Domains |
|---|---|---|---|---|
| Caterpillar Inc. | EIN | 370602744 | 20 | 2 |
| Target Corporation | EIN | 410215170 | 20 | 2 |
| Kim, Christopher | NPI | 1457650442 | 19 | 2 |
| Farley, Chad | NPI | 1053500314 | 19 | 2 |
| Almony, Gregory | NPI | 1023003142 | 19 | 2 |
| Taylor, Jerald | NPI | 1083631659 | 19 | 2 |
| Ky, Paul | NPI | 1043374028 | 19 | 1 |
| PAUL JOSEPH MONTALBANO MD | NPI | 1699793661 | 19 | 1 |
| The Coca-Cola Company | EIN | 580628465 | 18 | 2 |
| Parker Hannifin Corporation | EIN | 340451060 | 18 | 2 |
| The J.M.Smucker Co. | EIN | 340538550 | 18 | 2 |
| Air Products and Chemicals | EIN | 231274455 | 18 | 2 |
| General Mills Inc | EIN | 410274440 | 18 | 2 |
| Lee, Joseph | NPI | 1437383924 | 18 | 2 |
| Robbins, Brett | NPI | 1023068426 | 18 | 2 |

### EINs only, top 15

| EIN | Name | Tables |
|---|---|---|
| 410215170 | Target Corporation | 20 |
| 370602744 | Caterpillar Inc. | 20 |
| 410274440 | General Mills Inc | 18 |
| 410417775 | 3M Company | 18 |
| 580628465 | The Coca-Cola Company | 18 |
| 250317820 | Howmet Aerospace Inc. | 18 |
| 362495346 | Darling Ingredients- Paducah | 18 |
| 910470860 | Weyerhaeuser Company | 18 |
| 910425694 | The Boeing Company | 18 |
| 440324630 | Leggett & Platt | 18 |
| 521893632 | Lockheed Martin Corporation | 18 |
| 340538550 | The J.M.Smucker Co. | 18 |
| 910351110 | Paccar | 18 |
| 250900168 | Kennametal Inc. | 18 |
| 133386776 | Lear Corporation | 18 |

**Do not act on this list.** Two things break it, below.

---

## Q3. The top 5 EINs, table by table — and why the ranking is fake

Caterpillar, EIN 370602744, all 20 tables:

| Domain | Tables |
|---|---|
| economics | `FED_SEC_DERA_SUB_` **2024Q1 … 2026Q1** — 9 tables |
| other | `FED_OSHA_ITA_300A_SUMMARY_` 2023, 2024, 2025 |
| other | `FED_OSHA_ITA_CASE_DETAIL_` 2023, 2024, 2025 |
| other | `FED_DOL_FORM5500_FULL`, `FED_DOL_EBSA_FORM5500_SCHEDULE_SB` |
| other | `FED_IRS_AUTO_REVOCATIONS`, `FED_IRS_REVOCATION` |
| other | `FED_PBGC_TRUSTEED_PENSION_PLANS` |

### Artifact #1 — the count is a file-splitting count

Nine of Caterpillar's 20 tables are **one SEC quarterly file landed nine times**,
once per quarter. Six more are **OSHA landed once per year**. Collapse the
year and quarter suffixes and the picture changes:

| Company | Raw tables | Distinct source systems |
|---|---|---|
| Caterpillar | 20 | **6** |
| Target | 20 | **7** |
| General Mills | 18 | **6** |
| 3M | 18 | **6** |
| Coca-Cola | 18 | **6** |

The six are the same six every time: SEC filer index, DOL Form 5500,
OSHA injury logs, IRS status, PBGC pensions, and for Target the IRS 527 group.

**This is not a discovery about Caterpillar. It is a discovery about the SEC,
which publishes quarterly.** Any large public company with a pension plan and a
factory lands in exactly these six systems.

### Artifact #2 — collapsing the siblings does not fix it either

Re-ranked on collapsed families, the top 15 becomes:

| EIN | Name | Families |
|---|---|---|
| 311674625 | Native American Cancer Research Corporation | 14 |
| 841537632 | Global Connection International | 14 |
| 840446259 | Valley View Hospital Association | 14 |
| 840765729 | Rocky Mountain Health Care Services | 14 |
| 840743432 | Clinica Campesina Family Health Services | 14 |
| 450233470 | Banner Health | 14 |
| 840404231 | University of Denver | 14 |
| 846044855 | STRiVE | 14 |
| 841493585 | The Colorado Nonprofit Development Center | 14 |
| 840404264 | Urban League of Metropolitan Denver | 14 |
| 742477108 | Metro Community Provider Network Inc. | 14 |
| 841182143 | Rocky Mountain Human Services | 14 |
| 840526620 | Imagine! | 13 |
| 840745911 | Safehouse Denver, Inc. | 13 |
| 840402701 | Jewish Family Service of Colorado Inc. | 13 |

**Every one is a Colorado nonprofit.** Colorado's open-data portal landed as
**ten separate `PORTAL_SOC_COLORADO_INFORMA_*` tables**, each a different grant
extract. A Denver charity therefore lands in ten tables that a Boeing does not.

The ranking measures **how many ways an entity's home agency splits its files**.
Nothing else.

---

## What EIN actually reaches — all 55 tables

Grouped by system, with distinct EINs in each:

| System | Tables | Peak distinct EINs |
|---|---|---|
| IRS exempt-org master and status | 8 | 1,983,563 in `FED_IRS_EO_BMF` |
| DOL Form 5500 pension filings | 2 | 466,444 |
| OSHA ITA injury logs | 6 | 123,206 |
| IRS 527 political groups | 5 | 58,915 |
| Federal single audit | 1 | 68,126 |
| PBGC trusteed pensions | 2 | 20,835 |
| SEC DERA filer index | 9 | 4,744 |
| State and city portals | 21 | 5,000 at the cap |
| CourtListener schools | 1 | 2,569 |

### The load-bearing finding for the hunt

**EIN reaches none of the tables the investigator named.**

| Asked for | Key it actually uses | EIN present? |
|---|---|---|
| Federal contracts | UEI, DUNS, CAGE | **no** |
| SEC 13F holdings | CIK | **no** |
| Court dockets | DOCKET, CL_PERSON_ID | **no** |
| Campaign donations | FEC_CMTE_ID, FEC_CAND_ID | **no** |

EIN is a **tax and employment** key. It touches the IRS, the DOL, OSHA, the
PBGC, and the SEC's filer index. It does not touch procurement, holdings,
litigation or campaign money. A contracts-to-donations chain on EIN returns zero
rows and looks like a clean negative result. It is not one.

To cross from a company's tax identity into its federal money you need a bridge:
EIN → name → UEI, or EIN → CIK through the SEC filer index. The second is the
only one of those two with a real identifier on both ends.

### DOMAIN is not usable for EIN

| Domain | Tables | Distinct EINs |
|---|---|---|
| other | 46 | 3,772,566 |
| economics | 9 | 5,483 |

51 of 55 tables sit in `other`. That is why every top entity shows exactly 2
domains — 2 is the ceiling, not a signal. **Do not rank on `DOMAIN`.**

---

## The honest version of the question

"Which entity touches the most tables" is the wrong question while the table
count is a file-splitting count. Three ways to ask it properly:

| Approach | What it measures | Cost |
|---|---|---|
| Collapse to source **system**, drop portals | real cross-agency breadth | one group-by |
| Rank by distinct **key types** per `ENTITY_ID` | entities with several identities | one group-by |
| Rank by distinct **domains**, after re-bucketing | cross-subject reach | needs a domain fix first |

The second is the strongest. An entity carrying both an EIN and a UEI, or both
an NPI and a DEA number, is genuinely bridged across systems. That is a property
of the entity, not of its agency's publishing habits.

---

## Not checked

1. Whether `ENTITY_ID` is stable across key types — one company holding an EIN
   and a UEI may sit under two `ENTITY_ID` values, not one.
2. Whether the Colorado portal tables are ten real extracts or one file landed
   ten times. Only the table names were read.
3. `ROW_COUNT` in `ENTITY_INDEX` was not used. Every top entity showed 1.
4. The 21 portal tables carrying EIN include several at the 10,000-row API cap.
   Their EIN counts are floors.

## Cost

Four scripts, roughly 10 queries. Three group-bys over `ENTITY_INDEX` at 96.4M
rows; the rest are metadata or filtered to a handful of EINs. No prior run of
this pattern in the query log to price against.
