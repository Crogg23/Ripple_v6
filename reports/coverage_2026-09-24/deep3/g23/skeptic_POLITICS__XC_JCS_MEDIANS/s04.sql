-- FJC appeals: what is TAPE_YEAR 2099? rows, judgment-date spread, overlap with real tapes
with t as (select CIRCUIT, DOCKET, REOPEN, TAPE_YEAR, try_to_date(JUDGMENT_DATE::string) jd from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE),
k99 as (select distinct CIRCUIT, DOCKET, REOPEN from t where TAPE_YEAR::string = '2099'),
kreal as (select distinct CIRCUIT, DOCKET, REOPEN from t where TAPE_YEAR::string <> '2099')
select TAPE_YEAR::string tape, count(*) n_rows, count(jd) n_with_jd, min(jd) min_jd, max(jd) max_jd,
  (select count(*) from k99) n_keys_99,
  (select count(*) from k99 join kreal using (CIRCUIT, DOCKET, REOPEN)) n_keys_99_also_in_real
from t group by 1 order by 1
