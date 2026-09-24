-- deep-7 round 2 (coverage-r2-2026-09-24). Read-only. Numbered as run.
-- Every connection (5 in all) first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'coverage-r2-2026-09-24'. Those 10 lines are not counted in the 24.

-- [1] FARA: row count per stacked file, with fill counts for the key columns
select SOURCE_FILE, count(*) n,
  count_if(nullif(trim(FOREIGN_PRINCIPAL),'') is not null) fp_filled,
  count_if(nullif(trim(FOREIGN_PRINCIPAL_COUNTRY),'') is not null) fpc_filled,
  count_if(nullif(trim(COUNTRY_LOCATION_REPRESENTED),'') is not null) clr_filled,
  count_if(nullif(trim(SHORT_FORM_LAST_NAME),'') is not null) sf_filled,
  count_if(nullif(trim(REGISTRATION_NUMBER),'') is not null) regno_filled,
  count(distinct REGISTRATION_NUMBER) regnos,
  min(coalesce(FOREIGN_PRINCIPAL_REGISTRATION_DATE, SHORT_FORM_DATE, REGISTRANT_DATE, DATE)) mindt,
  max(coalesce(FOREIGN_PRINCIPAL_REGISTRATION_DATE, SHORT_FORM_DATE, REGISTRANT_DATE, DATE)) maxdt,
  sum(count(*)) over () total_rows
from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK group by 1 order by 2 desc;

-- [2] HOSPICE: total rows plus a 5-row sample
select count(*) over () total_rows, * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE limit 5;

-- [3] HOSPITAL_COMPARE: total rows plus a 5-row sample
select count(*) over () total_rows, * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_COMPARE limit 5;

-- [4] NH DEFICIENCIES: total rows plus a 5-row sample
select count(*) over () total_rows, * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES limit 5;

-- [5] RHC: total rows plus a 5-row sample
select count(*) over () total_rows, * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS limit 5;

-- [6] FARA: read the active flags in the foreign-principal file before filtering on them
select IS_ACTIVE_FOREIGN_PRINCIPAL, IS_ACTIVE_REGISTRATION, count(*) n, count(distinct REGISTRATION_NUMBER) registrants,
  count(distinct COUNTRY_LOCATION_REPRESENTED) countries, min(FOREIGN_PRINCIPAL_REGISTRATION_DATE) min_dt, max(FOREIGN_PRINCIPAL_REGISTRATION_DATE) max_dt,
  count_if(FOREIGN_PRINCIPAL_TERMINATION_DATE is null) no_term_date
from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK
where SOURCE_FILE = 'FARA_All_ForeignPrincipals.csv' group by 1,2 order by 3 desc;

-- [7] FARA: countries by distinct US registrants, all time, by decade of the principal's registration, and active now
select COUNTRY_LOCATION_REPRESENTED country, count(*) fp_rows, count(distinct REGISTRATION_NUMBER) registrants_all,
  count(distinct iff(year(try_to_date(FOREIGN_PRINCIPAL_REGISTRATION_DATE::varchar)) < 1990, REGISTRATION_NUMBER, null)) pre1990,
  count(distinct iff(year(try_to_date(FOREIGN_PRINCIPAL_REGISTRATION_DATE::varchar)) between 1990 and 2009, REGISTRATION_NUMBER, null)) r1990_2009,
  count(distinct iff(year(try_to_date(FOREIGN_PRINCIPAL_REGISTRATION_DATE::varchar)) between 2010 and 2016, REGISTRATION_NUMBER, null)) r2010_2016,
  count(distinct iff(year(try_to_date(FOREIGN_PRINCIPAL_REGISTRATION_DATE::varchar)) >= 2017, REGISTRATION_NUMBER, null)) r2017_on,
  count(distinct iff(IS_ACTIVE_FOREIGN_PRINCIPAL::varchar in ('true','TRUE','True','Y','1'), REGISTRATION_NUMBER, null)) active_registrants
from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK
where SOURCE_FILE = 'FARA_All_ForeignPrincipals.csv' group by 1 order by r2017_on desc limit 25;

