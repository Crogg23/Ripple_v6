# Single Audit bridge + ghost doctor hunt — 2026-09-05

Two questions from the lead investigator. All queries through the Python door,
`connect/db.py`. Scripts: `scratchpad/hunt9.py` … `hunt12.py`.

**Headline: the Single Audit EIN ↔ UEI bridge is real and clean from 2022 on.
The ghost doctor hunt returns 554 NPIs at first pass and 2 after the vintage is
corrected. The other 552 were excluded after the prescribing data ends.**

---

## 1. The Single Audit bridge — alive

`FED_FAC_SINGLE_AUDIT`, 411,638 rows. Column names differ from the draft query:
`AUDITEE_EIN` and `AUDITEE_UEI`, not `EIN` and `UEI`. There is also an
`AUDITOR_EIN`, which is the accounting firm, not the audited body.

Validity tested by format, not by null. EIN as nine digits, UEI as twelve
alphanumerics.

| Measure | Count | Share |
|---|---|---|
| Total rows | 411,638 | — |
| Valid `AUDITEE_EIN` | 411,638 | **100%** |
| Valid `AUDITEE_UEI` | 178,295 | 43.3% |
| **Both valid on the same row** | **178,295** | **43.3%** |
| Distinct EIN + UEI pairs | 61,577 | — |

**Every row with a UEI also has an EIN.** The 43% is not a data-quality problem.

### Why 43% — the chain, not the label

| Audit year | Rows | With UEI | Share |
|---|---|---|---|
| 2026 | 227 | 227 | 100.0% |
| 2025 | 34,603 | 34,603 | 100.0% |
| 2024 | 46,260 | 46,260 | 100.0% |
| 2023 | 47,813 | 47,813 | 100.0% |
| 2022 | 48,116 | 48,115 | 100.0% |
| 2021 | 46,021 | 938 | 2.0% |
| 2020 | 40,241 | 238 | 0.6% |
| 2019 | 37,409 | 67 | 0.2% |
| 2018 | 37,039 | 21 | 0.1% |
| 2017 | 36,918 | 11 | 0.0% |
| 2016 | 36,991 | 2 | 0.0% |

UEI replaced DUNS in **April 2022**. The cutover is visible to the row. Audits
filed from 2022 forward carry a UEI at 100%. Audits before that carry one only
where a late amendment added it.

**A missing UEI on a 2019 audit is not a gap. The identifier did not exist.**

### Is one EIN one UEI?

| Distinct UEIs per EIN | EINs |
|---|---|
| 1 | 56,264 |
| 2 | 2,271 |
| 3 | 92 |
| 4 | 21 |
| 5 | 12 |
| 6 | 8 |
| 7 | 5 |
| 8 | 3 |
| 9 | 3 |
| 10 | 1 |

**58,680 EINs mapped. 95.9% map to exactly one UEI.** The 2,271 two-UEI cases
are the interesting ones — an organization that re-registered in SAM, or a parent
filing under subsidiaries.

### Verdict

This is a usable EIN → UEI crosswalk covering 58,680 organizations. It is the
only one in the warehouse. It reaches:

- `FED_USASPENDING_ASSISTANCE_FULL` on UEI, already a STEEL edge at 68.5%
- `FED_IRS_EO_BMF` and four other IRS tables on EIN, at ~49%

**That closes the EIN-to-money gap flagged two reports ago, for nonprofits and
grantees only.** It does not cover a for-profit contractor that never took
federal assistance, because such a body never files a Single Audit.

---

## 2. The ghost doctor hunt

### The LEIE table

`FED_HHS_OIG_LEIE`, 83,842 rows. Both requested columns exist.

| Column | Holds |
|---|---|
| `EXCLDATE` | exclusion start, `YYYYMMDD` text |
| `REINDATE` | reinstatement, `00000000` when never reinstated |
| `WAIVERDATE` | waiver, same placeholder |
| `EXCLTYPE` | statute cited, e.g. `1128a1` |
| `NPI` | `0000000000` when absent |
| `BUSNAME` | set for businesses, names blank |

### The coverage floor that caps this entire hunt

| Measure | Count | Share |
|---|---|---|
| Total exclusion rows | 83,842 | — |
| Rows with a real NPI | 8,841 | **10.5%** |
| Distinct real NPIs | 8,660 | — |
| Never reinstated | 83,842 | **100%** |

**Only one exclusion in ten carries an NPI.** The other 75,001 are nurses, aides,
business entities and older cases where OIG never recorded one. They cannot be
joined to billing data at all.

