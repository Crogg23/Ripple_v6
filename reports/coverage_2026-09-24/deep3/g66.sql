-- deep3 / g66: proper look at five glance-only tables, 2026-09-24
-- Tables: EDUCATION__FED_FRB_H15_SELECTED_RATES, EDUCATION__FED_GOOGLE_POLADS_CREATIVE_ID_MAPPING,
--         EDUCATION__FED_CFTC_COT_FUTURES, EDUCATION__FED_ED_NCES_CIP_CODES,
--         EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND
-- Door: Python (connect/db.py) via g66/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g66/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- Column names and types for my 5 tables plus the join partners (Google advertiser stats, FEC committee dim, FEC PAC summary)
select table_schema, table_name, count(*) ncols,
  listagg(column_name || ':' || left(data_type,4), ', ') within group (order by ordinal_position) cols
from LIBRARY_MARTS.information_schema.columns
where table_name in ('EDUCATION__FED_FRB_H15_SELECTED_RATES','EDUCATION__FED_GOOGLE_POLADS_CREATIVE_ID_MAPPING',
 'EDUCATION__FED_ED_NCES_CIP_CODES','EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND','EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS',
 'FINANCE__FED_FEC_COMMITTEES_DIM','POLITICS__FED_FEC_PAC_SUMMARY','EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS')
 or (table_name = 'EDUCATION__FED_CFTC_COT_FUTURES' and (column_name like '\_%' or column_name like 'CONC%' or column_name like 'TRADERS_TOTAL%' or column_name like 'OPEN_INT%' or column_name like 'CFTC%' or column_name like 'AS_OF%' or column_name like 'MARKET%'))
group by 1,2 order by 1,2;

-- [q02] statement 2
-- H15 rates: is it clean? header rows, parse rate, duplicate dates, ND and blank counts, series start dates
with r as (
  select SERIES_DESCRIPTION d_txt, try_to_date(SERIES_DESCRIPTION) d,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS m1,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS m3,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_2_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y2,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_10_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y10,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_20_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y20,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_30_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y30
  from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_FRB_H15_SELECTED_RATES)
select count(*) n, count(d) parsed, count(distinct d) distinct_dates,
  listagg(distinct case when d is null then left(d_txt,40) end, ' || ') unparsed_vals,
  min(d) first_d, max(d) last_d,
  count_if(m3='ND') m3_nd, count_if(m3 is null or trim(m3)='') m3_blank, count_if(try_to_double(m3) is null and m3<>'ND' and trim(m3)<>'') m3_other,
  count_if(y10='ND') y10_nd, count_if(try_to_double(y10) is not null) y10_num,
  min(case when try_to_double(m1) is not null then d end) m1_start,
  min(case when try_to_double(y20) is not null then d end) y20_start,
  count_if(d between '1987-01-01' and '1993-09-30' and try_to_double(y20) is null) y20_gap_rows,
  count_if(d between '2002-03-01' and '2006-01-31' and try_to_double(y30) is null) y30_gap_rows,
  count_if(dayofweekiso(d) in (6,7)) weekend_rows,
  count_if(try_to_double(m3) < 0 or try_to_double(y10) < 0) negative_rows,
  max(try_to_double(y10)) y10_max, min(try_to_double(y10)) y10_min
from r;

-- [q03] statement 3
-- Google creative ID crosswalk: is it 1-to-1, why do IDs repeat 1.8K times, and does it land in CREATIVE_STATS?
with m as (select OLDCREATIVEID o, NEWCREATIVEID nw from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_ID_MAPPING),
oc as (select o, count(*) c, count(distinct nw) dn from m group by 1),
cs as (select distinct AD_ID from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS)
select (select count(*) from m) n, (select count(distinct o) from m) d_old, (select count(distinct nw) from m) d_new,
  (select count(distinct o||'|'||coalesce(nw,'')) from m) d_pairs,
  (select count_if(nw is null or trim(nw)='') from m) new_blank,
  (select count(*) from oc where c>1) old_repeated, (select max(c) from oc) max_rows_one_old, (select max(dn) from oc) max_new_per_old,
  (select count(*) from oc where c between 1700 and 1900) old_ids_near_1800,
  (select count(distinct nw) from m join cs on cs.AD_ID = m.nw) new_in_stats,
  (select count(distinct o) from m join cs on cs.AD_ID = m.o) old_in_stats,
  (select count(*) from cs) stats_ads;

