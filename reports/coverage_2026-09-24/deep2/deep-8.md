# Deep pass 8: opioid shipments, cosmetic injury reports, device clearances, high-risk device approvals, drug recalls

2026-09-24. Python door, tag `coverage-r2-2026-09-24`.
**18 query statements**, all logged in `deep-8.sql`. Plus 12 session settings: 2 per connection, 6 connections.
Small tables were pulled whole and worked in pandas. ARCOS was rolled up in the warehouse first.
Every pharmacy, company or person named here is a data match, not verified against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| HEALTH__FED_DEA_ARCOS | **live** | Food City Pharmacy #674, Knoxville TN: 13.8M oxycodone pills of 30mg or more, 2006-12. That is 64% of its pills. Tennessee pharmacies average 8% | The #1 buyer of strong oxycodone among 84,334 US pharmacies was a supermarket pharmacy in Knoxville, not a Florida pill mill |
| HEALTH__FED_FDA_DEVICE_PMA | probed | 30-day notices went from 19% of approval changes (2000-04) to 64% (2010 on). Medtronic ICD P980016 has 928 changes, 621 of them 30-day notices | Real and big, but already studied. The recall join is dead. The MAUDE join works by product code, and deaths there follow how sick the patients are |
| HEALTH__FED_FDA_DRUG_ENFORCEMENT | probed | 442 Class I drug recall events since 2016. The top firm has 9. Sterile injectable makers run 33-35% Class I; all firms run 12.9% | There are no big repeat offenders. The injectables pattern is known |
| HEALTH__FED_FDA_DEVICE_510K | dead | The device recall table's K-number field is blank on all 39,635 rows | The join the angle needs doesn't exist. The table has no predicate column either |
| HEALTH__FED_FDA_CAERS | dead | Talc powder reports hold 26,490 of 26,542 death reports (99.8%) | The deaths are J&J talc lawsuits. The table holds cosmetics only, no foods or supplements |

---

## 1. DEA ARCOS opioid shipments: **live**

**What the table is.** 178,598,026 shipment rows, 2006-2012, hydrocodone and oxycodone only.
I kept `TRANSACTION_CODE = 'S'`. That drops the 5 junk rows from the sweep-two trap.
I rolled pills up by buyer and year in the warehouse (615,368 rows). All the ranking was done locally after that.

**Pharmacy universe.** 84,334 retail and chain pharmacies.
I dropped the 2 VA mail-order pharmacies: Charleston SC (512M pills) and Leavenworth KS (105M).

### The angle as posed: pills per county resident, per pharmacy

**Checked:** each pharmacy's pills per year, divided by its county's 2020 population, outside WV, KY and OH.

**What came back is noise from small denominators:**
- Norton VA is an independent city of 3,687 people. Its Walmart works out to 137 pills per resident per year.
- Home Oxygen Service in Kimball NE shows 167. That's one year of data in a county of 3,434.
- The two VA mail-order pharmacies top the raw list at 184 and 179.

**Also:** Connecticut buyers don't match `DIM_COUNTY`. That table uses the 2022 planning regions, and ARCOS uses the old counties.
675M Connecticut pills get no population.

**Verdict on this version:** dead. Per-capita at pharmacy level measures how small the county line is, not the pharmacy.

### The version that works: strong oxycodone, against state and chain peers

**Checked:** each pharmacy's oxycodone pills at 30mg or more, as a share of all its pills.
- Denominator: the pharmacy's total hydrocodone plus oxycodone pills, 2006-12.
- Peers: the pharmacy's own state, and its own chain.
- National share: 6.7% of pharmacy pills are oxycodone 30mg or more. Florida: 21.0%. Tennessee: 8.0%. Texas: 1.9%.

**Food City Pharmacy #674, Knoxville TN, ZIP 37919** (DEA BF7000526):
- 21,555,400 pills in 2006-12. That's 19.7x the median Tennessee pharmacy's yearly volume.
- 13,819,900 of them oxycodone 30mg or more, which is 64.1%.
- Its own chain runs 4.7% at the median store, across 96 Food City pharmacies.
- **#1 of 84,334 US pharmacies on oxycodone 30mg or more.** Ahead of every Florida store.
  - The next two are Fort Lauderdale's J & H Stores (13.0M) and Pembroke Pines' Generic Depot #2 (10.6M).
