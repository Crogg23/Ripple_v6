-- #16c the 13 top-50 suppliers missing from PECOS (rewritten with joins): name, catheter/alginate money, LEIE date, NPPES enumeration; plus PECOS landing ingest stamp
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505','1063414571','1588302186','1689457772','1790533503','1528004108','1225009665','1871564211','1578139473','1629247036','1003970260','1881972040') group by 1),
 l as (select NPI, max(EXCLUSION_DATE)::varchar leie_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI in (select npi from s) group by 1),
 g as (select to_varchar(min(INGESTED_AT)) mi, to_varchar(max(INGESTED_AT)) ma from LIBRARY_RAW.LANDING.FED_CMS_PECOS_PROVIDER_ENROLLMENT)
select s.npi, s.org, s.st, round(s.paid) paid, round(s.cath) cath, round(s.alg) alg, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao, l.leie_dt, g.mi pecos_ingest_min, g.ma pecos_ingest_max
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi left join l on l.NPI=s.npi cross join g order by s.paid desc