-- [q04] statement 4
-- CIP codes: confirm it is a lookup; why CIP_CODE repeats; ACTION mix
with c as (select * from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_ED_NCES_CIP_CODES),
dup as (select CIP_CODE, count(*) k, count(distinct CIP_TITLE) t, count(distinct _SOURCE_RUN_ID) runs, count(distinct CIP_DEFINITION) defs
        from c group by 1 having count(*)>1)
select 'profile' k, count(*)::text a, count(distinct CIP_CODE)::text b, count(distinct CIP_CODE||'|'||CIP_TITLE)::text c,
  count(distinct _SOURCE_RUN_ID)::text d, count(distinct _SRC_SHA256)::text e,
  (select listagg(ACTION||':'||n, ' | ') from (select ACTION, count(*) n from c group by 1 order by n desc)) f
from c
union all
select 'dup_codes', count(*)::text, sum(k)::text, max(k)::text, max(t)::text, max(runs)::text, max(defs)::text from dup
union all
select * from (select 'dup_sample', CIP_CODE, k::text, t::text, runs::text, defs::text, null from dup order by k desc, CIP_CODE limit 4)
union all
select * from (select 'rows_60.0602', CIP_CODE, left(CIP_TITLE,50), ACTION, left(CIP_DEFINITION,60), _SOURCE_RUN_ID, left(_LOADED_AT::text,19) from c where CIP_CODE='60.0602' limit 6);

-- [q05] statement 5
-- CFTC futures profile: duplicates, keys, dates, impossible percentages (>100), text-number parse rate
with f as (select *, hash(*) h from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES)
select count(*) n, count(distinct h) distinct_rows,
  count(distinct trim(CFTC_CONTRACT_MARKET_CODE)||'|'||AS_OF_DATE_IN_FORM_YYYY_MM_DD) code_date,
  count(distinct trim(CFTC_CONTRACT_MARKET_CODE)) codes, count(distinct MARKET_AND_EXCHANGE_NAMES) names,
  min(AS_OF_DATE_IN_FORM_YYYY_MM_DD) d0, max(AS_OF_DATE_IN_FORM_YYYY_MM_DD) d1,
  count_if(AS_OF_DATE_IN_FORM_YYMMDD <> AS_OF_DATE_IN_FORM_YYYY_MM_DD) date_cols_disagree,
  count_if(trim(CFTC_CONTRACT_MARKET_CODE) <> trim(CFTC_CONTRACT_MARKET_CODE_QUOTES)) code_cols_disagree,
  count_if(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL > 100) g4s_over100, count_if(CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL > 100) g4l_over100,
  count_if(CONCENTRATION_NET_LT_8_TDR_SHORT_ALL > 100) n8s_over100,
  count_if(greatest(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL,CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL,CONCENTRATION_GROSS_LT_8_TDR_SHORT_ALL,CONCENTRATION_GROSS_LT_8_TDR_LONG_ALL) > 100) any_gross_over100,
  count_if(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL is null) g4s_null,
  count_if(try_to_number(trim(OPEN_INTEREST_ALL)) is null) oi_unparsed, count_if(try_to_number(trim(TRADERS_TOTAL_ALL)) is null) traders_unparsed,
  count_if(try_to_number(trim(OPEN_INTEREST_ALL)) = 0) oi_zero,
  count_if(dayofweekiso(AS_OF_DATE_IN_FORM_YYYY_MM_DD) <> 2) not_tuesday,
  count_if(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL < CONCENTRATION_NET_LT_4_TDR_SHORT_ALL) net_gt_gross
from f;

