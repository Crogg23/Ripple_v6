# Warehouse topographical map — 2026-09-05

Built for a lead investigator coming in cold. Structure and counts in sections
1–4 are live `INFORMATION_SCHEMA` queries run 2026-09-05 through the Python door
(`connect/db.py`). Scripts: `scratchpad/topo.py` … `topo5.py`, `fix1.py`.

**Section 5 is different.** The traps are carried from `.claude/traps.md`, dated
where known, and were *not* re-measured today except where marked "measured
2026-09-05." Treat them as leads to re-verify, not as fresh counts.

Revised 2026-09-05 after a skeptic pass. Nine numbers were wrong on the first
draft and are corrected below; the corrections are listed at the end.

One correction to the brief up front: there is no clinical schema here. This is
US/UK **public-records** data — companies, providers, facilities, money,
violations, courts. Provider-level Medicare and Open Payments data is the closest
thing to "clinical," and it is billing and payment records, not patient records.

---

## 1. The five databases

| Database | Role | Tables | Rows |
|---|---|---|---|
| `LIBRARY_RAW` | landed source files, one table per load | 2,214 | 1,370,379,039 |
| `LIBRARY_MARTS` | curated, analysis-ready, by subject | 676 | 908,247,190 |
| `LIBRARY_META` | the join layer and the registry | 60 | 1.13B |
| `LIBRARY_STAGING` | dbt views over raw | 3,600 views | — |
| `THE_LIBRARY` | the public-facing view shelf | 254 views | — |

`LIBRARY_RAW.LANDING` is the floor: **2,209 base tables, 96.6 GB,
1,349,549,819 rows.** `LIBRARY_RAW.RETIRED` holds 5 dead tables, 20,829,220 rows.

### `LIBRARY_MARTS` schemas — the subject shelf

| Schema | Tables | Rows | Schema | Tables | Rows |
|---|---|---|---|---|---|
| HEALTH | 98 | 363.2M | ENVIRONMENT | 75 | 107.7M |
| FINANCE | 56 | 102.1M | JUSTICE | 65 | 57.9M |
| MARITIME | 1 | 58.1M | HOUSING | 18 | 45.8M |
| ECONOMICS | 44 | 43.1M | CORPORATE_REGISTRY | 11 | 29.7M |
| POLITICS | 79 | 21.0M | IMMIGRATION | 15 | 19.9M |
| CONSUMER_PROTECTION | 1 | 17.2M | CONSUMER_SAFETY | 4 | 12.4M |
| REFERENCE | 34 | 8.4M | LABOR | 12 | 7.2M |
| EDUCATION | 17 | 4.6M | SCIENCE_RESEARCH | 6 | 2.5M |
| TRANSPORT | 12 | 2.2M | OPEN_DATA | 12 | 1.7M |
| TIMELINE | 32 + 403 views | 1.2M | ENERGY | 29 | 0.5M |

The 20 schemas above hold 621 of the 676 base tables. The remaining 55 sit in
~20 small schemas: PROCUREMENT at 355,977 rows, then EPSTEIN, INVESTIGATIONS,
HISTORY, GOVERNANCE, FOREIGN_INFLUENCE, CIVIL_RIGHTS, JUDICIARY and others, all
under 250k.

### `THE_LIBRARY` — 254 views, the front door

HEALTH 44 · GOVERNMENT 31 · JUSTICE 22 · CAMPAIGN_FINANCE 19 · COMPANIES 14 ·
ECONOMY 13 · ENERGY_ENVIRONMENT 12 · GOVERNMENT_SPENDING 11 · GEOGRAPHY 11 ·
CRIME_SECURITY 11 · HISTORY 8 · IMMIGRATION 8 · INVESTIGATIONS 7 · plus 13 more.

---

## 2. The biggest event tables in `LIBRARY_RAW.LANDING`

