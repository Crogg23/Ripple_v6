-- @senate_trade_tables_paper_check
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
order by 1, 3 desc
-- @senate_trade_tables_totals
select 'FINANCE__SENATE_TRADES' src, year(coalesce(transaction_date, filed_date)) y, count(*) n, count(distinct ptr_link) links,
  count(distinct coalesce(senator_name, senator_raw)) senators
from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES group by 1,2
union all
select 'FINANCE__FED_SENATE_STOCK_WATCHER', year(transaction_date), count(*), count(distinct ptr_link), count(distinct senator)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER group by 1,2
order by 1,2
-- @tx_cover_for_itemized
select report_info_ident, filer_ident, filer_name, form_type_cd, report_type_cd, applicable_year,
  period_start_dt, period_end_dt, received_dt, total_expend_gift, total_expend_award, total_expend_event
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
where try_to_double(total_expend_gift) > 0 or try_to_double(total_expend_award) > 0 or try_to_double(total_expend_event) > 0
   or report_info_ident in (select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS
                            union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_EVENTS
                            union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_AWARDS
                            union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS)
-- @tx_clients_for_itemized
select report_id, filer_id, filername, applicableyear, onbehalfname, onbehalfmailingcity
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING
where report_id in (select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS
                    union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_EVENTS
                    union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_AWARDS
                    union select report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS)
-- @tx_court_cases_in_courtlistener
select court_id, docket_number, case_name, date_filed, date_terminated
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where court_id in ('tex', 'texapp', 'texcrimapp')
  and docket_number in ('02-15-00342-CV','03-13-00084-CV','03-14-00375-CV','04-15-00610-CV','05-16-00573-CV','05-19-01248-CV','06-1502','07-0614','07-0615','07-0616','07-10-00108-CV','07-2673','07-2674','08-23-00345-CV','09-21-00111-CV','10-17-00202-CV','12-0150','13-06-00614-CR','14-0572','14-0645','15-0029','15-0073','15-0238','15-0666','15-0688','16-0082','16-0748','16-0880','16-1861','17-0105','17-0198','17-0329','17-0370','17-0405','17-0423','17-0588','17-0724','17-0732','17-0850','18-0413','18-0458','18-1231','18-3319','19-0686','19-0733','20-0606','21-0307','21-1094','22-0044','22-0493','22-0759','23-0629','23-0767','24-0102','24-0250','PD-0236-07','PD-0254-18','PD-0265-07')