-- [q06] statement 6
-- Google weekly spend profile: duplicates, key, rounding, zeros, week start day, name drift per ID
with w as (select *, hash(*) h from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND),
nm as (select ADVERTISER_ID, count(distinct ADVERTISER_NAME) k from w group by 1)
select count(*) n, count(distinct h) distinct_rows, count(distinct ADVERTISER_ID||'|'||WEEK_START_DATE) id_week,
  count(distinct ADVERTISER_ID) ids, count(distinct ADVERTISER_NAME) names,
  (select count(*) from nm where k>1) ids_multi_name,
  count_if(try_to_number(SPEND_USD) is null) usd_unparsed, count_if(try_to_number(SPEND_USD)=0) usd_zero,
  count_if(mod(try_to_number(SPEND_USD),100)<>0) usd_not_100_step,
  sum(try_to_number(SPEND_USD)) usd_total, max(try_to_number(SPEND_USD)) usd_max_week,
  count_if(try_to_number(SPEND_USD)=0 and (try_to_number(SPEND_EUR)>0 or try_to_number(SPEND_INR)>0 or try_to_number(SPEND_GBP)>0 or try_to_number(SPEND_BRL)>0 or try_to_number(SPEND_AUD)>0 or try_to_number(SPEND_MXN)>0)) usd0_other_ccy_pos,
  count_if(try_to_number(SPEND_USD)>0 and try_to_number(SPEND_EUR)=0 and try_to_number(SPEND_INR)=0 and try_to_number(SPEND_GBP)=0) usd_only_pos,
  listagg(distinct dayname(WEEK_START_DATE), ',') week_start_days,
  min(WEEK_START_DATE) w0, max(WEEK_START_DATE) w1, count(distinct WEEK_START_DATE) weeks
from w;

-- [q07] statement 7
-- Google advertiser stats: what PUBLIC_IDS_LIST holds (FEC ID, EIN, other), by region, with USD spend
with a as (select ADVERTISER_ID, ADVERTISER_NAME, REGIONS, PUBLIC_IDS_LIST p, try_to_number(SPEND_USD) usd
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS)
select 'summary' k, count(*)::text n, count(distinct ADVERTISER_ID)::text ids,
  count_if(REGIONS like '%US%')::text us_rows,
  count_if(REGIONS like '%US%' and regexp_like(p, '.*C[0-9]{8}.*'))::text us_fec,
  count_if(REGIONS like '%US%' and not regexp_like(coalesce(p,''), '.*C[0-9]{8}.*') and regexp_like(p, '.*[0-9]{2}-?[0-9]{7}.*'))::text us_ein_only,
  count_if(REGIONS like '%US%' and (p is null or trim(p)=''))::text us_blank,
  sum(case when REGIONS like '%US%' then usd end)::text us_usd
from a
union all
select * from (select 'sample', ADVERTISER_NAME, REGIONS, left(p,120), usd::text, ADVERTISER_ID, null, null from a where REGIONS like '%US%' order by usd desc nulls last limit 25);

-- [q08] statement 8
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
order by 1, 2, 3;

-- [q09] statement 9
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
order by s.usd26 desc limit 40;

-- [q10] statement 10
-- JOIN: Google advertisers that gave an FEC committee ID -> FEC PAC/party summary, 2024 cycle.
-- Test: Google US spend from 2023-01-01 through the FEC coverage end date vs everything the committee reported
-- paying out (TOTAL_DISBURSEMENTS) plus unpaid bills (DEBTS_OWED_BY) through that same date.
with a as (select ADVERTISER_ID id, regexp_substr(PUBLIC_IDS_LIST, 'C[0-9]{8}') fec
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS where regexp_like(PUBLIC_IDS_LIST, '.*C[0-9]{8}.*')),
w as (select ADVERTISER_ID id, ADVERTISER_NAME nm, WEEK_START_DATE wk, try_to_number(SPEND_USD) usd
      from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND where try_to_number(SPEND_USD) > 0),
p as (select CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COMMITTEE_DESIGNATION, TOTAL_DISBURSEMENTS disb, coalesce(DEBTS_OWED_BY,0) debt, COVERAGE_END_DATE ced
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
      where COVERAGE_END_DATE between '2023-01-01' and '2024-12-31'
      qualify row_number() over (partition by CMTE_ID order by COVERAGE_END_DATE desc, TOTAL_DISBURSEMENTS desc) = 1),