| Table | Rows | GB |
|---|---|---|
| FED_DEA_ARCOS_FULL | 178,598,026 | 6.22 |
| FED_SEC_13F_HOLDINGS | 101,261,252 | 1.78 |
| FED_USASPENDING_CONTRACTS_FULL_R2 | 93,153,424 | 9.69 |
| FED_FEC_INDIV_CONTRIBUTIONS | 84,172,112 | 2.82 |
| FED_COURTLISTENER_DOCKETS | 71,677,647 | 6.83 |
| FED_NOAA_AIS | 58,106,517 | 1.51 |
| FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | 31,403,215 | 0.82 |
| FED_FEC_COMMITTEE_TO_COMMITTEE | 28,558,310 | 0.63 |
| FED_FEMA_IA_HOUSING_REGISTRATIONS | 26,250,920 | 0.89 |
| FED_CMS_PARTD_PRESCRIBER_DRUG | 25,869,521 | 0.63 |
| FED_FDA_FAERS_DRUG | 20,914,284 | 0.19 |
| FED_USASPENDING_CONTRACTS_FULL | 20,000,000 | 6.00 |
| FED_USASPENDING_ASSISTANCE_FULL | 19,902,879 | 3.72 |
| FED_CFPB_HMDA_HISTORIC | 44,992,667 | reloaded all-records same day |
| FED_CFPB_COMPLAINTS | 17,179,788 | 1.30 |
| FED_EPA_CAMPD_EMISSIONS_DAILY | 16,513,971 | 0.38 |
| UK_COMPANIES_HOUSE_PSC | 15,804,612 | 1.48 |
| FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | 0.46 |
| FED_CMS_OPEN_PAYMENTS | 15,385,047 | 0.70 |
| FED_CMS_NPPES | 9,606,683 | 1.33 |

### Source families, by rows landed

| Family | Tables | Rows | Family | Tables | Rows |
|---|---|---|---|---|---|
| FED_DEA | 1 | 178.6M | FED_CMS | 52 | 154.5M |
| FED_USASPENDING | 9 | 144.2M | FED_COURTLISTENER | 28 | 119.9M |
| FED_FEC | 15 | 113.9M | FED_SEC | 27 | 113.6M |
| FED_EPA | 56 | 96.3M | FED_FDA | 23 | 74.6M |
| FED_NOAA | 3 | 59.9M | FED_CFPB | 6 | 38.6M |
| FED_FEMA | 3 | 26.3M | FED_FJC | 7 | 25.1M |
| UK_COMPANIES | 1 | 15.8M | FED_IRS | 12 | 14.1M |
| INTL_ELECTIONS | 1 | 12.6M | FED_EOIR | 1 | 12.6M |
| FED_DOL | 7 | 11.3M | INTL_GLEIF | 3 | 10.2M |
| PORTAL_CKA | 908 | 2.8M | FED_ITIS | 19 | 6.8M |

`PORTAL_CKA` is 908 small city/state open-data portal tables. 169 of them sit at
a 10,000-row API cap — counts on those are floors, not totals.

---

## 3. Column definitions — five core event tables

### `FED_DEA_ARCOS_FULL` — every opioid pill shipment, 2006–2014
45 columns, all `TEXT` except `_INGESTED_AT TIMESTAMP_NTZ`.

Seller: `REPORTER_DEA_NO`, `REPORTER_BUS_ACT`, `REPORTER_NAME`,
`REPORTER_ADDRESS1/2`, `REPORTER_CITY`, `REPORTER_STATE`, `REPORTER_ZIP`,
`REPORTER_COUNTY`, `REPORTER_FAMILY`.

Buyer: `BUYER_DEA_NO`, `BUYER_BUS_ACT`, `BUYER_NAME`, `BUYER_ADDRESS1/2`,
`BUYER_CITY`, `BUYER_STATE`, `BUYER_ZIP`, `BUYER_COUNTY`.

