with mme as (
  select BUYER_COUNTY_FIPS fips, sum(TOTAL_MME) mme, sum(DOSAGE_UNITS) pills
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS where BUYER_COUNTY_FIPS is not null and TRANSACTION_CODE = 'S' group by 1),
od as (
  select GEOID fips, avg(RATE) od_rate_19_24, count(*) yrs from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY where INTENT = 'Drug_OD' and PERIOD in ('2019','2020','2021','2022','2023','2024') and RATE >= 0 and COUNT_SUP is not null group by 1 having count(*) = 6),
j as (
  select c.COUNTY_FIPS, c.COUNTY_NAME, c.STATE_NAME, c.POPULATION_2020 pop, mme.mme/7/nullif(c.POPULATION_2020,0) mme_per_cap_yr, mme.pills/7/nullif(c.POPULATION_2020,0) pills_per_cap_yr, od.od_rate_19_24
  from LIBRARY_MARTS.CORE.DIM_COUNTY c join mme on mme.fips = c.COUNTY_FIPS join od on od.fips = c.COUNTY_FIPS where c.POPULATION_2020 >= 20000),
dec as (select j.*, ntile(10) over (order by mme_per_cap_yr) mme_decile from j)
select mme_decile, count(*) counties, round(avg(mme_per_cap_yr)) avg_mme_per_cap_yr, round(avg(pills_per_cap_yr),1) avg_pills_per_cap_yr, round(avg(od_rate_19_24),1) avg_od_rate_19_24, round(median(od_rate_19_24),1) med_od_rate
from dec group by 1 order by 1;
with mme as (
  select BUYER_COUNTY_FIPS fips, sum(TOTAL_MME) mme, sum(DOSAGE_UNITS) pills
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS where BUYER_COUNTY_FIPS is not null and TRANSACTION_CODE = 'S' group by 1),
od as (
  select GEOID fips, avg(RATE) od_rate_19_24, count(*) yrs from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY where INTENT = 'Drug_OD' and PERIOD in ('2019','2020','2021','2022','2023','2024') and RATE >= 0 and COUNT_SUP is not null group by 1 having count(*) = 6)
select c.COUNTY_NAME, c.STATE_NAME, c.POPULATION_2020 pop, round(mme.pills/7/nullif(c.POPULATION_2020,0),1) pills_per_cap_yr, round(od.od_rate_19_24,1) od_rate_19_24
from LIBRARY_MARTS.CORE.DIM_COUNTY c join mme on mme.fips = c.COUNTY_FIPS join od on od.fips = c.COUNTY_FIPS where c.POPULATION_2020 >= 20000
order by pills_per_cap_yr desc limit 25;
select TRANSACTION_CODE, count(*) n from LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS group by 1 order by 2 desc
