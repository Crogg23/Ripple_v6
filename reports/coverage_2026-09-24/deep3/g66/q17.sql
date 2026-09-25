-- JOIN: Google advertisers that gave only an EIN -> IRS exempt-org master file (subsection: 501c3 charity, c4 social welfare,
-- c5 labor, c6 trade group) and the IRS 527 political-org registry (Form 8871). Same cycle-to-date windows, 2022 vs 2026.
-- The BMF org name comes back beside the Google name so a name check can back the EIN match.
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p,
             try_to_number(replace(regexp_substr(PUBLIC_IDS_LIST, '[0-9]{2}-?[0-9]{7}'), '-', '')) ein
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS
           where PUBLIC_IDS_LIST ilike '%EIN ID%' and not regexp_like(PUBLIC_IDS_LIST, '.*C[0-9]{8}.*')),
b as (select try_to_number(EIN) ein, max(try_to_number(SUBSECTION_CODE)) sub, max(ORGANIZATION_NAME) bmf_nm, max(STATE) bmf_st
      from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF where try_to_number(EIN) in (select ein from a) group by 1),
k as (select distinct try_to_number(replace(EIN,'-','')) ein from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS),
cls as (select a.id, a.ein, b.bmf_nm, b.bmf_st,
          case when b.sub = 3 then 'c3_charity' when b.sub = 4 then 'c4_social_welfare' when b.sub = 5 then 'c5_labor'
               when b.sub = 6 then 'c6_trade' when b.sub is not null then 'c_other_' || b.sub
               when k.ein is not null then '527_registered' else 'no_irs_match' end cl
        from a left join b on b.ein = a.ein left join k on k.ein = a.ein),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd,
        case when WEEK_START_DATE between '2021-01-01' and '2022-08-02' then '2022_ctd'
             when WEEK_START_DATE between '2025-01-01' and '2026-08-02' then '2026_ctd' end win
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
x as (select w.*, cls.cl, cls.bmf_nm, cls.bmf_st, cls.ein from w join cls on cls.id = w.id where win is not null)
select 'by_class' k, win c1, cl c2, sum(usd)::text c3, count(distinct id)::text c4, round(100*ratio_to_report(sum(usd)) over (partition by win),1)::text c5, null c6
from x group by win, cl
union all
select * from (select 'top_c3_2026', any_value(nm), any_value(bmf_nm) || ' (' || any_value(bmf_st) || ')', sum(usd)::text, count(*)::text, min(wk)::text, max(wk)::text
  from x where win='2026_ctd' and cl='c3_charity' group by id order by sum(usd) desc limit 15)
union all
select * from (select 'top_c4_2026', any_value(nm), any_value(bmf_nm) || ' (' || any_value(bmf_st) || ')', sum(usd)::text, count(*)::text, min(wk)::text, max(wk)::text
  from x where win='2026_ctd' and cl='c4_social_welfare' group by id order by sum(usd) desc limit 12)
union all
select * from (select 'top_nomatch_2026', any_value(nm), any_value(ein)::text, sum(usd)::text, count(*)::text, min(wk)::text, max(wk)::text
  from x where win='2026_ctd' and cl='no_irs_match' group by id order by sum(usd) desc limit 12)
order by 1, 2, 4
