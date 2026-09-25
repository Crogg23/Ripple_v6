select CYCLE_FILE, upper(DONOR_NAME) d, upper(CITY) city, STATE, mode(upper(EMPLOYER)) emp, mode(upper(OCCUPATION)) occ,
 ((upper(DONOR_NAME) like 'ADELSON, SHELDON%' or upper(DONOR_NAME) like 'ADELSON, MIRIAM%' or upper(DONOR_NAME) like 'ADELSON, MIRIAN%') and (STATE = 'NV' or upper(CITY) like '%LAS VEGAS%')) in_builder,
 count(*) n, sum(TRANSACTION_AMT) amt
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where CYCLE_FILE >= 2022 and upper(DONOR_NAME) like '%ADELSON%' and coalesce(MEMO_CD,'') <> 'X'
group by 1,2,3,4 having sum(TRANSACTION_AMT) >= 50000 or in_builder
order by 1, amt desc
