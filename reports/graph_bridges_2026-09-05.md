# Real bridges — multi-identifier entities and cross-agency edges, 2026-09-05

Two queries requested. Both run through the Python door, `connect/db.py`.
Scripts: `scratchpad/hunt5.py` … `hunt7.py`.

**Headline: Q1 returns zero rows, and that is the finding. `ENTITY_ID` carries
exactly one key type by construction — all 40,038,834 of them. The
multi-identifier idea I suggested last round does not live in `ENTITY_INDEX`. It
lives in `ENTITY_XREF`, and that table draws a line the investigator needs.**

---

## Q1. The true multi-identifier entities — zero results

The query ran as written. `HAVING COUNT(DISTINCT KEY_TYPE) > 1` matched nothing.

Walking the chain:

```sql
select n_keys, count(*) from (
  select ENTITY_ID, count(distinct KEY_TYPE) n_keys
  from LIBRARY_META."CONNECT".ENTITY_INDEX group by 1
) group by 1 order by 1;
```

```
n_keys   entities
     1   40,038,834
```

**One bucket. No entity anywhere carries a second key type.**

### What that means

`ENTITY_ID` is not a company or a person. It is a **key instance** — one
identifier value, resolved across the tables that carry it. Boeing's EIN and
Boeing's UEI are two different `ENTITY_ID`s. They are never merged in this table.

This closes the open question flagged at the end of the previous report, which
asked whether `ENTITY_ID` was stable across key types. It is not, and the answer
is unambiguous: 40.0M entities, 40.0M single-key buckets.

`ENTITY_MAP` confirms the same shape. Its `SOURCE_COUNT` counts **tables**, not
key types:

| SOURCE_COUNT | Entities |
|---|---|
| 20 | 2 |
| 19 | 6 |
| 18 | 1,401 |
| 17 | 54,331 |
| 16 | 147,578 |
| 15 | 159,318 |
| 10 | 180,392 |
| 6 | 786,874 |

That is the same file-splitting artifact from the last report, in a different
table. Do not rank on it either.

---

## Q1, done properly — `ENTITY_XREF`, 2,672,384 rows

This is the crosswalk. Each row asserts that value A under key A relates to
value B under key B, sourced from a named table.

| Column | Holds |
|---|---|
| `KEY_A`, `VALUE_A` | left identifier |
| `KEY_B`, `VALUE_B` | right identifier |
| `SOURCE_TABLE` | where the assertion came from |
| `RELATION` | `asserted_same_row` or `asserted_affiliation` |
| `FANOUT` | how many B values one A value reaches |

### The two relations are not the same thing, and mixing them will burn you

| Relation | Means | Fanout |
|---|---|---|
| `asserted_same_row` | **the same entity**, two ID systems | 1 |
| `asserted_affiliation` | **two entities that touch** | up to 6,962 |

A CCN and an NPI on the same enrollment row are one facility with two numbers.
A CCN and an NPI in `FED_CMS_FACILITY_AFFILIATION` are a hospital and a doctor
who works there. **Only the first is an identity bridge.**

### Every key pair in the crosswalk

