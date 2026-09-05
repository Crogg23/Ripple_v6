# Carbon-dating the Part B tables — 2026-09-05

Queries through the Python door, `connect/db.py`. Scripts: `scratchpad/hunt18.py`
… `hunt20.py`.

**Headline: the COVID test works. The Part B table is 2022 or later, which puts
every dollar in Miranda's row at least seven years after his 2015 exclusion.**

**The drug-vintage test does not work, and cannot. 90% of his drug money sits in
rows CMS suppressed. The seven drugs that survive suppression were all approved
decades before he was banned.**

---

## Two corrections to the query as written

| In the draft | Actual |
|---|---|
| `HCPCS_CODE` | **`HCPCS_CD`** |
| `TOT_MDCR_PYMT_AMT` | **`AVG_MDCR_PYMT_AMT`** — an average, no total column |

The service-level table publishes an average payment per service. Total payment
per line is `TOT_SRVCS × AVG_MDCR_PYMT_AMT`. Every dollar figure below is that
product, and is therefore an estimate, not a published total.

---

## 1. The COVID test — hit, hard

`FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVICE`,
9,781,673 rows.

| HCPCS | Description | Rows | Services |
|---|---|---|---|
| **91320** | SARS-CoV-2 vac 30mcg tris-sucrose IM | 36,811 | **4,506,697** |
| **91322** | SARS-CoV-2 vac 50mcg/0.5mL IM | 31,354 | **3,668,923** |
| 87635 | COVID-19 antigen, amplified DNA/RNA probe | 8,131 | 798,991 |
| 86769 | COVID-19 antibody measurement | 161 | 104,577 |
| U0002 | 2019-nCoV non-CDC, any technique | 1,034 | 89,238 |
| **91304** | COVID-19 vaccine, recombinant spike protein nanoparticle | 2,101 | 83,998 |
| M0201 | Vaccine administration inside a patient's home | 676 | 57,357 |
| 86328 | COVID-19 antibody, qualitative | 81 | 6,594 |
| 91321 | SARS-CoV-2 vac 25mcg/0.25mL IM | 19 | 368 |
| 91318 | SARS-CoV-2 vac 3mcg tris-sucrose IM | 10 | 203 |
| 91319 | SARS-CoV-2 vac 10mcg tris-sucrose IM | 2 | 47 |
| U0001 | CDC 2019-nCoV real-time RT-PCR panel | 3 | 245 |

### What a hit means

The two biggest are 8.2 million vaccine administrations between them. This is
not a handful of stray codes — it is a table describing a year in which COVID
vaccination was routine Medicare business.

The **tris-sucrose** formulations, `91318` through `91320`, and the pediatric
low-dose codes are the later-generation Pfizer products. `91304` is the
recombinant nanoparticle vaccine, the last of the three major platforms to reach
the US market. `M0201` is the in-home administration add-on created during the
vaccination campaign.

**Floor: the table is 2021 at the absolute earliest. The specific code mix says
2022.** Codes `91318`–`91322` and `91304` are all 2022-era additions.

### The upper bound, and what it rests on

The companion `FED_CMS_PARTD_PRESCRIBER_DRUG` is **DY2022**, proven from its
source filename. CMS publishes the Part D and Part B provider files on the same
annual cycle and usually the same release. That makes **DY2022 the strong
inference** for this table, with DY2023 the alternative.

**Not proven from inside the warehouse.** The registry row for this table carries
no `TEMPORAL_COVERAGE`, no source URL and no notes. Confirming DY2022 versus
DY2023 needs the CMS download page, which is outside this warehouse.

### Why the exact year does not change the verdict

| If the year is | Miranda excluded 2015-06-18 | Gap |
|---|---|---|
| 2021 | billing recorded | 6 years after |
| 2022 | billing recorded | 7 years after |
| 2023 | billing recorded | 8 years after |

**Every branch lands in the same place.** The vintage question is now closed for
the purpose it was opened for.

---

## 2. Miranda's HCPCS breakdown — and why the drug test fails

21 rows. Estimated total $223,658.

| HCPCS | Description | Drug? | Benes | Services | Est. payment |
|---|---|---|---|---|---|
| J0897 | Injection, denosumab, 1 mg | **Y** | 12 | 3,960 | $81,963 |
| 99214 | Established patient visit, moderate | N | 152 | 366 | $36,133 |
| 99213 | Established patient visit, low | N | 194 | 388 | $26,166 |
| 96413 | Chemotherapy into vein, 1 hour or less | N | 28 | 190 | $19,201 |
| J9217 | Leuprolide acetate depot, 7.5 mg | **Y** | 11 | 97 | $13,133 |
| J1750 | Injection, iron dextran, 50 mg | **Y** | 39 | 919 | $12,043 |
| 99204 | New patient visit, moderate | N | 62 | 62 | $7,911 |
| 96365 | IV infusion, 1 hour or less | N | 58 | 158 | $7,434 |
| 96367 | IV infusion, additional sequential | N | 58 | 269 | $6,038 |
| 96417 | Additional new drug into vein | N | 15 | 51 | $2,522 |
| 99233 | Subsequent hospital care, moderate | N | 16 | 21 | $2,049 |
| 96415 | Chemotherapy into vein, additional hour | N | 11 | 75 | $1,658 |
| 96402 | Hormonal anti-neoplastic, SC or IM | N | 14 | 55 | $1,498 |
| 99232 | Subsequent hospital care, moderate | N | 12 | 22 | $1,427 |
| 96366 | IV infusion, each additional hour | N | 37 | 79 | $1,269 |

