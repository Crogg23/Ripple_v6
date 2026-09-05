# Alexander Frank — a full investigation, 2026-09-05

NPI `1164450573`. All queries through the Python door, `connect/db.py`.
Scripts: `scratchpad/frank1.py` … `frank4.py`.

**Revised the same day after a skeptic pass. Four claims were wrong and are
corrected below; the corrections log is at the end. The headline survived
re-query. The antipsychotic finding got stronger, not weaker, and now rests on
two independent years and two independent methods.**

---

## Headline

A family-practice doctor whose entire practice is one 58-bed Oklahoma nursing
home, a hospice and a home health agency. He wrote the **9th largest Part D drug
bill of any family physician in America**. His antipsychotic share sits at the
**99th percentile of his own specialty in both years measured**. The nursing home
he serves was cited for **prescribing unnecessary drugs** and for **failing to
reduce psychotropics**. He was then excluded from federal health programs under
the patient-abuse statute.

**The order of events is the story. It runs forward, and every step is dated.**

---

## The man

| Field | Value |
|---|---|
| NPI | 1164450573 |
| Name | **FRANK, ALEXANDER FREDERICK**, M.D. |
| NPPES address | 5721 NW 132nd St, Oklahoma City, OK 73142 |
| LEIE address | 5500 Pershing Circle, Edmond, OK 73034 |
| Entity type | 1 — individual |
| Specialty | Family Practice |
| `IND_PAC_ID` | 4587624473 |
| **Excluded** | **2025-08-20** |
| **Statute** | **`1128a2`** |
| Reinstated | never |

Both addresses are Oklahoma, Edmond adjoining Oklahoma City. Middle name matches
across LEIE and NPPES — **FREDERICK** and **FREDRICK**, one letter apart.

> **`1128a2` is the mandatory exclusion for conviction of a criminal offense
> relating to neglect or abuse of patients.** That reading comes from the statute,
> not from the warehouse — the table stores only the code. **Confirm against the
> statute text before publishing.** It is load-bearing for everything below.

**He has no Medicare enrollment record.** Zero rows in FFS enrollment, PECOS, or
order-and-referring. He appears in 14 tables and is enrolled in none of them.

---

## Step 1 — the practice is three post-acute facilities, and nothing else

`FED_CMS_FACILITY_AFFILIATION`, three rows, all under `IND_PAC_ID` 4587624473:

| Facility type | CCN | Name |
|---|---|---|
| **Nursing home** | 375414 | **HASKELL CARE CENTER**, Haskell OK |
| Hospice | 371701 | Neighborhood Hospice, LLC |
| Home health agency | 377668 | Universal Rehab Services |

His Part B billing confirms the shape:

| Field | Value |
|---|---|
| `RNDRNG_PRVDR_ENT_CD` | I — individual |
| Address | 5721 NW 132nd St, Oklahoma City |
| `TOT_BENES` | 464 |
| `TOT_SRVCS` | 3,140 |
| `TOT_MDCR_PYMT_AMT` | **$207,303.28** |
| `DRUG_MDCR_PYMT_AMT` | **$0** |
| `MED_MDCR_PYMT_AMT` | $207,303.28 |
| `BENE_AVG_RISK_SCRE` | **1.9925** |

> **Vintage correction.** The first draft called this "2022-era." The registry row
> for `fed_cms_medicare_provider` says the landed release is **R26 P05 V10 D24,
> data year 2023**. Two caveats both ways: registry notes record last-written
> intent, not landed state, and `partb_carbon_date_2026-09-05.md` proved only a
> **2021-or-later floor** from COVID codes. **Treat the Part B figures as DY2023,
> not proven.**

**Zero drug payments in Part B.** Every dollar is professional services. Average
patient risk score 1.99, roughly twice the Medicare norm of 1.0 — a very sick
panel, consistent with nursing-home residents.

The service codes name the practice outright:

