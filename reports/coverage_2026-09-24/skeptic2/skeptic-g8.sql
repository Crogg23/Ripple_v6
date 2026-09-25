-- skeptic g8, round 2, 2026-09-24. Read-only. Python door, tag skeptic-r2-2026-09-24.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'skeptic-r2-2026-09-24'
-- Statements per lead: L1 RHC 8, L2 hospice 5, L3 NH deficiencies 10 (two were table-name lookups, two failed and were rerun).

-- [L1-1] RHC: columns
select table_name, listagg(column_name, ',') within group (order by ordinal_position) cols from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_schema='HEALTH' and table_name in ('HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS','HEALTH__FED_CMS_HOSPICE','HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES','HEALTH__FED_CMS_NURSING_HOME') group by 1
-- [L1-2] find POS tables that could carry RHC certification dates
select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%POS%' or table_name ilike '%PROVIDER_OF_SERVICE%' order by 1,2
;

-- [L1-3] POS_OTHER columns
select listagg(column_name, ',') within group (order by ordinal_position) cols from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_POS_OTHER'
;

-- [L1-4] POS_OTHER: RHC category and date formats sample
select PRVDR_CTGRY_CD, count(*) n, count(distinct CCN) ccns, min(CRTFCTN_DT) min_cert, max(CRTFCTN_DT) max_cert, min(ORGNL_PRTCPTN_DT) min_orig, max(ORGNL_PRTCPTN_DT) max_orig, count_if(CHOW_CNT::varchar not in ('0','00','')) chow_nonzero, max(CHOW_DT) max_chow, count_if(nullif(trim(PGM_TRMNTN_CD::varchar),'') in ('00','0')) active
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER group by 1 order by 2 desc
;

-- [L1-5] RHC: enrollment-ID year vs POS original participation date and CHOW date, split for-profit
with r as (
  select lpad(trim(CCN),6,'0') ccn, PROPRIETARY_NONPROFIT pn, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') edt,
    case when try_to_number(substr(CCN,3,4)) between 3800 and 3974 or try_to_number(substr(CCN,3,4)) between 8900 and 8999 then 'FS' else 'PB/OT' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS),
p as (select lpad(trim(CCN),6,'0') ccn, max(try_to_date(ORGNL_PRTCPTN_DT::varchar)) orig, max(try_to_date(CRTFCTN_DT::varchar)) cert, max(try_to_date(CHOW_DT::varchar)) chow, max(try_to_number(CHOW_CNT::varchar)) chowc
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='12' group by 1)
select year(edt) ey, count(*) n, count(p.ccn) in_pos, count_if(pn='P') fp,
  count_if(year(p.orig) = year(edt) or year(p.orig) = year(edt)+1 or (year(p.orig)=year(edt)-1)) orig_within_1y,
  count_if(p.orig < dateadd(year,-2,edt)) orig_2y_before,
  count_if(p.chow between dateadd(day,-365,edt) and dateadd(day,365,edt)) chow_near_enr,
  count_if(pn='P' and p.orig < dateadd(year,-2,edt)) fp_old_clinic,
  count_if(pn='P' and year(p.orig) = year(edt)) fp_orig_same_year,
  count_if(pn='P' and p.chow between dateadd(day,-365,edt) and dateadd(day,365,edt)) fp_chow_near,
  count_if(pn='P' and cls='FS' and (p.orig >= dateadd(year,-1,edt))) fp_fs_truly_new
from r left join p on p.ccn = r.ccn where year(edt) between 2016 and 2025 group by 1 order by 1
;

-- [L1-6] POS RHC (includes terminated clinics): new clinics by original participation year, freestanding vs provider-based, still active, control type
with p as (select lpad(trim(CCN),6,'0') ccn, try_to_date(ORGNL_PRTCPTN_DT::varchar) orig, PGM_TRMNTN_CD t, GNRL_CNTL_TYPE_CD g, PRVDR_BSD_FAC_SW pbsw,
    case when try_to_number(substr(CCN,3,4)) between 3400 and 3499 or try_to_number(substr(CCN,3,4)) between 3975 and 3999 or try_to_number(substr(CCN,3,4)) between 8500 and 8899 then 'PB'
         when try_to_number(substr(CCN,3,4)) between 3800 and 3974 or try_to_number(substr(CCN,3,4)) between 8900 and 8999 then 'FS' else 'OT' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='12')
select year(orig) y, count(*) n, count_if(cls='PB') pb, count_if(cls='FS') fs, count_if(cls='OT') ot, count_if(t in ('00','0')) active_now,
  count_if(cls='PB' and t in ('00','0')) pb_active, count_if(cls='FS' and t in ('00','0')) fs_active, count_if(pbsw='Y') pbsw_y,
  listagg(distinct g, ',') ctl_codes
