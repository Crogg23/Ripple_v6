-- s07: the dull explanation, tested against peers. Did Nebraska's formal-action flow break at the Oct-2014 ICIS-Air migration?
-- Per state: formal actions a year 2010-2014 vs 2016-2025, informal a year same windows, and violation (FRV/HPV) rows entered 2015-2018 vs 2019-2025.
with f as (select PGM_SYS_ID, any_value(STATE) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
fa as (select f.st, count_if(year(a.SETTLEMENT_ENTERED_DATE) between 2010 and 2014) / 5 fa_pre, count_if(year(a.SETTLEMENT_ENTERED_DATE) between 2016 and 2025) / 10 fa_post
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join f on a.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
ia as (select f.st, count_if(year(i.ACHIEVED_DATE) between 2010 and 2014) / 5 ia_pre, count_if(year(i.ACHIEVED_DATE) between 2016 and 2025) / 10 ia_post
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS i join f on i.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
vh as (select f.st, count_if(v.ENF_RESPONSE_POLICY_CODE = 'FRV' and year(v.EARLIEST_FRV_DETERM_DATE) between 2015 and 2018) frv_15_18,
         count_if(v.ENF_RESPONSE_POLICY_CODE = 'FRV' and year(v.EARLIEST_FRV_DETERM_DATE) between 2019 and 2025) frv_19_25,
         count_if(v.ENF_RESPONSE_POLICY_CODE = 'HPV' and year(v.HPV_DAYZERO_DATE) between 2015 and 2018) hpv_15_18,
         count_if(v.ENF_RESPONSE_POLICY_CODE = 'HPV' and year(v.HPV_DAYZERO_DATE) between 2019 and 2025) hpv_19_25
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join f on v.PGM_SYS_ID = f.PGM_SYS_ID group by 1)
select fa.st, round(fa.fa_pre, 1) fa_yr_10_14, round(fa.fa_post, 1) fa_yr_16_25, round(fa.fa_post / nullif(fa.fa_pre, 0), 2) fa_ratio,
  round(ia.ia_pre, 1) ia_yr_10_14, round(ia.ia_post, 1) ia_yr_16_25, vh.frv_15_18, vh.frv_19_25, vh.hpv_15_18, vh.hpv_19_25
from fa left join ia on fa.st = ia.st left join vh on fa.st = vh.st
where fa.fa_pre >= 3
order by fa_ratio asc nulls first limit 25;