| HCPCS | What it is | Services | Est. paid |
|---|---|---|---|
| 99309 | Subsequent **nursing facility** care, moderate | 1,099 | $78,255 |
| 99349 | **Residence visit**, established patient | 762 | $59,464 |
| 99309 | Same, facility place of service | 245 | $18,693 |
| 99490 | Chronic care management, first 20 min | 382 | $17,686 |
| 99497 | Advance care planning | 152 | $9,289 |
| G0179 | **Home health** re-certification | 201 | $5,726 |
| 99306 | Initial nursing facility care, high | 37 | $4,672 |
| G0180 | Home health certification | 31 | $985 |

**Not one procedure. Not one test.** Nursing-home visits, house calls, care plans
and home-health certifications.

---

## Step 2 — the Part D bill does not fit that practice

`FED_CMS_PARTD_PRESCRIBER_DRUG`, **DY2022**, proven from the source filename
`MUP_DPR_RY24_P04_V10_DY22_NPIBN.csv`:

| Measure | Value |
|---|---|
| Rows | 492 |
| Distinct brand names | **486** |
| Total claims | **136,920** |
| **Total drug cost** | **$10,703,850.59** |
| **Rank among Family Practice prescribers** | **9 of 102,484** |

**A doctor with 464 Medicare patients and $207,303 in professional billing wrote
the ninth-largest Part D drug bill of any family physician in the United States.**

The 52:1 ratio between the two is **cross-year** — Part B is DY2023, Part D is
DY2022. Read it as a shape, not a precise multiple.

### The top of the list

| Brand | Generic | Claims | Benes | Cost | Per claim |
|---|---|---|---|---|---|
| Eliquis | Apixaban | 2,689 | 397 | $897,244 | $334 |
| **Invega Sustenna** | Paliperidone palmitate | 206 | 36 | **$619,074** | $3,005 |
| **Nuedexta** | Dextromethorphan/quinidine | 734 | 63 | **$531,329** | $724 |
| **Nuplazid** | Pimavanserin | 190 | 17 | **$406,124** | $2,137 |
| **Vraylar** | Cariprazine | 496 | 51 | **$375,006** | $756 |
| Trulicity | Dulaglutide | 373 | 65 | $333,658 | $895 |
| Xarelto | Rivaroxaban | 797 | 89 | $259,190 | $325 |
| **Latuda** | Lurasidone | 265 | 25 | **$227,714** | $859 |
| Januvia | Sitagliptin | 630 | 66 | $201,537 | $320 |
| **Aristada** | Aripiprazole lauroxil | 71 | 17 | **$195,194** | $2,749 |
| **Austedo** | Deutetrabenazine | 46 | — | **$148,926** | $3,238 |

Eliquis, Xarelto, Trulicity and Januvia are ordinary for an elderly panel.
**The bolded rows are not.**

`Invega Sustenna` and `Aristada` are **long-acting injectable antipsychotics** —
depot shots. 206 claims across 36 people is roughly monthly injection, all year.

`Nuplazid` is licensed for Parkinson's-disease psychosis and carries a boxed
warning about increased death in elderly patients with dementia-related
psychosis. 190 claims across **17 people**.

`Nuedexta` is licensed for pseudobulbar affect. `Austedo` is for tardive
dyskinesia — the movement disorder caused by long-term antipsychotic use.

---

## Step 3 — the peer test, run twice, two different ways

### Read A — DY2022, brand-list method, corrected

The first draft hard-coded 26 antipsychotic brand names. That list missed
**7.9% of national antipsychotic claims** — exactly the nursing-home shelf:
haloperidol decanoate, chlorpromazine, fluphenazine, perphenazine, the ER and
ODT forms, Invega Trinza. **The omission understated Frank more than it
understated his peers.**

Re-run on a 62-pair generic-name set, Family Practice prescribers with 1,000+
claims:

```
                    DRAFT     CORRECTED
Frank antipsych      7,867         8,294
Frank share          5.75%         6.06%
peer median          0.28%         0.29%
peer mean            0.59%         0.61%
peer p95             2.22%         2.28%
peer p99             4.56%         4.78%
rate percentile      99.45         99.45
volume percentile    99.99         99.99
peers compared      61,432        61,432
```

### Read B — DY2024, CMS's own antipsychotic measure

