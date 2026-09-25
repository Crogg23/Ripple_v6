-- deep3 / g05: proper look at five glance-only tables, 2026-09-24
-- Tables: HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS, HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS,
--         HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS, HEALTH__FED_CDC_DATA_PORTAL,
--         HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS
-- Door: Python (connect/db.py) via g05/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g05/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- HHA enrollments: profile of keys, flags, sentinel dates, ownership
select count(*) n, count(distinct ENROLLMENT_ID) enr, count(distinct CCN) ccn, count(distinct NPI) npi, count(distinct ASSOCIATE_ID) assoc,
  count_if(CCN is null or trim(CCN)='') ccn_blank, count_if(NPI is null or trim(NPI)='') npi_blank,
  count_if(MULTIPLE_NPI_FLAG='Y') multi_y, count_if(MULTIPLE_NPI_FLAG='N') multi_n,
  count_if(PROPRIETARY_NONPROFIT='P') forprofit, count_if(PROPRIETARY_NONPROFIT='N') nonprofit,
  count_if(INCORPORATION_DATE is null) inc_null, count_if(year(INCORPORATION_DATE)<1900) inc_pre1900,
  count_if(year(INCORPORATION_DATE)>=2019) inc_2019on,
  listagg(distinct PRACTICE_LOCATION_TYPE, '|') plt_vals, count(distinct ENROLLMENT_STATE) states,
  count(distinct upper(trim(ADDRESS_LINE_1))||'|'||left(ZIP_CODE,5)) addrs
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS;

-- [q02] statement 2
-- Hospital enrollments: profile, the NPIs that repeat 68 times, provider types
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS),
topnpi as (select NPI, count(*) n, count(distinct CCN) ccns, count(distinct ORGANIZATION_NAME) orgs, count(distinct ENROLLMENT_STATE) st,
             any_value(ORGANIZATION_NAME) org, listagg(distinct MULTIPLE_NPI_FLAG,'|') mf
           from t group by 1 order by n desc limit 6)
select 'npi' k, NPI a, n::text b, ccns::text c, orgs::text d, st::text e, org f, mf g from topnpi
union all
select 'profile', count(*)::text, count(distinct CCN)::text, count(distinct NPI)::text, count(distinct ASSOCIATE_ID)::text,
  count_if(MULTIPLE_NPI_FLAG='Y')::text, count_if(REH_CONVERSION_FLAG='Y')::text || ' reh / ' || count_if(REH_CONVERSION_DATE is not null)::text || ' dated',
  count_if(year(INCORPORATION_DATE)<1900)::text || ' pre1900; null ' || count_if(INCORPORATION_DATE is null)::text from t
union all
select 'ptype', PROVIDER_TYPE_CODE, PROVIDER_TYPE_TEXT, count(*)::text, count_if(PROPRIETARY_NONPROFIT='P')::text, count(distinct CCN)::text, null, null from t group by 2,3;

-- [q03] statement 3
-- ASM participants: profile, repeated NPIs, biggest practices, small-practice share by cohort
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS),
rep as (select NPI, count(*) n, count(distinct ASM_COHORT) coh, count(distinct ORGANIZATION_LEGAL_NAME) orgs, count(distinct STATE) st from t group by 1 having count(*)>1),
org as (select ORGANIZATION_LEGAL_NAME o, count(*) n, count(distinct NPI) npis, listagg(distinct STATE, ',') sts, listagg(distinct ASM_COHORT, ',') coh,
          max(ASM_CY27_SMALLPRACTICE) sp from t group by 1 order by n desc limit 15)
select 'profile' k, count(*)::text a, count(distinct NPI)::text b, count(distinct ORGANIZATION_LEGAL_NAME)::text c,
  count_if(ASM_CY27_SMALLPRACTICE='Yes')::text d, count_if(ASM_CY27_SMALLPRACTICE='No')::text e,
  (select count(*) from rep)::text || ' repeat npis; ' || (select count_if(coh>1) from rep)::text || ' in both cohorts; ' || (select count_if(orgs>1) from rep)::text || ' in 2+ orgs' f from t
union all select 'cohort', ASM_COHORT, count(*)::text, count(distinct NPI)::text, count_if(ASM_CY27_SMALLPRACTICE='Yes')::text, count(distinct ORGANIZATION_LEGAL_NAME)::text, count(distinct STATE)::text from t group by 2
union all select 'org', o, n::text, npis::text, sts, coh, sp from org
union all select 'cy28vals', ASM_CY28_PARTICIPANT, count(*)::text, null, null, null, null from t group by 2;

