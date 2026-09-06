# The 31 hunches, refined against the live warehouse

Written 2026-09-05. Python door, `connect/db.py`. Chat plug-in still 401.
Every table in the matrix was matched by name in `LIBRARY_RAW.LANDING`, then the
load-bearing join in each chain was run. Numbers below are from those runs.
Nothing here is a finding yet. These are seeds with a first number attached.

Refine means hone in. Nothing was dropped. Seven hunches are dead **as written**
and each gets the nearest live version.

Probe scripts and raw outputs:
`C:\Users\wroge\AppData\Local\Temp\claude\c--Code-Ripple-v6\dab9ca80-0672-4424-9b8b-657f26512d39\scratchpad\hunch_probes*.py` and `.json`.

---

## The three tiers

| Tier | Meaning | Count |
|---|---|---|
| **1 — seeded** | chain holds, first number already found, run now | 10 hunches, 9 rows |
| **2 — runs, one vintage** | chain holds, but no time axis; cross-section only | 15 |
| **3 — dead as written** | a leg does not exist in the warehouse; reframed | 6, plus 26 which lives in tier 2 |

### Tier 1 — seeded

| # | Hunch | First number | What it means |
|---|---|---|---|
| 22 | Redlined toxicity | **1,446** TRI sites in D zones, **32** in A | per km²: D 0.43, A 0.02, **18×** |
| 23 | Debarred DME | **8** excluded supplier NPIs, **$1.425B** of $10.94B | 13.0% of all DME supplier dollars |
| 2 | PE abuse trap | 618 chains; **Bria** $5.2M fines over 15 homes | 5.4 fines per home vs Genesis 1.1 |
| 27 | Pending workforce | **9** LEIE NPIs among 14,103 pending applicants | exclusions 2013–2025, all pre-application |
| 30+13 | Shell carousel | **39** of 3,956 testable homes incorporated *after* first penalty | 139 re-incorporated since June 2023 |
| 31 | Post-acute funnel | **475** hospital owners also hold an HHA | 334 also hold a hospice |
| 1 | Hospice ghosts | **4** excluded NPIs still listed at 8 hospices | plus 133 owners hold SNF and hospice |
| 5 | FEMA debt trap | 47 disasters 2015–17, 6.09M registrations | HMDA all-actions covers the same 3 years |
| 15 | Disaster grifters | **26** SAM-excluded UEIs hold 51 FEMA contracts, $169M | untimed: award vs exclusion date not yet checked |

### Tier 2 — runs, one vintage

| # | Hunch | Holds | The catch |
|---|---|---|---|
| 6 | Rural dialysis | CCN→NPI affiliation 8,221 NPIs; chain, mortality, waitlist cols | HPSA is a status flag on QPP, not a geography |
| 11 | Cost-report hypocrisy | HCRIS FY2023: net income, uncompensated care; 927k NPIs at 4,605 hospitals | use Open Payments **2023**, not 2024 |
| 12 | LTCH churn | 340 LTCH cost reports; 5,803 NPIs at 309 LTCHs; ventilator bed count in POS | tiny universe, fine |
| 18 | Outpatient hardware | royalty payments **$847M** in 2024, 15,053 rows | outpatient file is one year; "only after" needs two |
| 10 | Equipment kickback | DME by referrer 381k rows | three known column traps, see traps file |
| 21 | Hospital wage | HCRIS salaries FY2023 vs QCEW 2022, NAICS 622, 2,616 counties | one-year offset |
| 28 | MDS padding | MDS file is **one quarter, Q2 2026**, 551 items, 14,695 CCNs | HCRIS has **no SNFs**; swap in NH411 staffing hours and fines |
| 9 | Toxic wage siphon | GHGRP county 92% filled 2010–23; QCEW 2022; injury TTM to Jan 2026 | ecological, cross-section |
| 8 | Incarceration collapse | VERA 1970–2026; poisoning 1999–**2015**; HPSA dates | window is 2010–2015 |
| 19 | Quality bonus | QPP FINAL_SCORE, PAYMENT_ADJUSTMENT_PERCENTAGE; Part D DY2024 opioid rate | county overdose ends 2015; CDC_OVERDOSE is state-month |
| 29 | Pollution hospital failure | POS hospital terminations by year; TRI county 100% filled | 2023 shows 365 terminations vs ~100 typical, check before trusting |
| 25 | FQHC evaporation | 10,907 FQHC sites in POS; 2,212 voluntarily terminated all-time | since 2020 only 20 sites at 17 still-enrolled orgs; date parse needs a look |
| 20 | Nursing-to-dialysis | 120 NPIs sit at both a nursing home and a dialysis facility | no dialysis enrollment file, so no owner link |
| 24 | Specialty model | 6,637 NPIs, cohort named | model starts **CY2027**; no bonus exists yet; baseline only |
| 26 | Storm arbitrage | storm events mart 1.78M rows 1996–2025 by county with damage $ | USDA MFH is one snapshot; no "before" |

