# The Molina $114,040 — 2026-09-05

Queries through the Python door, `connect/db.py`. Script: `scratchpad/hunt26.py`.
NPI `1982679544`.

**Headline: nobody cut him a cheque. The record is a bad-debt write-off. Skye
Orthobiologics forgave $114,040 owed by a third-party entity, Del Sol Medical,
and CMS attributes it to Molina as the covered recipient. No product is named,
because none is involved.**

**The bigger find is the company. Skye Orthobiologics wrote off $7,195,734.55
across 30 providers in 2024, and one of those write-offs is $3,082,225 to
Alexander Frank — the same NPI that topped our very first ghost-doctor query.**

---

## The table question, settled first

There is no `FED_CMS_OPEN_PAYMENTS_2024`. The undated table is 2024:

```sql
select PROGRAM_YEAR, count(*) from FED_CMS_OPEN_PAYMENTS group by 1;
→ ('2024', 15,385,047)
```

**`FED_CMS_OPEN_PAYMENTS` is PY2024, single year, no mixing.** That closes an
open item from the earlier reports, which listed it as undated.

| Table | Program year | Rows |
|---|---|---|
| `FED_CMS_OPEN_PAYMENTS_2022` | 2022 | 13,306,564 |
| `FED_CMS_OPEN_PAYMENTS_2023` | 2023 | 14,700,786 |
| `FED_CMS_OPEN_PAYMENTS` | **2024** | 15,385,047 |

---

## The record, in full

`RECORD_ID` 1075873943.

| Field | Value |
|---|---|
| NPI | 1982679544 |
| Recipient | Molina, Hector |
| `COVERED_RECIPIENT_PROFILE_ID` | 561763 |
| Specialty | Allopathic & Osteopathic Physicians / General Practice |
| Recipient address | 6070 Gateway Blvd East, El Paso, TX |
| **Payer** | **Skye Orthobiologics LLC** |
| Payer ID | 100000226833 |
| Payer state | CA |
| Submitting entity | Skye Orthobiologics LLC — same company |
| **Amount** | **$114,040.00** |
| Payments in total | 1 |
| Date of payment | **2024-01-22** |
| Publication date | 2026-01-23 |
| Form of payment | Cash or cash equivalent |
| **Nature of payment** | **Debt forgiveness** |
| **Contextual information** | **"Bad Debt"** |
| Third-party recipient indicator | **Entity** |
| **Third-party receiving the value** | **Del Sol Medical** |
| Physician ownership indicator | No |
| Charity indicator | No |
| Dispute status | No |
| **`RELATED_PRODUCT_INDICATOR`** | **No** |
| Product named | **none** |

### Answering the three questions directly

**1. The payer.** Skye Orthobiologics LLC, a California entity, manufacturer ID
100000226833. It both submitted and made the payment — no GPO intermediary.

**2. The nature.** **Debt forgiveness.** Not a royalty, not consulting, not
research, not a speaking fee. The free-text `CONTEXTUAL_INFORMATION` says
**"Bad Debt"** in plain English.

**3. The product.** **None.** `RELATED_PRODUCT_INDICATOR` is `No` and every
`NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_n` field is empty. A
write-off is not attached to a product because it is not a sale.

### What actually happened, in plain words

Skye shipped product to **Del Sol Medical**. The bill went unpaid. Skye gave up
on collecting and wrote it off. Federal law makes a manufacturer report forgiven
debt as a transfer of value, attributed to the physician associated with the
account.

**Molina received no money.** He received relief from an obligation his practice
entity owed. That is a real transfer of value and it is correctly reported — but
it is not a six-figure cheque, and describing it as one would be wrong.

---

## Identity check — solid on NPI, loose on address

| Source | Name | Address | City |
|---|---|---|---|
| `FED_HHS_OIG_LEIE` | MOLINA, HECTOR OSCAR | 344 Marine Forces Drive #4947 | Grand Prairie, TX |
| `FED_CMS_NPPES` | MOLINA, HECTOR, MD MS | 1140 Empire Central Dr Ste 360 | Dallas, TX |
| `FED_CMS_OPEN_PAYMENTS` | Molina, Hector | 6070 Gateway Blvd East | **El Paso, TX** |

