-- FEC itemized individual gifts: donor surname DESTEFANE in MO, or employer RELIANT CARE (any state); memo rows dropped; grouped by donor, employer, committee
with g as (select DONOR_NAME, CITY, STATE, EMPLOYER, OCCUPATION, CMTE_ID, TRANSACTION_DATE, TRANSACTION_AMT, CYCLE_FILE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
  where coalesce(MEMO_CD,'') <> 'X' and ((DONOR_NAME ilike 'DESTEFANE%' and STATE='MO') or EMPLOYER ilike '%RELIANT CARE%' or EMPLOYER ilike 'RELIANTCARE%'))
select g.DONOR_NAME, g.CITY, g.EMPLOYER, g.OCCUPATION, g.CMTE_ID, max(c.CMTE_NM) cmte_name, count(*) gifts, sum(g.TRANSACTION_AMT) dollars, min(g.CYCLE_FILE) c0, max(g.CYCLE_FILE) c1
from g left join (select CMTE_ID, max(CMTE_NM) CMTE_NM from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES group by 1) c on c.CMTE_ID=g.CMTE_ID
group by 1,2,3,4,5 order by dollars desc
