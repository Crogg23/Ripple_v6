-- Google dull-explanation test: is the EIN-only surge just 2025's off-year state races (CA Prop 50, VA, NJ)?
-- Split the cycle window: off-year (Jan 1 - Dec 31) vs election year Jan 1 - Aug 2, 2022 cycle vs 2026 cycle.
-- Then the top EIN-only / blank-ID spenders in Jan 1 - Aug 2 2026, and every advertiser whose name looks like a government body.
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p,
             case when regexp_like(PUBLIC_IDS_LIST, '.*C[0-9]{8}.*') then 'FEC'
                  when PUBLIC_IDS_LIST ilike '%EIN ID%' then 'EIN_only'
                  when PUBLIC_IDS_LIST is null or trim(PUBLIC_IDS_LIST)='' then 'blank' else 'other' end idtype
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
x as (select w.*, coalesce(a.idtype,'no_stats') idtype, a.p,
        case when wk between '2021-01-01' and '2021-12-31' then '2021_offyr'
             when wk between '2022-01-01' and '2022-08-02' then '2022_janaug'
             when wk between '2025-01-01' and '2025-12-31' then '2025_offyr'
             when wk between '2026-01-01' and '2026-08-02' then '2026_janaug' end win
      from w left join a on a.id = w.id)
select 'win_idtype' k, win c1, idtype c2, sum(usd)::text c3, count(distinct id)::text c4, round(100*ratio_to_report(sum(usd)) over (partition by win),1)::text c5, null c6
from x where win is not null group by win, idtype
union all
select * from (select 'top_nonfec_2026', any_value(nm), idtype, sum(usd)::text, count(*)::text, left(any_value(p),45), min(wk)::text
  from x where win='2026_janaug' and idtype in ('EIN_only','blank') group by id, idtype order by sum(usd) desc limit 30)
union all
select * from (select 'govt_named', any_value(nm), idtype, sum(usd)::text, count(*)::text, min(wk)::text, max(wk)::text
  from x where regexp_like(upper(nm), '.*(DEPARTMENT OF|U\\.S\\. |UNITED STATES|AGENCY|ADMINISTRATION|BUREAU|MINISTRY|GOVERNMENT OF|STATE OF |COUNTY OF|CITY OF).*')
  group by id, idtype order by sum(usd) desc limit 15)