**Three different Texas cities.** The NPI matches exactly in all three and the
name matches, so this is one person by identifier. The addresses are 600 miles
apart, which is unusual and worth noting before publication.

The El Paso address is consistent with Del Sol Medical, which operates there.

### Exclusion

Excluded **2019-06-20** under `1128a1` — mandatory exclusion for conviction of a
program-related crime. Never reinstated. The write-off is dated 2024-01-22,
**four and a half years later.**

### His whole footprint is four tables

`FED_CMS_NPPES`, `FED_CMS_OPEN_PAYMENTS`,
`FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT`, `FED_HHS_OIG_LEIE`.

**No Medicare enrollment. No Part B. No Part D.** Same shape as Aswad — an
excluded provider with no federal billing trail in this warehouse.

---

## The company is the real lead

Skye Orthobiologics LLC, all 2024 Open Payments activity:

| Nature | Records | Total |
|---|---|---|
| **Debt forgiveness** | **30** | **$7,195,734.55** |
| Speaking or faculty compensation | 7 | $12,000.00 |

**99.8% of what this company reported to CMS in 2024 is bad debt.** Seven
speaking fees, thirty write-offs.

### All 30 write-offs

| Provider | NPI | Third-party entity | ST | Amount | Date |
|---|---|---|---|---|---|
| **Frank, Alexander** | 1164450573 | Previse Medical | OK | **$3,082,225.00** | 2024-01-15 |
| Carrington, Leah | 1629453030 | Enhanced Healthcare of the Ozarks | AR | $1,619,275.55 | 2024-12-30 |
| McGee, Dodie | 1124522909 | Choice Wound Care | MS | $772,115.00 | 2024-12-30 |
| Desai, Alpesh | 1386696904 | Heights Dermatology & Aesthetic Center | TX | $573,060.00 | 2024-11-01 |
| Jaafar, Fadi | 1679837504 | Precision Foot & Ankle Institute | MI | $167,400.00 | 2024-12-31 |
| Igbokwe, Eberenne | 1003102732 | EFIgbokwe, PLLC | TX | $123,750.00 | 2024-07-29 |
| Klein, Jeffrey | 1447357959 | Klein Foot Care Center | MI | $114,085.00 | 2024-12-31 |
| **Molina, Hector** | 1982679544 | **Del Sol Medical** | TX | **$114,040.00** | 2024-01-22 |
| De La Concepcion, Ludmila | 1467846295 | Blue D Class Medspa and Research | FL | $100,800.00 | 2024-12-01 |
| Brandwein, Daniel | 1679561849 | — | FL | $70,200.00 | 2024-11-12 |
| Burhani, Hatim | 1366698524 | Eastside Podiatry PLLC | MI | $69,600.00 | 2024-06-28 |
| Cabrera Lopez, Anibal | 1790311454 | AOC Healthcare Center | FL | $64,400.00 | 2024-08-16 |
| Zarate, Herman | 1861445884 | Capital Footcare | MD | $52,981.76 | 2024-12-23 |
| Smedley, Jonathan | 1679535553 | Precision Podiatry | TX | $36,000.00 | 2024-05-21 |
| Gheiler, Edward | 1750347753 | Palmetto Lakes Surgical Center | FL | $35,920.00 | 2024-01-02 |
| Richardson, William | 1649231424 | Natura Dermatology and Cosmetics | FL | $32,571.00 | 2024-12-24 |
| Strauss, Neil | 1053319145 | Advanced Foot, Ankle, and Wound Specialists | FL | $29,930.00 | 2024-08-05 |
| Geskin, Gennady | 1053319434 | US Wound and Vascular | PA | $29,088.00 | 2024-12-31 |
| Sadri, Soorena | 1578792339 | FootWorx Active Podiatry | FL | $24,993.24 | 2024-10-31 |
| Jaafar, Fadi | 1679837504 | Podiatry Professionals of Michigan | MI | $20,400.00 | 2024-06-21 |
| Kirby Ware, Ashley | 1912258450 | Ware Family Practice | MS | $14,000.00 | 2024-10-15 |
| Rivera, Orlando | 1720016827 | Rivera Foot and Ankle | TX | $12,200.00 | 2024-05-01 |
| Lee, Yueh | 1962472571 | Advanced Foot and Ankle Specialists | TX | $9,400.00 | 2024-11-20 |
| Das Wattley, Sharmila | 1164420907 | — | FL | $8,000.00 | 2024-09-16 |
| Alabi, Nathaniel | 1609308592 | Texas Heart and Vein Multi-specialty Group | TX | $6,600.00 | 2024-05-30 |
| Sandhu, Neil | 1134389364 | Annexus Dermatology & Aesthetics | FL | $4,800.00 | 2024-11-15 |
| Massey, Brad | 1164537445 | Conxcare | MS | $3,400.00 | 2024-08-09 |
| Thomson, Matthew | 1487893533 | Foremost Podiatry | MI | $2,240.00 | 2024-04-03 |
| Cross, Warren | 1437173663 | Cross Eye Centers | TX | $1,435.00 | 2024-08-06 |
| Isenberg, Mark | 1154328177 | Center for Podiatric Excellence | FL | $825.00 | 2024-12-03 |