- It took 31.5% of all the strong oxycodone that went to Knox County's 141 pharmacies (43.9M pills).
- The product is immediate-release 30mg tablets, not a cancer-ward OxyContin mix:
  - 30mg immediate-release lines: 5.24M + 1.94M pills.
  - OxyContin 80mg: 1.60M pills.
- Supplier: AmerisourceBergen shipped 13,235,200 of the 13,819,900 (95.8%).
- By year, strong oxycodone ran 1.50M (2006), peaked at 2.46M (2008), then fell to 1.42M (2012).
- Store #694 in the same ZIP ran 59.5% strong oxycodone: 3.07M of 5.16M pills.
  - River City Pharma shipped the single biggest order of the year to #674 in 2009, and to #694 in 2009 and 2010.

**Other pharmacies outside Florida with the same profile:**

| Pharmacy | Pills | Strong oxycodone | Its state |
|---|---|---|---|
| Lam's Pharmacy, Las Vegas NV | 18.3M | 7.97M (43.6%) | NV 8.6% |
| The Hometown Pharmacy, New Castle PA | 7.64M | 5.02M (65.7%) | PA 8.5% |
| Briargrove Pharmacy, Houston TX | 7.07M | 3.96M (55.9%) | TX 1.9% |

- Briargrove grew from 53,800 strong pills in 2006 to 1.32M in 2011. Its main supplier was Morris & Dickson, with 3.55M.

**The distributor side.** I built an outlier set of 160 pharmacies. Each one:
- runs 40% or more strong oxycodone,
- sells 5x or more its state's median pharmacy volume,
- and moved at least 1M pills.

108 of the 160 are in Florida. Together they took 471.7M strong pills, 9.4% of the national pharmacy total.

| Distributor | Share of the outliers' strong oxycodone | Share of all pharmacies' strong oxycodone | Lift |
|---|---|---|---|
| H. D. Smith | 21.1% | 4.7% | 4.5x |
| River City Pharma | 9.8% | 1.9% | 5.2x |
| KeySource Medical | 5.0% | 1.0% | 4.8x |
| Sunrise Wholesale | 2.1% | 0.4% | 5.6x |
| AmerisourceBergen | 22.2% | 14.8% | 1.5x |
| Cardinal Health | 9.6% | 22.7% | 0.43x |
| McKesson | 9.2% | 24.1% | 0.38x |

**What a hit means.** A Knoxville supermarket pharmacy moved more street-dose oxycodone than any Florida pill mill.
It ran 64% strong pills while its own chain ran about 5%, and one national distributor supplied nearly all of it.
That's a named pharmacy, a named supplier and a seven-year trail.

**What a miss would have meant.** If the top of the list were only Florida, Kermit WV and mail-order, this would be the 2019 Washington Post story again.

**Boring explanations:**
- *It's a pain or cancer pharmacy.* Only partly ruled out. The mix is immediate-release 30mg, the street favourite, not long-acting cancer doses.
  - But the address is not in ARCOS, only the ZIP. A pain clinic or hospital next door would explain part of it.
- *It's public since 2019.* Not ruled out. The Post put pharmacy-level lookups online in 2019. Knoxville press may have covered this store.
  - The next pass must check press coverage and any DEA or Tennessee Board of Pharmacy action before calling it new.
- *The small-distributor lift is known.* Mostly yes. DEA went after several Florida-era secondary wholesalers around 2011-12. That part is color, not the lead.
- *QUANTITY angle (RW0294493 at 15.9M).* Ruled out as a story. RW0294493 is Walgreen Co's own distribution center in Perrysburg OH. QUANTITY counts packages, not pills.

---

## 2. FDA PMA high-risk device approvals: probed

**What the table is.** 56,853 rows: 1,743 PMAs and 55,380 supplements (later changes).

**Checked: the 30-day notice path.** Share of supplements that were 30-day notices, by decision year:

| Years | Supplements | 30-day notice share |
|---|---|---|
| 2000-04 | 2,928 | 19% |
| 2005-09 | 5,780 | 44% |
| 2010-14 | 11,166 | 62% |
| 2015-19 | 12,687 | 64% |
| 2020-24 | 11,059 | 65% |