-- [8] FARA: registrants carrying the most foreign principals, with how many countries and how many still active
with fp as (
  select REGISTRATION_NUMBER, max(REGISTRANT_NAME) fp_regname, count(*) fps, count(distinct COUNTRY_LOCATION_REPRESENTED) countries,
    count_if(IS_ACTIVE_FOREIGN_PRINCIPAL::varchar in ('true','TRUE','True','Y','1')) active_fps,
    listagg(distinct iff(IS_ACTIVE_FOREIGN_PRINCIPAL::varchar in ('true','TRUE','True','Y','1'), COUNTRY_LOCATION_REPRESENTED, null), '; ') within group (order by iff(IS_ACTIVE_FOREIGN_PRINCIPAL::varchar in ('true','TRUE','True','Y','1'), COUNTRY_LOCATION_REPRESENTED, null)) active_countries
  from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_ForeignPrincipals.csv' group by 1),
reg as (select REGISTRATION_NUMBER, max(REGISTRANT_NAME) regname, max(STATE) st from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_Registrants.csv' group by 1)
select fp.REGISTRATION_NUMBER, coalesce(reg.regname, fp.fp_regname) registrant, reg.st, fp.fps, fp.countries, fp.active_fps, left(fp.active_countries, 160) active_countries
from fp left join reg on reg.REGISTRATION_NUMBER = fp.REGISTRATION_NUMBER order by active_fps desc, fps desc limit 20;

-- [9] FARA: join short-form agents to Congress legislators by first+last name, short form filed after the member's last term ended
with leg as (
  select upper(trim(NAME_FIRST)) f, upper(trim(NAME_LAST)) l, count(distinct BIOGUIDE) n_bio, max(BIOGUIDE) bio, max(NAME_OFFICIAL_FULL) fullname,
    max(PARTY) party, max(STATE) st, max(TERM_TYPE) ttype, max(try_to_date(TERM_END::varchar)) last_end, max(try_to_date(BIRTHDAY::varchar)) bday
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS group by 1,2),
sf as (
  select upper(trim(SHORT_FORM_FIRST_NAME)) f, upper(trim(SHORT_FORM_LAST_NAME)) l, REGISTRATION_NUMBER, max(REGISTRANT_NAME) regname_sf,
    min(try_to_date(SHORT_FORM_DATE::varchar)) sfd, max(try_to_date(SHORT_FORM_TERMINATION_DATE::varchar)) sfend
  from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_ShortForms.csv' group by 1,2,3),
reg as (select REGISTRATION_NUMBER, max(REGISTRANT_NAME) regname from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_Registrants.csv' group by 1),
fpc as (select REGISTRATION_NUMBER, listagg(distinct COUNTRY_LOCATION_REPRESENTED, '; ') within group (order by COUNTRY_LOCATION_REPRESENTED) ctry from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_ForeignPrincipals.csv' group by 1)
select count(*) over () matched_pairs, count_if(sf.sfd > leg.last_end) over () after_term_pairs,
  leg.fullname, leg.bio, leg.n_bio, leg.party, leg.st, leg.ttype, leg.last_end, leg.bday, sf.sfd, sf.sfend, sf.REGISTRATION_NUMBER, coalesce(reg.regname, sf.regname_sf) registrant, left(fpc.ctry, 120) countries
from sf join leg on leg.f = sf.f and leg.l = sf.l
left join reg on reg.REGISTRATION_NUMBER = sf.REGISTRATION_NUMBER left join fpc on fpc.REGISTRATION_NUMBER = sf.REGISTRATION_NUMBER
where leg.last_end >= '1970-01-01'
order by (sf.sfd > leg.last_end) desc, sf.sfd desc limit 80;

-- [10] FARA: registrant names for the top firms (which column holds the name in the registrants file)
select REGISTRATION_NUMBER, max(PERSON_NAME) person_name_col, max(REGISTRANT_NAME) registrant_name_col, max(COMPANY_ID) company_id_col, max(STATE) st, max(REGISTRANT_DATE) reg_dt, max(TERMINATION_DATE) term_dt
from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK
where SOURCE_FILE = 'FARA_All_Registrants.csv' and REGISTRATION_NUMBER in ('6170','6200','6492','5430','6399','7545','6549','3492','5870','2165','1750','5712','7070','7404','7542','7562','7543','7555','6377','5937','3028','3712','5852','6344','6415','5928','2244','3718','3634')
group by 1 order by 1;

-- [11] FARA: ex-members of Congress (name unique among legislators, term ended 1970+) with a short form filed after they left, one row per person
with leg as (
  select upper(trim(NAME_FIRST)) f, upper(trim(NAME_LAST)) l, count(distinct BIOGUIDE) n_bio, max(BIOGUIDE) bio, max(PARTY) party, max(STATE) st, max(TERM_TYPE) ttype,
    max(try_to_date(TERM_END::varchar)) last_end
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS group by 1,2),
sf as (
  select upper(trim(SHORT_FORM_FIRST_NAME)) f, upper(trim(SHORT_FORM_LAST_NAME)) l, REGISTRATION_NUMBER, min(try_to_date(SHORT_FORM_DATE::varchar)) sfd
  from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_ShortForms.csv' group by 1,2,3),
reg as (select REGISTRATION_NUMBER, max(PERSON_NAME) regname from LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK where SOURCE_FILE = 'FARA_All_Registrants.csv' group by 1),
m as (select leg.*, sf.sfd, sf.REGISTRATION_NUMBER, reg.regname from sf join leg on leg.f = sf.f and leg.l = sf.l left join reg on reg.REGISTRATION_NUMBER = sf.REGISTRATION_NUMBER
      where leg.n_bio = 1 and leg.last_end >= '1970-01-01' and sf.sfd > leg.last_end)
select count(*) over () people, count_if(min(sfd) >= '2017-01-01') over () people_first_2017_on, count_if(max(sfd) >= '2025-01-01') over () people_filed_2025_on,
  f || ' ' || l person, bio, max(party) party, max(st) st, max(ttype) ttype, max(last_end) left_office, min(sfd) first_sf, max(sfd) last_sf, count(distinct REGISTRATION_NUMBER) firms,
  left(listagg(distinct regname, '; '), 150) registrants
from m group by f, l, bio order by last_sf desc limit 70;

-- [12] HOSPICE: by county, certification year buckets, shared phone and shared street address (peers side by side)
with h as (
  select CCN, STATE, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER, '[^0-9]', '') ph,
    upper(regexp_replace(trim(ADDRESS_LINE_1), '[^A-Za-z0-9]', '')) || '|' || left(ZIP_CODE, 5) addr, year(CERTIFICATION_DATE) cy, OWNERSHIP_TYPE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE),
p as (select ph, count(*) n from h where length(ph) = 10 group by 1),
a as (select addr, count(*) n from h group by 1)
select iff(grouping(h.STATE) = 1, 'ALL US', h.STATE || ' / ' || coalesce(h.county, '?')) area, count(*) hospices,
  count_if(cy < 2019) cert_pre2019, count_if(cy between 2019 and 2021) cert_2019_21, count_if(cy between 2022 and 2023) cert_2022_23, count_if(cy >= 2024) cert_2024_on,
  count_if(p.n >= 2) shares_phone, count_if(p.n >= 3) phone_3plus, count_if(a.n >= 2) shares_addr, count_if(OWNERSHIP_TYPE ilike '%profit%' and OWNERSHIP_TYPE not ilike '%non%') for_profit
from h left join p on p.ph = h.ph left join a on a.addr = h.addr
group by grouping sets ((h.STATE, h.county), ()) order by hospices desc limit 22;

-- [13] HOSPICE: the phone numbers shared by 3 or more certified hospices, with how many different street addresses sit behind each
with h as (
  select CCN, FACILITY_NAME, STATE, CITY_TOWN, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER, '[^0-9]', '') ph,
    upper(regexp_replace(trim(ADDRESS_LINE_1), '[^A-Za-z0-9]', '')) || '|' || left(ZIP_CODE, 5) addr, CERTIFICATION_DATE, OWNERSHIP_TYPE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE)
select ph, count(*) hospices, count(distinct addr) addresses, count(distinct CITY_TOWN) cities, listagg(distinct STATE, ',') states, max(county) county,
  min(CERTIFICATION_DATE) first_cert, max(CERTIFICATION_DATE) last_cert, count_if(year(CERTIFICATION_DATE) >= 2019) cert_2019_on,
  listagg(distinct OWNERSHIP_TYPE, ',') own, left(listagg(distinct FACILITY_NAME, ' ; '), 220) names,
  count(*) over () phones_3plus, sum(count(*)) over () hospices_on_them
from h where length(ph) = 10 group by ph having count(*) >= 3 order by hospices desc, addresses desc limit 40;

-- [14] HOSPICE: the shared-phone clusters joined by CCN to Medicare hospice enrollments for owner ID and incorporation date, plus the CCN land rate
with h as (
  select CCN, FACILITY_NAME, ADDRESS_LINE_1, CITY_TOWN, STATE, CERTIFICATION_DATE, regexp_replace(TELEPHONE_NUMBER, '[^0-9]', '') ph
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE),
e as (select CCN, max(ASSOCIATE_ID) assoc, max(ORGANIZATION_NAME) org, max(INCORPORATION_DATE) inc, max(INCORPORATION_STATE) inc_st, count(*) enr
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS group by 1),
lr as (select count(*) hospices, count(e.CCN) landed from h left join e on e.CCN = h.CCN)
select lr.hospices, lr.landed, h.ph, h.CCN, h.FACILITY_NAME, h.ADDRESS_LINE_1, h.CITY_TOWN, h.STATE, h.CERTIFICATION_DATE, e.assoc, e.org, e.inc, e.inc_st
from h cross join lr left join e on e.CCN = h.CCN
where h.ph in ('7138741234','6235653922','2814101013','7136677202','8184706457','3235523300','8186360941','3238211419')
order by h.ph, h.CERTIFICATION_DATE;

-- [15] RHC: enrollments by the date inside ENROLLMENT_ID (month for 2019-2021, year otherwise), split by CCN class and for-profit
with r as (
  select ENROLLMENT_ID, try_to_date(substr(ENROLLMENT_ID, 2, 8), 'YYYYMMDD') edt, PROPRIETARY_NONPROFIT pn,
    try_to_number(substr(CCN, 3, 4)) c4,
    case when try_to_number(substr(CCN, 3, 4)) between 3400 and 3499 or try_to_number(substr(CCN, 3, 4)) between 3975 and 3999 or try_to_number(substr(CCN, 3, 4)) between 8500 and 8899 then 'provider-based'
         when try_to_number(substr(CCN, 3, 4)) between 3800 and 3974 or try_to_number(substr(CCN, 3, 4)) between 8900 and 8999 then 'freestanding' else 'other' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS)
select iff(year(edt) between 2019 and 2021, to_char(edt, 'YYYY-MM'), to_char(year(edt))) period, count(*) n,
  count_if(cls = 'provider-based') provider_based, count_if(cls = 'freestanding') freestanding, count_if(cls = 'other') other_ccn,
  count_if(pn = 'P') for_profit, count_if(pn = 'N') nonprofit, count_if(pn not in ('P','N') or pn is null) pn_other
from r group by 1 order by 1;

-- [16] RHC: the top organization NPIs by clinic count, with legal name, states, class, for-profit flag, enrollment window and multi-NPI flag
with r as (
  select *, try_to_date(substr(ENROLLMENT_ID, 2, 8), 'YYYYMMDD') edt,
    case when try_to_number(substr(CCN, 3, 4)) between 3400 and 3499 or try_to_number(substr(CCN, 3, 4)) between 3975 and 3999 or try_to_number(substr(CCN, 3, 4)) between 8500 and 8899 then 'PB'
         when try_to_number(substr(CCN, 3, 4)) between 3800 and 3974 or try_to_number(substr(CCN, 3, 4)) between 8900 and 8999 then 'FS' else 'OT' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS)
select NPI, count(*) clinics, count(distinct CCN) ccns, count(distinct ASSOCIATE_ID) assoc_ids, max(ORGANIZATION_NAME) org, listagg(distinct ENROLLMENT_STATE, ',') states,
  count_if(cls = 'PB') pb, count_if(cls = 'FS') fs, listagg(distinct PROPRIETARY_NONPROFIT, ',') pn, listagg(distinct MULTIPLE_NPI_FLAG, ',') multi_npi,
  min(edt) first_enr, max(edt) last_enr, count_if(edt between '2020-10-01' and '2020-12-31') enr_q4_2020, max(INCORPORATION_DATE) inc,
  left(listagg(distinct DOING_BUSINESS_AS_NAME, ' ; '), 120) dbas
from r group by NPI order by clinics desc limit 25;

-- [17] RHC: land rate of RHC owner IDs on the Medicare hospital enrollment file (same ASSOCIATE_ID, state agrees), by CCN class and for-profit flag
with r as (
  select ASSOCIATE_ID, STATE, PROPRIETARY_NONPROFIT pn,
    case when try_to_number(substr(CCN, 3, 4)) between 3400 and 3499 or try_to_number(substr(CCN, 3, 4)) between 3975 and 3999 or try_to_number(substr(CCN, 3, 4)) between 8500 and 8899 then 'provider-based'
         when try_to_number(substr(CCN, 3, 4)) between 3800 and 3974 or try_to_number(substr(CCN, 3, 4)) between 8900 and 8999 then 'freestanding' else 'other' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS),
hosp as (select ASSOCIATE_ID, listagg(distinct STATE, ',') hst, max(SUBGROUP_ACUTE_CARE) acute from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS group by 1)
select cls, pn, count(*) clinics, count(hosp.ASSOCIATE_ID) owner_is_a_hospital_enrollee, count_if(contains(hosp.hst, r.STATE)) same_state,
  round(100 * count(hosp.ASSOCIATE_ID) / count(*), 1) pct_hospital
from r left join hosp on hosp.ASSOCIATE_ID = r.ASSOCIATE_ID group by 1, 2 order by 1, 2;

-- [18] HOSPITAL_COMPARE: star rating values and footnotes, by hospital type group
select HOSPITAL_OVERALL_RATING rating, HOSPITAL_OVERALL_RATING_FOOTNOTE fn, count(*) n, count(distinct FACILITY_ID) ids,
  count_if(HOSPITAL_TYPE = 'Acute Care Hospitals') acute, count_if(HOSPITAL_TYPE = 'Critical Access Hospitals') cah,
  count_if(HOSPITAL_OWNERSHIP ilike 'Voluntary%') nonprofit, count_if(HOSPITAL_OWNERSHIP = 'Proprietary') for_profit
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_COMPARE group by 1, 2 order by 3 desc limit 20;

-- [19] HOSPITAL_COMPARE: F-003 nonprofit set (2022 officer pay vs 2022 charity care) joined to star rating by CCN
with pay as (
  select EIN, max(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) top_comp_org,
    sum(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) officer_comp_from_org
  from LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY where TAX_YEAR = '2022' and not IS_GROUP_RETURN and not IS_FORMER and (IS_OFFICER or IS_KEY_EMPLOYEE) and not IS_HIGHEST_COMPENSATED group by 1),
hc as (
  select PROVIDER_CCN, max(STATE_CODE) st, sum(NUMBER_OF_BEDS) beds, sum(COST_OF_CHARITY_CARE) charity, sum(TOTAL_DISCHARGES_ALL) discharges
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS where year(FISCAL_YEAR_END_DATE) = 2022 group by 1 having sum(COST_OF_CHARITY_CARE) > 0),
j as (
  select hc.*, pay.top_comp_org, pay.officer_comp_from_org, x.EIN, x.CCN
  from LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN x join pay on pay.EIN = x.EIN join hc on hc.PROVIDER_CCN = x.CCN where x.MATCH_TIER <= 2 and x.PROPRIETARY_NONPROFIT = 'N'),
s as (select FACILITY_ID, max(HOSPITAL_OVERALL_RATING) r, max(HOSPITAL_TYPE) htype, max(STATE) cst from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_COMPARE group by 1)
select iff(grouping(coalesce(s.r::varchar, iff(s.FACILITY_ID is null, 'not in compare', 'no rating'))) = 1, 'ALL', coalesce(s.r::varchar, iff(s.FACILITY_ID is null, 'not in compare', 'no rating'))) stars,
  count(*) hospitals, count_if(s.cst = j.st) state_agrees, round(median(j.beds)) med_beds, round(median(j.discharges)) med_discharges,
  round(median(j.top_comp_org)) med_top_officer, round(median(j.charity)) med_charity,
  round(100 * count_if(j.top_comp_org > j.charity) / count(*), 1) pct_top_over_charity,
  round(100 * count_if(j.officer_comp_from_org > j.charity) / count(*), 1) pct_all_officers_over_charity,
  round(median(j.charity / nullif(j.discharges, 0))) med_charity_per_discharge,
  round(median(j.top_comp_org / nullif(j.beds, 0))) med_top_pay_per_bed
from j left join s on s.FACILITY_ID = j.CCN
group by grouping sets ((coalesce(s.r::varchar, iff(s.FACILITY_ID is null, 'not in compare', 'no rating'))), ()) order by 1;

-- [20] NH DEFICIENCIES: scope-severity letters, dispute flags and date range, plus the penalty file's date range and types
select SCOPE_SEVERITY_CODE sev, count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) homes, count_if(CITATION_UNDER_IDR = 'Y') idr, count_if(CITATION_UNDER_IIDR = 'Y') iidr,
  count_if(COMPLAINT_DEFICIENCY = 'Y') complaint, count_if(STANDARD_DEFICIENCY = 'Y') standard, min(SURVEY_DATE) first_survey, max(SURVEY_DATE) last_survey,
  count_if(SURVEY_DATE >= '2023-01-01') since_2023,
  (select min(PENALTY_DATE) || ' to ' || max(PENALTY_DATE) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES) pen_range,
  (select listagg(PENALTY_TYPE || '=' || c, ', ') from (select PENALTY_TYPE, count(*) c from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES group by 1)) pen_types
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES group by 1 order by 1;

-- [21] NH DEFICIENCIES: harm-level (G-L) citations per chain against each chain's own-state expectation per bed, with fines, in the penalty file's window
with win as (select min(PENALTY_DATE) d0 from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES),
d as (
  select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN), 6, '0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) gplus,
    count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl, count(distinct iff(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L'), SURVEY_DATE, null)) gplus_surveys
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, win where SURVEY_DATE >= win.d0 group by 1),
p as (
  select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN), 6, '0') ccn, count_if(PENALTY_TYPE = 'Fine') fines, sum(iff(PENALTY_TYPE = 'Fine', FINE_AMOUNT, 0)) fine_amt
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES group by 1),
h as (
  select lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN), 6, '0') ccn, n.STATE, n.CHAIN_ID, n.CHAIN_NAME, n.NUMBER_OF_CERTIFIED_BEDS beds,
    coalesce(d.gplus, 0) gplus, coalesce(d.jkl, 0) jkl, coalesce(d.gplus_surveys, 0) gsurv, coalesce(p.fines, 0) fines, coalesce(p.fine_amt, 0) fine_amt
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n left join d on d.ccn = lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN), 6, '0') left join p on p.ccn = lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN), 6, '0')
  where n.NUMBER_OF_CERTIFIED_BEDS > 0),
