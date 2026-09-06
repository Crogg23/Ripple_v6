# 91 Trades, then a bill
- Checked: POLITICS__SENATE_TRADES (8,350 trades, last one 2020-12-02) against FED_GOVINFO_BILLSTATUS (36,465 bills, 118th-119th Congress, introduced 2023-01-03..2026-06-26) and FED_GOVINFO_BILL_COSPONSORS (367,742 rows, 2023-01-09..2026-06-25), on BIOGUIDE, bill introduced or cosponsored 0-90 days after the trade.
- First number: 0 trade→sponsor pairs and 0 trade→cosponsor pairs inside 90 days. The gap between the last trade and the first bill is 762 days; no window can bridge it.
- 43 of 57 trading senators do sponsor bills in 2023-26, so the people join works; the dates never touch.
- Hit would mean: buy, then legislate that sector within a quarter. Miss means what it means here: the two tables cover different years.
- Also missing: BILLSTATUS has no subject or policy-area column (checked information_schema), only TITLE; the "bill in that SIC" leg would be a title-text match even with overlapping years. House side (FD_PTR_INDEX) carries no tickers at all.
- Nearest substitute: none landed. Needs senate trades 2023+ (efdsearch) or bills 2012-2020 (govinfo 112th-116th). Do not build tonight.
- Cost: 5 queries (plus the shared discovery logged under 78); longest 11.8s (information_schema scan).
STATUS: dead
HEADLINE: 0 trades within 90 days of a bill — trades end 2020-12, bills start 2023-01, a 762-day hole with no substitute landed.
