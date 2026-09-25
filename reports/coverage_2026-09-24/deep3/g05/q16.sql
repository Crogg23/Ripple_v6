-- OTP NPIs -> Part B by provider (2024): land rate, pay per patient vs state median; reverse check: Part B 'Opioid Treatment Program' billers missing from the OTP list; OIG exclusions
with otp as (select NPI, any_value(PROVIDER_NAME) nm, any_value(STATE) st, count(*) sites from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS group by 1),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN bst, RNDRNG_PRVDR_LAST_ORG_NAME bnm, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
l as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
j as (select otp.*, b.typ, b.benes, b.pay, b.pay/nullif(b.benes,0) ppb, l.npi leie from otp left join b on b.npi=otp.NPI left join l on l.npi=otp.NPI),
jm as (select j.*, median(ppb) over (partition by st) st_med, count(ppb) over (partition by st) st_n from j)
select 'sum' k, count(*)::text a, count(typ)::text b, count_if(typ ilike '%opioid%')::text c, count(leie)::text d, round(median(ppb))::text e, round(sum(pay)/1e6,1)::text f, sum(benes)::text g, null h from j
union all select 'rev', count(*)::text, count_if(npi not in (select NPI from otp))::text, round(sum(iff(npi not in (select NPI from otp), pay, 0))/1e6,1)::text, listagg(distinct iff(npi not in (select NPI from otp), bst, null), ',')::text, null, null, null, null
  from b where typ ilike '%opioid%'
union all select * from (select 'top_ppb', NPI, left(nm,30), st, sites::text, benes::text, round(pay)::text, round(ppb)::text, round(st_med)::text||' (n='||st_n||')' from jm where ppb is not null order by ppb/nullif(st_med,0) desc limit 10)
union all select * from (select 'top_pay', NPI, left(nm,30), st, sites::text, benes::text, round(pay)::text, round(ppb)::text, round(st_med)::text from jm where pay is not null order by pay desc limit 6)
