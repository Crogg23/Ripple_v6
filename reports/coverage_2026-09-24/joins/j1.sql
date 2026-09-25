-- [s01]
-- find nursing-home, staffing, cost-report, PPP, OSHA, court and relief tables with row counts
select table_catalog, table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_schema not in ('TIMELINE') and (table_name ilike '%NURSING%' or table_name ilike '%SNF%' or table_name ilike '%PBJ%' or table_name ilike '%COST_REP%' or table_name ilike '%HCRIS%' or table_name ilike '%STAFFING%' or table_name ilike '%PPP%' or table_name ilike '%PROVIDER_RELIEF%' or table_name ilike '%FJC_IDB_CIVIL%' or table_name ilike '%COURTLISTENER_DOCKETS%' or table_name ilike '%OSHA_INSPECTIONS%' or table_name ilike '%FEC_INDIV%' or table_name ilike '%SKILLED%')
union all
select table_catalog, table_schema, table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
where table_name ilike '%NURSING%' or table_name ilike '%SNF%' or table_name ilike '%PBJ%' or table_name ilike '%COST_REP%' or table_name ilike '%HCRIS%' or table_name ilike '%STAFFING%' or table_name ilike '%SKILLED%'
order by 1,2,3
;

-- [s02]
-- Reliant homes (CHAIN_ID 446) -> SNF enrollment (CCN) -> owner file (ENROLLMENT_ID): every owner/controller, grouped per owner
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS)
select o.ASSOCIATE_ID_OWNER, o.TYPE_OWNER, coalesce(o.ORGANIZATION_NAME_OWNER, o.FIRST_NAME_OWNER||' '||o.LAST_NAME_OWNER) owner_name,
  o.STATE_OWNER, listagg(distinct o.ROLE_TEXT_OWNER, ' | ') roles, count(distinct rel.ccn) reliant_homes,
  min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) first_date, max(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) last_date,
  max(try_to_number(o.PERCENTAGE_OWNERSHIP)) max_pct
from rel join en on en.ccn=rel.ccn join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
group by 1,2,3,4 order by reliant_homes desc, owner_name
;

-- [s03]
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
;

-- [s04]
-- per Reliant home: earliest Reliant/DeStefane control date (ADP rows dropped), harm citations before/after it, all-time deficiency span, staffing, fines
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME, CITY, STATE, NUMBER_OF_CERTIFIED_BEDS beds, OVERALL_RATING star, SPECIAL_FOCUS_STATUS sff,
   REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY hprd, REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY rn, TOTAL_NURSING_STAFF_TURNOVER turn, NUMBER_OF_FINES nf, TOTAL_AMOUNT_OF_FINES_IN_DOLLARS fines, NUMBER_OF_PAYMENT_DENIALS pd,
   DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES first_appr
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
   where o.ASSOCIATE_ID_OWNER in ('1951309095','5092951160','4688749625','1658762539','1557792165','1951650696','7315471299') and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES)
select rel.*, j.rel_from, min(d.SURVEY_DATE) first_survey, max(d.SURVEY_DATE) last_survey,
  count_if(d.sev in ('G','H','I','J','K','L')) harm, count_if(d.sev in ('J','K','L')) jkl,
  count_if(d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE < j.rel_from) harm_before, count_if(d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE >= j.rel_from) harm_after
from rel left join j on j.ccn=rel.ccn left join d on d.ccn=rel.ccn
group by all order by j.rel_from desc nulls first
;

-- [s05]
-- per Reliant home: Medicare enrollment legal entity, incorporation date, NPI, and NursingHome411's ownership-change flag
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME, LEGAL_BUSINESS_NAME from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446')
select rel.ccn, rel.PROVIDER_NAME, rel.LEGAL_BUSINESS_NAME, e.ORGANIZATION_NAME, e.DOING_BUSINESS_AS_NAME, e.INCORPORATION_DATE, e.INCORPORATION_STATE, e.NPI, e.ENROLLMENT_ID, e.ADDRESS_LINE_1, e.CITY,
  f.PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS chow411, f.OWNERSHIP_TYPE_DETAIL, f.CHAIN_NAME chain411
from rel left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS e on lpad(trim(e.CCN),6,'0')=rel.ccn
left join LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 f on lpad(trim(f.CMS_CERTIFICATION_NUMBER_CCN),6,'0')=rel.ccn
order by e.INCORPORATION_DATE desc
;