`FED_CMS_PART_D_PRESCRIBERS` is landed at DY2024 and carries CMS's own
pre-computed field, `ANTPSYCT_GE65_TOT_CLMS`. **This is a different year and a
different definition, computed by CMS rather than by me.**

Frank's DY2024 row:

| Field | Value |
|---|---|
| Total claims | 41,925 |
| Total drug cost | $3,531,599.20 |
| Beneficiaries | 1,265 |
| 65+ claims | 31,654 |
| 65+ drug cost | $2,265,485.59 |
| **Antipsychotic 65+ claims** | **1,427** |
| **Antipsychotic 65+ cost** | **$303,465.32** |
| Antipsychotic 65+ beneficiaries | **154** |

Against 44,406 Family Practice peers with 1,000+ senior claims:

| | Antipsychotic share of 65+ claims |
|---|---|
| **Frank** | **4.51%** |
| peer 99th percentile | 4.445% |
| peer mean | 0.749% |
| **peer median** | **0.521%** |

**Rate percentile 99.04. Volume percentile 99.43.**

### What holding across both reads means

| | DY2022, my method | DY2024, CMS's method |
|---|---|---|
| Frank's share | 6.06% | 4.51% |
| Peer median | 0.29% | 0.521% |
| **Rate percentile** | **99.45** | **99.04** |
| Peers | 61,432 | 44,406 |

Two years apart. Two definitions. Two peer sets. **He clears the 99th percentile
in both.** A single-year artifact would not survive that.

> **Lead with the percentile, not the multiple.** CMS suppresses drug rows under
> 11 claims, so a peer who wrote 8 quetiapine scripts reads as **zero**
> antipsychotics. That depresses the peer median far more than it depresses
> Frank, whose volume clears the threshold on everything. **The "20x the median"
> figure is inflated by an unknown amount. The percentile rank is not.**

### His antipsychotic book — the largest rows, DY2022

| Drug | Claims | Benes | Cost |
|---|---|---|---|
| Invega Sustenna | 206 | 36 | $619,074 |
| Nuplazid | 190 | 17 | $406,124 |
| Vraylar | 496 | 51 | $375,006 |
| Latuda | 265 | 25 | $227,714 |
| Aristada | 71 | 17 | $195,194 |
| **Invega Trinza** | **14** | — | **$110,556** |
| Rexulti | 108 | — | $82,149 |
| Olanzapine | 1,747 | 250 | $71,271 |
| Clozapine | 1,100 | 70 | $54,111 |
| **Chlorpromazine Hcl** | **100** | — | **$51,434** |
| Quetiapine Fumarate | 1,666 | 248 | $47,427 |
| Abilify Maintena | 15 | — | $40,627 |
| Risperidone | 1,461 | 220 | $30,711 |
| **Paliperidone Er** | **59** | — | **$24,932** |
| Aripiprazole | 328 | 64 | $23,868 |
| **Fluphenazine Hcl** | **41** | — | **$10,563** |
| Haloperidol | 171 | 32 | $7,971 |
| **Invega** | **24** | — | **$6,319** |
| **Quetiapine Fumarate Er** | **82** | — | **$6,166** |
| **Clozapine Odt** | **22** | — | **$4,173** |
| **Olanzapine Odt** | **44** | — | **$2,218** |
| Ziprasidone | 43 | — | $2,390 |

Bold rows were missing from the first draft.

**1,122 clozapine claims across roughly 70 patients**, counting the ODT form.
Clozapine is a last-resort antipsychotic requiring registered blood monitoring for
agranulocytosis. Seventy patients on it, in a family practice, is extraordinary.

**Four separate paliperidone products** — Invega Sustenna, Invega Trinza, Invega,
Paliperidone ER — totalling $760,881. Trinza is the **three-month** depot
injection.

---

## Step 4 — the nursing home, and what inspectors found there

**HASKELL CARE CENTER**, CCN 375414.

| Field | Value |
|---|---|
| Address | 405 North Choctaw, Haskell, OK |
| Ownership | **For profit — Limited Liability company** |
| Certified beds | 58 |
| Average residents per day | **35.4** |

### One affiliated physician — and that is normal, not a finding