-- [q04] statement 4
-- CDC data portal: created per year, last data update per year, resource types, categories
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DATA_PORTAL)
select 'ids' k, 'rows/ids/pv_nonnull' a, count(*) n, count(distinct DATASET_ID) m, count(PAGE_VIEWS) x from t
union all select 'created', year(CREATED_AT)::text, count(*), count_if(RESOURCE_TYPE='dataset'), sum(DOWNLOAD_COUNT) from t group by 2
union all select 'data_upd', year(DATA_UPDATED_AT)::text, count(*), count_if(RESOURCE_TYPE='dataset'), sum(DOWNLOAD_COUNT) from t group by 2
union all select 'rtype', RESOURCE_TYPE, count(*), count(distinct DATASET_ID), sum(DOWNLOAD_COUNT) from t group by 2
union all select 'cat', DOMAIN_CATEGORY, count(*), count_if(RESOURCE_TYPE='dataset'), sum(DOWNLOAD_COUNT) from t group by 2
order by 1, 2;

-- [q05] statement 5
-- OTP providers: profile, effective-date years, biggest NPIs and names
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS)
select 'profile' k, count(*)::text a, count(distinct NPI)::text b, count(distinct NPI||'|'||upper(trim(ADDRESS_LINE_1))||'|'||left(ZIP,5))::text c,
  count_if(MEDICARE_ID_EFFECTIVE_DATE='2020-01-01')::text d, count(distinct upper(trim(ADDRESS_LINE_1))||'|'||left(ZIP,5))::text e, count(distinct PROVIDER_NAME)::text f from t
union all select 'effyear', year(MEDICARE_ID_EFFECTIVE_DATE)::text, count(*)::text, count(distinct NPI)::text, null, null, null from t group by 2
union all select * from (select 'topnpi', NPI, any_value(PROVIDER_NAME), count(*)::text, count(distinct STATE)::text,
  count(distinct upper(trim(ADDRESS_LINE_1))||left(ZIP,5))::text, min(MEDICARE_ID_EFFECTIVE_DATE)::text from t group by 2 order by count(*) desc limit 8)
union all select * from (select 'topname', upper(PROVIDER_NAME), null, count(*)::text, count(distinct NPI)::text, count(distinct STATE)::text, null
  from t group by 2 order by count(*) desc limit 12);

