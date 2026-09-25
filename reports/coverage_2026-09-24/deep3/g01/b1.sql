-- @estab_sample
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
where owner_operator_firm_name ilike 'sterigenics%' limit 3
-- @faers_by_quarter
select src_quarter, count(*) n,
  count_if(role_cod in ('PS','SS','C','I')) role_ok,
  count(distinct isr) isrs,
  count_if(isr is null or isr = '') isr_blank,
  count_if(primaryid is not null and primaryid <> '') pid_filled,
  count(dose_amt) dose_filled, max(dose_amt) max_dose,
  count(exp_dt) exp_filled
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
group by 1 order by 1
-- @va_all
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_ALLCAUSE_MORTALITY
-- @od_all
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_OVERDOSE
-- @inj_landing_all
select * from LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY
