-- EPA informal actions: by program x statute x action type, and date sanity
select PGM_SYS_ACRNM, STATUTE, ENF_TYPE_DESC, count(*) n, count(distinct REGISTRY_ID) facs,
  min(ACHIEVED_DATE) dmin, max(ACHIEVED_DATE) dmax, count_if(ACHIEVED_DATE is null) dnull,
  count_if(year(ACHIEVED_DATE) < 1990) pre1990, count(distinct ENF_IDENTIFIER) ids, count_if(REGISTRY_ID is null or trim(REGISTRY_ID)='') reg_blank
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
group by 1,2,3 order by n desc limit 40
