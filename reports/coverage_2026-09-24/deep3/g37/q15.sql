-- TRI facility -> ECHO (EPA_REGISTRY_ID = FRS_ID) -> 2023 TRI industry sector: parent companies with 15+ open TRI facilities,
-- share of their facilities out of compliance 6+ of the last 12 quarters, and formal actions; grouped by sector so parents meet their peers
with t as (select TRI_FACILITY_ID, EPA_REGISTRY_ID, STANDARDIZED_PARENT_COMPANY par from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY
           where FAC_CLOSED_IND = '0' and nullif(trim(STANDARDIZED_PARENT_COMPANY), '') is not null),
e as (select FRS_ID, max(QUARTERS_WITH_NONCOMPLIANCE) qnc, max(FORMAL_ACTION_COUNT) fac, count(*) erows
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select EPA_REGISTRY_ID from t) group by 1),
s as (select C_2_TRIFD id, any_value(C_23_INDUSTRY_SECTOR) sector, sum(C_65_ON_SITE_RELEASE_TOTAL) onsite
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 group by 1),
j as (select t.*, e.qnc, e.fac, e.erows, s.sector, s.onsite from t left join e on t.EPA_REGISTRY_ID = e.FRS_ID left join s on t.TRI_FACILITY_ID = s.id)
select 'parent' k, par, count(*) fac_n, count_if(qnc is not null) in_echo, count_if(qnc >= 6) qnc6, avg(qnc) avg_qnc, sum(fac) formal,
  count_if(sector is not null) filed23, mode(sector) top_sector, sum(onsite) onsite_lb, max(erows) max_erows
from j group by 2 having count(*) >= 15
union all
select 'sector', sector, count(*), count_if(qnc is not null), count_if(qnc >= 6), avg(qnc), sum(fac), count(*), null, sum(onsite), max(erows)
from j where sector is not null group by 2
union all
select 'all', 'open TRI facilities with a parent', count(*), count_if(qnc is not null), count_if(qnc >= 6), avg(qnc), sum(fac), count_if(sector is not null), null, sum(onsite), max(erows) from j
order by 1, 5 desc;
