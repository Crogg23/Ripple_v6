-- #1 other vintages: any table named like DME / durable medical in raw or marts
select 'RAW' db, table_schema, table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike any ('%DURABLE%','%DMEPOS%','%\_DME\_%','%DME\_%','%SUPPLIER%','%ALGINATE%')
union all
select 'MARTS', table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike any ('%DURABLE%','%DMEPOS%','%\_DME\_%','%DME\_%','%SUPPLIER%')
order by 1,3
-- #2 alginate codes A6196-A6199: whole-file paid, allowed, benes, suppliers; and the two suppliers
with s as (select SUPLR_NPI npi, HCPCS_CD c, try_to_number(TOT_SUPLR_SRVCS) sv, try_to_number(TOT_SUPLR_BENES) b, AVG_SUPLR_MDCR_PYMT_AMT p, AVG_SUPLR_MDCR_ALOWD_AMT a
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where HCPCS_CD in ('A6196','A6197','A6198','A6199'))
select c, count(distinct npi) suppliers, round(sum(sv*p)) paid, round(sum(sv*a)) allowed, sum(b) benes_rowsum, sum(sv) services,
 round(sum(iff(npi='1811518392',sv*p,0))) sunshine_paid, round(sum(iff(npi='1487343505',sv*p,0))) almaz_paid,
 sum(iff(npi in ('1811518392','1487343505'),b,0)) two_benes, count_if(b is null) null_benes
from s group by rollup(c) order by c nulls last
