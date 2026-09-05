# Frank thread 3: the 23 DME suppliers

Opened 2026-09-05. NPI `1164450573`, Alexander Frank, excluded 2025-08-20.
Python door, `connect/db.py`. Chat plug-in still 401.

**Verdict up front: this thread deflates.** The headline number that made it look
alarming does not survive a base rate. A first draft of this report then over-read
the exculpatory side, and a skeptic pass reversed that too. Both corrections are
kept below rather than quietly folded in.

---

## The source

`FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER`, 381,228
rows, ingested 2026-07-26. One row per referring provider. 99 columns.

The table carries a grand total plus three product families, each with its own
supplier, patient, service and dollar counts.

| Prefix | Family |
|---|---|
| `TOT_` | everything |
| `DME_` | durable medical equipment |
| `POS_` | prosthetics, orthotics and supplies |
| `DRUG_` | drugs and nutritional products |

Frank's row:

| Measure | Total | DME family | POS | Drug |
|---|---|---|---|---|
| Suppliers | **23** | 19 | suppressed `#` | suppressed `*` |
| HCPCS codes | 84 | 55 | suppressed | suppressed |
| Beneficiaries | 64 | 52 | suppressed | suppressed |
| Claims | 353 | 250 | suppressed | suppressed |
| **Services** | **36,017** | **4,741** | suppressed | suppressed |
| Medicare paid | **$76,930.72** | $49,932.39 | suppressed | suppressed |

**87% of his service count is outside the visible DME column.** 4,741 of 36,017.
The rest sits in prosthetics-and-supplies and drugs, both suppressed at the family
level. The total row still counts them.

The subtraction 36,017 − 4,741 = 31,276 is **a ceiling, not a value.** The residual
between the total and the three families is never negative but is positive on 21.5%
of testable rows, for reasons other than the families. Say **at most 31,276**.

### A correction that was itself wrong

A first draft of this report claimed two earlier reports disagreed about Frank's
row, citing 6 suppliers and $46,385.19 from `ghost_npi_partb_money_2026-09-05`.

**That was a false accusation. Those figures are a different doctor.**

| NPI | Name | State | Specialty | Suppliers | Paid |
|---|---|---|---|---|---|
| 1164450573 | Frank, Alexander | OK | Family Practice | 23 | $76,930.72 |
| 1285673012 | Miranda, Eduardo | TX | Hematology-Oncology | 6 | $46,385.19 |

The earlier report prints the specialty on the face of its own table and files the
row under Miranda's name. It was right. Nothing was superseded.

---

## Data trap: the family columns do not sum, and `SPRSN_IND is null` is not a clean row

### The additivity test

Run on the 171,372 rows where all three family suppression flags are null. **The
correct denominator is the rows where all four columns are actually populated,
not all 171,372.** A first draft divided by the wrong one and reported beneficiary
additivity as 18.7%. The real figure is very different.

| Measure | Testable rows | Sum matches total | Share |
|---|---|---|---|
| Beneficiaries | 52,912 | 31,992 | **60.5%** |
| Suppliers | 171,372 | 107,587 | 62.8% |
| Services | 171,372 | 134,516 | 78.5% |

### Two different mechanisms, not one

The sign of the residual separates them.

| Measure | Total below sum | Total equals sum | Total above sum |
|---|---|---|---|
| Services | **0** | 134,516 | 36,856 |
| Medicare paid | **0** | 134,622 | 36,750 |
| Suppliers | 42,083 | 107,587 | 21,702 |
| Beneficiaries | 13,384 | 31,992 | 7,536 |

- **A total below the sum means de-duplication.** One supplier or one patient
  appears in two families and is counted once at the top. This happens for
  suppliers and beneficiaries, and only for those.
- **Dollars can never be de-duplicated, and the money residual is never negative.**
  So the excess on services and payments is something else: **family blocks that
  are masked while the total still counts them.**

**`SPRSN_IND is null` does not mean the row is clean.** In that same
171,372-row cohort:

| Condition | Rows |
|---|---|
| `TOT_SUPLR_BENES` itself null | 88,344 |
| All three family service columns `'0'` with a positive total | 9,253 |

One sampled row reads `TOT_SUPLR_SRVCS = 9254` with DME, POS and DRUG all zero.

**How to apply.** Never add the family columns. Never compare a family column to a
total column as the same population. Never take a null suppression flag as proof
the row is whole.

