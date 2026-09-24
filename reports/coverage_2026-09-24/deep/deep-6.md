# Deep pass 6: five health tables

2026-09-24. Python door, query tag `coverage-b-2026-09-24`, read-only.
SQL: `reports/coverage_2026-09-24/deep/deep-6.sql`, 27 queries plus 8 session-setting statements = 35.

Every person, company and hospital named below is a **data match, not verified against primary records**.

---

## The menu

| Table | Verdict | The number |
|---|---|---|
| CMS opt-out affidavits | **live** | CA counselors + family therapists: 4,890 opted out, 199 billed 11+ Medicare patients in 2024 |
| Part D prescribers 2024 | probed | Top names are volume and specialty artifacts; 292 prescribers on the OIG ban list, 1 banned before 2024 and he has a waiver |
| HRSA Provider Relief Fund | probed | **The exclusion angle is dead:** $100K went to providers barred before payment, out of $135B. One lead: a 25-bed Utah hospital took 2.45x its 2019 revenue |
| FDA MAUDE 2020-21 | probed | LVAD deaths lead by design. Nevro's spinal stimulator has 69% of its device type's deaths on 1.7% of the reports, and none of them flag a device problem |
| FDA device recalls | probed | 64 Class I recalls open longer than 90% of closed ones took; 14 are one heart pump still implanted in patients |

---

## 1. HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS: **live**

**Headline:** California's counselors and family therapists turned Medicare down at 2.3x the rate of its psychologists and social workers.

**The premise needed a fix first.**
Triage said "mental-health providers are leaving Medicare." ➔ Counselors were never in: the benefit started January 2024. ➔ The right mechanic is "declined to join," not "left."

### What the file is
- 57,101 rows, 56,455 NPIs. Every OPTOUT_END_DATE is 2026-06-30 or later.
- So it's a **snapshot of who is opted out now**, not a history. The effective date is the first opt-out; renewals are automatic and don't add rows.
- Anyone who opted out and later came back into Medicare is gone from the file.

### Checked
1. Opt-outs by specialty and start year.
2. Counselor (MHC) and family-therapist (MFT) opt-outs by month, July 2022 to 2026.
3. By state: opt-outs next to PECOS billing enrollments and 2024 Part B billers, for MHC+MFT. Peers are psychologists + clinical social workers in the **same state**.

### The numbers
- MHC 7,710 rows, MFT 6,778. **99.8% started in 2024 or later.**
- January 2024 alone: 5,114 (1,826 MHC, 3,288 MFT). By 2026 the rate is down to about 150-210 a month combined. It was one wave at launch.

Opt-out share = opted out ÷ (opted out + PECOS billing enrollments). "Order and refer only" enrollments don't bill, so they're left out.

| Place | MHC+MFT opt-out share | Psych+CSW opt-out share | Ratio | MHC+MFT opted out | MHC+MFT who billed 11+ patients in 2024 |
|---|---|---|---|---|---|
| US | 14.1% | 9.5% | 1.5x | 14,409 | 3,458 (87,302 patients) |
| CA | **35.8%** | 15.6% | 2.3x | 4,890 | **199** (4,511 patients) |
| WA | 32.4% | 19.8% | 1.6x | 1,114 | 63 |
| OR | 18.7% | 12.0% | 1.6x | 445 | 42 |
| AL | 23.6% | 9.4% | 2.5x | 155 | 26 |
| VT | 20.5% | 5.5% | 3.7x | 147 | 36 |
| MS | 16.7% | 3.2% | 5.1x | 84 | 23 |
| OH | 4.3% | 3.1% | 1.4x | 164 | 126 |

- Opt-outs per 2024 biller: **4.2 nationally for MHC+MFT, 0.54 for psych+CSW.** California: 24.6.
- CA holds 34% of the nation's MHC+MFT opt-outs.

### Hit means
Counselors and therapists refuse Medicare far more than their peers in the same state. The 2024 benefit has names on paper but few people seeing seniors, worst on the West Coast.

### Miss means
If the rates matched their peers, opting out would just be the normal cash-pay default. No story specific to counselors.

### Boring explanation, and what's ruled out
- **Not ruled out: first-year ramp.** 2024 was the first year counselors could bill. Part B hides anyone with fewer than 11 patients, so 3,458 billers is a floor.
- **Not ruled out: market.** CA and WA have large private-pay therapy markets. Low Medicare rates are the known cause, and trade press has covered it.
- **Ruled out:** that opt-out is just a first paperwork step toward enrolling. Only **1 NPI** appears on both the opt-out list and PECOS.
- **Ruled out:** renewal double-counting. Renewals don't add rows.

