# 90 Appointee's old sector, agency's new awards
- Checked: GOVERNANCE__FED_REVOLVINGDOOR_PROJECT (406 rows, one run 2026-06-17) PERSON_NAME, AGENCY, INDUSTRY_SECTOR, appointee flags; landing FED_REVOLVINGDOOR_PROJECT columns; USAspending R2 columns (UPPERCASE, confirmed).
- First number: PERSON_NAME is 'nan' on 405 of 406 rows and '3' on the other one. Zero people. IS_POLITICAL_APPOINTEE and IS_REVOLVING_DOOR are false on all 406. The landing file has no name column at all (first column is 'H', then POSITION_TYPE, POSITION_NAME, SECTOR1..16); the mart's PERSON_NAME is a typed 'nan' string, not a redaction.
- What is there: 57 agencies (Treasury 42, Commerce 29, HHS 29 positions), 18 sectors (Real Estate 75, Agriculture/Big Food 73, Energy 37, Defense 33). It is a map of positions to the sectors that care about them, not a roster of who holds them.
- A hit would be an agency's NAICS mix tilting toward an appointee's prior sector after arrival. A miss: no person, no arrival date, so there is no "after". USAspending side untouched (no point scanning 93M rows without a date).
- Trap hit: mart columns PERSON_NAME/AGENCY/INDUSTRY_SECTOR read like a people table; the source is a position-interest matrix with 'nan' typed as text.
- Nearest substitute: Plum Book / OPM appointee lists are not landed; FED_HOUSE_FD_PTR_INDEX has names but no agency positions.
STATUS: dead
HEADLINE: 0 named appointees in 406 rows (PERSON_NAME = 'nan' on 405, '3' on one); the table is positions-by-sector, no person and no date to hang an award window on.
