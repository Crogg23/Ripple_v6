-- Subparts as a peer group with a public-health edge: ethylene oxide sterilizers (Part 63 Subpart O, major or area source tag);
-- NOVs, violations and formal actions since 2019 per plant (formal counted across air IDs sharing the FRS registry ID)
with sub as (select PGM_SYS_ID, listagg(distinct AIR_PROGRAM_SUBPART_CODE,'|') codes from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS
             where AIR_PROGRAM_SUBPART_CODE in ('CAAMACTO','CAAGACTMO') group by 1),
fac as (select f.PGM_SYS_ID, f.REGISTRY_ID, f.FACILITY_NAME, f.CITY, f.STATE, f.AIR_POLLUTANT_CLASS_CODE cls, f.AIR_OPERATING_STATUS_CODE op, f.NAICS_CODES, sub.codes
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES f join sub using (PGM_SYS_ID)),
allf as (select PGM_SYS_ID, REGISTRY_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where REGISTRY_ID in (select REGISTRY_ID from fac)),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1),
vh as (select PGM_SYS_ID, count(*) n, count(HPV_DAYZERO_DATE) hpv from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
       where coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE) >= '2019-01-01' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1),
fr as (select allf.REGISTRY_ID, count(distinct a.ACTIVITY_ID) n, sum(a.PENALTY_AMOUNT) pen from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join allf using (PGM_SYS_ID)
       where a.SETTLEMENT_ENTERED_DATE >= '2019-01-01' group by 1)
select 'summary' k, count(*)::text a, count_if(op='OPR')::text b, count_if(coalesce(inf.n,0)>0)::text c, count_if(coalesce(vh.n,0)>0)::text d, count_if(coalesce(fr.n,0)>0)::text e,
  median(coalesce(inf.n,0))::text f, null g, null h
from fac left join inf using (PGM_SYS_ID) left join vh using (PGM_SYS_ID) left join fr on fr.REGISTRY_ID=fac.REGISTRY_ID
union all select * from (select 'plant', FACILITY_NAME, CITY||' '||STATE, op||' '||coalesce(cls,''), coalesce(inf.n,0)::text, coalesce(vh.n,0)::text||' viol / '||coalesce(vh.hpv,0)::text||' hpv',
  coalesce(fr.n,0)::text, round(fr.pen)::text, NAICS_CODES
from fac left join inf using (PGM_SYS_ID) left join vh using (PGM_SYS_ID) left join fr on fr.REGISTRY_ID=fac.REGISTRY_ID
order by coalesce(inf.n,0)+coalesce(vh.n,0) desc limit 15)
