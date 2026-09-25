-- g18 deep pass 3, 2026-09-24. Every statement run, in order, numbered.
-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- [1] gifts_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS;

-- [2] events_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_EVENTS;

-- [3] awards_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_AWARDS;

-- [4] dockets_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS;

-- [5] efd_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_EFD_FILINGS;

-- [6] ptr_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR;

-- [7] cover_by_year
select applicable_year, form_type_cd, count(*) n_reports, count(distinct report_info_ident) n_ids,
  count_if(try_to_double(total_expend_gift) > 0) rep_gift, sum(try_to_double(total_expend_gift)) sum_gift,
  count_if(try_to_double(total_expend_award) > 0) rep_award, sum(try_to_double(total_expend_award)) sum_award,
  count_if(try_to_double(total_expend_event) > 0) rep_event, sum(try_to_double(total_expend_event)) sum_event,
  count_if(total_expend_gift is not null and total_expend_gift <> '' and try_to_double(total_expend_gift) is null) gift_unparsed
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
group by 1,2 order by 1,2;

-- [8] senate_trade_tables_paper_check
select 'FINANCE__SENATE_TRADES' src, coalesce(senator_name, senator_raw) senator, count(*) n_lines,
  count_if(asset_type ilike 'PDF%') pdf_lines, count_if(filing_kind = 'paper') paper_lines,
  count(distinct ptr_link) n_links, min(transaction_date) t0, max(transaction_date) t1, min(filed_date) f0, max(filed_date) f1
from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES
where asset_type ilike 'PDF%' or filing_kind = 'paper' or senator_name ilike '%blumenthal%' or senator_raw ilike '%blumenthal%'
group by 1,2
union all
select 'FINANCE__FED_SENATE_STOCK_WATCHER', senator, count(*), count_if(asset_type ilike 'PDF%'), null,
  count(distinct ptr_link), min(transaction_date), max(transaction_date), null, null
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER
where asset_type ilike 'PDF%' or senator ilike '%blumenthal%'
group by 1,2
union all
select 'POLITICS__SENATE_TRADES', senator, count(*), count_if(asset_type ilike 'PDF%'), null,
  count(distinct ptr_link), min(transaction_date), max(transaction_date), null, null
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
where asset_type ilike 'PDF%' or senator ilike '%blumenthal%'
group by 1,2
order by 1, 3 desc;

-- [9] senate_trade_tables_totals
select 'FINANCE__SENATE_TRADES' src, year(coalesce(transaction_date, filed_date)) y, count(*) n, count(distinct ptr_link) links,
  count(distinct coalesce(senator_name, senator_raw)) senators
from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES group by 1,2
union all
select 'FINANCE__FED_SENATE_STOCK_WATCHER', year(transaction_date), count(*), count(distinct ptr_link), count(distinct senator)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER group by 1,2
order by 1,2;

-- [10] tx_cover_for_itemized
select report_info_ident, filer_ident, filer_name, form_type_cd, report_type_cd, applicable_year,
  period_start_dt, period_end_dt, received_dt, total_expend_gift, total_expend_award, total_expend_event
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
where try_to_double(total_expend_gift) > 0 or try_to_double(total_expend_award) > 0 or try_to_double(total_expend_event) > 0
   or report_info_ident in (select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS
                            union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_EVENTS
                            union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_AWARDS
                            union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS);

-- [11] tx_clients_for_itemized
select report_id, filer_id, filername, applicableyear, onbehalfname, onbehalfmailingcity
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING
where report_id in (select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS
                    union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_EVENTS
                    union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_AWARDS
                    union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS);

-- [12] tx_court_cases_in_courtlistener
select court_id, docket_number, case_name, date_filed, date_terminated
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where court_id in ('tex', 'texapp', 'texcrimapp')
  and docket_number in ('02-15-00342-CV','03-13-00084-CV','03-14-00375-CV','04-15-00610-CV','05-16-00573-CV','05-19-01248-CV','06-1502','07-0614','07-0615','07-0616','07-10-00108-CV','07-2673','07-2674','08-23-00345-CV','09-21-00111-CV','10-17-00202-CV','12-0150','13-06-00614-CR','14-0572','14-0645','15-0029','15-0073','15-0238','15-0666','15-0688','16-0082','16-0748','16-0880','16-1861','17-0105','17-0198','17-0329','17-0370','17-0405','17-0423','17-0588','17-0724','17-0732','17-0850','18-0413','18-0458','18-1231','18-3319','19-0686','19-0733','20-0606','21-0307','21-1094','22-0044','22-0493','22-0759','23-0629','23-0767','24-0102','24-0250','PD-0236-07','PD-0254-18','PD-0265-07');

-- [13] tx_itemization_all_categories_by_year
with f as (select applicableyear y, count(*) food_rows, count(distinct report_id) food_reps from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE group by 1),
     e as (select applicableyear y, count(*) ent_rows, count(distinct report_id) ent_reps from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT group by 1),
     t as (select applicableyear y, count(*) tran_rows, count(distinct report_id) tran_reps from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION group by 1),
     cv as (select applicable_year y,
              count_if(try_to_double(total_expend_food) > 0) cov_food_reps, sum(try_to_double(total_expend_food)) cov_food_usd,
              count_if(try_to_double(total_expend_entertainment) > 0) cov_ent_reps, sum(try_to_double(total_expend_entertainment)) cov_ent_usd,
              count_if(try_to_double(total_expend_transportation) > 0) cov_tran_reps, sum(try_to_double(total_expend_transportation)) cov_tran_usd
            from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER group by 1)
select cv.*, f.food_rows, f.food_reps, e.ent_rows, e.ent_reps, t.tran_rows, t.tran_reps
from cv left join f on f.y = cv.y left join e on e.y = cv.y left join t on t.y = cv.y
where cv.y >= '2004' order by cv.y;

-- [14] tx_clients_top_gift_filers
select filer_id, filername, upper(trim(onbehalfname)) client, min(applicableyear) y0, max(applicableyear) y1, count(*) n
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING
where filer_id in ('00081042','00081168','00013737','00068112','00068309','00020172','00056279','00038905','00067126','00070108','00068588','00020220')
group by 1,2,3 order by 1, n desc;