gf as (select a.fec, count(distinct a.id) n_adv, listagg(distinct w.nm, ' / ') names, sum(w.usd) g24
       from w join a on a.id = w.id where w.wk between '2023-01-01' and '2024-12-31' group by 1),
gc as (select a.fec, sum(w.usd) g_to_ced from w join a on a.id = w.id join p on p.CMTE_ID = a.fec
       where w.wk >= '2023-01-01' and dateadd(day,6,w.wk) <= p.ced group by 1),
j as (select gf.*, p.COMMITTEE_NAME, p.COMMITTEE_TYPE, p.COMMITTEE_DESIGNATION, p.disb, p.debt, p.ced, coalesce(gc.g_to_ced,0) g_to_ced
      from gf left join p on p.CMTE_ID = gf.fec left join gc on gc.fec = gf.fec),
dim as (select distinct CMTE_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM)
select 'land' k, count(*)::text fec_ids, count(ced)::text in_pac_summary, (select count(*) from gf join dim on dim.CMTE_ID = gf.fec)::text in_dim,
  sum(g24)::text google24, sum(iff(ced is not null, g24, 0))::text google24_landed,
  count_if(g_to_ced > disb + debt)::text over_disb, null, null, null, null
from j
union all
select * from (select 'over', fec, left(names,70), COMMITTEE_NAME, COMMITTEE_TYPE||'/'||COMMITTEE_DESIGNATION, g24::text, g_to_ced::text, disb::text, debt::text, ced::text, n_adv::text
  from j where g_to_ced > disb + debt order by g_to_ced - (disb+debt) desc limit 25);

-- [q11] statement 11
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
  group by id, idtype order by sum(usd) desc limit 15);

-- [q12] statement 12
-- CFTC: the impossible rows. Top-4/top-8 trader share of open interest over 100 percent, and net above gross.
select MARKET_AND_EXCHANGE_NAMES, AS_OF_DATE_IN_FORM_YYYY_MM_DD d, OPEN_INTEREST_ALL oi, TRADERS_TOTAL_ALL traders,
  CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL g4l, CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL g4s,
  CONCENTRATION_GROSS_LT_8_TDR_LONG_ALL g8l, CONCENTRATION_GROSS_LT_8_TDR_SHORT_ALL g8s,
  CONCENTRATION_NET_LT_4_TDR_LONG_ALL n4l, CONCENTRATION_NET_LT_4_TDR_SHORT_ALL n4s,
  OF_OI_TOTAL_REPORTABLE_LONG_ALL pct_rept_long, OF_OI_TOTAL_REPORTABLE_SHORT_ALL pct_rept_short
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where greatest(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL, CONCENTRATION_GROSS_LT_8_TDR_SHORT_ALL, CONCENTRATION_GROSS_LT_8_TDR_LONG_ALL,
               CONCENTRATION_NET_LT_8_TDR_SHORT_ALL, CONCENTRATION_NET_LT_8_TDR_LONG_ALL) > 100
   or CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL < CONCENTRATION_NET_LT_4_TDR_SHORT_ALL
order by d;

-- [q13] statement 13
-- CFTC time check: rows, report dates and markets per year. Looks for gaps, the separately loaded 2024, and where 2026 stops.
select year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) yr, count(*) n, count(distinct AS_OF_DATE_IN_FORM_YYYY_MM_DD) dates,
  count(distinct trim(CFTC_CONTRACT_MARKET_CODE)) markets, round(count(*)/count(distinct AS_OF_DATE_IN_FORM_YYYY_MM_DD),0) mkts_per_date,
  min(AS_OF_DATE_IN_FORM_YYYY_MM_DD) first_d, max(AS_OF_DATE_IN_FORM_YYYY_MM_DD) last_d,
  count(distinct CFTC_MARKET_CODE_IN_INITIALS) exchanges,
  median(try_to_number(trim(TRADERS_TOTAL_ALL))) med_traders
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
group by 1 order by 1;

