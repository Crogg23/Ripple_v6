# Sweep 2026-09-24: sweep2-d

25 rows: 15 place, 5 names, 5 time. All 25 are marked.
**0 live · 16 probed · 4 dead · 5 skip.**
Statements: **34 of 120.** All were read-only SELECT or WITH, plus the allowed `ALTER SESSION` timeout once per connection.
Two statements failed. Statement 6 (an R2 `LIMIT 5` with a `COUNT(*)` subquery) hit the 300-second timeout. Statement 33 had a reserved-word alias and was rerun as statement 34.
Queries are in `sweep2-d.sql`.

**Reused data.** The contracts and assistance county pairs reuse sweep-d's county extracts from the shared scratchpad: `d_contracts_pc.csv`, `d_assist_pc.csv`, `d_cdc_drug.csv` and `d_dim.csv`. They were joined locally, so those pairs cost no new statements.
Money is rolled up to the place-of-performance county and divided by `DIM_COUNTY.POPULATION_2020`. Only counties with 10,000+ people are counted.

## Every row

| id | status | the number that mattered |
|---|---|---|
| G2 assistance ~ HPSA primary care | probed | Spearman 0.22. Share of counties scoring 18+: 9% in the lowest money decile, 22% in the highest. Coahoma MS and McDowell WV are high on both |
| G2 contracts ~ CDC drug poisoning | dead | Spearman 0.06. The CDC file ends in 2015 and holds bands only |
| G2 contracts ~ HPSA primary care | dead | Spearman −0.005. The median score is 14 in every money decile |
| G2 CDC drug poisoning ~ BULK | skip | BULK is a 50k-row, 10-day sample |
| G2 CDC injury ~ BULK | skip | same |
| G2 HPSA primary care ~ BULK | skip | same |
| G2 HRSA shortage ~ BULK | skip | same |
| G:JUSTICE__XC_MAPPING_POLICE_VIOLENCE | probed | Killings per million people per year: NM 10.7, RI 0.7. MA fell from 1.4 to 0.6; ID rose from 2.9 to 5.9 |
| G2 assistance ~ county double burden | probed | Spearman 0.25. Buchanan, Wise and Tazewell VA, plus Harlan and Pike KY, are in the top money decile and have a >30 overdose band |
| G2 contracts ~ county double burden | dead | Spearman 0.06. The double-burden share is flat across money deciles |
| G2 double burden ~ BULK | skip | BULK sample |
| G:ECONOMICS__FED_SBA_LOANS | probed | Approved $ per resident: UT $4.2k, WV $872. 7A charge-offs: WV 5.5%, MT 2.4% |
| G:FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | probed | Lincoln SD holds $8.2M of deposits per resident (Citibank's booking office). Oglala Lakota SD has 13.7k people and 0 branches |
| G2 assistance ~ DEA ARCOS | probed | Spearman 0.32. Mingo WV: 232 pills per person per year |
| G:ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | probed | ZIP 76108 (Lockheed, Fort Worth) got $316B. The top 100 ZIPs hold 46% of all contract $ |
| N:ECONOMICS__FED_SBA_LOANS | probed | Charged off: Matco Tools 31%, Cold Stone 21%, Dunkin 4%. The IRS BMF name bridge is 0.01% |
| N:ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | probed | 29.9M rows say REDACTED DUE TO PII. 99.99% of UEIs carry one name |
| N:JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | probed | CERT_NUMBER is filled on 98% of rows. 87% of those certs land in SOD, and the names agree 98.9% |
| N:JUSTICE__XC_WAPO_FATAL_FORCE | probed | MPV carries a WAPO_ID: 10,348 of 10,430 land, and the date agrees 95.7%. At least 3 people are in the table twice |
| N:JUSTICE__FED_FJC_ARTICLE_III_JUDGES | probed | CourtListener's FJC_ID matches FJC's JID: 3,710 of 4,074 land, and birth year agrees 99.8% |
| T:JUSTICE__FED_COURTLISTENER_DOCKETS | probed | 13% of rows have no filing date. The spikes are mass-tort cases: N.D. Fla 2020 has 230k filings, 57x its median |
| T:JUSTICE__FED_COURTLISTENER_POSITIONS | probed | Committee vote to confirmation: 1 day before 1980, 88 days in the 2010s. The feed stops after 2019 |
| T:HEALTH__FED_CMS_NURSING_HOME_PENALTIES | probed | Illinois cut off payment at 43.6% of its homes vs 12.9% nationally. 46.5% of homes cut off got another penalty later |
| T:JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | probed | Two years after a bank's first cease-and-desist order, its deposits were 0.93x their prior level (national 1.18x). 26% of those banks had left SOD |
| T:JUSTICE__XC_WAPO_FATAL_FORCE | dead | Shootings rose from 995 (2015) to 1,175 (2024). The only names are victims, so there's no money trail |

## Top three rows, walked (none reached live)

### 1. Nursing-home payment cutoffs by state and chain (T:HEALTH__FED_CMS_NURSING_HOME_PENALTIES)
- **Checked:** all 16,180 penalty rows, joined on CCN to the 14,700-home provider table. Every CCN joined. I measured which homes got a payment cutoff, what happened after the first one, and the current star rating.
- **Number:** 1,898 homes got a payment cutoff between 2023-06 and 2026-05. 46.5% of them were penalized again after it, and 49% are 1-star now (7% of homes with no penalty). Illinois cut off 43.6% of its homes; the national rate is 12.9%, and Idaho and South Dakota are at 0%. Adjusted for state, Cascades Healthcare had 9 of 20 homes cut off against 2.0 expected. Arcadia Care's raw rate is 16 of 22 (73%), but that's mostly Illinois.
- **Hit means:** where a home sits decides whether Medicare ever stops paying it. A few chains draw cutoffs at 3-4x their states' rates.
- **Miss means:** the gap is survey-agency habit, not how bad the homes are.
- **Boring explanation:** state survey agencies recommend remedies differently. The table covers only three years.

### 2. FDIC enforcement to bank deposits (T and N:JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS)
- **Checked:** `CERT_NUMBER` joined to SOD `FDIC_CERT`. For each bank, I took its first cease-and-desist order from 1995 to 2022 and compared its deposits the year before with its deposits two years after.
- **Number:** 1,305 banks. Median deposits after two years were 0.93x the starting level, against 1.18x nationally. 64% shrank and 26% had left SOD. For orders from 2008-12, the median was 0.90x.
- **Hit means:** banks under an order shrink or disappear, and the join is clean enough to follow individual banks.
- **Miss means:** there's no "kept growing after the order" story.
- **Boring explanation:** cease-and-desist orders land on banks that are already sick.

### 3. Pills vs federal assistance (G2 assistance ~ DEA ARCOS)
- **Checked:** ARCOS sales rows 2006-12 per buyer county, divided by population, against assistance $ per person. That's 2,451 counties.
- **Number:** Spearman 0.32. Pills per person per year rise from 20 in the lowest money decile to 40-44 in the top decile. Mingo WV is at 232 (the Strosnider pharmacy in Kermit), with Logan WV and Floyd and Pike KY close behind.
- **Hit means:** pill-flooded counties also run on federal transfers.
- **Miss means:** nothing links the two beyond poverty.
- **Boring explanation:** Appalachian poverty and disability drive both. The years don't line up either: assistance covers 2007-26, ARCOS covers 2006-12.

## New data traps

1. **VA mail-order pharmacies (CMOP) sit in ARCOS as retail buyers.** The one in North Charleston SC bought 512M dosage units, and Leavenworth KS bought 105M. That puts Charleston at 209 pills per person per year and Leavenworth at 206. Drop CMOP buyers before any per-county rate.
2. **ARCOS has 5 junk rows:** `TRANSACTION_CODE` is '9143' or '9193' and `BUYER_COUNTY_FIPS` is null. Three of them hold 2.14B dosage units. Filter to `TRANSACTION_CODE='S'`.
3. **SOD `BRANCH_STATE_COUNTY_FIPS` lost its leading zero** on 9,820 county-years in states 01-09 (CA, AL, AR, CO, CT...). Unpadded, Los Angeles shows zero branches. Use `LPAD(...,5,'0')`.
4. **SBA `BORROWER_ZIP` lost its leading zeros** on about 245k loans: MA, NJ, CT, NH, RI, ME and VT are 4 digits, and PR is 3. Same shape as the ATF ZIP trap.
5. **FDIC `CMP_AMOUNT_TOTAL` repeats within a docket.** CBW Bank's $20.4M (2024) and $20.5M (2025) are one penalty (FDIC-22-0171k). 37 dockets repeat the same amount. 23 orders carry cert '0'.
6. **County double burden: `JAIL_RATE_YEAR` runs from 1970 to 2024** (14 counties are stuck at 1978). `BLACK_JAIL_RATE` goes as high as 160,000 per 100k. The overdose band is CDC's 16-band scale.
7. **HRSA HPSA primary care: 70% of the 79k rows are Withdrawn or Proposed for Withdrawal.** Filter to `HPSA_STATUS='Designated'`.
8. **The FJC→CourtListener key is JID, not NID.** For judges appointed 2019-26, JID just copies NID, and CourtListener has no FJC_ID for 363 of them.
9. **WaPo fatal force double-counts at least 3 people:** same date and age, different city (Kelly G. Abbott WI, Thomas Phan CA, Eduardo Munoz TX).
10. **MPV `NATIVE_AMERICAN_PERCENT...` is a 0-1 fraction for the census tract**, not a ZIP percentage.
11. **CourtListener financial disclosures: `YEAR_COL` runs from 0 to 14423.**

## Housekeeping
- My scratch files are all prefixed `sweep2-d_`. I only read sweep-d's `d_*` files.
- Statement 6 burned 300 seconds of warehouse time on R2. A bare `LIMIT 5` with a `COUNT(*)` subquery on R2 doesn't return; a plain GROUP BY finished in 167 seconds.
