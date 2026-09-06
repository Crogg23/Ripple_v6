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

---

## Appendix, 2026-09-05: categories the 31 never touched

None of the 31 use campaign finance, lobbying, or political money. Not because
those tables are missing — they're landed and trapped in `.claude/traps.md`
already. Nobody pointed the matrix at them. Not probed yet, zero warehouse
cost so far.

### 32 Excluded-entity donor overlap
- **Chain:** LEIE or SAM-excluded org names → FEC `itcont` contributor names, or FEC committee treasurer/officer names.
- **Would show:** a banned provider's owners or execs also funding campaigns.
- **Known trap:** name-only match is noise unless a multi-word name or a shared address confirms it. Verify individually, per the 2026-09-03 surname-leak trap.

### 33 Nursing-home chain PAC money
- **Chain:** the 618 PE-owned nursing chains from hunch 2 → FEC committee names matched to the parent company.
- **Would show:** whether the worst fine-rate chains also run a PAC.
- **Known trap:** `FED_FEC_COMMITTEES` repeats IDs across cycles with no cycle column; join the DIM table, not the raw table.

### 34 Earmarked district vs redlined zone
- **Chain:** `FED_HOUSE_DISBURSEMENTS` by district → TRI density by HOLC grade from hunch 22, rolled up to district.
- **Would show:** whether the worst-polluted districts get more or less member spending.
- **Known trap:** 7.6% of disbursement rows are subtotal rows holding 75% of the naive dollar sum. Filter `DESCRIPTION LIKE '%TOTALS%'` first.

### 35 Committee assignment vs stock trades
- **Chain:** `FED_HOUSE_FD_PTR_INDEX` trade filings → committee membership, if committee rosters are landed.
- **Would show:** a member trading in an industry their committee regulates.
- **Known trap:** DOCID is not unique, 41,883 rows over 41,860 distinct; dedupe on a full-row hash first. Committee-roster table not yet confirmed landed.

### 36 DME/nursing-home money to the committees that oversee CMS
- **Chain:** the debarred-DME supplier or PE-chain names from 23 and 2 → FEC contributor names → committee jurisdiction over CMS.
- **Would show:** whether the same industry flagged for fraud also funds its own oversight committee.
- **Known trap:** same name-leak risk as 32; needs individual verification, not a bulk join.

### 37 Sanctioned individuals in political money
- **Chain:** OFAC/UN/UK sanctions names, already confirmed as a real small list — cross against FEC contributor names.
- **Would show:** a sanctioned person's name still moving through the US political system.
- **Known trap:** none yet specific to this pair; apply the same multi-word-name confirmation rule.

### What's confirmed landed for this appendix
FEC committees, FEC committee-to-committee, House disbursements, House
financial disclosure index. Lobbying disclosure and a House committee-roster
table are referenced in code but not confirmed landed — check before building
34 or 35 further.

### Next step
Each of these needs one probe query to get a first number, same as the
original 31. That's warehouse cost. Say go and a price estimate comes first.

---

## Appendix 2, 2026-09-05: the rest of the warehouse

Same shape as 32–37: chain, what it would show, known trap. Not probed, zero
warehouse cost. Everything below was scoped from local files only: the live-rows
build of 2026-09-05 (`reports/viz/_build/chain/live_rows.json`, 2,949 tables),
the dbt staging models for column names, `.claude/traps.md`, and the registry
dump. Column names are from the staging SQL and were **not** re-checked live.

**Read the table name as the mart unless it says LANDING.** Several bare
LANDING names are stubs: `FED_FDA_DEVICE_510K` is 88 rows, `FED_FDA_MAUDE`
1,386, `FED_FDA_GUDID` 2,542. The HEALTH marts hold the real files. The other
way round too: `FED_DOL_FORM5500_FULL` is 4.3M rows where the mart is 33k,
`FED_CMS_NADAC` landing is 1.5M where the mart is 359k, `FED_FARA_BULK`
landing is 222k where the mart is 48k. Check both before calling a gap.

**Numbering.** Hunches 32–75 already exist in
`reports/hunch_expansion_32_75_2026-09-05.md`, so the 32–37 appendix above
collides with them. Everything here starts at **76**. The six above are not
renumbered; that is Chris's call.

### What 1–75 never touched

Row counts are the mart or landing table as of the 2026-09-05 build.

| Category | Biggest landed tables | Rows | Touched by 1–75? |
|---|---|---|---|
| SEC markets | 13F holdings, insider Form 4 trans, DERA subs, PCAOB AP | 101M, 2.7M, 53k, 155k | no |
| Congress money | FEC indiv, independent expenditures, leadership PACs, House disbursements | 84M, 261k, 8.6k, 4.9M | 32–37 sketched only |
| Lobbying | Senate LDA filings, CA lobby, TX lobby, FARA bulk landing | 831k, 525k, 284k, 222k | no |
| Political ads | Google political ads creative, geo, weekly spend | 1.6M, 614k, 299k | no |
| Votes and bills | Voteview votes, bill cosponsors, committee membership, MEDSL returns | 946k, 368k, 3.9k, 30k | no |
| Judges | CourtListener investments, disclosures, gifts, debts, positions | 1.9M, 66k, 2k, 19k, 51k | no |
| Courts | FJC IDB civil, bankruptcy, criminal, appellate; JPML MDLs | 10.9M, 7.0M, 6.3M, 988k, 162 | no |
| Opioid supply | DEA ARCOS transactions 2006–2014 | 178.6M | **no, the biggest table in the house** |
| FDA | MAUDE, device recalls, 510k, PMA, drug recalls, GUDID | 2.7M, 40k, 176k, 57k, 18k, 5.1M | no |
| Disaster and infrastructure | NFIP community status, NID dams, PHMSA, NRC spills, orphan wells, FracFocus | 25k, 93k, 2k, 1.0M, 118k, 7.2M | 5, 15, 26, 50 used IA and storms only |
| Labor | OSHA inspections, OSHA 300A, MSHA violations, OLMS unions, OFLC visas, Form 5500 FULL, PBGC | 5.2M, 1.2M, 3.1M, 618k, 665k, 4.3M, 5k | no |
| Immigration | ICE detention stints, detainers, EOIR | 2.6M, 610k, 12.6M | no |
| Corporate and offshore | UK PSC, ICIJ, GLEIF, FATCA FFI, IRS 527 directors | 15.8M, 3.3M, 3.4M, 516k, 190k | no |
| Consumer finance | CFPB complaints, FDIC SOD branches, FDIC enforcement, FHLB, SBA, PPP | 17.2M, 2.8M, **14**, 6k, 2.2M, 969k | hunch 17 touched FDIC bank data only |
| Vehicles and transport | NHTSA recalls and complaints, NTSB, FAA registry, FRA, AIS | 242k, 2.2M, 31k, 315k, 1.2M, 58M | no |
| Security | OpenSanctions, OFAC, CSL, ransomware victims, CISA KEV, NICS, ATF FFL | 1.3M, 19k, 26k, 31k, 1.7k, 16k, 78k | 37 sketched only |
| Energy | EIA 860 owners and plants, 861 utilities, eGRID, CAMPD daily | 5.5k, 16k, 1.7k, 12k, 16.5M | no |
| Housing beyond HMDA | Section 8 contracts, FHA portfolio, FHFA HPI, suspended counterparties | 24k, 62k, 185k, 241 | 26, 55, 72 used HUD and USDA snapshots |
| Research | NIH Reporter, SBIR, Retraction Watch | 2.1M, 220k, 72k | no |

