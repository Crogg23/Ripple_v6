-- #17 same product menu: suppliers billing catheters (A4353), alginate (A6197), CGM supplies (A4239) and knee+wrist braces (L1852, L3916) together
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  count(distinct iff(HCPCS_CD in ('A4353','A6197','A4239','L1852','L3916'), HCPCS_CD, null)) menu, count(distinct HCPCS_CD) codes,
  sum(iff(HCPCS_CD in ('A4353','A6197'), try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT, 0)) cath_alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL group by 1)
select menu, count(*) suppliers, round(sum(paid)) paid, listagg(iff(menu>=4, org||' ('||st||') $'||round(paid/1e6,1)||'M/'||codes||' codes', null), '; ') within group (order by paid desc) who
from s where menu>=3 group by 1 order by 1 desc
