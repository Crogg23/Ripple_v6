-- misses to confirm: (a) HHS-OIG exclusion list rows naming DESTEFANE or RELIANT CARE or a Reliant home NPI; (b) hospital cost reports (HCRIS) on any Reliant CCN
select 'leie' src, count(*) n, listagg(coalesce(BUSINESS_NAME,'')||' '||coalesce(LAST_NAME,'')||','||coalesce(FIRST_NAME,'')||' '||coalesce(CITY,'')||' '||coalesce(STATE,'')||' '||coalesce(EXCLUSION_DATE::varchar,''), '; ') detail
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
where upper(LAST_NAME)='DESTEFANE' or upper(BUSINESS_NAME) like '%RELIANT CARE%'
   or NPI in (select NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS e join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n on lpad(trim(e.CCN),6,'0')=lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0') where n.CHAIN_ID='446')
union all
select 'hcris', count(*), listagg(distinct PROVIDER_CCN, ',') from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS
where lpad(trim(PROVIDER_CCN::varchar),6,'0') in (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446')
