# Deep pass 0: ER injuries, car complaints, car recalls, OSHA visits, single audits

2026-09-24. Python door, tag `coverage-b-2026-09-24`. **33 of 35 statements** (32 logged in `deep-0.sql`, plus 1 that failed at compile before the log started).
Every person or company named here is a data match. None is checked against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| ECONOMICS__FED_FAC_SINGLE_AUDIT | **live** | Lower Brule Sioux Tribe: going-concern doubt 10 of 10 years, material noncompliance 10 of 10, federal spend $16.7M → $35.7M | Auditors kept flagging a few groups every year, and the federal money kept growing |
| CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | probed | Jeep fuel system: 8 fatal complaints (25 deaths) sat 13.1 years before the 2014 recall | The method works, but it finds scandals that are already known. Death counts are padded by repeat filers |
| CONSUMER_SAFETY__FED_NHTSA_RECALLS | probed | Mercedes' 28.66B units is really 9.40M. One campaign repeats on 18,662 rows | The Mercedes lead is an artifact. On re-recalls, Tesla is 24% vs about 6% for its peers, and that's already known |
| CONSUMER_SAFETY__FED_CPSC_NEISS | probed | E-bikes and mopeds went 4.0x from 2019 to 2023 while all injuries went 0.95x | Real, but CPSC publishes it. Weights reset in 2024 and floors doubled in 2025 |
| ECONOMICS__FED_DOL_OSHA_INSPECTIONS | probed | California holds 30,245 of the accident and fatality inspections since 2015. Utah is next at 2,529 | The national "worst employers" list is really a California list |

---

## 1. FAC single audits: **live**

**Checked**
- 411,638 reports, one per REPORT_ID. 68,128 EINs. Audit years 2016-2026.
- The flags hold Yes, No or GSA_MIGRATION. 316 going-concern rows say GSA_MIGRATION, and all of them are 2022 Census rows.
- Rates are per audit report. Material weakness: tribal 22.8%, state 12.6%, local 11.4%, higher-ed 7.3%, non-profit 5.9%.
- I grouped by EIN and audit year, leaving out state entities, then counted the years that carry each flag.
- **Going concern 3+ years:** 362 of 48,202 auditees with 3+ audited years, or 0.75%.
- **Tribes:** 13 of 827 tribes with 3+ audited years have going concern in 3+ years.
- **Lower Brule Sioux Tribe** (EIN 460222351), row by row:
  - Going concern: every year, 2016-2025.
  - Material noncompliance: every year, 2016-2025.
  - Material weakness: every Census year, 2016-2022. It flips to No in the GSA FAC years, 2023-2025.
  - Opinions listed as qualified or adverse, 2019-2022.
  - Federal spend: $16.7M (FY2016), $35.3M (FY2022), $35.7M (FY2025). $246.2M over 10 years.
  - Auditor: REDW LLC every year since 2017.
  - Only 3 tribes with 5+ audited years reach 10+ going-concern-plus-noncompliance flag-years. Lower Brule has 20. The other two are Pine Ridge schools: Loneman at 12, Porcupine at 10.
- **Hope the Mission** (LA homeless-services nonprofit): going concern and material weakness in all 3 years, 2022-2024. $60.3M, $20.3M, $70.0M. Auditor Armanino.
- **Material weakness 5+ straight years:** 571 of 39,120 auditees with 5+ audited years, or 1.5%.
  - Tribes: 83 of 822, or 10.1%.
  - Local: 268 of 14,441, or 1.9%.
  - Non-profit: 180 of 22,009, or 0.8%.
  - Top names: Baltimore and Detroit (10 of 10, noncompliance 7), Atlanta 9/9, Navajo Nation 9/9, Three Affiliated Tribes 10/10 ($824.9M), LA County, LAUSD, Chicago Housing Authority.

**Hit means:** a named group got federal money every year while its own auditor doubted it could survive and flagged it for breaking the rules. For Lower Brule, the money more than doubled over that stretch.

**Miss means:** the flags would be boilerplate or artifacts. The row check on Lower Brule rules that out for that one group: one EIN, one name family, the same auditor, flags set every year.