---

## The headline number does not hold

The handoff carried this forward: *36,017 services for 64 beneficiaries — 563 per
patient. Untouched.*

The arithmetic is right. 36,017 ÷ 64 = 562.8. Then the base rate.

| Measure | Frank | National median | Referrers above him | Percentile |
|---|---|---|---|---|
| Services per beneficiary | **562.8** | 38.1 | **18,213 of 208,605** | 91.3rd |
| Total services | 36,017 | 461 | 11,300 of 381,228 | 97.0th |
| Distinct suppliers | 23 | 6 | 34,939 of 381,228 | 90.8th |
| Medicare paid | $76,931 | $7,149 | 27,408 of 381,228 | 92.8th |

**18,213 referring providers bill more services per patient than Frank does.**

### And 91.3rd is itself the top of a band

172,623 rows, 45% of the file, drop out because their beneficiary count is
suppressed. Those providers have ten or fewer patients.

| Bound | Referrers above Frank | His percentile |
|---|---|---|
| Counting only rows with a published ratio | 30,230 guaranteed | **92.1** |
| Counting every hidden row that could clear it | up to 72,586 | **81.0** |

12,018 of the hidden rows have so many services that they beat 562.8 even at ten
beneficiaries. **The true percentile sits between 81 and 92, and the reported 91.3
is the flattering end.** This cuts toward the deflate, not away from it.

### Within his own specialty

| Family practice referrers | Value |
|---|---|
| With a services-per-patient ratio | 44,907 |
| Median ratio | 58.3 |
| Above Frank's 562.8 | **2,050** |
| Frank's percentile | 95.4th |
| Median Medicare paid | $9,259 |
| Above Frank's $76,931 | 4,609 |
| Frank's percentile on money | 89.7th |

### Against the rest of the investigation

| Finding | Where Frank ranks |
|---|---|
| Part D total cost, family physicians | **9 of 102,484** |
| Antipsychotic share DY2022 | **99.45th percentile** |
| Home health re-cert ratio | **98.97th percentile** |
| **DME services per patient** | **91.3rd, and that is a ceiling** |
| **DME suppliers used** | **90.8th percentile** |

**This is the weakest signal in the whole file on him.**

### Five ratios the first draft never computed

Hunting for something extreme that got talked away. Nothing found.

| Ratio | Frank | National median | Percentile |
|---|---|---|---|
| **Suppliers per beneficiary** | **0.359** | 0.462 | **39.2nd, below median** |
| Paid per service | $2.14 | $17.97 | 12.9th |
| Paid per beneficiary | $1,202 | $600 | 79.9th |
| Claims per beneficiary | 5.5 | 3.9 | 80.7th |
| Services per claim | 102.0 | 7.6 | 87.5th |

**23 suppliers across 64 patients is below-median density.** 126,745 referrers use
more suppliers per patient than he does. Cheap unit price against a high unit count
is the consumables shape, not the fraud shape.

### Who sits above him

| Specialty | Referrers above Frank |
|---|---|
| Urology | 2,894 |
| Nurse practitioner | 2,879 |
| Pulmonary disease | 2,301 |
| Family practice | 2,050 |
| Internal medicine | 1,825 |
| Nephrology | 1,320 |

Catheters, oxygen, dialysis supplies, infusion sets. **The metric counts units, not
events.** One patient on daily catheters generates hundreds of services a year by
definition.

---

## The patient mix, and the claim that reversed

The same row carries the demographics of the 64 patients.

| Measure | Frank | National median | Above him | Percentile |
|---|---|---|---|---|
| Dual eligible share | 62.5% | 12.1% | 3,920 of 54,055 | 92.8th |
| Dementia share | 50.0% | 0.0% | 3,112 of 55,394 | 94.4th |
| **Average risk score** | **3.117** | **1.755** | **45,744 of 381,227** | **88.0th** |
| Average age | 74.1 | 74.1 | 188,928 of 381,228 | 50.4th |

Also in that panel: 90.6% hypertension, 62.5% mood disorder, 57.8% depression,
56.3% heart failure, 54.7% diabetes, 43.8% chronic kidney disease.

### The reversal

A first draft concluded: *his panel is sicker relative to peers than his supply
volume is high relative to peers.* **That was an artifact of three different
denominators.** Volume was ranked on 208,605 rows, dual on 54,055, dementia on
55,394, risk on 381,227.

