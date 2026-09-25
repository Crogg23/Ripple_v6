with b as (select RNDRNG_NPI n, HCPCS_CD h, HCPCS_DESC hd, try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar) a, try_to_double(TOT_SRVCS::varchar) s, try_to_double(TOT_BENES::varchar) bn, try_to_double(AVG_MDCR_ALOWD_AMT::varchar) px
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399')
select h, max(hd) hd, round(sum(a)) allowed, count(distinct n) billers, sum(s) sqcm, sum(bn) bene_rows, round(avg(px)) avg_px, round(sum(a)/(select sum(a) from b),4) share
from b group by h order by allowed desc limit 30
