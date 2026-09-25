-- JOIN (dull-explanation test): were the House offices with pre-election ad spend actually on that November ballot?
-- Official accounts with spend in weeks starting inside the 90 days before a general election, per election year,
-- matched to the FEC candidate file: House race, same election year, incumbent (I), name holds the member's first and last word.
with w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND
           where try_to_number(SPEND_USD) > 0
             and (upper(ADVERTISER_NAME) like '%U.S. HOUSE OF REPRESENTATIVES%' or upper(ADVERTISER_NAME) like '%US HOUSE OF REPRESENTATIVES%'
                  or upper(ADVERTISER_NAME) like 'OFFICE OF REP%')
             and upper(ADVERTISER_NAME) not like '% FOR %'),
e as (select column1::date ed from values ('2018-11-06'),('2020-11-03'),('2022-11-08'),('2024-11-05')),
b as (select w.id, any_value(w.nm) nm, year(e.ed) yr, any_value(e.ed) ed, sum(w.usd) blackout_usd, count(*) wks, min(w.wk) first_wk, max(w.wk) last_wk
      from w join e on w.wk >= dateadd(day,-90,e.ed) and w.wk < e.ed group by w.id, year(e.ed)),
n as (select b.*, trim(regexp_replace(regexp_replace(upper(nm), '\\s*-\\s*U\\.?S\\.? HOUSE OF REPRESENTATIVES.*$', ''), '^(OFFICE OF )?REP\\.?\\s+', '')) member
      from b),
t as (select n.*, split_part(member, ' ', 1) w1, regexp_substr(member, '[A-Z\\-]+$') wlast from n),
c as (select CAND_ID, CAND_NAME, CAND_ELECTION_YR, CAND_ICI, CAND_STATUS, CAND_OFFICE_ST, CAND_OFFICE_DISTRICT
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES where CAND_OFFICE = 'H' and CAND_ELECTION_YR in (2018, 2020, 2022, 2024))
select t.member, t.yr, t.blackout_usd, t.wks, t.first_wk, t.last_wk,
  count(c.CAND_ID) n_match, listagg(distinct c.CAND_ID || ' ' || c.CAND_NAME || ' ' || c.CAND_OFFICE_ST || '-' || c.CAND_OFFICE_DISTRICT || ' ICI=' || coalesce(c.CAND_ICI,'?') || ' st=' || coalesce(c.CAND_STATUS,'?'), ' ; ') matches
from t left join c on c.CAND_ELECTION_YR = t.yr and contains(upper(c.CAND_NAME), t.wlast) and contains(upper(c.CAND_NAME), t.w1)
group by 1,2,3,4,5,6
order by t.blackout_usd desc
