-- MSHA join: accidents and citations dated 30+ days AFTER a mine's current idle/abandoned status took effect
with m as (select MINE_ID, CURRENT_MINE_STATUS st, CURRENT_STATUS_DT sdt, CURRENT_MINE_NAME nm, CURRENT_CONTROLLER_NAME ctrl, STATE, COAL_METAL_IND cm
           from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES
           where CURRENT_MINE_STATUS in ('Abandoned','Abandoned and Sealed','Temporarily Idled','NonProducing') and CURRENT_STATUS_DT >= '2000-01-01'),
a as (select a.MINE_ID, count(*) n, count_if(a.IS_FATALITY) fat, sum(a.DAYS_LOST) dl, max(a.ACCIDENT_DATE) last_dt,
        count_if(a.ACCIDENT_DATE > dateadd(year,1,m.sdt)) n_1yr
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS a join m on a.MINE_ID=m.MINE_ID and a.ACCIDENT_DATE > dateadd(day,30,m.sdt) group by 1),
v as (select v.MINE_ID, count(*) n, count_if(v.IS_SIGNIFICANT_AND_SUBSTANTIAL) ss, max(v.VIOLATION_OCCUR_DATE) last_dt,
        count_if(v.VIOLATION_OCCUR_DATE > dateadd(year,1,m.sdt)) n_1yr
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v join m on v.MINE_ID=m.MINE_ID and v.VIOLATION_OCCUR_DATE > dateadd(day,30,m.sdt) group by 1),
j as (select m.*, a.n acc, a.fat, a.dl, a.last_dt acc_last, a.n_1yr acc_1yr, v.n viol, v.ss, v.last_dt viol_last, v.n_1yr viol_1yr
      from m left join a using (MINE_ID) left join v using (MINE_ID))
select 'status' k, st a, count(*)::text b, count_if(acc>0)::text c, sum(acc)::text d, sum(fat)::text e, sum(dl)::text f,
  count_if(viol>0)::text g, sum(viol)::text h, count_if(acc_1yr>0)::text i, count_if(viol_1yr>0)::text l, null o
from j group by 2
union all
select 'range', 'acc/viol dates', (select min(ACCIDENT_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS),
  (select max(ACCIDENT_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS),
  (select min(VIOLATION_OCCUR_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS),
  (select max(VIOLATION_OCCUR_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS), null,null,null,null,null,null
union all
(select 'mine', MINE_ID||' '||nm, st||' '||sdt::text, ctrl, STATE||' '||cm, acc::text, fat::text, dl::text, acc_1yr::text, acc_last::text, viol::text, viol_last::text
 from j where acc_1yr>0 order by acc_1yr desc, acc desc limit 25)
