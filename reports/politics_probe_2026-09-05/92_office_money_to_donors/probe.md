# 92 Office money to donors

- Checked: member-office detail disbursements (subtotals out, try_to_number, AMOUNT > 0) with person-shaped payee names (2+ words, company words excluded) keyed LAST, FIRST; matched to FEC individual donors keyed the same way, restricted to the SAME member's own campaign committees (office → legislator on last name + first initial, 769/1,030 unique; → FEC_IDS → committee dim CAND_ID, 679 offices, 742 committees). No city on the disbursement side, so the tightener is "gave to this member's committee", not city.
- First number: 1,325 payee-donor pairs across 8 spend categories. 569 are salaried staff ($115.0M paid, $1.01M given). 756 sit in non-salary categories (travel, supplies, equipment: $2.57M paid, $1.43M given) — but 749 of those 756 payees ALSO appear on a House payroll; only 7 pairs (2 people, $41K paid, $9K given) never do.
- Eye check, 3 of 3 same person, 0 of 3 a vendor: Cole Rojewski / Valadao ($131K travel, chief of staff; later on Granger's payroll), William Harper / McCollum ($264K equipment+supplies+travel, chief of staff), Steven Pfrang / LaHood ($1.09M salary, $10.1K given). The "vendors" are staffers filing expense reimbursements under their own names.
- A hit would mean outside vendors paid from the allowance also fund the member. A miss (this) means the leg is staff giving to their boss — legal, common, a different story.
- Trap hit: FINANCE__FED_FEC_INDIV_CONTRIBUTIONS is 99.99% 2023-2026 (18.1M/40.1M/21.0M/5.0M rows by year; 12 stray rows 2000-2020, sentinels to 3312). Disbursements run 2015-2026, so 2016-2022 payments are being matched to donations years later.

STATUS: dead
HEADLINE: 1,325 payee-donor pairs, but 1,318 are House staffers (salary or expense reimbursement) giving to their own boss; only 2 people, $41K paid / $9K given, are not on any payroll.
