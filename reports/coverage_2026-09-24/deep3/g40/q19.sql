-- (rerun of q18 after a GROUP BY slip) The series that stops: San Joaquin Valley APCD informal actions by month 2023-2026, vs its formal actions
-- and compliance evaluations by year; and every California air district: operating majors, informal and formal actions by period
with f as (select PGM_SYS_ID, STATE, LOCAL_CONTROL_REGION_NAME lcr, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where STATE='CA'),
maj as (select coalesce(lcr,'(no district)') lcr, count(*) n_maj from f where cls='MAJ' and op='OPR' group by 1),
inf as (select a.ACTIVITY_ID, a.ACHIEVED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.ACHIEVED_DATE between '2019-01-01' and '2026-07-31'),
frm as (select a.ACTIVITY_ID, a.SETTLEMENT_ENTERED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.SETTLEMENT_ENTERED_DATE between '2019-01-01' and '2026-09-24'),
ev as (select a.ACTIVITY_ID, coalesce(try_to_date(a.ACTUAL_END_DATE::text), try_to_date(a.ACTUAL_END_DATE::text,'MM/DD/YYYY')) d, a.STATE_EPA_FLAG ag, f.lcr
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES a join f using (PGM_SYS_ID)),
allx as (select 'i' src, ACTIVITY_ID, d, coalesce(lcr,'(no district)') lcr from inf
         union all select 'f', ACTIVITY_ID, d, coalesce(lcr,'(no district)') from frm
         union all select 'e', ACTIVITY_ID, d, coalesce(lcr,'(no district)') from ev where d between '2019-01-01' and '2026-09-24')
select 'sjv_inf_month' k, to_char(date_trunc('month',d),'YYYY-MM') a, count(distinct ACTIVITY_ID)::text b, listagg(distinct ag,'') c, null d, null e, null f, null g
  from inf where lcr like 'San Joaquin%' and d>='2023-07-01' group by 2
union all select 'sjv_year', year(d)::text, count(distinct iff(src='i',ACTIVITY_ID,null))::text, count(distinct iff(src='f',ACTIVITY_ID,null))::text,
  count(distinct iff(src='e',ACTIVITY_ID,null))::text, max(iff(src='i',d,null))::text, max(iff(src='f',d,null))::text, max(iff(src='e',d,null))::text
  from allx where lcr like 'San Joaquin%' group by 2
union all select 'ca_district', left(x.lcr,50), max(maj.n_maj)::text,
  count(distinct iff(src='i' and year(d) between 2019 and 2023, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2024, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='f' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='e' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text
from allx x left join maj on maj.lcr=x.lcr group by 2