### The pattern in that list

| Signal | Reading |
|---|---|
| **17 of 30 are podiatrists or wound-care providers** | one product line, one specialty |
| **FL 11, TX 7, MI 5, MS 3** | geographically clustered |
| **Fadi Jaafar appears twice** | two entities, $187,800 combined |
| **11 write-offs land on 2024-12-30 or 12-31** | year-end book-clearing |
| **Top 4 are 84% of the total** | $6,046,675 of $7,195,735 |

Skye Orthobiologics sells amniotic and placental tissue allografts. Those are
billed to Medicare at high per-unit prices in wound care. **A supplier writing
off $7.2M owed by wound-care practices is either a collapsed sales channel or a
consignment arrangement that was never going to be paid.** Which one is not
answerable from this table.

### Two of the 30 are on the exclusion list

| Provider | NPI | Statute | Excluded | Write-off date | Order |
|---|---|---|---|---|---|
| **MOLINA, HECTOR** | 1982679544 | 1128a1 | **2019-06-20** | 2024-01-22 | **after exclusion** |
| **FRANK, ALEXANDER** | 1164450573 | 1128a2 | **2025-08-20** | 2024-01-15 | **before exclusion** |

**Alexander Frank is the name that topped our very first ghost query** — $10.7M
in Part D drug cost, the largest of the 554. He received a **$3.08M** write-off
from Skye in January 2024 and was excluded nineteen months later, in August 2025,
under `1128a2`.

The write-off **predates** the exclusion, so it is not a post-exclusion payment.
It is something arguably more interesting: **the largest single transfer of value
in this company's entire 2024 filing went to a doctor the government barred the
following year.**

---

## What is supported

| Statement | Supported? |
|---|---|
| The $114,040 is debt forgiveness, not a payment | **yes, field and free text** |
| The payer is Skye Orthobiologics LLC | **yes** |
| No product is named | **yes, indicator is No** |
| The value went to Del Sol Medical, an entity | **yes** |
| `FED_CMS_OPEN_PAYMENTS` is PY2024 | **yes** |
| Skye wrote off $7,195,734.55 across 30 providers | **yes** |
| Frank got $3.08M and was excluded 19 months later | **yes** |
| Someone cut an excluded doctor a six-figure cheque | **no. This is a write-off** |
| The write-offs are improper | **not shown. Reporting them is the legal requirement** |

---

## Not checked

1. Whether Del Sol Medical in El Paso links to Del Sol Medical Center, the
   hospital. Name only, no identifier.
2. Frank's $3.08M against his $10.7M Part D prescribing. Different years, but the
   two are worth putting side by side.
3. Whether the other 28 providers have Part B or Part D volume matching the size
   of their write-off.
4. Skye Orthobiologics in SAM, USAspending, or as an FDA tissue establishment.
5. Molina's three addresses. The 600-mile spread is unexplained.

## Cost

One script plus three ad-hoc query sets against `FED_CMS_OPEN_PAYMENTS` at 15.4M
rows, mostly filtered to one NPI or one payer. Small. No prior run of this
pattern in the query log to price against.
