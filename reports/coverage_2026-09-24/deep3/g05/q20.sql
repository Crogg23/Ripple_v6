-- OTP completeness: Part B 2024 'Opioid Treatment Program' billers whose NPI is not in the OTP list, by state, and whether their name+state is in the list under another NPI
with otp as (select NPI, upper(PROVIDER_NAME) nm, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS),
b as (select RNDRNG_NPI npi, upper(RNDRNG_PRVDR_LAST_ORG_NAME) bnm, RNDRNG_PRVDR_STATE_ABRVTN bst, RNDRNG_PRVDR_CITY city, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER where RNDRNG_PRVDR_TYPE ilike '%opioid%'),
miss as (select b.*, exists(select 1 from otp where otp.STATE=b.bst and left(otp.nm,12)=left(b.bnm,12)) name_state_in_list from b where b.npi not in (select NPI from otp))
select 'state' k, bst a, count(*)::text b, count_if(name_state_in_list)::text c, round(sum(pay)/1e6,2)::text d, sum(benes)::text e, null f
from miss group by 2
union all select * from (select 'row', npi, left(bnm,34), bst||' '||city, name_state_in_list::text, benes::text, round(pay)::text from miss order by pay desc limit 12)
order by 1, 2