### Tier 3 — dead as written, reframed

| # | Hunch | Why it dies | Nearest live version |
|---|---|---|---|
| 3 | Environmental redlining | lender LEI ∩ EPA crosswalk finds banks' **own** sites, not financed plants; tract shapes not landed | HMDA denial rate by county vs TRI density by county; merge with 22 |
| 17 | Polluter bank | FDIC LEI column **0% filled**; no financing edge in any table | Regions 59, Valley 26, RBC 15 EPA sites they own themselves |
| 4 | Bribed opiate pipeline | OTP NPIs are orgs; **0 of 1,340** appear in Part D | Part D DY2022 buprenorphine share × Open Payments 2022 from makers; OTP as county flag |
| 7 | Ghost clinics | UDS site NPI is the org; opt-out is people; FFS holds **zero** practitioners under FQHC IDs | opt-out density by ZIP vs HPSA |
| 14 | RHC harvesters | same missing org→doctor bridge | RHC ZIP RUCA vs enrollment address only |
| 16 | Diabetes mills | MDPP ∩ LEIE = **0** of 1,037 | park it |
| 26 | Storm arbitrage | NOAA_WEATHER_API is **287 alert rows**, not storm history | moved to tier 2 with the storm events mart |

Two entries mention 26. It dies on the NOAA table and lives on the mart. Counted once, in tier 2.

---

## The bridge that decides seven of them

Chris's matrix leans on **org → individual** links five times: FQHC → doctor, RHC →
doctor, OTP → prescriber, MDPP → clinician, hospital → HHA.

What was checked: the PECOS associate ID, `PECOS_ASCT_CNTL_ID` in the public
enrollment file, against the `ASSOCIATE_ID` in every facility enrollment file.

| Test | Result | Read |
|---|---|---|
| FQHC associate IDs found in FFS enrollment | 1,558 IDs, 11,565 NPIs | the org side joins |
| Of those NPIs, practitioner type `14-xx` | **0** | no doctor rides an org's ID |
| Hospital ID also in HHA enrollments | 475 | org → org works |
| Hospital ID also in hospice enrollments | 334 | org → org works |
| SNF ID also in hospice enrollments | 133 | Frank's shape, 133 times |

**Hit means:** two facility enrollments share an owner. **Miss means:** the
reassignment file that ties a doctor to a group is not landed. Org-to-org is live.
Org-to-person only exists through `FED_CMS_FACILITY_AFFILIATION`, which covers
hospitals, HHAs, hospices, nursing homes, dialysis, IRF, LTCH, and **nothing else**.

---

## Per-hunch cards

Each card: the refined hunch in one line, the chain that actually holds, what was
run, the number, and the trap.

### 1 Hospice ghost network
- **Refined:** excluded doctors still listed at hospices whose owner also runs a nursing home.
- **Chain:** LEIE NPI → AFFILIATION type Hospice → HOSPICE_ENROLLMENTS ASSOCIATE_ID → SNF_ENROLLMENTS.
- **Run:** LEIE ∩ hospice affiliation, NPI ≠ `0000000000`.
- **Number:** 4 NPIs, 8 hospices; all excluded 2024 or later; affiliation snapshot 2026-07-11.
- **Trap:** no hospice utilization file is landed. No live-discharge rate, no days, no dollars.

### 2 Private equity abuse trap
- **Refined:** which chains pay fines per bed at the highest rate and repeat the same tag.
- **Chain:** NURSINGHOME411 CHAIN_ID → DEFICIENCIES 2017–2026 → PENALTIES 2023–2026, all on CCN.
- **Run:** fines by chain.
- **Number:** 618 chains; 10,162 of 14,713 homes in one. Bria Health Services 15 homes, $5.24M, 5.4 fines each. Genesis 202 homes, $10.3M, 1.1 each.
- **Trap:** penalties file starts 2023-06-17. Deficiencies go back to 2017. Do not mix windows.

