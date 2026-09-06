# Politics and markets probe, 2026-09-05

22 hunches, one first number each, read-only, Python door. lit = worth a deep dive, dim = runs but thin, dead = leg missing.

| status | count |
|---|---|
| dead | 6 |
| lit | 8 |
| dim | 8 |

## lit

**33. Nursing-home chain PAC money**
- 40 chains' staff gave $14.9M 2023–26; Saber's CEO alone $1.2M on 120 fines; only 5 true nursing-chain PACs exist and moved $166K.
- [probe](33_chain_pacs/probe.md)

**36. DME/nursing-home money to the committees that oversee CMS**
- 51% of nursing/health-chain PAC candidate money lands on CMS's four oversight committees vs 7.6% base rate (6.7x); chain staff 16% vs 10%.
- [probe](36_industry_to_overseers/probe.md)

**77. Judges invested in the parties before them**
- 79 federal judges disclosed stock in a company while assigned 193 cases naming it (2003-2020); the 2,865-docket wide number is 93% bank deposit accounts, not stock.
- [probe](77_judges_stock_vs_parties/probe.md)

**84. Independent expenditures aimed at the CMS overseers**
- $773M in independent expenditures hit the 126 current members of E&C, Ways & Means and Senate Finance 2018–2024, 73% of it against them, $594M on Senate Finance alone.
- [probe](84_ie_at_cms_overseers/probe.md)

**85. Device and pharma PACs into leadership PACs**
- 31 device/pharma corporate PACs put $8.07M into 358 leadership PACs in 2024–2026, Abbott first at $1.17M across 141 PACs, and the top five doctor-payers are still unmatched.
- [probe](85_maker_pacs_to_leadership_pacs/probe.md)

**87. Foreign agents giving at home**
- 681 registered FARA agents at 181 firms gave $25.8M to 1,378 federal committees while registered, employer-confirmed; name-only inflates that 9x.
- [probe](87_fara_agents_donating/probe.md)

**88. The same people run the 527 and the PAC**
- 1,758 people treasure both a 527 and an FEC committee at the same ZIP; 848 of them bridge two different organizations.
- [probe](88_shared_treasurers/probe.md)

**95. Gifts, debts and the parties before the bench**
- 150 federal judges listed a creditor on their disclosure while assigned 831 cases naming that creditor (2003-2020), Wells Fargo and Chase leading; gifts and reimbursements barely touch litigants (40 dockets).
- [probe](95_judge_gifts_vs_parties/probe.md)

## dim

**34. Earmarked district vs redlined zone**
- At state level (the only level possible), redlined-zone toxic density and member office spend are unrelated: Spearman 0.004 across 37 states, top vs bottom quartile $1.45M vs $1.42M.
- [probe](34_member_spend_vs_redlined/probe.md)

**35. Committee assignment vs stock trades**
- 153 current House committee members filed 1,739 trade reports since 2023 (Ways and Means: 21 members, 324 filings) — but the index says who filed, never what they bought.
- [probe](35_committee_vs_trades/probe.md)

**37. Sanctioned individuals in political money**
- 380 sanctioned-name keys match FEC donors ($4.0M) and 0 of the 3 verified are the sanctioned person; the leg runs, the number is noise.
- [probe](37_sanctioned_in_fec/probe.md)

**78. Senators trade the industry their committee marks up**
- 13 senators made 227 trades in 80 tickers inside their own committee's sector — but the trades are 2014-2020 and the roster is 2025, so the seat and the trade never line up in time.
- [probe](78_senators_trade_their_committee/probe.md)

**86. Ad money the FEC never saw**
- 956 six-figure Google political advertisers ($725M) have no FEC committee, but 10 of the top 15 are state races and ballot measures, so the federal "never saw" slice is unmeasured.
- [probe](86_google_ads_no_fec/probe.md)

**89. State dinners, federal checks**
- 9 Texas lobby filers are also self-described lobbyist donors in FEC, $89,080; loosen to exact name and it's 232 filers / $4.04M with about half surviving an eye check.
- [probe](89_state_gifts_federal_checks/probe.md)

**93. Rejected ballots and jail counties**
- top-decile rejection counties (3.8% of mail ballots) sit at 391 jailed per 100k vs 340 in the zero-rejection decile, but Black share goes 2.2% -> 7.8%; race moves, jail barely does, 1,632 counties, one EAVS vintage.
- [probe](93_rejected_ballots_jail/probe.md)

**94. Judges' politics and their dockets**
- Plaintiffs win 36.5% before Democratic-appointee-affiliated judges vs 36.7% before Republican across 1.44M decided civil cases; the donation leg is dead (0 pre-bench FEC rows, name matches are strangers).
- [probe](94_judge_politics_vs_dockets/probe.md)

## dead

**32. Excluded-entity donor overlap**
- 40 name hits, $647K, 0 of 3 verified real, 11 of 3,418 gifts same-state — LEIE org names do not reach FEC donors without an address bridge.
- [probe](32_excluded_donors/probe.md)

**82. Unions with a shortage and a PAC**
- 0 real shortage dollars in 617,710 OLMS filings; the 78 non-zero SHORTAGE_AMOUNT rows are column-shifted years, PAC flag alone is set on 41,766 filings.
- [probe](82_union_shortage_pac/probe.md)

**83. Lobby surge around the rule that sets the fine**
- 0 overlapping years: lobby filings stop at 2021, CMS rules start 2023-01-03; AHCA's 158 LDA filings can't be lined up with any of the 921 CMS docs.
- [probe](83_lobby_surge_cms_rules/probe.md)

**90. Appointee's old sector, agency's new awards**
- 0 named appointees in 406 rows (PERSON_NAME = 'nan' on 405, '3' on one); the table is positions-by-sector, no person and no date to hang an award window on.
- [probe](90_appointee_sector_awards/probe.md)

**91. Trades, then a bill**
- 0 trades within 90 days of a bill — trades end 2020-12, bills start 2023-01, a 762-day hole with no substitute landed.
- [probe](91_trade_then_bill/probe.md)

**92. Office money to donors**
- 1,325 payee-donor pairs, but 1,318 are House staffers (salary or expense reimbursement) giving to their own boss; only 2 people, $41K paid / $9K given, are not on any payroll.
- [probe](92_office_money_to_donors/probe.md)
