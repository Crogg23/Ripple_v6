-- (rerun: cast pct/date to text for the union) Medicare owner files (home health owners mart, SNF ownership landing): any individual owner whose first+last name equals one of the 29 cluster officials, or any organization owner named like a cluster entity; agency state shown for the second-field check
with ao(f,l) as (select * from values ('ADEBAYO','OSHINUGA'),('ADEJUMOKE','OSHINUGA'),('ALFRED','PEREZ'),('AMY','GARCIA'),('ANN','LOZANO'),('ARTURO','ELIZONDO'),('BENJAMIN','ARISE'),('CHARLES','ROY'),('DARRELL','ELLIOTT'),('FAYE','HORN'),('JAMES','GRISMORE'),('JASMINE','PEREZ'),('JENNIFER','ROY'),('JOHN','PRICE'),('KAYLA','VASQUEZ'),('KIMBERLEY','WINN'),('MARIA','RAMOS'),('MARK','MITCHELL'),('PATRICK','ILOANYA'),('RUBEN','MONTEZ'),('SEGUN','OGUNGBEMI'),('SHANNA','WURM'),('SHAPOUR','OLIA'),('STACY','SAIZ'),('SYLVIA','MUNIZ'),('SYLVIE','BOAL'),('THOMAS','OZGO'),('TRACY','GLEASON'),('YOLANDA','GARZA'))
select 'HHA' src, h.ORGANIZATION_NAME agency, h.CCN, h.AGENCY_STATE st, coalesce(h.FIRST_NAME_OWNER||' '||h.LAST_NAME_OWNER, h.ORGANIZATION_NAME_OWNER) owner, h.ROLE_TEXT_OWNER role, h.PERCENTAGE_OWNERSHIP::string pct, h.ASSOCIATION_DATE_OWNER::string dt, h.CITY_OWNER owner_city
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS h
where (upper(trim(h.FIRST_NAME_OWNER)), upper(trim(h.LAST_NAME_OWNER))) in (select f,l from ao)
   or h.ORGANIZATION_NAME_OWNER ilike any ('%CFHC%','%JP2D%','%TULIP HOSPICE%','%J ROY CONSULTING%','%OSHINUGA%','%WURZBACH%')
union all
select 'SNF', s.ORGANIZATION_NAME, null, s.STATE_OWNER, coalesce(s.FIRST_NAME_OWNER||' '||s.LAST_NAME_OWNER, s.ORGANIZATION_NAME_OWNER), s.ROLE_TEXT_OWNER, s.PERCENTAGE_OWNERSHIP::string, s.ASSOCIATION_DATE_OWNER::string, s.CITY_OWNER
from LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP s
where (upper(trim(s.FIRST_NAME_OWNER)), upper(trim(s.LAST_NAME_OWNER))) in (select f,l from ao)
   or s.ORGANIZATION_NAME_OWNER ilike any ('%CFHC%','%JP2D%','%TULIP HOSPICE%','%J ROY CONSULTING%','%OSHINUGA%')
order by 1, 5
