# sweep-a: 25 singles rows

**Result: 19 probed, 5 skip, 1 dead, 0 live.**
None of my rows has a number that points at a story nobody has reported.
The main haul is **eight data traps**, four of them on the lead column of their row.

Statements: **63 of 120.** Six of them errored (a wrong table name, two wrong column guesses, one `ISNAN`), so they read nothing.
Every query is in `sweep-a.sql`.
Table names are `LIBRARY_MARTS.<SCHEMA>.<SCHEMA>__<TABLE>`, the row id with the schema added in front. The brief's short form does not resolve.

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| HEALTH__FED_HRSA_NPDB | probed | **mart TOTAL_PAYMENT is empty on all 1.91M rows**; landing PAYMENT holds 532,681 payments, median $105K, $137.8B |
| FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | probed | ActBlue $6.8B + WinRed $2.6B, 70M of their rows are 24T earmarks that recipients also book as 15E; odd row: "DODO GOVERNMENT" $100M type 19 |
| ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | probed | 93.1M rows, $450-775B a year; min/max are fat-finger pairs that cancel (±$344.7B in 2013) |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | probed | 128.2M rows, all 12 months of every year (the old 1M-a-year cap is gone); Medicare/Medicaid rows 2012-16 stop at exactly $9,999,999,999 |
| ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | skip | cap still holds: exactly 1,000,000 rows each year, 2-5 months landed |
| ECONOMICS__FED_USASPENDING_CONTRACTS | skip | one fiscal year only (Oct 2024 to Sep 2025), already inside R2 |
| PROCUREMENT__FED_USASPENDING_BULK | skip | 50K-row sample |
| HOUSING__FED_CFPB_HMDA | probed | DC 2022 only, 28,301 rows, denials 14.2% |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | skip | row-for-row copy of FED_CFPB_HMDA (EXCEPT returns 0) |
| HOUSING__FED_CFPB_HMDA_LAR | probed | DC 2023, 17,474 rows, denials 17.1%; may be the full DC year, not a sample (not checked) |
| IMMIGRATION__FED_ICE_DETENTION_STINTS | probed | only 141,515 of 2.57M stints are before 2023; bond posted on 94.5% of bonded stints |
| TRANSPORT__FED_FRA_CROSSING_INCIDENTS | probed | deaths per crash rose 7.6% (1970s) to 13.0% (2020s); Amtrak 24%, Metra 27% |
| TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | probed | TOTAL_DAMAGE_COST repeats in full on each railroad's row; $17.6B raw sum double counts |
| JUSTICE__FED_FJC_IDB_CRIMINAL | probed | 6.30M rows = 2.64M defendants; FINE_AMOUNT_1 stops at $99,999,999 (71 rows) |
| JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | probed | money in $ thousands, 9999 means $10M or more; only 457K cases have AMOUNT_RECEIVED > 0 |
| JUSTICE__XC_MAPPING_POLICE_VIOLENCE | probed | 15,476 killings, officers charged in 267 (1.7%); Phoenix 185 deaths, 0 charges |
| JUSTICE__XC_WAPO_FATAL_FORCE | probed | **MENTAL_ILLNESS_RELATED and BODY_CAMERA_PRESENT are 'false' on all 10,430 rows** |
| ECONOMICS__FED_SBA_LOANS | probed | **LENDER_NAME blank on all 1.95M 7A loans**; 2007 vintage charged off 29.3% |
| JUSTICE__FED_FJC_ARTICLE_III_JUDGES | probed | 4,074 judges; confirmed judges only, so committee outcomes can't show who was blocked |
| POLITICS__FED_FJC_JUDGES | skip | older snapshot: all 4,067 of its judges (by NID) are in the 4,074 |
| HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | probed | **GROSS_INCOME is '0' or blank on all 26.25M rows**; Katrina LA $4.35B vs Irma FL $1.15B |
| JUSTICE__INTL_HUDOC | probed | every judgment stored twice (English + French); **JUDGMENT_DATE blank** on the top 10 document types |
| POLITICS__MEMBER_INDIV_DONATIONS | probed | earmarked share median 58% (2024) to 64% (2026); self-funding counts gifts only, not loans |
| POLITICS__MEMBER_MONEY_RAISED | probed | top Gallego $129.3M (2024); net never above gross |
| CRIMINAL_JUSTICE__FED_BJS_DATA | dead | anonymous survey rows, max 15 incidents per person, no one to name |

