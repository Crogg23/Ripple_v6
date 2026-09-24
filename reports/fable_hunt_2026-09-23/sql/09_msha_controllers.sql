select min(CAL_YR), max(CAL_YR), count(*) from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS;
select min(CAL_YR), max(CAL_YR), count(*), sum(iff(IS_FATALITY,1,0)) fatal from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS;
with v as (
  select CONTROLLER_ID, max(CONTROLLER_NAME) ctrl, count(*) viol, sum(iff(IS_SIGNIFICANT_AND_SUBSTANTIAL,1,0)) ss, sum(PROPOSED_PENALTY) proposed, sum(AMOUNT_PAID) paid, count(distinct MINE_ID) mines
  from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS where CAL_YR between 2018 and 2024 group by 1),
a as (
  select CONTROLLER_ID, count(*) accidents, sum(iff(IS_FATALITY,1,0)) fatal, sum(DAYS_LOST) days_lost
  from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS where CAL_YR between 2018 and 2024 group by 1),
m as (
  select CURRENT_CONTROLLER_ID CONTROLLER_ID, sum(NO_EMPLOYEES) employees, count(*) mines_now, sum(iff(IS_ACTIVE,1,0)) active_mines
  from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 1)
select v.ctrl, v.CONTROLLER_ID, v.mines, m.employees, v.viol, v.ss, round(v.proposed/1e6,2) proposed_m, round(v.paid/1e6,2) paid_m, round(100*v.paid/nullif(v.proposed,0),0) pct_paid,
  a.accidents, a.fatal, round(1000.0*v.ss/nullif(m.employees,0),1) ss_per_1k_emp, round(1000.0*a.accidents/nullif(m.employees,0),1) acc_per_1k_emp
from v left join a using (CONTROLLER_ID) left join m using (CONTROLLER_ID)
where m.employees >= 500 order by a.fatal desc nulls last, ss_per_1k_emp desc limit 40;