Nineteen categories. SEC, lobbying and ARCOS alone are 280M rows with no hunch on them.

Two mislabels to know before grouping by schema: Senate LDA filings and the
Google political ads tables sit in `LIBRARY_MARTS.EDUCATION`. The registry
domain column lies on at least 12 rows, per the 2026-09-01 trap.

---

### A. SEC and markets

### 76 Insiders sell before the fines land
- **Chain:** FEC-free. Public nursing-home and hospital operators (Ensign, Brookdale, NHC, HCA, Tenet, CHS, UHS) → `FED_SEC_EDGAR_COMPANY_TICKERS` CIK → `FED_SEC_INSIDER_NONDERIV_TRANS` (TRANS_DATE, TRANS_CODE, TRANS_ACQUIRED_DISP_CD, TRANS_PRICEPERSHARE) via `FED_SEC_INSIDER_SUBMISSION` ISSUERCIK → NH411 CHAIN_ID fines and G-tags from hunches 2 and 44.
- **Would show:** insider dispositions clustering in the 90 days before a chain's fine or G-tag spike.
- **Known trap:** registry says insider tables are one quarter, 2025Q1, yet the mart holds 2.67M rows. Count distinct PERIOD_OF_REPORT before calling it a series. Chain name → CIK is a name match; multi-word rule.

### 77 Judges invested in the parties before them
- **Chain:** `FED_COURTLISTENER_INVESTMENTS` (1.9M rows, PERSON_ID) → `FED_COURTLISTENER_POSITIONS` court → `FED_FJC_IDB_CIVIL` FILING_JUDGE + DISTRICT → DEFENDANT / PLAINTIFF names → `FED_SEC_EDGAR_COMPANY_TICKERS`.
- **Would show:** a judge holding stock in a defendant while the case ran, by year of disclosure.
- **Known trap:** IDB FILING_JUDGE is a district-local code, not a person; the CL judges table carries FJC_ID, so route CL → FJC → IDB code through `FED_FJC_SERVICE`. IDB party names are truncated and first-listed only. Investment descriptions are OCR text, not tickers.

### 78 Senators trade the industry their committee marks up
- **Chain:** `POLITICS__SENATE_TRADES` (TICKER, TRANSACTION_DATE, AMOUNT band, MATCH_METHOD) → `FED_CONGRESS_COMMITTEE_MEMBERSHIP` BIOGUIDE → `FED_SEC_DERA_SUB_*` SIC by CIK → `FED_VOTEVIEW_ROLLCALLS` CAST_CODE by ICPSR in the same window.
- **Would show:** trades inside 30 days of a committee vote on that SIC's regulator, per senator.
- **Known trap:** SENATE_TRADES has no staging model; its columns are not confirmed locally. AMOUNT is a range string. Unmatched senators are NULL by design. Committee membership is a current snapshot with no term dates, so a 2019 trade against a 2026 roster is wrong.

### 79 The auditor changed the year before the bank died
- **Chain:** `FED_FDIC_FAILED_BANKS` (BANK_NAME, FAIL_DATE, ESTIMATED_LOSS_THOUSANDS) → `FED_FDIC_SOD_BRANCH_DEPOSITS` HOLDING_COMPANY_RSSD → holding company name → `FED_PCAOB_FORM_AP_FILINGS` (FIRM_NAME, ISSUER_NAME, AUDIT_REPORT_DATE).
- **Would show:** audit-firm swaps in the two years before failure, and the small firms that audited the most failures.
- **Known trap:** the filer is the holding company, not the bank. Failed-banks has no CIK. Form AP begins 2017; pre-2017 failures have no leg.

### 80 Going-concern auditees still winning contracts
- **Chain:** `FED_FAC_SINGLE_AUDIT` IS_GOING_CONCERN_INCLUDED = Y, AUDITEE_UEI, FY_END_DATE → `FED_USASPENDING_CONTRACTS_FULL_R2` RECIPIENT_UEI, ACTION_DATE after FY_END_DATE.
- **Would show:** contract dollars awarded after an auditor doubted the recipient could survive. Hunch 64 ran material weakness on the capped assistance table; contracts R2 is the full 93M.
- **Known trap:** UEI absent before April 2022, DUNS→UEI backfill under it. Case-sensitive lowercase column names on USAspending landing tables.

### 81 Pension dumped on PBGC while insiders sold
- **Chain:** `FED_PBGC_TRUSTEED_PLANS` (EIN, DATE_OF_PLAN_TERMINATION, participants) → `FED_DOL_FORM5500` SPONSOR_DFE_EIN, NET_ASSETS_EOY_AMT → `FED_SEC_DERA_SUB_*` EIN → CIK → `FED_SEC_INSIDER_NONDERIV_TRANS`.
- **Would show:** sponsors whose insiders disposed of stock in the year before the plan went to PBGC.
- **Known trap:** 574 of 5,176 PBGC EINs are short, leading zeros lost. Use `FED_DOL_FORM5500_FULL`, 4.3M rows in LANDING; the mart is a 33k slice. `FED_PBGC_TRUSTEED_PENSION_PLANS` at 21,596 and `FED_PBGC_DATA` at 140k are the bigger PBGC legs; pick by column, not by name.

### 82 Unions with a shortage and a PAC
- **Chain:** `FED_DOL_OLMS` (UNION_NAME, SHORTAGE_AMOUNT, PAC_FUNDS, TOTAL_RECEIPTS, FISCAL_YEAR_END) → `FINANCE__FED_FEC_COMMITTEES_DIM` CONNECTED_ORG_NM → `FED_FEC_COMMITTEE_TO_CANDIDATE`.
- **Would show:** locals reporting a shortage, the LM word for missing money, in the same year their PAC gave.
- **Known trap:** SHORTAGE_AMOUNT fill rate unknown. Union name and connected-org name differ in form; multi-word rule, and the affiliation abbreviation helps.

