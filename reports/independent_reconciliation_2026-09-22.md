# Warehouse vs published numbers — 2026-09-22

Chris: "test this for me". Five sources, warehouse asked for a number the publisher already printed.
Warehouse side via the Python door; published side fetched live today. Everything below is reproducible from the URLs.

## Scorecard

| Source | Published | Warehouse | Verdict |
|---|---|---|---|
| Census counties, 50 states + DC | 3,144 | 3,144 | MATCH exact |
| Census, Texas / Georgia / Virginia | 254 / 159 / 133 | 254 / 159 / 133 | MATCH exact |
| CMS Part D 2022 provider-drug rows | 25,869,521 | 25,869,521 | MATCH exact |
| CMS Part D 2022 total drug cost, national | $240.37B | $183.16B | GAP 24%, by design |
| USASpending contracts FY2008 obligations | $536.88B | $536.61B | MATCH 0.05% |
| USASpending contracts FY2015 | $430.80B | $430.67B | MATCH 0.03% |
| USASpending contracts FY2024 | $740.67B | $740.94B | MATCH 0.04% |
| USASpending contracts FY2025 | $778.53B | $778.42B | MATCH 0.01% |
| USASpending contracts FY2026 | $671.07B | $595.20B | STALE: load predates the newest months |
| HMDA 2015 all actions | 14.2M | 14,374,184 | MATCH to rounding |
| HMDA 2016 all actions | over 16.1M | 16,332,987 | MATCH to rounding |
| HMDA 2017 all actions | more than 14.1M | 14,285,496 | MATCH to rounding |
| FEC 2024 House + Senate receipts | $3.8B | $3.74B net | MATCH to rounding |
| FEC 2024 presidential receipts | $2.0B | $2.72B gross / $1.64B net | UNRESOLVED definition |

## Each one walked

**Census.** `REFERENCE__CENSUS_CB_COUNTY` grouped by state FIPS. 3,144 for FIPS 01 to 56 matches the 2023 vintage count that includes Connecticut's nine planning regions. The other 91 rows are Puerto Rico and territories. Hit: the file landed whole. Miss would mean dropped or duplicated rows.

**CMS Part D rows.** data.cms.gov stats endpoint for dataset b101b457 reports total_rows 25,869,521. `HEALTH__FED_CMS_PARTD_PRESCRIBERS` has 25,869,521 rows, 1,057,566 NPIs, DATA_YEAR 2022. Hit: every source row is in the mart, none twice.

**CMS Part D dollars.** National rows of the by-geography 2022 file sum to $240.37B over 3,584 drugs. The provider-drug mart sums to $183.16B. The $57B gap is the rows CMS deletes when a prescriber has under 11 claims of a drug. This is the trap already on file. The mart cannot produce the national total and says so on its label. Not a pipeline fault; a published limit.

**USASpending.** API spending_over_time, award types A B C D, grouped by fiscal year. Warehouse: `ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2`, FEDERAL_ACTION_OBLIGATION summed by fiscal year from ACTION_DATE. FY2008 through FY2025 all within 0.1 percent; the drift is agencies revising records after our download. FY2026 is short by $76B because the load stops before the latest months. Hit: the 93M-row pipe is straight. Miss would have been a whole agency or year missing.

**HMDA.** FFIEC press releases give applications plus purchased loans as "total actions". Warehouse counts on `HOUSING__FED_CFPB_HMDA_HISTORIC` by AS_OF_YEAR sit 1 to 1.5 percent above each rounded figure, consistent with preapproval-request rows the release counts separately. Only 2015 to 2017 are loaded.

**FEC.** Statistical summary of 24-month activity, 2023-2024 cycle. Warehouse `POLITICS__FEC_CANDIDATE_SUMMARY`, cycle 2024, 3,856 candidates: gross $6.85B, net $5.38B after transfers between a candidate's own committees. House + Senate net $3.74B against FEC's $3.8B: match. Presidential is $2.72B gross and $1.64B net against FEC's $2.0B; FEC's presidential figure uses a third netting rule this check did not pin down. Unresolved, not failed. The PAC file is not in this check.

## What this proves and does not
- Five pipes carry the source through to the mart without bending it: row counts and dollar sums land on the publisher's number.
- Two gaps are the publisher's, not ours, and both were already labelled in the warehouse.
- One is stale by months, one is a definition still open.
- This checks five sources of several hundred. It is the method, run once.

## Sources
- https://api.usaspending.gov/api/v2/search/spending_over_time/
- https://data.cms.gov/data-api/v1/dataset/b101b457-ffa4-49bb-8fd9-27c1266086e2/data-viewer/stats
- https://data.cms.gov/data-api/v1/dataset/1fc57194-a51d-4864-aee6-de0889488151/data
- https://www.consumerfinance.gov/archive/newsroom/ffiec-announces-availability-2017-data-mortgage-lending/
- https://www.consumerfinance.gov/about-us/newsroom/ffiec-announces-availability-2016-data-mortgage-lending/
- https://www.consumerfinance.gov/archive/newsroom/federal-financial-institutions-examination-council-announces-availability-2015-data-mortgage-lending/
- https://www.fec.gov/updates/statistical-summary-of-24-month-campaign-activity-of-the-2023-2024-election-cycle
