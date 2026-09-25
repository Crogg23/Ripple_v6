-- j5: Texas hospice clusters. Every statement run, in order, 2026-09-24. Door: Python (connect/db.py).
-- Each connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'
-- 16 statements total. Failed / broken runs, kept for the record:
--   statement 10: failed (150K PPP table spells columns without underscores)
--   statement 11: ran but returned 0 rows because '\b' inside a Snowflake string is not a regex word boundary; result discarded
--   statement 15: failed (numeric vs text in a UNION); statement 16 is the rerun
-- Result files: j5/<label>.json

-- [s01] statement 1
-- find every table that could carry hospice money, owners, officials, exclusions, Texas corporate records
select 'MARTS' db, table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_schema <> 'TIMELINE' and (table_name ilike '%HOSPICE%' or table_name ilike '%LEIE%' or table_name ilike '%EXCLU%' or table_name ilike '%AFFILIAT%' or table_name ilike '%NPPES%' or table_name ilike '%POST_ACUTE%' or table_name ilike '%PAC%' or table_name ilike '%TX_SOS%' or table_name ilike '%TEXAS%' or table_name ilike '%OPENCORP%' or table_name ilike '%CORP%REG%' or table_name ilike '%GEOGRAPHIC_VAR%' or table_name ilike '%REVOC%' or table_name ilike '%CAHPS%' or table_name ilike '%OWNER%' or table_name ilike '%DOCKET%' or table_name ilike '%PART_A%' or table_name ilike '%UTILIZ%')
union all
select 'RAW', table_schema, table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
where table_schema='LANDING' and (table_name ilike '%HOSPICE%' or table_name ilike '%LEIE%' or table_name ilike '%EXCLU%' or table_name ilike '%AFFILIAT%' or table_name ilike '%NPPES%' or table_name ilike '%POST_ACUTE%' or table_name ilike '%PAC\\_%' or table_name ilike '%TX_SOS%' or table_name ilike '%TEXAS%' or table_name ilike '%OPENCORP%' or table_name ilike '%GEOGRAPHIC_VAR%' or table_name ilike '%REVOC%' or table_name ilike '%CAHPS%' or table_name ilike '%OWNER%' or table_name ilike '%PART_A%' or table_name ilike '%UTILIZ%' or table_name ilike '%TX\\_%')
order by 1,2,3
;

