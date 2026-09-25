-- Every air ID at the plant address, on the registry ID, or named Tesla / NUMMI anywhere: NOVs and formal actions
with f as (select PGM_SYS_ID, REGISTRY_ID, left(FACILITY_NAME,40) nm, left(STREET_ADDRESS,30) st, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op, NAICS_CODES, left(LOCAL_CONTROL_REGION_NAME,20) lcr
   from {F}
   where FACILITY_NAME ilike '%TESLA%' or FACILITY_NAME ilike '%NUMMI%' or FACILITY_NAME ilike '%NEW UNITED MOTOR%' or STREET_ADDRESS ilike '%45500%FREMONT%' or REGISTRY_ID='110000482898'),
inf as (select PGM_SYS_ID, count(distinct iff(ACHIEVED_DATE>='2019-01-01',ACTIVITY_ID,null)) n19, count(distinct ACTIVITY_ID) n_all, max(ACHIEVED_DATE) last_inf
   from {I} where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1),
frm as (select PGM_SYS_ID, count(distinct iff(SETTLEMENT_ENTERED_DATE>='2010-01-01',ACTIVITY_ID,null)) f10, count(distinct ACTIVITY_ID) f_all, max(SETTLEMENT_ENTERED_DATE) last_frm,
     sum(iff(SETTLEMENT_ENTERED_DATE>='2010-01-01',PENALTY_AMOUNT,0)) pen10, count_if(SETTLEMENT_ENTERED_DATE is null) f_nodate
   from {A} where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1)
select f.*, coalesce(inf.n19,0) n19, coalesce(inf.n_all,0) n_all, inf.last_inf, coalesce(frm.f10,0) f10, coalesce(frm.f_all,0) f_all, frm.last_frm, frm.pen10, frm.f_nodate
from f left join inf using (PGM_SYS_ID) left join frm using (PGM_SYS_ID)
order by coalesce(inf.n_all,0) desc, coalesce(frm.f_all,0) desc limit 40