from p where year(orig) between 2016 and 2025 group by 1 order by 1
;

-- [L1-7] POS RHC: monthly new provider-based vs freestanding clinics 2020-07 to 2022-06 (grandfather rush test), all clinics incl. terminated
with p as (select try_to_date(ORGNL_PRTCPTN_DT::varchar) orig,
    case when try_to_number(substr(CCN,3,4)) between 3400 and 3499 or try_to_number(substr(CCN,3,4)) between 3975 and 3999 or try_to_number(substr(CCN,3,4)) between 8500 and 8899 then 'PB'
         when try_to_number(substr(CCN,3,4)) between 3800 and 3974 or try_to_number(substr(CCN,3,4)) between 8900 and 8999 then 'FS' else 'OT' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='12')
select to_char(orig,'YYYY-MM') m, count_if(cls='PB') pb, count_if(cls='FS') fs from p where orig between '2020-01-01' and '2022-06-30' group by 1 order by 1
;

-- [L1-8] RHC: Fast Pace in enrollment file and POS: counts, NPIs, CCNs, dates, CHOWs; plus denominator of for-profit freestanding since Jul 2021
with r as (
  select lpad(trim(CCN),6,'0') ccn, NPI, ORGANIZATION_NAME, DOING_BUSINESS_AS_NAME, PROPRIETARY_NONPROFIT pn, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') edt,
    case when try_to_number(substr(CCN,3,4)) between 3800 and 3974 or try_to_number(substr(CCN,3,4)) between 8900 and 8999 then 'FS' else 'NFS' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS),
p as (select lpad(trim(CCN),6,'0') ccn, max(try_to_date(ORGNL_PRTCPTN_DT::varchar)) orig, max(try_to_number(CHOW_CNT::varchar)) chowc, max(PGM_TRMNTN_CD) t
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='12' group by 1),
pfp as (select count(*) fp_fs_since from r where cls='FS' and pn='P' and edt >= '2021-07-01')
select (select fp_fs_since from pfp) fp_fs_since_jul21, count(*) rows_, count(distinct r.ccn) ccns, count(distinct NPI) npis, count_if(cls='FS' and pn='P') fs_fp, min(edt) min_enr, max(edt) max_enr,
  min(p.orig) min_orig, max(p.orig) max_orig, count_if(p.orig < '2021-07-01') orig_before_jul21, count_if(p.chowc > 0) with_chow, count_if(to_char(p.orig,'YYYY-MM')='2022-02') orig_feb22,
  count_if(r.ORGANIZATION_NAME not ilike 'FAST PACE%') via_dba_only, listagg(distinct r.ORGANIZATION_NAME, ' ; ') orgs
from r left join p on p.ccn = r.ccn where r.ORGANIZATION_NAME ilike 'FAST PACE%' or r.DOING_BUSINESS_AS_NAME ilike 'FAST PACE%'
;

-- [L2-3] find any table that could show hospice billing or revocation (name search)
select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_schema <> 'TIMELINE' and (table_name ilike '%HOSPICE%' or table_name ilike '%REVOC%' or table_name ilike '%PRECLUSION%' or table_name ilike '%OPT_OUT%') order by 1,2
;