---

## Top three (none are live; these are the closest)

### 1. FEC "DODO GOVERNMENT", $100M, type 19
- **Checked:** the biggest non-memo rows in FINANCE__FED_FEC_INDIV_CONTRIBUTIONS.
- **What showed up:** Soros $125M and Bloomberg's own money are known. One row isn't: donor "DODO GOVERNMENT", entity ORG, $100,000,000, type 19 (a gift to an electioneering-communication filer), committee C30003578, dated 2025-10-25.
- **A hit means:** a $100M gift behind issue ads, with no one named behind it.
- **A miss means:** a junk or test filing that the FEC keeps in its bulk data.
- **Boring reason:** most likely a filer typo or a joke filing. The name alone says so. Pull the image of the original filing before anything else.

### 2. SBA 7A: the 2007 loans
- **Checked:** charge-off share by approval year, counting every funded loan (cancelled loans left out).
- **Numbers:** 2007 loans: 29.3% charged off, 24.4% of the dollars. 2006: 25.5%. 2010-2018: 5-7%.
- **A hit means:** the pre-crisis book was badly underwritten, and the table can say whose loans they were.
- **A miss means:** this is the 2008 recession, already written up many times.
- **Boring reason:** the recession. And the lender can't be checked, because LENDER_NAME is blank on every 7A loan.
- **A mistake I fixed:** counting closed loans only first made 2022-23 look like 13-16%. On all funded loans it's 3.3% and 2.2%. Fast failures close first, so a young year looks worse than it is.

### 3. FRA crossings: fewer crashes, deadlier ones
- **Checked:** crashes and deaths per decade in TRANSPORT__FED_FRA_CROSSING_INCIDENTS.
- **Numbers:** 76,105 crashes in the 1980s, 13,866 in the 2020s. Deaths per crash: 7.6% in the 1970s, 13.0% in the 2020s.
- **A hit means:** crossings got safer for cars, and the deaths that remain are on foot.
- **A miss means:** a change in what counts as reportable.
- **Boring reason:** gates and signals cut the car crashes, so pedestrians and trespassers, who die more often, are a bigger share of what's left. Next check: split by HIGHWAY_USER.

---

## New data traps: columns that look real and aren't

1. **NPDB: the mart TOTAL_PAYMENT is 100% null** (1.91M rows). The landing table has `PAYMENT` and `TOTALPMT` as `'$57500'` strings. The mart's number conversion lost every one of them. The public file also reports payments as the midpoint of a dollar band, so apparent bunching near round numbers is really the bands.
2. **WaPo fatal force: MENTAL_ILLNESS_RELATED and BODY_CAMERA_PRESENT are 'false' on every row.** A broken load, not a finding.
3. **FEMA IA: GROSS_INCOME is '0' (6.34M rows) or blank (19.9M rows).** It is the row's lead number, and it never holds a real income.
4. **SBA: LENDER_NAME is blank on every 7A loan.** Also: PROGRAM is `' 7A'` with a leading space, and IS_DEFAULTED is null on the 12,154 charged-off 504 loans.
5. **HUDOC: JUDGMENT_DATE is blank** on the ten biggest document types. Every judgment is also stored twice, once in English and once in French.
6. **Money columns that hit a ceiling** (numbers stop at a maximum, so totals are floors):
   - USAspending assistance: $9,999,999,999 on Medicare/Medicaid rows, 2012-2016
   - FJC criminal: FINE_AMOUNT_1 stops at $99,999,999
   - FJC civil: money is in $ thousands, and 9999 means $10M or more
   - FRA crossings: VEHICLE_DAMAGE_COST stops at $1,000,000
7. **FRA equipment accidents:** TOTAL_DAMAGE_COST repeats in full on every railroad's row. Remove duplicates on INCIDENT_KEY before adding up.
8. **A memory note is out of date:** `trap-usaspending-assistance-1m-per-year-cap` says 1M rows a year. The table now holds 128.2M rows, with all 12 months of every fiscal year. CONTRACTS_FULL still has the cap.

Two copies to retire: HMDA_DC_ONLY (same rows as HMDA) and POLITICS FJC_JUDGES (older copy of the Article III table).
