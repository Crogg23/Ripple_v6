-- FJC appeals: decode PUBLICATION_STATUS against OPINION_DISPOSITION and DISPOSITION, FY2019-2025, with 4th Circuit counts
select PUBLICATION_STATUS, OPINION_DISPOSITION, DISPOSITION, count(*) n,
  sum(iff(CIRCUIT='4',1,0)) n_ca4,
  sum(iff(nullif(OUTCOME,'-8') is not null,1,0)) n_outcome_filled,
  sum(iff(HEARING_DATE is not null,1,0)) n_hearing,
  min(iff(CIRCUIT='4',DOCKET,null)) ex_ca4_docket
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
where TAPE_YEAR between '2019' and '2025'
group by 1,2,3 order by 4 desc limit 60;