-- [s06]
-- before/after acquisition: harm (G-L) and J-L per 100 bed-years since 2023-06-17, for Reliant legacy homes, Reliant 2024-25 acquisitions split at their own control date, and other MO homes split at 2024-12-01
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, CHAIN_ID, STATE, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE in ('MO','KS') and NUMBER_OF_CERTIFIED_BEDS>0),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
   where o.ASSOCIATE_ID_OWNER in ('1951309095','5092951160','4688749625','1658762539','1557792165','1951650696','7315471299') and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
b as (select nh.*, j.rel_from, '2023-06-17'::date w0, (select max(SURVEY_DATE) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES) w1,
   case when nh.CHAIN_ID='446' and j.rel_from is null then 'reliant_no_owner_row'
        when nh.CHAIN_ID='446' and j.rel_from < '2023-06-17' then 'reliant_legacy'
        when nh.CHAIN_ID='446' then 'reliant_acquired'
        when nh.STATE='MO' then 'other_mo' else 'other_ks' end grp,
   case when grp='reliant_acquired' then j.rel_from when grp in ('other_mo','other_ks') then '2024-12-01'::date else null end split
   from nh left join j on j.ccn=nh.ccn),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
   where SURVEY_DATE >= '2023-06-17' and SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')),
h as (select b.ccn, count_if(d.SURVEY_DATE < coalesce(b.split, b.w1+1)) harm_pre, count_if(d.SURVEY_DATE >= b.split) harm_post,
   count_if(d.sev in ('J','K','L') and d.SURVEY_DATE < coalesce(b.split, b.w1+1)) jkl_pre, count_if(d.sev in ('J','K','L') and d.SURVEY_DATE >= b.split) jkl_post
   from b left join d on d.ccn=b.ccn group by 1)
select grp, count(*) homes, sum(beds) beds, min(w1) w1,
  sum(harm_pre) harm_pre, round(sum(beds*datediff('day', w0, coalesce(split, w1))/365.25),0) bedyrs_pre, round(100*sum(harm_pre)/nullif(sum(beds*datediff('day', w0, coalesce(split, w1))/365.25),0),2) harm_rate_pre, round(100*sum(jkl_pre)/nullif(sum(beds*datediff('day', w0, coalesce(split, w1))/365.25),0),2) jkl_rate_pre,
  sum(harm_post) harm_post, round(sum(iff(split is null,0,beds*datediff('day', split, w1)/365.25)),0) bedyrs_post, round(100*sum(harm_post)/nullif(sum(iff(split is null,0,beds*datediff('day', split, w1)/365.25)),0),2) harm_rate_post, round(100*sum(jkl_post)/nullif(sum(iff(split is null,0,beds*datediff('day', split, w1)/365.25)),0),2) jkl_rate_post
from b join h on h.ccn=b.ccn group by 1 order by 1
;

-- [s07]
-- per-home before/after for the 12 homes Reliant took over in 2024-25: harm and J-L before vs after the control date, window 2023-06-17 to file end, with fines by penalty date
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME, STATE, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
   where o.ASSOCIATE_ID_OWNER in ('1951309095','5092951160','4688749625','1658762539','1557792165','1951650696','7315471299') and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17'),
p as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PENALTY_DATE, PENALTY_TYPE, FINE_AMOUNT from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES)
select nh.ccn, nh.PROVIDER_NAME, nh.STATE, nh.beds, j.rel_from,
  round(datediff('day','2023-06-17'::date, j.rel_from)/365.25,2) yrs_pre, round(datediff('day', j.rel_from, '2026-05-20'::date)/365.25,2) yrs_post,
  (select count(distinct SURVEY_DATE) from d where d.ccn=nh.ccn and d.SURVEY_DATE < j.rel_from) surveys_pre, (select count(distinct SURVEY_DATE) from d where d.ccn=nh.ccn and d.SURVEY_DATE >= j.rel_from) surveys_post,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE < j.rel_from) harm_pre,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE >= j.rel_from) harm_post,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('J','K','L') and d.SURVEY_DATE < j.rel_from) jkl_pre,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('J','K','L') and d.SURVEY_DATE >= j.rel_from) jkl_post,
  (select count(*) from d where d.ccn=nh.ccn and d.SURVEY_DATE < j.rel_from) alltags_pre, (select count(*) from d where d.ccn=nh.ccn and d.SURVEY_DATE >= j.rel_from) alltags_post,
  (select coalesce(sum(FINE_AMOUNT),0) from p where p.ccn=nh.ccn and p.PENALTY_DATE < j.rel_from) fines_pre, (select coalesce(sum(FINE_AMOUNT),0) from p where p.ccn=nh.ccn and p.PENALTY_DATE >= j.rel_from) fines_post
