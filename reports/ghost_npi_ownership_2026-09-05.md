# Who owns the two ghost NPIs — 2026-09-05

Follow-up on `1285673012` and `1871571406`. All queries through the Python door,
`connect/db.py`. Scripts: `scratchpad/hunt13.py` … `hunt15.py`.

**Headline: nobody owns them. Both NPIs are individual sole practitioners with a
null `ORG_NAME`. There is no parent company, no group practice, no employer tax
ID. The corporate entity the investigator is looking for does not exist in the
data because there isn't one.**

**What is there instead is worse: Miranda is affiliated with four named Texas
hospitals, and CMS still lists him as authorized to order and refer across all
five program types.**

---

## The direct answer

| Question asked | Answer |
|---|---|
| Organization name | **none.** `ORG_NAME` is null on both |
| Group practice | **none.** Miranda's PAC ID has one member, himself |
| Clinic | **none recorded** as an enrolled entity |
| Tax ID | **not in the warehouse.** NPPES redacts EIN, 100% empty |
| Employer NPI | **none.** Both are `ENTITY_TYPE_CODE` 1, individual |
| PAC ID | **8022034875**, Miranda only. Aswad has none |

---

## Miranda, NPI 1285673012

### Identity, corroborated across four tables

| Source | Name | Address | City | State |
|---|---|---|---|---|
| `FED_HHS_OIG_LEIE` | MIRANDA, EDUARDO SIRIA | 8306 Estate Drive | Laredo | TX |
| `FED_CMS_NPPES` | MIRANDA, EDUARDO, M.D. | 2344 Laguna Del Mar Ct Ste 101 | Laredo | TX |
| `FED_CMS_OPEN_PAYMENTS_2022` | MIRANDA | 2344 Laguna Del Mar Ct Ste 104 | Laredo | TX |
| `FED_CMS_PARTD_PRESCRIBER_DRUG` | Miranda, Eduardo | — | Laredo | TX |

Same NPI, same city, same surname, and the LEIE address is a residential street
while the others are the same office building. **This is one person, not an NPI
collision.**

### Enrollment — a solo practitioner

`FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT` and
`FED_CMS_PECOS_PROVIDER_ENROLLMENT` agree exactly:

| Field | Value |
|---|---|
| `NPI` | 1285673012 |
| `PECOS_ASCT_CNTL_ID` | **8022034875** |
| `ENRLMT_ID` | **I20070525000116** |
| `PROVIDER_TYPE_CD` | 14-83 |
| `PROVIDER_TYPE_DESC` | PRACTITIONER - HEMATOLOGY/ONCOLOGY |
| `STATE_CD` | TX |
| `ORG_NAME` | **null** |
| `MULTIPLE_NPI_FLAG` | N |

The `ENRLMT_ID` prefix `I` means **individual**. The enrollment dates to
2007-05-25 by the ID's embedded date.

**Who else shares PAC ID 8022034875?** Queried directly. One row. Himself.
There is no group.

### The four hospitals — resolved by CCN

`FED_CMS_FACILITY_AFFILIATION` lists four hospital affiliations under
`IND_PAC_ID` 8022034875:

| CCN | Hospital | Legal name in `HOSPITAL_ENROLLMENTS` |
|---|---|---|
| 450643 | Doctors Hospital of Laredo | DOCTORS HOSPITAL OF LAREDO |
| 450092 | Fort Duncan Medical Center | **FORT DUNCAN MEDICAL CENTER, L.P.** |
| 451387 | Uvalde Memorial Hospital | **UVALDE COUNTY HOSPITAL AUTHORITY** |
| 451390 | Dimmit Regional Hospital | DIMMIT REGIONAL HOSPITAL DISTRICT |

Two of those four resolve to a different legal name than their trade name. Fort
Duncan is a limited partnership. Uvalde is a county hospital authority, a public
body.

**This is an affiliation, not ownership.** `FED_CMS_FACILITY_AFFILIATION` is the
table with `RELATION` = `asserted_affiliation` and a fanout to 6,962. It says a
practitioner has privileges or a relationship at a facility. It does not say the
facility employs him or bills for him.

### Still authorized to order and refer

`FED_CMS_ORDER_AND_REFERRING`, landed 2026-08-05:

| NPI | Name | PARTB | DME | HHA | PMD | HOSPICE |
|---|---|---|---|---|---|---|
| 1285673012 | MIRANDA, EDUARDO | **Y** | **Y** | **Y** | **Y** | **Y** |

Every flag is Y. That file is CMS's list of practitioners eligible to order or
refer for Medicare Part B, durable medical equipment, home health, prosthetics
and hospice.

**Excluded 2015-06-18. Still flagged Y on all five in a file landed 2026-08-05.**

Caveat, stated plainly: `_INGESTED_AT` is the **load** date, not the file's own
vintage. The table carries no publication date column. What is proven is that
the file as landed in August 2026 says Y. What is not proven is the exact CMS
publication date of that extract.

### The prescribing, and why the dollars are so high

$7,702,674 across 46 drugs and 1,334 claims in calendar 2022. That is $5,774 per
claim. The top eight:

| Brand | Generic | Claims | Cost |
|---|---|---|---|
| Ibrance | Palbociclib | 50 | $749,617 |
| Imbruvica | Ibrutinib | 51 | $722,465 |
| Xtandi | Enzalutamide | 47 | $675,915 |
| Kisqali | Ribociclib Succinate | 38 | $621,066 |
| Promacta | Eltrombopag Olamine | 44 | $606,183 |
| Tasigna | Nilotinib Hcl | 43 | $512,472 |
| Lenvima | Lenvatinib Mesylate | 22 | $496,402 |
| Jakafi | Ruxolitinib Phosphate | 23 | $374,649 |