Transaction: `TRANSACTION_ID`, `TRANSACTION_CODE`, `TRANSACTION_DATE`,
`DRUG_CODE`, `NDC_NO`, `DRUG_NAME`, `PRODUCT_NAME`, `INGREDIENT_NAME`,
`QUANTITY`, `UNIT`, `MEASURE`, `STRENGTH`, `DOS_STR`, `DOSAGE_UNIT`,
`CALC_BASE_WT_IN_GM`, `MME_CONVERSION_FACTOR`, `ACTION_INDICATOR`,
`ORDER_FORM_NO`, `CORRECTION_NO`, `COMBINED_LABELER_NAME`,
`REVISED_COMPANY_NAME`.

Lineage: `_INGESTED_AT`, `_SOURCE_RUN_ID`, `_SRC_SHA256`.

**Trap:** `TRANSACTION_DATE` is `MMDDYYYY` text, and two rows hold floats.

### `FED_USASPENDING_CONTRACTS_FULL_R2` — federal contract actions, 2011–2026
39 columns, all `TEXT` except `_INGESTED_AT`.

Award: `CONTRACT_AWARD_UNIQUE_KEY`, `AWARD_ID_PIID`, `ACTION_DATE`,
`PERIOD_OF_PERFORMANCE_START_DATE`, `PERIOD_OF_PERFORMANCE_CURRENT_END_DATE`,
`AWARD_TYPE`, `LAST_MODIFIED_DATE`, `USASPENDING_PERMALINK`.

Money: `FEDERAL_ACTION_OBLIGATION`, `TOTAL_DOLLARS_OBLIGATED`,
`CURRENT_TOTAL_VALUE_OF_AWARD`.

Agency: `AWARDING_AGENCY_NAME`, `AWARDING_SUB_AGENCY_NAME`,
`FUNDING_AGENCY_NAME`.

Vendor: `RECIPIENT_UEI`, `RECIPIENT_DUNS`, `CAGE_CODE`, `RECIPIENT_NAME`,
`RECIPIENT_DOING_BUSINESS_AS_NAME`, `RECIPIENT_PARENT_UEI`,
`RECIPIENT_PARENT_NAME`, `RECIPIENT_CITY_NAME`, `RECIPIENT_STATE_CODE`,
`RECIPIENT_ZIP_4_CODE`, `RECIPIENT_COUNTRY_NAME`, `FOREIGN_OWNED`.

Work: `PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE`,
`PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME`, `NAICS_CODE`, `NAICS_DESCRIPTION`,
`PRODUCT_OR_SERVICE_CODE_DESCRIPTION`, `TRANSACTION_DESCRIPTION`.

People: `HIGHLY_COMPENSATED_OFFICER_1..2_NAME` and `_AMOUNT`.

**Trap:** `RECIPIENT_UEI` did not exist before April 2022. Pre-2022 matches on
UEI ride a backfilled DUNS→UEI map.

### `FED_FEC_INDIV_CONTRIBUTIONS` — individual campaign donations, thru 2026
24 columns, all `TEXT` except `INGESTED_AT NUMBER`.

`CMTE_ID`, `AMNDT_IND`, `RPT_TP`, `TRANSACTION_PGI`, `IMAGE_NUM`,
`TRANSACTION_TP`, `ENTITY_TP`, `NAME`, `CITY`, `STATE`, `ZIP_CODE`, `EMPLOYER`,
`OCCUPATION`, `TRANSACTION_DT`, `TRANSACTION_AMT`, `OTHER_ID`, `TRAN_ID`,
`FILE_NUM`, `MEMO_CD`, `MEMO_TEXT`, `SUB_ID`.

**Trap:** lineage columns here have **no leading underscore** — `INGESTED_AT`,
`SOURCE_RUN_ID`, `SRC_SHA256`. This is the majority form warehouse-wide, not the
exception — see trap 3. `INGESTED_AT` is a NUMBER holding epoch micros, so
`year()` throws.

**Trap:** sum with the sibling `itoth` table only after `MEMO_CD <> 'X'`.
93% of itoth is earmark memos and will double-count.