| Pair | Relation | Source table | Rows | Distinct A | Distinct B | Max fanout |
|---|---|---|---|---|---|---|
| CCN → NPI | affiliation | `FED_CMS_FACILITY_AFFILIATION` | 2,249,953 | 38,104 | 940,206 | **6,962** |
| FEC_CAND_ID → FEC_CMTE_ID | affiliation | `FED_FEC_COMMITTEE_TO_CANDIDATE` | 191,201 | 2,804 | 6,222 | 821 |
| **FRS_ID → LEI** | **same row** | `XC_EPA_CORPORATE_CROSSWALK` | 73,948 | 73,948 | 22,736 | **1** |
| **CCN → NPI** | **same row** | `FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS` | 14,251 | 14,251 | 14,247 | **1** |
| BIOGUIDE → ICPSR | affiliation | `FED_VOTEVIEW_MEMBERS` | 12,655 | 12,584 | 12,655 | 3 |
| **BIOGUIDE → ICPSR** | **same row** | `FED_CONGRESS_LEGISLATORS` | 12,298 | 12,298 | 12,298 | **1** |
| FEC_CAND_ID → FEC_CMTE_ID | affiliation | `FED_FEC_BULK_LINKAGES` | 11,939 | 11,177 | 11,427 | 14 |
| **CCN → NPI** | **same row** | `FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS` | 11,413 | 11,413 | 11,372 | **1** |
| **CCN → NPI** | **same row** | `FED_CMS_FQHC_ENROLLMENTS` | 9,955 | 9,955 | 9,304 | **1** |
| FEC_CAND_ID → FEC_CMTE_ID | affiliation | `FED_FEC_BULK` | 8,221 | 7,746 | 8,221 | 4 |
| FEC_CAND_ID → FEC_CMTE_ID | affiliation | `FED_FEC_BULK_COMMITTEES` | 7,223 | 6,921 | 7,223 | 4 |
| IMO → MMSI | affiliation | `FED_NOAA_AIS` | 6,684 | 6,630 | 6,684 | 21 |
| **CCN → NPI** | **same row** | `FED_CMS_HOSPITAL_ENROLLMENTS` | 5,966 | 5,966 | 5,962 | **1** |
| CIK → EIN | affiliation | `FED_SEC_EDGAR_FINANCIALS` | 5,791 | 5,757 | 5,772 | 2 |
| **CIK → EIN** | **same row** | `FED_SEC_DERA_SUB_*` | ~4,200–4,800 each | same | same | **1** |
| **CCN → NPI** | **same row** | `FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS` | 5,313 | 5,313 | 5,132 | **1** |
| **CCN → NPI** | **same row** | `FED_CMS_HOSPICE_ENROLLMENTS` | 4,798 | 4,798 | 4,788 | **1** |

### The answer to "what are the top key combinations"

Only **six** distinct key pairs exist in the whole warehouse:

| Pair | Bridges | Identity or affiliation |
|---|---|---|
| CCN ↔ NPI | facility ↔ provider | both, in separate tables |
| CIK ↔ EIN | SEC filer ↔ tax ID | identity, fanout 1 |
| FRS_ID ↔ LEI | EPA facility ↔ global legal entity | identity, fanout 1 |
| BIOGUIDE ↔ ICPSR | two congressional ID systems | identity, fanout 1 |
| FEC_CAND_ID ↔ FEC_CMTE_ID | candidate ↔ committee | affiliation only |
| IMO ↔ MMSI | vessel hull ↔ radio call | affiliation, fanout 21 |

**There is no EIN ↔ UEI pair. There is no NPI ↔ DEA pair.** Both would be
obvious bridges and neither is built. The DEA number is in the warehouse on
149,244 entities and connects to nothing.

### The one bridge that reaches from health into corporate

`CIK ↔ EIN` at fanout 1 is the only path from a company's tax identity to its
SEC filings. About 4,700 companies per quarter. That is the bridge named at the
end of the last report, and it is real.

`FRS_ID ↔ LEI` at 73,948 rows and fanout 1 is the sleeper. It runs an EPA
facility straight to a global legal-entity ID, which then reaches 3.4M LEI
entities. **This is the strongest built bridge from the physical world into
corporate ownership.**

---

## Q2. Cross-agency STEEL edges

The query ran as written. First, the filter itself:

### The `SPLIT_PART(A,'_',2)` filter is leaky

`CONNECT_EDGES` tier distribution, with the investigator's filter applied:

| Tier | Edges | "Cross-agency" by the filter |
|---|---|---|
| CORROBORATED | 2,513 | 2,067 |
| STEEL | 1,345 | 402 |
| BRIDGE | 512 | 177 |
| GEO | 140 | 121 |
| STRONG | 2 | 1 |

Three of the top rows are **not** cross-agency. The filter reads the second
underscore segment, which is not always the agency:

| A | B | Filter sees | Truth |
|---|---|---|---|
| `INT_UK_COMPANIES_HOUSE` | `UK_COMPANIES_HOUSE_PSC` | UK vs COMPANIES | same registry |
| `IRS527_8871_ORGS` | `IRS527_DIRECTORS_OFFICERS` | 8871 vs DIRECTORS | same IRS file |
| `IRS527_8871_ORGS` | `IRS527_RELATED_ENTITIES` | 8871 vs RELATED | same IRS file |