---

### B. Political money, beyond 32–37

### 83 Lobby surge around the rule that sets the fine
- **Chain:** `EDUCATION__FED_SENATE_LDA_FILINGS` client and registrant names for nursing-home, DME, hospice and dialysis trade groups → `FED_FEDERAL_REGISTER_DOCUMENTS` (AGENCIES like CMS, DOCKET_IDS, PUBLICATION_DATE, COMMENTS_CLOSE_ON) → the chain fines from hunch 2.
- **Would show:** quarterly lobby spend rising into the comment window of the rule that governs the fine.
- **Known trap:** LDA sits in the EDUCATION mart. No staging model, so column names are unconfirmed. Registry says 1.94M filings exist; 831k landed, coverage window unknown.

### 84 Independent expenditures aimed at the CMS overseers
- **Chain:** `FED_FEC_INDEPENDENT_EXPENDITURES` (CAND_ID, SPE_ID, SUP_OPP, EXP_AMO, EXP_DATE) → `FED_FEC_CAND_CMTE_LINKAGE` → `FED_CONGRESS_LEGISLATORS` FEC_IDS → `FED_CONGRESS_COMMITTEE_MEMBERSHIP` for Energy and Commerce, Ways and Means, Senate Finance.
- **Would show:** who spends for and against the members who write Medicare law, by industry of the spender.
- **Known trap:** the SUP_OPP CSV is the source of truth for for/against; pas2 and oth 24A/24E are cross-check only. Roster is current-only.

### 85 Device and pharma PACs into leadership PACs
- **Chain:** Open Payments payer names, APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME → `FINANCE__FED_FEC_COMMITTEES_DIM` CONNECTED_ORG_NM → `FED_FEC_COMMITTEE_TO_CANDIDATE` → `FED_FEC_LEADERSHIP_PAC` linkage.
- **Would show:** which makers' corporate PACs fund which members' leadership PACs, ranked by the maker's doctor-payment total.
- **Known trap:** raw `FED_FEC_COMMITTEES` repeats IDs across cycles, inflates 2.14×; use the DIM. The payer ID column named PAYMENT is an ID, never sum it.

### 86 Ad money the FEC never saw
- **Chain:** `FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND` (ADVERTISER_NAME, ELECTION_CYCLE, SPEND_USD) and `_GEO_SPEND` (COUNTRY_SUBDIVISION_PRIMARY) → `FED_FEC_PAC_SUMMARY` INDEPENDENT_EXPENDITURES by committee → `FED_MEDSL_*_RETURNS` margins.
- **Would show:** advertisers with six-figure Google spend and no FEC committee, by state.
- **Known trap:** POLADS sits in the EDUCATION mart. Use SPEND_USD only; the other 20 currency columns are zero-filled for US rows. Advertiser name is not a committee name.

### 87 Foreign agents giving at home
- **Chain:** `FED_FARA_BULK` (REGISTRANT_NAME, FOREIGN_PRINCIPAL_COUNTRY, REGISTRATION_DATE, TERMINATION_DATE) → `FED_FEC_INDIV_CONTRIBUTIONS` EMPLOYER or DONOR_NAME inside the registration window.
- **Would show:** registered agents of a foreign principal donating to the members who sit on Foreign Affairs.
- **Known trap:** use `FED_FARA_BULK` in LANDING, 222k rows; the mart is 48k and `FED_FARA` is a 30-row stub. EMPLOYER is dirty free text, never a key.

### 88 The same people run the 527 and the PAC
- **Chain:** `POLITICS__IRS527_DIRECTORS_OFFICERS` (name, title, address) → `FINANCE__FED_FEC_COMMITTEES_DIM` TRES_NM + CMTE_ZIP.
- **Would show:** one treasurer bridging a state-level dark-money 527 and a federal committee.
- **Known trap:** name plus ZIP or it's noise. 527 Schedule A/B, the 17.9M itemized rows, is not landed, so no 527 dollars yet.

### 89 State dinners, federal checks
- **Chain:** `TX_LOBBY_FOOD_BEVERAGE`, `_ENTERTAINMENT`, `_GIFTS` (FILERNAME, RECIPIENTNAME*, ACTIVITYAMOUNTCD ranges, ACTIVITYDATE) and `CA_LOBBY_COVER` FIRM_NAME → `FED_FEC_INDIV_CONTRIBUTIONS` by the same lobbyist name and city.
- **Would show:** lobbyists who feed state legislators while giving federally to the same party's delegation.
- **Known trap:** Texas amounts are range codes, not dollars. CA contributions table is 6.5k rows, a slice.

### 90 Appointee's old sector, agency's new awards
- **Chain:** `FED_REVOLVINGDOOR_PROJECT` (PERSON_NAME, AGENCY, INDUSTRY_SECTOR, SECTOR1..16) → `FED_USASPENDING_CONTRACTS_FULL_R2` AWARDING_AGENCY_NAME + NAICS_CODE by year.
- **Would show:** an agency's award mix tilting toward the appointee's prior sector after arrival.
- **Known trap:** 406 rows, no position dates, so "after arrival" needs a date from elsewhere. Sector columns are wide; unpivot first.

### 91 Trades, then a bill
- **Chain:** `POLITICS__SENATE_TRADES` TICKER + date → `FED_GOVINFO_BILLSTATUS` SPONSOR_BIOGUIDE and `_BILL_COSPONSORS` → bill subject → `FED_SEC_EDGAR_COMPANY_TICKERS` SIC.
- **Would show:** a member buys, then sponsors or cosponsors a bill in that SIC inside 90 days.
- **Known trap:** House side is an index of filings, DOCID not unique, hash-dedupe; the trade lines live in PDFs. Senate side has tickers, but SENATE_TRADES columns are not confirmed locally. Bill subject column not confirmed locally.

### 92 Office money to donors
- **Chain:** `FED_HOUSE_DISBURSEMENTS` payee, AMOUNT, office, SOD_QUARTER → `FED_FEC_INDIV_CONTRIBUTIONS` DONOR_NAME + city → the office's member via BIOGUIDE.
- **Would show:** members' allowance flowing to vendors who also donate to them.
- **Known trap:** 7.6% subtotal rows hold 75% of the naive sum; filter DESCRIPTION LIKE '%TOTALS%'. AMOUNT is text with six column-shifted rows. SOD_QUARTER has 42 spellings.