### Next pass
- Seniors per billing counselor by state. No 65+ population table turned up in the catalog.
- County level from ZIP_CODE. The file has no county column.
- CA split into MHC vs MFT.

---

## 2. HEALTH__FED_CMS_PART_D_PRESCRIBERS: probed

**Headline:** The top opioid and antipsychotic names are volume and specialty artifacts. Of 292 prescribers on the OIG ban list, 291 were banned in 2024 or later, and the one earlier ban has a waiver.

### What the file is
- 1,416,883 NPIs, one row each. DATA_YEAR is 2024 on every row.
- The antipsychotic suppression flag holds only `*` or blank. The 65+ totals flag holds `#` (298,276 rows), `*` (37,285) or blank. No non-numeric junk in the count columns.

### Checked
1. **Long-acting opioid claims, ranked against the specialty's own top 1%.** The cutoff is the 99th percentile among prescribers in that specialty with any long-acting claims.
2. **Antipsychotic claims for patients 65+,** ranked by count. Then by *share of 65+ claims* inside a nursing-home-scale band: non-psych prescribers with 30,000+ claims for patients 65 and up.
3. **Every Part D NPI joined to LEIE on NPI,** with last name as the second field.

### The numbers
- 67,613 prescribers wrote any long-acting opioid; 1,673 wrote 500+. 19,377 wrote 500+ opioid claims of any kind.
- **Family practice:** the top-1% cutoff is 231 long-acting claims. Bruce Mackey (Edmond OK) wrote 2,289, which is 9.9x. Stephen Kelly (Oklahoma City) 2,124; Rene Pulido (Jacksonville FL) 1,855; Sabera Shabnam (Branson MO) 1,853.
  - Mackey's opioids are 7,481 of his 9,430 claims (79%). That's a pain practice filed under family medicine.
- **Antipsychotics:** non-psychiatrists wrote **78%** of the 14.2M claims for patients 65+ (11.1M).
  - The national #1, Robert Pearlstein (Plymouth Meeting PA), has 17,107 antipsychotic claims. But he has **351,254 claims for patients 65+**, and his antipsychotic share is 4.9%, about the band's 90th percentile. The rank comes from volume.
  - Band (904 prescribers): median share 2.08%, 90th percentile 4.29%, 99th percentile 7.03%.
  - Top of the band: Kermys Rodriguez Roche (Santa Isabel PR) 15.3%, 7.3x the median; Maria Bernal NP (Miami) 11.8%; Chandra Anand (Chicago) 10.1%, whose patients average 63 years old.
- **LEIE:** 292 NPI matches, 283 with the last name agreeing (97%).
  - Banned before 2024: 1. Banned during 2024: 54. Banned after 2024: 237.
  - The one pre-2024 ban: Eduardo Miranda (Laredo TX), banned 2015-06-18 under 1128a1, with $7.5M of 2024 drug cost. His LEIE row has **HAS_WAIVER = True**. That explains it.
  - Four names from the top lists were banned later:
    - Nathan Hanflink (Eustis FL): #60 on opioids, #64 on long-acting. Banned 2026-04-30 under 1128b7, fraud and kickbacks.
    - Lawrence Peters (Louisville KY): #217 on long-acting. Banned 2025-06-19 under 1128a4, a controlled-substance felony.
    - Alexander Frank (Oklahoma City): #409 on antipsychotics. Banned 2025-08-20 under 1128a2, patient abuse or neglect.
    - Randall Berinhout (Stockbridge GA): #839 on opioids. Banned 2025-06-19 under 1128a1.

### Hit means
Named prescribers far above their peers who were also banned, and still paid, would be an enforcement-lag story.

### Miss means
The top lists are pain practices and nursing-home volume. That's the known, well-worn prescriber-list story.

### Boring explanation, and what's ruled out
- **Ruled in:** pain practices filed as FP/IM; nursing-home doctors carry enormous volumes; psych-heavy patient panels in PR, Miami and Chicago.
- **Ruled out:** rate columns hitting 100 on tiny denominators. I ranked on counts and on shares inside a volume band, not on OPIOID_PRSCRBR_RATE.
- The "banned later" angle is real but thin: 2 of the top 1,000 long-acting prescribers, against 292 of 1.42M overall. That's about 10x the base rate, but on two people.

---

## 3. HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND: probed

**Headline:** **The exclusion angle is dead.** Relief tracked revenue. One lead survives: a Utah hospital with 40 nursing homes under its name.

### What the file is
- 419,846 payee lines, $135.06B, file dated 2025-03-28. Name, city, state and amount only.
- 130 lines of $100M or more hold $25.6B (19%). Payees with hospital-type names: 6,587 lines, $59.8B (44%).