### All seven of his visible drug codes

| HCPCS | Drug | Benes | Services | Est. payment |
|---|---|---|---|---|
| J0897 | Denosumab | 12 | 3,960 | $81,963 |
| J9217 | Leuprolide acetate | 11 | 97 | $13,133 |
| J1750 | Iron dextran | 39 | 919 | $12,043 |
| J3489 | Zoledronic acid | 13 | 154 | $695 |
| J2469 | Palonosetron HCl | 11 | 650 | $446 |
| J1100 | Dexamethasone sodium phosphate | 19 | 2,024 | $180 |
| J1200 | Diphenhydramine HCl | 50 | 200 | $130 |

**Total visible drug payment: $108,590.**

### The drug-vintage test cannot run, and here is exactly why

| Source | Drug payment |
|---|---|
| Provider-level table, `DRUG_MDCR_PYMT_AMT` | **$1,102,884.56** |
| Service-level table, all 7 drug rows | **$108,590** |
| **Missing** | **$994,295, or 90.2%** |

CMS suppresses any service-level row covering **fewer than 11 beneficiaries.**
Every one of Miranda's 21 surviving rows has 11 benes or more. That is not a
coincidence — it is the suppression threshold, visible in the data.

An oncologist giving a $20,000-a-dose targeted infusion to six patients produces
exactly the row CMS deletes. **The expensive drugs are structurally invisible in
the service-level file.**

The seven that survive are all high-volume, low-cost, given to many patients:

| Drug | US approval era |
|---|---|
| Diphenhydramine | 1940s |
| Dexamethasone | 1950s–60s |
| Iron dextran | 1950s–70s |
| Leuprolide acetate | 1985 |
| Zoledronic acid | 2001 |
| Palonosetron | 2003 |
| Denosumab | 2010 |

**Every one predates the 2015 exclusion by five years or more.** The "billing for
a drug invented after he lost his license" test returns nothing — not because it
is false, but because the file cannot answer it.

---

## The two Part B tables do not agree, and that is a trap

| Table | Rows for Miranda | Total services | Payment |
|---|---|---|---|
| Provider-level | 1 | **62,599** | **$1,229,994** |
| Service-level | 21 | **9,883** | **$223,658** |
| Gap | — | 52,716 services | $1,006,336 |

### Is it two vintages, or is it suppression?

Tested on five other NPIs with more than 5,000 services:

| NPI | Service-level | Provider-level | Gap |
|---|---|---|---|
| 1063122232 | 11,610 | 11,623 | 0.1% |
| 1396885935 | 7,750 | 7,754 | 0.1% |
| 1255315511 | 11,306 | 11,457 | 1.3% |
| 1285148346 | 6,713 | 6,741 | 0.4% |
| 1013998921 | 4,284,172 | 10,795,389 | **60.3%** |

Four of five agree within 1.3%. **The tables are the same vintage.** A vintage
mismatch would show a uniform gap, not four near-matches.

The gap is **suppression**, and it is wildly uneven. It is near zero for a
generalist seeing many patients per code, and 60–84% for a provider whose volume
concentrates in few-beneficiary lines.

Distinct NPI counts confirm it: **1,296,739** in the provider table,
**1,207,473** in the service table. 89,266 providers appear at provider level
with **every one** of their service lines suppressed.

### Read it as a rule

**The service-level table is not a breakdown of the provider-level table.** It is
a filtered subset. Summing it will understate any provider whose work is
concentrated, and the understatement is largest exactly where the money is
largest per patient.

Anyone building a "top billers by drug" analysis on the service table will
systematically miss high-cost, low-volume specialists.

---

## What this round proves

| Statement | Supported? |
|---|---|
| The Part B tables are 2021 or later | **yes, from COVID codes** |
| Most likely DY2022 | **strong inference, not proven** |
| Miranda's billing is post-exclusion under every candidate year | **yes** |
| The two Part B tables share one vintage | **yes, 4 of 5 NPIs within 1.3%** |
| 90% of his drug money is suppressed | **yes** |
| He billed for a post-2015 drug | **cannot be tested from this file** |
| $1.23M was paid during his exclusion | **yes, given the year floor** |

---

## Not checked

1. The CMS download page, to settle DY2022 versus DY2023. Outside the warehouse.
2. Whether `FED_CMS_NADAC` at 1.5M rows carries HCPCS effective dates. It is a
   drug pricing file and may allow a tighter carbon-date.
3. The 89,266 fully-suppressed providers. That population is worth its own pass.
4. Whether NPI 1013998921, the 60% gap case, is a lab or a billing aggregator.
5. Aswad in the service-level table. He has no provider-level row, so likely none.

## Cost

Three scripts, about 10 queries. Four scans of
`..._BY_PROVIDER_AND_SERVICE` at 9.78M rows, three of them full group-bys. No
prior run of this pattern in the query log to price against.