### 93 Rejected ballots and jail counties
- **Chain:** `FED_EAC_EAVS` (FIPSCODE, the coded A–F columns) → `DIM_COUNTY` → `XC_VERA_INCARCERATION_TRENDS` → `FED_MEDSL_HOUSE_RETURNS` margin.
- **Would show:** counties with the highest rejected-mail-ballot share, against jail rate and race.
- **Known trap:** 430 coded columns, no codebook landed. Blank, 'not applicable' and zero are three different things in EAVS.

### 94 Judges' politics and their dockets
- **Chain:** `FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS` → `FED_FEC_INDIV_CONTRIBUTIONS` pre-appointment gifts by name and city → `FED_FJC_IDB_CIVIL` DISPOSITION and NATURE_OF_SUIT by judge.
- **Would show:** disposition mix by the judge's party and donation history, per nature of suit.
- **Known trap:** IDB judge is a code; route through `FED_FJC_SERVICE`. FEC OCCUPATION is free text.

### 95 Gifts, debts and the parties before the bench
- **Chain:** `FED_COURTLISTENER_DISCLOSURE_GIFTS` (2k), `_REIMBURSEMENTS` (33k), `_DEBTS` (19k), `_SPOUSAL_INCOME` (20k) by PERSON_ID → positions court → `FED_COURTLISTENER_DOCKETS` party names in that court and year.
- **Would show:** a reimbursement source or creditor appearing as a party in the judge's own court.
- **Known trap:** disclosure rows are OCR text with a redacted flag. Dockets is 71.7M rows, landing only.

---

### C. Disaster and infrastructure

### 96 Flood money where flood insurance was refused
- **Chain:** `FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK` (COMMUNITY_NAME, COUNTY, STATE, PARTICIPATING_IN_NFIP_FLAG, REGULAR_EMERGENCY_PROGRAM_DATE) → `FED_FEMA_IA_HOUSING_REGISTRATIONS` (COUNTY, DAMAGED_CITY, DISASTER_NUMBER, FLOOD_DAMAGE_AMOUNT).
- **Would show:** IA flood dollars paid in communities that opted out of NFIP, repeated across disasters.
- **Known trap:** community ID is not a county FIPS; match on state + county + name. IA county is text.

### 97 Rebuilt three times
- **Chain:** IA registrations DAMAGED_ZIP_CODE × DISASTER_NUMBER where DESTROYED = Y, verified loss RPFVL → count of disasters per ZIP → `FED_HUD_ASSISTED_HOUSING_PROJECTS` and `FED_USDA_RD_MFH_ACTIVE_PROJECTS` in the same ZIP.
- **Would show:** ZIPs with destroyed homes in three or more declarations since 2015 and the subsidized units still sitting there.
- **Known trap:** rows are registrations, not households. REPORTED_DAMAGE is self-report, RPFVL is inspected; say which. Hunch 72 found Puerto Rico dominating repeat-disaster lists, run a states-only view.

### 98 Poor dams above nursing homes
- **Chain:** `FED_NID_DAMS` (HAZARD_POTENTIAL = High, CONDITION_ASSESSMENT = Poor or Unsatisfactory, HAS_EMERGENCY_ACTION_PLAN = No, LAST_INSPECTION_DATE, LATITUDE, LONGITUDE) → ST_DISTANCE to nursing homes, hospitals, HUD projects.
- **Would show:** facilities within 5 km of a high-hazard poor-condition dam with no emergency plan and no inspection in five years.
- **Known trap:** two NID copies at 92,766 rows each; pick one. Condition is 'Not Available' on most private dams. Distance is not downstream; use it as proximity only.

### 99 Tailings ponds and open violations
- **Chain:** `FED_MSHA_MINES` (MINE_ID, NO_TAILING_PONDS, CURRENT_CONTROLLER_NAME) → `FED_NID_DAMS` PRIMARY_PURPOSE = Tailings, OWNER_NAMES → `FED_MSHA_VIOLATIONS` AMOUNT_DUE by CONTROLLER_ID.
- **Would show:** controllers holding poor-condition tailings dams and the biggest unpaid MSHA penalty pile.
- **Known trap:** MSHA values carry literal double quotes, strip before cast. NID OWNER_NAMES is a semicolon list.

### 100 Pop-up disaster contractors
- **Chain:** `FED_USASPENDING_CONTRACTS_FULL_R2` AWARDING_SUB_AGENCY_NAME like FEMA, ACTION_DATE → first-ever ACTION_DATE per RECIPIENT_UEI in the full table → IA DECLARATION_DATE for the place of performance.
- **Would show:** vendors whose first federal award of any kind came within 60 days of the declaration they were paid under.
- **Known trap:** first-in-file is not first-ever. UEI backfill before 2022. Hunches 15 and 49 timed exclusions; this times incorporation-by-proxy.

### 101 Old flood maps, new flood damage
- **Chain:** `FED_NOAA_STORM_EVENTS` (CZ_FIPS, EVENT_TYPE flood, DAMAGE_PROPERTY, year) → `FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK` CURRENTLY_EFFECTIVE_MAP_DATE by county.
- **Would show:** counties with the most flood damage since 2015 still on a rate map older than 20 years.
- **Known trap:** DAMAGE_PROPERTY is text with K/M/B suffixes, parse before summing. CZ_FIPS is a county or a forecast zone depending on CZ_TYPE.

### 102 Three fossil burdens, one water system
- **Chain:** `FED_PHMSA_FLAGGED_INCIDENTS` (lat/lon, OPERATOR_NAME, TOTAL_FATALITIES) + `FED_USGS_ORPHANED_OIL_GAS_WELLS` (COUNTY) + `FED_FRACFOCUS_REGISTRY` (COUNTY_NAME, TOTAL_BASE_WATER_VOLUME, distinct DISCLOSURE_ID) → county → `FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT` by PWSID → `SDWA_GEOGRAPHIC_AREAS`.
- **Would show:** counties stacking pipeline incidents, orphan wells and fracking water draw against the worst drinking-water compliance. Hunches 32 and 60 used water alone.
- **Known trap:** FracFocus rows are ingredients; dedupe on DISCLOSURE_ID before counting wells. Orphan wells carry no orphaning date.

