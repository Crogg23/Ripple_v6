# Skeptic g8, round 2, 2026-09-24

Leads from `deep2/deep-7.md`. My SQL is in `skeptic-g8.sql`, labelled [L1-n], [L2-n], [L3-n].
Door: Python. Chat plug-in not tried (brief says it is dead).
Every person or company named is a **data match, not verified against primary records.**

| Lead | Verdict | Grade |
|---|---|---|
| RHC for-profit flip after the 2021 pay law | **NARROWED** | B |
| Houston hospice suite 610 / shared phones | **CONFIRMED** (one caveat added) | B |
| Reliant Care Management harm citations | **CONFIRMED** (stronger than written) | A- chart / B story |

---

## HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS: NARROWED

**Claim as written:** after the 2021 pay change, for-profit share of new RHC enrollments went 27% (2020) to 56% (2023). Fast Pace holds 189 clinics under 48 NPIs, all enrolled Nov 2021 on. "No big year-end-2020 rush."

**What I checked:**
- [L1-4] Found a second clock: `HEALTH__FED_CMS_POS_OTHER`, category 12 = RHC. 12,864 CCNs, 5,756 still active. It has original participation date, CHOW count and CHOW date, and it **keeps terminated clinics**.
- [L1-5] Joined enrollment CCNs to POS. Land rate about 98% every year.
  - For-profit share reproduced: 104 of 389 (26.7%) in 2020, 193 of 344 (56.1%) in 2023.
  - **CHOW attack fails.** For-profit enrollments with a CHOW within a year of the enrollment date: 3 to 14 a year. For-profit "new" enrollments whose clinic started 2+ years earlier: 8 to 21 a year.
  - Truly new for-profit freestanding clinics (POS start no more than a year before enrollment): 73 (2020), then 172, 142, 162, 133 (2021-2024).
- [L1-6] **Survivorship attack fails.** POS by original participation year, dead clinics included: freestanding 123 (2020), then 154, 230, 209, 179 (2021-2024). Provider-based 301 (2020) down to 122 (2022).
- [L1-7] **Rush attack succeeds.** By POS participation date, provider-based starts spike: **60 in Dec 2020 and 50 in Mar 2021**, against about 20 in a normal month. The deep pass used the enrollment-ID date, a different clock, and missed it.
- [L1-8] Fast Pace: 189 by legal name (confirmed), **192 with a DBA-only match** (Calcasieu Urgent Care LLC). **50 NPIs, not 48.** 4 have POS start dates before July 2021 (one from 1985) and 5 carry a CHOW: a few acquired clinics, not all new builds. **64 Fast Pace clinics started in one month, Feb 2022.** 192 of 731 for-profit freestanding since July 2021 = 26%.

**What a hit means / what a miss means:**
- Hit: new freestanding for-profit clinics nearly doubled per year after the law. It holds on dead clinics and on a second date field.
- Miss (partial): the jump in **share** is half denominator. CAA 2021 capped new hospital-owned RHCs (enrolled after 2020-12-31), so hospitals rushed in before the date, then stopped. That is the law doing what it said, and RHC trade groups wrote about it at the time. Not news.
- The new part is who filled the gap: one urgent-care chain took a quarter of the new for-profit slots, 64 in a single month.
- Untested: whether these sites are really rural.

**Corrected headline:** After Congress capped new hospital-owned rural clinics in 2021, hospitals rushed 60 in during December 2020, then new hospital-owned clinics fell by more than half. New freestanding clinics went from 123 in 2020 to 230 in 2022. One urgent-care chain, Fast Pace, holds 192 of them, and 64 opened in February 2022 alone.

**Portfolio grade:** B. Needs the rule text quoted and a rurality check.

**Next join that would make it a story:** RHC CCN to `POS_OTHER.CBSA_URBN_RRL_IND` on CCN (tests "really rural", one query). Fast Pace NPIs to Part B / Open Payments on NPI for billing volume. RHC cost reports on CCN for per-visit rate, if landed.

---

## HEALTH__FED_CMS_HOSPICE: CONFIRMED