- Median PMA: 14 supplements. The 99th percentile is 328.
- Top three are all Medtronic heart devices:

| PMA | Device | Changes | 30-day notices |
|---|---|---|---|
| P980016 | ICD | 928 | 621 |
| P010031 | InSync CRT-D | 897 | 614 |
| P980035 | Kappa pacing system | 817 | 593 |

- Peers, 30-day share of 2010-on supplements: Medtronic 74%, Boston Scientific 71%, Abbott 60%, Biotronik 46%.

**Checked: the recall join.** The device recall table's `PRODUCT_CODE` and `K_NUMBER_LIST` are blank on all 39,635 rows.
- I searched the recall text for P plus six digits.
- Only 13 recall rows (12 events, 2 of them Class I) name a PMA that lands in this table with the recalling firm agreeing.
- **The recall join is dead.**

**Checked: the MAUDE join by product code.** MAUDE here runs 2020-01-01 to 2021-09-30 only: 2.74M reports, 14,987 death reports.
- 99.3% of reports land on a 510(k) or PMA product code.
- Product codes found only in PMA hold 10,778 of the 14,987 death reports (72%).
- Top: ventricular assist pumps (DSQ) 3,033 deaths, catheter-placed aortic valves (NPT) 1,136, wearable defibrillators (MVK) 617.

**What a hit would mean.** The heaviest 30-day-notice devices also rack up the most recalls or deaths, beyond their peers.
**What the miss means.** Deaths follow the sickest patients (heart-pump patients), not the review path.
And recall rates can't be tied to a PMA at all.

**Boring explanation.** Long-lived pacemaker and defibrillator lines pile up manufacturing changes. Supplement counts on heart devices are a published research theme (from memory, not re-checked here).
**Ruled out?** No. It stands.

---

## 3. FDA drug recalls (enforcement): probed

**What the table is.** 17,876 recalled product rows = 4,643 recall events. Each event has exactly one recalling firm.
I counted distinct `EVENT_ID`, not rows.

**Checked:** Class I events per firm since 2016, the reasons, and Class I share against all firms.
- 3,432 events since 2016. 442 are Class I (12.9%).
- All 442 say "Voluntary: Firm initiated". None were ordered by FDA.

**Top firms by Class I events since 2016** (raw firm string):

| Firm | Class I events | Share of the firm's own events |
|---|---|---|
| Fresenius Kabi USA | 9 | 9 of 27, 33% |
| Pfizer Inc. | 9 | — |
| AuroMedics Pharma | 8 | 8 of 23, 35% |
| CareFusion 213, El Paso | 6 | fungus (Aspergillus) contamination, 2020-21 |

- AuroMedics' Class I reasons include glass, mold and rubber particles in injectable vials.
- 18 firms have 3 or more Class I events since 2016. Together they hold 76 of the 442 (17%).

**Class I reasons since 2016:**

| Reason | Class I events |
|---|---|
| Sterility or contamination | 182 |
| Undeclared drug in supplements (sex pills, weight loss) | 93 |
| Label mix-ups | 82 |

**The planned join (to Medicare and the VA):** not tried. No warehouse table lists VA or Medicare purchases by drug maker.
The NDC list (18% filled) could reach the Medicaid drug price survey (NADAC). But a recall pulls lots, not the whole NDC, so "still sold after the recall" is the expected answer.

**What a hit would mean.** One maker, or one plant, keeps having Class I recalls far above its peers.
**What the miss means.** The top firm has 9 in ten years. The excess is sterile injectables as a group, which is known.

**Boring explanation.** Injectable makers make more sterile products, and one bad vial triggers a Class I recall. Ruled in, not out.

---

## 4. FDA 510(k) device clearances: dead

**What the table is.** 175,686 clearances.
There is no predicate-device column, so the "predicate spawns recalled descendants" angle can't be asked here.

**Checked: the K-number join to recalls.**
- `K_NUMBER_LIST` and `PRODUCT_CODE` are blank on all 39,635 rows of HEALTH__FED_FDA_DEVICE_ENFORCEMENT.
- I pulled every K plus six digits from the recall description and lot text.
  - Most hits are lot numbers. One row alone holds 98,292 matches.
