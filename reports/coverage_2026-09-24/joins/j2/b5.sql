-- #15 top 15 A6197 suppliers: NPPES enumeration date + official, PECOS presence, LEIE presence (all on NPI)
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid, sum(try_to_number(TOT_SUPLR_BENES)) b
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where HCPCS_CD='A6197' group by 1 order by paid desc limit 15)
select s.npi, s.org, s.st, round(s.paid) paid, s.b, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.NPI_DEACTIVATION_DATE::varchar deact, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao,
 (select count(*) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT p where p.NPI=s.npi) pecos_rows,
 (select max(EXCLUSION_DATE)::varchar from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l where l.NPI=s.npi) leie_dt
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi order by s.paid desc
-- #16 the 13 top-50 suppliers missing from PECOS: name, state, catheter and alginate money, LEIE date, NPPES enumeration; plus PECOS landing ingest stamp
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505','1063414571','1588302186','1689457772','1790533503','1528004108','1225009665','1871564211','1578139473','1629247036','1003970260','1881972040') group by 1)
select s.npi, s.org, s.st, round(s.paid) paid, round(s.cath) cath, round(s.alg) alg, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao,
 (select max(EXCLUSION_DATE)::varchar from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l where l.NPI=s.npi) leie_dt,
 (select to_varchar(max(_INGESTED_AT)) from LIBRARY_RAW.LANDING.FED_CMS_PECOS_PROVIDER_ENROLLMENT) pecos_ingest
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi order by s.paid desc
