-- NPDES data-flow test for the Missouri/Ohio gap: formal and informal actions on individual permits per year, MO, OH vs all other states.
-- If MO or OH simply stopped sending actions to ICIS, their yearly counts would fall to near zero
with fa as (select substr(NPDES_ID, 1, 2) st, year(SETTLEMENT_ENTERED_DATE) y, count(*) n, count(distinct NPDES_ID) permits
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS
            where substr(NPDES_ID, 3, 1) = '0' and year(SETTLEMENT_ENTERED_DATE) between 2012 and 2026 group by 1, 2),
ia as (select substr(NPDES_ID, 1, 2) st, year(ACHIEVED_DATE) y, count(*) n
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS
       where substr(NPDES_ID, 3, 1) = '0' and year(ACHIEVED_DATE) between 2012 and 2026 group by 1, 2)
select coalesce(fa.y, ia.y) y,
  sum(iff(coalesce(fa.st, ia.st) = 'MO', fa.n, 0)) mo_formal, sum(iff(coalesce(fa.st, ia.st) = 'MO', ia.n, 0)) mo_informal,
  sum(iff(coalesce(fa.st, ia.st) = 'OH', fa.n, 0)) oh_formal, sum(iff(coalesce(fa.st, ia.st) = 'OH', ia.n, 0)) oh_informal,
  sum(iff(coalesce(fa.st, ia.st) not in ('MO', 'OH'), fa.n, 0)) rest_formal, sum(iff(coalesce(fa.st, ia.st) not in ('MO', 'OH'), ia.n, 0)) rest_informal,
  sum(iff(coalesce(fa.st, ia.st) = 'TX', fa.n, 0)) tx_formal, sum(iff(coalesce(fa.st, ia.st) = 'PA', fa.n, 0)) pa_formal
from fa full outer join ia on fa.st = ia.st and fa.y = ia.y
group by 1 order by 1;
