-- The series that stops: San Joaquin Valley APCD informal actions by month 2023-2026, vs its formal actions and compliance evaluations by year;
-- and every California air district: operating majors, informal and formal actions by period (is the district in the file at all?)
with f as (select PGM_SYS_ID, STATE, LOCAL_CONTROL_REGION_NAME lcr, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where STATE='CA'),
inf as (select a.ACTIVITY_ID, a.ACHIEVED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.ACHIEVED_DATE between '2019-01-01' and '2026-07-31'),
frm as (select a.ACTIVITY_ID, a.SETTLEMENT_ENTERED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.SETTLEMENT_ENTERED_DATE between '2019-01-01' and '2026-09-24'),
ev as (select a.ACTIVITY_ID, coalesce(try_to_date(a.ACTUAL_END_DATE::text), try_to_date(a.ACTUAL_END_DATE::text,'MM/DD/YYYY')) d, a.STATE_EPA_FLAG ag, f.lcr
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES a join f using (PGM_SYS_ID))
select 'sjv_inf_month' k, to_char(date_trunc('month',d),'YYYY-MM') a, count(distinct ACTIVITY_ID)::text b, listagg(distinct ag,'') c, null d, null e, null f, null g
  from inf where lcr like 'San Joaquin%' and d>='2023-07-01' group by 2
union all select 'sjv_year', y::text, sum(nf)::text, sum(nfr)::text, sum(nev)::text, null, null, null from (
  select year(d) y, count(distinct ACTIVITY_ID) nf, 0 nfr, 0 nev from inf where lcr like 'San Joaquin%' group by 1
  union all select year(d), 0, count(distinct ACTIVITY_ID), 0 from frm where lcr like 'San Joaquin%' group by 1
  union all select year(d), 0, 0, count(distinct ACTIVITY_ID) from ev where lcr like 'San Joaquin%' and d between '2019-01-01' and '2026-09-24' group by 1) group by 1
union all select 'ca_district', left(coalesce(lcr,'(no district)'),50),
  (select count(*) from f f2 where coalesce(f2.lcr,'')=coalesce(x.lcr,'') and f2.cls='MAJ' and f2.op='OPR')::text,
  count(distinct iff(src='i' and year(d) between 2019 and 2023, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2024, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='f' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='e' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text
from (select 'i' src, ACTIVITY_ID, d, lcr from inf union all select 'f', ACTIVITY_ID, d, lcr from frm union all select 'e', ACTIVITY_ID, d, lcr from ev where d between '2019-01-01' and '2026-09-24') x
group by x.lcr