- Only 132 recall rows (65 events, 7 Class I rows) carry a K-number that lands here with the applicant matching the recalling firm.
  - That's 0.3% of recall rows.

**Fallback: firm-level name join** (first two words of the name).
- 87.9% of the 14,641 recall events since 2012 land on a 510(k) applicant. So do 85.3% of the 960 Class I events.
- Class I events since 2012, set against clearances since 2002:

| Firm | Class I events | Clearances |
|---|---|---|
| Datascope | 14 | 23 |
| Arrow | 11 | 22 |
| Hamilton Medical | 10 | 31 |
| Smiths Medical | 25 | 87 |
| Baxter Healthcare | 32 | 118 |
| Draeger Medical | 20 | 81 |

- The median firm has 0.

**What a hit would mean.** Specific cleared devices, or the devices they were cleared against, keep turning into Class I recalls.
**What the miss means.** This warehouse can't tie a recall to a clearance. The firm-level list is balloon pumps, infusion pumps and ventilators. Those are life-support machines, known for recalls.

**Boring explanation.** Device type drives Class I, and the big makers have long, public recall histories. Not ruled out.

---

## 5. FDA CAERS adverse event reports: dead

**What the table is.** 85,511 reports, one per report number, 2001 to 2025-08-29.
**It is cosmetics only.**
- Kratom, energy drinks, 5-Hour and Hydroxycut: 0 reports each.
- The word "supplement" appears on 7 reports.
- The catalog summary says foods, supplements and cosmetics. That's wrong.

**Checked:** deaths and hospital stays per suspect product, by year, before and after MoCRA (the 2022 cosmetics law).
- Reports naming talc or body powder: 71,583 of 85,511 (83.7%).
- They hold 26,490 of 26,542 death reports (99.8%) and 15,663 of 16,388 hospitalizations (95.6%).
- Top products are unmistakable:
  - "Johnsons powder no UPC": 13,820 death reports.
  - "J and J baby powder": 11,186.
  - "Shower to Shower no UPC": 8,815.
- Top reactions on death reports: ovarian cancer and mesothelioma.
- The MoCRA jump is J&J filing claims: 25,142 expedited 15-day reports in 2024, up from 158 in 2023.

**Everything that isn't talc: 13,928 reports.**
- 52 deaths in 25 years, and 725 hospital stays.
- Hospital stays: 38 in 2023, 79 in 2024, 48 in 2025 (to August).
- The single most serious non-talc product is SkinShift Vitamin C Serum, with 17 hospital stays.
  - All 17 were received on 2016-03-01 with the reaction "Adverse Reaction". That's a batch entry, not a cluster.

**What a hit would mean.** A non-litigation product drawing deaths or hospital stays out of line with its peers.
**What the miss means.** Outside talc, no product tops 5 serious reports except that batch entry.

**Boring explanation.** Lawsuit filings drive the reports. Confirmed, not just named.

---

## New data traps

- **Device recall table has no device keys.** HEALTH__FED_FDA_DEVICE_ENFORCEMENT has `K_NUMBER_LIST` and `PRODUCT_CODE` blank on all 39,635 rows.
  - K and P numbers in the text are mostly lot numbers. Only 0.3% of rows carry a real clearance number.
- **MAUDE is 21 months, not "2020 on".** HEALTH__FED_FDA_MAUDE runs 2020-01-01 to 2021-09-30. `BASELINE_510K_NUMBER` is blank on every row.
- **CAERS is cosmetics only, and 84% talc lawsuits.** The catalog says foods and supplements too. The 2024 jump is J&J's mandatory post-MoCRA filings.
- **ARCOS per-capita by pharmacy is a denominator artifact.** Independent cities like Norton VA (3,687 people) and one-year buyers top the list.
  - Connecticut buyers fail the `DIM_COUNTY` join (2022 planning regions). That's 675M pills with no population.
- **Drug recall rows are not recalls.** 17,876 rows = 4,643 events. `MANUFACTURER_NAME_LIST`, NDC and application number are each filled on about 18% of rows.