### 103 Spillers on the payroll
- **Chain:** `FED_USCG_NRC_INCIDENTS` (RESPONSIBLE_COMPANY, RESPONSIBLE_STATE, CALL_TYPE, DATE_TIME_RECEIVED) → `FED_USASPENDING_CONTRACTS_FULL_R2` RECIPIENT_NAME → `FED_SAM_EXCLUSIONS`.
- **Would show:** the top hundred spill reporters and their federal contract dollars in the same years. Extends the `FINDINGS.FEDERAL_CONTRACTOR_EPA_VIOLATOR` view to spills.
- **Known trap:** RESPONSIBLE_COMPANY is free text with no ID. Most of 1.03M incidents are minor sheens; filter CALL_TYPE.

### 104 Serial LLCs, repeat crashes
- **Chain:** `FED_NTSB_AVIATION_EVENTS` (EV_ID, EV_DATE, INJ_TOT_F) → `FED_NTSB_AVIATION_AIRCRAFT` registration → `FED_FAA_AIRCRAFT_REGISTRY` (REGISTRANT_NAME, TYPE_REGISTRANT, STREET, CITY) → registrants sharing an address.
- **Would show:** addresses behind many LLC-registered aircraft with more than one fatal event.
- **Known trap:** N-numbers recycle; join on registration plus a date window around CERT_ISSUE_DATE. NTSB aircraft columns not confirmed locally.

### 105 Same crossing, five hits
- **Chain:** `FED_FRA_CROSSING_INCIDENTS` crossing ID × year → `FED_FRA_CASUALTIES` → `FED_FRA_RAIL_DEATHS_BY_RAILROAD`.
- **Would show:** crossings struck five or more times since 2010, by railroad and county.
- **Known trap:** no crossing inventory table is landed, so "never upgraded" is untestable. Cross-section only. Crossing ID column not confirmed locally.

---

### D. Health corners the 75 skipped

### 106 The pill counties then, the prescribers now
- **Chain:** `FED_DEA_ARCOS_FULL` (BUYER_DEA_NO, BUYER_ZIP, BUYER_COUNTY, CALC_BASE_WT_IN_GM × MME_CONVERSION_FACTOR, TRANSACTION_DATE 2006–2014) → MME per capita by county → `FED_CDC_DRUG_POISONING_COUNTY` 1999–2015 → `FED_CMS_PART_D_PRESCRIBERS` DY2024 OPIOID_PRSCRBR_RATE by ZIP.
- **Would show:** whether the 2006–2014 top-MME counties are still the top opioid-rate counties in 2024, and which pharmacies there later hit LEIE.
- **Known trap:** 178.6M rows, the biggest table in the warehouse and never queried by a hunch. TRANSACTION_DATE is MMDDYYYY text, two rows hold floats. BUYER_DEA_NO joins nothing else; DEA_NO lives in one table. The small `FED_DEA_ARCOS` is the aggregated retail summary, not this.

### 107 Distributor share vs who signed the settlement
- **Chain:** ARCOS REPORTER_NAME share by state, McKesson, Cardinal, AmerisourceBergen → `FED_NAAG_MULTISTATE_SETTLEMENTS` (DEFENDANTS, TOTAL_SETTLEMENT_AMOUNT, TOTAL_STATE_SHARE, LEAD_AGS, PARTICIPATING_AGS, YEAR).
- **Would show:** states hit hardest per capita that were not lead AGs, and what they got.
- **Known trap:** 882 settlements, TOTAL_STATE_SHARE fill unknown. Defendant names are free text.

### 108 Royalties on a recalled device
- **Chain:** `FED_FDA_DEVICE_ENFORCEMENT` (RECALLING_FIRM, PRODUCT_CODE, CLASSIFICATION Class I, RECALL_INITIATION_DATE) → `FED_FDA_DEVICE_510K` K_NUMBER, APPLICANT → Open Payments NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_n and PDI → royalty recipients from hunches 18 and 57 → outpatient volume after the recall.
- **Would show:** surgeons paid royalties on a device later Class-I recalled, and whether their volume dropped.
- **Known trap:** use `HEALTH__FED_FDA_DEVICE_510K`, 175,686 rows; the LANDING name is an 88-row stub. Device name in Open Payments is free text across five product blocks. PRODUCT_CODE links 510k to recall cleanly; the payment leg is a name match.

### 109 Death reports by clearance path
- **Chain:** `FED_FDA_MAUDE` (EVENT_TYPE = Death, BRAND_NAME, DEVICE_REPORT_PRODUCT_CODE, BASELINE_510K_NUMBER) → `FED_FDA_DEVICE_510K` (CLEARANCE_TYPE, THIRD_PARTY_FLAG, EXPEDITED_REVIEW_FLAG).
- **Would show:** death reports per cleared device concentrating under third-party or expedited review.
- **Known trap:** use `HEALTH__FED_FDA_MAUDE`, 2.74M rows; LANDING `FED_FDA_MAUDE` is 1,386 and `_FULL` is 13k. MAUDE is 2020Q1 onward only. One report holds several devices via DEVICE_SEQUENCE_NUMBER; count reports, not rows.

### 110 Generic price spike, who rode it
- **Chain:** `FED_CMS_NADAC` (NDC, NADAC_PER_UNIT, EFFECTIVE_DATE) three-times jumps → `FED_NLM_DAILYMED_SPL_SETID_MAP` NDC → name → `FED_CMS_PARTD_PRESCRIBER_DRUG` "Gnrc_Name" Tot_Drug_Cst DY2022 by prescriber.
- **Would show:** the prescribers whose spend on a spiked generic rose fastest, and their Open Payments from its maker.
- **Known trap:** Part D drug file has names, no NDC; the bridge is DailyMed or string match. Use `FED_CMS_NADAC` in LANDING, 1.5M rows; the mart is a 359k slice. Drug-file columns are mixed case and need quotes.

### 111 Tribal areas losing the nearest hospital
- **Chain:** `FED_IHS_FACILITIES` and `FED_IHS_SCB_FACILITY` lat/lon → nearest non-IHS hospital in `FED_CMS_POS_OTHER` → TRMNTN_EXPRTN_DT → HPSA.
- **Would show:** IHS service areas whose nearest full hospital terminated since 2015, and the new drive distance.
- **Known trap:** IHS files carry no CCN; geography only. Hunch 29's 2023 termination spike is probably a coding sweep, check PGM_TRMNTN_CD.

### 112 Retractions per grant dollar
- **Chain:** `FED_NIH_REPORTER` (ORG_NAME, ORG_UEI, AWARD_AMOUNT) and `FED_SBIR_STTR_AWARDS` (UEI, COMPANY, PI_NAME, AWARD_AMOUNT) → `FED_RETRACTION_WATCH` (INSTITUTIONS, AUTHORS, REASONS, RETRACTION_DATE).
- **Would show:** institutions and SBIR firms with the most misconduct retractions per federal research dollar.
- **Known trap:** NIH Reporter is capped at FY2000–2002 by explicit instruction; SBIR is the live money leg. INSTITUTIONS is a semicolon list. Two Retraction Watch copies, 71,591 and 71,608 rows, not reconciled.

