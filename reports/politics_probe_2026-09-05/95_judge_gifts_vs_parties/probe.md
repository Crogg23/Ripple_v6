# 95 Gifts, debts and the parties before the bench
- Checked: DISCLOSURE_DEBTS.CREDITOR_NAME, _GIFTS.SOURCE, _REIMBURSEMENTS.SOURCE (multi-word names only, generic first words dropped) -> FINANCIAL_DISCLOSURES (PERSON_ID, YEAR) -> DOCKETS where ASSIGNED_TO_ID is the judge, normalized CASE_NAME carries the name, case open in that year. Dockets never pulled row-level; joined on judge id first.
- First number: **debts: 831 dockets, 150 judges, 64 creditors (2003-2020)** - a judge listing Wells Fargo (469 dockets), Chase (208), Huntington, PNC, SunTrust, Sallie Mae as a creditor while assigned suits naming them. Gifts: 8 dockets / 4 judges (one judge, Wells Fargo Bank as gift source, 4 cases). Reimbursements: 32 dockets / 21 judges, nearly all state bars (Florida Bar 11) and a university.
- Eye check: debts 8 of 8 real (creditor "Wells Fargo Bank, NA", case "Wells Fargo Bank v. Ahn", same judge, same year). Non-debt 10 of 12 real; misses are generic keys CREDIT UNION and COMMONWEALTH OF.
- Hit means: a judge owed money to, or was paid travel by, an entity that was a party in the judge's own courtroom that year. Miss means: the creditor is a card issuer never sued by name, or the OCR name broke.
- Traps: creditor names are OCR text - AMCRICAN EXPRESS 167 rows, UMION LEAGUE CHUB 20 - so exact-name keys undercount. Gift and reimbursement sources are bar associations, clubs and law schools (top 12 of each), not litigants; only the debts leg carries commercial parties. Same YEAR pollution as 77: 46% of disclosures have no parseable year. A mortgage with Wells Fargo is ordinary, not a recusal trigger by itself - the deep dive needs the DISPOSITION per hit.
- Cost: 13 distinct queries, longest 140s (the docket join), ~330s total.

STATUS: lit
HEADLINE: 150 federal judges listed a creditor on their disclosure while assigned 831 cases naming that creditor (2003-2020), Wells Fargo and Chase leading; gifts and reimbursements barely touch litigants (40 dockets).