Every one is an oral targeted cancer or blood-disorder drug. That matches the
HEMATOLOGY/ONCOLOGY enrollment exactly and explains the per-claim figure. These
are not volume prescriptions; they are a small number of very expensive ones.

### Industry was still calling

| Table | Payments | Total | Distinct manufacturers |
|---|---|---|---|
| `FED_CMS_OPEN_PAYMENTS_2022` | 225 | $4,415.57 | **45** |
| `FED_CMS_OPEN_PAYMENTS_2023` | 211 | $5,111.17 | **43** |
| `FED_CMS_OPEN_PAYMENTS` | 201 | $5,528.36 | **49** |

Small dollars, mostly food and beverage under $25. The number that matters is
**45 separate manufacturers in one year**, seven years after the exclusion.
Named payers include Astellas Pharma US, Amgen, and Sobi.

### The 18 tables he appears in

`FED_CMS_FACILITY_AFFILIATION`, `FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING`,
`FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFERRER`,
`FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT`,
`FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`,
`..._BY_PROVIDER_AND_SERVICE`, `FED_CMS_MEDICARE_PROVIDER`, `FED_CMS_NPPES`,
`FED_CMS_OPEN_PAYMENTS`, `_2022`, `_2023`, `_PROFILE_SUPPLEMENT`,
`FED_CMS_ORDER_AND_REFERRING`, `FED_CMS_PARTD_PRESCRIBER_DRUG`,
`FED_CMS_PART_D_PRESCRIBERS`, `FED_CMS_PECOS_PROVIDER_ENROLLMENT`,
`FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE`, `FED_HHS_OIG_LEIE`.

The DME-by-referrer table and the fiscal-intermediary attending table are both
untested here and both carry money.

---

## Aswad, NPI 1871571406

A much thinner trail. Seven tables, not eighteen.

| Source | Detail |
|---|---|
| `FED_HHS_OIG_LEIE` | ASWAD, MOHAMED BASEL. UPIN H95172. 2104 S Shelly Dr, Deming NM 88030. `1128a1`, excluded 2016-01-20 |
| `FED_CMS_NPPES` | ASWAD, MOHAMED, MD. 1020 S 8th St, Deming NM. Entity type 1 |
| `FED_CMS_PARTD_PRESCRIBER_DRUG` | 174 drugs, 9,940 claims, $2,552,958 |
| `FED_CMS_OPEN_PAYMENTS_2022` | 6 payments, $120.48, 4 manufacturers |
| `FED_CMS_OPEN_PAYMENTS_2023` | 1 payment, $200.00 |

### What is absent, and that absence is informative

| Table | Miranda | Aswad |
|---|---|---|
| FFS enrollment | yes | **no row** |
| PECOS enrollment | yes | **no row** |
| Facility affiliation | 4 hospitals | **no row** |
| Order and referring | Y on all five | **no row** |
| PAC ID | 8022034875 | **none** |

Aswad has **no Medicare enrollment record at all**. He is not enrolled, not
affiliated with any facility, and not authorized to order or refer — yet
`FED_CMS_PARTD_PRESCRIBER_DRUG` credits him with $2.55M in 2022 Part D drug cost.

Part D prescribing does not require Medicare enrollment the way billing does, so
this is not impossible on its face. It does mean **there is no corporate entity
to find for Aswad. There is no enrollment record to attach one to.**

---

## What the tables support, and what they do not

| Statement | Supported? |
|---|---|
| Both NPIs are individuals, not organizations | **yes** |
| No parent company or group practice is recorded | **yes** |
| Miranda has four named hospital affiliations | **yes** |
| Miranda is flagged Y to order and refer, as landed 2026-08-05 | **yes** |
| Part D recorded $10.3M combined under two excluded NPIs in 2022 | **yes** |
| A hospital or company was cashing the checks | **not shown** |
| Either person personally wrote these prescriptions | **not shown** |
| Fraud | **not shown** |

An NPI is a number. Part D reports the prescriber NPI on the claim; it does not
report who typed it. A practice billing under a departed or excluded doctor's
NPI produces exactly this data shape, and so does an excluded doctor still
practicing. **These tables cannot separate those two.**

The claim that Miranda was convicted in 2013 of black-market drug fraud came
from the investigator. It is **not** verified in this warehouse. What the
warehouse shows is `EXCLTYPE` `1128a1`, the mandatory exclusion for conviction of
a program-related crime, dated 2015-06-18.

---

## Specialty discrepancy, unresolved

| Source | Miranda's specialty |
|---|---|
| `FED_HHS_OIG_LEIE` | INTERNAL MEDICINE |
| `FED_CMS_PECOS_PROVIDER_ENROLLMENT` | PRACTITIONER - HEMATOLOGY/ONCOLOGY |
| `FED_CMS_PARTD_PRESCRIBER_DRUG` | INTERNAL MEDICINE |

The drugs are unambiguously oncology. LEIE specialty is recorded once, at
exclusion, and is coarse. Not a contradiction, but it is unexplained and should
be closed before publication.

---

## Not checked

1. `FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFERRER` for
   Miranda. It carries money and he is in it.
2. `FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING`, same.
3. `FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`, which holds
   Part B billing, not prescribing. That is the "cashing the checks" table.
4. The true publication vintage of `FED_CMS_ORDER_AND_REFERRING`. Only the load
   date is known.
5. Whether either hospital's own `HOSPITAL_ENROLLMENTS` row names an owner that
   appears elsewhere in the warehouse.
6. Whether Aswad appears in any state medical board or NPDB table.

## Cost

Three scripts, about 14 queries, all filtered to two NPIs or four CCNs. The
largest scan was `FED_CMS_PARTD_PRESCRIBER_DRUG` at 25.9M rows, filtered. No
prior run of this pattern in the query log to price against.