-- [q14] statement 14
-- CFTC lead hunt: which markets have their 4 biggest traders holding more of one side now than ever?
-- Now = the 13 report dates 2026-05-05 .. 2026-08-04. History = 2016-2025 same market (trimmed code).
-- Only markets with 300+ history weeks and 50+ traders now (thin markets are concentrated by arithmetic).
with f as (select trim(CFTC_CONTRACT_MARKET_CODE) code, MARKET_AND_EXCHANGE_NAMES nm, AS_OF_DATE_IN_FORM_YYYY_MM_DD d,
             try_to_number(trim(OPEN_INTEREST_ALL)) oi, try_to_number(trim(TRADERS_TOTAL_ALL)) tr,
             CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL g4s, CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL g4l
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
           where AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2016-01-01' and greatest(g4s, g4l) <= 100),
h as (select code, count(*) wks, median(g4s) med_s, max(g4s) max_s, median(g4l) med_l, max(g4l) max_l, median(oi) med_oi, median(tr) med_tr
      from f where d < '2026-01-01' group by 1),
n as (select code, max_by(nm, d) nm, count(*) wks_now, avg(g4s) now_s, max(g4s) now_max_s, avg(g4l) now_l, max(g4l) now_max_l, avg(oi) now_oi, avg(tr) now_tr
      from f where d between '2026-05-05' and '2026-08-04' group by 1),
j as (select n.*, h.wks, h.med_s, h.max_s, h.med_l, h.max_l, h.med_oi, h.med_tr,
        n.now_s - h.med_s d_s, n.now_l - h.med_l d_l
      from n join h on h.code = n.code where h.wks >= 300 and n.now_tr >= 50 and n.wks_now >= 10)
select code, left(nm,55) nm, round(now_s,1) now_s, round(med_s,1) med_s, round(max_s,1) hist_max_s, round(now_max_s,1) now_max_s,
  round(now_l,1) now_l, round(med_l,1) med_l, round(max_l,1) hist_max_l, round(now_max_l,1) now_max_l,
  round(now_oi,0) now_oi, med_oi, round(now_tr,0) now_tr, med_tr, wks,
  round(median(d_s) over (),1) peer_med_d_s, round(median(d_l) over (),1) peer_med_d_l, count(*) over () n_mkts,
  count_if(now_max_s > max_s) over () n_record_s, count_if(now_max_l > max_l) over () n_record_l
from j
qualify row_number() over (order by greatest(d_s, d_l) desc) <= 30
order by greatest(d_s, d_l) desc;

-- [q15] statement 15
-- H15 time check: longest runs of trading days with the 10-year yield below the 3-month yield (inverted curve)
with r as (select try_to_date(SERIES_DESCRIPTION) d,
             try_to_double(MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS) m3,
             try_to_double(MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_10_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS) y10
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_FRB_H15_SELECTED_RATES),
s as (select d, m3, y10, iff(y10 < m3, 1, 0) inv from r where d is not null and m3 is not null and y10 is not null),
g as (select *, row_number() over (order by d) - row_number() over (partition by inv order by d) grp from s)
select min(d) start_d, max(d) end_d, count(*) trading_days, round(min(y10 - m3),2) deepest_pts,
  (select min(d) from s) series_start, (select count(*) from s) days_both
from g where inv = 1 group by grp
qualify row_number() over (order by count(*) desc) <= 6
order by trading_days desc;

-- [q16] statement 16
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
  from per join tot on tot.id = per.id left join a on a.id = per.id order by per.blackout_usd desc, tot.total_usd desc limit 40);

-- [q17] statement 17
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
order by 1, 2, 4;

-- [q18] statement 18
-- CFTC peer + time: electricity futures (commodity code 064) by hub family and year, 2016 - Aug 2026.
-- Open-interest-weighted share of the short side and the long side held by the 4 biggest traders.
-- Question: is PJM's rise in top-4 short concentration PJM-only, or every power hub?
with f as (select upper(MARKET_AND_EXCHANGE_NAMES) nm, year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) yr, AS_OF_DATE_IN_FORM_YYYY_MM_DD d,
             try_to_number(trim(OPEN_INTEREST_ALL)) oi, try_to_number(trim(TRADERS_TOTAL_ALL)) tr,
             CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL g4s, CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL g4l, trim(CFTC_CONTRACT_MARKET_CODE) code
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
           where CFTC_COMMODITY_CODE = '064' and AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2016-01-01' and greatest(g4s, g4l) <= 100),
