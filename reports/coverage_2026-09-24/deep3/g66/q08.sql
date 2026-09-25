-- Google weekly US spend, same window across cycles: Jan 1 of the off-year to Aug 2 of the election year.
-- Split by what ID the advertiser gave Google (FEC ID / EIN only / blank / other), plus spend by advertisers new that cycle, plus top-10 share.
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p,
             case when regexp_like(PUBLIC_IDS_LIST, '.*C[0-9]{8}.*') then 'FEC'
                  when PUBLIC_IDS_LIST ilike '%EIN ID%' then 'EIN_only'
                  when PUBLIC_IDS_LIST is null or trim(PUBLIC_IDS_LIST)='' then 'blank' else 'other' end idtype
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS),
w as (select ADVERTISER_ID id, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
fst as (select id, min(wk) first_wk from w group by 1),
cyc as (select column1 cy from values (2020),(2022),(2024),(2026)),
x as (select cy, w.id, coalesce(a.idtype,'no_stats') idtype, iff(f.first_wk >= date_from_parts(cy-1,1,1), 'new', 'returning') newness, sum(usd) usd
      from w join cyc on w.wk between date_from_parts(cy-1,1,1) and date_from_parts(cy,8,2)
      left join a on a.id = w.id join fst f on f.id = w.id
      group by 1,2,3,4),
rk as (select cy, id, usd, row_number() over (partition by cy order by usd desc) r, sum(usd) over (partition by cy) tot from x)
select 'by_idtype' k, cy::text c1, idtype c2, sum(usd)::text c3, count(*)::text c4, round(100*ratio_to_report(sum(usd)) over (partition by cy),1)::text c5 from x group by cy, idtype
union all
select 'by_newness', cy::text, newness, sum(usd)::text, count(*)::text, round(100*ratio_to_report(sum(usd)) over (partition by cy),1)::text from x group by cy, newness
union all
select 'new_by_idtype', cy::text, idtype, sum(usd)::text, count(*)::text, null from x where newness='new' group by cy, idtype
union all
select 'top10_share', cy::text, null, sum(iff(r<=10,usd,0))::text, max(tot)::text, round(100*sum(iff(r<=10,usd,0))/max(tot),1)::text from rk group by cy
union all
select 'median_adv', cy::text, null, median(usd)::text, count(*)::text, null from x group by cy
union all
select * from (select 'other_prefix', regexp_substr(p, '^[A-Za-z ]+'), null, count(*)::text, null, null from a where idtype='other' group by 2 order by 4 desc limit 8)
order by 1, 2, 3