from nh join j on j.ccn=nh.ccn where j.rel_from >= '2023-06-17' order by j.rel_from
;

-- [s08]
-- CMS penalties on CCN: Reliant MO homes vs other MO homes. fines, dollars, payment denials, per 100 beds; plus penalty date span and duplicate check on FINE_ID
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, iff(CHAIN_ID='446','reliant','other_mo') grp, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO'),
p as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PENALTY_DATE, PENALTY_TYPE, FINE_ID, FINE_AMOUNT, PAYMENT_DENIAL_LENGTH_IN_DAYS pdd from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES where STATE='MO'),
pp as (select nh.grp, p.* from p join nh on nh.ccn=p.ccn)
select grp, (select count(*) from nh n2 where n2.grp=x.grp) homes, (select sum(beds) from nh n2 where n2.grp=x.grp) beds,
  count(*) penalties, count(distinct ccn) homes_penalized, count_if(PENALTY_TYPE ilike 'fine%') fines, sum(FINE_AMOUNT) fine_dollars, max(FINE_AMOUNT) max_fine,
  count_if(PENALTY_TYPE ilike 'payment%') pay_denials, sum(pdd) denial_days, min(PENALTY_DATE) p0, max(PENALTY_DATE) p1,
  count(FINE_ID) fine_ids, count(distinct FINE_ID) distinct_fine_ids,
  round(100*sum(FINE_AMOUNT)/(select sum(beds) from nh n2 where n2.grp=x.grp),0) fine_dollars_per_100_beds,
  round(100*count_if(PENALTY_TYPE ilike 'payment%')/(select sum(beds) from nh n2 where n2.grp=x.grp),3) denials_per_100_beds
from pp x group by grp order by grp
;