```sql
select NPI, PROVIDER_LAST_NAME from FED_CMS_FACILITY_AFFILIATION where CCN='375414';
→ 1164450573  FRANK
```

**The first draft called this out in bold. That was wrong.** Base rates across
the same table:

| Metric | Value |
|---|---|
| Nursing-home CCNs in the file | 14,501 |
| **Median providers per home** | **2** |
| Mean | 2.8 |
| Homes listing exactly one provider | **5,148 — 35.5%** |
| **Oklahoma homes listing exactly one** | **112 of 218** |

A median of two physicians per nursing home is not reality. **The file badly
under-reports affiliation.** Haskell listing one doctor is the modal case in
Oklahoma. It is not evidence that Frank was the sole physician.

What remains true is narrower and still useful: **Frank's own affiliation list
contains this home and nothing outside post-acute care.**

### The deficiency record — 19 of 26 citations shown

`FED_CMS_NURSING_HOME_DEFICIENCIES` holds **26** rows for Haskell. The seven
omitted are administrative — PASARR coordination twice, lab timeliness, call
system, staffing posting, food sourcing, assessment transmission. Nothing
exculpatory. The file spans 2017-03-23 to 2026-05-20, so Haskell genuinely has
**no citations before 2022-04-14.**

| Survey | Tag | What inspectors cited | Scope | Complaint? |
|---|---|---|---|---|
| **2022-04-14** | **F757** | **"Each resident's drug regimen must be free from unnecessary drugs."** | E | standard |
| **2022-04-14** | **F758** | **"Implement gradual dose reductions and non-pharmacological interventions prior to initiating or instead of continuing psychotropic medication."** | D | standard |
| 2022-04-14 | F756 | Licensed pharmacist monthly drug regimen review | D | standard |
| 2022-04-14 | F700 | Bed rails — assess risk, informed consent | E | standard |
| 2022-04-14 | F686 | Pressure ulcer care and prevention | D | standard |
| 2022-04-14 | F684 | Appropriate treatment per orders | E | standard |
| 2022-04-14 | F688 | Range of motion and mobility | E | standard |
| 2022-04-14 | F689 | Free from accident hazards, adequate supervision | E | standard |
| 2022-04-14 | F609 | Timely report suspected abuse, neglect or theft | D | standard |
| 2023-08-10 | F656 | Complete care plan meeting resident needs | E | standard |
| 2023-08-10 | F657 | Care plan developed within 7 days | E | standard |
| **2023-11-21** | **F689** | Free from accident hazards, adequate supervision | **G** | **complaint** |
| **2024-09-27** | **F607** | **Policies to prevent abuse, neglect and theft** | E | **complaint** |
| **2024-09-27** | **F609** | **Timely report suspected abuse or neglect** | E | **complaint** |
| **2024-09-27** | **F610** | **Respond appropriately to all alleged violations** | E | **complaint** |
| 2024-09-27 | F641 | Accurate resident assessment | D | complaint |
| 2024-09-27 | F684 | Appropriate treatment per orders | D | complaint |
| 2024-09-27 | F695 | Safe respiratory care | D | standard |
| 2024-09-27 | F732 | Post nurse staffing daily | F | standard |

**Scope-severity `G` means actual harm to a resident, isolated.** It is the
highest severity in this record and it came from a complaint.

### The one penalty on file

| Date | Type | Amount |
|---|---|---|
| 2023-11-21 | Fine | **$3,422** |

Same date as the `G` harm citation.

---

## Step 5 — the timeline

| Date | What happened | Source |
|---|---|---|
| **2022-04-14** | Haskell cited: **unnecessary drugs**, failure to reduce **psychotropics** | nursing home deficiencies |
| **calendar 2022** | Frank writes **$10.7M** in Part D, **6.06% antipsychotics**, 99.45th pctile | Part D by drug |
| 2022 | Acadia is his top payer, product named **NUPLAZID** | Open Payments 2022 |
| 2023-08-10 | Haskell cited: care plans incomplete | nursing home deficiencies |
| **2023-11-21** | Haskell cited **scope G — actual harm**, complaint. **$3,422 fine** | deficiencies + penalties |
| 2023 | Acadia is again his top payer, again **NUPLAZID** | Open Payments 2023 |
| **2024-01-15** | **Skye Orthobiologics forgives $3,082,225** owed by "Previse Medical" | Open Payments 2024 |
| **calendar 2024** | Antipsychotics **4.51% of senior claims**, 99.04th pctile | Part D prescribers |
| **2024-09-27** | Haskell cited on **three abuse-and-neglect tags** — all complaint-driven | deficiencies |
| **2025-08-20** | **Frank excluded under `1128a2`** | LEIE |

