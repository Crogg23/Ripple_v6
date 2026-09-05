# Two FINDINGS views, evaluated — 2026-09-05

Queries through the Python door, `connect/db.py`. Script: `scratchpad/hunt25.py`.

**Headline one: the 137 and the 287 do not overlap at all. The prebuilt view
covers 2023–2024 only. Zero of its 287 rows touch 2022. Our hand-built run filled
a hole in the view, rather than duplicating it.**

**Headline two: `FEDERAL_CONTRACTOR_EPA_VIOLATOR` holds 57 rows, every one with
exactly one violating facility and not a single significant-non-compliance flag.
It is a working screen that found almost nothing, and the reason is the join key.**

---

## 1. `EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION` — reconciled

### The span and the grand total

| Measure | Value |
|---|---|
| Earliest `FIRST_PAID_YEAR` | **2023** |
| Latest `LAST_PAID_YEAR` | **2024** |
| Doctors | **287** |
| Post-exclusion payments | **1,439** |
| **Total paid after exclusion** | **$511,627.42** |

### By year pair

| First paid | Last paid | Doctors | Total |
|---|---|---|---|
| 2024 | 2024 | 127 | $148,561.75 |
| 2023 | 2023 | 94 | **$328,632.95** |
| 2023 | 2024 | 66 | $34,432.72 |

Three buckets, nothing else. **The view's window is exactly 2023–2024.**

### The reconciliation

```sql
select count(*) from ...EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION
where FIRST_PAID_YEAR <= 2022 and LAST_PAID_YEAR >= 2022;
→ 0
```

**Zero.** Not a subset, not a superset — a disjoint window.

| | Our run | The view |
|---|---|---|
| Year | **2022** | **2023–2024** |
| Source table | `FED_CMS_OPEN_PAYMENTS_2022` | the 2023 and undated tables |
| Excluded NPIs | 137 | 287 |
| Payments | 648 | 1,439 |
| Total | $338,872.42 | $511,627.42 |

**Combined 2022–2024: $850,499.84 across 1,987 payments.** The two do not
double-count on year, though individual doctors recur.

The view was built against `FED_CMS_OPEN_PAYMENTS` and
`FED_CMS_OPEN_PAYMENTS_2023`. `FED_CMS_OPEN_PAYMENTS_2022` is landed at 13.3M
rows and is **not wired into this view.** That is a one-line fix and it would add
137 provider-years.

### Exclusion year distribution — the tail is the story

| Excluded | Doctors | Paid after |
|---|---|---|
| 1995 | 1 | $12.87 |
| 2000 | 1 | $20.00 |
| 2008 | 2 | $91.74 |
| 2009 | 5 | $1,286.44 |
| 2010 | 11 | $2,171.67 |
| 2011 | 7 | $5,086.86 |
| 2012 | 11 | $1,240.08 |
| 2013 | 11 | $4,611.57 |
| 2014 | 20 | $1,331.24 |
| 2015 | 22 | $14,128.99 |
| 2016 | 25 | $1,881.67 |
| 2017 | 25 | $3,663.84 |
| 2018 | 21 | $4,233.82 |
| 2019 | 20 | **$117,960.89** |
| 2020 | 20 | $2,679.18 |
| 2021 | 19 | **$320,053.01** |
| 2022 | 37 | $6,011.33 |
| 2023 | 29 | $25,162.22 |

**Someone excluded in 1995 was still receiving industry payments in 2023 or
2024.** That is a thirty-year gap. Two more were excluded in 2000 and 2008.

The dollars concentrate hard in 2019 and 2021 exclusions — $438,013 of the
$511,627 total, 85.6%, from 39 people.

### Top recipients

| NPI | Name | Statute | Excluded | Payments | Paid | Years | Payers |
|---|---|---|---|---|---|---|---|
| 1194706754 | **ASFORA, WILSON** | 1128b7 | 2021 | 2 | **$318,325.02** | 2023 | 2 |
| 1982679544 | MOLINA, HECTOR | 1128a1 | 2019 | 1 | **$114,040.00** | 2024 | 1 |
| 1194956326 | GERBAKHER, ALEXANDER | 1128b7 | 2023 | 2 | $12,866.44 | 2024 | 2 |
| **1285673012** | **MIRANDA, EDUARDO** | 1128a1 | **2015** | **412** | $10,639.53 | 2023–24 | **60** |
| 1093002586 | FRANZESE, JOSEPH | 1128b4 | 2023 | 8 | $4,589.41 | 2024 | 1 |
| 1861518755 | BEAGUE, THOMAS | 1128a3 | 2011 | 20 | $3,589.13 | 2023–24 | 9 |
| 1891876520 | JOSEPH, ROBERT | 1128a3 | 2023 | 107 | $3,323.76 | 2024 | 14 |
| 1578558789 | TIWARI, KAMAL | 1128a1 | 2013 | 5 | $2,962.59 | 2023–24 | 3 |
| 1639196108 | RANDALL, MICHAEL | 1128a4 | 2017 | 1 | $1,600.00 | 2023 | 1 |
| 1518958040 | LOPEZ, ALFREDO | 1128a1 | 2019 | 25 | $1,281.28 | 2023–24 | 10 |

### Two names carry across both windows

**ASFORA, WILSON** — Medtronic paid him $301,647 in 2022 and **$318,325 in
2023**. Two years, $619,972, from device royalties, both after his April 2021
exclusion. **This is a continuing stream, not a one-off.** That materially
strengthens what looked like a single anomalous row.

**MIRANDA, EDUARDO** — 45 payers in 2022, **60 payers across 2023–24** on 412
payments. The number of companies calling on him **went up** after the year we
examined. Nobody else in the 287 comes close on breadth.