### 113 MDL products still promoted
- **Chain:** `FED_JPML_PENDING_MDLS` (LITIGATION, PENDING_CASES, JUDGE) → product and maker names → Open Payments payer + product → Part D or Part B volume after the MDL formed.
- **Would show:** drugs and devices under mass litigation whose makers kept paying doctors, and whether prescribing fell.
- **Known trap:** 162 rows, litigation names free text. Freshness unknown per registry.

---

### E. Labor

### 114 Injuries up, inspections zero
- **Chain:** `FED_OSHA_ITA_300A_SUMMARY_2023/24/25` (EIN, ESTABLISHMENT_ID, NAICS_CODE, TOTAL_DEATHS, TOTAL_DAFW_CASES, TOTAL_HOURS_WORKED) → rate trend per establishment → `FED_DOL_OSHA_INSPECTION` ESTAB_NAME + SITE_ZIP, OPEN_DATE → `FED_BLS_QCEW` wage.
- **Would show:** establishments whose days-away rate rose three years running with no inspection, rolled up by EIN to Form 5500, FAC and 990.
- **Known trap:** 300A is self-reported and thresholded to 20-plus employees in listed NAICS. Inspections carry no EIN; match name plus ZIP. EIN fill rate on 300A unchecked. The Form 5500 rollup needs `FED_DOL_FORM5500_FULL`, not the mart.

### 115 Unpaid penalties, then the accident
- **Chain:** `FED_MSHA_VIOLATIONS` (CONTROLLER_ID, PROPOSED_PENALTY, AMOUNT_DUE, AMOUNT_PAID, DOCKET_STATUS_CD) → `FED_MSHA_ACCIDENTS` by MINE_ID after the unpaid pile formed → `FED_MSHA_MINES` NO_EMPLOYEES.
- **Would show:** controllers ranked by unpaid penalty per employee, and accidents that followed.
- **Known trap:** literal double quotes on every value. Contested dockets sit in AMOUNT_DUE for years; split contested from delinquent.

### 116 Visa floor, willful violations
- **Chain:** `FED_DOL_OFLC` (EMPLOYER_NAME, VISA_CLASS, SOC_CODE, TOTAL_WORKER_POSITIONS, wage columns) → `FED_DOL_OSHA_INSPECTION` willful or repeat citations by ESTAB_NAME → `FED_SAM_EXCLUSIONS`.
- **Would show:** employers filing hundreds of H-2A or H-1B positions at the prevailing-wage floor with willful OSHA findings.
- **Known trap:** wage reflects the floor, not pay, per registry. EMPLOYER_NAME free text. Several programs share one table; filter VISA_CLASS.

### 117 PPP forgiven, fines unpaid
- **Chain:** `FED_SBA_PPP` (BORROWERNAME, BORROWERZIP, NAICSCODE 623110, FORGIVENESSAMOUNT) → `FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS` ORGANIZATION_NAME + ZIP_CODE → `FED_CMS_NURSING_HOME_PENALTIES`.
- **Would show:** nursing-home operators forgiven PPP who then paid the largest CMS fines, or none.
- **Known trap:** PPP is 150k-plus loans only. No EIN in PPP; name plus ZIP.

### 118 Lenders that charged off, then got an order
- **Chain:** `FED_SBA_LOANS` (BANKNAME, BANKFDICNUMBER, CHARGEOFFDATE, GROSSCHARGEOFFAMOUNT) → `FED_FDIC_ENFORCEMENT` (FDIC_CERT_NUMBER, ACTION_TYPE, DATE) → `FED_FDIC_FAILED_BANKS`.
- **Would show:** the lenders with the highest SBA charge-off rate and whether an enforcement order came before or after.
- **Known trap:** dead as written. `FED_FDIC_ENFORCEMENT` is **14 rows**. Nearest live version: charge-off rate by lender against `FED_FDIC_FAILED_BANKS` only. Six decade files with drifting schemas. BANKFDICNUMBER fill unknown.

---

### F. Immigration

### 119 Cost per detainee-day
- **Chain:** `FED_ICE_DETENTION_STINTS` (DETENTION_FACILITY_CODE, BOOK_IN_AT, BOOK_OUT_AT, DETENTION_RELEASE_REASON) → `FED_ICE_DETENTION_FACILITY_CODES` city and lat/lon → `FED_USASPENDING_CONTRACTS_FULL_R2` ICE sub-agency, place-of-performance city → `FED_SAM_EXCLUSIONS`.
- **Would show:** contractor dollars per detainee-day by facility, and the facilities with the longest median stay.
- **Known trap:** person-level data, authorized 2026-08-05; aggregate only, never surface PERSON_HASH. Contracts are by vendor, not facility. Facility list freshness unknown.

### 120 Detainers vs jail counties
- **Chain:** `FED_ICE_DETAINERS` → facility code → county → `XC_VERA_INCARCERATION_TRENDS`.
- **Would show:** counties where detainers per jail admission run highest.
- **Known trap:** the detainers mart carries one column; the landing table's width is unconfirmed. `FED_EOIR_CASE_DATA` is one unparsed tab-separated column and is dead until split.

---

### G. Corporate, offshore, nonprofit

### 121 Offshore doctors and donors
- **Chain:** `FED_ICIJ_OFFSHORELEAKS_OFFICERS` (NAME, COUNTRIES) → `FED_FEC_INDIV_CONTRIBUTIONS` DONOR_NAME + CITY, and Open Payments recipient names + city.
- **Would show:** US physicians and political donors who are officers of leaked offshore entities.
- **Known trap:** the officers table has no staging model; NAME and COUNTRIES are not confirmed locally. Eight ICIJ copies were the same snapshot with different blanks; use one. Many officer names are nominee directors. Multi-word plus city or nothing.

### 122 Sanctioned owners of UK companies
- **Chain:** `UK_COMPANIES_HOUSE_PSC` (NAME, NATIONALITY, COUNTRY_OF_RESIDENCE, DOB_MONTH, DOB_YEAR, NATURES_OF_CONTROL) → `INTL_OPENSANCTIONS_DEFAULT` and `FED_OFAC_SDN` names with birth date.
- **Would show:** sanctioned persons holding control of live UK companies, with the month and year of birth as the tie-breaker the name-leak trap needs.
- **Known trap:** 15.8M PSC rows. OpenSanctions IDENTIFIERS is an untyped blob; PROGRAM_IDS on 13% of rows. Use CEASED_ON to time it.

