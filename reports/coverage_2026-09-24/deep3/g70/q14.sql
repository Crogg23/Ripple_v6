-- SDWA within-state test: private groundwater community systems serving 25-500 people, mobile home parks (MH+MP) vs other residential (RA, SU, HA, OR, MU), per state; health-based and monitoring violations 2021-2025
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, PRIMACY_AGENCY_CODE st, POPULATION_SERVED_COUNT pop from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
      where PWS_ACTIVITY_CODE = 'A' and GW_SW_CODE = 'GW' and PWS_TYPE_CODE = 'CWS' and OWNER_TYPE_CODE = 'P' and POPULATION_SERVED_COUNT between 25 and 500),
v as (select PWSID, count(distinct iff(IS_HEALTH_BASED_IND = 'Y', VIOLATION_ID, null)) hb, count(distinct iff(VIOLATION_CATEGORY_CODE in ('MR', 'MON'), VIOLATION_ID, null)) mr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where COMPL_PER_BEGIN_DATE >= '2021-01-01' and COMPL_PER_BEGIN_DATE < '2026-01-01' and VIOLATION_ID is not null group by 1),
x as (select p.st, case when sa.code in ('MH', 'MP') then 'MHP' when sa.code in ('RA', 'SU', 'HA', 'OR', 'MU') then 'RES' end grp, iff(pop <= 100, 'small', 'mid') band,
        coalesce(v.hb, 0) > 0 anyhb, coalesce(v.mr, 0) > 0 anymr
      from p join sa on sa.PWSID = p.PWSID left join v on v.PWSID = p.PWSID where sa.code in ('MH', 'MP', 'RA', 'SU', 'HA', 'OR', 'MU')),
cell as (select st, band, count_if(grp = 'MHP') m_n, count_if(grp = 'MHP' and anyhb) m_hb, count_if(grp = 'MHP' and anymr) m_mr,
           count_if(grp = 'RES') r_n, count_if(grp = 'RES' and anyhb) r_hb, count_if(grp = 'RES' and anymr) r_mr from x group by 1, 2),
st as (select st, sum(m_n) m_n, sum(m_hb) m_hb, sum(m_mr) m_mr, sum(r_n) r_n, sum(r_hb) r_hb, sum(r_mr) r_mr,
          sum(iff(r_n > 0, m_n * r_hb / r_n, null)) m_hb_expected, sum(iff(r_n > 0, m_n * r_mr / r_n, null)) m_mr_expected from cell group by 1)
select * from (select 'state' k, st, m_n, m_hb, round(100 * m_hb / nullif(m_n, 0), 1) m_pct_hb, r_n, r_hb, round(100 * r_hb / nullif(r_n, 0), 1) r_pct_hb,
  round(100 * m_mr / nullif(m_n, 0), 1) m_pct_mr, round(100 * r_mr / nullif(r_n, 0), 1) r_pct_mr, round(m_hb_expected, 0) m_hb_exp from st where m_n >= 40 order by m_n desc limit 30)
union all select 'all_states_matched', null, sum(m_n), sum(m_hb), round(100 * sum(m_hb) / sum(m_n), 1), sum(r_n), sum(r_hb), round(100 * sum(r_hb) / sum(r_n), 1),
  round(100 * sum(m_mr) / sum(m_n), 1), round(100 * sum(m_mr_expected) / sum(m_n), 1), round(sum(m_hb_expected), 0) from st where r_n > 0 and m_n > 0
union all select 'states_mhp_worse_hb', null, count_if(m_n >= 40 and r_n >= 40), count_if(m_n >= 40 and r_n >= 40 and m_hb / m_n > r_hb / r_n), null,
  count_if(m_n >= 40 and r_n >= 40 and m_mr / m_n > r_mr / r_n), null, round(median(iff(m_n >= 40 and r_n >= 40, 100 * (m_hb / m_n - r_hb / r_n), null)), 1), null, null, null from st
