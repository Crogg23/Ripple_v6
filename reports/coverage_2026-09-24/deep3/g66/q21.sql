-- Google, eyeball rows: official House/Senate accounts with spend in weeks starting inside the last 60 days before a general election.
-- q19 showed nearly every office stops in the week that crosses the 60-day line; these are the ones that did not.
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND
      where try_to_number(SPEND_USD) > 0
        and (upper(ADVERTISER_NAME) like '%HOUSE OF REPRESENTATIVES%' or upper(ADVERTISER_NAME) like '%- U.S. SENATE%'
             or upper(ADVERTISER_NAME) like 'OFFICE OF REP%' or upper(ADVERTISER_NAME) like 'OFFICE OF SENATOR%')
        and upper(ADVERTISER_NAME) not like '% FOR %'),
e as (select column1::date ed from values ('2018-11-06'),('2020-11-03'),('2022-11-08'),('2024-11-05'))
select w.nm, w.id, left(a.p,25) public_id, e.ed election, w.wk, datediff(day, w.wk, e.ed) days_before, w.usd
from w join e on w.wk >= dateadd(day,-60,e.ed) and w.wk < e.ed
left join a on a.id = w.id
order by w.nm, w.wk