`REINDATE` is `00000000` on every single row. OIG publishes the currently
excluded list and drops people when they are reinstated, so the column is not a
filter — it is a constant. Filtering on it changes nothing.

### First pass — 554 NPIs, and why the number is wrong

Joining active-exclusion NPIs to `FED_CMS_PARTD_PRESCRIBER_DRUG` returns **554
distinct NPIs**. The top of that list runs to $10.7M in drug cost.

That number is not a finding. `FED_CMS_PARTD_PRESCRIBER_DRUG` has **no year
column**, and only one such table is landed. Its vintage comes from the registry:

```
NAME: CMS Medicare Part D Prescribers - by Provider and Drug (DY2022)
URL:  .../MUP_DPR_RY24_P04_V10_DY22_NPIBN.csv
```

`DY22` in the filename. **The prescribing data is calendar 2022.**

Bucketing the 554 against that:

| Exclusion timing | NPIs |
|---|---|
| Excluded **after** 2022 | 522 |
| Excluded **during** 2022 | 30 |
| Excluded **before** 2022 | **2** |

**522 of the 554 are not ghosts.** They prescribed in 2022 and were excluded in
2023, 2024, 2025 or 2026 — often *because* of what the prescribing shows. The
naive join reads the arrow backwards.

The 30 excluded during 2022 are ambiguous. Part D reports a full calendar year
with no dates, so prescribing before the exclusion and prescribing after it are
indistinguishable in this table.

### The two that survive

Excluded before 2022, never reinstated, still prescribing through calendar 2022:

| NPI | Excluded | Statute | Specialty | LEIE state | Part D name | Part D state | Drugs | Claims | Drug cost |
|---|---|---|---|---|---|---|---|---|---|
| 1285673012 | 2015-06-18 | 1128a1 | Internal Medicine | TX | Miranda, Eduardo | TX | 46 | 1,334 | **$7,702,674** |
| 1871571406 | 2016-01-20 | 1128a1 | Oncology | NM | Aswad, Mohamed | NM | 174 | 9,940 | **$2,552,958** |

**`1128a1` is the mandatory exclusion for conviction of a program-related
crime.** It is the most serious category on the list, not a technical lapse.

Both corroborate on two independent fields: the state matches between LEIE and
Part D, and the surname matches. That rules out a simple NPI transcription
error on one side.

Miranda: excluded **seven years** before the prescribing year, $7.7M in Part D
drug cost across 46 drugs on 1,334 claims. The cost-per-claim of ~$5,774 says
these are specialty or biologic drugs, not routine generics.

Aswad: excluded **six years** before, $2.55M across 174 drugs.

### What a hit means, and what it does not

| Reading | Supported? |
|---|---|
| Part D paid for scripts written under an excluded NPI | **yes, that is what the tables say** |
| The excluded person personally wrote them | **not shown** |
| Fraud | **not shown** |

An NPI is a number, not a person. A practice can keep billing under a departed
doctor's NPI, which is itself a known fraud pattern but a different one. The
next step is `FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT`, which
carries `NPI`, `ORG_NAME` and `PECOS_ASCT_CNTL_ID` — that says which organization
the NPI was enrolled under.

### Why the real number is a floor, not a total

Four separate reasons this hunt undercounts:

1. **90% of exclusions carry no NPI.** Unjoinable.
2. **One year of Part D is landed.** A doctor excluded in 2018 who billed in
   2019, 2020 and 2021 is invisible.
3. **Part D suppresses prescribers under 11 claims.** Small-volume ghosts vanish.
4. **Part D is prescriptions only.** Procedures, imaging and surgery billed by an
   excluded provider are in other CMS files, not tested here.

---

## Not checked

1. Whether the two NPIs are still active in NPPES, and under which organization.
2. Whether either NPI appears in `FED_CMS_OPEN_PAYMENTS` for 2022.
3. The 30 excluded-during-2022 cases. A month-level test needs a CMS file with
   service dates.
4. Whether `MULTIPLE_NPI_FLAG` in the enrollment table flags either NPI.
5. Whether the 2,271 two-UEI EINs are re-registrations or parent-subsidiary.

## Cost

Four scripts, about 12 queries. Three joins of the 8,660-row LEIE NPI set against
`FED_CMS_PARTD_PRESCRIBER_DRUG` at 25.9M rows, plus two full scans of
`FED_CMS_NPPES` at 9.6M and `FED_FAC_SINGLE_AUDIT` at 412k. No prior run of this
pattern in the query log to price against.
