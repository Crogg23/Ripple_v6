with ss as (select RNDRNG_NPI n, max(upper(RNDRNG_PRVDR_LAST_ORG_NAME)) ln, max(upper(RNDRNG_PRVDR_FIRST_NAME)) fn, max(RNDRNG_PRVDR_STATE_ABRVTN) st, max(upper(RNDRNG_PRVDR_CITY)) city, max(RNDRNG_PRVDR_TYPE) typ,
   sum(try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar)) a
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399' group by 1),
r as (select ss.*, row_number() over (order by a desc) rk from ss)
select 'leie' src, r.rk, r.n, r.ln, r.fn, r.typ, r.city, r.st, round(r.a) ss_allowed, l.EXCLUSION_TYPE x, l.EXCLUSION_DATE::varchar xd, upper(l.CITY) xcity, iff(l.NPI=r.n,'npi','name+state') how
 from r join LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l on l.NPI = r.n or (upper(l.LAST_NAME)=r.ln and upper(l.FIRST_NAME)=r.fn and l.STATE=r.st)
union all
select 'sam', r.rk, r.n, r.ln, r.fn, r.typ, r.city, r.st, round(r.a), s.EXCLUSION_TYPE||' / '||s.EXCLUDING_AGENCY||' / '||s.EXCLUSION_PROGRAM||' / term '||coalesce(s.TERMINATION_DATE_RAW,''), s.ACTIVATION_DATE::varchar, upper(s.CITY), iff(s.NPI=r.n,'npi','name+state')
 from r join LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS s on s.NPI = r.n or (upper(s.LAST_NAME)=r.ln and upper(s.FIRST_NAME)=r.fn and s.STATE=r.st)
order by rk