### MOLINA, HECTOR is new and worth a look

$114,040 from a **single payment**, single payer, in 2024. Excluded 2019 under
`1128a1`, the mandatory conviction statute. Five years, then a six-figure cheque.
**Not investigated here.**

---

## 2. `FEDERAL_CONTRACTOR_EPA_VIOLATOR` — 57 rows

### Columns

| Column | Holds |
|---|---|
| `PARENT_UEI` | the contractor's parent UEI |
| `COMPANY_NAME` | name |
| `VIOLATING_FACILITIES` | count of EPA facilities in violation |
| `ANY_SNC` | significant non-compliance flag, Y/N |
| `TOTAL_EPA_PENALTIES` | dollars in EPA penalties |
| `TOTAL_FORMAL_ACTIONS` | count of formal EPA actions |
| `FEDERAL_DOLLARS_OBLIGATED` | federal contract dollars |
| `N_AWARDS`, `N_AGENCIES` | contract breadth |
| `MATCH_CONFIDENCE` | 1.00, 0.85 or 0.80 |

### Top 5 by federal dollars

| Company | Fed dollars | Awards | Agencies | EPA penalty | Actions |
|---|---|---|---|---|---|
| **SPACE EXPLORATION TECHNOLOGIES CORP.** | **$100,832,599,497** | 312 | 8 | $90,000 | 1 |
| MASSACHUSETTS INSTITUTE OF TECHNOLOGY | $1,000,899,068 | 75 | 6 | $0 | 1 |
| EDUCATIONAL TESTING SERVICE | $992,158,088 | 30 | 1 | $1,000 | 1 |
| JCB, Inc. | $660,927,623 | 58 | 1 | $4,400 | 1 |
| MEDLINE INDUSTRIES, INC. | $635,896,473 | 1,594 | 5 | $0 | 9 |

Then Moog $592.9M, National Air Cargo $374.5M, PG&E $360.5M.

### Top 5 by EPA penalty

| Company | Penalty | Actions | Fed dollars |
|---|---|---|---|
| GENERAL MOTORS COMPANY | $654,150 | 1 | $348,998,897 |
| EDWARDS LIFESCIENCES LLC | $500,000 | 3 | $30,693,440 |
| SITEONE LANDSCAPE SUPPLY | $311,313 | 2 | $4,683 |
| Imperial Irrigation District | $299,857 | 2 | $5,256,646 |
| THOMAS JEFFERSON UNIVERSITY | $215,070 | 2 | $54,040,093 |

### The shape says the screen is underpowered

| Measure | Value |
|---|---|
| Rows | **57** |
| Total federal dollars | **$106,996,950,324** |
| Total EPA penalties | **$3,006,703** |
| Total formal actions | 125 |
| Total violating facilities | **58** |
| **Rows flagged `ANY_SNC` = Y** | **0** |

**58 violating facilities across 57 companies.** Every company has exactly one,
bar a single exception. **Not one row carries a significant-non-compliance flag.**

`MATCH_CONFIDENCE` splits 46 at 1.00, 7 at 0.85, 4 at 0.80.

### Why the yield is so low — the chain

The warehouse holds **3.3M EPA-registered facilities** and **93.2M USASpending
contract rows**. A join between them returning 57 companies is not a finding
about American industry. It is a finding about the join.

The view keys on `PARENT_UEI`. From the earlier bridge work:

| Key | Distinct values | Tables |
|---|---|---|
| UEI | 827,685 | 9 |
| FRS_ID | 5,404,044 | 17 |

UEI did not exist before **April 2022**, and EPA's own facility registry does not
carry it. Matching an EPA facility to a federal contractor requires going
facility → company → UEI, and the only built path for that is
`FRS_ID ↔ LEI` at 73,948 rows, which the view does not appear to use.

**The screen is real and the 57 rows are probably sound. The recall is the
problem, not the precision.** Zero SNC flags across 57 companies is what an
underpowered join looks like, not evidence that federal contractors comply.

### The one number worth carrying

SpaceX: **$100.8 billion obligated, $90,000 in EPA penalties.** That single row
is 94% of the view's total federal dollars. The ratio is arresting but it rests
on one facility and one formal action, so it is a headline without a body.

---

## What is supported

| Statement | Supported? |
|---|---|
| The view spans 2023–2024 only | **yes** |
| Zero overlap with our 2022 run | **yes, tested directly** |
| View total is $511,627.42 across 287 doctors | **yes** |
| Combined 2022–2024 is $850,499.84 | **yes, on disjoint years** |
| Asfora received $619,972 across two years | **yes** |
| A 1995 exclusion was still being paid in 2023–24 | **yes** |
| `FEDERAL_CONTRACTOR_EPA_VIOLATOR` has 57 rows, zero SNC | **yes** |
| The EPA screen is underpowered by its UEI key | **inferred, not proven** |
| Federal contractors mostly comply with EPA rules | **no. The view cannot support that** |

---

## Not checked

1. The exact source tables inside the view definition. Inferred from the year
   window, not read.
2. Whether adding `FED_CMS_OPEN_PAYMENTS_2022` to the view is safe. It would need
   the same column shape.
3. MOLINA, HECTOR — one payment, $114,040, 2024. Uninvestigated.
4. Whether the EPA view's low yield is UEI recall or a deliberate high-confidence
   filter. Reading the definition would settle it.
5. The other 10 `FINDINGS` views. Only three have been counted this session.

## Cost

One script plus two ad-hoc query sets, all against views over already-built
marts. Small. No prior run of this pattern in the query log to price against.