h as (select *, case when nm like '%PJM%' then 'PJM' when nm like '%ISO NE%' or nm like '%MASS HUB%' then 'ISO-NE'
                     when nm like '%ERCOT%' then 'ERCOT' when nm like '%MISO%' or nm like '%INDIANA%' then 'MISO'
                     when nm like '%NYISO%' or nm like '%NY ZONE%' or nm like '%ZONE G%' or nm like '%ZONE J%' or nm like '%ZONE A%' then 'NYISO'
                     when nm like '%SP15%' or nm like '%NP15%' or nm like '%CAISO%' or nm like '%PALO VERDE%' or nm like '%MID-C%' or nm like '%MID C%' or nm like '%MIDC%' then 'WEST'
                     else 'OTHER' end hub
      from f)
select hub, yr, count(distinct code) contracts, count(*) contract_weeks,
  round(sum(g4s*oi)/nullif(sum(oi),0),1) w_g4s, round(sum(g4l*oi)/nullif(sum(oi),0),1) w_g4l,
  round(median(g4s),1) med_g4s, round(avg(oi)*count(distinct code)/1000,0) approx_oi_k, round(median(tr),0) med_traders
from h group by 1,2 order by 1,2;

-- [q18b] statement 19
-- (rerun: the first try filtered CFTC_COMMODITY_CODE = '064' and matched 0 rows)
-- CFTC peer + time: electricity futures (commodity code 64, contract codes starting 064) by hub family and year, 2016 - Aug 2026.
-- Open-interest-weighted share of the short side and the long side held by the 4 biggest traders.
-- Question: is PJM's rise in top-4 short concentration PJM-only, or every power hub?
with f as (select upper(MARKET_AND_EXCHANGE_NAMES) nm, year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) yr, AS_OF_DATE_IN_FORM_YYYY_MM_DD d,
             try_to_number(trim(OPEN_INTEREST_ALL)) oi, try_to_number(trim(TRADERS_TOTAL_ALL)) tr,
             CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL g4s, CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL g4l, trim(CFTC_CONTRACT_MARKET_CODE) code
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
           where (try_to_number(trim(CFTC_COMMODITY_CODE)) = 64 or left(trim(CFTC_CONTRACT_MARKET_CODE),3) = '064') and AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2016-01-01' and greatest(g4s, g4l) <= 100),
h as (select *, case when nm like '%PJM%' then 'PJM' when nm like '%ISO NE%' or nm like '%MASS HUB%' then 'ISO-NE'
                     when nm like '%ERCOT%' then 'ERCOT' when nm like '%MISO%' or nm like '%INDIANA%' then 'MISO'
                     when nm like '%NYISO%' or nm like '%NY ZONE%' or nm like '%ZONE G%' or nm like '%ZONE J%' or nm like '%ZONE A%' then 'NYISO'
                     when nm like '%SP15%' or nm like '%NP15%' or nm like '%CAISO%' or nm like '%PALO VERDE%' or nm like '%MID-C%' or nm like '%MID C%' or nm like '%MIDC%' then 'WEST'
                     else 'OTHER' end hub
      from f)
select hub, yr, count(distinct code) contracts, count(*) contract_weeks,
  round(sum(g4s*oi)/nullif(sum(oi),0),1) w_g4s, round(sum(g4l*oi)/nullif(sum(oi),0),1) w_g4l,
  round(median(g4s),1) med_g4s, round(avg(oi)*count(distinct code)/1000,0) approx_oi_k, round(median(tr),0) med_traders
from h group by 1,2 order by 1,2;

-- [q19] statement 20
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
order by t.blackout_usd desc;