### 3 Environmental redlining
- **Refined:** merged into 22. The lender leg does not exist.
- **Run:** HMDA 2017 lender → LEI bridge. Raw concat matched 121 of 5,762. `AGENCY_CODE || ltrim(RESPONDENT_ID,'0')` matched 4,593.
- **Then:** lender LEI ∩ EPA corporate crosswalk. Hits are the banks' own EPA-registered sites. Regions 59, Valley National 26, RBC 15.
- **Trap:** the crosswalk's null-parent bucket fakes 681 lenders → 1,807 sites. Filter `ULTIMATE_PARENT_LEI is not null`.

### 4 Bribed opiate pipeline
- **Refined:** high buprenorphine-share prescribers in DY2022 who took 2022 money from the makers.
- **Run:** OTP NPIs ∩ Part D DY2022.
- **Number:** 0 of 1,340. OTP rows are organizations.
- **Trap:** OTP `NPI` column holds space-separated multiples, e.g. `1003081399 1013055110`. Part D has one drug-level year. No "spike after".

### 5 FEMA disaster debt trap
- **Refined:** rate spread and HOEPA flags by tract in the 12 months after a 2015–2017 declaration, against the same tract the year before.
- **Chain:** FEMA IA FIPS + DECLARATIONDATE → HMDA_HISTORIC county + tract + RATE_SPREAD + ACTION_TAKEN + race.
- **Number:** 47 disasters, 6,090,110 registrations, 636 counties in the window. HMDA 2015: 14.4M, 2016: 16.3M, 2017: 14.3M, all 8 action codes present.
- **Trap:** `FED_CFPB_HMDA` and `_LAR` at 28k and 17k rows are samples. Use HISTORIC only.

### 6 Rural dialysis monopoly
- **Refined:** chain-owned dialysis in HPSA-flagged QPP clinicians' hands, mortality and waitlist ratio vs peers, plus Open Payments.
- **Chain:** DIALYSIS CCN, CHAIN_OWNED, MORTALITY_RATE_FACILITY, waitlist ratio → AFFILIATION 8,221 NPIs → QPP HPSA status, FINAL_SCORE → OPEN_PAYMENTS.
- **Trap:** MEDICARE_DIALYSIS_FACILITIES at 12.4M rows is a long measure table, one row per facility per measure per year. Not a directory.

### 7 Ghost clinics in deserts
- **Refined:** dead as written. Site NPI is the org's, 6,048 distinct on 19,038 sites. Opt-out is people. No bridge landed.
- **Nearest:** opt-out affidavit count by ZIP, 56,455 NPIs 1998–2025, against HPSA ZIPs.

### 8 Incarceration and collapse
- **Refined:** counties whose jail population jumped 2010–2015, primary-care HPSA designation dates after, poisoning deaths after.
- **Number:** VERA 3,075 counties; 2020+ years thin out to 597 counties by 2026. Poisoning ends 2015.
- **Trap:** VERA's later years are partial, not zero. A drop after 2019 is coverage, not decarceration.

### 9 Toxic wage siphon
- **Refined:** GHGRP tonnage per county 2022 against QCEW 2022 county wage and 2025 violent-injury rate.
- **Number:** GHGRP county FIPS 125,377 of 136,005 filled. QCEW 2022 only, 4,429 areas. Injury TTM Feb 2025–Jan 2026, INTENT column carries suicide and homicide.
- **Trap:** no overdose in the injury file. Cross-section, one year each.

### 10 Equipment kickback loop
- **Refined:** as written, with the three DME-referrer traps applied.
- **Trap:** null suppression flag is not a whole row; families do not sum; BENE_DUAL_CNT and CC percents censored at 11. Use BENE_AVG_RISK_SCRE.

### 11 Cost-report hypocrisy
- **Refined:** hospitals with negative net income FY2023 whose affiliated doctors took the most 2023 pharma money.
- **Chain:** HCRIS 6,103 rows, NET_INCOME, COST_OF_UNCOMPENSATED_CARE → AFFILIATION 927,092 NPIs at 4,605 hospitals → OPEN_PAYMENTS_2023.
- **Trap:** HCRIS is hospitals only: STH 3,236, CAH 1,382, PH 646, RH 389, LTCH 340, CH 91. No SNF, no HHA.

### 12 LTCH ventilator churn
- **Refined:** LTCH cost margin vs ventilator bed count vs device royalties to affiliated doctors.
- **Number:** 340 LTCH cost reports; 311 in the directory; 5,803 affiliated NPIs; POS carries `VNTLTR_BED_CNT`.

### 13 Fire trap shell game
- **Refined:** merged into 30. Same mechanism, second trigger.
- **Number:** fire deficiencies 2016-07 to 2026-05, 13,914 CCNs. 83 homes carry a G-or-worse fire tag since June 2024.

