# Sweep 2026-09-24: sweep-d

25 rows: 15 place, 5 names, 5 time. All 25 are marked.
**2 live · 13 probed · 5 dead · 5 skip.**
Statements: **49 of 120** (read-only SELECT/WITH), plus the allowed `ALTER SESSION` timeout once per connection.
Queries are in `sweep-d.sql`. County work was aggregated in the warehouse, and the county rows were joined locally against `CORE.DIM_COUNTY.POPULATION_2020`.

## Every row

| id | status | the number that mattered |
|---|---|---|
| G:ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | probed | Brewster TX $459k per person (border wall). Table is 1M rows per FY over 43-120 days, so it's a sample |
| G:HOUSING__FED_CFPB_HMDA_HISTORIC | probed | Originated $/resident/yr: DC $13.5k vs PR $726. Denial rate PR 36%, MS 29% |
| G:PROCUREMENT__FED_USASPENDING_BULK | skip | 50k-row sample, 10 days |
| G:ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | probed | Cass ND $3.9M/person = Medicare-contractor "MULTIPLE RECIPIENTS" rows; 24% of $ has no county |
| G:HEALTH__FED_HRSA_NPDB | probed | NY $963/resident in malpractice paid vs AL $149. TOTAL_PAYMENT is 100% null |
| G:HOUSING__FED_CFPB_HMDA | skip | DC only, 2022 |
| G:HOUSING__FED_CFPB_HMDA_DC_ONLY | skip | DC only, 2022 |
| G:IMMIGRATION__FED_ICE_DETENTION_STINTS | **live** | Stays with a bond recorded: LA 4.1%, NM 3.7%, TX 5.0% vs PA 29.6%, VA 28.1% |
| G:HOUSING__FED_CFPB_HMDA_LAR | skip | DC only, 2023 sample |
| G:HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | probed | GROSS_INCOME is null or 0 on all 26.25M rows. Cameron Parish: 6,008 registrations vs 5,617 residents |
| G2 assistance ~ CDC injury | probed | Spearman 0.41; OD median 17.8 → 36.0 per 100k across money deciles (791 counties) |
| G2 assistance ~ HRSA shortage | probed | Spearman 0.27; Bethel and Nome AK high on both |
| G2 contracts ~ CDC injury | dead | Spearman −0.09 |
| G2 contracts ~ HRSA shortage | dead | Spearman −0.13 |
| G2 assistance ~ CDC drug poisoning | dead | CDC file ends 2015 and holds bands only; 0.25 |
| N:HOUSING__FED_CFPB_HMDA_HISTORIC | **live** | loanDepot denied 56.3% of 1.45M applications vs Wells 13.8%. Bridge hits 92.8% of rows |
| N:ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | probed | UEI→one name 99.998% (420,990 UEIs). Top names are drug distributors |
| N:TRANSPORT__FED_FRA_CROSSING_INCIDENTS | probed | Name bridge to FRA deaths table: 497/1,065 names, code agrees 99.6%, 98.4% of rows |
| N:JUSTICE__XC_MAPPING_POLICE_VIOLENCE | probed | 588 "Name withheld". Agency→grant recipient: 458 name hits, 214 state-agree (47%) |
| N:PROCUREMENT__FED_USASPENDING_BULK | skip | 50k sample of CONTRACTS_FULL |
| T:JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | probed | Table ends around 2021. Jun 2020 spike 58,687 filings = 3M earplug MDL (N.D. Fla) |
| T:IMMIGRATION__FED_ICE_DETENTION_STINTS | probed | Final orders 76k (2022) → 524k (2025). Top facility has 1 detainer row, so the partner doesn't bridge |
| T:TRANSPORT__FED_FRA_CROSSING_INCIDENTS | dead | Union Pacific got $0.95M in contracts over 12 FYs; there's no money trail |
| T:HEALTH__FED_CMS_NURSING_HOME | probed | Event date column 100% null; 263 homes last surveyed 2019-22 |
| T:JUSTICE__XC_MAPPING_POLICE_VIOLENCE | dead | 1,039-1,270 killings/yr, flat. Phoenix PD grants only FY07/FY09 |

## Top live rows, walked

