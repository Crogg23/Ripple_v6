-- MSHA join: operator churn. Violations since 2010 by violator (operator-format IDs only), per mine; how many operators each working mine has cycled through, and what earlier operators left unpaid
with mines as (select MINE_ID, CURRENT_OPERATOR_ID cop, CURRENT_CONTROLLER_ID cid, CURRENT_CONTROLLER_NAME cname, CURRENT_MINE_NAME mname,
                 CURRENT_MINE_STATUS st, COAL_METAL_IND cm, STATE, NO_EMPLOYEES emp
               from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES),
v as (select v.MINE_ID, v.VIOLATOR_ID, max(v.VIOLATOR_NAME) vname, min(v.VIOLATION_OCCUR_DATE) d0, max(v.VIOLATION_OCCUR_DATE) d1, count(*) n,
        sum(iff(v.VIOLATION_OCCUR_DATE < '2024-01-01', coalesce(v.AMOUNT_DUE,0) - coalesce(v.AMOUNT_PAID,0), 0)) unpaid_old
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v join mines m on v.MINE_ID = m.MINE_ID
      where v.VIOLATION_OCCUR_DATE >= '2010-01-01' and length(v.VIOLATOR_ID) = length(m.cop) and left(v.VIOLATOR_ID,1) = left(m.cop,1)
      group by 1, 2),
pm as (select m.MINE_ID, any_value(m.cop) cop, any_value(m.cid) cid, any_value(m.cname) cname, any_value(m.mname) mname, any_value(m.st) st, any_value(m.cm) cm,
         any_value(m.STATE) state, any_value(m.emp) emp, count(*) nops, count_if(v.VIOLATOR_ID <> m.cop) n_prior,
         sum(iff(v.VIOLATOR_ID <> m.cop, v.unpaid_old, 0)) unpaid_prior, sum(v.unpaid_old) unpaid_all, sum(v.n) nviol,
         listagg(v.vname || ' ' || year(v.d0) || '-' || year(v.d1), ' > ') within group (order by v.d0) chain
       from mines m join v on v.MINE_ID = m.MINE_ID group by m.MINE_ID),
w as (select * from pm where st in ('Active','Intermittent','Temporarily Idled','NonProducing'))
select 'peer' k, cm a, count(*)::text b, median(nops)::text c, count_if(nops >= 3)::text d, count_if(nops >= 4)::text e,
  round(sum(unpaid_prior)/1e6,2)::text f, round(sum(unpaid_all)/1e6,2)::text g, null h, null i
from w group by cm
union all
(select 'ctrl', cname, cid, count(*)::text, count_if(nops >= 3)::text, round(avg(nops),2)::text, round(sum(unpaid_prior)/1e6,2)::text,
   round(sum(unpaid_all)/1e6,2)::text, listagg(distinct state, ','), sum(emp)::text
 from w group by cname, cid order by count_if(nops >= 3) desc, sum(unpaid_prior) desc limit 15)
union all
(select 'ctrl_unpaid', cname, cid, count(*)::text, count_if(nops >= 3)::text, round(avg(nops),2)::text, round(sum(unpaid_prior)/1e6,2)::text,
   round(sum(unpaid_all)/1e6,2)::text, listagg(distinct state, ','), sum(emp)::text
 from w group by cname, cid order by sum(unpaid_prior) desc limit 12)
union all
(select 'mine', MINE_ID || ' ' || mname, st || ' ' || cm || ' ' || state, cname, nops::text, round(unpaid_prior/1e3,1)::text, nviol::text, emp::text, left(chain, 300), null
 from w order by nops desc, unpaid_prior desc limit 15)
