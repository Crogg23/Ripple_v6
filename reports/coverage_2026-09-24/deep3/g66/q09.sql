-- Google: top 40 US spenders in the 2026 cycle so far (2025-01-01 to 2026-08-02), with ID given to Google,
-- first week ever seen, and spend in the same window of the 2022 cycle (2021-01-01 to 2022-08-02)
with a as (select ADVERTISER_ID id, PUBLIC_IDS_LIST p from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
s as (select id, any_value(nm) nm, min(wk) first_wk, max(wk) last_wk,
        sum(iff(wk between '2025-01-01' and '2026-08-02', usd, 0)) usd26,
        sum(iff(wk between '2021-01-01' and '2022-08-02', usd, 0)) usd22,
        sum(iff(wk between '2023-01-01' and '2024-12-31', usd, 0)) usd24full,
        count_if(wk between '2025-01-01' and '2026-08-02') weeks26,
        max(iff(wk between '2025-01-01' and '2026-08-02', usd, 0)) maxwk26
      from w group by 1)
select s.nm, s.id, left(a.p, 60) public_ids, s.first_wk, s.last_wk, s.usd26, s.weeks26, s.maxwk26, s.usd22, s.usd24full
from s left join a on a.id = s.id
where s.usd26 > 0
order by s.usd26 desc limit 40
