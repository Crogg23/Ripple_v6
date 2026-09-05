# Pharma payments to excluded providers, 2022 — 2026-09-05

Queries through the Python door, `connect/db.py`. Script: `scratchpad/hunt22.py`.
Source: `FED_CMS_OPEN_PAYMENTS_2022` joined to `FED_HHS_OIG_LEIE`.

**Headline: 137 actively excluded NPIs received 648 payments totalling
$338,872.42 from 141 manufacturers during 2022.**

**But 89% of that total is a single row — a $301,647 Medtronic device royalty to
one excluded neurosurgeon. Strip it and the rest is $37,225 spread across 136
people, in lunches. Two completely different stories sit in one number.**

---

## The method, stated before the numbers

Every payment was date-tested against the exclusion:

```sql
join LEIE on NPI
where EXCLDATE < DATE_OF_PAYMENT
```

Without that test the same join returns **532 NPIs, 9,162 payments,
$1,329,835.35.** That number is wrong by a factor of four. Most of those people
were excluded *after* being paid, which is the same trap that turned 554 ghost
prescribers into 2.

| Test applied | Excluded NPIs | Payments | Total |
|---|---|---|---|
| Naive NPI join | 532 | 9,162 | $1,329,835.35 |
| **Date-tested** | **137** | **648** | **$338,872.42** |

Only the date-tested row is reportable.

---

## 1. The headline count

| Measure | All manufacturers | Miranda's 45 only |
|---|---|---|
| Distinct excluded NPIs paid | **137** | 47 |
| Payments | 648 | 335 |
| **Total paid** | **$338,872.42** | $16,172.68 |
| Manufacturers involved | **141** | 45 |

The 45 companies that paid Miranda also paid **46 other excluded providers** that
year. They are not an unusual subset — they are a representative one.

---

## 2. The number breaks in two

| Nature of payment | Count | Total | Share |
|---|---|---|---|
| **Royalty or License** | 6 | **$303,420.98** | **89.5%** |
| Food and Beverage | 582 | $21,468.88 | 6.3% |
| Consulting Fee | 5 | $8,373.31 | 2.5% |
| Education | 43 | $3,105.37 | 0.9% |
| Debt forgiveness | 2 | $1,479.34 | 0.4% |
| Travel and Lodging | 8 | $949.54 | 0.3% |
| Speaking or faculty | 2 | $75.00 | 0.0% |

**582 of 648 payments are meals.** They average $36.89.

### The one row that carries the total

| Field | Value |
|---|---|
| NPI | 1194706754 |
| Name | **ASFORA, WILSON** |
| Specialty | Neurological Surgery |
| Location | Sioux Falls, SD |
| Payer | **Medtronic, Inc.** |
| Amount | **$301,647.00** |
| Date | 2022-06-02 |
| Nature | **Royalty or License** |
| Excluded | **2021-04-30**, statute `1128b7` |

Excluded **thirteen months** before the payment. `1128b7` is the permissive
exclusion for fraud or kickbacks.

This is not a sales-rep lunch. It is a device royalty stream — a company paying a
surgeon for the use of his patented design, continuing after his exclusion.

**One row, one company, 89% of the year's total.**

### What is left after removing it

| | Amount |
|---|---|
| Total, date-tested | $338,872.42 |
| Less Asfora royalty | −$301,647.00 |
| **Remaining, 136 NPIs** | **$37,225.42** |

$274 per excluded provider, per year. That is the compliance-failure story, and
it is about **contact**, not money.

---

## 3. Top 10 payers by dollars

| Payer | Excluded NPIs | Payments | Total |
|---|---|---|---|
| **Medtronic, Inc.** | 5 | 6 | **$301,980.53** |
| Takeda Pharmaceuticals U.S.A. | 2 | 6 | $8,389.52 |
| Align Technology, Inc. | 2 | 5 | $3,575.71 |
| Globus Medical, Inc. | 2 | 2 | $1,644.64 |
| ZIMVIE INC. | 3 | 20 | $1,439.92 |
| **ABBVIE INC.** | **23** | 38 | $1,274.62 |
| Abbott Laboratories | 11 | 19 | $1,222.22 |
| Merit Medical Systems Inc | 1 | 1 | $986.89 |
| Dentsply Sirona Inc | 2 | 3 | $948.40 |
| Intuitive Surgical, Inc. | 2 | 7 | $939.54 |

Then ViiV Healthcare $854.86, Zimmer Biomet $675.00, Janssen Pharmaceuticals
$658.14, Gilead $548.24, Boston Scientific $544.23.

**Six of the top ten are device makers, not drug makers.** Devices pay royalties
and consulting fees; drugs buy lunch. That is why the dollar ranking looks
nothing like the reach ranking.

## Top 10 payers by breadth — how many excluded providers each reached

