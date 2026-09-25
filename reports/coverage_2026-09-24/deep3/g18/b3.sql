-- @tx_itemization_all_categories_by_year
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
where cv.y >= '2004' order by cv.y
-- @tx_clients_top_gift_filers
select filer_id, filername, upper(trim(onbehalfname)) client, min(applicableyear) y0, max(applicableyear) y1, count(*) n
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING
where filer_id in ('00081042','00081168','00013737','00068112','00068309','00020172','00056279','00038905','00067126','00070108','00068588','00020220')
group by 1,2,3 order by 1, n desc
