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
  from j where g_to_ced > disb + debt order by g_to_ced - (disb+debt) desc limit 25)
