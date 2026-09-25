with ie as (select *, try_to_date(EXP_DATE,'DD-MON-YY') d from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where SPE_ID = 'C00796045')
select upper(CAND_NAME) cand, CAN_OFFICE_STATE st, SUP_OPP, FEC_ELECTION_YR, IS_SUPERSEDED::string sup, AMNDT_IND,
 count(*) n, count(distinct TRAN_ID) tran_ids, count(distinct FILE_NUM) files, sum(EXP_AMO) amt, min(d) d0, max(d) d1,
 count(distinct TRAN_ID||'|'||EXP_AMO::string||'|'||EXP_DATE) distinct_lines
from ie group by 1,2,3,4,5,6 order by 4,1,5