### 14 RHC subsidy harvesters
- **Refined:** dead as written. 5,530 RHC orgs; the doctor bridge is not landed.
- **Nearest:** RHC enrollment ZIP vs RUCA rural code, orgs enrolled as rural at urban ZIPs.

### 15 Disaster grifter scams
- **Refined:** SAM-excluded contractors holding FEMA contracts, award date vs exclusion date.
- **Run:** SAM UNIQUE_ENTITY_ID ∩ USASpending contracts R2, sub-agency like emergency management.
- **Number:** 26 UEIs, 51 distinct contracts, $168,975,003 award-level. Net obligated in the file $22,066,026.
- **Skeptic fix:** first pass summed TOTAL_DOLLARS_OBLIGATED across action rows, a lifetime total repeated per action, and read $314M over 154 rows. Use max per CONTRACT_AWARD_UNIQUE_KEY and distinct UEIs on the SAM side. The all-agency figure from the same pass is withdrawn.
- **Dead legs:** FEMA IA registrations carry no applicant identity. SAM ∩ FEMA assistance CFDA 97 = 0.
- **Not done:** exclusion ACTIVE_DATE vs action date. Most will predate. Untimed numbers are not findings.

### 16 Diabetes billing mills
- **Number:** 0 of 1,037 MDPP NPIs on LEIE. Park.

### 17 Polluter bank financing
- **Refined:** dead as written. FDIC `LEI` is 0 of 27,836 filled. No financing edge exists in any landed table.
- **Nearest:** banks' own EPA-registered sites through the LEI bridge, above.

### 18 Outpatient hardware funnel
- **Refined:** surgeons with 2022–2024 royalty income, joint and spine HCPCS volume at their affiliated hospital in the outpatient year.
- **Number:** Royalty or License 2024: 15,053 rows, $846.8M. Outpatient by service 116,182 rows.
- **Trap:** one outpatient year; check the registry for which.

### 19 Quality bonus laundering
- **Refined:** QPP positive payment adjustment × Part D DY2024 opioid prescriber rate top decile.
- **Trap:** QPP registry row has no URL or notes; vintage unrecorded. County overdose ends 2015.

### 20 Nursing-to-dialysis churn
- **Number:** 120 NPIs affiliated with both types. No dialysis enrollment file, so no shared-owner test.
- **Better:** 133 SNF owners also hold a hospice. That is the Frank pattern at scale.

### 21 Hospital wage starvation
- **Refined:** HCRIS TOTAL_SALARIES per discharge vs QCEW NAICS 622 county average weekly wage.
- **Number:** 2,616 counties with private hospital wage rows, 2022. HCRIS FY2023.

### 22 Redlined toxicity loop
- **Refined:** TRI facility density per km² by HOLC grade, then injury rate for the containing county.
- **Run:** ST_CONTAINS on 10,154 HOLC polygons, TRI points with decimal coords.
- **Number:** A 32 sites / 1,366 km². B 315 / 2,942. C 1,350 / 5,462. D 1,446 / 3,355.
- **Traps:** `FAC_LATITUDE` is DDMMSS text, `182848` = 18.48°, on 48,566 rows. `PREF_LONGITUDE` is stored positive. Only 36,721 of 64,990 have decimal coords; convert the rest. HOLC_GRADE has 814 blanks and trailing spaces; one bad polygon throws `Invalid Lng/Lat pair '251,30'`, use `try_to_geography`.

### 23 Debarred DME laundering
- **Refined:** the 8 are the catheter ring, all excluded June 2026 under 1128A(a), all organizations. Hidden-owner version needs the PECOS ownership file, not landed.
- **Number:** Sunshine Senior Solutions $860.3M, 45,054,960 catheter units for 42,083 beneficiaries. Eight total $1.425B of the file's $10.943B, 13.0%.
- **Skeptic check:** grain is one row per supplier × HCPCS × rental flag, no rollups. Paid over allowed is 76.7%, Medicare's 80% after coinsurance, so services × average payment is the right dollar. First pass read 2.7% low because bare try_to_number rounds to integer.
- **Trap:** file has no year column, ingested 2026-07-26. Dollars = `TOT_SUPLR_SRVCS × AVG_SUPLR_MDCR_PYMT_AMT` per HCPCS row. Say the vintage before publishing anything.

### 24 Specialty model extraction
- **Refined:** baseline now, compare in 2028. ASM_CY27_PARTICIPANT is the first live flag. Cohorts: Heart Failure and Low Back Pain.

