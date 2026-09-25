-- #11 PECOS coverage check: are big DME suppliers in the PECOS enrollment table at all?
with s as (select SUPLR_NPI npi, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL group by 1),
 r as (select npi, paid, row_number() over (order by paid desc) rk from s),
 p as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT)
select iff(rk<=50,'top50','rest') grp, count(*) suppliers, count(p.NPI) in_pecos,
 listagg(iff(rk<=50 and p.NPI is null, r.npi, null), ',') within group (order by rk) top50_missing
from r left join p on r.npi=p.NPI group by 1
-- #12 the June-2026 1128Aa DME batch in LEIE: who, where, when, and billing in the supplier file (NPI join)
with l as (select NPI, BUSINESS_NAME, SPECIALTY, EXCLUSION_DATE, CITY, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where EXCLUSION_TYPE='1128Aa' and EXCLUSION_DATE between '2026-06-01' and '2026-06-30'),
 s as (select SUPLR_NPI, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg, sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL group by 1)
select l.EXCLUSION_DATE::varchar dt, l.BUSINESS_NAME, l.SPECIALTY, l.CITY, l.STATE, l.NPI, round(s.paid) paid, round(s.alg) alginate, round(s.cath) catheter from l left join s on l.NPI=s.SUPLR_NPI order by dt, l.STATE
-- #13 other DME suppliers in the two ZIPs (33483 Delray Beach, 11377 Woodside) and the two DME-taxonomy neighbors at 100 E Linton
select SUPLR_NPI, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_ST1) st1, max(SUPLR_PRVDR_ZIP5) zip, count(*) codes, round(sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT)) paid,
 listagg(distinct HCPCS_CD, ',') within group (order by HCPCS_CD) hcpcs
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL
where SUPLR_PRVDR_ZIP5 in ('33483','11377') or SUPLR_NPI in ('1326505710','1083959159') group by 1 order by paid desc
-- #14 DOJ press-release link text (Wayback replay), FCA settlements, CourtListener dockets: names and alginate
select 'DOJ_LISTING' src, CAPTURED_AT::varchar dt, LINK_TEXT txt, RESOLVED_URL url from LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
 where LINK_TEXT ilike any ('%SUNSHINE SENIOR%','%ALMAZ%','%PESSOA%','%TSOTSKHALASHVILI%','%ALGINATE%','%WOUND DRESSING%','%CATHETER%')
union all
select 'FCA', SETTLEMENT_DATE::varchar, CASE_TITLE||' / '||coalesce(PERSON_NAME,''), PRESS_RELEASE_URL from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_DOJ_FCA_SETTLEMENTS
 where CASE_TITLE ilike any ('%SUNSHINE%','%ALMAZ%') or PERSON_NAME ilike any ('%PESSOA%','%TSOTSKHALASHVILI%')
union all
select 'CL_DOCKET', DATE_FILED::varchar, CASE_NAME||' | '||coalesce(DOCKET_NUMBER,'')||' | court '||coalesce(COURT_ID,''), CAUSE from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
 where CASE_NAME ilike any ('%SUNSHINE SENIOR SOLUTIONS%','%ALMAZ MED%','%TSOTSKHALASHVILI%','%DANA PESSOA%','%PESSOA, DANA%','%V. PESSOA%')