Five distinct CMS datasets plus the OIG exclusion list. The 2022 survey happened
**inside** the drug year, not before it.

---

## Step 6 — who was paying him, and for what

| Year | Payments | Total | Payers |
|---|---|---|---|
| 2022 | 36 | $914.79 | 10 |
| 2023 | 18 | $569.55 | 8 |
| **2024** | **1** | **$3,082,225.00** | **1** |

### The lunch money names the drugs

| Year | Payer | Product named | Paid |
|---|---|---|---|
| 2022 | **ACADIA Pharmaceuticals** | **NUPLAZID** | $468.77 |
| 2022 | ITI, Inc. | CAPLYTA | $236.73 |
| 2022 | Gilead Sciences | — | $52.51 |
| 2022 | GlaxoSmithKline | TRELEGY ELLIPTA | $36.16 |
| 2022 | Avanir Pharmaceuticals | **Nuedexta** | $31.02 |
| 2022 | Indivior Inc. | PERSERIS | $17.77 |
| 2023 | **ACADIA Pharmaceuticals** | **NUPLAZID** | $245.29 |
| 2023 | Corium, LLC | Adlarity | $102.50 |
| 2023 | ITI, Inc. | CAPLYTA | $52.39 |
| 2023 | Sumitomo Pharma America | APTIOM | $26.79 |
| 2023 | Indivior Inc. | PERSERIS | $17.56 |
| 2023 | Otsuka America | **NUEDEXTA** | $15.28 |

**Acadia was his single largest payer in both 2022 and 2023, and the product on
the record is Nuplazid both times** — the drug carrying the boxed warning about
elderly dementia patients, which he prescribed 190 times to 17 people in DY2022.

Caplyta and Perseris are also antipsychotics. **Only DY2022 by-drug data is
landed**, so whether he wrote them in 2023 cannot be checked here.

Same caution as always: $468.77 does not buy $406,124. The payments show **who
was in the building**, not what changed hands.

### And then 2024

One record. $3,082,225. Debt forgiveness. Bad debt owed by **Previse Medical**.
The payer is **Skye Orthobiologics LLC**, which sells amniotic and placental
tissue allografts for wound care.

That single write-off is **43% of Skye's entire 2024 Open Payments filing**, and
the largest of the 30 write-offs the company reported.

**A wound-care supplier was owed $3.08M by an entity tied to a doctor whose
practice is a nursing home, a hospice and a home health agency.** Pressure ulcer
care was among the 2022 citations at Haskell.

**What "Previse Medical" is, and how it relates to Frank, is not in this
warehouse.** No identifier is attached to the name.

---

## Step 7 — the DME trail

| Field | Value |
|---|---|
| Distinct suppliers billing on his referrals | **23** |
| Supplier HCPCS codes | 84 |
| Beneficiaries | 64 |
| Claims | 353 |
| **Services** | **36,017** |
| Submitted charges | $438,324.10 |
| **Medicare paid to suppliers** | **$76,930.72** |

**36,017 services for 64 beneficiaries — 563 services per patient.** Twenty-three
separate supply companies billed Medicare on this one doctor's referrals.

Not investigated. It is the next thread.

---

## What the data supports

