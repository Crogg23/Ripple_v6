-- FJC appeals database: distinct appeals per circuit per judgment year (a docket repeats across yearly snapshots,
-- so count distinct circuit+docket+reopen). Denominator for "Supreme Court cases per 1,000 appeals decided".
select CIRCUIT, year(try_to_date(JUDGMENT_DATE::string)) jy,
  count(distinct CIRCUIT||'|'||DOCKET||'|'||REOPEN) n_appeals, count(*) n_rows,
  count(distinct TAPE_YEAR) n_snapshots, min(TAPE_YEAR) min_tape, max(TAPE_YEAR) max_tape
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1,2