### 1. ICE bond gap by state (G:IMMIGRATION__FED_ICE_DETENTION_STINTS)
- **Checked:** 2023-25 book-ins, rolled to the stay (`STAY_ID`), with the stay's state taken from its last stint. I measured the share of stays with any `INITIAL_BOND_SET_AMOUNT`.
- **Number:** NM 3.7%, LA 4.1% (213k stays), TX 5.0% (360k), AZ 6.1% vs FL 13.6%, CO 17.4%, VA 28.1%, PA 29.6%. That's a 7x gap. Median bond is $5k-$10k everywhere.
- **Hit means:** where you're held decides whether you ever see a bond.
- **Miss means:** the gap is who is held, not where.
- **Boring explanation (strong):** border states hold recent arrivals, and arriving aliens and expedited-removal cases can't get an immigration-judge bond. Also, bond-posted share is about 93% of bond-set share, so the field may only fill when bond is actually posted.
- **Next pass:** control for `CASE_CATEGORY` / `ENTRY_STATUS` / `ENTRY_DATE`, and compare interior arrests held in LA against the same kind held in PA.

### 2. loanDepot denial rate (N:HOUSING__FED_CFPB_HMDA_HISTORIC)
- **Checked:** top 20 lenders by rows, then bridged to `HMDA_ARID2017_LEI_XREF`. The key is `AGENCY_CODE || LTRIM(RESPONDENT_ID without '-', '0')`: 5,388 of 7,473 lenders and 41.8M of 45.0M rows. I eyeballed the top 10 names: Wells, Quicken, loanDepot, Chase, US Bank, Nationstar, BofA, Freedom, Caliber, Navy Federal. All correct.
- **Number:** loanDepot (HUD 26-4599244) has 1,451,218 applications 2015-17 with 56.3% denied. Compare Quicken 26.2%, Wells 13.8%, Chase 8.5%, Freedom 4.9%.
- **Hit means:** one of the biggest nonbank lenders turned away more than half its applicants. Next step: who got turned away (race, income, tract).
- **Miss means:** the denominator is the story, not the lender.
- **Boring explanation:** online lead-gen funnels take all comers, and banks carry purchased-loan rows (action 6) that shrink their rates. The rate here is denied / all rows. Re-run as denied / (originated + approved + denied) before trusting it.

### 3. No third live row
The next-strongest is assistance $ vs overdose (Spearman 0.41), but big-city Medicaid money explains it. Left it probed.

## New data traps

1. **NPDB dollars live in `PAYMENT_FLAG`, not `TOTAL_PAYMENT`.** `TOTAL_PAYMENT` is null on all 1,911,185 rows. `PAYMENT_FLAG` holds '$205000' text on P and M rows. The neighbouring columns look shifted (`PAYMENT_NUMBER` holds 'S'). This updates the "NPDB PAYMENT is a $ string" line in `trap-three-tables-not-what-they-look-like`.
2. **Assistance trap is stale.** `FED_USASPENDING_ASSISTANCE_FULL` now holds 128.2M rows with all 365 days in every FY 2007-26. The 1M-per-year cap in `trap-usaspending-assistance-1m-per-year-cap` no longer holds; the catalog summary already says "no row cap". **CONTRACTS_FULL is still capped:** exactly 1M per FY, 43-120 days each, mostly Jul-Sep.
3. **Assistance recipient county FIPS is a float with lost padding.** `PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE` reads '4243.0' (PA 42 + county 43) on 4-41% of FY2007-17 rows (0% from FY2018 on). Use place-of-performance county, which is clean 5-digit text.
4. **Nursing home `DATE_OF_MOST_RECENT_HEALTH_INSPECTION` is null on all 14,700 rows.** Use `RATING_CYCLE_1_STANDARD_SURVEY_HEALTH_DATE`, which is 100% filled, 2019-09 to 2026-04.
5. **FEMA IA `GROSS_INCOME` is empty:** null on 19.9M rows and '0' on 6.3M. No income in the table.
6. **FRA crossing `INCIDENT_YEAR` is 2-digit text** ('00'-'99'), so MIN/MAX lie. Use `DATE`.
7. **DIM_COUNTY uses Connecticut's 2022 planning regions (091xx).** USAspending's old CT county codes land nowhere, so CT ranks bottom on any per-person join.
8. **HMDA ARID key:** `ARID_2017` is agency + respondent id with leading zeros stripped. The naive concat hits 11.6% of lenders; the stripped one hits 72% of lenders and 92.8% of rows.

## Housekeeping
I overwrote another agent's scratchpad file `b1.sql`. The shared scratchpad already held one when I first wrote mine. My files now use a `d_` prefix. If a sibling agent's `b1.sql` went missing at 09:54, that was me.