-- [q06] statement 6
-- HHA: street addresses shared by 3+ different organizations (distinct ASSOCIATE_ID); share by state, then the top addresses
with t as (select CCN, ASSOCIATE_ID, ORGANIZATION_NAME, STATE,
             upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z, upper(CITY) city,
             try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
g as (select a1, z, count(*) n, count(distinct ASSOCIATE_ID) orgs from t group by 1,2),
tt as (select t.*, g.orgs from t join g using (a1, z)),
st as (select STATE, count(*) agencies, count_if(orgs>=3) at_shared3, count_if(orgs>=2) at_shared2 from tt group by 1),
top as (select a1, z, any_value(city) city, any_value(STATE) st, count(*) n, max(orgs) orgs, min(enr_dt) first_enr, max(enr_dt) last_enr,
          listagg(distinct left(ORGANIZATION_NAME,28), '; ') names
        from tt where orgs>=3 group by 1,2 order by orgs desc, n desc limit 25)
select 'nat' k, null a, sum(agencies)::text b, sum(at_shared3)::text c, sum(at_shared2)::text d, null e, null f, null g, null h from st
union all select * from (select 'state', STATE, agencies::text, at_shared3::text, at_shared2::text, round(100*at_shared3/agencies,1)::text, null, null, null
  from st where agencies>=100 order by at_shared3/agencies desc limit 15)
union all select 'addr', a1||' '||z, city, st, n::text, orgs::text, first_enr::text, last_enr::text, names from top;

-- [q07] statement 7
-- HHA: new Medicare enrollments per year (date inside ENROLLMENT_ID), in the six 2013-2019 moratorium metros (approx by ZIP3), LA County (approx ZIP3), and the rest
with t as (select try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt, left(ZIP_CODE,3) z3, STATE, INCORPORATION_DATE
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
r as (select *, case
   when STATE='FL' and z3 in ('330','331','332','333') then 'MIA_FTL'
   when STATE='IL' and z3 between '600' and '608' then 'CHICAGO'
   when STATE='TX' and z3 in ('770','772','773','774','775') then 'HOUSTON'
   when STATE='TX' and z3 in ('750','751','752','753','760','761','762') then 'DALLAS'
   when STATE='MI' and z3 between '480' and '483' then 'DETROIT'
   when STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935')) then 'LA_COUNTY'
   else 'REST' end rg from t)
select year(enr_dt) yr,
  count_if(rg='MIA_FTL') mia_ftl, count_if(rg='CHICAGO') chicago, count_if(rg='HOUSTON') houston, count_if(rg='DALLAS') dallas, count_if(rg='DETROIT') detroit,
  count_if(rg='LA_COUNTY') la_county, count_if(rg='REST') rest, count(*) total,
  count_if(enr_dt is null) bad_id, count_if(year(INCORPORATION_DATE)=year(enr_dt)) inc_same_yr
from r group by 1 order by 1;

-- [q08] statement 8
-- HHA join to Home Health Compare (CCN): LA County (approx ZIP3) vs rest of CA vs rest of US, by enrollment era, and shared-address (3+ orgs) vs not
with t as (select lpad(trim(CCN),6,'0') ccn, ASSOCIATE_ID, STATE, left(ZIP_CODE,3) z3,
             upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z,
             try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
g as (select a1, z, count(distinct ASSOCIATE_ID) orgs from t group by 1,2),
tt as (select t.*, g.orgs,
  case when STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935')) then '1_LA' when STATE='CA' then '2_restCA' else '3_restUS' end rg,
  case when year(enr_dt)<2013 then 'a_pre2013' when year(enr_dt)<2019 then 'b_2013_18' else 'c_2019on' end era
  from t join g using (a1, z)),
h as (select lpad(trim(CCN),6,'0') ccn, QUALITY_OF_PATIENT_CARE_STAR_RATING star,
        HOW_MUCH_MEDICARE_SPENDS_ON_AN_EPISODE_OF_CARE_AT_THIS_AGENCY_COMPARED_TO_MEDICARE_SPENDING_ACROSS_ALL_AGENCIES_NATIONALLY spend,
        try_to_number(NO_OF_EPISODES_TO_CALC_HOW_MUCH_MEDICARE_SPENDS_PER_EPISODE_OF_CARE_AT_AGENCY_COMPARED_TO_SPENDING_AT_ALL_AGENCIES_NATIONAL) eps,
        PPH_RISK_STANDARDIZED_RATE pph, PPH_PERFORMANCE_CATEGORIZATION pphcat, DTC_RISK_STANDARDIZED_RATE dtc
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH)
select rg, era, iff(orgs>=3,'shared3','alone') addr, count(*) agencies, count(h.ccn) landed, count(h.star) n_star, round(avg(h.star),2) avg_star,
  count(h.spend) n_spend, round(median(h.spend),2) med_spend, round(avg(h.spend),2) avg_spend,
  round(sum(h.spend*h.eps)/nullif(sum(iff(h.spend is not null, h.eps, null)),0),2) epw_spend, sum(iff(h.spend is not null, h.eps, 0)) eps,
  round(median(h.pph),2) med_pph, count_if(h.pphcat ilike 'worse%') pph_worse, round(median(h.dtc),2) med_dtc
from tt left join h on h.ccn = tt.ccn
group by 1,2,3 order by 1,2,3;

-- [q09] statement 9
-- HHA -> POS file (CCN) for the exact county: check the ZIP3 LA approximation per year, then top counties for 2019+ enrollments vs their pre-2013 count
with t as (select lpad(trim(CCN),6,'0') ccn, STATE, left(ZIP_CODE,3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
p as (select lpad(trim(CCN),6,'0') ccn, max(lpad(FIPS_STATE_CD,2,'0')||lpad(FIPS_CNTY_CD,3,'0')) fips, max(STATE_CD) pst, max(CITY_NAME) pcity
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER group by 1),
j as (select t.*, p.fips, p.pcity, (STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935'))) la_z3 from t left join p using (ccn))
select 'yr' k, year(enr_dt)::text a, count(*) total, count(fips) landed, count_if(fips='06037') la_exact, count_if(la_z3) la_zip3,
  count_if(fips='06037' and not la_z3) exact_not_z3, count_if(la_z3 and fips<>'06037') z3_not_exact
from j where year(enr_dt)>=2010 group by 2
union all
select * from (select 'cty', fips||' '||any_value(STATE)||' '||any_value(pcity), count_if(year(enr_dt)>=2019), count(*), count_if(year(enr_dt)<2013),
  count_if(year(enr_dt) between 2013 and 2018), null, null
  from j where fips is not null group by fips order by 3 desc limit 12)
order by 1 desc, 2;

-- [q10] statement 10
-- HHA owners at the addresses with 8+ organizations (HOME_HEALTH_OWNERS by ENROLLMENT_ID): do the agencies share owners?
with t as (select ENROLLMENT_ID, CCN, ORGANIZATION_NAME,
             upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z, ADDRESS_LINE_2, ASSOCIATE_ID
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
g as (select a1, z from t group by 1,2 having count(distinct ASSOCIATE_ID)>=8),
tc as (select t.* from t join g using (a1, z)),
o as (select ENROLLMENT_ID, ASSOCIATE_ID_OWNER, TYPE_OWNER, OWNER_NAME, ROLE_TEXT_OWNER, PERCENTAGE_OWNERSHIP from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS),
jo as (select tc.a1, tc.z, tc.ENROLLMENT_ID, o.ASSOCIATE_ID_OWNER, o.TYPE_OWNER, o.OWNER_NAME, o.ROLE_TEXT_OWNER from tc join o using (ENROLLMENT_ID)),
own_anywhere as (select ASSOCIATE_ID_OWNER, count(distinct ENROLLMENT_ID) n_any from o group by 1),
peraddr as (select a1, z, count(distinct ENROLLMENT_ID) agencies_with_owner_rows, count(distinct ASSOCIATE_ID_OWNER) owners,
   count(distinct iff(TYPE_OWNER='I', ASSOCIATE_ID_OWNER, null)) indiv_owners from jo group by 1,2),
shared as (select a1, z, ASSOCIATE_ID_OWNER, any_value(OWNER_NAME) nm, any_value(TYPE_OWNER) ty, count(distinct ENROLLMENT_ID) n_here from jo group by 1,2,3 having count(distinct ENROLLMENT_ID)>=2)
select 'addr' k, g.a1||' '||g.z a, (select count(*) from tc where tc.a1=g.a1 and tc.z=g.z)::text b,
  (select count(distinct ADDRESS_LINE_2) from tc where tc.a1=g.a1 and tc.z=g.z)::text c,
  p.agencies_with_owner_rows::text d, p.owners::text e, p.indiv_owners::text f,
  (select count(*) from shared s where s.a1=g.a1 and s.z=g.z)::text g2,
  (select max(n_here) from shared s where s.a1=g.a1 and s.z=g.z)::text h
from g left join peraddr p using (a1, z)
union all
select * from (select 'owner', s.a1||' '||s.z, s.nm, s.ty, s.n_here::text, oa.n_any::text, null, null, null
  from shared s join own_anywhere oa using (ASSOCIATE_ID_OWNER) order by s.n_here desc, oa.n_any desc limit 20);

-- [q11] statement 11
-- HHA eyeball: every agency at 14545 Friar St, Van Nuys, joined to Home Health Compare (CCN): suite, enrollment date, certification date, star, spend ratio, episodes
with t as (select lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID, ORGANIZATION_NAME, ADDRESS_LINE_2, INCORPORATION_DATE, PROPRIETARY_NONPROFIT,
             try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
           where upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) = '14545 FRIAR ST' and left(ZIP_CODE,5)='91411'),
h as (select lpad(trim(CCN),6,'0') ccn, CERTIFICATION_DATE, QUALITY_OF_PATIENT_CARE_STAR_RATING star, FOOTNOTE_FOR_QUALITY_OF_PATIENT_CARE_STAR_RATING star_fn,
        HOW_MUCH_MEDICARE_SPENDS_ON_AN_EPISODE_OF_CARE_AT_THIS_AGENCY_COMPARED_TO_MEDICARE_SPENDING_ACROSS_ALL_AGENCIES_NATIONALLY spend,
        NO_OF_EPISODES_TO_CALC_HOW_MUCH_MEDICARE_SPENDS_PER_EPISODE_OF_CARE_AT_AGENCY_COMPARED_TO_SPENDING_AT_ALL_AGENCIES_NATIONAL eps, TYPE_OF_OWNERSHIP
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH)
select t.ccn, t.enr_dt, h.CERTIFICATION_DATE, t.INCORPORATION_DATE, t.ADDRESS_LINE_2, left(t.ORGANIZATION_NAME,32) org, t.PROPRIETARY_NONPROFIT pnp,
  h.star, left(h.star_fn,40) star_fn, h.spend, h.eps, h.TYPE_OF_OWNERSHIP
from t left join h using (ccn) order by t.enr_dt;

-- [q12] statement 12
-- Hospital REH conversions: old CCN (CAH_OR_HOSPITAL_CCN) -> FINDINGS.HOSPITAL_CLOSURE_RISK margins, vs rural hospitals in the same states that did not convert
with reh as (select ENROLLMENT_STATE st, REH_CONVERSION_DATE dt, CAH_OR_HOSPITAL_CCN raw_old, lpad(trim(split_part(CAH_OR_HOSPITAL_CCN,'|',1)),6,'0') old_ccn,
               lpad(trim(CCN),6,'0') new_ccn, ORGANIZATION_NAME, PROPRIETARY_NONPROFIT pnp
             from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS where REH_CONVERSION_FLAG='Y' or PROVIDER_TYPE_CODE='00-24'),
r as (select lpad(trim(CCN),6,'0') ccn, STATE, IS_RURAL, OPERATING_MARGIN_PCT m, NEGATIVE_OPERATING_MARGIN neg, RISK_TIER, FY_END, NET_PATIENT_REVENUE npr, MEDICAID_DEPENDENCE_PCT mcd
      from LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK),
conv as (select reh.*, r.m, r.neg, r.RISK_TIER, r.FY_END, r.npr, r.IS_RURAL, (select count(*) from r r2 where r2.ccn=reh.new_ccn) new_ccn_in_r from reh left join r on r.ccn=reh.old_ccn),
peer as (select r.* from r where r.IS_RURAL and r.STATE in (select st from reh) and r.ccn not in (select old_ccn from reh where old_ccn is not null))
select 'sum_conv' k, count(*)::text a, count(m)::text b, round(median(m),1)::text c, count_if(neg)::text d, round(median(npr)/1e6,1)::text e, sum(new_ccn_in_r)::text f, null g, null h from conv
union all select 'sum_peer', count(*)::text, count(m)::text, round(median(m),1)::text, count_if(neg)::text, round(median(npr)/1e6,1)::text, null, null, null from peer
union all select 'conv_row', st, dt::text, raw_old, left(ORGANIZATION_NAME,34), pnp, round(m,1)::text, RISK_TIER, FY_END from conv
union all select 'conv_year', year(dt)::text, count(*)::text, null, null, null, null, null, null from conv group by 2
order by 1, 2;

-- [q13] statement 13
-- Hospital enrollments: new enrollments by era (date inside ENROLLMENT_ID) and type, for-profit and psych mix; plus the pre-1900 incorporation dates
with t as (select *, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS)
select 'era' k, case when year(enr_dt)<2013 then 'a_pre2013' when year(enr_dt)<2019 then 'b_2013_18' else 'c_2019on' end a, PROVIDER_TYPE_CODE b,
  count(*) n, count_if(PROPRIETARY_NONPROFIT='P') fp, count_if(SUBGROUP_PSYCHIATRIC='Y') psych, count_if(SUBGROUP_PSYCHIATRIC='Y' and PROPRIETARY_NONPROFIT='P') psych_fp,
  count_if(SUBGROUP_LONG_TERM='Y') ltch, count_if(SUBGROUP_REHABILITATION='Y') rehab, count_if(SUBGROUP_SHORT_TERM='Y') shortterm,
  count_if(STATE='TX') tx, count_if(STATE='TX' and PROPRIETARY_NONPROFIT='P') tx_fp, count_if(enr_dt is null) bad_id
from t group by 2,3
union all select 'inc_pre1900', INCORPORATION_DATE::text, null, count(*), null, null, null, null, null, null, null, null, null from t where year(INCORPORATION_DATE)<1900 group by 2
union all select * from (select 'new_state_2019on', STATE, null, count(*), count_if(PROPRIETARY_NONPROFIT='P'), count_if(SUBGROUP_PSYCHIATRIC='Y'), null, null, null, null, null, null, null
  from t where year(enr_dt)>=2019 and PROVIDER_TYPE_CODE='00-09' group by 2 order by 4 desc limit 10)
order by 1, 2, 3;

-- [q14] statement 14
-- ASM participants -> Part B by provider (2024, RNDRNG_NPI), OIG exclusion list, opt-out list: land rate, specialty, state agreement; plus orgs whose ASM state disagrees with Part B
with a as (select NPI, any_value(STATE) st, any_value(ASM_COHORT) coh, any_value(ORGANIZATION_LEGAL_NAME) org, max(ASM_CY27_SMALLPRACTICE) sp
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS group by 1),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN bst, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
l as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
o as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS),
j as (select a.*, b.typ, b.bst, b.benes, b.pay, l.npi leie, o.npi optout from a left join b on b.npi=a.NPI left join l on l.npi=a.NPI left join o on o.npi=a.NPI)
select 'total' k, coh a, null b, count(*) n, count(typ) landed, count_if(bst=st) same_state, count(leie) leie, count(optout) optout, round(median(pay)) med_pay, round(median(benes)) med_benes
from j group by 2
union all select * from (select 'spec', coh, typ, count(*), count(typ), count_if(bst=st), count(leie), count(optout), round(median(pay)), round(median(benes)) from j where typ is not null group by 2,3 qualify row_number() over (partition by coh order by count(*) desc) <= 8)
union all select * from (select 'mismatch', org, st||'>'||listagg(distinct bst, ','), count(*), null, null, null, null, null, null from j where bst is not null and bst<>st group by org, st order by 4 desc limit 10)
order by 1, 2, 4 desc;

-- [q15] statement 15
-- OTP sites per state vs 2024 drug overdose deaths (CDC VSRR, 12 months ending December 2024, reported value; NYC folded into NY); plus sites added since 2021
with s as (select STATE st, count(distinct upper(trim(ADDRESS_LINE_1))||left(ZIP,5)) sites, count(distinct NPI) npis,
             count_if(year(MEDICARE_ID_EFFECTIVE_DATE)>=2021) since2021
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS group by 1),
d as (select iff(STATE='YC','NY',STATE) st, sum(try_to_number(replace(DATA_VALUE,',',''))) deaths, count(*) nrows
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_OVERDOSE
      where INDICATOR='Number of Drug Overdose Deaths' and PERIOD ilike '12 month%' and YEAR='2024' and (MONTH ilike 'dec%' or MONTH in ('12'))
        and STATE not in ('US') group by 1)
select coalesce(s.st, d.st) st, s.sites, s.npis, s.since2021, d.deaths, d.nrows, round(d.deaths/nullif(s.sites,0),1) deaths_per_site,
  round(median(d.deaths/nullif(s.sites,0)) over (),1) med_all
from s full outer join d on d.st=s.st
order by deaths_per_site desc nulls first;

-- [q16] statement 16
-- OTP NPIs -> Part B by provider (2024): land rate, pay per patient vs state median; reverse check: Part B 'Opioid Treatment Program' billers missing from the OTP list; OIG exclusions
with otp as (select NPI, any_value(PROVIDER_NAME) nm, any_value(STATE) st, count(*) sites from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS group by 1),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN bst, RNDRNG_PRVDR_LAST_ORG_NAME bnm, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
l as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
j as (select otp.*, b.typ, b.benes, b.pay, b.pay/nullif(b.benes,0) ppb, l.npi leie from otp left join b on b.npi=otp.NPI left join l on l.npi=otp.NPI),
jm as (select j.*, median(ppb) over (partition by st) st_med, count(ppb) over (partition by st) st_n from j)
select 'sum' k, count(*)::text a, count(typ)::text b, count_if(typ ilike '%opioid%')::text c, count(leie)::text d, round(median(ppb))::text e, round(sum(pay)/1e6,1)::text f, sum(benes)::text g, null h from j
union all select 'rev', count(*)::text, count_if(npi not in (select NPI from otp))::text, round(sum(iff(npi not in (select NPI from otp), pay, 0))/1e6,1)::text, listagg(distinct iff(npi not in (select NPI from otp), bst, null), ',')::text, null, null, null, null
  from b where typ ilike '%opioid%'
union all select * from (select 'top_ppb', NPI, left(nm,30), st, sites::text, benes::text, round(pay)::text, round(ppb)::text, round(st_med)::text||' (n='||st_n||')' from jm where ppb is not null order by ppb/nullif(st_med,0) desc limit 10)
union all select * from (select 'top_pay', NPI, left(nm,30), st, sites::text, benes::text, round(pay)::text, round(ppb)::text, round(st_med)::text from jm where pay is not null order by pay desc limit 6);

-- [q17] statement 17
-- HHA vs hospice enrollments: same street address + ZIP (two fields agree) at the biggest HHA clusters; and share of each file's 2019+ enrollments in LA-area ZIP3s
with norm as (select 'HHA' src, upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z, left(ZIP_CODE,3) z3, STATE, ASSOCIATE_ID,
                try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
              union all
              select 'HOSPICE', upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')), left(ZIP_CODE,5), left(ZIP_CODE,3), STATE, ASSOCIATE_ID,
                try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS),
n2 as (select *, (STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935'))) la from norm),
top as (select a1, z from n2 where src='HHA' group by 1,2 order by count(distinct ASSOCIATE_ID) desc limit 12)
select 'addr' k, top.a1||' '||top.z a, count_if(src='HHA') hha, count_if(src='HOSPICE') hospice, null d, null e, null f
from top join n2 using (a1, z) group by 2
union all select 'share', src, count(*), count_if(year(enr_dt)>=2019), count_if(la and year(enr_dt)>=2019), count_if(la and year(enr_dt)<2013), count_if(year(enr_dt)<2013) from n2 group by 2
order by 1, 3 desc;

-- [q18] statement 18
-- ASM eyeball: the participants whose NPI is on the OIG exclusion list or the Medicare opt-out list, with both names so the match can be checked
with a as (select NPI, any_value(FIRST_NAME||' '||LAST_NAME) nm, any_value(STATE) st, any_value(ASM_COHORT) coh, any_value(ORGANIZATION_LEGAL_NAME) org
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS group by 1),
l as (select trim(NPI) npi, EXCLUSION_TYPE, EXCLUSION_DATE, REINSTATEMENT_DATE, WAS_REINSTATED, HAS_WAIVER, LAST_NAME, FIRST_NAME, STATE, SPECIALTY
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
o as (select trim(NPI) npi, OPTOUT_EFFECTIVE_DATE, OPTOUT_END_DATE, SPECIALTY, FIRST_NAME, LAST_NAME, STATE_CODE, LAST_UPDATED
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS)
select 'leie' k, a.NPI, a.nm, a.st, a.coh, left(a.org,30) org, l.EXCLUSION_TYPE x1, l.EXCLUSION_DATE::text x2, l.REINSTATEMENT_DATE::text x3,
  l.FIRST_NAME||' '||l.LAST_NAME x4, l.STATE x5, l.WAS_REINSTATED::text||'/'||l.HAS_WAIVER::text x6, l.SPECIALTY x7
from a join l on l.npi=a.NPI
union all
select 'optout', a.NPI, a.nm, a.st, a.coh, left(a.org,30), o.SPECIALTY, o.OPTOUT_EFFECTIVE_DATE::text, o.OPTOUT_END_DATE::text,
  o.FIRST_NAME||' '||o.LAST_NAME, o.STATE_CODE, o.LAST_UPDATED::text, null
from a join o on o.npi=a.NPI
order by 1, 8;

-- [q19] statement 19
-- CDC portal: datasets whose own description says they update weekly/monthly, and how many have not had new data in 6 or 12 months before the 2026-08-11 pull; last-data-update month since mid-2024; top stale 'weekly' non-COVID datasets
with t as (select *, case when DESCRIPTION ilike '%updated weekly%' or DESCRIPTION ilike '%weekly basis%' or DESCRIPTION ilike '%updated each week%' or DESCRIPTION ilike '%updated every week%' then 'weekly'
                         when DESCRIPTION ilike '%updated monthly%' or DESCRIPTION ilike '%monthly basis%' or DESCRIPTION ilike '%updated each month%' then 'monthly' else 'other' end freq,
                    (DATASET_NAME ilike '%covid%' or DESCRIPTION ilike '%covid%' or DATASET_NAME ilike '%sars-cov%') covid
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DATA_PORTAL where RESOURCE_TYPE='dataset')
select 'freq' k, freq a, covid::text b, count(*) n, count_if(DATA_UPDATED_AT < '2026-02-11') stale6m, count_if(DATA_UPDATED_AT < '2025-08-11') stale12m, sum(DOWNLOAD_COUNT) dl, null c
from t group by 2,3
union all select 'lastdata_month', to_char(DATA_UPDATED_AT,'YYYY-MM'), null, count(*), count_if(freq='weekly'), count_if(covid), sum(DOWNLOAD_COUNT), null from t where DATA_UPDATED_AT >= '2024-07-01' group by 2
union all select * from (select 'stale_weekly', left(DATASET_NAME,60), DOMAIN_CATEGORY, DOWNLOAD_COUNT, null, null, null, to_char(DATA_UPDATED_AT,'YYYY-MM-DD')||' created '||to_char(CREATED_AT,'YYYY-MM-DD')
  from t where freq='weekly' and not covid and DATA_UPDATED_AT < '2026-02-11' order by DOWNLOAD_COUNT desc limit 15)
order by 1, 2;

-- [q20] statement 20
-- OTP completeness: Part B 2024 'Opioid Treatment Program' billers whose NPI is not in the OTP list, by state, and whether their name+state is in the list under another NPI
with otp as (select NPI, upper(PROVIDER_NAME) nm, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS),
b as (select RNDRNG_NPI npi, upper(RNDRNG_PRVDR_LAST_ORG_NAME) bnm, RNDRNG_PRVDR_STATE_ABRVTN bst, RNDRNG_PRVDR_CITY city, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER where RNDRNG_PRVDR_TYPE ilike '%opioid%'),
miss as (select b.*, exists(select 1 from otp where otp.STATE=b.bst and left(otp.nm,12)=left(b.bnm,12)) name_state_in_list from b where b.npi not in (select NPI from otp))
select 'state' k, bst a, count(*)::text b, count_if(name_state_in_list)::text c, round(sum(pay)/1e6,2)::text d, sum(benes)::text e, null f
from miss group by 2
union all select * from (select 'row', npi, left(bnm,34), bst||' '||city, name_state_in_list::text, benes::text, round(pay)::text from miss order by pay desc limit 12)
order by 1, 2;

-- [q21] statement 21
-- ASM peer comparison: participants vs same-specialty clinicians in the same states who are not in the model (Part B 2024): headcount share vs Medicare payment share, median pay and patients
with a as (select NPI, any_value(ASM_COHORT) coh from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS group by 1),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st, try_to_number(TOT_BENES) benes, TOT_MDCR_PYMT_AMT pay
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
      where RNDRNG_PRVDR_TYPE in ('Cardiology','Physical Medicine and Rehabilitation','Orthopedic Surgery','Pain Management','Anesthesiology','Interventional Pain Management','Neurosurgery')),
sts as (select distinct b.typ, b.st from b join a on a.NPI=b.npi),
j as (select b.*, (a.NPI is not null) inmodel from b join sts using (typ, st) left join a on a.NPI=b.npi)
select typ, count(*) clinicians, count_if(inmodel) in_model, round(100*count_if(inmodel)/count(*),1) pct_heads,
  round(100*sum(iff(inmodel,pay,0))/sum(pay),1) pct_pay, round(median(iff(inmodel,pay,null))) med_pay_in, round(median(iff(not inmodel,pay,null))) med_pay_out,
  round(median(iff(inmodel,benes,null))) med_benes_in, round(median(iff(not inmodel,benes,null))) med_benes_out, count(distinct st) states
from j group by 1 order by 2 desc;

-- [q22] statement 22
-- HHA robustness: exact state shares by era (STATE column, no ZIP approximation); top ZIP3 prefixes nationally for 2019+ enrollments; HHA NPIs on the OIG exclusion list
with t as (select NPI, STATE, left(ZIP_CODE,3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
l as (select trim(NPI) npi, EXCLUSION_DATE, EXCLUSION_TYPE, BUSINESS_NAME from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL)
select * from (select 'state' k, STATE a, count_if(year(enr_dt)>=2019) b, count_if(year(enr_dt)<2013) c, count_if(year(enr_dt) between 2013 and 2018) d, count(*) e
  from t group by 2 order by 3 desc limit 8)
union all select 'nat', 'all', count_if(year(enr_dt)>=2019), count_if(year(enr_dt)<2013), count_if(year(enr_dt) between 2013 and 2018), count(*) from t
union all select * from (select 'zip3', STATE||' '||z3, count_if(year(enr_dt)>=2019), count_if(year(enr_dt)<2013), count_if(year(enr_dt) between 2013 and 2018), count(*)
  from t group by 2 order by 3 desc limit 14)
union all select 'leie', l.BUSINESS_NAME||' | '||t.STATE||' | '||l.EXCLUSION_TYPE, year(l.EXCLUSION_DATE), year(t.enr_dt), null, null from t join l on l.npi=trim(t.NPI)
order by 1, 3 desc;

-- [q23] statement 23
-- ASM base rate: share of same-specialty, same-state Part B 2024 clinicians NOT in the model who are on the OIG list or the opt-out list; plus when the ASM table was loaded (mart + landing metadata)
with a as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
      where RNDRNG_PRVDR_TYPE in ('Cardiology','Physical Medicine and Rehabilitation','Orthopedic Surgery','Pain Management','Anesthesiology','Interventional Pain Management','Neurosurgery')),
l as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
o as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS)
select 'base' k, iff(a.NPI is null,'not_in_model','in_model') a, count(*)::text b, count(l.npi)::text c, count(o.npi)::text d, round(100*count(l.npi)/count(*),3)::text e, round(100*count(o.npi)/count(*),3)::text f
from b left join a on a.NPI=b.npi left join l on l.npi=b.npi left join o on o.npi=b.npi group by 2
union all select 'mart_meta', table_name, row_count::text, created::text, last_altered::text, null, null from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%AMBULATORY_SPECIALTY%'
union all select 'landing_meta', table_name, row_count::text, created::text, last_altered::text, null, null from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike '%AMBULATORY%' or table_name ilike '%ASM%PARTIC%';

-- [q24] statement 24
-- HHA owners behind 2019+ enrollments (HOME_HEALTH_OWNERS by ENROLLMENT_ID): Valley/Glendale/Burbank ZIP3 912-916 vs rest of US; how many agencies sit with an individual owner who holds 3+ agencies anywhere
with t as (select ENROLLMENT_ID, STATE, left(ZIP_CODE,3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
o as (select ENROLLMENT_ID, ASSOCIATE_ID_OWNER, TYPE_OWNER, OWNER_NAME, ROLE_TEXT_OWNER from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS),
reach as (select ASSOCIATE_ID_OWNER, count(distinct ENROLLMENT_ID) n_agencies from o where TYPE_OWNER='I' group by 1),
nt as (select t.*, iff(STATE='CA' and z3 between '912' and '916','valley','restUS') rg from t where year(enr_dt)>=2019),
jo as (select nt.rg, nt.ENROLLMENT_ID, o.ASSOCIATE_ID_OWNER, o.OWNER_NAME, r.n_agencies from nt join o using (ENROLLMENT_ID) join reach r using (ASSOCIATE_ID_OWNER) where o.TYPE_OWNER='I'),
per as (select rg, ENROLLMENT_ID, count(distinct ASSOCIATE_ID_OWNER) owners, max(n_agencies) max_reach from jo group by 1,2)
select 'grp' k, rg a, (select count(*) from nt where nt.rg=per.rg)::text b, count(*)::text c, round(median(owners),1)::text d,
  count_if(max_reach>=3)::text e, round(100*count_if(max_reach>=3)/count(*),1)::text f, null g
from per group by rg
union all select * from (select 'top_owner', any_value(OWNER_NAME), rg, count(distinct ENROLLMENT_ID)::text, max(n_agencies)::text, null, null, null
  from jo group by ASSOCIATE_ID_OWNER, rg order by count(distinct ENROLLMENT_ID) desc limit 12);

-- [q25] statement 25
-- HHA eyeball: the one HHA NPI that matched the OIG exclusion list, both names side by side
select h.NPI, h.ORGANIZATION_NAME, h.DOING_BUSINESS_AS_NAME, h.CITY, h.STATE, h.ENROLLMENT_ID, l.BUSINESS_NAME, l.LAST_NAME, l.FIRST_NAME, l.GENERAL_CATEGORY, l.SPECIALTY,
  l.EXCLUSION_TYPE, l.EXCLUSION_DATE, l.CITY lcity, l.STATE lstate
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS h
join LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l on trim(l.NPI)=trim(h.NPI) and l.NPI_IS_REAL;
