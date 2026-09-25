-- key Reliant owners (on 2+ Reliant homes): real name, and every SNF they appear on nationwide, split inside vs outside CHAIN_ID 446
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
keyown as (select o.ASSOCIATE_ID_OWNER from rel join en on en.ccn=rel.ccn join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID group by 1 having count(distinct rel.ccn)>=2)
select o.ASSOCIATE_ID_OWNER, o.TYPE_OWNER,
  max(coalesce(nullif(trim(o.ORGANIZATION_NAME_OWNER),''), trim(o.FIRST_NAME_OWNER)||' '||trim(o.MIDDLE_NAME_OWNER)||' '||trim(o.LAST_NAME_OWNER))) owner_name,
  max(o.TITLE_OWNER) title,
  count(distinct en.ccn) all_homes, count(distinct iff(rel.ccn is null, en.ccn, null)) homes_outside_446,
  listagg(distinct iff(rel.ccn is null, en.ccn||':'||en.STATE, null), ',') outside_list
from keyown k join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ASSOCIATE_ID_OWNER=k.ASSOCIATE_ID_OWNER
join en on en.ENROLLMENT_ID=o.ENROLLMENT_ID left join rel on rel.ccn=en.ccn
group by 1,2 order by all_homes desc