-- [s02] statement 2
-- roster: every certified hospice in Harris and Bexar counties TX, plus any TX hospice on the two cluster phones, with its enrollment row (CCN join) and a POS termination check (CCN join)
with h as (select CCN, FACILITY_NAME, ADDRESS_LINE_1, ADDRESS_LINE_2, CITY_TOWN, ZIP_CODE, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, OWNERSHIP_TYPE, CERTIFICATION_DATE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE
  where STATE='TX' and (upper(trim(COUNTY_PARISH)) in ('HARRIS','BEXAR') or regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') in ('7138741234','2814101013'))),
e as (select CCN, count(*) n_enr, max(NPI) npi, max(ASSOCIATE_ID) assoc, max(ORGANIZATION_NAME) org, max(DOING_BUSINESS_AS_NAME) dba, max(INCORPORATION_DATE) inc, max(PROPRIETARY_NONPROFIT) pnp, max(ADDRESS_LINE_1||' '||coalesce(ADDRESS_LINE_2,'')) eaddr
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS where STATE='TX' or ENROLLMENT_STATE='TX' group by 1),
pos as (select CCN, max(PRVDR_CTGRY_CD) cat, max(PGM_TRMNTN_CD) trm, max(TRMNTN_EXPRTN_DT) trm_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where STATE_CD='TX' group by 1)
select h.*, e.n_enr, e.npi, e.assoc, e.org, e.dba, e.inc, e.pnp, e.eaddr, pos.cat, pos.trm, pos.trm_dt
from h left join e on e.CCN=h.CCN left join pos on pos.CCN=h.CCN
order by h.county, h.ph
;

-- [s03] statement 3
-- NPPES: every Texas organization NPI with a hospice taxonomy (251G00000X) in slots 1-5, with authorized official and practice address/phone
select NPI, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME lbn, PROVIDER_OTHER_ORGANIZATION_NAME dba,
  PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a1, PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a2,
  PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME city, left(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE,5) zip,
  regexp_replace(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER,'[^0-9]','') ph,
  PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS m1, PROVIDER_ENUMERATION_DATE enum_dt, NPI_DEACTIVATION_DATE deact_dt, LAST_UPDATE_DATE upd,
  upper(trim(AUTHORIZED_OFFICIAL_FIRST_NAME)) ao_first, upper(trim(AUTHORIZED_OFFICIAL_MIDDLE_NAME)) ao_mid, upper(trim(AUTHORIZED_OFFICIAL_LAST_NAME)) ao_last,
  AUTHORIZED_OFFICIAL_TITLE_OR_POSITION ao_title, regexp_replace(AUTHORIZED_OFFICIAL_TELEPHONE_NUMBER,'[^0-9]','') ao_ph,
  IS_ORGANIZATION_SUBPART sub, PARENT_ORGANIZATION_LBN parent
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
where ENTITY_TYPE_CODE in ('2','2.0') and PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME='TX'
  and '251G00000X' in (HEALTHCARE_PROVIDER_TAXONOMY_CODE_1, HEALTHCARE_PROVIDER_TAXONOMY_CODE_2, HEALTHCARE_PROVIDER_TAXONOMY_CODE_3, HEALTHCARE_PROVIDER_TAXONOMY_CODE_4, HEALTHCARE_PROVIDER_TAXONOMY_CODE_5)
;

-- [s04] statement 4
-- any column anywhere in the marts or landing named like hospice (money or use by county/provider)
select 'MARTS' db, table_schema, table_name, listagg(column_name, ',') within group (order by column_name) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_schema not in ('TIMELINE','INFORMATION_SCHEMA') and (column_name ilike '%HOSPC%' or column_name ilike '%HOSPICE%' or column_name ilike '%HOS\\_%')
group by 1,2,3
union all
select 'RAW', table_schema, table_name, listagg(column_name, ',') within group (order by column_name)
from LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS where table_schema='LANDING' and (column_name ilike '%HOSPC%' or column_name ilike '%HOSPICE%' or column_name ilike '%HOS\\_%')
group by 1,2,3
order by 1,2,3
;

-- [s05] statement 5
-- NPPES national: every organization NPI with hospice taxonomy 251G00000X in slots 1-5 (peer group for "one official, many hospices, one building")
select NPI, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, upper(trim(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME)) city,
  upper(PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS) a1, upper(coalesce(PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS,'')) a2,
  regexp_replace(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER,'[^0-9]','') ph,
  PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME lbn, PROVIDER_ENUMERATION_DATE enum_dt, NPI_DEACTIVATION_DATE deact_dt,
  upper(trim(AUTHORIZED_OFFICIAL_FIRST_NAME)) ao_first, upper(trim(AUTHORIZED_OFFICIAL_LAST_NAME)) ao_last, IS_ORGANIZATION_SUBPART sub
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
where ENTITY_TYPE_CODE in ('2','2.0')
  and '251G00000X' in (HEALTHCARE_PROVIDER_TAXONOMY_CODE_1, HEALTHCARE_PROVIDER_TAXONOMY_CODE_2, HEALTHCARE_PROVIDER_TAXONOMY_CODE_3, HEALTHCARE_PROVIDER_TAXONOMY_CODE_4, HEALTHCARE_PROVIDER_TAXONOMY_CODE_5)
;

-- [s06] statement 6
-- all TX certified hospices (roster) with their enrollment row, full outer so enrollment-only rows show too
with h as (select CCN, FACILITY_NAME, ADDRESS_LINE_1, CITY_TOWN, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, OWNERSHIP_TYPE, CERTIFICATION_DATE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE where STATE='TX'),
e as (select CCN, NPI, ASSOCIATE_ID, ORGANIZATION_NAME, DOING_BUSINESS_AS_NAME, INCORPORATION_DATE, ADDRESS_LINE_1 e_a1, CITY e_city
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS where STATE='TX')
select coalesce(h.CCN,e.CCN) ccn, h.FACILITY_NAME, h.ADDRESS_LINE_1, h.CITY_TOWN, h.county, h.ph, h.OWNERSHIP_TYPE, h.CERTIFICATION_DATE,
  e.NPI, e.ASSOCIATE_ID, e.ORGANIZATION_NAME, e.DOING_BUSINESS_AS_NAME, e.INCORPORATION_DATE, e.e_a1, e.e_city, iff(h.CCN is null,'enr_only',iff(e.CCN is null,'roster_only','both')) side
from h full outer join e on e.CCN=h.CCN
;

-- [s07] statement 7
-- clinicians Medicare lists at the 34 cluster hospice CCNs (CCN join), how many hospice CCNs each lists nationally, and their Part B billing (NPI join)
with cl as (select column1 ccn from values ('741649'),('971659'),('971695'),('971743'),('971758'),('971769'),('971787'),('971795'),('A91507'),('A91509'),('A91562'),('A91564'),('A91565'),('A91572'),('A91574'),('A91578'),('A91591'),('A91592'),('A91595'),('A91607'),('A91611'),('A91619'),('A91620'),('A91623'),('A91625'),('A91626'),('A91627'),('A91631'),('A91644'),('A91654'),('A91662'),('A91677'),('A91696'),('A91711')),
a as (select NPI, max(PROVIDER_FIRST_NAME) fn, max(PROVIDER_LAST_NAME) ln, listagg(distinct CCN, ',') ccns, count(distinct CCN) n_cl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where CCN in (select ccn from cl) group by 1),
allh as (select NPI, count(distinct CCN) n_hospice, count(distinct iff(CCN like 'A9%' or CCN like '97%' or CCN like '74%' or CCN like '67%' or CCN like '45%', CCN, null)) n_tx_hospice
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where FACILITY_TYPE ilike '%hospice%' and NPI in (select NPI from a) group by 1),
pb as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_CITY city, TOT_BENES, TOT_MDCR_PYMT_AMT pay
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER where RNDRNG_NPI in (select NPI from a))
select a.*, allh.n_hospice, allh.n_tx_hospice, pb.typ, pb.city, pb.TOT_BENES, pb.pay,
  (select count(*) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where CCN in (select ccn from cl)) rows_matched,
  (select count(distinct CCN) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION where CCN in (select ccn from cl)) ccns_matched
from a left join allh on allh.NPI=a.NPI left join pb on pb.npi=a.NPI order by allh.n_hospice desc nulls last
;

-- [s08] statement 8
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
;

-- [s09] statement 9
-- CourtListener dockets: any case name with an official surname from the four clusters or a CFHC entity, plus every Texas federal case with HOSPICE in the name since 2015
select COURT_ID, DATE_FILED, DATE_TERMINATED, DOCKET_NUMBER, left(CASE_NAME,160) case_name, NATURE_OF_SUIT, CAUSE,
  case when CASE_NAME ilike '%OSHINUGA%' then 'oshinuga' when CASE_NAME ilike '%BENJAMIN ARISE%' or CASE_NAME ilike 'ARISE%' then 'arise'
       when CASE_NAME ilike '%CFHC%' or CASE_NAME ilike '%COMMUNITY FIRST HOSPICE%' then 'cfhc' when CASE_NAME ilike '%GLEASON%' and CASE_NAME ilike '%HOSPICE%' then 'gleason'
       when CASE_NAME ilike '%JP2D%' then 'jp2d' else 'tx hospice' end hit
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where CASE_NAME ilike '%OSHINUGA%' or CASE_NAME ilike '%BENJAMIN ARISE%' or CASE_NAME ilike 'ARISE,%' or CASE_NAME ilike '%CFHC%' or CASE_NAME ilike '%COMMUNITY FIRST HOSPICE%' or CASE_NAME ilike '%JP2D%'
   or (CASE_NAME ilike '%HOSPICE%' and COURT_ID in ('txsd','txwd','txnd','txed','txsb','txwb','txnb','txeb','ca5') and DATE_FILED >= '2015-01-01')
order by hit, DATE_FILED
;

-- [s10] statement 10
-- federal money by name: PPP loans (both tables) and USAspending assistance to Texas recipients whose normalized name equals a cluster legal/brand name (83 keys); city shown for the second-field check
with k(nk) as (select * from values ('ABIBHOSPICECARE'),('ABOVEBEYONDHOSPICE'),('ACACIAHOSPICE'),('ADVANCEDHOLISTICPALLIATIVECARE'),('ALDERHOSPICE'),('ALLFAITHHOSPICECARE'),('ALTAVITAHOSPICE'),('AMAZINGLYGRACEHOSPICE'),('ANCHOREDBYGRACEHOSPICECARE'),('ARIELHOSPICE'),('ARMSOFCOMPASSIONHOSPICECARE'),('ASHHOSPICE'),('BALSAMHOSPICE'),('BEXARHOSPICE'),('BIRCHHOSPICE'),('BLUEROSEHOSPICEANDPALLIATIVECARE'),('BRIGHTLIGHTINFUSIONHHANDPALLIATIVECARE'),('BUTTERFLYHOSPICEPALLATIVECARE'),('CELESTIALHOSPICE'),('CFHCNO12'),('CFHCNO13'),('CFHCNO14'),('CFHCNO15'),('CFHCNO17'),('CFHCNO18'),('CFHCNO19'),('CFHCNO20'),('CFHCNO21'),('CFHCNO22'),('CFHCNO23'),('CFHCNO4'),('CFHCNO7'),('CHARTERHEALTHCAREOFSANANTONIO'),('CHESTNUTHOSPICE'),('COMMUNITYFIRSTHOSPICECAREOFSANANTONIO'),('COMPASSIONHOSPICEOFTEXAS'),('CYPRESSHOSPICE'),('DISTINGUISHEDHOSPICE'),('DIVINECOMFORTCAREHOSPICE'),('DIVINEENCOUNTERHOSPICE'),('ELMHOSPICE'),('EVERGREENHOSPICE'),('FAMILYFIRSTHOSPICE'),('FOURPILLARSHOSPICE'),('GENISAHOSPICEINTEGRATIVECARE'),('HARMONYHOSPICE'),('HARMONYHOSPICECARE'),('HARRISCOUNTYHOSPICE'),('HEARTSOULHOSPICE'),('HFCHNO4'),('HICKORYHOSPICE'),('HONEYBEEHOSPICE'),('HOUSTONFIRSTHOSPICEANDPALLIATIVECARE'),('JP2DHEALTHSYSTEMS'),('JUNIPERHOSPICE'),('LOVINGHANDSHOSPICE'),('LOVINGTOUCHHOSPICE'),('MAPLEHOSPICE'),('MIDTOWNHOSPICE'),('NESTHOMEHOSPICE'),('NESTHOMEHOSPICEANDPALLIATIVECARE'),('NEWDAWNHOSPICE'),('NIGHTINGALEHOSPICECAREOFTEXAS'),('OLIVETREEHOSPICE'),('ORIGINSHOSPICE'),('PINEHOSPICE'),('PINNACLEHOSPICESERVICES'),('PRIDEHOSPICECARE'),('REDWOODHOSPICE'),('ROWANHOSPICE'),('SIGNATUREHOSPICEPALLIATIVECARE'),('SOUTHERNSKYHOSPICE'),('SPECIALTYHOSPICE'),('SPRUCEHOSPICE'),('SYCAMOREHOSPICE'),('TEXASHEALTHCARESOLUTIONS'),('TEXASHEROESHOSPICE'),('TIMELESSMOMENTSHOSPICE'),('TREASUREDMOMENTSHOSPICE'),('WESLEYHEALTHCARE'),('WILLOWTREEHOSPICE'),('WILMINGTONHOSPICE'),('YELLOWROSEHOSPICECARE')),
ppp as (select 'PPP' src, BORROWER_NAME nm, BORROWER_CITY city, DATE_APPROVED dt, CURRENT_APPROVAL_AMOUNT amt, JOBS_REPORTED jobs,
   regexp_replace(regexp_replace(upper(BORROWER_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP where BORROWER_STATE='TX'
  union all
  select 'PPP150K', BORROWER_NAME, BORROWER_CITY, DATE_APPROVED, CURRENT_APPROVAL_AMOUNT, JOBS_REPORTED,
   regexp_replace(regexp_replace(upper(BORROWER_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','')
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWER_STATE='TX'),
usa as (select 'USASPENDING' src, RECIPIENT_NAME nm, RECIPIENT_CITY_NAME city, min(ACTION_DATE) dt, sum(FEDERAL_ACTION_OBLIGATION) amt, listagg(distinct CFDA_NUMBER, ',') jobs,
   regexp_replace(regexp_replace(upper(RECIPIENT_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE='TX' and (RECIPIENT_NAME ilike '%HOSPICE%' or RECIPIENT_NAME ilike '%CFHC%' or RECIPIENT_NAME ilike '%HEALTH%')
  group by 1,2,3,7)
select src, nm, city, dt, amt, jobs from ppp where nk in (select nk from k)
union all
select src, nm, city, dt::string, amt, jobs from usa where nk in (select nk from k)
order by 1,2
;

-- [s10] statement 11
-- (rerun: 150K table uses unseparated column names) federal money by name: PPP loans (both tables) and USAspending assistance to Texas recipients whose normalized name equals a cluster legal/brand name (83 keys); city shown for the second-field check
with k(nk) as (select * from values ('ABIBHOSPICECARE'),('ABOVEBEYONDHOSPICE'),('ACACIAHOSPICE'),('ADVANCEDHOLISTICPALLIATIVECARE'),('ALDERHOSPICE'),('ALLFAITHHOSPICECARE'),('ALTAVITAHOSPICE'),('AMAZINGLYGRACEHOSPICE'),('ANCHOREDBYGRACEHOSPICECARE'),('ARIELHOSPICE'),('ARMSOFCOMPASSIONHOSPICECARE'),('ASHHOSPICE'),('BALSAMHOSPICE'),('BEXARHOSPICE'),('BIRCHHOSPICE'),('BLUEROSEHOSPICEANDPALLIATIVECARE'),('BRIGHTLIGHTINFUSIONHHANDPALLIATIVECARE'),('BUTTERFLYHOSPICEPALLATIVECARE'),('CELESTIALHOSPICE'),('CFHCNO12'),('CFHCNO13'),('CFHCNO14'),('CFHCNO15'),('CFHCNO17'),('CFHCNO18'),('CFHCNO19'),('CFHCNO20'),('CFHCNO21'),('CFHCNO22'),('CFHCNO23'),('CFHCNO4'),('CFHCNO7'),('CHARTERHEALTHCAREOFSANANTONIO'),('CHESTNUTHOSPICE'),('COMMUNITYFIRSTHOSPICECAREOFSANANTONIO'),('COMPASSIONHOSPICEOFTEXAS'),('CYPRESSHOSPICE'),('DISTINGUISHEDHOSPICE'),('DIVINECOMFORTCAREHOSPICE'),('DIVINEENCOUNTERHOSPICE'),('ELMHOSPICE'),('EVERGREENHOSPICE'),('FAMILYFIRSTHOSPICE'),('FOURPILLARSHOSPICE'),('GENISAHOSPICEINTEGRATIVECARE'),('HARMONYHOSPICE'),('HARMONYHOSPICECARE'),('HARRISCOUNTYHOSPICE'),('HEARTSOULHOSPICE'),('HFCHNO4'),('HICKORYHOSPICE'),('HONEYBEEHOSPICE'),('HOUSTONFIRSTHOSPICEANDPALLIATIVECARE'),('JP2DHEALTHSYSTEMS'),('JUNIPERHOSPICE'),('LOVINGHANDSHOSPICE'),('LOVINGTOUCHHOSPICE'),('MAPLEHOSPICE'),('MIDTOWNHOSPICE'),('NESTHOMEHOSPICE'),('NESTHOMEHOSPICEANDPALLIATIVECARE'),('NEWDAWNHOSPICE'),('NIGHTINGALEHOSPICECAREOFTEXAS'),('OLIVETREEHOSPICE'),('ORIGINSHOSPICE'),('PINEHOSPICE'),('PINNACLEHOSPICESERVICES'),('PRIDEHOSPICECARE'),('REDWOODHOSPICE'),('ROWANHOSPICE'),('SIGNATUREHOSPICEPALLIATIVECARE'),('SOUTHERNSKYHOSPICE'),('SPECIALTYHOSPICE'),('SPRUCEHOSPICE'),('SYCAMOREHOSPICE'),('TEXASHEALTHCARESOLUTIONS'),('TEXASHEROESHOSPICE'),('TIMELESSMOMENTSHOSPICE'),('TREASUREDMOMENTSHOSPICE'),('WESLEYHEALTHCARE'),('WILLOWTREEHOSPICE'),('WILMINGTONHOSPICE'),('YELLOWROSEHOSPICECARE')),
ppp as (select 'PPP' src, BORROWER_NAME nm, BORROWER_CITY city, DATE_APPROVED dt, CURRENT_APPROVAL_AMOUNT amt, JOBS_REPORTED jobs,
   regexp_replace(regexp_replace(upper(BORROWER_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP where BORROWER_STATE='TX'
  union all
  select 'PPP150K', BORROWERNAME, BORROWERCITY, DATEAPPROVED, CURRENTAPPROVALAMOUNT, JOBSREPORTED,
   regexp_replace(regexp_replace(upper(BORROWERNAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','')
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE='TX'),
usa as (select 'USASPENDING' src, RECIPIENT_NAME nm, RECIPIENT_CITY_NAME city, min(ACTION_DATE) dt, sum(FEDERAL_ACTION_OBLIGATION) amt, listagg(distinct CFDA_NUMBER, ',') jobs,
   regexp_replace(regexp_replace(upper(RECIPIENT_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE='TX' and (RECIPIENT_NAME ilike '%HOSPICE%' or RECIPIENT_NAME ilike '%CFHC%' or RECIPIENT_NAME ilike '%HEALTH%')
  group by 1,2,3,7)
select src, nm, city, dt, amt, jobs from ppp where nk in (select nk from k)
union all
select src, nm, city, dt::string, amt, jobs from usa where nk in (select nk from k)
order by 1,2
;

-- [s10] statement 12
-- (rerun 2: Snowflake string needs \b for a regex word boundary; rerun 1: 150K table uses unseparated column names) federal money by name: PPP loans (both tables) and USAspending assistance to Texas recipients whose normalized name equals a cluster legal/brand name (83 keys); city shown for the second-field check
with k(nk) as (select * from values ('ABIBHOSPICECARE'),('ABOVEBEYONDHOSPICE'),('ACACIAHOSPICE'),('ADVANCEDHOLISTICPALLIATIVECARE'),('ALDERHOSPICE'),('ALLFAITHHOSPICECARE'),('ALTAVITAHOSPICE'),('AMAZINGLYGRACEHOSPICE'),('ANCHOREDBYGRACEHOSPICECARE'),('ARIELHOSPICE'),('ARMSOFCOMPASSIONHOSPICECARE'),('ASHHOSPICE'),('BALSAMHOSPICE'),('BEXARHOSPICE'),('BIRCHHOSPICE'),('BLUEROSEHOSPICEANDPALLIATIVECARE'),('BRIGHTLIGHTINFUSIONHHANDPALLIATIVECARE'),('BUTTERFLYHOSPICEPALLATIVECARE'),('CELESTIALHOSPICE'),('CFHCNO12'),('CFHCNO13'),('CFHCNO14'),('CFHCNO15'),('CFHCNO17'),('CFHCNO18'),('CFHCNO19'),('CFHCNO20'),('CFHCNO21'),('CFHCNO22'),('CFHCNO23'),('CFHCNO4'),('CFHCNO7'),('CHARTERHEALTHCAREOFSANANTONIO'),('CHESTNUTHOSPICE'),('COMMUNITYFIRSTHOSPICECAREOFSANANTONIO'),('COMPASSIONHOSPICEOFTEXAS'),('CYPRESSHOSPICE'),('DISTINGUISHEDHOSPICE'),('DIVINECOMFORTCAREHOSPICE'),('DIVINEENCOUNTERHOSPICE'),('ELMHOSPICE'),('EVERGREENHOSPICE'),('FAMILYFIRSTHOSPICE'),('FOURPILLARSHOSPICE'),('GENISAHOSPICEINTEGRATIVECARE'),('HARMONYHOSPICE'),('HARMONYHOSPICECARE'),('HARRISCOUNTYHOSPICE'),('HEARTSOULHOSPICE'),('HFCHNO4'),('HICKORYHOSPICE'),('HONEYBEEHOSPICE'),('HOUSTONFIRSTHOSPICEANDPALLIATIVECARE'),('JP2DHEALTHSYSTEMS'),('JUNIPERHOSPICE'),('LOVINGHANDSHOSPICE'),('LOVINGTOUCHHOSPICE'),('MAPLEHOSPICE'),('MIDTOWNHOSPICE'),('NESTHOMEHOSPICE'),('NESTHOMEHOSPICEANDPALLIATIVECARE'),('NEWDAWNHOSPICE'),('NIGHTINGALEHOSPICECAREOFTEXAS'),('OLIVETREEHOSPICE'),('ORIGINSHOSPICE'),('PINEHOSPICE'),('PINNACLEHOSPICESERVICES'),('PRIDEHOSPICECARE'),('REDWOODHOSPICE'),('ROWANHOSPICE'),('SIGNATUREHOSPICEPALLIATIVECARE'),('SOUTHERNSKYHOSPICE'),('SPECIALTYHOSPICE'),('SPRUCEHOSPICE'),('SYCAMOREHOSPICE'),('TEXASHEALTHCARESOLUTIONS'),('TEXASHEROESHOSPICE'),('TIMELESSMOMENTSHOSPICE'),('TREASUREDMOMENTSHOSPICE'),('WESLEYHEALTHCARE'),('WILLOWTREEHOSPICE'),('WILMINGTONHOSPICE'),('YELLOWROSEHOSPICECARE')),
ppp as (select 'PPP' src, BORROWER_NAME nm, BORROWER_CITY city, DATE_APPROVED dt, CURRENT_APPROVAL_AMOUNT amt, JOBS_REPORTED jobs,
   regexp_replace(regexp_replace(upper(BORROWER_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP where BORROWER_STATE='TX'
  union all
  select 'PPP150K', BORROWERNAME, BORROWERCITY, DATEAPPROVED, CURRENTAPPROVALAMOUNT, JOBSREPORTED,
   regexp_replace(regexp_replace(upper(BORROWERNAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','')
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE='TX'),
usa as (select 'USASPENDING' src, RECIPIENT_NAME nm, RECIPIENT_CITY_NAME city, min(ACTION_DATE) dt, sum(FEDERAL_ACTION_OBLIGATION) amt, listagg(distinct CFDA_NUMBER, ',') jobs,
   regexp_replace(regexp_replace(upper(RECIPIENT_NAME),'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE='TX' and (RECIPIENT_NAME ilike '%HOSPICE%' or RECIPIENT_NAME ilike '%CFHC%' or RECIPIENT_NAME ilike '%HEALTH%')
  group by 1,2,3,7)
select src, nm, city, dt, amt, jobs from ppp where nk in (select nk from k)
union all
select src, nm, city, dt::string, amt, jobs from usa where nk in (select nk from k)
union all
select 'CONTROL ppp TX hospice-named rows', null, null, null, count(*), null from ppp where nm ilike '%HOSPICE%'
union all
select 'CONTROL usaspending TX hospice-named recipients', null, null, null, count(*), null from usa where nm ilike '%HOSPICE%'
order by 1,2
;

-- [s10] statement 13
-- (rerun 2: Snowflake string needs \\b for a regex word boundary; rerun 1: 150K table uses unseparated column names) federal money by name: PPP loans (both tables) and USAspending assistance to Texas recipients whose normalized name equals a cluster legal/brand name (83 keys); city shown for the second-field check
with k(nk) as (select * from values ('ABIBHOSPICECARE'),('ABOVEBEYONDHOSPICE'),('ACACIAHOSPICE'),('ADVANCEDHOLISTICPALLIATIVECARE'),('ALDERHOSPICE'),('ALLFAITHHOSPICECARE'),('ALTAVITAHOSPICE'),('AMAZINGLYGRACEHOSPICE'),('ANCHOREDBYGRACEHOSPICECARE'),('ARIELHOSPICE'),('ARMSOFCOMPASSIONHOSPICECARE'),('ASHHOSPICE'),('BALSAMHOSPICE'),('BEXARHOSPICE'),('BIRCHHOSPICE'),('BLUEROSEHOSPICEANDPALLIATIVECARE'),('BRIGHTLIGHTINFUSIONHHANDPALLIATIVECARE'),('BUTTERFLYHOSPICEPALLATIVECARE'),('CELESTIALHOSPICE'),('CFHCNO12'),('CFHCNO13'),('CFHCNO14'),('CFHCNO15'),('CFHCNO17'),('CFHCNO18'),('CFHCNO19'),('CFHCNO20'),('CFHCNO21'),('CFHCNO22'),('CFHCNO23'),('CFHCNO4'),('CFHCNO7'),('CHARTERHEALTHCAREOFSANANTONIO'),('CHESTNUTHOSPICE'),('COMMUNITYFIRSTHOSPICECAREOFSANANTONIO'),('COMPASSIONHOSPICEOFTEXAS'),('CYPRESSHOSPICE'),('DISTINGUISHEDHOSPICE'),('DIVINECOMFORTCAREHOSPICE'),('DIVINEENCOUNTERHOSPICE'),('ELMHOSPICE'),('EVERGREENHOSPICE'),('FAMILYFIRSTHOSPICE'),('FOURPILLARSHOSPICE'),('GENISAHOSPICEINTEGRATIVECARE'),('HARMONYHOSPICE'),('HARMONYHOSPICECARE'),('HARRISCOUNTYHOSPICE'),('HEARTSOULHOSPICE'),('HFCHNO4'),('HICKORYHOSPICE'),('HONEYBEEHOSPICE'),('HOUSTONFIRSTHOSPICEANDPALLIATIVECARE'),('JP2DHEALTHSYSTEMS'),('JUNIPERHOSPICE'),('LOVINGHANDSHOSPICE'),('LOVINGTOUCHHOSPICE'),('MAPLEHOSPICE'),('MIDTOWNHOSPICE'),('NESTHOMEHOSPICE'),('NESTHOMEHOSPICEANDPALLIATIVECARE'),('NEWDAWNHOSPICE'),('NIGHTINGALEHOSPICECAREOFTEXAS'),('OLIVETREEHOSPICE'),('ORIGINSHOSPICE'),('PINEHOSPICE'),('PINNACLEHOSPICESERVICES'),('PRIDEHOSPICECARE'),('REDWOODHOSPICE'),('ROWANHOSPICE'),('SIGNATUREHOSPICEPALLIATIVECARE'),('SOUTHERNSKYHOSPICE'),('SPECIALTYHOSPICE'),('SPRUCEHOSPICE'),('SYCAMOREHOSPICE'),('TEXASHEALTHCARESOLUTIONS'),('TEXASHEROESHOSPICE'),('TIMELESSMOMENTSHOSPICE'),('TREASUREDMOMENTSHOSPICE'),('WESLEYHEALTHCARE'),('WILLOWTREEHOSPICE'),('WILMINGTONHOSPICE'),('YELLOWROSEHOSPICECARE')),
ppp as (select 'PPP' src, BORROWER_NAME nm, BORROWER_CITY city, DATE_APPROVED dt, CURRENT_APPROVAL_AMOUNT amt, JOBS_REPORTED jobs,
   regexp_replace(regexp_replace(upper(BORROWER_NAME),'\\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP where BORROWER_STATE='TX'
  union all
  select 'PPP150K', BORROWERNAME, BORROWERCITY, DATEAPPROVED, CURRENTAPPROVALAMOUNT, JOBSREPORTED,
   regexp_replace(regexp_replace(upper(BORROWERNAME),'\\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\\b',''),'[^A-Z0-9]','')
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE='TX'),
usa as (select 'USASPENDING' src, RECIPIENT_NAME nm, RECIPIENT_CITY_NAME city, min(ACTION_DATE) dt, sum(FEDERAL_ACTION_OBLIGATION) amt, listagg(distinct CFDA_NUMBER, ',') jobs,
   regexp_replace(regexp_replace(upper(RECIPIENT_NAME),'\\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE)\\b',''),'[^A-Z0-9]','') nk
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE='TX' and (RECIPIENT_NAME ilike '%HOSPICE%' or RECIPIENT_NAME ilike '%CFHC%' or RECIPIENT_NAME ilike '%HEALTH%')
  group by 1,2,3,7)
select src, nm, city, dt, amt, jobs from ppp where nk in (select nk from k)
union all
select src, nm, city, dt::string, amt, jobs from usa where nk in (select nk from k)
union all
select 'CONTROL ppp TX hospice-named rows', null, null, null, count(*), null from ppp where nm ilike '%HOSPICE%'
union all
select 'CONTROL usaspending TX hospice-named recipients', null, null, null, count(*), null from usa where nm ilike '%HOSPICE%'
order by 1,2
;

-- [s14] statement 14
-- NPPES, any taxonomy, any state: every organization NPI whose authorized official is one of the six core cluster officials (first+last), to see their footprint beyond hospice
select upper(trim(AUTHORIZED_OFFICIAL_FIRST_NAME))||' '||upper(trim(AUTHORIZED_OFFICIAL_LAST_NAME)) ao, NPI, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME lbn,
  HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tax1, PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a1, PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a2,
  PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME city, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st,
  regexp_replace(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER,'[^0-9]','') ph, PROVIDER_ENUMERATION_DATE enum_dt, NPI_DEACTIVATION_DATE deact, AUTHORIZED_OFFICIAL_TITLE_OR_POSITION title
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
where ENTITY_TYPE_CODE in ('2','2.0') and (upper(trim(AUTHORIZED_OFFICIAL_FIRST_NAME)), upper(trim(AUTHORIZED_OFFICIAL_LAST_NAME))) in
  (('BENJAMIN','ARISE'),('ADEBAYO','OSHINUGA'),('ADEJUMOKE','OSHINUGA'),('JENNIFER','ROY'),('TRACY','GLEASON'),('ANN','LOZANO'),('JOHN','PRICE'))
order by ao, enum_dt
;

-- [s15] statement 15
-- Medicare owner files (home health owners mart, SNF ownership landing): any individual owner whose first+last name equals one of the 29 cluster officials, or any organization owner named like a cluster entity; agency state shown for the second-field check
with ao(f,l) as (select * from values ('ADEBAYO','OSHINUGA'),('ADEJUMOKE','OSHINUGA'),('ALFRED','PEREZ'),('AMY','GARCIA'),('ANN','LOZANO'),('ARTURO','ELIZONDO'),('BENJAMIN','ARISE'),('CHARLES','ROY'),('DARRELL','ELLIOTT'),('FAYE','HORN'),('JAMES','GRISMORE'),('JASMINE','PEREZ'),('JENNIFER','ROY'),('JOHN','PRICE'),('KAYLA','VASQUEZ'),('KIMBERLEY','WINN'),('MARIA','RAMOS'),('MARK','MITCHELL'),('PATRICK','ILOANYA'),('RUBEN','MONTEZ'),('SEGUN','OGUNGBEMI'),('SHANNA','WURM'),('SHAPOUR','OLIA'),('STACY','SAIZ'),('SYLVIA','MUNIZ'),('SYLVIE','BOAL'),('THOMAS','OZGO'),('TRACY','GLEASON'),('YOLANDA','GARZA'))
select 'HHA' src, h.ORGANIZATION_NAME agency, h.CCN, h.AGENCY_STATE st, coalesce(h.FIRST_NAME_OWNER||' '||h.LAST_NAME_OWNER, h.ORGANIZATION_NAME_OWNER) owner, h.ROLE_TEXT_OWNER role, h.PERCENTAGE_OWNERSHIP pct, h.ASSOCIATION_DATE_OWNER dt, h.CITY_OWNER owner_city
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS h
where (upper(trim(h.FIRST_NAME_OWNER)), upper(trim(h.LAST_NAME_OWNER))) in (select f,l from ao)
   or h.ORGANIZATION_NAME_OWNER ilike any ('%CFHC%','%JP2D%','%TULIP HOSPICE%','%J ROY CONSULTING%','%OSHINUGA%','%WURZBACH%')
union all
select 'SNF', s.ORGANIZATION_NAME, null, s.STATE_OWNER, coalesce(s.FIRST_NAME_OWNER||' '||s.LAST_NAME_OWNER, s.ORGANIZATION_NAME_OWNER), s.ROLE_TEXT_OWNER, s.PERCENTAGE_OWNERSHIP::string, s.ASSOCIATION_DATE_OWNER, s.CITY_OWNER
from LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP s
where (upper(trim(s.FIRST_NAME_OWNER)), upper(trim(s.LAST_NAME_OWNER))) in (select f,l from ao)
   or s.ORGANIZATION_NAME_OWNER ilike any ('%CFHC%','%JP2D%','%TULIP HOSPICE%','%J ROY CONSULTING%','%OSHINUGA%')
order by 1, 5
;

-- [s15] statement 16
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
;

