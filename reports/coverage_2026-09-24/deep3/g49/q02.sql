-- FJC appeals: the dockets with the most rows (glance saw 1116673 at 1.6K rows). Duplicate load, or mass appeal?
select CIRCUIT, DOCKET, count(*) n, count(distinct REOPEN) n_reopen, count(distinct TAPE_YEAR) n_tape,
  count(distinct APPEAL_RECORD_ID) n_recid, count(distinct APPELLANT) n_appellant_names,
  min(APPELLANT) a_min, max(APPELLANT) a_max, max(APPELLEE) ee_max,
  min(DOCKET_DATE) dd_min, max(DOCKET_DATE) dd_max, mode(NATURE_OF_SUIT) nos, mode(APPEAL_TYPE) atype, mode(OUTCOME) outcome
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1,2 order by n desc limit 15
