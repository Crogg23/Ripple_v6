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
order by deaths_per_site desc nulls first
