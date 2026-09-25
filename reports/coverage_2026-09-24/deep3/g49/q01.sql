-- FJC appeals: shape by yearly snapshot (TAPE_YEAR). Is one appeal one row, or repeated across snapshots?
select TAPE_YEAR, count(*) n_rows,
  count(distinct CIRCUIT||'|'||DOCKET||'|'||REOPEN) n_appeals,
  count(distinct APPEAL_RECORD_ID) n_recid,
  count(JUDGMENT_DATE) n_judgment,
  min(try_to_date(DOCKET_DATE::string)) min_dd, max(try_to_date(DOCKET_DATE::string)) max_dd,
  max(try_to_date(JUDGMENT_DATE::string)) max_jd,
  sum(iff(FILING_FEE_STATUS='FP',1,0)) n_fp,
  count(distinct _SOURCE_RUN_ID) n_runs
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1 order by 1
