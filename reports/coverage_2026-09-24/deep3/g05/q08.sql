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
group by 1,2,3 order by 1,2,3
