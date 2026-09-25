-- FJC appeals: decode OUTCOME by appeal type, with DISPOSITION / METHOD / procedural-termination alongside (terminated tapes only)
select APPEAL_TYPE::string t, OUTCOME::string o, count(*) n,
  sum(iff(DISPOSITION::string='1',1,0)) d1, sum(iff(DISPOSITION::string='2',1,0)) d2,
  sum(iff(DISPOSITION::string='4',1,0)) d4, sum(iff(DISPOSITION::string='5',1,0)) d5,
  sum(iff(METHOD::string='1',1,0)) m1, sum(iff(METHOD::string='3',1,0)) m3, sum(iff(METHOD::string='4',1,0)) m4,
  sum(iff(PROCEDURAL_TERMINATION::string<>'-8',1,0)) proc_term, sum(iff(US_APPELLANT::string='1',1,0)) us_appellant
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
where TAPE_YEAR::string <> '2099' and APPEAL_TYPE::string in ('1','3','4','6','19','21','17')
group by 1,2 order by 1,3 desc
