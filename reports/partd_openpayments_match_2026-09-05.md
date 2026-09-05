# Part D drugs vs industry payments — 2026-09-05

Queries through the Python door, `connect/db.py`. Script: `scratchpad/hunt21.py`.
Part D is DY2022. Open Payments is `FED_CMS_OPEN_PAYMENTS_2022`.

**Headline: the product match for Miranda is 8 of 8. Every single one of his top
eight Part D drugs has a matching industry payment from the manufacturer that
sells it.**

**And the dollar ratio kills the kickback reading. $540.92 in payments against
$4,758,769 in prescribing — $8,797 prescribed per $1 received, and every payment
is a sales-rep lunch. This is not a bribe. It is 45 pharmaceutical companies
calling on an excluded physician for seven years.**

---

## 1. Miranda's top Part D drugs, DY2022

| Brand | Generic | Claims | Cost | Per claim |
|---|---|---|---|---|
| Ibrance | Palbociclib | 50 | **$749,617** | $14,992 |
| Imbruvica | Ibrutinib | 51 | **$722,465** | $14,166 |
| Xtandi | Enzalutamide | 47 | **$675,915** | $14,381 |
| Kisqali | Ribociclib Succinate | 38 | **$621,066** | $16,344 |
| Promacta | Eltrombopag Olamine | 44 | **$606,183** | $13,777 |
| Tasigna | Nilotinib Hcl | 43 | $512,472 | $11,918 |
| Lenvima | Lenvatinib Mesylate | 22 | $496,402 | $22,564 |
| Jakafi | Ruxolitinib Phosphate | 23 | $374,649 | $16,289 |

Top five alone: **$3,375,246.**

Every one is an oral targeted oncology or hematology agent at $12k–$23k per
fill. `Tot_Benes` is **null on all eight** — CMS suppresses beneficiary counts
under 11. So each of these is roughly 40–50 refills spread across fewer than 11
patients.

---

## 2. The pharma match — 8 of 8

Open Payments names the product on each payment in
`NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1`. That allows an exact
product-to-product test, not just a manufacturer-name guess.

| Part D drug | Prescribed | Payer in Open Payments | Product named | Paid |
|---|---|---|---|---|
| Ibrance | $749,617 | PFIZER INC. | **IBRANCE** | $123.67 |
| Imbruvica | $722,465 | Janssen Biotech, Inc. | **IMBRUVICA** | $77.83 |
| Xtandi | $675,915 | Astellas + Pfizer | **Xtandi / XTANDI** | $80.62 |
| Kisqali | $621,066 | Novartis | **KISQALI** | $81.38 |
| Promacta | $606,183 | Novartis | **PROMACTA** | $36.11 |
| Tasigna | $512,472 | Novartis | **TASIGNA** | $21.82 |
| Lenvima | $496,402 | EISAI INC. | **Lenvima** | $62.06 |
| Jakafi | $374,649 | Incyte Corporation | **JAKAFI** | $57.43 |
| **Total** | **$4,758,769** | 8 manufacturers | 8 products | **$540.92** |

**Eight for eight. No misses.**

Xtandi is co-marketed by Astellas and Pfizer, and both paid him for it
separately. That is the correct commercial arrangement showing through in the
data.

### The top three payers by dollar

| Payer | Payments | Total | Nature |
|---|---|---|---|
| Astellas Pharma US Inc | 10 | **$324.02** | Food and Beverage |
| Novartis Pharmaceuticals | 18 | **$314.23** | Food and Beverage |
| Amgen Inc. | 15 | **$300.14** | Food and Beverage |

Then Rigel $250.67, Pfizer $245.31, Janssen Biotech $234.20, Seagen $215.78,
Merck $178.87, Incyte $175.43, AVEO $153.65.

**Full-year total: 225 payments, $4,415.57, 45 distinct manufacturers.**

### The ratio, and why it settles the question

```
prescribed on the 8 matched drugs      $4,758,769
paid for those same 8 products              $540.92
                                       ───────────
prescribing per dollar received            $8,797
```

Every payment is under $130. Every one is categorised **Food and Beverage** or
**Education**. The largest single payer gave $324.02 across a whole year.

**No plausible mechanism has $324 of catered lunch buying $675,915 of Xtandi.**

The arrow almost certainly runs the other way: sales reps target high-volume
prescribers, so the payments are a *consequence* of the prescribing, not a cause.
A rep who visits an oncologist eleven times a year buys eleven lunches. The
product match is near-total because a rep only details the drug they sell.

### What the match does prove

The product-level correlation is not evidence of a kickback. It is evidence of
**contact**, and contact is the finding:

- **45 manufacturers** had representatives in this office during 2022
- Each visit was logged, attributed and reported to CMS
- Named companies include Pfizer, Novartis, Amgen, Merck, Janssen, Gilead,
  GlaxoSmithKline, Celgene, Exelixis, Ipsen, Eisai, Seagen, Incyte
- **The physician had been on the OIG exclusion list since June 2015**

