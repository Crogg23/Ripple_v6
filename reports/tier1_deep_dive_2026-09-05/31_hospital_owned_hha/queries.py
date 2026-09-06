"""Hunch 31: hospital-owned home health agencies vs independent. Every query, one place.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/31_hospital_owned_hha/queries.py
Writes data.json next to this file for story.py."""
import json, decimal
from pathlib import Path
from _shared import q

HERE = Path(__file__).resolve().parent
q.open_log(HERE / "queries.log")

HH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH"
HE = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS"
HO = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS"
SP = "HOW_MUCH_MEDICARE_SPENDS_ON_AN_EPISODE_OF_CARE_AT_THIS_AGENCY_COMPARED_TO_MEDICARE_SPENDING_ACROSS_ALL_AGENCIES_NATIONALLY"
EP = "NO_OF_EPISODES_TO_CALC_HOW_MUCH_MEDICARE_SPENDS_PER_EPISODE_OF_CARE_AT_AGENCY_COMPARED_TO_SPENDING_AT_ALL_AGENCIES_NATIONAL"

# hospital-owned = the HHA's PECOS enrollment shares an ASSOCIATE_ID (the enrolling organisation) with a hospital enrollment.
BASE = f"""with owned as (select distinct e.CCN from {HE} e join {HO} h on h.ASSOCIATE_ID = e.ASSOCIATE_ID),
enr as (select distinct CCN from {HE}),
g as (select c.*,
  case when o.CCN is not null then 'hospital-owned' when n.CCN is not null then 'independent' else 'not in PECOS' end grp,
  try_to_number(QUALITY_OF_PATIENT_CARE_STAR_RATING, 3, 1) star,
  try_to_number({SP}, 10, 2) spend,
  try_to_number({EP}) eps,
  case when try_to_number({EP}) is null then '0 none' when try_to_number({EP}) < 100 then '1 <100'
       when try_to_number({EP}) < 250 then '2 100-249' when try_to_number({EP}) < 500 then '3 250-499' else '4 500+' end band
  from {HH} c left join owned o on o.CCN = c.CCN left join enr n on n.CCN = c.CCN)"""

out = {}

# --- traps first: is CCN a key, is ASSOCIATE_ID a key, what does the star column hold
out["hh_keys"] = q.run(f"select count(*) n, count(distinct CCN) d, min(length(CCN)) mn, max(length(CCN)) mx from {HH}", "HH ccn is a key")
out["he_keys"] = q.run(f"select count(*) n, count(distinct CCN) d, count(distinct ASSOCIATE_ID) a, count(distinct NPI) npi, sum(iff(length(CCN)=7,1,0)) suffixed from {HE}", "HE keys")
out["ho_keys"] = q.run(f"select count(*) n, count(distinct CCN) d, count(distinct ASSOCIATE_ID) a from {HO}", "HO keys")
out["star_values"] = q.run(f"select QUALITY_OF_PATIENT_CARE_STAR_RATING s, count(*) n from {HH} group by 1 order by 1", "star raw values")
out["star_footnotes"] = q.run(BASE + " select grp, FOOTNOTE_FOR_QUALITY_OF_PATIENT_CARE_STAR_RATING f, count(*) n from g where star is null group by 1,2 order by 1,3 desc", "why star is blank")
out["survey_tables"] = q.run("select table_schema, table_name from LIBRARY_RAW.information_schema.tables where table_name ilike '%HHCAHPS%' or table_name ilike '%PATIENT_SURVEY%' or table_name ilike '%HOME_HEALTH%' order by 1,2", "is a patient-survey star landed anywhere")
out["suffix_parents"] = q.run(f"select count(*) n, sum(iff(p.CCN is not null,1,0)) parent_in_care_compare from (select CCN from {HE} where length(CCN)=7) s left join {HH} p on p.CCN = left(s.CCN,6)", "7-char CCNs are branches of a 6-char parent")
out["owned_stripped"] = q.run(f"select count(distinct left(e.CCN,6)) hha from {HE} e join {HO} h on h.ASSOCIATE_ID = e.ASSOCIATE_ID", "owned count, suffix stripped")

