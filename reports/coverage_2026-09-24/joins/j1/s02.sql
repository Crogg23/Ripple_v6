-- Reliant homes (CHAIN_ID 446) -> SNF enrollment (CCN) -> owner file (ENROLLMENT_ID): every owner/controller, grouped per owner
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS)
select o.ASSOCIATE_ID_OWNER, o.TYPE_OWNER, coalesce(o.ORGANIZATION_NAME_OWNER, o.FIRST_NAME_OWNER||' '||o.LAST_NAME_OWNER) owner_name,
  o.STATE_OWNER, listagg(distinct o.ROLE_TEXT_OWNER, ' | ') roles, count(distinct rel.ccn) reliant_homes,
  min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) first_date, max(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) last_date,
  max(try_to_number(o.PERCENTAGE_OWNERSHIP)) max_pct
from rel join en on en.ccn=rel.ccn join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
group by 1,2,3,4 order by reliant_homes desc, owner_name
