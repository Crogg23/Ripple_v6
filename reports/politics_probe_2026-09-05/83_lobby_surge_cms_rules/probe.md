# 83 Lobby surge around the rule that sets the fine
- Checked: EDUCATION__FED_SENATE_LDA_FILINGS (819,649 rows, FILING_UUID unique; landing 831,376) by FILING_YEAR; client-name pull for AHCA, LeadingAge, hospice, dialysis, homecare; REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS (94,731) CMS docs by year.
- First number: LDA covers 1999-2010 and 2020-2021 only (2011-2019 missing, 14 years of 24 in a 1.94M-filing registry). Federal Register runs 2023-01-03 to 2026-06-16. Shared years between the two legs: zero.
- Trade groups do exist in LDA: American Health Care Association 158 filings ($5.7M income / $23.0M expenses), Fresenius 194, DaVita 94+58, Kidney Care Council 99, Hospice Action Network 75, AAHomecare 70+56. Names split on spelling (DAVITA INC / DAVITA, INC.; FKA suffixes).
- CMS Federal Register docs: 268 (2023), 317 (2024), 211 (2025), 125 (2026 to June), about two-thirds with a COMMENTS_CLOSE_ON date.
- A hit would be quarterly lobby spend rising into a CMS comment window. A miss here is structural: no quarter in the lobby file overlaps any rule in the register file.
- Trap hit: LDA sits in EDUCATION and its year coverage is two islands; INCOME/EXPENSES are TEXT and mutually exclusive by filer type (registrant income vs in-house expenses), never sum them together.
- Nearest substitute: none landed for 2022-2026 LDA; the leg needs the Senate LDA API years 2022+.
STATUS: dead
HEADLINE: 0 overlapping years: lobby filings stop at 2021, CMS rules start 2023-01-03; AHCA's 158 LDA filings can't be lined up with any of the 921 CMS docs.
