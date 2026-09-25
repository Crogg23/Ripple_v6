-- # FAERS late-filing test: days from company awareness (MFR_DT) to FDA receipt (FDA_DT), spike quarters vs normal quarters, same drugs. Expedited reports are due in 15 days
with d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q,
   MFR_DT mfr, coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, upper(trim(REPT_COD)) rept from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
   where SRC_QUARTER in ('2010q2','2010q4','2011q2','2011q3','2012q1','2012q4','2013q3','2014q2')),
dr as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id,
   case when upper(DRUGNAME) like 'AVANDIA%' then 'AVANDIA' when upper(DRUGNAME) in ('TARCEVA','ERLOTINIB TABLET') then 'TARCEVA' else upper(trim(DRUGNAME)) end drug
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where SRC_QUARTER in ('2010q2','2010q4','2011q2','2011q3','2012q1','2012q4','2013q3','2014q2') and upper(trim(ROLE_COD))='PS'
   and (upper(DRUGNAME) like 'AVANDIA%' or upper(trim(DRUGNAME)) in ('TARCEVA','ERLOTINIB TABLET','AVASTIN','HERCEPTIN','RITUXAN','XELODA','TRACLEER','GLIVEC','GLEEVEC'))),
de as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
c as (select dr.drug, d.q, d.cs, min(d.mfr) mfr, min(d.fda) fda, max(iff(de.id is not null,1,0)) died from d join dr on dr.id=d.id left join de on de.id=d.id group by 1,2,3)
select drug, q, count(*) cases, sum(died) death_cases, count(mfr) has_mfr_dt, median(datediff(day,mfr,fda)) med_days_mfr_to_fda,
  count_if(datediff(day,mfr,fda)>15) over_15d, count_if(datediff(day,mfr,fda)>365) over_1yr, min(mfr) earliest_mfr, max(fda) latest_fda
from c group by 1,2 order by 1,2
-- # FAERS INDI trap check: across the 2012q4 format switch, how is 'unknown reason' spelled, and what share of lines is it
select SRC_QUARTER q, count(*) n,
  count_if(upper(INDI_PT) like '%UNKNOWN%') unknown_any, count_if(INDI_PT like '%UNKNOWN%') unknown_upper, count_if(INDI_PT like '%nknown%') unknown_mixed,
  count(distinct INDI_PT) dist_raw, count(distinct upper(INDI_PT)) dist_upper, count(nullif(trim(DRUG_SEQ),'')) has_drug_seq, count(nullif(trim(INDI_DRUG_SEQ),'')) has_indi_drug_seq
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI where SRC_QUARTER between '2011q3' and '2014q2' group by 1 order by 1
