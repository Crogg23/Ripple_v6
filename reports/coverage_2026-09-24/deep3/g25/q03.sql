-- EPA informal actions: same months (Jan-Jul) across years, by program; plus full-year totals
select year(ACHIEVED_DATE) yr, count(*) n_all, count_if(month(ACHIEVED_DATE) <= 7) jan_jul,
  count_if(PGM_SYS_ACRNM='ICIS' and month(ACHIEVED_DATE) <= 7) icis_jj, count_if(PGM_SYS_ACRNM='RCRAINFO' and month(ACHIEVED_DATE) <= 7) rcra_jj,
  count_if(PGM_SYS_ACRNM not in ('ICIS','RCRAINFO') and month(ACHIEVED_DATE) <= 7) other_jj,
  count(distinct REGISTRY_ID) facs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
where year(ACHIEVED_DATE) >= 2008 group by 1 order by 1
