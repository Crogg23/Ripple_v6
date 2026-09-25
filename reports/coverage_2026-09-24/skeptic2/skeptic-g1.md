# Skeptic round 2, group g1: deep-0 leads 1 and 2

2026-09-24. Python door, tag `skeptic-r2-2026-09-24`. Read-only. Every statement is in `skeptic-g1.sql`.
Budget: lead 1 used 11 statements (one failed to compile and was rerun), lead 2 used 8.
Every person, company or group named here is a data match. None is checked against primary records.

| Lead | Verdict | Grade |
|---|---|---|
| IRS auto-revocations x single audits | **NARROWED** | B |
| NHTSA PE19010 Nissan (open 7 years) | **CONFIRMED** (numbers reproduce) | B |
| NHTSA EA18003 VW (the "second" 7-8 year probe) | **BROKEN** | D |

---

## ECONOMICS__FED_IRS_AUTO_REVOCATIONS: NARROWED

**Claim as written:** 64 nonprofits spent $940M in federal money after the IRS revoked their exemption. 27 are HUD elderly/disabled housing ($435M). 5 still hold active HUD Section 202 contracts.

**What I checked:**
- A02. Single-audit table grain: 411,638 rows = 411,638 report IDs. One row per report, so no repeated totals across rows.
- A02. IRS master file (BMF): 1,983,563 EINs, 62 states/territories, loaded 2026-08-10. That is a full snapshot, so "not in the BMF" means something.
- A04. Rebuilt the clean set. **64 EINs, $939,835,377.** It reproduces exactly.
- A04/A08. **The $940M is not mostly revoked charities.** The top rows are governments or EIN slips:
  - Hawaii Health Systems Corp: a state agency, $148.9M
  - Des Moines schools: $51.2M
  - Elko County School District: $17.6M. It files under 886000985 in every other year.
  - UNC Hospitals: $6.9M
  - Pawtucket Housing Authority: $13.6M. Its 2022 audit used 056000192. Every other year it used 056000191, a one-digit slip.
- A08. **Hunters Woods Elderly Developments (VA), $54.0M, is a false hit.**
  - The same name, in the same state, holds EIN 475323918 in the BMF, with a ruling of 2016-02.
  - It filed single audits under that EIN from 2016 to 2023.
  - The revoked EIN is an old or mistaken number, not a revoked charity.
- A05. The two-row EINs, Jaycee and Dalewood, are real repeat revocations.
  - The 2010 revocation was reinstated back to 2010-05-15.
  - They were revoked again 2020-05-15, with no reinstatement.
  - Winchester Senior Housing (NV) WAS reinstated on 2017-09-15. Its only hit year is 2016. It is not "still revoked."
- A09b. My housing count: elderly/disabled housing names, minus Puerto Rico, minus housing authorities, minus Hunters Woods.
  - **26 EINs, $362.4M summed across years**
  - **$77.1M if you take each one's largest single year**
  - 16 of the 26 filed a single audit for 2024 or later
- A10. **The dollars are a loan balance repeated every year, not spending.** Year by year, in $K:
  - Hoover Seniors: 5,288 / 5,297 / 5,281 / ... / 5,358
  - Camellia Manor: 2,890 to 2,879
  - Tupqich: about 1,006-1,021
  - Bishop Richard B Martin HDFC: about 12.9-13.5M every year
  - That is the HUD 202 capital advance balance, restated in every audit. Summing across years multiplies it.
- A06/A07. The HUD Section 8 contract table has **no state column**. So the deep pass's HUD match was name-only.
  - I checked state against HUD's Picture of Subsidized Households (Q4 2025), which does carry a state:
    - Camellia Manor: GA = GA
    - Jaycee Estates: OH = OH, 99 units
    - Hoover Senior Apts: CA = CA
    - Tupqich Elder Apts: AK = AK
    - Hillside Gulfport Manor: HUD says MS. The single audit says New Orleans, LA, which is probably the management office's address. Plausible, not proven.
  - All 5 show Active 202 contracts, ending 2028-2033.
  - Jaycee's "two contracts" is one property ID on two rows, 50 and 49 units.

**What a hit means / what a miss means:**
- Hit: small single-property HUD elderly-housing owners lost federal tax exemption years ago. HUD is still paying them rent subsidy and carrying their capital advance.
- Miss: if HUD's 202/811 rules do not require 501(c)(3)/(c)(4) status for the owner, or the IRS reinstated them in a way neither file shows, it is paperwork.
- My belief, **not verified**: 24 CFR 891 requires the owner to be a private nonprofit with (c)(3) or (c)(4) status. That rule is the hinge. Check it before anything else.
- Not ruled out: some of these file under a parent's group return and got swept up anyway.

