-- MSHA churn, tested inside the group: do mines that cycle operators leave more assessed penalties unpaid? Plus the operator-by-operator chain at the top three mines
with mines as (select MINE_ID, CURRENT_OPERATOR_ID cop, CURRENT_MINE_STATUS st, COAL_METAL_IND cm from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES),
v as (select v.MINE_ID, v.VIOLATOR_ID, max(v.VIOLATOR_NAME) vname, min(v.VIOLATION_OCCUR_DATE) d0, max(v.VIOLATION_OCCUR_DATE) d1, count(*) n,
        count_if(v.IS_SIGNIFICANT_AND_SUBSTANTIAL) ss, sum(iff(v.VIOLATION_OCCUR_DATE < '2024-01-01', v.AMOUNT_DUE, 0)) due_old,
        sum(iff(v.VIOLATION_OCCUR_DATE < '2024-01-01', v.AMOUNT_PAID, 0)) paid_old, sum(v.PROPOSED_PENALTY) prop
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v join mines m on v.MINE_ID = m.MINE_ID
      where v.VIOLATION_OCCUR_DATE >= '2010-01-01' and length(v.VIOLATOR_ID) = length(m.cop) and left(v.VIOLATOR_ID,1) = left(m.cop,1)
      group by 1, 2),
pm as (select m.MINE_ID, any_value(m.cm) cm, any_value(m.st) st, count(*) nops, sum(v.due_old) due_old, sum(v.paid_old) paid_old, sum(v.n) nviol, sum(v.ss) ss
       from mines m join v on v.MINE_ID = m.MINE_ID group by 1)
select 'bucket' k, cm a, iff(nops >= 3, '3+', nops::text) b, count(*)::text c, round(sum(due_old)/1e6,2)::text d, round(sum(paid_old)/1e6,2)::text e,
  round(100*(1 - sum(paid_old)/nullif(sum(due_old),0)),1)::text f,
  round(100*median(iff(due_old > 0, 1 - paid_old/due_old, null)),1)::text g,
  count_if(due_old > 0 and paid_old/due_old < 0.5)::text h, round(100.0*sum(ss)/nullif(sum(nviol),0),1)::text i
from pm where st in ('Active','Intermittent','Temporarily Idled','NonProducing') group by 2, 3
union all
(select 'chain', MINE_ID, vname, year(d0) || '-' || year(d1), n::text, ss::text, round(prop)::text, round(due_old)::text, round(paid_old)::text, VIOLATOR_ID
 from v where MINE_ID in ('1518001','4407150','1518973') order by MINE_ID, d0)
