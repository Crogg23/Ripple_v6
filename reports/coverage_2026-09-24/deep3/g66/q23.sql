-- Google: federal executive agencies in the political-ad data. Any agency-like name or DHS component, spend by year,
-- plus the DHS account's month-by-month spend (the agency's ads started 2025-03).
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
g as (select * from w where regexp_like(upper(nm), '.*(HOMELAND|BORDER PROTECTION|IMMIGRATION AND CUSTOMS|WHITE HOUSE|DEPARTMENT OF|DEPT OF|U\\.S\\. DEPARTMENT|FEDERAL EMERGENCY|SECRETARY OF|CENTERS FOR MEDICARE|SOCIAL SECURITY ADMIN|CENSUS BUREAU|U\\.S\\. ARMY|U\\.S\\. NAVY|AIR FORCE).*'))
select 'agency_year' k, g.nm c1, left(a.p,25) c2, year(g.wk)::text c3, sum(g.usd)::text c4, count(*)::text c5
from g left join a on a.id = g.id group by g.nm, a.p, year(g.wk)
union all
select 'dhs_month', nm, null, to_char(date_trunc('month', wk), 'YYYY-MM'), sum(usd)::text, count(*)::text
from w where upper(nm) = 'DEPARTMENT OF HOMELAND SECURITY' group by nm, date_trunc('month', wk)
order by 1, 2, 4
