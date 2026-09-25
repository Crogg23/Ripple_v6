-- FJC appeals: judgment-date cast health per circuit, and an independent 5th-circuit recount by judgment year
select CIRCUIT, count(*) n_rows, count(JUDGMENT_DATE) n_jd, 
  sum(iff(JUDGMENT_DATE is not null and try_to_date(JUDGMENT_DATE::string) is null,1,0)) n_castfail,
  min(JUDGMENT_DATE::string) mn_raw, max(JUDGMENT_DATE::string) mx_raw, any_value(JUDGMENT_DATE::string) sample_raw,
  count(distinct iff(year(try_to_date(JUDGMENT_DATE::string)) between 2015 and 2017, DOCKET||'|'||REOPEN, null)) n_1517,
  count(distinct iff(year(try_to_date(JUDGMENT_DATE::string)) between 2021 and 2023, DOCKET||'|'||REOPEN, null)) n_2123,
  count(distinct iff(year(try_to_date(JUDGMENT_DATE::string)) between 2015 and 2017, DOCKET, null)) n_1517_docketonly,
  count(distinct iff(year(try_to_date(JUDGMENT_DATE::string)) between 2021 and 2023, DOCKET, null)) n_2123_docketonly,
  min(TAPE_YEAR) min_tape, max(TAPE_YEAR) max_tape
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1 order by 1
