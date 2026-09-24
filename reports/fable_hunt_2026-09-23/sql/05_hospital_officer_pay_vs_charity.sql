select IS_OFFICER, IS_KEY_EMPLOYEE, IS_HIGHEST_COMPENSATED, IS_TRUSTEE_OR_DIRECTOR, count(*) n, round(avg(REPORTABLE_COMP_FROM_ORG)) avg_comp from LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY where TAX_YEAR='2022' group by 1,2,3,4 order by n desc limit 12;
with pay as (
  select EIN, max(HOSPITAL_NAME) hname, max(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) top_comp_org, max_by(PERSON_NAME, REPORTABLE_COMP_FROM_ORG) top_person, max_by(TITLE, REPORTABLE_COMP_FROM_ORG) top_title,
    sum(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) officer_comp_from_org, count(*) officers
  from LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY where TAX_YEAR = '2022' and not IS_GROUP_RETURN and not IS_FORMER and (IS_OFFICER or IS_KEY_EMPLOYEE) and not IS_HIGHEST_COMPENSATED group by 1),
hc as (
  select PROVIDER_CCN, max(HOSPITAL_NAME) hname, max(STATE_CODE) st, sum(NUMBER_OF_BEDS) beds, sum(COST_OF_CHARITY_CARE) charity, sum(TOTAL_BAD_DEBT_EXPENSE) bad_debt, sum(TOTAL_DISCHARGES_ALL) discharges
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS where year(FISCAL_YEAR_END_DATE) = 2022 group by 1 having sum(COST_OF_CHARITY_CARE) > 0),
j as (
  select hc.*, pay.top_comp_org, pay.top_person, pay.top_title, pay.officer_comp_from_org, pay.officers, x.EIN
  from LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN x join pay on pay.EIN = x.EIN join hc on hc.PROVIDER_CCN = x.CCN where x.MATCH_TIER <= 2 and x.PROPRIETARY_NONPROFIT = 'N')
select count(*) hospitals, sum(iff(top_comp_org > charity,1,0)) top_officer_over_charity, round(100*sum(iff(top_comp_org > charity,1,0))/count(*),1) pct_top,
  sum(iff(officer_comp_from_org > charity,1,0)) all_officers_over_charity, round(100*sum(iff(officer_comp_from_org > charity,1,0))/count(*),1) pct_all,
  round(median(top_comp_org)) med_top_officer, round(median(charity)) med_charity, round(sum(officer_comp_from_org)/1e9,2) officer_comp_bn, round(sum(charity)/1e9,2) charity_bn, round(sum(beds)) beds from j;
with pay as (
  select EIN, max(HOSPITAL_NAME) hname, max(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) top_comp_org, max_by(PERSON_NAME, REPORTABLE_COMP_FROM_ORG) top_person, max_by(TITLE, REPORTABLE_COMP_FROM_ORG) top_title,
    sum(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) officer_comp_from_org, count(*) officers
  from LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY where TAX_YEAR = '2022' and not IS_GROUP_RETURN and not IS_FORMER and (IS_OFFICER or IS_KEY_EMPLOYEE) and not IS_HIGHEST_COMPENSATED group by 1),
hc as (
  select PROVIDER_CCN, max(HOSPITAL_NAME) hname, max(STATE_CODE) st, sum(NUMBER_OF_BEDS) beds, sum(COST_OF_CHARITY_CARE) charity, sum(TOTAL_BAD_DEBT_EXPENSE) bad_debt, sum(TOTAL_DISCHARGES_ALL) discharges
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS where year(FISCAL_YEAR_END_DATE) = 2022 group by 1 having sum(COST_OF_CHARITY_CARE) > 0)
select hc.hname, hc.st, hc.PROVIDER_CCN ccn, x.EIN, hc.beds, hc.discharges, round(hc.charity/1e6,2) charity_m, round(pay.top_comp_org/1e6,2) top_officer_m, pay.top_person, pay.top_title, round(pay.officer_comp_from_org/1e6,1) all_officers_m, pay.officers, round(pay.top_comp_org/hc.charity,1) ratio
from LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN x join pay on pay.EIN = x.EIN join hc on hc.PROVIDER_CCN = x.CCN
where x.MATCH_TIER <= 2 and x.PROPRIETARY_NONPROFIT = 'N' and hc.discharges >= 5000 and pay.top_comp_org > hc.charity order by ratio desc limit 25;
with pay as (
  select EIN, sum(REPORTABLE_COMP_FROM_ORG + coalesce(OTHER_COMPENSATION,0)) officer_comp_from_org
  from LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY where TAX_YEAR = '2022' and not IS_GROUP_RETURN and not IS_FORMER and (IS_OFFICER or IS_KEY_EMPLOYEE) and not IS_HIGHEST_COMPENSATED group by 1),
hc as (
  select PROVIDER_CCN, max(STATE_CODE) st, sum(NUMBER_OF_BEDS) beds, sum(COST_OF_CHARITY_CARE) charity, sum(TOTAL_DISCHARGES_ALL) discharges
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS where year(FISCAL_YEAR_END_DATE) = 2022 group by 1 having sum(COST_OF_CHARITY_CARE) > 0)
select hc.st, count(*) hospitals, sum(iff(pay.officer_comp_from_org > hc.charity,1,0)) officers_over_charity, round(100*sum(iff(pay.officer_comp_from_org > hc.charity,1,0))/count(*)) pct
from LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN x join pay on pay.EIN = x.EIN join hc on hc.PROVIDER_CCN = x.CCN
where x.MATCH_TIER <= 2 and x.PROPRIETARY_NONPROFIT = 'N' group by 1 having count(*) >= 15 order by pct desc
