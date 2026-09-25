-- #18 the two suppliers' share of each code they bill, nationally (paid and patients-rowsum)
with s as (select SUPLR_NPI npi, HCPCS_CD c, try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT p, try_to_number(TOT_SUPLR_BENES) b
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL
  where HCPCS_CD in ('A4353','A6197','A4239','E2103','L1852','L3916','L0651','L0486'))
select c, count(distinct npi) suppliers, round(sum(p)) paid, round(sum(iff(npi='1811518392',p,0))) sunshine, round(sum(iff(npi='1487343505',p,0))) almaz,
 round(100*sum(iff(npi in ('1811518392','1487343505'),p,0))/sum(p),1) two_pct_paid, sum(b) benes_rowsum, sum(iff(npi in ('1811518392','1487343505'),b,0)) two_benes
from s group by 1 order by paid desc
