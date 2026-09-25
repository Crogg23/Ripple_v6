-- Google: congressional OFFICIAL office accounts (names like 'REP. X - U.S. HOUSE OF REPRESENTATIVES'), which are paid with public money.
-- House rules bar unsolicited mass communications (paid ads included) in the 90 days before an election the Member is on the ballot for
-- (Senate: 60 days). Test: spend in weeks starting inside the 90 (60) days before each general election day,
-- vs spend in the 90 (60) days just before that window. Also: which IDs these accounts gave Google.
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
o as (select distinct id from w
      where (upper(nm) like '%U.S. HOUSE OF REPRESENTATIVES%' or upper(nm) like '%- U.S. SENATE%' or upper(nm) like 'OFFICE OF CONGRESS%'
             or upper(nm) like 'OFFICE OF SENATOR%' or upper(nm) like 'OFFICE OF REP%' or upper(nm) like 'CONGRESSMAN %' or upper(nm) like 'CONGRESSWOMAN %')
        and upper(nm) not like '% FOR %'),
e as (select column1::date ed from values ('2018-11-06'),('2020-11-03'),('2022-11-08'),('2024-11-05')),
x as (select w.id, w.nm, w.wk, w.usd, iff(upper(w.nm) like '%SENATE%', 60, 90) bdays, e.ed,
        case when w.wk >= dateadd(day, -iff(upper(w.nm) like '%SENATE%', 60, 90), e.ed) and w.wk < e.ed then 'blackout'
             when w.wk >= dateadd(day, -2*iff(upper(w.nm) like '%SENATE%', 60, 90), e.ed) and w.wk < dateadd(day, -iff(upper(w.nm) like '%SENATE%', 60, 90), e.ed) then 'before' end zone
      from w join o on o.id = w.id left join e on w.wk between dateadd(day,-200,e.ed) and dateadd(day,-1,e.ed)),
per as (select id, any_value(nm) nm, count(distinct wk) wks,
          min(wk) first_wk, max(wk) last_wk,
          sum(iff(zone='blackout', usd, 0)) blackout_usd, count(distinct iff(zone='blackout', wk, null)) blackout_wks,
          sum(iff(zone='before', usd, 0)) before_usd,
          listagg(distinct iff(zone='blackout', year(ed)::text, null), ',') blackout_years
        from x group by id),
tot as (select id, sum(usd) total_usd from w where id in (select id from o) group by id)
select 'summary' k, count(*)::text c1, count_if(blackout_usd > 0)::text c2, sum(blackout_usd)::text c3, sum(before_usd)::text c4,
  (select sum(total_usd) from tot)::text c5, (select count(distinct p) from a where id in (select id from o))::text c6,
  (select listagg(p, ' | ') from (select p, count(*) n from a where id in (select id from o) group by 1 order by n desc limit 4))::text c7, null c8
from per
union all
select * from (select 'office', per.nm, per.id, tot.total_usd::text, per.blackout_usd::text, per.blackout_wks::text, per.before_usd::text,
  coalesce(per.blackout_years,'') || ' | ' || per.first_wk || '..' || per.last_wk, left(a.p, 30)
  from per join tot on tot.id = per.id left join a on a.id = per.id order by per.blackout_usd desc, tot.total_usd desc limit 40)