**Claim as written:** Five hospices in 7322 Southwest Fwy Suite 610, "Rooms A to E", certified within 8 weeks in 2023. 6 share one phone in a Rosedale St building. Harris County: 16.7% of hospices share a phone with another hospice, against 4.5% nationally.

**What I checked:**
- [L2-1] Every row at both buildings and on both phones.
  - Suite 610 Rooms A-E: Origins, Timeless Moments, Heart & Soul, Loving Hands, Blue Rose. Certified **2023-04-13 to 2023-06-08**, 8 weeks. 4 on (281) 410-1013; Room D lists no phone. Confirmed.
  - **New:** all five have a **blank ownership type** and **no row in the Medicare hospice enrollment file.** No owner ID, no NPI, nothing to follow.
  - The building alone means nothing: other hospices there sit in Suite 868 and "Suite 1-1182" (looks like a mail drop). The one suite split into lettered rooms is the signal.
  - 2922 Rosedale: 6 on (713) 874-1234 in suites 1200-1410, certified 2022-04-01 to 2022-10-14. Confirmed. The same phone is on Heritage Hospice (owner Tulip Hospice LLC) and Compassion Hospice of Texas, San Antonio (owner New Dawn Hospice Inc).
- [L2-2] Harris: 37 of 221 share a phone (16.7%). US: 309 of 6,852 (4.5%). Confirmed. 8 of the 37 are same-brand pairs (Choice, Premier, Harbor, Peaceful Bridge, JOL): ordinary central lines.
- [L2-5] Stricter test, shares a phone with a **differently named** hospice (first 6 letters differ, filler 909-000-0000 dropped): Harris **13.1%** (29 of 221), Bexar 10.9%, Clark NV 5.2%, LA 2.4%, everywhere else 1.2%. The gap gets **wider**, not narrower.
- [L2-3] There is no hospice billing or revocation table in the warehouse.
- [L2-4] Certified but not in the enrollment file: Harris 48 of 221 (22%), rest of CA/NV/AZ/TX 721 of 3,353 (22%), rest of US 107 of 3,278 (3%). **"Missing from enrollment" is a four-state pattern, not a Houston one.** Those are CMS's hospice enhanced-oversight states.

**Round 1 overlap:** none. Round 1 was LA address stacking and the CFHC NO4-NO22 series at 2819 NW Loop 410, San Antonio. The San Antonio hospice on the Houston phone is at 15600 San Pedro Ave under New Dawn Hospice Inc, not a CFHC entity.

**What a hit means / what a miss means:**
- Hit: Houston hospices with different names share phones at about 10x the rate seen outside Harris, Bexar, LA and Clark counties. Five sit in one suite and were certified in 8 weeks.
- Not ruled out: the roster does not prove they **bill**. No enrollment row could mean never enrolled or already revoked. A shared answering service could explain phone groups; it does not explain one suite split into rooms.
- Known story? Texas is one of CMS's four enhanced-oversight states and Houston hospice cases have been prosecuted. These specific addresses: I don't know of coverage, and I can't check the web.

**Corrected headline:** Five Houston hospices list one suite, 7322 Southwest Fwy #610, split into Rooms A to E. All five were certified between April 13 and June 8, 2023, four share one phone, and none has an owner on file in Medicare's enrollment list. Across Harris County, 13% of hospices share a phone with a differently named hospice, against 1.2% everywhere outside Harris, Bexar, Los Angeles and Clark counties.

**Portfolio grade:** B. Needs a primary check (Texas HHSC license search, CMS revocations) on whether the Room A-E five still operate.

**Next join that would make it a story:** hospice CCN to a Medicare hospice utilization file on CCN (not landed); the 874-1234 owner ASSOCIATE_IDs to a hospice owner file (not landed); Texas SOS on legal name for officers.

---

## HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: CONFIRMED

**Claim as written:** Reliant Care Management (MO/KS, 32 homes) drew 3.4x the harm citations per bed of its own states: 152 vs 45 expected, 70 immediate jeopardy.

