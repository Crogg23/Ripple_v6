-- NRC main copy, rail peers by year 2015-2025: Norfolk Southern (any spelling incl. NS abbreviations) vs CSX, Union Pacific, BNSF,
-- all railroads by org name, and the org type / source of NS calls, to test whether NS's 2020 fall is name drift
with m as (select upper(trim(RESPONSIBLE_COMPANY)) co, year(DATE_TIME_RECEIVED) y, RESPONSIBLE_ORG_TYPE ot, SOURCE src
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS where year(DATE_TIME_RECEIVED) between 2015 and 2025),
c as (select y, ot, src,
        case when co like '%NORFOLK SOUTHERN%' or co like '%NORFOLK SO%' or co like 'NS RAIL%' or co like 'N S RAIL%' or co like 'NSRR%' or co = 'NS' or co like 'NS %' then 'NS'
             when co like '%CSX%' then 'CSX' when co like '%UNION PACIFIC%' or co like 'UPRR%' then 'UP' when co like '%BNSF%' or co like '%BURLINGTON NORTHERN%' then 'BNSF'
             when co like '%CANADIAN NATIONAL%' or co like 'CN RAIL%' then 'CN' when co like '%RAIL%' then 'OTHER_RAIL' else null end fam, co
      from m)
select fam, count_if(y = 2015) y15, count_if(y = 2016) y16, count_if(y = 2017) y17, count_if(y = 2018) y18, count_if(y = 2019) y19,
  count_if(y = 2020) y20, count_if(y = 2021) y21, count_if(y = 2022) y22, count_if(y = 2023) y23, count_if(y = 2024) y24, count_if(y = 2025) y25,
  count(distinct co) spellings, listagg(distinct iff(y in (2019, 2020), ot || '/' || src, null), '; ') types_19_20
from c where fam is not null group by 1 order by 1;
