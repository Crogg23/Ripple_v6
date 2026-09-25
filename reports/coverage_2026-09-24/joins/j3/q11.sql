with b as (select RNDRNG_NPI n, max(RNDRNG_PRVDR_TYPE) typ, sum(try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar)) a, max(try_to_double(TOT_BENES::varchar)) mb, sum(try_to_double(TOT_SRVCS::varchar)) sq
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399' group by 1),
p as (select b.*, a/mb per_pt, sq/mb sq_per_pt, v.DRUG_TOT_BENES::number db, a/nullif(v.DRUG_TOT_BENES::number,0) per_drug_pt from b left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER v on v.RNDRNG_NPI=b.n),
g as (select 'all' grp, * from p union all select 'general_surgery', * from p where typ='General Surgery' union all select 'top20', * from p qualify row_number() over (order by a desc) <= 20)
select grp, count(*) n, round(median(a)) med_allowed, round(median(per_pt)) med_per_pt, round(percentile_cont(0.9) within group (order by per_pt)) p90_per_pt, round(max(per_pt)) max_per_pt,
  round(median(sq_per_pt)) med_sqcm_per_pt, round(max(sq_per_pt)) max_sqcm_per_pt,
  count_if(per_pt >= 3280000) n_ge_kapadia, round(median(per_drug_pt)) med_per_drug_pt,
  max(iff(n='1669736427', rank_pp, null)) kapadia_rank_per_pt
from (select g.*, rank() over (partition by grp order by per_pt desc) rank_pp from g) group by grp
