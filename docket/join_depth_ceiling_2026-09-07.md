# How many layers a chain can hold — 2026-09-07

## The mechanic

A chain survives by multiplying its per-hop match rate.
Depth is not the constraint. The **kind** of key is.

```
hops   all steel   county FIPS   one cross-key hop anywhere
  2      96.0%        72.2%              8.8%
  4      92.2%        52.2%              8.5%
  6      88.6%        37.7%              8.1%
 10      81.7%        19.7%              7.5%
```

Read the third column again. A cross-key hop costs the same whether it is
hop two or hop nine. It caps the whole chain at a sample, forever.

| Key class | Rate | Chain rule |
|---|---|---|
| NPI, CCN, FRS_ID, PWSID, NPDES_ID, LEI, CL_PERSON_ID | 98–100% | chain freely |
| EIN, CIK, FEC ids | 86–100% | chain freely |
| FIPS | 73–100% | terminal only, never a pivot |
| UEI, DUNS | 10–80% | one hop, then stop |
| CIK~EIN, EIN~UEI, DUNS~UEI | 2–16% | sample, never a rate |
| NAME@ZIP | 8% | sample, multi-word names only |

The catalog's own bridge rule: only hard-key crosswalks are materialised.
`NPI, EIN, CIK, DUNS, CCN, IMO, MMSI, UEI, LEI`.
Code keys never bridge: `NAICS, SIC, NCES, DOCKET, PATENT, FIPS, ZIP`.

## The pivot tables that let a chain change key

A hop needs a table carrying **both** keys. These exist today.

| Bridge | Rows | Turns |
|---|---|---|
| `HEALTH__FED_CMS_FACILITY_AFFILIATION` | 2,260,193 | NPI ➔ CCN |
| `ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK` | 5,300,149 | FRS_ID ➔ corporate ID |
| `ECONOMICS__INTL_GLEIF_RELATIONSHIPS` | 485,285 | LEI ➔ parent LEI |
| `HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT` | 1,697,025 | payment profile ➔ NPI |
| `HEALTH__SAM_EXCLUDED_PROVIDERS` | 16,144 | SAM entity ➔ NPI |
| `HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES` | 19,038 | NPI ➔ CCN ➔ parent centre |
| `POLITICS__MEMBER_CROSSWALK` | 12,794 | BIOGUIDE ➔ a dozen id systems |
| `POLITICS__MEMBER_FEC_ID` | 1,715 | BIOGUIDE ➔ FEC_CAND_ID |
| `XWALK_ZCTA_COUNTY` | 46,960 | ZIP ➔ FIPS |
| `FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE` | 10,398 | CIK ➔ ticker |
| `HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF` | 5,399 | old lender id ➔ LEI |
| `HEALTH__FQHC_SITE_PEOPLE` | 239,265 | clinician ➔ site ➔ exclusion |

Twelve pivots. That is the real budget.

## What actually makes a chain impressive

Not table count. **Turns** — the number of times the chain changes what kind
of thing it is about. A stranger feels a turn. They do not feel a seventh join.

```
person ➔ facility ➔ company ➔ parent ➔ place ➔ population
   1        2          3        4        5        6
```

Six turns is the ceiling with today's bridges.

---

## Chain A — six turns, no cross-key hop, ~87% survival

**One doctor, all the way out to the county's death rate.**

```
LAYER  TABLE                                              KEY IN    KEY OUT
  1    HEALTH__FED_CMS_NPPES                              —         NPI
  2    HEALTH__FED_CMS_OPEN_PAYMENTS                      NPI       NPI
  3    HEALTH__FED_CMS_PART_D_PRESCRIBERS                 NPI       NPI
  4    HEALTH__FED_CMS_FACILITY_AFFILIATION      pivot    NPI       CCN
  5    HEALTH__FED_CMS_HOSPITAL_COMPARE                   CCN       CCN
  6    HEALTH__FED_CMS_HCRIS                              CCN       CCN
  7    XWALK_ZCTA_COUNTY                         pivot    ZIP       FIPS
  8    DIM_COUNTY                                         FIPS      FIPS
  9    HEALTH__FED_CDC_DRUG_POISONING_COUNTY              FIPS      —
 10    JUSTICE__XC_VERA_INCARCERATION_TRENDS              FIPS      —
```

The question it answers:
*Do the counties whose hospitals employ the most pharma-paid, highest-opioid
prescribers carry the highest overdose and jail rates?*

Turns: person ➔ facility ➔ place ➔ population. Four.
A hit means the money is traceable from one doctor's pocket to a county's morgue.
A miss means prescribing is national and the county effect washes out — also worth showing.

## Chain B — six turns, the corporate x-ray, ~85% survival

**One smokestack out to the global parent and back down to the workers.**

```
LAYER  TABLE                                              KEY IN    KEY OUT
  1    ENVIRONMENT__FED_EPA_FRS_FACILITIES                —         FRS_ID
  2    ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS         FRS_ID    FRS_ID
  3    ENVIRONMENT__FED_EPA_ECHO                          FRS_ID    FRS_ID
  4    ENVIRONMENT__FED_EPA_TRI_BASIC_2023                FRS_ID    FRS_ID
  5    ENVIRONMENT__FED_EPA_GHGRP_EMISSION                FRS_ID    FRS_ID
  6    ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK   pivot    FRS_ID    LEI
  7    ECONOMICS__INTL_GLEIF_RELATIONSHIPS       pivot    LEI       parent LEI
  8    ECONOMICS__INTL_GLEIF                              LEI       country
  9    XWALK_ZCTA_COUNTY                         pivot    ZIP       FIPS
 10    ECONOMICS__FED_BLS_QCEW                            FIPS      —
 11    HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY             FIPS      —
```

The question it answers:
*Which foreign-owned parent companies hold the most American pollution, and
what do the counties around those sites earn and die of?*

Turns: facility ➔ company ➔ parent ➔ country ➔ place ➔ population. Six. Ceiling.

## Chain C — the greedy one, where it breaks

Adding a stock layer forces `LEI ➔ CIK`, a cross-key hop.

```
  ...  ECONOMICS__INTL_GLEIF                              LEI       ?
  12   FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE    CIK       ticker      2–16%
  13   FINANCE__FED_SEC_13F_SUBMISSION                    CIK       holdings
```

Survival falls from 85% to roughly 8%. Everything upstream is still true,
but the finished number is a sample, not a rate. Build it as a named-example
panel — *here are nine parents we could resolve to a ticker* — never as a percentage.

## The rules that fall out

1. Steel keys chain as deep as you like. Ten hops still returns four rows in five.
2. FIPS is a destination, never a doorway. Aggregate there and stop.
3. One cross-key hop caps the whole chain at a sample. Spend it last, or not at all.
4. Twelve bridge tables exist. Every turn must land on one of them.
5. Six turns is today's ceiling. A seventh needs a bridge nobody has built.