### Checked
1. **Exclusions:** payee NAME_KEY + state against LEIE (all rows) and SAM (every agency but HHS), both cleaned with the same key rule. City is the second field. The exclusion date is compared with 2020-04-10, when payments started.
2. **Hospitals:** payee key + city + state against FY2019 cost reports (HCRIS). Measured paid ÷ 2019 net patient revenue, and paid per bed, by quintile of Medicaid-day share. Short-term hospitals only.
3. For outliers: count SNF enrollments filed under the hospital's own name in the same state.

### The numbers
- Exclusion matches: 491 lines. **City agrees on 111 lines, $12.5M,** which is 0.009% of the fund.
  - **Barred before payment, city agrees: 14 lines, $100,322.** Largest: New Life Rheumatology Center LLC (Clifton NJ), $58,040.
  - Banned after taking the money, organizations: 47 lines, $11.2M. Examples: Gamma Healthcare (Poplar Bluff MO) $1.47M, banned 2024; Maison De'Ville Nursing Home (Houma LA) $1.09M, banned 2022.
  - LEIE person matches barred before payment: the city differs on 220 of 228 (SAM: 170 of 175). Namesakes, the known collision.
- Hospitals: 1,501 matched from 6,036 FY2019 reports; 780 short-term hospitals usable, $20.7B.

| Medicaid-day quintile (short-term) | Paid ÷ 2019 net patient revenue | Median $ per bed |
|---|---|---|
| 1 (least Medicaid) | 7.0% | $114,782 |
| 2 | 7.2% | $117,272 |
| 3 | 7.8% | $122,655 |
| 4 | 8.8% | $121,969 |
| 5 (most Medicaid) | 8.2% | $124,800 |

- Flat. If anything, safety-net hospitals got a little more per dollar of revenue.
- Critical-access hospitals: median 19.8% of revenue, against 8.2% for short-term hospitals. That's the rural tranche working as designed.
- 52 matched hospitals got more than 50% of their 2019 revenue; 6 got more than 100%. 33 of the 52 are critical-access; 12 are in TX and 12 in KS.
- **Lead:** Beaver Valley Hospital (Beaver UT), 25 beds, took **$22.3M, 2.45x** its 2019 net patient revenue of $9.1M. **40 SNF enrollments in Utah carry its name.** The relief was likely sized on the nursing homes.
  - Only 5 of the 52 have nursing homes under the same name, so this explains a few, not the pattern.

### Hit means
Barred providers cashing big checks, or rich hospitals paid more per bed, would be the story.

### Miss means
Tiny hits and flat ratios mean the formula worked as written.

### Boring explanation, and what's ruled out
- **Ruled in:** the payment formula followed revenue, which the flat 7-9% shows. Name-only matching collides.
- **Match bias:** health systems paid under a system name don't match one hospital, so the matched set leans toward standalone hospitals.

---

## 4. HEALTH__FED_FDA_MAUDE: probed

**Headline:** LVADs top the death reports by design. The one sharp outlier, Nevro's spinal stimulator, has zero device-problem flags on its 168 death reports, which points at reporting practice.

### What the file is
- 2,743,561 rows. Received 2020-01-01 to 2021-09-30, 21 months.
- Death: 15,013 rows, 14,985 reports. **3,131 death rows describe events before 2020.**

### Checked
1. Death and injury reports (distinct MDR_REPORT_KEY) by maker × product code, compared with **all makers in the same product code**.
2. For the outliers: device-problem flag, event-date age, and how many reports landed on a single day.
3. Injuries by brand: the peak month against the median month.

### The numbers

| Maker, device | Deaths | Death share of its reports | Same product code, all makers | Note |
|---|---|---|---|---|
| Thoratec, HeartMate 3 LVAD | 1,748 | 17.6% | 12.6% | 374 events before 2020 |
| HeartWare, HVAD | 1,242 | 9.1% | 12.6% | **98 death reports received on 2021-08-20** |
| Zoll, LifeVest | 617 | 3.3% | only maker | |
| **Nevro, Senza stimulator** | **168** | **22.8%** | rest of code: 76 on ~42,200 (0.18%) | **0 of 168 flag a device problem** |
| Spectranetics, Stellarex balloon | 158 | 39.7% | 27.1% | **147 of 158 events before 2020** |
| Medtronic, 630G pump | 160 | 0.4% | 97% of the code's deaths | 1 flags a device problem |

- Dexcom: **7 death reports.** The Dexcom angle is malfunction volume, not deaths.
- Injuries: Essure 18,838, peaking April 2020 at 5x its median month. HVAD injuries peaked June 2021 at 6.6x, the month sales stopped.