### 25 FQHC evaporation
- **Refined:** FQHC orgs still enrolled whose POS sites are terminated, in HPSA counties.
- **Number:** 10,907 FQHC CCNs in POS category 21. Voluntary termination code 01 on 2,212 all-time. Since 2020: 20 sites, 17 orgs, 19 counties.
- **Trap:** nursing homes are **not** in POS_OTHER at all. FQHCs are.

### 26 Storm housing arbitrage
- **Refined:** USDA MFH vacancy today in counties with a $10M+ storm event, vs counties without.
- **Number:** storm events mart 1,780,730 rows 1996–2025 with CZ_FIPS and DAMAGE_PROPERTY. USDA MFH 13,550 projects with VACANT_UNITS.
- **Trap:** NOAA_WEATHER_API is 287 alert rows. USDA MFH is one snapshot; "failed to restore" needs a second.

### 27 Pending provider workforce
- **Refined:** excluded people applying for Medicare enrollment, and where they are already affiliated.
- **Number:** 9 distinct NPIs of 14,103 distinct pending; 10 LEIE rows. Exclusion dates 2013-04 to 2025-11. Pending snapshot 2026-07-26. 152 pending NPIs already sit at 233 facilities.
- **Trap:** the pending union has 17 duplicate NPIs; dedupe before joining or Louisville's 2 rows read as 4.

### 28 MDS assessment padding
- **Refined:** cross-section only. High acuity share, Q2 2026, vs deficiency tags 2025–26 vs NH411 staffing hours and fines.
- **Trap:** MDS file is a single quarter. HCRIS has no SNFs. Swap that leg.

### 29 Pollution hospital failure
- **Refined:** TRI sites per county vs HCRIS net income FY2023 vs POS hospital terminations.
- **Number:** terminations 2015–2022 run 68–122 a year; 2023 is 365; 2024 99.
- **Trap:** the 2023 spike is probably a coding sweep, not closures. Check `PGM_TRMNTN_CD` values that year.

### 30 PECOS shell carousel
- **Refined:** nursing homes whose current owner incorporated after the home's first penalty or fire tag.
- **Run:** SNF_ENROLLMENTS INCORPORATION_DATE vs earliest PENALTY_DATE.
- **Number:** 6,660 penalized homes, 3,956 with a parseable INCORPORATION_DATE; 39 incorporated after their first penalty; 139 incorporated since June 2023.
- **Floor:** PENALTY_DATE starts 2023-06-17, so "first penalty" means first since then. 39 is a floor.
- **Traps:** `FED_CMS_PECOS_PROVIDER_ENROLLMENT` and `..._FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT` are the same file, equal hash, so the matrix path joins a table to itself. `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` is `N` on all 14,700 rows.

### 31 Post-acute referral funnel
- **Refined:** hospital-owned HHAs vs independents on discharge-to-community, spend per episode, star rating. Ownership through shared ASSOCIATE_ID, no affiliation needed.
- **Number:** 519 hospital-owned HHAs. Star 3.16 vs 3.25. DTC 84.6 vs 79.9, higher is better. Spend per episode 0.976 vs 0.968, owned spend more.
- **Read:** mixed. Owned agencies rate lower and spend more, but discharge home more. Star is rated on 95% of owned and 63% of independents, so the unrated independents are missing. Steering itself needs claims, which are not landed.
- **Skeptic fix:** first pass used bare try_to_number, which rounds 3.5 to 4 and 0.98 to 1; it reported 3.38 vs 3.50 and a spend ratio that pointed the wrong way.

---

## Traps found today, appended to `.claude/traps.md`

Fifteen. The two that matter most: no org-to-person enrollment bridge is landed, and
the nursing-home ownership-change flag is a constant.

## Two caveats that sit under every LEIE number here

- LEIE carries a real NPI on 8,661 of 83,842 rows; 75,001 hold `0000000000`. Every LEIE-join count in this file is a floor over a tenth of the exclusion list. Hunch 16's zero is not evidence of absence.
- Bare `try_to_number(x)` is NUMBER(38,0) and rounds. Every average and ratio here now uses `try_to_number(x,18,6)` or was rerun by the skeptic with it.

## Skeptic verdict

Ten claims attacked. Six confirmed exactly: the redlining gradient, the associate-ID counts, the PECOS twin file, the CHOW constant, the missing bridge, the shell-carousel 39. Four corrected above: DME dollars, pending row count, FEMA contract dollars, the HHA comparison. The redlining gradient held with a third more coordinates added: D over A went 18.4× to 17.8×.
