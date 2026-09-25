-- ASM participants -> Part B by provider (2024, RNDRNG_NPI), OIG exclusion list, opt-out list: land rate, specialty, state agreement; plus orgs whose ASM state disagrees with Part B
with a as (select NPI, any_value(STATE) st, any_value(ASM_COHORT) coh, any_value(ORGANIZATION_LEGAL_NAME) org, max(ASM_CY27_SMALLPRACTICE) sp
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS group by 1),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN bst, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
l as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
o as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS),
j as (select a.*, b.typ, b.bst, b.benes, b.pay, l.npi leie, o.npi optout from a left join b on b.npi=a.NPI left join l on l.npi=a.NPI left join o on o.npi=a.NPI)
select 'total' k, coh a, null b, count(*) n, count(typ) landed, count_if(bst=st) same_state, count(leie) leie, count(optout) optout, round(median(pay)) med_pay, round(median(benes)) med_benes
from j group by 2
union all select * from (select 'spec', coh, typ, count(*), count(typ), count_if(bst=st), count(leie), count(optout), round(median(pay)), round(median(benes)) from j where typ is not null group by 2,3 qualify row_number() over (partition by coh order by count(*) desc) <= 8)
union all select * from (select 'mismatch', org, st||'>'||listagg(distinct bst, ','), count(*), null, null, null, null, null, null from j where bst is not null and bst<>st group by org, st order by 4 desc limit 10)
order by 1, 2, 4 desc