# --- who owns
out["owners"] = q.run(f"select count(distinct h.ASSOCIATE_ID) systems, count(distinct h.CCN) hospital_ccn, count(distinct e.CCN) hha from {HE} e join {HO} h on h.ASSOCIATE_ID = e.ASSOCIATE_ID", "how many systems own how many HHAs")
out["big_owners"] = q.run(f"select e.ASSOCIATE_ID, min(h.ORGANIZATION_NAME) hosp, count(distinct e.CCN) hhas from {HE} e join {HO} h on h.ASSOCIATE_ID = e.ASSOCIATE_ID group by 1 order by 3 desc limit 8", "biggest owners")
out["name_check"] = q.run(BASE + " select grp, sum(iff(regexp_like(upper(PROVIDER_NAME),'.*(HOSPITAL|MEDICAL CENTER|HEALTH SYSTEM|CLINIC|HEALTHCARE SYSTEM).*'),1,0)) namehit, count(*) n from g group by 1 order by 1", "second way: hospital-ish names by group")
out["cc_ownership"] = q.run(BASE + " select grp, TYPE_OF_OWNERSHIP, count(*) n, round(avg(star),2) mean_star, round(avg(spend),3) mean_spend from g group by 1,2 order by 1,3 desc", "care compare ownership type by group")

# --- the first-pass number, rebuilt
out["by_group"] = q.run(BASE + """ select grp, count(*) n,
  sum(iff(star is null,1,0)) star_missing, round(100*avg(iff(star is null,1,0)),1) pct_star_missing,
  round(avg(star),2) mean_star, median(star) med_star,
  sum(iff(spend is null,1,0)) spend_missing, round(avg(spend),3) mean_spend, median(spend) med_spend,
  sum(iff(eps is null,1,0)) eps_missing, median(eps) med_eps,
  median(datediff('year', CERTIFICATION_DATE, '2026-07-01')) med_age_yrs
  from g group by 1 order by 1""", "headline by group")
out["star_dist"] = q.run(BASE + " select grp, star, count(*) n from g where star is not null group by 1,2 order by 1,2", "star distribution")
out["star_lowhigh"] = q.run(BASE + " select grp, count(star) rated, round(100*sum(iff(star<=2,1,0))/count(star),1) pct_low, round(100*sum(iff(star>=4,1,0))/count(star),1) pct_high from g group by 1 order by 1", "share 2 stars or under, 4 or over")

# --- missingness is volume
out["by_band"] = q.run(BASE + """ select band, grp, count(*) n, round(100*avg(iff(star is null,1,0)),1) pct_star_missing,
  round(avg(star),2) mean_star, round(avg(spend),3) mean_spend, round(100*avg(iff(spend is null,1,0)),1) pct_spend_missing
  from g where grp <> 'not in PECOS' group by 1,2 order by 1,2""", "by episode band")
out["band_all"] = q.run(BASE + " select band, count(*) n, round(100*avg(iff(star is null,1,0)),1) pct_star_missing from g group by 1 order by 1", "missing star by band, everyone")

# --- outcomes
out["outcomes"] = q.run(BASE + """ select grp, count(*) n,
  round(avg(DTC_RISK_STANDARDIZED_RATE),2) dtc, sum(iff(DTC_RISK_STANDARDIZED_RATE is null,1,0)) dtc_miss,
  round(avg(PPH_RISK_STANDARDIZED_RATE),2) pph, sum(iff(PPH_RISK_STANDARDIZED_RATE is null,1,0)) pph_miss,
  round(avg(PPR_RISK_STANDARDIZED_RATE),2) ppr, sum(iff(PPR_RISK_STANDARDIZED_RATE is null,1,0)) ppr_miss,
  round(avg(try_to_number(HOW_OFTEN_PATIENTS_GOT_BETTER_AT_WALKING_OR_MOVING_AROUND,6,2)),2) walk,
  round(avg(try_to_number(HOW_OFTEN_THE_HOME_HEALTH_TEAM_BEGAN_THEIR_PATIENTS_CARE_IN_A_TIMELY_MANNER,6,2)),2) timely,
  round(avg(PERCENT_OF_RESIDENTS_EXPERIENCING_ONE_OR_MORE_FALLS_WITH_MAJOR_INJURY),2) falls
  from g group by 1 order by 1""", "outcome rates by group")