Restricted to the 3,468 family practice rows carrying all four measures:

| Dimension | Above Frank | Percentile |
|---|---|---|
| **Services per beneficiary** | **210** | **93.9th** |
| Dementia share | 270 | 92.2nd |
| Risk score | 277 | 92.0th |
| Dual share | 428 | 87.7th |

**On a common cohort his volume percentile is the highest of the four, not the
lowest.** The all-specialty common cohort of 20,318 rows gives the same ordering
within a third of a point.

The tell was available without the cohort test. **The one uncensored sickness
measure is the risk score**, non-null on 381,227 of 381,228 rows, and it puts him
at 88.0th — below his volume percentile. The first draft led with the two censored
measures and buried the clean one.

### Both censored measures are censored at 11

| Column | Published values |
|---|---|
| `BENE_DUAL_CNT` | 0, or 11 and above. **Never 1 through 10** |
| `BENE_CC_BH_ALZ_NONALZDEM_V2_PCT` | 0, or a share implying 11 or more |

Fill on the dementia column: 325,834 null, 37,000 exactly zero, 18,394 positive.

**The dementia median reads 0.0 because the middle of the distribution is deleted,
not because the typical referrer has no dementia patients.** A provider with 30
patients and 10 of them demented reads null, not 33%.

So "94.4th percentile" is a percentile inside a distribution with a hole in it. It
is arithmetically right and misleading without this line.

One thing that holds it up: the censoring is numerator-only. The maximum published
share is 1.0 and 1,210 rows publish with fewer than 11 non-dementia patients. So
the 3,112 above him is not itself undercounted.

---

## What could not be done, and why

**The 23 suppliers cannot be named.** This is the referrer-side file. It carries no
supplier NPI, no supplier name, nothing but a count. The companion table
`..._BY_SUPPL`, 440,670 rows, has full supplier identity and no referrer column.

**There is no referrer-to-supplier link in the warehouse.** The two tables share no
key. Matching on state plus HCPCS plus rough volume would produce candidates, not
a join, and would be inference dressed as evidence. Not done.

**Vintage is unknown.** The registry row for this table is blank. Ingested
2026-07-26. Frank's Part D is DY2022 and his Part B is DY2023-unproven. **Every
percentile here assumes the peer file and Frank's row are the same year, and this
table has no year column.** That is load-bearing for all of it and unresolved.

---

## What is claimed, and what is not

| Claim | Supported |
|---|---|
| Frank's row shows 23 suppliers, 36,017 services, 64 patients, $76,931 | **yes** |
| 87% of the service count is outside the visible DME column | **yes** |
| Exactly 31,276 services sit in POS and drugs | **no. At most 31,276** |
| The family columns do not sum to the total | **yes. Benes match on 60.5% of testable rows** |
| The non-additivity is de-duplication | **only for suppliers and benes. Money is masking** |
| A null suppression flag means a clean row | **no. 9,253 rows are zero-filled** |
| 563 services per patient is extreme | **no. Between 30,230 and 72,586 referrers are higher** |
| 23 suppliers is a lot | **no. Below median density. 126,745 referrers use more per patient** |
| His DME panel is sicker than typical | **yes, on every measure** |
| His panel sickness outruns his supply volume | **no. Reversed on a common cohort** |
| The dementia and dual percentiles are clean | **no. Both censored at 11** |
| The suppliers can be named | **no. No referrer-to-supplier link is landed** |
| The DME row and the Part D row are the same year | **not established** |
| Anything here is evidence of fraud | **no** |

---

## The honest close on this thread

The thread was carried forward on one number: 563 services per patient.

**That number is real and it is not unusual.** It lands somewhere between the 81st
and 92nd percentile of referring providers, and his supplier density is below the
national median.

The patient mix is genuinely extreme — dual eligible, demented, high risk — but it
does not outrun the volume once measured on a common cohort. **The first draft
claimed it did. It does not.** What is true is narrower: the volume and the
sickness both sit around the 92nd to 94th percentile together, which is what a
nursing-home dementia panel ordering consumables looks like.

The thread is closed. Nothing here corroborates the exclusion and nothing here
contradicts it.

The two Frank findings that still stand alone are the antipsychotic share at the
99.45th percentile and the home health re-certification ratio at the 98.97th. Both
remain flags and not verdicts, for the same reason: **Part D and Part B carry no
diagnosis.**