st as (select STATE, sum(gplus) / sum(beds) g_per_bed, count_if(gplus > 0 and fines = 0) / nullif(count_if(gplus > 0), 0) unfined_share from h group by 1),
c as (
  select h.CHAIN_ID, max(h.CHAIN_NAME) chain, count(*) homes, sum(beds) beds, listagg(distinct h.STATE, ',') states, sum(gplus) gplus, sum(jkl) jkl,
    round(sum(st.g_per_bed * h.beds), 1) expected, count_if(gplus > 0) g_homes, count_if(gsurv >= 2) repeat_g_homes,
    count_if(gplus > 0 and fines = 0) g_homes_unfined, round(sum(iff(gplus > 0, st.unfined_share, 0)), 1) expected_unfined, round(sum(fine_amt) / 1e6, 2) fines_m
  from h join st on st.STATE = h.STATE where h.CHAIN_ID is not null group by 1)
select (select d0 from win) window_start, (select count(*) from h) homes_all, (select sum(gplus) from h) gplus_all, (select count(*) from c where homes >= 10) chains_10plus,
  CHAIN_ID, chain, homes, beds, left(states, 40) states, gplus, jkl, expected, round(gplus / nullif(expected, 0), 2) o_e, g_homes, repeat_g_homes, g_homes_unfined, expected_unfined, fines_m
