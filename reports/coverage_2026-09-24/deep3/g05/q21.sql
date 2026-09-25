-- ASM peer comparison: participants vs same-specialty clinicians in the same states who are not in the model (Part B 2024): headcount share vs Medicare payment share, median pay and patients
with a as (select NPI, any_value(ASM_COHORT) coh from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS group by 1),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
      where RNDRNG_PRVDR_TYPE in ('Cardiology','Physical Medicine and Rehabilitation','Orthopedic Surgery','Pain Management','Anesthesiology','Interventional Pain Management','Neurosurgery')),
sts as (select distinct b.typ, b.st from b join a on a.NPI=b.npi),
j as (select b.*, (a.NPI is not null) inmodel from b join sts using (typ, st) left join a on a.NPI=b.npi)
select typ, count(*) clinicians, count_if(inmodel) in_model, round(100*count_if(inmodel)/count(*),1) pct_heads,
  round(100*sum(iff(inmodel,pay,0))/sum(pay),1) pct_pay, round(median(iff(inmodel,pay,null))) med_pay_in, round(median(iff(not inmodel,pay,null))) med_pay_out,
  round(median(iff(inmodel,benes,null))) med_benes_in, round(median(iff(not inmodel,benes,null))) med_benes_out, count(distinct st) states
from j group by 1 order by 2 desc