**Boring:**
- Tribal self-determination, Medicaid and school money is mostly formula money. Agencies often can't cut it over audit flags. Not ruled out. That is the story's hinge.
- Top dollars in going-concern years belong to known cases:
  - Brazos Higher Education Authority, $24.9B: FFELP student loans winding down, and loan balances count as "expended."
  - Puerto Rico agencies, PROMESA era.
  - NYC safety-net hospitals: Jamaica 9/9, Wyckoff 9/9, St. Barnabas, Brooklyn Hospital, Maimonides.
- **Ruled out:** the 80% top-1% share is states. States are dropped here, but see the trap below.

**Traps**
- ⚠ **Material weakness rate doubles when the source system changes.** 5.2-6.2% on Census reports (2016-2022). 14.5% (2023) and 14.0% (2024) on GSA FAC. Late GSA FAC filers for 2016-2022 run 38-62%. A streak that crosses 2022→2023 is not like-for-like.
- 47 rows are typed `local` but named "State of ..." ("State of Arizona" shows 7/7 material weakness at $24.7B a year). Filtering out `state` does not remove all states.
- EIN 660433481 carries 8 different auditee names. One EIN is not always one group.
- There's no findings or questioned-costs table in the warehouse. "Repeat finding" and "questioned costs" can't be tested.

---

## 2. NHTSA complaints: probed

**Checked**
- 2,227,941 rows. 1,607,298 complaints (ODINO). A complaint that names several components gets several rows.
- **Deaths, counted once per complaint:** max per ODINO, with 99s dropped, gives 4,388 deaths on about 2,850 fatal complaints. The facts row said 8.6K. It counts each complaint once per component row, so it's about 2x too high.
- 99 sentinels: 17 death rows and 31 injury rows.
- Fatal complaints skew old: 1,679 filed before 2010, 721 since 2015.
- **The join:**
  - Complaints with any death or injury, matched to vehicle recalls on make + model + model year + component head. The head is the text before `:` and `,`.
  - Only complaints received before the recall's owner-notice date count.
  - Each complaint is counted once per campaign.
- **Top campaigns by fatal complaints received before the recall:**

| Campaign | Vehicle, part | Fatal before | Deaths | First fatal | Years ahead of recall |
|---|---|---|---|---|---|
| 19V182000 | Honda/Acura, air bags (Takata) | 21 | 23 | 2004-08-03 | 14.7 |
| 14V047000 | GM Cobalt family, air bags (ignition-switch set) | 13 | 21 | 2005-07-15 | 8.8 |
| 13V252000 | Jeep Liberty / Grand Cherokee, fuel system | 8 | 25 | 2001-07-04 | 13.1 |
| 24V153000 | Tesla, forward collision avoidance | 8 | 9 | 2014-07-10 | 9.8 |
| 22V817000 / 23V073000 | Freightliner Cascadia, service brakes | 5 | 5 | 2018-10-12 | 5.0 |

**Hit means:** complaints about dead people sat on file for years before the maker recalled that part. The top of the list is Takata, GM's ignition switch, Jeep's fuel tanks, Toyota's sudden acceleration and Tesla driver-assist. That shows the join works. It also shows the top is all known.

**Miss means:** nothing new sits above the known scandals. That's what happened.

**Boring, and what the spot check found:**
- A component match is loose. An air-bag death complaint can be about a bag that didn't deploy, not a Takata rupture.
- **Checked on text, 3 leads:**
  - Lincoln MKS "54 deaths" is one family filing the same 2 keyless-ignition deaths 7 times, plus one junk row with DEATHS = 40 that holds only a YouTube link.
  - Tesla Model S suspension's 11 fatal complaints read like one filer (same wording) posting crash-news links and junkyard listings. There's no filer ID to prove it's one person. One filing admits it used a wrecked car's VIN.
  - Freightliner's 5 are about brakes or braking systems, but one re-files another.
- **"Never recalled" doesn't hold up:**
  - Only 41.2% of fatal complaints match any vehicle recall on make + model + year.
  - The top "unrecalled" item, Ford Explorer tires with 82 fatal complaints, is Firestone. Firestone recalled the tires as equipment, so a vehicle-only filter misses it.
  - Absence is not a finding here.

**Traps**
- ⚠ Junk death counts under 99 exist (40 deaths, 38 injured on one link-only row). Dropping 99 is not enough.
- One filer can make up a whole "defect."

---

## 3. NHTSA recalls: probed

**Checked**
- 241,861 rows, 15,116 campaigns. POTENTIALLY_AFFECTED_UNITS holds one value per campaign in every campaign (0 exceptions). No campaign spans two makers.
- **Mercedes:** 28.66B summed over rows, 9.40M once per campaign.
  - Campaign 21V058000 alone has 18,662 rows × 1,292,258 units = 24.1B.
- **Real ranking, units counted once per campaign:**
  - The maker key is the first word of MFG_NAME.
  - Ford 94.3M (760 campaigns), Chrysler 73.0M, GM 71.1M, Honda 62.1M, Toyota 61.6M, Nissan 26.5M, Hyundai 22.6M. Mercedes 9.4M (392 campaigns).
- **Re-recalls:** the share of model-year + component combos recalled in 3+ separate campaigns. The denominator is combos recalled at least once.
  - Tesla 24.0% (81 of 338), Subaru 14.9%, Daimler 14.5%, Honda 13.3%, Ford 11.2%.
  - Hyundai 3.8%, Kia 2.9%, Volvo 3.0%.
- **Most re-recalled single combos:**
  - Altec "AERIAL DEVICE" MY2019, 21 campaigns.
  - Ford E-350 mobility conversions, 17.
  - Ford Maverick 2022 electrical, 14 (2022-2026).
  - **Freightliner Cascadia MY2019 service brakes, 13** (2018-08 to 2023-10).
  - Honda CR-V and Odyssey air bags, 12 (Takata).

**Hit means:** a maker keeps recalling the same part on the same model year, so each fix didn't hold. Cascadia is the cleanest case. It has 13 brake recalls on one model year, plus 5 fatal complaints filed before the 2023 recalls.

**Miss means:** the Mercedes lead is dead. It's rows repeating, not size.

**Boring:**
- Tesla has four models, and its software recalls land under one component head across many years. Tesla's recall count has been covered widely.
- Altec's "model" is a product category, not one model.
- The E-350 recalls come from different upfitters.
- Honda's repeats are Takata growing wave by wave.

**Traps**
- Maker names drift. GM appears as "General Motors LLC", "General Motors, LLC" and "GENERAL MOTORS CORP."; Chrysler under 3 names; Takata under 2.
- NOTIFICATION_DATE uses 1111-11-11 as a placeholder, and 3,962 rows are null.

---

## 4. CPSC NEISS: probed

**Checked**
- 9,794,971 rows, 1999-2025, weights on all but 194.
- I summed STATISTICAL_WEIGHT by product code and year. A case counts under any of its 3 product slots. Labels come from `EDUCATION__FED_CPSC_NEISS_CODES`.
- **The national total moves on its own.** All cases, weighted:
  - 2019: 13.46M
  - 2023: 12.74M
  - 2024: 15.07M (+18%)
  - 2025: 16.49M (+9%)
- **2024 is a weight reset, not more injuries.**
  - Sample cases rose only 7%.
  - Average weight per case: stratum S 74.6 → 106.7, V 16.9 → 27.6, M 81.3 → 55.0.
- **2025 floors surge:** code 1807 went 1.86M → 3.08M (+1.22M) in one year. It rose in every hospital stratum (S 645K → 1.05M, V 455K → 691K, L 389K → 665K). That's most of 2025's +1.42M. It looks like a coding change.
- **Codes split, so a new code fakes a new product:**
  - 5042 (powered scooters/skateboards) ends 2019 and becomes 5022 + 5025 in 2020.
  - 1329 (unpowered scooters) becomes 5023 + 5024.
  - 3215 (mopeds / power-assisted cycles) ends 2023 and becomes 5045 (e-bikes) + 5046 in 2024.
- **Joined-up series,** with 2019→2023 as the clean window before the weight reset. All injuries: 0.95x.

| Family | 2019 | 2023 | 2025 | 2019→2023 |
|---|---|---|---|---|
| E-bikes + mopeds (3215 → 5045 + 5046) | 21.8K | 87.6K | 134.4K | **4.0x** |
| Scooters + hoverboards (5042 + 1329 → 5022-5025) | 99.8K | 160.5K | 290.1K | 1.6x |
| Utility vehicles / UTVs (5044) | 4.9K | 14.9K | 14.3K | 3.0x (thin: 86 → 242 cases) |
| Tractors (1062) | 4.8K | 7.6K | 13.7K | 1.6x |
| Batteries (884) | 13.9K | 20.0K | 24.8K | 1.4x |

