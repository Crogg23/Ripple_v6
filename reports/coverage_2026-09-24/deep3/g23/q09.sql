-- FJC appointments to the courts of appeals: who appointed each judge, party, dates.
-- Used to (a) test whether an appeals JCS score is just the appointer's score, (b) see how far the JCS list reaches in time.
select NID, SEQUENCE, JUDGE_NAME, COURT_TYPE, COURT_NAME, APPOINTING_PRESIDENT, PARTY_OF_APPOINTING_PRESIDENT,
  COMMISSION_DATE, TERMINATION_DATE
from LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT
where COURT_TYPE ilike '%appeals%'