Those are dropped below.

### The genuine cross-agency STEEL bridges, live right now

| A | B | Key | Matched | Rate |
|---|---|---|---|---|
| `FED_FAC_SINGLE_AUDIT` | `FED_USASPENDING_ASSISTANCE_FULL` | UEI | 40,746 | 68.5% |
| `FED_FAC_SINGLE_AUDIT` | `FED_IRS_990_EFILE_INDEX` | EIN | 33,683 | 49.4% |
| `FED_FAC_SINGLE_AUDIT` | `FED_IRS_BMF` | EIN | 33,429 | 49.1% |
| `FED_FAC_SINGLE_AUDIT` | `FED_IRS_EO_BMF` | EIN | 33,407 | 49.0% |
| `FED_FAC_SINGLE_AUDIT` | `FED_IRS_PUB78_ELIGIBLE_DONEES` | EIN | 30,159 | 44.3% |
| `INTL_GLEIF` | `XC_EPA_CORPORATE_CROSSWALK` | LEI | 22,743 | **100.0%** |
| `FED_DOL_EBSA_FORM5500_SCHEDULE_SB` | `FED_PBGC_TRUSTEED_PENSION_PLANS` | EIN | 18,989 | 91.1% |
| `INTL_GLEIF_REPEX` | `XC_EPA_CORPORATE_CROSSWALK` | LEI | 17,861 | 78.5% |
| `FED_CMS_NURSING_HOME` | `FED_NURSINGHOME411` | CCN | 14,431 | 99.9% |
| `FED_CMS_FACILITY_LEVEL_MDS_FREQUENCY` | `FED_NURSINGHOME411` | CCN | 14,426 | 99.9% |
| `FED_CMS_NURSING_HOME_DEFICIENCIES` | `FED_NURSINGHOME411` | CCN | 14,372 | 99.9% |
| `FED_CMS_SNF_ENROLLMENTS` | `FED_NURSINGHOME411` | CCN | 14,222 | 99.8% |
| `FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES` | `FED_NURSINGHOME411` | CCN | 13,676 | 99.9% |
| `FED_CMS_FACILITY_AFFILIATION` | `FED_NURSINGHOME411` | CCN | 13,110 | 90.7% |
| `FED_CONGRESS_LEGISLATORS` | `FED_VOTEVIEW_MEMBERS` | BIOGUIDE | 12,584 | **100.0%** |
| `FED_CONGRESS_LEGISLATORS` | `FED_VOTEVIEW_MEMBERS` | ICPSR | 12,298 | **100.0%** |
| `FED_NIH_REPORTER` | `FED_USASPENDING_ASSISTANCE_FULL` | DUNS | 9,748 | 65.3% |
| `FED_NIH_REPORTER` | `FED_USASPENDING_ASSISTANCE_FULL` | UEI | 9,454 | 79.4% |
| `FED_CMS_NPPES` | `FED_HHS_OIG_LEIE` | NPI | 8,660 | **100.0%** |
| `FED_PCAOB_FORM_AP_FILINGS` | `FED_SEC_EDGAR_FINANCIALS` | CIK | 8,082 | 99.6% |
| `FED_SBIR_STTR_AWARDS` | `FED_USASPENDING_ASSISTANCE_FULL` | UEI | 7,217 | 42.1% |
| `FED_SBIR_STTR_AWARDS` | `FED_USASPENDING_ASSISTANCE_FULL` | DUNS | 7,227 | 33.5% |
| `FED_PCAOB_FORM_AP_FILINGS` | `FED_SEC_EDGAR_COMPANY_TICKERS` | CIK | 7,206 | 89.9% |
| `FED_IRS_BMF` | `FED_OSHA_ITA_300A_SUMMARY_2023` | EIN | 7,446 | **6.0%** |
| `FED_IRS_EO_BMF` | `FED_OSHA_ITA_300A_SUMMARY_2023` | EIN | 7,444 | **6.0%** |
| `FED_IRS_990_EFILE_INDEX` | `FED_OSHA_ITA_300A_SUMMARY_2023` | EIN | 7,193 | 5.8% |

