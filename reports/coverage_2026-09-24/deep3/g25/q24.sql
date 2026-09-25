-- FEC candidates: 2024 filers by office joined to the FEC candidate summary (cycle 2024): how many raised anything, how many reached $5,000;
-- the one Claremont CA address; and what the 2020 House out-of-state mailing addresses are
with c as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES),
s as (select CAND_ID, max(TTL_RECEIPTS) rcpt from LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY where CYCLE = '2024' group by 1),
c24 as (select distinct CAND_ID, CAND_OFFICE, CAND_STATUS from c where CAND_ELECTION_YR = 2024)
select 'y2024' k, CAND_OFFICE a, null b, count(distinct c24.CAND_ID) n1, count(distinct s.CAND_ID) n2, count(distinct iff(s.rcpt > 0, s.CAND_ID, null)) n3,
  count(distinct iff(s.rcpt >= 5000, s.CAND_ID, null)) n4, count(distinct iff(CAND_STATUS = 'N', c24.CAND_ID, null)) n5
from c24 left join s on s.CAND_ID = c24.CAND_ID group by 2
union all
select 'claremont', upper(trim(CAND_ST1)), null, count(distinct c.CAND_ID), count(distinct s.CAND_ID), count(distinct iff(s.rcpt > 0, s.CAND_ID, null)), min(CAND_ELECTION_YR), max(CAND_ELECTION_YR)
from c left join s on s.CAND_ID = c.CAND_ID where upper(CAND_ST1) like '1742 WOODBEND%' group by 2
union all
select 'oos2020', CAND_ST, CAND_OFFICE_ST, count(*), count(distinct CAND_ID), count_if(nullif(trim(CAND_ST),'') is null), null, null
from c where CAND_ELECTION_YR = 2020 and CAND_OFFICE = 'H' and CAND_ST <> CAND_OFFICE_ST group by 2, 3 qualify row_number() over (order by count(*) desc) <= 12
order by 1, 4 desc