### `FED_CMS_PARTD_PRESCRIBER_DRUG` — Medicare Part D scripts by prescriber
25 columns, all `TEXT` except `_INGESTED_AT TIMESTAMP_NTZ`.
Column names are **mixed case**, unlike almost everything else here.

Prescriber: `Prscrbr_NPI`, `Prscrbr_Last_Org_Name`, `Prscrbr_First_Name`,
`Prscrbr_City`, `Prscrbr_State_Abrvtn`, `Prscrbr_State_FIPS`, `Prscrbr_Type`,
`Prscrbr_Type_Src`.

Drug: `Brnd_Name`, `Gnrc_Name`.

Volume: `Tot_Clms`, `Tot_30day_Fills`, `Tot_Day_Suply`, `Tot_Drug_Cst`,
`Tot_Benes`, and the 65-and-over mirror set `GE65_*` with suppression flags
`GE65_Sprsn_Flag` and `GE65_Bene_Sprsn_Flag`.

### `FED_CMS_OPEN_PAYMENTS` — industry payments to doctors
94 columns, all `TEXT` except `_INGESTED_AT NUMBER`.

Recipient: `NPI`, `COVERED_RECIPIENT_PROFILE_ID`, `COVERED_RECIPIENT_TYPE`,
first/middle/last/suffix names, full address block, `CCN`,
`TEACHING_HOSPITAL_ID`, `TEACHING_HOSPITAL_NAME`, six
`COVERED_RECIPIENT_PRIMARY_TYPE_n`, six `COVERED_RECIPIENT_SPECIALTY_n`, five
`COVERED_RECIPIENT_LICENSE_STATE_CODEn`.

Payer: `SUBMITTING_APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_NAME`, plus
`APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID/NAME/STATE/COUNTRY`.