-- [L2-1] HOSPICE: every row at the two Houston buildings or on the two phones, with enrollment-file owner fields
with h as (select CCN, FACILITY_NAME, ADDRESS_LINE_1, ADDRESS_LINE_2, CITY_TOWN, COUNTY_PARISH, TELEPHONE_NUMBER, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, OWNERSHIP_TYPE, CERTIFICATION_DATE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE
  where (STATE='TX' and (ADDRESS_LINE_1 ilike '7322 SOUTHWEST F%' or ADDRESS_LINE_1 ilike '2922 ROSEDALE%')) or regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') in ('7138741234','2814101013')),
e as (select CCN, max(ASSOCIATE_ID) assoc, max(ORGANIZATION_NAME) org, max(DOING_BUSINESS_AS_NAME) dba, max(INCORPORATION_DATE) inc, max(ADDRESS_LINE_1||' '||coalesce(ADDRESS_LINE_2,'')) eaddr, max(NPI) npi, count(*) n
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS group by 1)
select h.*, e.assoc, e.org, e.dba, e.inc, e.eaddr, e.npi from h left join e on e.CCN = h.CCN order by h.ADDRESS_LINE_1, h.CERTIFICATION_DATE
;

-- [L2-2] HOSPICE: every shared phone touching Harris County, with group size, names, blank-ownership count; plus national and Harris totals
with h as (select CCN, FACILITY_NAME, STATE, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, OWNERSHIP_TYPE, CERTIFICATION_DATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE),
p as (select ph, count(*) n from h where length(ph)=10 group by 1),
tot as (select count(*) us_n, count_if(p.n>=2) us_share, count_if(h.county='HARRIS' and h.STATE='TX') harris_n, count_if(h.county='HARRIS' and h.STATE='TX' and p.n>=2) harris_share,
   count_if(nullif(trim(h.OWNERSHIP_TYPE),'') is null) us_blank_own, count_if(h.county='HARRIS' and h.STATE='TX' and nullif(trim(h.OWNERSHIP_TYPE),'') is null) harris_blank_own
   from h left join p on p.ph=h.ph)
select tot.*, h.ph, p.n grp_size, count_if(h.county='HARRIS') in_harris, min(CERTIFICATION_DATE) c0, max(CERTIFICATION_DATE) c1, left(listagg(FACILITY_NAME||'('||h.STATE||')', '; '),300) names
from h join p on p.ph=h.ph and p.n>=2 cross join tot
where h.ph in (select ph from h where county='HARRIS' and STATE='TX')
group by all order by grp_size desc
;

-- [L2-4] HOSPICE: certified roster rows with no Medicare enrollment row, Harris vs rest, by blank ownership and cert year 2022+
with h as (select CCN, STATE, upper(trim(COUNTY_PARISH)) county, nullif(trim(OWNERSHIP_TYPE),'') own, CERTIFICATION_DATE cd from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE),
e as (select distinct CCN from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS)
select iff(county='HARRIS' and STATE='TX','HARRIS', iff(STATE in ('CA','NV','AZ','TX'),'CA/NV/AZ/TX other','REST')) area, count(*) n, count(e.CCN) enrolled,
  count_if(own is null) blank_own, count_if(own is null and e.CCN is null) blank_and_unenrolled, count_if(own is not null and e.CCN is null) owned_unenrolled,
  count_if(cd >= '2022-01-01') cert22, count_if(cd >= '2022-01-01' and e.CCN is null) cert22_unenrolled
from h left join e on e.CCN=h.CCN group by 1 order by 1
;

-- [L2-5] HOSPICE: hospices sharing a phone with a DIFFERENT brand (first 6 letters of name differ), by area; filler 9090000000 excluded
with h as (select CCN, STATE, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, left(regexp_replace(upper(FACILITY_NAME),'[^A-Z]',''),6) b from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE),
p as (select ph, count(*) n, count(distinct b) nb from h where length(ph)=10 and ph <> '9090000000' group by 1)
select iff(county='HARRIS' and STATE='TX','HARRIS TX', iff(county='BEXAR' and STATE='TX','BEXAR TX', iff(county='LOS ANGELES' and STATE='CA','LA CA', iff(county='CLARK' and STATE='NV','CLARK NV','ALL OTHER')))) area,
  count(*) n, count_if(p.n>=2) share_phone, count_if(p.n>=2 and p.nb>=2) share_with_other_brand, round(100*count_if(p.n>=2 and p.nb>=2)/count(*),1) pct_other_brand
from h left join p on p.ph=h.ph group by rollup(1) order by 2 desc
;

-- [L3-1] NH DEFICIENCIES: duplicate test on the whole file (same home, survey date, tag, severity) and processing-date vintages
select count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN, SURVEY_DATE, DEFICIENCY_TAG_NUMBER, SCOPE_SEVERITY_CODE) distinct_key,
  count(distinct CMS_CERTIFICATION_NUMBER_CCN, SURVEY_DATE, DEFICIENCY_TAG_NUMBER, SCOPE_SEVERITY_CODE, SURVEY_TYPE) distinct_key_type,
  count(distinct PROCESSING_DATE) vintages, min(PROCESSING_DATE) p0, max(PROCESSING_DATE) p1, listagg(distinct SURVEY_TYPE, ',') survey_types, listagg(distinct INSPECTION_CYCLE, ',') cycles
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
-- [L3-2] NH: every chain label containing RELIANT, with chain IDs, home counts, states, facility count field
select CHAIN_ID, CHAIN_NAME, count(*) homes, listagg(distinct STATE, ',') states, max(NUMBER_OF_FACILITIES_IN_CHAIN) fac_field, sum(NUMBER_OF_CERTIFIED_BEDS) beds, count_if(SPECIAL_FOCUS_STATUS is not null and trim(SPECIAL_FOCUS_STATUS)<>'') sff, count_if(ABUSE_ICON='Y') abuse, avg(OVERALL_RATING) avg_star, listagg(distinct OWNERSHIP_TYPE, ',') own
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_NAME ilike '%RELIANT%' or LEGAL_BUSINESS_NAME ilike '%RELIANT%' group by 1,2
;