### Hit means
A maker with far more deaths than its own product-code peers, with device problems flagged and spread over time, would be device-specific harm.

### Miss means
The death share tracks the product code. That's volume and sick patients.

### Boring explanation, and what's ruled out
- **Ruled in:** LVAD patients die of heart failure. Stellarex deaths are retrospective trial reports; the paclitaxel signal is known from 2019. HVAD's deaths were batch-filed after the sales stop. Essure injuries are litigation-driven.
- **Open:** Nevro. It filed only 737 reports in total, 1.7% of its code, yet 69% of the code's deaths, and none flagged the device. Either Nevro reports every death it hears of and under-reports the rest, or the others skip deaths. Spinal stimulators were widely covered in 2023.

---

## 5. HEALTH__FED_FDA_DEVICE_ENFORCEMENT: probed

**Headline:** 478 Class I recalls are still open. 64 have run longer than 90% of closed ones took, and 14 of those are one heart pump that's still inside patients.

### What the file is
- 39,635 product rows. One recall event spans many rows; I counted distinct EVENT_ID.
- Ongoing Class I: **478 events, 1,735 rows, 199 firms**; 899 of the rows started in 2024 or later.

### Checked
1. Class I recalls with status Ongoing, per firm: events, oldest start, and days open up to the newest REPORT_DATE, 2026-07-29.
2. Peer yardstick: time from start to termination for 473 Class I recalls closed since 2012. **Median 733 days; 90th percentile 1,682 days (4.6 years).**

### The numbers
- **64 open Class I recalls are past 4.6 years.**
  - HeartWare/Medtronic HVAD 14; Maquet/Datascope balloon pumps 6; other Medtronic 6; BD CareFusion Alaris 5, plus 3 Alaris repair shops; Philips 4.
- Most ongoing Class I events by firm: Baxter 22, Philips 20, Abiomed 19, Boston Scientific 14, Datascope 14.
  - **Medline shows up as 13 + 12 under two spellings, 25 in total,** which would put it first.
- Oldest open recalls:
  - Philips Trilogy ventilator foam: started 2018-06-12, 8.1 years, 229,353 devices.
  - Allergan textured breast implants: started 2019-07-24, 7.0 years, 4.0M units.
  - Medtronic MiniMed 630G: started 2019-11-21, 6.7 years.

### Hit means
Firms whose "can kill" recalls stay open far longer than their peers': the fix never reached the devices.

### Miss means
Open times fall in the normal closing range. Nothing there.

### Boring explanation, and what's ruled out
- **Ruled in:** implants can't be pulled back. HVAD pumps, pacemakers and breast implants keep a recall "ongoing" while patients carry them. FDA also closes the paperwork slowly.
- Kit assemblers like Medline multiply the rows. Philips and HVAD are famous.
- **Sensitive:** 36 of the 64 started in 2021, right at the cutoff, so the count moves with the yardstick.

---

## Data traps found

- **Opt-out file is a snapshot, not a history.** Every OPTOUT_END_DATE is 2026-06-30 or later, and the effective date is the *first* opt-out. Counts by year mean "still opted out, by start year." Anyone who came back to Medicare has dropped out of the file.
- **PECOS mixes billing with order-and-refer.** PROVIDER_TYPE_DESC includes "ORDER AND REFERRING ONLY - …" rows. Filter to `PRACTITIONER%` before calling anyone in-network.
- **Recall firm names aren't normalized.** Medline appears under 2 spellings; HeartWare under 5 ("HeartWare Inc", "Heartware", "Heartware, Inc.", "HeartWare, Inc", "Heartware, Inc"). Counting by RECALLING_FIRM splits one company.
- **Recall start dates can be retrospective.** Abiomed event 98868 started 2011-01-17 and was classified 2026-05-28 ("Retrospective submission"). Check CENTER_CLASSIFICATION_DATE before quoting a recall's age. One Class II row starts in 1930.
- **MAUDE death reports aren't dated deaths.** 21% of death rows describe pre-2020 events, and batch days happen: HVAD filed 98 on 2021-08-20. PRODUCT_PROBLEM_FLAG is 'N' on most death reports.
- **Antipsychotic rank is volume.** The #1 prescriber has 351,254 claims for patients 65+. Rank on share within a volume band.
- **LEIE HAS_WAIVER is load-bearing.** A banned prescriber with a waiver can legally be paid. Check it before calling a banned-and-paid hit.
- **A relief-fund hospital payee can carry nursing-home money.** Beaver Valley Hospital (UT) has 40 SNF enrollments under its name and took 2.45x its revenue.
- Tooling: `ASOF` is a reserved word in Snowflake, so a CTE with that name fails to compile.