| Statement | Supported? |
|---|---|
| Frank's affiliations are one nursing home, one hospice, one home health agency | **yes** |
| He wrote $10,703,850.59 in Part D in DY2022 | **yes, re-queried** |
| That ranks 9th of 102,484 family physicians | **yes, re-queried** |
| DY2022 antipsychotic share 6.06%, 99.45th percentile | **yes, corrected list** |
| DY2024 antipsychotic share 4.51%, 99.04th percentile | **yes, CMS's own field** |
| Haskell cited for unnecessary drugs and psychotropic reduction failure | **yes, 2022-04-14** |
| Haskell cited on three abuse-and-neglect tags in 2024 | **yes, all complaint-driven** |
| Frank excluded 2025-08-20 under `1128a2` | **yes** |
| `1128a2` is the patient-abuse statute | **from the statute, not the warehouse — verify** |
| Skye forgave $3,082,225 tied to him in Jan 2024 | **yes** |
| **He was Haskell's only physician** | **no. 35.5% of homes list one; the file under-reports** |
| **Part B and Part D are the same year** | **no. Part B is DY2023, Part D is DY2022** |
| **"20x the peer median"** | **inflated. Suppression depresses the median. Use the percentile** |
| **He harmed patients** | **not shown here** |
| **The antipsychotics were inappropriate** | **not shown. No diagnosis data exists in these tables** |
| **The deficiencies were caused by his prescribing** | **not shown. Citations name the facility, not him** |
| **The exclusion relates to Haskell** | **not shown. LEIE records no facility** |

**The gap that matters:** Part D carries no diagnosis. A resident with genuine
schizophrenia needs clozapine. Nothing in this warehouse distinguishes
appropriate treatment of severe mental illness from chemical restraint of
dementia patients. **That distinction requires the medical records, and it is the
whole case.**

What the data does establish is that **a prescriber at the 99th percentile in two
separate years was writing into a facility inspectors cited for exactly the
practice the numbers describe, in one of those years.** That is a lead of unusual
quality. It is not a conclusion.

---

## Corrections applied after the skeptic pass

| # | First draft said | Measured | Where it came from |
|---|---|---|---|
| 1 | He is the only physician at Haskell | 35.5% of homes list one | no base rate checked |
| 2 | Part B is "2022-era" | registry says DY2023 | assumed, not checked |
| 3 | No `%ANTIPSYCH%` column exists | `ANTPSYCT_GE65_*` does | searched the wrong spelling |
| 4 | Only DY2022 Part D is landed | `FED_CMS_PART_D_PRESCRIBERS` is DY2024 | it was in my own table list |
| 5 | Antipsychotic share 5.75% | 6.06% | brand list missed 7.9% nationally |
| 6 | "His full antipsychotic book" | 12 of 22 rows shown | list was partial |
| 7 | "The deficiency record" | 19 of 26 shown | subset presented as whole |
| 8 | 492 distinct drugs | 486 distinct brand names | row count, not distinct |
| 9 | 2023 payments shown against Part D cost | those were DY2022 figures | column repeated a prior year |

Two of those were consequential. **#4 handed the investigation a second
independent year**, which is why the finding is now stronger than the draft
claimed. **#1 removed a bold claim that was actually the modal case.**

---

## Not checked

1. The 23 DME suppliers and the 36,017 services. Largest untested money trail.
2. Neighborhood Hospice and Universal Rehab Services. Both affiliated, neither
   examined. Hospice fraud is a known pattern in exactly this practice shape.
3. Haskell's own antipsychotic percentage. `FED_NURSINGHOME411` and the CMS
   nursing tables were checked for a facility-level measure; none is landed.
4. Previse Medical. A name with no identifier attached.
5. DY2023 Part D. Neither the by-drug nor the by-prescriber table covers it.
6. The other 28 Skye write-off recipients, and whether their practices share this
   nursing-home shape.
7. Whether the Oklahoma medical board or NPDB carries an entry. `FED_HRSA_NPDB`
   is landed but de-identified.
8. The true landed vintage of the Part B tables. Registry says DY2023, COVID
   codes prove only 2021-or-later. Unresolved.

## Cost

Four scripts plus three ad-hoc query sets, and a skeptic pass that re-ran the
peer test independently. The heaviest queries were two window-function scans of
`FED_CMS_PARTD_PRESCRIBER_DRUG` at 25.9M rows and one of
`FED_CMS_PART_D_PRESCRIBERS`. No prior run of this pattern in the query log to
price against.