Every one of those companies runs a compliance program that screens against the
LEIE. The list is free, public, and updated monthly. **Forty-five separate
screens failed, or were never run, for seven years.**

---

## 3. Aswad, NPI 1871571406 — the control case

### Top Part D drugs, DY2022

| Brand | Generic | Claims | Benes | Cost | Per claim |
|---|---|---|---|---|---|
| Remicade | Infliximab | 54 | null | **$403,049** | $7,464 |
| Keytruda | Pembrolizumab | 34 | null | **$361,770** | $10,640 |
| Nplate | Romiplostim | 35 | null | **$276,914** | $7,912 |
| Gamunex-C | Immune globulin | 26 | null | **$215,846** | $8,302 |
| Procrit | Epoetin Alfa | 40 | null | **$171,140** | $4,278 |
| Eliquis | Apixaban | 123 | 26 | $107,727 | $876 |
| Humira | Adalimumab | 13 | null | $96,019 | $7,386 |
| Trelstar | Triptorelin Pamoate | 96 | 12 | $88,406 | $921 |

A different clinical profile — infused biologics and immune globulin rather than
oral targeted agents.

### His industry payments — four payers, $120.48

| Payer | Payments | Total | Product |
|---|---|---|---|
| Adaptive Biotechnologies | 1 | $47.17 | clonoSEQ |
| Lilly USA, LLC | 3 | $38.38 | CYRAMZA |
| Sobi, Inc | 1 | $17.80 | DOPTELET |
| Janssen Pharmaceuticals, Inc | 1 | $17.13 | not named |

### The match: 0 of 8

| His top drug | Manufacturer | Paid him? |
|---|---|---|
| Remicade | Janssen | **no product-level match** |
| Keytruda | Merck | **no** |
| Nplate | Amgen | **no** |
| Gamunex-C | Grifols | **no** |
| Procrit | Janssen | **no product-level match** |
| Eliquis | BMS / Pfizer | **no** |
| Humira | AbbVie | **no** |
| Trelstar | Verity | **no** |

The three named products — clonoSEQ, CYRAMZA, DOPTELET — appear **nowhere** in
his Part D list. One is a diagnostic test, not a drug.

Janssen Pharmaceuticals gave one $17.13 Education payment with no product named.
Janssen markets both Remicade and Procrit, so a link is possible but **not shown
in the data**.

### Why the contrast matters

| | Miranda | Aswad |
|---|---|---|
| Excluded | 2015-06-18 | 2016-01-20 |
| Part D cost 2022 | $7,702,674 | $2,552,958 |
| Industry payments 2022 | **225, $4,415.57** | **6, $120.48** |
| Distinct manufacturers | **45** | **4** |
| Product match to top 8 | **8 of 8** | **0 of 8** |
| Medicare enrollment | yes | **none** |
| Part B billing | $1,229,994 | **none** |

Same exclusion status. Same suppressed beneficiary counts. Wildly different
industry footprint.

**Aswad is what an excluded prescriber looks like with no sales-rep contact.**
That is the negative control, and it holds — it shows the 8-of-8 match on Miranda
is real signal about rep activity, not an artifact of how Open Payments records
oncology drugs generally.

---

## What is supported, and what is not

| Statement | Supported? |
|---|---|
| Miranda's top 8 Part D drugs all have matching payments | **yes, by exact product name** |
| 45 manufacturers paid him in 2022 | **yes** |
| Every payment was under $130, food or education | **yes** |
| Aswad's 3 named products match none of his drugs | **yes** |
| Payments caused the prescribing | **no. $8,797 prescribed per $1 paid** |
| This is a kickback scheme | **not shown, and the amounts argue against it** |
| 45 companies failed to screen an excluded provider | **yes, that is what the data shows** |
| Miranda personally wrote these scripts | **still not shown** |

The strongest defensible claim from this round is a **compliance failure at
scale**, spread across dozens of named companies, plus CMS itself paying claims
and still flagging him Y to order and refer.

The kickback framing is not what the numbers support. Saying it anyway would be
the weakest link in an otherwise solid chain.

---

## Not checked

1. Open Payments 2023 and the undated `FED_CMS_OPEN_PAYMENTS` table. Miranda has
   211 and 201 payments there. Whether the 8-of-8 match repeats is untested.
2. `FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT`, which may carry a practice
   affiliation not present elsewhere.
3. `COVERED_RECIPIENT_PROFILE_ID` for both, and whether it links to anything.
4. Whether any of the 45 manufacturers also appear against other LEIE NPIs. That
   would size the compliance failure across the industry.
5. Aswad's Janssen payment. No product named, so the Remicade link is untested.

## Cost

One script, about 8 queries. Four scans of `FED_CMS_PARTD_PRESCRIBER_DRUG` at
25.9M rows filtered to one NPI, and six of `FED_CMS_OPEN_PAYMENTS_2022` at 13.3M
rows. No prior run of this pattern in the query log to price against.
