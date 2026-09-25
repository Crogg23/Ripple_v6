-- clinicians Medicare lists at the 34 cluster hospice CCNs (CCN join), how many hospice CCNs each lists nationally, and their Part B billing (NPI join)
with cl as (select column1 ccn from values ('741649'),('971659'),('971695'),('971743'),('971758'),('971769'),('971787'),('971795'),('A91507'),('A91509'),('A91562'),('A91564'),('A91565'),('A91572'),('A91574'),('A91578'),('A91591'),('A91592'),('A91595'),('A91607'),('A91611'),('A91619'),('A91620'),('A91623'),('A91625'),('A91626'),('A91627'),('A91631'),('A91644'),('A91654'),('A91662'),('A91677'),('A91696'),('A91711')),
a as (select NPI, max(PROVIDER_FIRST_NAME) fn, max(PROVIDER_LAST_NAME) ln, listagg(distinct CCN, ',') ccns, count(distinct CCN) n_cl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where CCN in (select ccn from cl) group by 1),
allh as (select NPI, count(distinct CCN) n_hospice, count(distinct iff(CCN like 'A9%' or CCN like '97%' or CCN like '74%' or CCN like '67%' or CCN like '45%', CCN, null)) n_tx_hospice
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where FACILITY_TYPE ilike '%hospice%' and NPI in (select NPI from a) group by 1),
pb as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_CITY city, TOT_BENES, TOT_MDCR_PYMT_AMT pay
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER where RNDRNG_NPI in (select NPI from a))
select a.*, allh.n_hospice, allh.n_tx_hospice, pb.typ, pb.city, pb.TOT_BENES, pb.pay,
  (select count(*) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where CCN in (select ccn from cl)) rows_matched,
  (select count(distinct CCN) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where CCN in (select ccn from cl)) ccns_matched
from a left join allh on allh.NPI=a.NPI left join pb on pb.npi=a.NPI order by allh.n_hospice desc nulls last
