-- Verify in the warehouse: Title V certs deduped by ACTIVITY_ID, deviation-flag fill and Y rate 2020-2025 for TX, CO, LA, national; plus violations per operating major 2016-2025
with c as (select PGM_SYS_ID, ACTIVITY_ID, max(FACILITY_RPT_DEVIATION_FLAG) flag, max(ACTUAL_END_DATE) d, count(*) copies
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS group by 1,2),
fac as (select PGM_SYS_ID, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
cs as (select f.STATE, count(*) certs, count_if(c.flag is not null) flagged, count_if(c.flag='Y') y
       from c join fac f using (PGM_SYS_ID) where year(c.d) between 2020 and 2025 group by 1),
vs as (select f.STATE, count(*) viol from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join fac f using (PGM_SYS_ID)
       where coalesce(v.EARLIEST_FRV_DETERM_DATE, v.HPV_DAYZERO_DATE) between '2016-01-01' and '2025-12-31' group by 1),
ms as (select STATE, count(*) majors from fac where cls='MAJ' and op='OPR' group by 1),
st as (select ms.STATE, ms.majors, coalesce(vs.viol,0) viol, round(coalesce(vs.viol,0)/ms.majors,2) viol_per_major, cs.certs, cs.flagged, cs.y, round(cs.y/nullif(cs.flagged,0),3) y_rate
       from ms left join vs using (STATE) left join cs using (STATE) where ms.majors >= 50)
select * from st where STATE in ('TX','CO','LA','CA','NC','PA')
union all select 'MEDIAN(majors>=50)', median(majors), median(viol), median(viol_per_major), median(certs), median(flagged), median(y), median(y_rate) from st
union all select 'DUP_ACTIVITY_IDS', count_if(copies>1), sum(copies)-count(*), null, count(*), null, null, null from c