-- [q20] statement 21
-- CFTC time detail: PJM Western Hub day-ahead peak and off-peak futures (ICE), by quarter 2023 - 2026.
-- Top-4 share of the short side, open interest, number of traders, number of big commercial shorts.
select trim(CFTC_CONTRACT_MARKET_CODE) code, left(any_value(MARKET_AND_EXCHANGE_NAMES),45) nm,
  year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) || 'Q' || quarter(AS_OF_DATE_IN_FORM_YYYY_MM_DD) q, count(*) wks,
  round(avg(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL),1) g4s, round(avg(CONCENTRATION_GROSS_LT_8_TDR_SHORT_ALL),1) g8s,
  round(avg(CONCENTRATION_NET_LT_4_TDR_SHORT_ALL),1) n4s, round(avg(CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL),1) g4l,
  round(avg(try_to_number(trim(OPEN_INTEREST_ALL))),0) oi, round(avg(try_to_number(trim(TRADERS_TOTAL_ALL))),0) traders,
  round(avg(try_to_number(trim(TRADERS_COMMERCIAL_SHORT_ALL))),1) comm_short_traders,
  round(avg(try_to_double(trim(OF_OI_COMMERCIAL_SHORT_ALL))),1) pct_comm_short
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where trim(CFTC_CONTRACT_MARKET_CODE) in ('0643DB','0643DC') and AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2023-01-01'
group by 1, 3 order by 1, 3;

-- [q21] statement 22
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
order by w.nm, w.wk;

-- [q22] statement 23
-- CFTC verification: (1) full-history record check for the two PJM Western Hub day-ahead contracts, back to their first report;
-- (2) why CFTC_COMMODITY_CODE = '064' matched nothing: the raw stored values for power rows.
select 'pjm' k, trim(CFTC_CONTRACT_MARKET_CODE) code, min(AS_OF_DATE_IN_FORM_YYYY_MM_DD)::text first_d, max(AS_OF_DATE_IN_FORM_YYYY_MM_DD)::text last_d,
  count(*)::text wks,
  max(iff(AS_OF_DATE_IN_FORM_YYYY_MM_DD < '2016-01-01', CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, null))::text max_pre2016,
  max(iff(AS_OF_DATE_IN_FORM_YYYY_MM_DD between '2016-01-01' and '2025-12-31', CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, null))::text max_2016_2025,
  max(iff(AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2026-01-01', CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, null))::text max_2026,
  max_by(AS_OF_DATE_IN_FORM_YYYY_MM_DD, CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL)::text date_of_max,
  count_if(AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2026-01-01' and CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL > 65)::text wks_2026_over65,
  count_if(AS_OF_DATE_IN_FORM_YYYY_MM_DD < '2025-01-01' and CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL > 65)::text wks_pre2025_over65
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where trim(CFTC_CONTRACT_MARKET_CODE) in ('0643DB','0643DC')
group by 2
union all
select 'code_raw', '[' || CFTC_COMMODITY_CODE || ']', length(CFTC_COMMODITY_CODE)::text, count(*)::text, min(left(trim(CFTC_CONTRACT_MARKET_CODE),3)), null, null, null, null, null, null
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where left(trim(CFTC_CONTRACT_MARKET_CODE),3) = '064' or try_to_number(trim(CFTC_COMMODITY_CODE)) = 64
group by 2, 3;

-- [q23] statement 24
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
order by 1, 2, 4;

-- [q24] statement 25
-- H15 check: the Treasury sold no 30-year bonds from Feb 2002 to Feb 2006, yet q02 found only 43 empty 30-year rows in that window.
-- Is the 30-year column really the 30-year? Per year 2000-2007: numeric count, ND count, blank count, average 20y and 30y.
with r as (select try_to_date(SERIES_DESCRIPTION) d,
             MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_20_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y20,
             MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_30_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y30
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_FRB_H15_SELECTED_RATES)
select year(d) yr, count(*) n, count_if(try_to_double(y30) is not null) y30_num, count_if(y30 = 'ND') y30_nd,
  count_if(y30 is null or trim(y30) = '') y30_blank, round(avg(try_to_double(y20)),2) avg_y20, round(avg(try_to_double(y30)),2) avg_y30,
  min(iff(try_to_double(y30) is null and (y30 is null or trim(y30)=''), d, null)) first_blank_30, max(iff(try_to_double(y30) is null and (y30 is null or trim(y30)=''), d, null)) last_blank_30
from r where d between '2000-01-01' and '2007-12-31' group by 1 order by 1;