**What I checked:**
- [L3-1] Duplicates: 418,479 rows, 418,479 distinct (home, survey date, tag, severity). One vintage, 2026-06-01. No double counting.
- [L3-2] Chain label: one CHAIN_ID ('446'), 32 homes, facility-count field agrees. 3,122 beds. **Average star 1.19, 5 SFF candidates, 13 abuse icons.**
- [L3-3] Per home since 2023-06-17: **152 harm, 70 J-L. Confirmed.**
  - It is **31 Missouri homes and 1 Kansas home** (Holton, 7 harm). "MO/KS" oversells Kansas.
  - One bad home? Top home (Bridgewood, Kansas City) = 24. Top 4, all SFF candidates, = 76, half the total. 24 of 32 homes have harm.
  - Almost all harm came from **complaint** surveys. Bridgewood had 33 survey dates in about 3 years.
- [L3-4] Reliant vs other Missouri homes, per 100 certified beds:

| Group | Homes | Harm | Standard-survey harm | J-L | Surveys per home | Harm per survey |
|---|---|---|---|---|---|---|
| Other MO | 456 | 1.22 | 0.25 | 0.42 | 5.0 | 0.25 |
| Reliant, all | 31 | **4.71** | 0.75 | **2.14** | 9.4 | 0.50 |
| Reliant minus top 1 | 30 | 4.16 | 0.79 | 1.86 | 8.6 | 0.47 |
| Reliant minus top 4 | 27 | 2.77 | 0.60 | 1.00 | 7.3 | 0.35 |

  - Against non-Reliant Missouri homes it is **3.9x**, not 3.4x. The deep pass left Reliant inside its own state baseline, which was conservative.
  - Top 4 removed: still **2.3x**. Routine standard surveys only: **3.0x**. Per survey visit: **2.0x**. More visits explain part of it, not all.
- [L3-5 to L3-10] Chain-timing attack, through the SNF enrollment and owner files. Owner dates are free text, parsed MM/DD/YYYY, "ADP" role rows dropped.
  - **133 of 152 harm citations came after Reliant's earliest ownership or control date at that home.** 15 before, 4 at a home with no Reliant owner row (Cassville).
  - **63 of 70 J-L** came after.
  - The top four homes were Reliant's long before the window: Bridgewood 2008, Heritage 1993/96, Gregory Ridge 2016, North Village Park 1989.
  - Holton KS joined 2025-01-25; its last J-L is 2024-08-19, **before** Reliant. The Kansas piece is mostly pre-Reliant.
  - One helper column in [L3-10] (homes joined in window = 33, of 32) is a join fan-out. I did not use it.
- Bed base: certified beds, not residents. Reliant runs near full (231 residents in 239 beds at Four Seasons), so a resident base would not shrink the gap.

**What a hit means / what a miss means:**
- Hit: a 31-home Missouri operator draws about 4x the harm citations per bed of other Missouri homes, at homes it has run for years. It holds above 2x with its four worst homes removed.
- Miss: none of my attacks broke it. Duplicates, one-home, state strictness, ownership timing, survey counts: none explains it.
- Known? CMS's own stars already say it: 1.19 stars on average, 5 SFF candidates. This re-derives CMS's verdict with a cleaner, checkable number. Missouri press may have covered Reliant; I can't check.
- Minor, for the deep pass: CHAIN_ID is text, and independents sit in one '' bucket, not null. "About 300 chains" may include that bucket. It does not move Reliant.

**Corrected headline:** Reliant Care Management's 31 Missouri nursing homes drew 4.7 harm-level citations per 100 beds since mid-2023, against 1.2 at other Missouri homes (3.9x). 133 of the 152 came after Reliant took control, and with its four worst homes removed it is still 2.3x.

**Portfolio grade:** A- for the chart (own-state, survives leave-out and timing). B for a story until a few J-L citation texts are read.

**Next join that would make it a story:** `HEALTH__FED_CMS_NURSING_HOME_PENALTIES` on CCN for fines after the J-L dates; `LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP` owners (ASSOCIATE_ID_OWNER) to Missouri SOS on name; the relief-money rows in `reports/dead_ends_build_B_prf_2026-09-07.md` on CCN.

---

**Statements:** L1 8, L2 5, L3 10 (two table-name lookups, two failed and rerun). All under the 12 cap.