-- [s09]
-- staffing (CMS provider info, PBJ-based): Reliant MO vs other MO for-profit vs other MO non-profit/gov; resident-weighted hours per resident per day, turnover, stars
with nh as (select iff(CHAIN_ID='446','reliant', iff(OWNERSHIP_TYPE ilike 'For profit%','other_mo_forprofit','other_mo_nonprofit_gov')) grp, *
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO')
select grp, count(*) homes, count(REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY) homes_w_staffing,
  round(sum(REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY*AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)/sum(iff(REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY is null,0,AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)),2) total_hprd,
  round(sum(REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY*AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)/sum(iff(REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY is null,0,AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)),3) rn_hprd,
  round(sum(REPORTED_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY*AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)/sum(iff(REPORTED_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY is null,0,AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)),2) aide_hprd,
  round(sum(ADJUSTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY*AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)/sum(iff(ADJUSTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY is null,0,AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)),2) casemix_adj_total_hprd,
  round(median(REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY),2) med_total_hprd,
  round(avg(TOTAL_NURSING_STAFF_TURNOVER),1) avg_turnover, count(TOTAL_NURSING_STAFF_TURNOVER) n_turn,
  round(avg(NURSING_CASE_MIX_INDEX),3) avg_cmi, round(avg(OVERALL_RATING),2) avg_star, round(avg(STAFFING_RATING),2) avg_staff_star,
  round(sum(AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY)/sum(NUMBER_OF_CERTIFIED_BEDS),3) occupancy,
  count_if(OVERALL_RATING=1) one_star
from nh group by 1 order by 1
;

-- [s10]
-- PPP ($150K+ file): Reliant home legal entities (enrollment ORGANIZATION_NAME, normalized) = BORROWERNAME normalized, state MO/KS; also any borrower name containing RELIANT CARE or DESTEFANE
with rel as (select lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, n.PROVIDER_NAME, upper(n.CITY) city, n.STATE, e.ORGANIZATION_NAME,
   regexp_replace(regexp_replace(upper(e.ORGANIZATION_NAME),'[^A-Z0-9 ]',''),' (L L C|LLC|INC|LP|LLP|CO)$','') k
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS e on lpad(trim(e.CCN),6,'0')=lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0')
   where n.CHAIN_ID='446'),
ppp as (select BORROWERNAME, BORROWERADDRESS, upper(BORROWERCITY) city, BORROWERSTATE, DATEAPPROVED, CURRENTAPPROVALAMOUNT, FORGIVENESSAMOUNT, JOBSREPORTED, NAICSCODE, LOANNUMBER, SERVICINGLENDERNAME,
   regexp_replace(regexp_replace(upper(BORROWERNAME),'[^A-Z0-9 ]',''),' (L L C|LLC|INC|LP|LLP|CO)$','') k
   from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE in ('MO','KS'))
select rel.ccn, rel.PROVIDER_NAME, rel.city home_city, ppp.BORROWERNAME, ppp.city ppp_city, ppp.BORROWERADDRESS, ppp.DATEAPPROVED, ppp.CURRENTAPPROVALAMOUNT, ppp.FORGIVENESSAMOUNT, ppp.JOBSREPORTED, ppp.NAICSCODE, ppp.SERVICINGLENDERNAME, ppp.LOANNUMBER
from ppp left join rel on rel.k=ppp.k
where rel.ccn is not null or ppp.k ilike '%RELIANT CARE%' or ppp.k ilike '%DESTEFANE%' or ppp.k ilike 'MMA HEALTHCARE%' or ppp.k ilike 'BKY HEALTHCARE%'
order by ppp.DATEAPPROVED
;

-- [s11]
-- PPP miss check: how many MO/KS rows exist, how many nursing-home NAICS (623110) in MO, date span, and a sample of MO nursing-home borrowers
select BORROWERSTATE, count(*) n, count_if(NAICSCODE='623110') nh_naics, min(DATEAPPROVED) d0, max(DATEAPPROVED) d1, min(CURRENTAPPROVALAMOUNT) minamt,
  listagg(iff(NAICSCODE='623110' and BORROWERNAME ilike '%HEALTH%CARE%CENTER%', BORROWERNAME||' ('||BORROWERCITY||')', null), '; ') within group (order by BORROWERNAME) sample_hcc
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE in ('MO','KS') group by 1
;

-- [s12]
-- Provider Relief Fund: prebuilt chain row for CHAIN_ID 446, plus raw PRF lines in MO/KS whose name matches a Reliant home name or entity (name + state)
select 'chain_row' src, CHAIN_NAME name, null city, MATCHED_HOMES::varchar homes, MATCHED_RELIEF_DOLLARS amt, EXACT_MATCH_DOLLARS::varchar extra from LIBRARY_MARTS.HEALTH.HEALTH__NURSING_HOME_RELIEF_BY_CHAIN where CHAIN_ID='446'
union all
select 'prf_line', f.PROVIDER_NAME, f.CITY, f.STATE, f.PAYMENT_AMOUNT, n.PROVIDER_NAME
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND f
join (select distinct PROVIDER_NAME, upper(CITY) city, STATE, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446') n
  on f.STATE=n.STATE and (regexp_replace(upper(f.PROVIDER_NAME),'[^A-Z0-9]','') like n.k||'%' or f.PROVIDER_NAME ilike '%RELIANT CARE%')
where f.STATE in ('MO','KS')
order by 1, 2
;

-- [s13]
-- OSHA inspections: establishment name starts with a Reliant home name (punctuation stripped), same state and same city; or name contains RELIANT CARE
with n as (select distinct PROVIDER_NAME, upper(CITY) city, STATE, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
o as (select ACTIVITY_NR, ESTAB_NAME, upper(SITE_CITY) city, SITE_STATE, SITE_ADDRESS, OPEN_DATE, CLOSE_CASE_DATE, INSP_TYPE, INSP_SCOPE, SAFETY_HLTH, NAICS_CODE, OWNER_TYPE, regexp_replace(upper(ESTAB_NAME),'[^A-Z0-9]','') k
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS where SITE_STATE in ('MO','KS'))
select n.PROVIDER_NAME, n.city home_city, o.ESTAB_NAME, o.city osha_city, o.SITE_ADDRESS, o.OPEN_DATE, o.INSP_TYPE, o.INSP_SCOPE, o.SAFETY_HLTH, o.NAICS_CODE, o.ACTIVITY_NR
from o left join n on o.SITE_STATE=n.STATE and o.k like n.k||'%'
where (n.k is not null) or o.ESTAB_NAME ilike '%RELIANT CARE%'
order by o.OPEN_DATE desc
;

-- [s14]
-- OSHA 300A injury summaries 2023-2025, MO nursing homes (NAICS 623110): match to Reliant homes on name prefix + city (or company name RELIANT); injury rate per 100 FTE vs other MO nursing homes; hours sanity 500-4500 per worker
with n as (select distinct PROVIDER_NAME, upper(CITY) city, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446' and STATE='MO'),
a as (select 2023 yr, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY) city, STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES emp, TOTAL_HOURS_WORKED hrs, TOTAL_DAFW_CASES dafw, TOTAL_DJTR_CASES djtr, TOTAL_OTHER_CASES oth, TOTAL_DEATHS deaths from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 where STATE='MO' and NAICS_CODE::varchar='623110'
  union all select 2024, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DEATHS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 where STATE='MO' and NAICS_CODE::varchar='623110'
  union all select 2025, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DEATHS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 where STATE='MO' and NAICS_CODE::varchar='623110'),
m as (select a.*, n.PROVIDER_NAME matched_home from a left join n on regexp_replace(upper(a.ESTABLISHMENT_NAME),'[^A-Z0-9]','') like n.k||'%' and a.city=n.city),
f as (select *, iff(matched_home is not null or COMPANY_NAME ilike '%RELIANT CARE%', 'reliant', 'other_mo_623110') grp from m
  where try_to_number(emp)>0 and try_to_number(hrs)/try_to_number(emp) between 500 and 4500)
select grp, yr, count(*) filings, count(distinct matched_home) homes, sum(try_to_number(emp)) emp, sum(try_to_number(hrs)) hrs,
  sum(try_to_number(dafw)+try_to_number(djtr)+try_to_number(oth)) cases, sum(try_to_number(dafw)) dafw,
  round(200000*sum(try_to_number(dafw)+try_to_number(djtr)+try_to_number(oth))/sum(try_to_number(hrs)),2) trir, round(200000*sum(try_to_number(dafw))/sum(try_to_number(hrs)),2) dafw_rate,
  listagg(distinct iff(grp='reliant', ESTABLISHMENT_NAME||'|'||COMPANY_NAME||'|'||EIN, null), '; ') reliant_names
from f group by 1,2 order by 1,2
;

-- [s14]
-- [rerun, numeric columns] OSHA 300A injury summaries 2023-2025, MO nursing homes (NAICS 623110): match to Reliant homes on name prefix + city (or company name RELIANT); injury rate per 100 FTE vs other MO nursing homes; hours sanity 500-4500 per worker
with n as (select distinct PROVIDER_NAME, upper(CITY) city, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446' and STATE='MO'),
a as (select 2023 yr, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY) city, STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES emp, TOTAL_HOURS_WORKED hrs, TOTAL_DAFW_CASES dafw, TOTAL_DJTR_CASES djtr, TOTAL_OTHER_CASES oth, TOTAL_DEATHS deaths from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 where STATE='MO' and NAICS_CODE::varchar='623110'
  union all select 2024, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DEATHS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 where STATE='MO' and NAICS_CODE::varchar='623110'
  union all select 2025, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DEATHS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 where STATE='MO' and NAICS_CODE::varchar='623110'),
m as (select a.*, n.PROVIDER_NAME matched_home from a left join n on regexp_replace(upper(a.ESTABLISHMENT_NAME),'[^A-Z0-9]','') like n.k||'%' and a.city=n.city),
f as (select *, iff(matched_home is not null or COMPANY_NAME ilike '%RELIANT CARE%', 'reliant', 'other_mo_623110') grp from m
  where coalesce(emp::float,0)>0 and coalesce(hrs::float,0)/coalesce(emp::float,0) between 500 and 4500)
select grp, yr, count(*) filings, count(distinct matched_home) homes, sum(coalesce(emp::float,0)) emp, sum(coalesce(hrs::float,0)) hrs,
  sum(coalesce(dafw::float,0)+coalesce(djtr::float,0)+coalesce(oth::float,0)) cases, sum(coalesce(dafw::float,0)) dafw,
  round(200000*sum(coalesce(dafw::float,0)+coalesce(djtr::float,0)+coalesce(oth::float,0))/sum(coalesce(hrs::float,0)),2) trir, round(200000*sum(coalesce(dafw::float,0))/sum(coalesce(hrs::float,0)),2) dafw_rate,
  listagg(distinct iff(grp='reliant', ESTABLISHMENT_NAME||'|'||COMPANY_NAME||'|'||EIN, null), '; ') reliant_names
from f group by 1,2 order by 1,2
;

-- [s15]
-- OSHA 300A eyeball: every Reliant-matched filing row 2023-2025 (name prefix + city, or company RELIANT), with address to confirm
with n as (select distinct PROVIDER_NAME, upper(CITY) city, ADDRESS, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446' and STATE='MO'),
a as (select 2023 yr, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY) city, STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES emp, TOTAL_HOURS_WORKED hrs, TOTAL_DAFW_CASES dafw, TOTAL_DJTR_CASES djtr, TOTAL_OTHER_CASES oth, TOTAL_DAFW_DAYS dafw_days from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 where STATE='MO'
  union all select 2024, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DAFW_DAYS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 where STATE='MO'
  union all select 2025, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DAFW_DAYS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 where STATE='MO')
select a.yr, n.PROVIDER_NAME matched_home, n.ADDRESS home_addr, a.ESTABLISHMENT_NAME, a.COMPANY_NAME, a.EIN, a.city, a.STREET_ADDRESS, a.emp, a.hrs, a.dafw, a.djtr, a.oth, a.dafw_days
from a left join n on regexp_replace(upper(a.ESTABLISHMENT_NAME),'[^A-Z0-9]','') like n.k||'%' and a.city=n.city
where n.k is not null or a.COMPANY_NAME ilike '%RELIANT%CARE%' or a.COMPANY_NAME ilike '%RELIANTCARE%'
order by a.yr, a.ESTABLISHMENT_NAME
;

-- [s16]
-- FEC itemized individual gifts: donor surname DESTEFANE in MO, or employer RELIANT CARE (any state); memo rows dropped; grouped by donor, employer, committee
with g as (select DONOR_NAME, CITY, STATE, EMPLOYER, OCCUPATION, CMTE_ID, TRANSACTION_DATE, TRANSACTION_AMT, CYCLE_FILE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
  where coalesce(MEMO_CD,'') <> 'X' and ((DONOR_NAME ilike 'DESTEFANE%' and STATE='MO') or EMPLOYER ilike '%RELIANT CARE%' or EMPLOYER ilike 'RELIANTCARE%'))
select g.DONOR_NAME, g.CITY, g.EMPLOYER, g.OCCUPATION, g.CMTE_ID, max(c.CMTE_NM) cmte_name, count(*) gifts, sum(g.TRANSACTION_AMT) dollars, min(g.CYCLE_FILE) c0, max(g.CYCLE_FILE) c1
from g left join (select CMTE_ID, max(CMTE_NM) CMTE_NM from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES group by 1) c on c.CMTE_ID=g.CMTE_ID
group by 1,2,3,4,5 order by dollars desc
;

-- [s17]
-- federal civil cases (FJC IDB): plaintiff or defendant names RELIANT CARE, DESTEFANE, or a distinctive Reliant home name (generic single names like HERITAGE only with CARE CENTER)
select DISTRICT, OFFICE, DOCKET, FILE_DATE, TERM_DATE, NATURE_OF_SUIT, PLAINTIFF, DEFENDANT, DISPOSITION, JUDGMENT, AMOUNT_RECEIVED, TAPE_YEAR, count(*) over (partition by DISTRICT, DOCKET) yearly_rows
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
where regexp_like(upper(coalesce(PLAINTIFF,'')||' | '||coalesce(DEFENDANT,'')),
 '.*(RELIANT CARE|RELIANTCARE|DESTEFANE|NORTH VILLAGE PARK|BRIDGEWOOD HEALTH|GREGORY RIDGE|HERITAGE CARE CENTER|CRESTWOOD HEALTH|CHARITON PARK|EASTVIEW MANOR|FOUR SEASONS LIVING|EDGEWOOD MANOR HEALTH|NATHAN RICHARD|BERNARD CARE|GIETNER|GRAND MANOR HEALTH|HIDDEN LAKE HEALTH|PARKWAY HEALTH CARE|NICKS HEALTH|NICK.S HEALTH|PORTAGEVILLE HEALTH|WESTVIEW NURSING|MMA HEALTHCARE|BKY HEALTHCARE|REST HAVEN HEALTH|WELLSVILLE HEALTH|HOLTON HEALTH|BRUNSWICK HEALTH|SARCOXIE|ODESSA HEALTH|BROOKFIELD HEALTH|SOUTH COUNTY HEALTH|STONECREST HEALTH|GREENVILLE HEALTH|MILAN HEALTH|FAIR VIEW HEALTH|ST ELIZABETH CARE|CASSVILLE HEALTH).*')
order by FILE_DATE desc
;

-- [s18]
-- CourtListener dockets: case name contains RELIANT CARE, DESTEFANE, or a distinctive Reliant home/entity name; Missouri/Kansas/8th Cir/appellate courts shown with court id
select COURT_ID, DOCKET_NUMBER, DATE_FILED, DATE_TERMINATED, CASE_NAME, NATURE_OF_SUIT, CAUSE, ID
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where regexp_like(upper(CASE_NAME), '.*(RELIANT CARE|RELIANTCARE|DESTEFANE|NORTH VILLAGE PARK|BRIDGEWOOD HEALTH|GREGORY RIDGE HEALTH|HERITAGE CARE CENTER|CRESTWOOD HEALTH CARE CENTER|CHARITON PARK|EASTVIEW MANOR|FOUR SEASONS LIVING|EDGEWOOD MANOR HEALTH|NATHAN RICHARD|BERNARD CARE|GIETNER|HIDDEN LAKE HEALTH|PARKWAY HEALTH CARE|NICK.?S HEALTH CARE|PORTAGEVILLE HEALTH|WESTVIEW NURSING|MMA HEALTHCARE OF|BKY HEALTHCARE|REST HAVEN HEALTH CARE|WELLSVILLE HEALTH|HOLTON HEALTH|SARCOXIE HEALTH|STONECREST HEALTH|MILAN HEALTH CARE).*')
order by DATE_FILED desc
;

-- [s19]
-- USAspending assistance (all programs FY2007-26): MO/KS recipients named RELIANT CARE or a distinctive Reliant home/entity name; per recipient x program: UEI, dollars, loan face value, first/last action date
select RECIPIENT_NAME, RECIPIENT_UEI, RECIPIENT_CITY_NAME, RECIPIENT_STATE_CODE, CFDA_NUMBER, max(CFDA_TITLE) cfda_title, count(*) txns,
  sum(FEDERAL_ACTION_OBLIGATION) obligated, sum(FACE_VALUE_OF_LOAN) loan_face, min(ACTION_DATE) first_action, max(ACTION_DATE) last_action, max(RECIPIENT_PARENT_NAME) parent
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL
where RECIPIENT_STATE_CODE in ('MO','KS') and regexp_like(upper(RECIPIENT_NAME), '.*(RELIANT CARE|RELIANTCARE|NORTH VILLAGE PARK|BRIDGEWOOD HEALTH|GREGORY RIDGE HEALTH|HERITAGE CARE CENTER|CRESTWOOD HEALTH CARE|CHARITON PARK|EASTVIEW MANOR|FOUR SEASONS LIVING|EDGEWOOD MANOR HEALTH|NATHAN RICHARD HEALTH|BERNARD CARE|GIETNER|GRAND MANOR HEALTH|HIDDEN LAKE HEALTH|PARKWAY HEALTH CARE|NICK.?S HEALTH CARE|PORTAGEVILLE HEALTH|WESTVIEW NURSING|MMA HEALTHCARE OF|BKY HEALTHCARE|REST HAVEN HEALTH CARE|WELLSVILLE HEALTH|HOLTON HEALTH|BRUNSWICK HEALTH|SARCOXIE HEALTH|ODESSA HEALTH CARE|BROOKFIELD HEALTH|SOUTH COUNTY HEALTH CARE|STONECREST HEALTH|GREENVILLE HEALTH CARE|MILAN HEALTH|FAIR VIEW HEALTH|ST\.? ELIZABETH CARE|CASSVILLE HEALTH).*')
group by 1,2,3,4,5 order by 1, 5
;

-- [s20]
-- USAspending miss check: MO rows, rows whose recipient name contains HEALTH CARE CENTER, and a sample, for CFDA 93.498 (Provider Relief) and 59.073 (PPP)
select RECIPIENT_STATE_CODE, count(*) n, count_if(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%') hcc, count_if(CFDA_NUMBER='93.498') prf_rows, count_if(CFDA_NUMBER='59.073') ppp_rows,
  listagg(distinct iff(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%' and CFDA_NUMBER in ('93.498','59.073'), RECIPIENT_NAME, null), '; ') within group (order by iff(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%' and CFDA_NUMBER in ('93.498','59.073'), RECIPIENT_NAME, null)) sample
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE in ('MO') group by 1
;

-- [s20]
-- [rerun, alias] USAspending miss check: MO rows, rows whose recipient name contains HEALTH CARE CENTER, and a sample, for CFDA 93.498 (Provider Relief) and 59.073 (PPP)
select RECIPIENT_STATE_CODE, count(*) n, count_if(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%') hcc, count_if(CFDA_NUMBER='93.498') prf_rows, count_if(CFDA_NUMBER='59.073') ppp_rows,
  listagg(distinct iff(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%' and CFDA_NUMBER in ('93.498','59.073'), RECIPIENT_NAME, null), '; ') within group (order by iff(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%' and CFDA_NUMBER in ('93.498','59.073'), RECIPIENT_NAME, null)) name_sample
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE in ('MO') group by 1
;

-- [s21]
-- Provider Relief Fund, second pass: MO/KS lines for the Reliant homes the first name-prefix pass missed (corporate names MMA/BKY/EASTVIEW MANOR INC, and every 2024-25 acquisition, whose 2020-21 money went to the prior operator)
select PROVIDER_NAME, CITY, STATE, PAYMENT_AMOUNT
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND
where STATE in ('MO','KS') and regexp_like(upper(PROVIDER_NAME), '.*(MMA HEALTHCARE|BKY HEALTHCARE|EASTVIEW MANOR|BERNARD CARE|WESTVIEW NURSING|MILAN HEALTH|STONECREST|ST\.? ELIZABETH CARE|HIDDEN LAKE|SOUTH COUNTY HEALTH|BROOKFIELD HEALTH|SARCOXIE|ODESSA HEALTH|HOLTON HEALTH|BRUNSWICK HEALTH|GIETNER|WELLSVILLE HEALTH|REST HAVEN HEALTH|FAIR VIEW HEALTH|FAIRVIEW HEALTH|GRAND MANOR|CASSVILLE HEALTH|RELIANT).*')
order by PROVIDER_NAME
;

-- [s22]
-- misses to confirm: (a) HHS-OIG exclusion list rows naming DESTEFANE or RELIANT CARE or a Reliant home NPI; (b) hospital cost reports (HCRIS) on any Reliant CCN
select 'leie' src, count(*) n, listagg(coalesce(BUSINESS_NAME,'')||' '||coalesce(LAST_NAME,'')||','||coalesce(FIRST_NAME,'')||' '||coalesce(CITY,'')||' '||coalesce(STATE,'')||' '||coalesce(EXCLUSION_DATE::varchar,''), '; ') detail
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
where upper(LAST_NAME)='DESTEFANE' or upper(BUSINESS_NAME) like '%RELIANT CARE%'
   or NPI in (select NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS e join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n on lpad(trim(e.CCN),6,'0')=lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0') where n.CHAIN_ID='446')
union all
select 'hcris', count(*), listagg(distinct PROVIDER_CCN, ',') from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS
where lpad(trim(PROVIDER_CCN::varchar),6,'0') in (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446')
;

-- [s23]
-- MO homes binned by reported total nurse hours per resident-day (half-hour bins): homes, Reliant homes, harm and J-L citations per 100 beds since 2023-06-17 (dose-response check for the staffing link)
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, CHAIN_ID, NUMBER_OF_CERTIFIED_BEDS beds, REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY hprd
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO' and NUMBER_OF_CERTIFIED_BEDS>0),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) harm, count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17' and STATE='MO' group by 1)
select case when hprd is null then 'no data' when hprd < 2 then '<2.0' when hprd >= 5 then '5.0+' else to_varchar(floor(hprd*2)/2,'0.0')||'-'||to_varchar(floor(hprd*2)/2+0.5,'0.0') end hprd_bin,
  count(*) homes, count_if(CHAIN_ID='446') reliant_homes, sum(beds) beds, sum(coalesce(harm,0)) harm, sum(coalesce(jkl,0)) jkl,
  round(100*sum(coalesce(harm,0))/sum(beds),2) harm_per_100_beds, round(100*sum(coalesce(jkl,0))/sum(beds),2) jkl_per_100_beds,
  round(100*sum(iff(CHAIN_ID='446',0,coalesce(harm,0)))/nullif(sum(iff(CHAIN_ID='446',0,beds)),0),2) harm_per_100_beds_nonreliant
from nh left join d on d.ccn=nh.ccn group by 1 order by 1
;

-- [s24]
-- chart rows: MO homes by staffing bin (reported total nurse hours per resident-day) x Reliant or not: homes, beds, harm (G-L) and J-L citations since 2023-06-17 per 100 beds
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, iff(CHAIN_ID='446','Reliant','Other MO') grp, NUMBER_OF_CERTIFIED_BEDS beds, REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY hprd
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO' and NUMBER_OF_CERTIFIED_BEDS>0),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) harm, count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17' and STATE='MO' group by 1)
select case when hprd is null then 'no data' when hprd < 2.5 then 'under 2.5' when hprd < 3 then '2.5-3.0' when hprd < 3.5 then '3.0-3.5' else '3.5+' end hprd_bin, grp,
  count(*) homes, sum(beds) beds, sum(coalesce(harm,0)) harm, sum(coalesce(jkl,0)) jkl,
  round(100*sum(coalesce(harm,0))/sum(beds),2) harm_per_100_beds, round(100*sum(coalesce(jkl,0))/sum(beds),2) jkl_per_100_beds
from nh left join d on d.ccn=nh.ccn group by 1,2 order by 1,2
;

