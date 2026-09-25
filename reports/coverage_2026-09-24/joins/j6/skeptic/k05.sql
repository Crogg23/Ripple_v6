with r as (
 select SUB_ID, CYCLE_FILE, CMTE_ID, upper(DONOR_NAME) d, upper(CITY) city, STATE, ZIP_CODE, upper(EMPLOYER) emp, upper(OCCUPATION) occ, ENTITY_TYPE, TRANSACTION_TYPE, TRANSACTION_DATE, TRANSACTION_AMT, MEMO_CD, IS_MEMO_TRANSACTION, OTHER_ID
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS where CMTE_ID = 'C00796045')
select 'ADELSON_ANY' k, CYCLE_FILE::string c, d, city||' '||STATE||' '||ZIP_CODE loc, emp||' / '||occ eo, ENTITY_TYPE||' '||TRANSACTION_TYPE||' '||coalesce(MEMO_CD,'-') t, TRANSACTION_DATE::string dt, TRANSACTION_AMT amt, SUB_ID::string sid
from r where d like '%ADELSON%'
union all
select 'BY_ETYPE_2024', CYCLE_FILE::string, ENTITY_TYPE, TRANSACTION_TYPE, coalesce(MEMO_CD,'-'), count(*)::string||' rows / '||count(distinct SUB_ID)::string||' subids', min(TRANSACTION_DATE)::string||'..'||max(TRANSACTION_DATE)::string, sum(TRANSACTION_AMT), null
from r group by CYCLE_FILE, ENTITY_TYPE, TRANSACTION_TYPE, MEMO_CD
union all
select * from (select 'TOP_2024', CYCLE_FILE::string, d, city||' '||STATE, max(ENTITY_TYPE), null, null, sum(TRANSACTION_AMT) a, null from r where coalesce(MEMO_CD,'')<>'X' and CYCLE_FILE=2024 group by CYCLE_FILE, d, city, STATE qualify row_number() over (order by a desc) <= 8)
order by 1,2,8 desc
