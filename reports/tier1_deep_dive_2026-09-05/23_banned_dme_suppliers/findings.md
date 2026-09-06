# Hunch 23 — how much money did banned DME suppliers collect?

First pass said: $1.4B collected by LEIE-excluded suppliers, one company $860M.
Second pass, 2026-09-05, Python door, SELECT only. Every query in `queries.py`, log in `queries.log`, raw results in `results.json`.

## The two files

| File | What it is | Rows | Date |
|---|---|---|---|
| `HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL` | Medicare's public DME supplier file. One row per supplier x product code (HCPCS). 55,598 suppliers. | 440,670 | **No year column. Landing ingested 2026-07-26.** |
| `HEALTH__FED_HHS_OIG_LEIE` | HHS Inspector General's exclusion list — people and companies banned from federal health programs. | 83,747 | Newest exclusion 2026-08-20; landing stamp decodes to 2026-08-27 |

NPI = National Provider Identifier, the ten-digit number every Medicare biller carries. It is the only key the two files share.

## What was checked

**1. Money.** The supplier file does not carry a total paid. It carries an *average* Medicare payment per service (`AVG_SUPLR_MDCR_PYMT_AMT`) and a service count (`TOT_SUPLR_SRVCS`, TEXT). Money = services x average, summed per supplier. Whole file: **$10.94B paid** ($14.26B allowed). `try_to_number` on the count returns null on zero rows.

**2. The match, on NPI.** LEIE rows kept only where `NPI_IS_REAL` and NPI is not blank and not `'0000000000'`. That leaves 8,839 rows, 8,660 distinct NPIs, out of 83,747. Joined to the supplier file on NPI.

**Hit: 8 suppliers.** Together **$1,425,018,337** — 13.0% of every DME dollar in the file. The other 55,590 suppliers split $9.52B with a median of $4,008 each.

| NPI | Supplier (file) | LEIE business name | State both sides | Paid | Excluded | Type |
|---|---|---|---|---|---|---|
| 1811518392 | Sunshine Senior Solutions, LLC | SUNSHINE SENIOR SOLUTIONS, LLC | FL | **$860.3M** | 2026-06-20 | 1128Aa |
| 1063414571 | JL Webb DME LLC | JL WEBB DME, LLC | KY | $116.1M | 2026-06-19 | 1128Aa |
| 1588302186 | Absolute Medical Supplies Services LLC | ABSOLUTE MEDICAL SUPPLIES SERV | PA | $109.4M | 2026-06-24 | 1128Aa |
| 1689457772 | Main Street DME, Inc. | MAIN STREET DME, INC | GA | $93.8M | 2026-06-28 | 1128Aa |
| 1528004108 | Southeastern Medequip, Inc. | SOUTHEASTERN MEDEQUIP, INC | FL | $87.5M | 2026-06-20 | 1128Aa |
| 1225009665 | Express Healthcare Inc | EXPRESS HEALTHCARE, INC | AL | $86.4M | 2026-06-19 | 1128Aa |
| 1578139473 | Lifeline Medical Supply, Inc | LIFELINE MEDICAL SUPPLY, INC | FL | $62.3M | 2026-06-20 | 1128Aa |
| 1063294221 | Temecula Medical Supplies | TEMECULA MEDICAL SUPPLIES, INC | CA | $9.1M | 2026-06-19 | 1128Aa |

1128Aa is a rare code with one shape: 172 rows in the whole LEIE, 25 dated 2026, 24 of those in the 19–28 June window, and all 24 are DME businesses (specialty DME-GENERAL / OXYGEN / ORTHOTICS / PROSTHETICS, in FL, TX, KY, NY, PA, GA, AL, CA, MS, CT, IL). The 8 hits are a subset of that one batch; the other 16 in the batch do not appear in the supplier file.

**3. Is the $860M company really excluded?** Yes. Matched on NPI 1811518392, one LEIE row, and the business name and state agree on both sides. Not a name match — the name was only checked afterwards as a witness.

**4. Rebuilt a different way.** Matched on business name instead of NPI (punctuation stripped, upper-cased). 30 name hits. Six of them are the same NPIs as above, **$1.31B — 92% of the $1.43B**. Two drop on the name route for mechanical reasons: Absolute Medical (LEIE truncates the name at 30 chars) and Temecula (LEIE carries an "INC" suffix the supplier file does not). The name route adds one real thing: **a second Express Healthcare Inc in Alabama, NPI 1871564211, $75.2M, same name and state, not on LEIE by NPI.** The other 22 name hits are pharmacies and podiatrists from the 1990s in different states — the generic-name trap, ignored. The number reproduces within the two explained drops.

