with b as (select RNDRNG_NPI n, HCPCS_CD h, left(HCPCS_DESC,40) hd, try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar) a, try_to_double(TOT_SRVCS::varchar) s, try_to_double(TOT_BENES::varchar) bn
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399'),
p as (select n, sum(a) ss_allowed, sum(s) sqcm, max(bn) max_code_benes, count(*) codes,
   max_by(h, a) top_code, max_by(hd, a) top_desc, max(a)/sum(a) top_share from b group by n),
r as (select p.*, row_number() over (order by ss_allowed desc) rk from p)
select r.rk, r.n npi, v.RNDRNG_PRVDR_LAST_ORG_NAME last, v.RNDRNG_PRVDR_FIRST_NAME first, v.RNDRNG_PRVDR_TYPE typ, v.RNDRNG_PRVDR_CITY city, v.RNDRNG_PRVDR_STATE_ABRVTN st,
  round(r.ss_allowed) ss_allowed, r.sqcm, r.max_code_benes, r.codes, r.top_code, r.top_desc, round(r.top_share,3) top_share,
  v.TOT_BENES prov_benes, v.TOT_MDCR_ALOWD_AMT prov_allowed, v.DRUG_MDCR_ALOWD_AMT drug_allowed, v.DRUG_TOT_BENES drug_benes, v.DRUG_SPRSN_IND,
  (select count(*) from p) n_billers, (select round(sum(ss_allowed)) from p) nat_allowed
from r left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER v on v.RNDRNG_NPI = r.n
where r.rk <= 30 order by r.rk
