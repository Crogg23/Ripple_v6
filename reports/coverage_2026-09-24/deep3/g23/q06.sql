-- SCDB: per-justice vote counts, to check SCOTUS_JUSTICE.N_VOTES / N_CASES and the last term loaded
select JUSTICE_CODE, JUSTICE_NAME, min(TERM) first_term, max(TERM) last_term, count(*) n_rows,
  count(distinct VOTE_ID) n_vote_id, count(distinct CASE_ID) n_case, count(distinct DOCKET_ID) n_docket,
  count(distinct _SOURCE_RUN_ID) n_runs
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
group by 1,2 order by first_term, 1
