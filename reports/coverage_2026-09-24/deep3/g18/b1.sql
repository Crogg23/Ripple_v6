-- @gifts_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS
-- @events_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_EVENTS
-- @awards_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_AWARDS
-- @dockets_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS
-- @efd_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_EFD_FILINGS
-- @ptr_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR
-- @cover_by_year
select applicable_year, form_type_cd, count(*) n_reports, count(distinct report_info_ident) n_ids,
  count_if(try_to_double(total_expend_gift) > 0) rep_gift, sum(try_to_double(total_expend_gift)) sum_gift,
  count_if(try_to_double(total_expend_award) > 0) rep_award, sum(try_to_double(total_expend_award)) sum_award,
  count_if(try_to_double(total_expend_event) > 0) rep_event, sum(try_to_double(total_expend_event)) sum_event,
  count_if(total_expend_gift is not null and total_expend_gift <> '' and try_to_double(total_expend_gift) is null) gift_unparsed
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
group by 1,2 order by 1,2
