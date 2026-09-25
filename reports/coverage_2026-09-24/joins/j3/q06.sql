with ss as (select RNDRNG_NPI n, sum(try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar)) a
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399' group by 1),
op as (select NPI, APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME m, try_to_double(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS::varchar) amt
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS where NPI is not null and trim(NPI) <> ''),
agg as (select op.m, round(sum(amt)) all_amt, count(distinct op.NPI) all_npis,
  round(sum(iff(ss.n is not null, amt, 0))) biller_amt, count(distinct ss.n) biller_npis,
  round(sum(iff(ss.n is not null, ss.a, 0))) dummy
  from op left join ss on ss.n = op.NPI group by op.m)
select m, all_amt, all_npis, biller_amt, biller_npis, round(biller_amt/nullif(all_amt,0),3) biller_share,
  (select count(*) from ss) n_billers, (select count(distinct NPI) from op where NPI in (select n from ss)) billers_with_any_payment
from agg where biller_npis > 0 order by biller_amt desc limit 60
