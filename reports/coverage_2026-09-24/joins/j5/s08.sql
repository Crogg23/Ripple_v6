-- exclusions: the 29 cluster authorized officials (first+last name), the 68 cluster org names, and the 14 affiliated clinicians (NPI) against OIG LEIE and SAM exclusions, any state (state shown for the second-field check)
with ao(f,l) as (select * from values ('ADEBAYO','OSHINUGA'),('ADEJUMOKE','OSHINUGA'),('ALFRED','PEREZ'),('AMY','GARCIA'),('ANN','LOZANO'),('ARTURO','ELIZONDO'),('BENJAMIN','ARISE'),('CHARLES','ROY'),('DARRELL','ELLIOTT'),('FAYE','HORN'),('JAMES','GRISMORE'),('JASMINE','PEREZ'),('JENNIFER','ROY'),('JOHN','PRICE'),('KAYLA','VASQUEZ'),('KIMBERLEY','WINN'),('MARIA','RAMOS'),('MARK','MITCHELL'),('PATRICK','ILOANYA'),('RUBEN','MONTEZ'),('SEGUN','OGUNGBEMI'),('SHANNA','WURM'),('SHAPOUR','OLIA'),('STACY','SAIZ'),('SYLVIA','MUNIZ'),('SYLVIE','BOAL'),('THOMAS','OZGO'),('TRACY','GLEASON'),('YOLANDA','GARZA')),
docs(npi) as (select * from values ('1003981242'),('1477940856'),('1174028039'),('1427168061'),('1558417147'),('1588699797'),('1922331776'),('1356536031'),('1093997488'),('1093033243'),('1679702872'),('1396931457'),('1437105863'),('1023113792'))
select 'LEIE' src, 'official name' how, l.FIRST_NAME, l.LAST_NAME, l.BUSINESS_NAME, l.SPECIALTY, l.EXCLUSION_TYPE, l.EXCLUSION_DATE, l.CITY, l.STATE
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l join ao on upper(trim(l.FIRST_NAME))=ao.f and upper(trim(l.LAST_NAME))=ao.l
union all
select 'LEIE', 'clinician NPI', l.FIRST_NAME, l.LAST_NAME, l.BUSINESS_NAME, l.SPECIALTY, l.EXCLUSION_TYPE, l.EXCLUSION_DATE, l.CITY, l.STATE
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l where l.NPI in (select npi from docs)
union all
select 'LEIE', 'hospice word, TX business', l.FIRST_NAME, l.LAST_NAME, l.BUSINESS_NAME, l.SPECIALTY, l.EXCLUSION_TYPE, l.EXCLUSION_DATE, l.CITY, l.STATE
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l where l.STATE='TX' and (l.BUSINESS_NAME ilike '%CFHC%' or l.BUSINESS_NAME ilike '%HOSPICE%')
union all
select 'SAM', 'official name', s.FIRST_NAME, s.LAST_NAME, s.ENTITY_NAME, s.EXCLUSION_PROGRAM, s.EXCLUSION_TYPE, s.ACTIVATION_DATE, s.CITY, s.STATE
from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS s join ao on upper(trim(s.FIRST_NAME))=ao.f and upper(trim(s.LAST_NAME))=ao.l
union all
select 'SAM', 'hospice word, TX entity', s.FIRST_NAME, s.LAST_NAME, s.ENTITY_NAME, s.EXCLUSION_PROGRAM, s.EXCLUSION_TYPE, s.ACTIVATION_DATE, s.CITY, s.STATE
from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS s where s.STATE='TX' and (s.ENTITY_NAME ilike '%CFHC%' or s.ENTITY_NAME ilike '%HOSPICE%')
