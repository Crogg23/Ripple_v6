# 77 Judges invested in the parties before them
- Checked: INVESTMENTS description (2-word company key) = EDGAR TITLE key -> FINANCIAL_DISCLOSURES (PERSON_ID, YEAR) -> DOCKETS where ASSIGNED_TO_ID is that judge, CASE_NAME carries the company, case open in the disclosure year. FJC/IDB route skipped: IDB FILEJUDG is blank on the five biggest districts; dockets already carry the CL judge id (32.4M rows, 3,350 judges).
- First number: **193 dockets, 79 judges, 99 judge-company pairs (2003-2020)** where the holding reads as stock (common/shares/ticker/& Co). Wide match is 2,865 dockets / 374 judges / 44 companies, but 2,662 of those are bare names like "Wells Fargo Bank Accounts" = deposit accounts, not stock. Wells Fargo is 94 of the 193; Exxon 20, Costco 16, Verizon 15, JPMorgan 12.
- Eye check: 11 of 12 stock-only sample rows real (holding "Wells Fargo common stock", case "DataMotion Texas v. Wells Fargo Bank"); the miss is a forfeiture case naming a Fifth Third account. Wide pass: LAS VEGAS (Sands vs Metro Police), GULF COAST, "1st Source Bank (CDs" were false, dropped.
- Hit means: a judge disclosed owning shares in a company while assigned a case naming it; 28 USC 455(b)(4) says any financial interest recuses. Miss means: the OCR description never named the company, or the disclosure YEAR did not parse.
- Traps: FINANCIAL_DISCLOSURES.YEAR is column-shifted text on 38,530 of 70,776 rows (only 32,246 parse 1990-2030), so every count here is a floor on 46% of disclosures; ID repeats (70,776 rows, 66,286 distinct). An INVESTMENT row saying "<bank> Accounts" is cash, not equity; a 2-word key catches places and fund families (Wells Fargo Advantage) unless filtered.
- Cost: 28 distinct queries, longest 57s, ~390s total.

STATUS: lit
HEADLINE: 79 federal judges disclosed stock in a company while assigned 193 cases naming it (2003-2020); the 2,865-docket wide number is 93% bank deposit accounts, not stock.