### 123 Parents nobody will name
- **Chain:** `INTL_GLEIF_REPEX` (LEI, EXCEPTION_CATEGORY, EXCEPTION_REASON_1) → `INTL_GLEIF` (ENTITY_LEGAL_JURISDICTION, ENTITY_COUNTRY) → HMDA LEI xref lenders and the EPA corporate crosswalk.
- **Would show:** US lenders and polluters whose ultimate parent is a declared reporting exception, and the jurisdictions they sit in.
- **Known trap:** GLEIF prunes ended relationships; the July vintage is in RAW.RETIRED. REPEX is 6.3M rows; the exception list is itself the lead.

### 124 Thin charity, fat officers
- **Chain:** hunch 68 hospitals → `FED_IRS_BMF` (NTEE E22, EIN, REVENUE_AMT) by name + state → `FED_IRS_990_EFILE_INDEX` return URLs.
- **Would show:** officer compensation at the 37 nonprofit hospitals under 1% charity care.
- **Known trap:** dead as written. `FED_IRS_990` is a 200-row stub and the e-file index holds URLs, no amounts. The XML parse is a separate build. Tier 3.

### 125 527s that lost their exemption
- **Chain:** `POLITICS__IRS527_8871_ORGS` EIN → `FED_IRS_AUTO_REVOCATIONS` (REVOCATION_DATE, REINSTATEMENT_DATE, EXEMPTION_TYPE) → `POLITICS__IRS527_8872_REPORTS` filed after.
- **Would show:** political orgs still filing 8872 reports after revocation.
- **Known trap:** revocation is a 501(c) list; check EXEMPTION_TYPE before calling a 527 hit real. Hunch 65 found reinstatements erase most of these.

---

### H. Consumer finance and banking

### 126 Complaints before the order
- **Chain:** `FED_CFPB_COMPLAINTS` (COMPANY, PRODUCT, ISSUE, STATE, DATE_RECEIVED, COMPANY_RESPONSE) monthly by company → `FED_FDIC_ENFORCEMENT` (INSTITUTION_NAME, ACTION_TYPE, DATE) → HMDA lender denial rate by race via the LEI xref.
- **Would show:** lenders whose complaint volume climbed for a year before an enforcement order, and their denial gap.
- **Known trap:** the enforcement leg is dead, `FED_FDIC_ENFORCEMENT` is 14 rows; run complaints straight against the HMDA denial gap. 17.2M complaints, unverified by CFPB. COMPANY mixes subsidiary and parent. HMDA denials exist after the all-records reload, per hunch 5.

### 127 Branches leaving the D zones
- **Chain:** `FED_FDIC_SOD_BRANCH_DEPOSITS` (SURVEY_YEAR, FDIC_CERT, BRANCH_NUMBER, BRANCH_DEPOSITS_THOUSANDS, SIMS_LATITUDE, SIMS_LONGITUDE) → ST_CONTAINS on the HOLC polygons from hunch 22.
- **Would show:** net branch count and deposits by HOLC grade, year over year.
- **Known trap:** find which survey years landed before claiming a trend. Branch numbers get reused. SIMS lat/lon fill unchecked.

### 128 Still on the FHLB roll
- **Chain:** `FED_FHFA_FHLB_MEMBERSHIP` (MEMBER_NAME, CERT, MEM_DATE) → `FED_FDIC_ENFORCEMENT` FDIC_CERT_NUMBER → `FED_FDIC_FAILED_BANKS` FDIC_CERT.
- **Would show:** members under an open enforcement order, and how many failed banks were members at failure.
- **Known trap:** the enforcement half is dead, 14 rows. Failed-banks half stands. No advance amounts in the membership file, so no dollars. Cert join is clean.

### 129 Complaints pile up, recall comes late
- **Chain:** `FED_NHTSA_COMPLAINTS` (C3 manufacturer, C4 make, C5 model, C6 year, C8 date, C12 component) → `FED_NHTSA_RECALLS` (MAKETXT, MODELTXT, YEARTXT, COMPNAME, BGMAN, ODATE, RCDATE, POTAFF).
- **Would show:** make-model-years where complaints on a component ran two-plus years ahead of the recall, ranked by units affected.
- **Known trap:** complaints are headerless C1..C54 with 110k blank dates. Component vocab differs between files.

### 130 Expiring Section 8 in hot markets
- **Chain:** `FED_HUD_MF_SECTION8_CONTRACTS` (TRACS_OVERALL_EXPIRATION_DATE, ASSISTED_UNITS_COUNT, RENT_TO_FMR_RATIO, PROPERTY_ID) → county → `FED_FHFA_HPI` (PLACE_ID, YR, INDEX_SA) growth.
- **Would show:** where the most assisted units expire 2026–2028 in the fastest-appreciating counties.
- **Known trap:** expiration is not opt-out. PROPERTY_ID has no crosswalk to other HUD tables. HPI PLACE_ID mixes state, MSA and ZIP3 levels.

### 131 FHA rates by lender in D zones
- **Chain:** `FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT` (ORIGINATING_MORTGAGEE_NAME, INTEREST_RATE, PROPERTY_ZIP, ENDORSEMENT_YEAR) → ZIP to HOLC grade → HMDA lender by name.
- **Would show:** lenders charging the highest FHA rates in redlined ZIPs.
- **Known trap:** one month's snapshot. Lender name, not LEI.

---

### I. Justice and security

### 132 Bankruptcy after the declaration
- **Chain:** `FED_FJC_IDB_BANKRUPTCY` (DEBTOR1_ZIP, FILE_DATE, CURRENT_CHAPTER, NATURE_OF_DEBT, CASE_KEY) → IA DECLARATION_DATE by county → hospital terminations from hunch 29 as a second trigger.
- **Would show:** Chapter 7 filings per capita in the 12 months after a declaration against the same ZIP the year before.
- **Known trap:** one case appears in several snapshots; dedupe on CASE_KEY. Debtor ZIP is at filing.

### 133 Sued chains, fined chains
- **Chain:** `FED_FJC_IDB_CIVIL` (DEFENDANT, NATURE_OF_SUIT, FILE_DATE, AMOUNT_DEMANDED, DISPOSITION, CLASS_ACTION) → NH411 CHAIN_ID names → penalties.
- **Would show:** suits per bed by chain, and whether suits lead or follow the CMS fine.
- **Known trap:** DEFENDANT is truncated and first-listed only. Nature-of-suit codes need the FJC codebook, not landed.

