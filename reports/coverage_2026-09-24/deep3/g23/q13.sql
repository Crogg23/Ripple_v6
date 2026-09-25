-- SCDB: argued cases by source court and term, split by whether a federal party petitioned
-- (petitioner code 1 = U.S. attorney general, 27 = United States, 300-499 = federal departments and agencies)
select TERM, CASE_SOURCE_CODE,
  iff(PETITIONER_CODE in (1, 27) or PETITIONER_CODE between 300 and 499, 'fed', 'other') pet,
  PARTY_WINNING, count(distinct CASE_ID) n_cases,
  listagg(distinct iff(TERM >= 2021 and CASE_SOURCE_CODE = 25, CASE_NAME, null), ' | ') names_5th
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
where DECISION_TYPE_CODE in (1,6,7) and TERM >= 2005
group by 1,2,3,4