out["dtc_cat"] = q.run(BASE + " select grp, DTC_PERFORMANCE_CATEGORIZATION cat, count(*) n from g group by 1,2 order by 1,2", "discharge-to-community category")
out["pph_cat"] = q.run(BASE + " select grp, PPH_PERFORMANCE_CATEGORIZATION cat, count(*) n from g group by 1,2 order by 1,2", "preventable hospitalization category")

# --- the fair fight: volume-matched cohort, 100+ episodes
out["cohort"] = q.run(BASE + """ select grp, count(star) n_star, round(avg(star),3) mean_star, round(stddev(star),3) sd_star,
  count(spend) n_spend, round(avg(spend),4) mean_spend, round(stddev(spend),4) sd_spend,
  round(avg(DTC_RISK_STANDARDIZED_RATE),2) dtc, round(stddev(DTC_RISK_STANDARDIZED_RATE),2) sd_dtc,
  round(avg(PPH_RISK_STANDARDIZED_RATE),2) pph, round(stddev(PPH_RISK_STANDARDIZED_RATE),2) sd_pph,
  round(100*avg(iff(star is null,1,0)),1) pct_star_missing
  from g where eps >= 100 and grp <> 'not in PECOS' group by 1 order by 1""", "cohort 100+ episodes")
out["cohort_prop"] = q.run(BASE + " select grp, count(*) n, round(avg(star),2) mean_star, round(avg(spend),3) mean_spend from g where eps >= 100 and grp <> 'not in PECOS' and TYPE_OF_OWNERSHIP = 'PROPRIETARY' group by 1 order by 1", "cohort, for-profit only")
out["spend_hist"] = q.run(BASE + " select grp, floor(spend*20)/20 bin, count(*) n from g where spend is not null and grp <> 'not in PECOS' group by 1,2 order by 1,2", "spend histogram")
out["spend_above"] = q.run(BASE + " select grp, count(spend) n, round(100*sum(iff(spend>1.0,1,0))/count(spend),1) pct_above_national from g where grp <> 'not in PECOS' group by 1 order by 1", "share above national spend")

# --- states
out["states"] = q.run(BASE + """ select STATE, sum(iff(grp='hospital-owned',1,0)) owned_n, sum(iff(grp='independent',1,0)) ind_n,
  round(100*avg(iff(grp='hospital-owned' and star is null,1,0))/nullif(avg(iff(grp='hospital-owned',1,0)),0),1) owned_miss,
  round(100*avg(iff(grp='independent' and star is null,1,0))/nullif(avg(iff(grp='independent',1,0)),0),1) ind_miss,
  round(avg(iff(grp='hospital-owned',star,null)),2) owned_star, round(avg(iff(grp='independent',star,null)),2) ind_star,
  round(avg(iff(grp='hospital-owned',spend,null)),3) owned_spend, round(avg(iff(grp='independent',spend,null)),3) ind_spend
  from g where grp <> 'not in PECOS' group by 1 order by owned_n desc""", "state breakdown")

# --- skeptic fixes: episode-weighted spend, blanks inside the cohort, episode column ceiling
out["spend_weighted"] = q.run(BASE + " select grp, count(spend) n, round(sum(spend*eps)/sum(eps),4) weighted_spend, round(avg(spend),4) plain_spend from g where eps >= 100 and grp <> 'not in PECOS' and spend is not null group by 1 order by 1", "cohort spend, weighted by episodes")
out["spend_by_band"] = q.run(BASE + " select band, grp, count(spend) n, round(avg(spend),4) plain_spend, round(sum(spend*eps)/sum(eps),4) weighted_spend from g where eps >= 100 and grp <> 'not in PECOS' and spend is not null group by 1,2 order by 1,2", "spend gap by band")
out["cohort_blanks"] = q.run(BASE + " select grp, iff(star is null,'blank','rated') has_star, count(*) n, round(avg(DTC_RISK_STANDARDIZED_RATE),1) dtc, round(avg(spend),4) spend from g where eps >= 100 and grp <> 'not in PECOS' group by 1,2 order by 1,2", "blanks still inside the cohort, and how they score")
out["eps_ceiling"] = q.run(BASE + " select max(eps) mx, sum(iff(eps=998,1,0)) at_998, sum(iff(eps>=500,1,0)) band_500 from g", "episode column ceiling")


def conv(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
    return str(o)

json.dump(out, open(HERE / "data.json", "w"), default=conv, indent=1)
print("wrote", HERE / "data.json")