- **Who gets hurt, 2025, primary product:**
  - E-bikes (5045): 100.6K; 25% kids; 78% male; 14.9% admitted or held. Code 5046: 23.8% admitted.
  - Powered scooters (5022): 162.7K; median age 25; 13.3% admitted.
  - UTVs: 37% kids.
  - Batteries: 68% kids, median age 5.

**Hit means:** e-bike and moped ER injuries quadrupled while all injuries were flat. That's real, and big.

**Miss means:** anything that only rises in 2024-2025 can't be separated from the weight reset.

**Boring:**
- CPSC publishes the micromobility rise itself. Not a new find.
- UTVs are the less-told riser, but they rest on 86-242 sample cases.
- Not tested: magnets, water beads, gummies, cannabis. See the trap.

**Traps**
- ⚠ **NARRATIVE is blank on all 3,924,911 rows from 2015-2025.** There's no text to spot-check and no keyword search.
- ⚠ The 2024 weight reset and the 2025 floors jump. Any trend running through 2024 needs a same-design window.

---

## 5. OSHA inspections: probed

**Checked**
- 5,196,412 inspections, one per ACTIVITY_NR, 1970-2026. 861,985 since 2015. 80,073 have no close date.
- Types: A (accident) and M (fatality/catastrophe, since 2011). 60,050 since 2015.
- **By state:**
  - California: 30,245, almost all type A (26,721).
  - Next: Utah 2,529, Texas 2,441, North Carolina 2,408.
  - Texas, Florida and New York use M. California uses A.
- **Top employers,** names normalized, A+M since 2015:

| Employer | A+M | In CA | Notes |
|---|---|---|---|
| United Parcel Service | 107 (+28 as "UPS") | 81 | 32 still open |
| Sierra Pacific Industries | 62 | 61 | 67% of its inspections are accident-type, 16 sites |
| Walmart | 54 (+24 as "Walmart Stores") | 37 | |
| Safeway | 53 | 50 | |
| Foster Poultry Farms | 47 | 47 | 13 in 2020-21 |
| Tesla | 44 | 43 | **18 still open; median 486 days to close**. Most of the top 12 run 139-251; Kaiser 456 |
| Kaiser | 36 | 36 | 24 in 2020-21, the COVID years |

- **Open 5+ years:** 9,809 of 464,524 inspections opened 2015-2020 (2.1%) still have no close date. The top of that list:
  - A name fragment, "DE", in Puerto Rico.
  - "TESTING OIS 2": 21 test rows across 20 states.
  - Small Maryland contractors with 60-100% of cases open. That looks like a state-plan artifact.

**Hit means:** one employer keeps drawing accident inspections at many sites, measured against peers in its own state.

**Miss means:** the national ranking says nothing. It's a California list.

**Boring:**
- In California, type A likely covers serious-injury reports, not just deaths. This table can't prove that; the accident table would.
- Big employers have more sites.
- There's no headcount denominator: NR_IN_ESTAB is junk, as the facts row says.
- **Not ruled out.** The next pass is the 300A join (hours, deaths) inside California.

**Traps**
- ⚠ "TESTING OIS 2" test inspections are in the data.
- The open-case counts are mostly Maryland and Puerto Rico bookkeeping.
- Name drift splits UPS, Walmart and Amazon across several keys.

---

## New data traps (for the trap files)
1. NEISS `NARRATIVE` is empty on every 2015-2025 row.
2. NEISS weights reset in 2024 (+18% national with +7% cases). Floors (1807) jumped 66% in 2025.
3. NEISS product codes split in 2020 (scooters) and 2024 (e-bikes). A new code looks like a new product.
4. NHTSA complaints `DEATHS` summed over rows double counts, since ODINO repeats per component. Junk values under 99 exist (40), and repeat filers exist.
5. FAC material weakness rate goes from 6% to 14% at the Census → GSA FAC switch (2023).
6. FAC `ENTITY_TYPE = 'local'` includes 47 "State of ..." rows.
7. OSHA inspections contain "TESTING OIS 2" test rows. California's type A isn't the same thing as other states' type M.

## Housekeeping
- The scratchpad is shared across the 10 agents. My first batch ran through another agent's `run.py`. It failed at compile with no data read, but it left my query text in `deep-4.sql` and bumped that agent's `count.txt` by 1.
- I briefly moved another agent's `b1.sql`, then put it back in place. After that I used only `scratchpad/deep0/`.