from c where homes >= 10 order by o_e desc limit 30;

-- [22] RHC: for-profit freestanding clinics enrolled July 2021 on, by owner (Fast Pace names folded together), with the window totals before and after
with r as (
  select *, try_to_date(substr(ENROLLMENT_ID, 2, 8), 'YYYYMMDD') edt,
    case when try_to_number(substr(CCN, 3, 4)) between 3800 and 3974 or try_to_number(substr(CCN, 3, 4)) between 8900 and 8999 then 'FS' else 'NOT_FS' end cls
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS),
w as (select count_if(cls = 'FS' and PROPRIETARY_NONPROFIT = 'P' and edt between '2019-01-01' and '2021-06-30') fsp_before_30mo,
             count_if(cls = 'FS' and PROPRIETARY_NONPROFIT = 'P' and edt between '2021-07-01' and '2025-12-31') fsp_after_54mo,
             count_if(ORGANIZATION_NAME ilike 'FAST PACE%') fast_pace_all from r)
select w.*, iff(ORGANIZATION_NAME ilike 'FAST PACE%', 'FAST PACE (all entities)', ORGANIZATION_NAME) owner, count(*) clinics, listagg(distinct ENROLLMENT_STATE, ',') states,
  count(distinct NPI) npis, min(edt) first_enr, max(edt) last_enr