### Read the match rate, not the matched count

`MATCH_RATE` is the share of the smaller side that found a partner. It separates
a bridge you can walk from one you cannot.

| Rate | Reading |
|---|---|
| 100% | every row on the narrow side lands. Walk it. |
| 90–99% | near-complete. Losses are a vintage or a spelling. |
| 42–80% | real but partial. Absence proves nothing. |
| 6% | the join runs and returns almost nothing useful. |

The IRS ↔ OSHA edges at 6% are the trap on this list. They are tiered STEEL
because the key type is exact, but only one nonprofit in seventeen appears in
OSHA's injury log. **A nonprofit missing from an IRS↔OSHA join is almost
certainly a coverage gap, not a clean employer.**

### The four strongest, and what each one buys

| Bridge | Key | What it opens |
|---|---|---|
| `FED_CMS_NPPES` ↔ `FED_HHS_OIG_LEIE` | NPI | 8,660 providers **excluded from federal health programs**, tied to the full 9.6M registry at 100% |
| `INTL_GLEIF` ↔ `XC_EPA_CORPORATE_CROSSWALK` | LEI | polluting facilities to global corporate ownership, 100% |
| `FED_CONGRESS_LEGISLATORS` ↔ `FED_VOTEVIEW_MEMBERS` | BIOGUIDE | every member of Congress to their full voting record, 100% |
| `FED_FAC_SINGLE_AUDIT` ↔ `FED_USASPENDING_ASSISTANCE_FULL` | UEI | 40,746 federal grantees to their audit findings, 68.5% |

The NPPES ↔ LEIE edge is the one I would hunt first. A 100% rate on an
exclusion list means every excluded provider resolves to a name, address and
specialty. From there, `FED_CMS_PARTD_PRESCRIBER_DRUG` and
`FED_CMS_OPEN_PAYMENTS` both carry NPI.

---

## `BRIDGE_ENTITIES` — the hand-built shortlist, 53,799 rows

Separate table, already filtered to entities spanning more than one domain.

| Column | Holds |
|---|---|
| `ENTITY_ID`, `ENTITY_TYPE`, `DISPLAY_LABEL` | the entity |
| `DOMAIN_COUNT`, `DOMAINS` | subject buckets it spans |
| `SOURCE_COUNT`, `SOURCES` | tables it appears in |

Samples:

```
WHITE BIRD CLINIC          2 domains  5 sources
  spending_budget, corporate_entities
  FED_FAC_SINGLE_AUDIT, FED_IRS_BMF, FED_IRS_EO_BMF, FED_IRS_990_EFILE_INDEX

Toll Brothers, Inc.        2 domains  14 sources
  money_finance, corporate_entities
  FED_SEC_EDGAR_COMPANY_TICKERS, FED_SEC_EDGAR_FINANCIALS, FED_SEC_EDGAR_INSIDERS
```

Note `SOURCE_COUNT` 14 against three named sources. The array is truncated in
display, or the count includes tables not listed. **Not diagnosed.**

---

## Not checked

1. Whether `MATCH_RATE` is computed against the smaller or the larger side.
   Read here as the smaller side, from `A_DISTINCT` and `B_DISTINCT` on the
   sample rows. Not proven.
2. The 402 cross-agency STEEL edges below the top 25. Only the top were pulled.
3. Whether `XC_EPA_CORPORATE_CROSSWALK` is an authoritative EPA product or a
   third-party file. The `XC_` prefix suggests a crosswalk, not a source.
4. Whether the CCN ↔ NPI `asserted_same_row` rows across six enrollment tables
   agree with each other. Six tables assert the same pair type independently.
5. `BRIDGE_ENTITIES` `SOURCE_COUNT` versus the length of its `SOURCES` array.

## Cost

Three scripts, about 12 queries. Two group-bys over `ENTITY_INDEX` at 96.4M
rows, one over `ENTITY_XREF` at 2.7M, one over `ENTITY_MAP` at 40M. The rest are
small. No prior run of this pattern in the query log to price against.
