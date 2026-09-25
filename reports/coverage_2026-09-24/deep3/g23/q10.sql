-- SCDB: Supreme Court cases by term x the court the case came from x outcome, one count per case.
-- Used to join circuit ideology (XC_JCS_MEDIANS) to how often the Court overturned each circuit.
select TERM, CASE_SOURCE_CODE, DECISION_TYPE_CODE, PARTY_WINNING, CASE_DISPOSITION_CODE,
  LC_DISPOSITION_DIRECTION_CODE, DECISION_DIRECTION_CODE,
  count(distinct CASE_ID) n_cases, count(distinct iff(MIN_VOTES = 0, CASE_ID, null)) n_unanimous,
  count(*) n_rows
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
group by 1,2,3,4,5,6,7
