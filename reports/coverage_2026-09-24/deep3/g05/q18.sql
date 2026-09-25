-- ASM eyeball: the participants whose NPI is on the OIG exclusion list or the Medicare opt-out list, with both names so the match can be checked
with a as (select NPI, any_value(FIRST_NAME||' '||LAST_NAME) nm, any_value(STATE) st, any_value(ASM_COHORT) coh, any_value(ORGANIZATION_LEGAL_NAME) org
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS group by 1),
l as (select trim(NPI) npi, EXCLUSION_TYPE, EXCLUSION_DATE, REINSTATEMENT_DATE, WAS_REINSTATED, HAS_WAIVER, LAST_NAME, FIRST_NAME, STATE, SPECIALTY
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
o as (select trim(NPI) npi, OPTOUT_EFFECTIVE_DATE, OPTOUT_END_DATE, SPECIALTY, FIRST_NAME, LAST_NAME, STATE_CODE, LAST_UPDATED
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS)
select 'leie' k, a.NPI, a.nm, a.st, a.coh, left(a.org,30) org, l.EXCLUSION_TYPE x1, l.EXCLUSION_DATE::text x2, l.REINSTATEMENT_DATE::text x3,
  l.FIRST_NAME||' '||l.LAST_NAME x4, l.STATE x5, l.WAS_REINSTATED::text||'/'||l.HAS_WAIVER::text x6, l.SPECIALTY x7
from a join l on l.npi=a.NPI
union all
select 'optout', a.NPI, a.nm, a.st, a.coh, left(a.org,30), o.SPECIALTY, o.OPTOUT_EFFECTIVE_DATE::text, o.OPTOUT_END_DATE::text,
  o.FIRST_NAME||' '||o.LAST_NAME, o.STATE_CODE, o.LAST_UPDATED::text, null
from a join o on o.npi=a.NPI
order by 1, 8