from r cross join w where cls = 'FS' and PROPRIETARY_NONPROFIT = 'P' and edt >= '2021-07-01'
group by all order by clinics desc limit 15;

-- [23] NH DEFICIENCIES: how chains spread on harm-vs-own-state (chains with 10+ homes), plus the biggest chains for reference
with win as (select min(PENALTY_DATE) d0 from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES),
d as (
  select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN), 6, '0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) gplus, count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, win where SURVEY_DATE >= win.d0 group by 1),
h as (
  select lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN), 6, '0') ccn, n.STATE, n.CHAIN_ID, n.CHAIN_NAME, n.NUMBER_OF_CERTIFIED_BEDS beds, n.OWNERSHIP_TYPE own,
    coalesce(d.gplus, 0) gplus, coalesce(d.jkl, 0) jkl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n left join d on d.ccn = lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN), 6, '0') where n.NUMBER_OF_CERTIFIED_BEDS > 0),
st as (select STATE, sum(gplus) / sum(beds) g_per_bed from h group by 1),
c as (select CHAIN_ID, max(CHAIN_NAME) chain, count(*) homes, sum(gplus) gplus, sum(jkl) jkl, sum(st.g_per_bed * h.beds) expected
      from h join st on st.STATE = h.STATE where CHAIN_ID is not null group by 1 having count(*) >= 10),
