with v as (
  select CONTROLLER_ID, max(CONTROLLER_NAME) ctrl, count(*) viol, sum(iff(IS_SIGNIFICANT_AND_SUBSTANTIAL,1,0)) ss, sum(PROPOSED_PENALTY) proposed, sum(AMOUNT_PAID) paid
  from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS where CAL_YR between 2018 and 2024 group by 1),
a as (select CONTROLLER_ID, count(*) accidents, sum(iff(IS_FATALITY,1,0)) fatal from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS where CAL_YR between 2018 and 2024 group by 1),
m as (select CURRENT_CONTROLLER_ID CONTROLLER_ID, sum(NO_EMPLOYEES) employees, max(COAL_METAL_IND) cm from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 1),
top as (
  select v.ctrl, v.CONTROLLER_ID, m.employees, m.cm, v.ss, round(1000.0*v.ss/nullif(m.employees,0)) ss_per_1k, a.fatal, round(100*v.paid/nullif(v.proposed,0)) pct_paid,
    upper(regexp_replace(split_part(v.ctrl,' ',1),'[^A-Z0-9]','')) w1, upper(regexp_replace(split_part(v.ctrl,' ',2),'[^A-Z0-9]','')) w2
  from v left join a using (CONTROLLER_ID) left join m using (CONTROLLER_ID) where m.employees >= 500),
fec as (
  select upper(regexp_replace(EMPLOYER,'[^A-Z0-9 ]','')) emp, DONOR_NAME, OCCUPATION, TRANSACTION_AMT, CMTE_ID, CYCLE_FILE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS where CYCLE_FILE in ('2020','2022','2024','2026') and ENTITY_TYPE='IND' and MEMO_CD is distinct from 'X' and EMPLOYER is not null),
j as (
  select top.ctrl, top.CONTROLLER_ID, top.employees, top.cm, top.ss, top.ss_per_1k, top.fatal, top.pct_paid, fec.DONOR_NAME, fec.OCCUPATION, fec.TRANSACTION_AMT, fec.CMTE_ID
  from top join fec on fec.emp like top.w1 || ' ' || top.w2 || '%' where length(top.w1) >= 3 and length(top.w2) >= 3 and top.w1 not in ('THE') )
select ctrl, cm, employees, ss, ss_per_1k, fatal, pct_paid, count(*) gifts, count(distinct DONOR_NAME) donors, round(sum(TRANSACTION_AMT)) usd, max_by(DONOR_NAME, TRANSACTION_AMT) top_donor, max(TRANSACTION_AMT) top_gift
from j group by 1,2,3,4,5,6,7 order by usd desc limit 30
