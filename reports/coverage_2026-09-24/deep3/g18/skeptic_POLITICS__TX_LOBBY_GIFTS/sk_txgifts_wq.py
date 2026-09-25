import sys
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
QS = {
'q1_headline_sql': """
with cv as (
  select report_info_ident id, filer_ident, try_to_number(applicable_year) y, try_to_double(total_expend_gift) gift
  from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where try_to_double(total_expend_gift) > 0),
rep as (select *, count(*) over (partition by filer_ident, gift) nrep from cv),
it as (select distinct report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS)
select case when y<=2011 then '2005-11' when y<=2018 then '2012-18' else '2019-26' end era,
  count(*) n, count_if(it.report_id is not null) item, round(100*count_if(it.report_id is not null)/count(*),1) pct,
  round(sum(gift)) usd, count(distinct filer_ident) filers,
  count(distinct iff(it.report_id is not null, filer_ident, null)) item_filers,
  count_if(filer_ident <> '00013737') n_exk, count_if(it.report_id is not null and filer_ident <> '00013737') item_exk
from rep left join it on it.report_id = rep.id
where gift >= 1000 and not (nrep >= 3) and y between 2005 and 2026
group by 1 order by 1""",
'q2_fresh_raw_vs_mart': """
select 'raw_gifts' t, count(*) n, max(RECEIVEDDT)::string mx, count(distinct REPORTINFOIDENT) ids from LIBRARY_RAW.LANDING.TX_LOBBY_GIFTS
union all select 'mart_gifts', count(*), max(receiveddt)::string, count(distinct report_id) from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS
union all select 'raw_cover', count(*), null, null from LIBRARY_RAW.LANDING.TX_LOBBY_COVER
union all select 'mart_cover', count(*), max(received_dt)::string, count(distinct report_info_ident) from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
union all select 'mart_cover_2025plus', count(*), max(received_dt)::string, count_if(try_to_double(total_expend_gift)>0) from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where try_to_number(applicable_year) >= 2025""",
'q3_by_year_gift_and_food_1k': """
with cv as (
  select report_info_ident id, try_to_number(applicable_year) y, try_to_double(total_expend_gift) gift, try_to_double(total_expend_food) food
  from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where try_to_number(applicable_year) between 2005 and 2026
    and (try_to_double(total_expend_gift) >= 1000 or try_to_double(total_expend_food) >= 1000)),
g as (select distinct report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS),
f as (select distinct report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE),
e as (select distinct report_id from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT)
select y,
  count_if(gift>=1000) gift_1k, count_if(gift>=1000 and g.report_id is not null) gift_1k_item,
  count_if(gift>=1000 and (f.report_id is not null or e.report_id is not null)) gift_1k_other_sched,
  count_if(food>=1000) food_1k, count_if(food>=1000 and f.report_id is not null) food_1k_item
from cv left join g on g.report_id=cv.id left join f on f.report_id=cv.id left join e on e.report_id=cv.id
group by 1 order by 1""",
}
def main(keys):
    c = db.connect(); cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    for k in keys:
        sql = QS[k]
        h = sql.lstrip().upper()
        assert (h.startswith('SELECT') or h.startswith('WITH')) and ';' not in sql, k
        print('==', k, flush=True)
        try:
            cur.execute(sql); cols=[d[0] for d in cur.description]
            print(cols)
            for r in cur.fetchall(): print(r)
        except Exception as e:
            print('ERROR', str(e)[:400])
    c.close()
main(sys.argv[1:])