-- [L3-3 rerun, CHAIN_ID is text] NH: Reliant per home since 2023-06-17: beds, harm (G-L) and J-L citations, survey dates, complaint vs standard harm, SFF status, first-approved date
with d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) g, count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl,
    count(distinct SURVEY_DATE) surveys, count(distinct iff(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L'), SURVEY_DATE, null)) gsurv,
    count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L') and COMPLAINT_DEFICIENCY='Y') g_compl, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L') and STANDARD_DEFICIENCY='Y') g_std,
    max(iff(SCOPE_SEVERITY_CODE in ('J','K','L'), SURVEY_DATE, null)) last_ij
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17' group by 1)
select n.PROVIDER_NAME, n.CITY, n.STATE, n.NUMBER_OF_CERTIFIED_BEDS beds, n.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY res, n.SPECIAL_FOCUS_STATUS sff, n.DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES first_appr,
  coalesce(d.g,0) g, coalesce(d.jkl,0) jkl, d.surveys, d.gsurv, d.g_compl, d.g_std, d.last_ij, sum(coalesce(d.g,0)) over () tot_g, sum(coalesce(d.jkl,0)) over () tot_jkl
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n left join d on d.ccn = lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0') where n.CHAIN_ID = '446' order by g desc
;

-- [L3-5] find SNF enrollment and owner tables and their key columns
select table_catalog, table_schema, table_name, listagg(column_name, ',') within group (order by ordinal_position) cols from LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS where table_schema='LANDING' and table_name in ('FED_CMS_SNF_OWNERSHIP','FED_CMS_SNF_ENROLLMENTS') group by 1,2,3
;

-- [L3-6] Reliant homes: owner association dates for any owner whose name contains RELIANT, via SNF enrollment (CCN -> ENROLLMENT_ID)
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID, INCORPORATION_DATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SNF_ENROLLMENTS)
select rel.PROVIDER_NAME, en.INCORPORATION_DATE, o.ORGANIZATION_NAME_OWNER, o.ROLE_TEXT_OWNER, o.ASSOCIATION_DATE_OWNER, o.MANAGEMENT_SERVICES_COMPANY_OWNER
from rel left join en on en.ccn=rel.ccn left join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID and (o.ORGANIZATION_NAME_OWNER ilike '%RELIANT%')
order by o.ASSOCIATION_DATE_OWNER desc nulls first
;

-- [L3-7] locate the SNF enrollment table
select table_catalog, table_schema, table_name from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%SNF%ENROLL%' union all select table_catalog, table_schema, table_name from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike '%SNF%ENROLL%'
;

-- [L3-8] locate skilled-nursing enrollment table (broader name search)
select table_catalog, table_schema, table_name from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_schema<>'TIMELINE' and (table_name ilike '%SKILLED%' or table_name ilike '%NURSING%ENROLL%' or table_name ilike '%SNF%') union all select table_catalog, table_schema, table_name from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike '%SKILLED%' or table_name ilike '%SNF%'
;

-- [L3-9 rerun of L3-6 on the right table name] Reliant homes: owner association dates for any owner whose name contains RELIANT, via SNF enrollment (CCN -> ENROLLMENT_ID)
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID, INCORPORATION_DATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS)
select rel.PROVIDER_NAME, en.INCORPORATION_DATE, o.ORGANIZATION_NAME_OWNER, o.ROLE_TEXT_OWNER, o.ASSOCIATION_DATE_OWNER, o.MANAGEMENT_SERVICES_COMPANY_OWNER
from rel left join en on en.ccn=rel.ccn left join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID and (o.ORGANIZATION_NAME_OWNER ilike '%RELIANT%')
order by o.ASSOCIATION_DATE_OWNER desc nulls first
;

-- [L3-10] Reliant: harm citations since 2023-06-17 split by before/after the home's earliest Reliant ownership-or-control date (ADP role excluded)
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, STATE, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER, 'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
      where o.ORGANIZATION_NAME_OWNER ilike '%RELIANT%' and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
      where SURVEY_DATE >= '2023-06-17' and SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L'))
select count(distinct rel.ccn) homes, count(distinct j.ccn) homes_with_reliant_date, count_if(j.rel_from > '2023-06-17') homes_joined_in_window,
  count(d.ccn) harm_all, count_if(d.SURVEY_DATE >= j.rel_from) harm_after_reliant, count_if(d.SURVEY_DATE < j.rel_from) harm_before_reliant, count_if(d.ccn is not null and j.rel_from is null) harm_no_date,
  count_if(d.sev in ('J','K','L') and d.SURVEY_DATE >= j.rel_from) jkl_after
from rel left join j on j.ccn=rel.ccn left join d on d.ccn=rel.ccn
;