Payment: `RECORD_ID`, `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `DATE_OF_PAYMENT`,
`NUMBER_OF_PAYMENTS_INCLUDED_IN_TOTAL_AMOUNT`,
`FORM_OF_PAYMENT_OR_TRANSFER_OF_VALUE`,
`NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`, travel city/state/country,
`PHYSICIAN_OWNERSHIP_INDICATOR`, `CHARITY_INDICATOR`, third-party indicators,
`DISPUTE_STATUS_FOR_PUBLICATION`, `DELAY_IN_PUBLICATION_INDICATOR`,
`PROGRAM_YEAR`, `PAYMENT_PUBLICATION_DATE`.

Product: five repeating blocks of
`COVERED_OR_NONCOVERED_INDICATOR_n`,
`INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_n`,
`PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_n`,
`NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_n`,
`ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_n`,
`ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_n`.

### The main dimension: `FED_CMS_NPPES` — 9.6M providers
`NPI`, `ENTITY_TYPE_CODE`, `REPLACEMENT_NPI`,
`EMPLOYER_IDENTIFICATION_NUMBER_EIN`,
`PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME`,
`PROVIDER_LAST_NAME_LEGAL_NAME`, `PROVIDER_FIRST_NAME`, `PROVIDER_MIDDLE_NAME`,
name prefix/suffix/credential, a full "other name" block, and mailing and
practice address blocks with city, state, postal code, phone, fax.

`ENTITY_TYPE_CODE` 1 = individual, 2 = organization.

---

## 4. Relationships — there are no foreign keys

Checked directly:

| Database | PRIMARY KEY constraints | FOREIGN KEY constraints |
|---|---|---|
| `LIBRARY_RAW` | 0 | 0 |
| `LIBRARY_MARTS` | 0 | 0 |
| `LIBRARY_META` | 5 | 0 |

Zero declared FKs warehouse-wide. That is by design — these are raw government
files, and Snowflake would not enforce a constraint anyway. **The join graph is a
materialized data structure, not a schema constraint.** It lives in
`LIBRARY_META."CONNECT"`.

> The schema name `CONNECT` is a reserved word. It **must** be double-quoted:
> `LIBRARY_META."CONNECT".KEYSET_LIVE`. Unquoted, it throws a syntax error.

### The join layer

| Table | Rows | What it is |
|---|---|---|
| `KEYSET_LIVE` | 290,557,744 | every (table, key type, value) seen — the discover book |
| `MATCH_PAIRS` | 187,054,143 | candidate pairs from blocking |
| `DISPLAY_KEYSET_LIVE` | 96,399,174 | the display slice, spec tables only |
| `ENTITY_INDEX` | 96,399,174 | key occurrence → entity |
| `CONNECT_NODES` | 96,399,174 | node per key occurrence |
| `ENTITY_GOLDEN` | 40,038,834 | one canonical row per resolved entity |
| `ENTITY_MAP` | 40,038,834 | key → entity id |
| `GOLD_PAIRS` | 6,538,936 | confirmed links |
| `ENTITY_XREF` | 2,672,384 | id-system crosswalk |
| `BRIDGE_ENTITIES` | 53,799 | hand-built bridges |
| `CONNECT_EDGES` | 4,512 | table-to-table edges |

That is the 11 that matter. `LIBRARY_META."CONNECT"` holds **27 base tables**
in all; the rest are config, watermarks, retired stubs and small lookup tables.

Column shapes differ between the two keysets, which is a live footgun:

- `KEYSET_LIVE` → `TABLE_NAME`, `KEY`, `VAL`
- `DISPLAY_KEYSET_LIVE` → `TABLE_NAME`, `KEY_TYPE`, `VAL`
- `ENTITY_GOLDEN` → `ENTITY_ID`, `ENTITY_TYPE`, `KEY_TYPE`, `KEY_VALUE`,
  `CANONICAL_NAME`, `NAME_NORM`, `CANONICAL_ADDR`, `NAME_SOURCE`, `RUN_ID`,
  `BUILT_AT`
- `CONNECT_NODES` → `NODE_ID`, `KEY_TYPE`, `KEY_VALUE`, `TABLE_NAME`, `RUN_ID`,
  `BUILT_AT`

### The linking keys, ranked — `KEYSET_LIVE`

| Key type | Occurrences | Distinct values | Tables |
|---|---|---|---|
| AWARD_KEY | 94,739,082 | 88,815,304 | 4 |
| NAME@ZIP | 48,250,806 | 28,588,137 | 122 |
| DOCKET | 35,044,169 | 28,946,314 | 17 |
| **NPI** | 31,481,346 | 9,608,817 | **34** |
| **FRS_ID** | 24,169,658 | 5,404,044 | **17** |
| COMPANY_NO | 16,560,637 | 10,977,911 | 2 |
| **EIN** | 9,424,337 | 3,412,085 | **34** |
| LEI | 6,582,190 | 3,409,553 | 7 |
| PECOS_ENRLMT_ID | 6,015,617 | 2,980,094 | 8 |
| PECOS_PAC_ID | 5,889,786 | 2,459,761 | 9 |
| NPDES_ID | 3,513,381 | 1,213,740 | 10 |
| PWSID | 2,844,162 | 434,042 | 10 |
| ZIP | 1,605,373 | 64,700 | 129 |
| UEI | 1,039,429 | 827,685 | 9 |
| DUNS | 1,027,791 | 963,834 | 5 |
| CAGE | 339,362 | 246,834 | 2 |
| CCN | 263,696 | 82,134 | 25 |
| CIK | 260,690 | 181,245 | 19 |
| NAME | 198,080 | 151,667 | 23 |
| FEC_CMTE_ID | 161,583 | 45,294 | 10 |
| DEA_NO | 148,588 | 148,588 | 1 |
| MINE_ID | 136,672 | 91,906 | 3 |
| ADDRESS | 110,858 | 104,346 | 12 |
| FEC_CAND_ID | 96,858 | 23,213 | 9 |
| NAICS | 95,680 | 77,780 | 16 |
| NAME@FIPS | 74,512 | 71,437 | 4 |
| CL_PERSON_ID | 61,200 | 16,232 | 8 |
| EIA_PLANT_ID | 56,387 | 16,300 | 10 |
| FIPS | 49,482 | 9,702 | 15 |
| FDIC_CERT | 47,315 | 27,839 | 3 |

The display slice adds a few more with real reach: `RSSD` 42,117 across 2 tables,
`BIOGUIDE` 27,160 across 5, `ICPSR` 13,316, `NCUA_CHARTER` 12,975,
`CL_COURT_ID` 9,879, `IMO` 9,323, `ICE_FACILITY` 7,502, `EIA_UTILITY_ID` 6,642.

### There is no single primary key. There are four identity keys.

**Reach** means the number of tables the key appears in. Volume does not pick a
join key — `AWARD_KEY` has 94.7M rows but sits in only 4 tables, so it is an
award line item, not a bridge.

Reach alone does not pick one either, and the first draft of this report got that
wrong. By raw reach the top two are **`ZIP` at 129 tables** and **`NAME@ZIP` at
122**. Both are excluded here deliberately:

- `ZIP` is a **geography** key. It groups rows by place. It does not identify
  anything, so joining on it merges unrelated entities.
- `NAME@ZIP` is a **fuzzy** key, built by the resolver, not present in any source
  file. It is a blocking device for candidate generation. A single-word name
  match on it clears at only 8%; multi-word clears at 92%.
- `DOCKET` at 17 tables and `AWARD_KEY` at 4 are **event** keys. They identify a
  case or an award, not a party.

What is left are the **identity** keys — a value a real registrar assigned to a
real thing. Those are the bridges:

| Rank | Key | Entity | Discover reach | Wired reach | What it joins |
|---|---|---|---|---|---|
| 1 | **NPI** | provider | 34 tables | **59** | all health, provider-level |
| 2 | **EIN** | organization | 34 tables | **55** | nonprofits, employers, filers |
| 3 | **FRS_ID** | facility | 17 tables | **20** | every EPA program |
| 4 | **CCN** | facility | 25 tables | **38** | Medicare facilities |
| 5 | **UEI / DUNS** | vendor | 9 / 5 | 8 / 9 | contracting, sanctions |

**Discover reach** is the table count in `KEYSET_LIVE`, the discover book — every
key ever seen, wired or not. **Wired reach** is the count in
`DISPLAY_KEYSET_LIVE`, the display slice. Use the wired number when you need to
know a join will actually resolve; the discover number lists tables that may not
be joined yet.

**Not yet checked, and it matters:** reach is a table count, not proof of a
usable join. A column can be present and empty. `FED_FCC_LICENSING.EIN` is 100%
empty string across 1.69M rows and still registered as a key. Before trusting any
of these numbers, count distinct values on the specific table you plan to join.

Below those, keys are domain-local: `PWSID` for drinking water, `NPDES_ID` for
discharge permits, `MINE_ID` for mines, `CCN` for Medicare facilities,
`CIK` for SEC filers, `FEC_CMTE_ID` and `FEC_CAND_ID` for campaign finance,
`CL_PERSON_ID` and `DOCKET` for courts, `COMPANY_NO` for UK companies,
`LEI` for global legal entities, `IMO` for vessels.

### Resolved entities — `ENTITY_GOLDEN`, 40.0M rows

| Entity type | Anchor key | Count |
|---|---|---|
| organization | COMPANY_NO | 10,977,911 |
| provider | NPI | 9,608,832 |
| facility | FRS_ID | 5,404,078 |
| organization | EIN | 3,775,590 |
| organization | LEI | 3,409,553 |
| organization | PECOS_PAC_ID | 2,459,761 |
| facility | NPDES_ID | 1,214,130 |
| organization | DUNS | 964,134 |
| organization | UEI | 827,909 |
| facility | PWSID | 434,047 |
| organization | CAGE | 247,042 |
| organization | CIK | 181,305 |
| organization | DEA_NO | 149,244 |
| facility | MINE_ID | 91,906 |
| facility | CCN | 82,067 |
| organization | FEC_CMTE_ID | 46,536 |
| organization | FDIC_CERT | 27,839 |
| organization | RSSD | 26,815 |
| person | FEC_CAND_ID | 22,955 |
| person | CL_PERSON_ID | 16,232 |
| person | BIOGUIDE | 12,781 |
| person | ICPSR | 12,677 |
| vessel | IMO | 9,019 |

Five entity types: **organization, provider, facility, person, vessel.**

**Unresolved contradiction, flagged not fixed.** `ENTITY_GOLDEN` counts more
distinct values than `KEYSET_LIVE` does for three keys:

| Key | `KEYSET_LIVE` distinct | `ENTITY_GOLDEN` | Gap |
|---|---|---|---|
| EIN | 3,412,085 | 3,775,590 | +363,505 |
| FEC_CMTE_ID | 45,294 | 46,536 | +1,242 |
| DEA_NO | 148,588 | 149,244 | +656 |

If golden were derived purely from the live keyset it could not exceed it. Either
one of the two is stale from a different run, or golden pulls keys from a source
the keyset does not index. **Not diagnosed.** Anyone treating `KEYSET_LIVE` as the
complete key inventory should resolve this first.

Note the asymmetry. Organizations and facilities resolve well. **People barely
resolve at all** — only ~65k person entities across four ID systems, all of them
public figures with an assigned identifier. There is no general person resolver.

---

## 5. Traps the investigator must know before the first query

1. **Quote `"CONNECT"`.** It is a reserved word. Unquoted throws immediately.
2. **Everything is `TEXT`.** Dollars, dates, counts. Cast before you compare.
   `FED_HRSA_NPDB.PAYMENT` is a string with a leading `$`.
3. **The lineage column has two names and three types.** Measured 2026-09-05
   across `LIBRARY_RAW.LANDING`:

   | Column | Type | Tables |
   |---|---|---|
   | `INGESTED_AT` | TEXT | 1,563 |
   | `_INGESTED_AT` | NUMBER | 259 |
   | `INGESTED_AT` | NUMBER | 224 |
   | `_INGESTED_AT` | TIMESTAMP_NTZ | 122 |
   | `_INGESTED_AT` | TEXT | 40 |

   **The unprefixed `INGESTED_AT` is the majority — 1,787 tables against 421.**
   Writing `_INGESTED_AT` blind fails on 80% of the warehouse. `TIMESTAMP_NTZ` is
   the rare case, 122 of 2,209. On the 483 NUMBER tables the value is epoch
   micros and `year()` throws. Check the column before you use it, every time.
4. **The prefix does not follow the source family.** `FED_CMS_OPEN_PAYMENTS` and
   `FED_CMS_PARTD_PRESCRIBER_DRUG` both use `_INGESTED_AT`, but with different
   types — NUMBER on the first, TIMESTAMP_NTZ on the second.
   `FED_FEC_INDIV_CONTRIBUTIONS` uses the bare `INGESTED_AT`. Same warehouse,
   same loader era, three shapes.
5. **`FED_CMS_PARTD_PRESCRIBER_DRUG` is mixed case.** `Prscrbr_NPI`, not
   `PRSCRBR_NPI`.
6. **169 `PORTAL_CKA` tables sit at a 10,000-row API cap.** Counts on those are
   floors.
7. **Landing table name ≠ `UPPER(SOURCE_ID)`.** Joining the registry to landing
   on name alone fabricates orphans.
8. **Registry notes record last-written status, not current state.** Trust a
   `count(*)`, never a note.
9. **Coverage: count `DISPLAY_KEYSET_LIVE` rows.** `CONNECT_WATERMARK` will say
   a table is wired when the keyset says it is not.
10. **A column that looks like an ID is not an ID** until you have counted
    distinct values and looked at a sample.

### Tables that are structurally broken, not just messy

| Table | Rows | Problem |
|---|---|---|
| `FED_EOIR_CASE_DATA` | 12,631,225 | one column, tab-separated text, unparsed |
| `FED_NHTSA_COMPLAINTS` | 2,227,941 | headerless `C1..C54` |
| `FED_MSHA_VIOLATIONS` | 3,087,266 | every value carries literal double quotes |
| `FED_CFPB_HMDA_HISTORIC` | 19,136,434 | originations only, zero denials |
| `FED_FDA_FAERS_*` | 20,914,284 | ends 2014q2 |
| `FED_SBA_PPP` | 968,524 | 150k+ loans only |

For `FED_NHTSA_COMPLAINTS` the usable positions are: `C3` manufacturer,
`C4` make, `C5` model, `C6` model year, `C8` date `YYYYMMDD`, `C12` component.
110k rows have a blank date.

---

## 6. The four-line orientation for the lead investigator

1. Start in `THE_LIBRARY` views or `LIBRARY_MARTS`. Only drop to
   `LIBRARY_RAW.LANDING` when the mart does not have the column you need.
2. To connect two subjects, do not guess a join — query
   `LIBRARY_META."CONNECT".KEYSET_LIVE` for a key type both tables carry.
3. `NPI` and `EIN` are the widest identity bridges — 59 and 55 wired tables.
   `FRS_ID` is the environmental bridge at 20. Never join on `ZIP` or `NAME@ZIP`
   to establish identity, however wide their reach looks.
4. Cast everything. Assume every column is a string until proven otherwise.
5. Check the lineage column's name and type on the specific table. There are two
   names and three types across the warehouse, and no rule predicts which.

---

## Cost

About 12 `INFORMATION_SCHEMA` queries, which scan metadata and are effectively
free. Three group-bys over the join layer — `KEYSET_LIVE` at 290M rows,
`DISPLAY_KEYSET_LIVE` at 96M, `ENTITY_GOLDEN` at 40M. No prior run of this exact
pattern in the query log to price against.


---

## 7. Corrections applied after the skeptic pass

The first draft of this report, written earlier the same day, was wrong on the
following. All are fixed above.

| # | Claim in draft 1 | Measured | Where it came from |
|---|---|---|---|
| 1 | `_INGESTED_AT` is NUMBER on 11 tables | 483 tables | memory index, never queried |
| 2 | Only FEC drops the underscore | 1,787 tables drop it | inverted assumption |
| 3 | `LIBRARY_MARTS` has 589 tables | 676 | stale figure from an August report |
| 4 | `LIBRARY_MARTS` holds ~880M rows | 908,247,190 | rounded from the stale figure |
| 5 | `FED_CMS_OPEN_PAYMENTS` has 99 columns | 94 | eyeballed, not counted |
| 6 | `FED_NHTSA_COMPLAINTS` has 2.6M rows | 2,227,941 | recalled, not queried |
| 7 | `LANDING` has 2,208 tables, 96.2 GB | 2,209, 96.6 GB | rounding drift |
| 8 | PROCUREMENT is under 250k rows | 355,977 | miscategorised |
| 9 | The join layer is 11 tables | 27 base tables | only the big ones listed |

Two further corrections of reasoning, not arithmetic:

- **The reach ranking broke its own rule.** Draft 1 defined reach as the table
  count, then ranked NPI first at 34 while its own table showed `ZIP` at 129.
  Section 4 now separates identity keys from geography, fuzzy and event keys, and
  says why.
- **Draft 1 claimed every number was fresh.** The section 5 traps were carried
  from the trap log. The header now says so.

Still open, and deliberately not closed here:

1. The `ENTITY_GOLDEN` versus `KEYSET_LIVE` gap above.
2. Whether the identity keys are populated on the tables they reach. Reach is a
   table count. No distinct-value or null check was run per table.
3. The traps in section 5 that were carried forward. Each needs its own query
   before it is trusted.