### 134 Convicted, not yet excluded
- **Chain:** `FED_FJC_IDB_CRIMINAL` (DEFENDANT_NAME, FILING_OFFENSE_CODE_1 health-care fraud, DISTRICT, FILE_DATE, disposition) → `FED_HHS_OIG_LEIE` name + EXCLDATE → NPPES.
- **Would show:** health-fraud defendants with no LEIE entry, and the lag from judgment to exclusion for those with one.
- **Known trap:** DEFENDANT_NAME is often redacted or initials; check fill. Offense codes need the codebook. LEIE has a real NPI on a tenth of rows.

### 135 Ransomed hospitals, next year's stars
- **Chain:** `XC_RANSOMWARELIVE_VICTIMS` (POST_TITLE, GROUP_NAME, DISCOVERED, COUNTRY) → `FED_CMS_HOSPITAL_GENERAL` and NH411 names → star rating and terminations after.
- **Would show:** the hospitals and nursing homes hit, by gang, and what happened to their ratings.
- **Known trap:** POST_TITLE is the gang's own label for the victim. 31k rows, multi-word rule.

### 136 Exploited vendors, federal IT dollars
- **Chain:** `FED_CISA_KEV` (VENDOR_PROJECT, PRODUCT, DATE_ADDED, KNOWN_RANSOMWARE_CAMPAIGN_USE) → `FED_USASPENDING_CONTRACTS_FULL_R2` RECIPIENT_NAME, NAICS 5415.
- **Would show:** vendors with the most exploited vulnerabilities against their federal contract totals.
- **Known trap:** VENDOR_PROJECT is a brand, not a legal entity.

### 137 Sanctioned ships in US water
- **Chain:** `FED_OFAC_SDN` vessel rows (IMO_NUMBER, VESSEL_FLAG, program) → `FED_NOAA_AIS` IMO → positions inside US ports after the designation date.
- **Would show:** designated vessels pinging US ports.
- **Known trap:** IMO was regex-extracted from SDN REMARKS. AIS is 58M rows, landing only, columns and date window unconfirmed locally.

### 138 Federal grants to the deadliest departments
- **Chain:** `XC_MAPPING_POLICE_VIOLENCE` (AGENCY_RESPONSIBLE_FOR_DEATH, ORI, county, year) → `FED_USASPENDING_ASSISTANCE_FULL` recipient name → COPS and JAG dollars.
- **Would show:** departments ranked by killings per officer against their federal grant dollars.
- **Known trap:** the assistance table is a 1M-row-per-year cap holding 34% of days, per hunch 66. Agency names free text, ORI partial.

### 139 Gun dealers, denials, deaths
- **Chain:** `FED_ATF_FFL` dealers by county → `FED_FBI_NICS_CHECKS` by state-month → `XC_MAPPING_POLICE_VIOLENCE` and `FED_CDC_INJURY_VIOLENCE_COUNTY` firearm rows.
- **Would show:** dealer density against firearm death rate, state level.
- **Known trap:** NICS is state-month, so the county leg collapses. FFL columns not confirmed locally. Tier 2.

---

### J. Energy

### 140 Who owns the dirtiest plants
- **Chain:** `FED_EPA_EGRID_PLANT_2022` (ORIS code, CO2 tons, NOX rate) → `FED_EIA860_4_OWNER` (PLANT_CODE, OWNER_NAME, PERCENT_OWNED) → `FED_SEC_13F_POSITIONS` ISSUER_NAME → `FED_FEC_PAC_SUMMARY` by owner PAC.
- **Would show:** the funds and PACs behind the top-emitting plants, weighted by percent owned.
- **Known trap:** owner names are not LEIs or CIKs. eGRID is one year. 13F VALUE is in thousands in the raw file.

### 141 Worst outages, most storms, same rates
- **Chain:** `FED_EIA861_RELIABILITY` (SAIDI, SAIFI by utility) → `FED_EIA861_SERVICE_TERRITORY` utility → county → `FED_NOAA_STORM_EVENTS` damage by county → `FED_EIA861_SALES_ULT_CUST` revenue per customer.
- **Would show:** utilities with the worst outage minutes in the most storm-hit counties, and what they charge.
- **Known trap:** reliability is self-reported with two SAIDI definitions, IEEE and other. 971 rows.

### 142 Emission spikes with no violation
- **Chain:** `FED_EPA_CAMPD_EMISSIONS_DAILY` (16.5M rows, landing) unit-day SO2 and NOx → `FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY` by FRS → `FED_EPA_AQS_SITES` nearby monitors.
- **Would show:** units with daily emission spikes and no violation on record.
- **Known trap:** CAMPD `_INGESTED_AT` holds epoch micros as seconds. Columns not confirmed locally.

---

### K. Two that are dead on arrival, so nobody re-checks

| # | Hunch | Why it dies | Nearest live version |
|---|---|---|---|
| 143 | Clinical trial sponsors paying their own PIs | `FED_CLINICALTRIALS` is 500 rows; AACT not landed | wish list |
| 144 | Immigration court outcomes by judge and detention facility | `FED_EOIR_CASE_DATA` is one unparsed column | split the column first, then hunch 119 gets a court leg |

---

### Wish list additions, scored the same way as the first five

| Rank | File | Unlocks |
|---|---|---|
| 6 | FJC IDB codebooks for nature-of-suit and offense codes | 133, 134, 94 |
| 7 | House disbursement and PTR detail lines, not the index | 91, 92 |
| 8 | EAVS codebook | 93 |
| 9 | FRA crossing inventory | 105 |
| 10 | IRS 527 Schedule A/B, 17.9M rows | 88, 125 |
| 11 | EOIR column split, no new download | 144, 119 |
| 12 | AACT clinical trials | 143, 113 |

### Skeptic verdict on this appendix
Local files only, no warehouse. Column claims held on 24 of 24 cards checked;
row counts held on 30-plus. Four cards quoted the mart as the ceiling while a
bigger LANDING table sat in the same JSON; fixed above. One leg was a 14-row
table, `FED_FDIC_ENFORCEMENT`; 118, 126 and 128 now say so. Three cards cited
columns with no staging model and now say so. The blind spot stands: a column
can exist and be empty, and nothing here checked fill.

### Next step
Same as appendix 1. Each card is one probe query for a first number. That is
warehouse cost. Say go on a category letter and a price estimate comes first.
The Python door is the only one open; the chat plug-in is still 401.