**Corrected headline:**
- 26 small HUD elderly/disabled-housing nonprofits kept filing federal single audits after the IRS auto-revoked their exemption.
- None shows a reinstatement, and none is in the Aug 2026 IRS master file. 16 filed for 2024 or later.
- 5 match active HUD Section 202 contracts by name and state: Camellia Manor GA, Jaycee Estates OH, Hoover Seniors CA, Tupqich AK, Hillside Gulfport MS.
- The money is mostly a HUD capital-advance balance restated each year: $77.1M if you take each one's largest year.
- **Drop the $940M and the $435M.** Those sum a repeated balance across years, and $940M also mixes in governments.

**Portfolio grade:** B. The count and the names hold up. The dollar figure has to change. The HUD rule must be checked outside the warehouse.

**Next join that would make it a story:**
- USAspending assistance, joined on FAC `AUDITEE_UEI` to the recipient UEI, with assistance listings 14.157 (202) and 14.181 (811).
- That gives the actual yearly rent-subsidy payments instead of the loan balance, and dates the most recent payment.

---

## CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS: CONFIRMED for PE19010, BROKEN for EA18003

**Claim as written:**
- Nissan's false-braking probe PE19010 has been open 2,572 days, against a 234-day median.
- 75 complaints came in before it opened and 273 after.
- Two probes have sat open 7-8 years with no recall while complaints kept coming.

**What I checked:**
- B02. File freshness: loaded 2026-09-19. Newest open is 2026-09-14, newest close 2026-09-03. 29 probes closed in 2026.
  - So closures are being picked up. The file is not frozen.
  - It cannot prove the status of any one probe.
- B03. PE19010 covers 2017-2019 Rogue, 3 rows, component "forward collision avoidance: AEB."
  - It opened 2019-09-09 after petition DP19-001 from the Center for Auto Safety.
  - It is open on every row. The recall number is an empty string.
- B04. The recall file has **no recall** on a 2017-2019 Rogue that touches collision avoidance, brakes or "emergency braking."
- B05. **The right comparison is PEs only.**
  - Closed PEs opened 2010 or later: 410. Median 215 days, 90th percentile 650 days.
  - The slowest closed PE took 2,596 days.
  - Only 2 PEs opened before 2022 are still open: PE19010 and PE21012 (Ferrari).
  - PE19010 is at 12x the PE median.
- B06. No successor probe. DP19001, the petition, closed 2019-09-16 and PE19010 is the grant. There is no later Nissan AEB EA.
- B07. Rogue 2017-19 complaints coded to forward collision avoidance, by year received:
  - 8 / 50 / 26 / 30 / 71 / 56 / 40 / 32 / 17 / 18, for 2017 through 2026
  - That is 75 before the open date and 273 after, **reproduced**
  - They peaked in 2021 and are down to 17-18 a year
  - Another 241 complaints describe AEB or phantom braking in the text but sit under a different component, 117 of them in 2019. The component-only count is a floor.
- B05/B06/B04. **EA18003 (VW clockspring) is not a "no recall" probe.**
  - The clockspring defect was recalled in 2015 (15V-483, after PE15010).
  - Recall query RQ17009 then upgraded to EA18003. It is a check on whether the 2015 fix worked.
- B08. **EA18003's complaint counts are mostly the wrong defect.**
  - The loose "AIR BAGS" match on the same cars pulls in inflator recalls: 16V-078, 18V-148 and 24V-834 all cover the same models.
  - Of the 714 "after" complaints, 307 mention the clockspring. 409 mention the inflator, Takata, rupture or a recall.
  - Before the open date, 1,159 of 1,413 are inflator/recall.
  - Injury complaints after the open that mention the clockspring: **1** (the deep pass had 34, plus 2 deaths).

**What a hit means / what a miss means:**
- Hit (PE19010): the short first-step probe on phantom braking has sat 7 years. It is the oldest open PE since 2010, with no recall, and owners keep complaining.
- Miss: nhtsa.gov shows PE19010 closed or upgraded after the 2026-09-19 pull. Or Nissan fixed it with a software update or service bulletin, which is not a recall and would not show here.
- Famous? The 2019 petition and the probe's opening drew trade-press coverage, as far as I know. I cannot check later coverage without the web.

**Corrected headline:**
- NHTSA's preliminary evaluation into false automatic emergency braking on 2017-2019 Nissan Rogues (PE19010, opened 2019-09-09 after a safety-group petition) is still open in the September 2026 file.
- It has run 2,572 days, 12x the 215-day median for a closed PE.
- It is one of only two pre-2022 PEs still open, and no Rogue braking recall exists.
- 273 complaints coded to the system came in after it opened, tapering to about 17 a year.
- **Drop EA18003 from the headline.** It follows up on a 2015 recall, and its complaint count is mostly Takata-type inflator complaints.

**Portfolio grade:** B for PE19010. It needs one outside check, the live status on nhtsa.gov. D for EA18003 as written.

**Next join that would make it a story:**
- Complaints joined on VIN or ODINO to the complaint text, for a hand-coded sample of the 273. Are they real phantom-braking crashes or near-misses?
- Then the Nissan Technical Service Bulletins, which are not in the warehouse, if a quiet software fix exists.
