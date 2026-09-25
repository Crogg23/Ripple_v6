-- FJC appeals (AO data behind Table B-12): per circuit x fiscal year, rows and PUBLICATION_STATUS code mix
select CIRCUIT, TAPE_YEAR, count(*) n_rows,
  count(distinct DOCKET||'|'||REOPEN) n_appeals,
  sum(iff(PUBLICATION_STATUS='-8',1,0)) ps_m8,
  sum(iff(PUBLICATION_STATUS='0',1,0)) ps_0,
  sum(iff(PUBLICATION_STATUS='1',1,0)) ps_1,
  sum(iff(PUBLICATION_STATUS='2',1,0)) ps_2,
  sum(iff(PUBLICATION_STATUS='3',1,0)) ps_3,
  sum(iff(PUBLICATION_STATUS='4',1,0)) ps_4,
  sum(iff(PUBLICATION_STATUS='5',1,0)) ps_5,
  sum(iff(coalesce(PUBLICATION_STATUS,'x') not in ('-8','0','1','2','3','4','5'),1,0)) ps_other,
  min(DOCKET) dk_min, max(DOCKET) dk_max
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
where TAPE_YEAR between '2016' and '2026'
group by 1,2 order by 1,2;
