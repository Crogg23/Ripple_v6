-- National sweep for blind spots: per air jurisdiction (district if any, else state), inspections still logged in 2025
-- but violations / informal actions stopped or collapsed vs their 2021-2023 average
with f as (select PGM_SYS_ID, coalesce(LOCAL_CONTROL_REGION_NAME, 'state ' || STATE) jur, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
i as (select f.jur, count(distinct iff(year(ACHIEVED_DATE) between 2021 and 2023, ACTIVITY_ID, null))/3 inf_avg2123,
        count(distinct iff(year(ACHIEVED_DATE)=2025, ACTIVITY_ID, null)) inf25, max(ACHIEVED_DATE) inf_last
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a join f using (PGM_SYS_ID)
      where ACHIEVED_DATE between '1990-01-01' and '2026-07-31' group by 1),
v as (select f.jur, count_if(year(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE)) between 2021 and 2023)/3 v_avg2123,
        count_if(year(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE))=2025) v25, max(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE)) v_last
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY a join f using (PGM_SYS_ID)
      where coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE) <= '2026-09-24' group by 1),
e as (select f.jur, count(distinct iff(year(coalesce(try_to_date(ACTUAL_END_DATE::text), try_to_date(ACTUAL_END_DATE::text,'MM/DD/YYYY')))=2025, ACTIVITY_ID, null)) ev25
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES a join f using (PGM_SYS_ID) group by 1),
m as (select jur, count_if(cls='MAJ' and op='OPR') maj from f group by 1)
select left(m.jur,45) jur, m.maj, e.ev25, round(i.inf_avg2123,1) inf_avg2123, coalesce(i.inf25,0) inf25, i.inf_last, round(v.v_avg2123,1) v_avg2123, coalesce(v.v25,0) v25, v.v_last
from m left join e using (jur) left join i using (jur) left join v using (jur)
where m.maj >= 10 and coalesce(e.ev25,0) >= 50
  and (coalesce(v.v25,0) <= 0.25*coalesce(v.v_avg2123,0) or coalesce(v.v_last,'1900-01-01') < '2021-01-01' or coalesce(i.inf_last,'1900-01-01') < '2021-01-01')
order by m.maj desc