| Payer | Excluded NPIs | Payments | Total |
|---|---|---|---|
| **ABBVIE INC.** | **23** | 38 | $1,274.62 |
| Boston Scientific Corporation | 11 | 18 | $544.23 |
| Abbott Laboratories | 11 | 19 | $1,222.22 |
| Lilly USA, LLC | 7 | 16 | $263.21 |
| Janssen Pharmaceuticals, Inc | 6 | 9 | $658.14 |
| Novo Nordisk Inc | 6 | 7 | $358.50 |
| Merck Sharp & Dohme LLC | 5 | 17 | $352.92 |
| Medtronic, Inc. | 5 | 6 | $301,980.53 |
| Allergan, Inc. | 4 | 11 | $278.19 |
| AstraZeneca Pharmaceuticals LP | 4 | 13 | $487.55 |

Then Teva 4, Astellas 4, Gilead 4, Boehringer Ingelheim 3, Eisai 3.

**AbbVie reached 23 excluded providers in one year for $1,274.62.** That is 38
sales calls on people the government had barred from federal health programs.

---

## 4. The excluded providers who got paid

| NPI | Name | Specialty | ST | Excluded | Statute | Payers | Total |
|---|---|---|---|---|---|---|---|
| 1194706754 | **ASFORA, WILSON** | Neurology | SD | 2021-04-30 | 1128b7 | 1 | **$301,647.00** |
| 1023087293 | SIMMONS, WALTER | Emergency Medicine | AZ | 2022-03-20 | 1128b1 | 1 | $8,373.31 |
| **1285673012** | **MIRANDA, EDUARDO** | Internal Medicine | TX | **2015-06-18** | 1128a1 | **45** | $4,415.57 |
| 1871675769 | ANEROUSIS, MARY | Dentist | NJ | 2019-05-20 | 1128a1 | 1 | $3,512.42 |
| 1700925203 | KIM, GILBERT | Dentist | NY | 2014-09-18 | 1128a1 | 2 | $1,950.00 |
| 1255479804 | BROWN, CHARLES | Nurse/Nurses Aide | PA | 2013-07-18 | 1128a2 | 4 | $1,197.50 |
| 1922062181 | BISHAI, EMAD | Pain Management | TX | 2021-11-08 | 1128b7 | 8 | $1,102.84 |
| 1881634954 | LUPIANO, JOHN | Internal Medicine | NY | **2011-09-20** | 1128a1 | 5 | $1,027.14 |
| 1518958040 | LOPEZ, ALFREDO | Neurology | IN | 2019-11-20 | 1128a1 | 14 | $818.37 |
| 1053360966 | FUENTES, EDWIN | Family Practice | WV | 2018-05-20 | 1128a1 | 23 | $622.01 |

### Miranda is the outlier, and not on money

He ranks **third by dollars** but **first by breadth, by a factor of two**:

| Provider | Distinct payers |
|---|---|
| Miranda | **45** |
| Fuentes | 23 |
| Lopez | 14 |
| Bishai | 8 |
| Lupiano | 5 |

Nobody else on the excluded list was being called on by 45 separate companies.

### The longest-running failure is not Miranda

**LUPIANO, JOHN** was excluded **2011-09-20** — a decade before the payments —
and five manufacturers still paid him in 2022. Miranda's seven-year gap is not
the record.

---

## What this supports, and what it does not

| Statement | Supported? |
|---|---|
| 137 actively excluded NPIs were paid in 2022 | **yes, date-tested** |
| Total was $338,872.42 | **yes** |
| 141 manufacturers were involved | **yes** |
| 89% of the total is one Medtronic royalty | **yes** |
| AbbVie reached the most excluded providers, 23 | **yes** |
| This is an industry-wide compliance failure | **yes, on contact** |
| Manufacturers knowingly paid excluded providers | **not shown** |
| These payments were illegal | **not shown.** Open Payments reporting is itself the legal requirement, and every one of these was reported |

The companies disclosed all of it. That is why the data exists. The failure is
that **none of them cross-checked a free, public, monthly-updated federal list
before writing the cheque.**

---

## Four reasons this is a floor, not a total

1. **Only 10.5% of LEIE rows carry an NPI.** 75,001 exclusions cannot be joined
   at all. Nurses, aides and business entities are almost entirely invisible.
2. **LEIE is a current snapshot.** OIG removes people on reinstatement. Anyone
   excluded before 2022, paid in 2022, and reinstated since is **gone from the
   list** and uncountable here.
3. **One year only.** 2022 is the only Open Payments year tested. The 2023 table
   and the undated one are landed and untested.
4. **Open Payments NPI is optional.** Records with a blank or malformed NPI were
   excluded by the format filter and cannot be matched.

---

## Not checked

1. `FED_CMS_OPEN_PAYMENTS_2023` and the undated `FED_CMS_OPEN_PAYMENTS`. Same
   join, two more years, would triple the window.
2. Whether Asfora appears in Part B or Part D, and whether Medtronic devices
   were implanted on his order after 2021.
3. Name-based matching for the 75,001 NPI-less exclusions. Blocked by the
   single-word-collision trap unless multi-word only.
4. Whether the 141 manufacturers overlap with federal contractors in
   `FED_USASPENDING_%` under a UEI.
5. The five other excluded NPIs Medtronic paid, beyond Asfora.

## Cost

One script, seven queries, each a full scan of `FED_CMS_OPEN_PAYMENTS_2022` at
13.3M rows joined to `FED_HHS_OIG_LEIE` at 83,842. Heaviest work of the session
so far. No prior run of this pattern in the query log to price against.
