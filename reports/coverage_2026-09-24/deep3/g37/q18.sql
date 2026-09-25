-- TRI peer group: ethanol plants (primary NAICS 325193 in the 2023 TRI file). Per parent: plants, ECHO match, quarters out of compliance,
-- formal actions; plus each POET plant's ECHO row (programs, 12-quarter history string) to see what kind of violation it is
with b as (select C_2_TRIFD id, any_value(C_30_PRIMARY_NAICS) naics from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 group by 1),
t as (select t.TRI_FACILITY_ID, t.EPA_REGISTRY_ID, t.FACILITY_NAME, t.CITY_NAME, t.STATE_ABBR, coalesce(nullif(trim(t.STANDARDIZED_PARENT_COMPANY), ''), '(no parent)') par
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY t join b on t.TRI_FACILITY_ID = b.id where b.naics = '325193' and t.FAC_CLOSED_IND = '0'),
e as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select EPA_REGISTRY_ID from t)),
j as (select t.*, e.QUARTERS_WITH_NONCOMPLIANCE qnc, e.FORMAL_ACTION_COUNT fac, e.THREE_YR_COMPLIANCE_HISTORY h, e.HAS_AIR_PROGRAM air, e.HAS_WATER_PROGRAM wat,
        e.COMPLIANCE_STATUS cst, e.LAST_PENALTY_AMT_ALLOCATED pen, e.DATE_LAST_FORMAL_ACTION dlfa
      from t left join e on t.EPA_REGISTRY_ID = e.FRS_ID)
select 'par' k, par a, count(*)::text b, count_if(qnc is not null)::text c, count_if(qnc >= 6)::text d, round(avg(qnc), 2)::text e, sum(fac)::text f,
  count_if(qnc >= 1)::text g, null h, null i
from j group by rollup(par) having count(*) >= 4 or par is null
union all
select * from (select 'poet', FACILITY_NAME, CITY_NAME || ', ' || STATE_ABBR, qnc::text, h, fac::text, 'air=' || air::text || ' water=' || wat::text, cst, coalesce(pen::text, '-') || ' ' || coalesce(dlfa::text, '-'), EPA_REGISTRY_ID
  from j where par ilike 'POET%' order by qnc desc nulls last limit 40);
