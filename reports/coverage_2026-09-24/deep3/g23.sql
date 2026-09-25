-- deep3 / g23: proper look at five glance-only tables, 2026-09-24
-- Tables: POLITICS__XC_JCS_COA, POLITICS__XC_JCS_SCOTUS, POLITICS__JCS_MEDIANS,
--         POLITICS__XC_JCS_MEDIANS, POLITICS__SCOTUS_JUSTICE
-- Door: Python (connect/db.py) via g23/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g23/<label>.json.
-- The five tables are tiny (40 to ~4,700 rows), so each is pulled whole once and analysed locally
-- in g23/analyze.py; no statement cost for the local checks.

-- [q01] statement 1
-- Pull the whole appeals-judge score table, plus a row count and distinct row-number count
select t.*, count(*) over () n_rows, count(distinct UNNAMED_0) over () n_rownum
from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_COA t;

-- [q02] statement 2
-- Pull the whole Supreme Court justice-by-term score table
select t.*, count(*) over () n_rows, count(distinct UNNAMED_0) over () n_rownum
from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_SCOTUS t;

-- [q03] statement 3
-- Pull the whole medians mart (typed)
select * from LIBRARY_MARTS.POLITICS.POLITICS__JCS_MEDIANS order by YEAR;

-- [q04] statement 4
-- Pull the whole raw medians table (text), with circuit medians
select t.*, count(*) over () n_rows from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_MEDIANS t;

-- [q05] statement 5
-- Pull the 40-row justice table
select * from LIBRARY_MARTS.POLITICS.POLITICS__SCOTUS_JUSTICE order by FIRST_TERM, JUSTICE_CODE;

-- [q06] statement 6
-- SCDB: per-justice vote counts, to check SCOTUS_JUSTICE.N_VOTES / N_CASES and the last term loaded
select JUSTICE_CODE, JUSTICE_NAME, min(TERM) first_term, max(TERM) last_term, count(*) n_rows,
  count(distinct VOTE_ID) n_vote_id, count(distinct CASE_ID) n_case, count(distinct DOCKET_ID) n_docket,
  count(distinct _SOURCE_RUN_ID) n_runs
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
group by 1,2 order by first_term, 1;

-- [q07] statement 7
-- The typed SCOTUS ideology mart, to compare with the raw XC table
select * from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_SCOTUS;

-- [q08] statement 8
-- The typed appeals ideology mart, to compare with the raw XC table (703 vs 705)
select * from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA;

-- [q09] statement 9
-- FJC appointments to the courts of appeals: who appointed each judge, party, dates.
-- Used to (a) test whether an appeals JCS score is just the appointer's score, (b) see how far the JCS list reaches in time.
select NID, SEQUENCE, JUDGE_NAME, COURT_TYPE, COURT_NAME, APPOINTING_PRESIDENT, PARTY_OF_APPOINTING_PRESIDENT,
  COMMISSION_DATE, TERMINATION_DATE
from LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT
where COURT_TYPE ilike '%appeals%';

-- [q10] statement 10
-- SCDB: Supreme Court cases by term x the court the case came from x outcome, one count per case.
-- Used to join circuit ideology (XC_JCS_MEDIANS) to how often the Court overturned each circuit.
select TERM, CASE_SOURCE_CODE, DECISION_TYPE_CODE, PARTY_WINNING, CASE_DISPOSITION_CODE,
  LC_DISPOSITION_DIRECTION_CODE, DECISION_DIRECTION_CODE,
  count(distinct CASE_ID) n_cases, count(distinct iff(MIN_VOTES = 0, CASE_ID, null)) n_unanimous,
  count(*) n_rows
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
group by 1,2,3,4,5,6,7;

-- [q11] statement 11
-- SCDB: the 5th Circuit's argued cases, terms 2015-2024, one row per case, for eyeballing and to see who petitioned
select distinct TERM, CASE_ID, CASE_NAME, DECISION_TYPE_CODE, PETITIONER_CODE, RESPONDENT_CODE, PARTY_WINNING,
  CASE_DISPOSITION_CODE, LC_DISPOSITION_DIRECTION_CODE, DECISION_DIRECTION_CODE, MAJ_VOTES, MIN_VOTES
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
where CASE_SOURCE_CODE = 25 and TERM >= 2015 and DECISION_TYPE_CODE in (1,6,7)
order by TERM, CASE_ID;

-- [q12] statement 12
-- FJC appeals database: distinct appeals per circuit per judgment year (a docket repeats across yearly snapshots,
-- so count distinct circuit+docket+reopen). Denominator for "Supreme Court cases per 1,000 appeals decided".
select CIRCUIT, year(try_to_date(JUDGMENT_DATE::string)) jy,
  count(distinct CIRCUIT||'|'||DOCKET||'|'||REOPEN) n_appeals, count(*) n_rows,
  count(distinct TAPE_YEAR) n_snapshots, min(TAPE_YEAR) min_tape, max(TAPE_YEAR) max_tape
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1,2;

-- [q13] statement 13
-- SCDB: argued cases by source court and term, split by whether a federal party petitioned
-- (petitioner code 1 = U.S. attorney general, 27 = United States, 300-499 = federal departments and agencies)
select TERM, CASE_SOURCE_CODE,
  iff(PETITIONER_CODE in (1, 27) or PETITIONER_CODE between 300 and 499, 'fed', 'other') pet,
  PARTY_WINNING, count(distinct CASE_ID) n_cases,
  listagg(distinct iff(TERM >= 2021 and CASE_SOURCE_CODE = 25, CASE_NAME, null), ' | ') names_5th
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
where DECISION_TYPE_CODE in (1,6,7) and TERM >= 2005
group by 1,2,3,4;