**5. Is the exclusion date before the data year?** **No. This is the finding that flips the hunch.** All eight exclusions fall between 2026-06-19 and 2026-06-28. The payment file landed 2026-07-26 and CMS publishes this file a year or more after the calendar year it covers. The year is not in the file; whichever year it is, the billing came first and the ban came after. The exclusion list holds 8,129 real-NPI exclusions dated before 2026; **none of them appear in the supplier file.** That is expected, not a finding: only 520 of the 8,129 are organizations and only 33 of those carry a DME specialty (22 DME-GENERAL). The other 8,096 are individuals, pharmacies, home health agencies, clinics — entities that never bill this file. So the 0-of-8,129 says the file has no zombie suppliers among 33 candidates, nothing more.

**6. What the money was.** Two product codes.
- A4353, intermittent urinary catheter with insertion supplies: the eight took **$741M of $1,154M (64%)** and billed for 173,215 patients. The other 326 catheter suppliers combined billed for 71,935.
- A6197, large alginate wound dressing: **$402M of $649M (62%)**, almost all Sunshine.
- Sunshine alone: 45.1M catheters for 42,083 patients (1,071 each), 23.9M dressings for 48,325 patients, plus knee, wrist and back braces and glucose monitors — 8 codes.
- Per-patient catheter volume does not separate them from honest suppliers (median 734 vs 1,065 a year). Patient count does.

## What a hit means / what a miss means

- A hit on NPI means the same billing entity is on both lists. It does not by itself say the payments were fraudulent; the 1128Aa type says a conviction happened.
- A miss (an excluded supplier absent from the file) means either they billed nothing that year, or the file's year predates their entry, or their NPI in LEIE is blank or the sentinel — 74,908 of 83,747 LEIE rows have no usable NPI, so people excluded without an NPI on record can never match here.

## What a skeptic would attack

- **"Still collected" implies billing after the ban.** It does not. Every date is after the data. Fixed in the headline.
- **The file year is unknown.** True. No column, registry row blank. Stated everywhere as "ingested 2026-07-26". If the file is CY2024 or CY2023 the story is the same either way: the ban is June 2026.
- **Money is services x average, not a published total.** Rounding on the average is per row; the whole-file $10.94B is consistent with Medicare DME spend of that size. Allowed-amount route gives $14.26B, same ranking.
- **"The ones who collected the most got banned" — not quite.** The pattern is wider than the ban. At least three unbanned suppliers bill the same way on A4353: Almaz Med Supply (NY, NPI 1487343505, rank 2 in the whole file at $473M, $206M of it catheters, 1,738 catheters per patient), ND Medical Solutions (PA, $88M catheters, 41,606 patients), and the Express Healthcare twin (AL, $75M). $370M of catheter money sits outside the eight. The ban caught a batch, not the pattern.
- **Sunshine's $860M could be a data error.** Eight separate rows, each internally consistent (benes, services, average), and the company sits on the exclusion list for a program crime. Not an error.
- **Name-only twin.** Express Healthcare Inc, NPI 1871564211, $75M, is not counted. Counting it would need proof it is the same company. Parked, not added.

## Traps hit
- LEIE `_INGESTED_AT` in the mart is epoch-microseconds-as-seconds (year 56,656,460); the Python connector throws on fetch. Read it with `to_varchar`, or decode the landing `INGESTED_AT` integer.
- LEIE landing: 75,001 `'0000000000'` NPI sentinels and 77,887 blank UPINs — the mart nulls the sentinel and sets `NPI_IS_REAL`.
- Supplier landing `_SOURCE_RUN_ID` is unique per row (440,670 values) — it is not a run id, do not group by it.
- Supplier mart has no `_INGESTED_AT`; the ingest date lives only on the landing table.

STATUS: confirmed but reframed
HEADLINE: 8 DME suppliers now on the OIG exclusion list were paid $1.43B — 13% of all Medicare DME dollars in the file — with Sunshine Senior Solutions (FL) alone at $860M; all 8 were banned in June 2026, after the billing, not before.