dist as (select count(*) chains, median(gplus / expected) med_oe, count_if(gplus / expected >= 2) oe_2x, count_if(gplus / expected >= 1.5) oe_15x, count_if(gplus / expected < 1) under_1x from c),
ind as (select sum(gplus) g, sum(st.g_per_bed * h.beds) e, count(*) n from h join st on st.STATE = h.STATE where CHAIN_ID is null)
select dist.*, round(ind.g / ind.e, 2) independents_oe, ind.n independents, c.chain, c.homes, c.gplus, c.jkl, round(c.expected, 1) expected, round(c.gplus / c.expected, 2) o_e, round(c.gplus - c.expected) excess
from c cross join dist cross join ind
where c.homes >= 60 or c.chain ilike any ('%RELIANT%', '%BRIA%', '%LAHASKY%', '%TUTERA%', '%HURLBUT%', '%PLAINVIEW%')
order by excess desc limit 30;

-- [24] HOSPICE: every certified hospice in the four Houston buildings behind the shared phones, with phone and certification date
select upper(regexp_replace(ADDRESS_LINE_1, '\\s+', ' ')) addr, CCN, FACILITY_NAME, TELEPHONE_NUMBER, CERTIFICATION_DATE, OWNERSHIP_TYPE
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE
where STATE = 'TX' and (ADDRESS_LINE_1 ilike '2922 ROSEDALE%' or ADDRESS_LINE_1 ilike '7322 SOUTHWEST F%' or ADDRESS_LINE_1 ilike '7207 REGENCY SQ%' or ADDRESS_LINE_1 ilike '2646 S%LOOP W%')
order by 1, CERTIFICATION_DATE;
