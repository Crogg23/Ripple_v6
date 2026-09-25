-- South Coast blank, checked by county not by district label: LA, Orange, Riverside, San Bernardino facilities, all-time enforcement records and last dates
with f as (select PGM_SYS_ID, coalesce(LOCAL_CONTROL_REGION_NAME,'(none)') lcr, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
           where STATE='CA' and upper(COUNTY_NAME) in ('LOS ANGELES','ORANGE','RIVERSIDE','SAN BERNARDINO')),
i as (select PGM_SYS_ID, count(*) n, max(ACHIEVED_DATE) mx from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1),
fo as (select PGM_SYS_ID, count(*) n, max(SETTLEMENT_ENTERED_DATE) mx, listagg(distinct STATE_EPA_FLAG,'') ag from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1),
v as (select PGM_SYS_ID, count(*) n, max(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE)) mx from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1)
select left(f.lcr,40) lcr, count(*) facs, count_if(cls='MAJ' and op='OPR') maj_opr,
  sum(coalesce(i.n,0)) inf_all, max(i.mx) inf_last, sum(coalesce(fo.n,0)) frm_all, max(fo.mx) frm_last, listagg(distinct fo.ag,'') frm_agencies,
  sum(coalesce(v.n,0)) viol_all, max(v.mx) viol_last
from f left join i using (PGM_SYS_ID) left join fo using (PGM_SYS_ID) left join v using (PGM_SYS_ID)
group by 1 order by facs desc
