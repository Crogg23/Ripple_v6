-- @schedB_liberty_group_addresses
select upper(RECIPIENT_NAME) nm, upper(RECIPIENT_ADDR1) a1, upper(RECIPIENT_ADDR2) a2, upper(RECIPIENT_CITY) city, RECIPIENT_STATE st,
  count(*) n, count(distinct EIN) eins, count(distinct FORM_ID_NUMBER) forms, sum(EXPENDITURE_AMOUNT) amt, min(EXPENDITURE_DATE) d0, max(EXPENDITURE_DATE) d1,
  listagg(distinct ORG_NAME, ' | ') within group (order by ORG_NAME) payers
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES
where upper(RECIPIENT_NAME) like '%LIBERTY GROUP%'
   or regexp_replace(upper(RECIPIENT_ADDR1),'[^A-Z0-9]','') like '11403RDST%'
group by 1,2,3,4,5 order by amt desc
-- @fec_ie_liberty_group_payee
select SPE_NAM, PAY, count(*) n, sum(EXP_AMO) amt, min(EXP_DATE) d0, max(EXP_DATE) d1, listagg(distinct CAND_NAME, ' | ') cands
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
where upper(PAY) like '%LIBERTY GROUP%' or upper(SPE_NAM) like '%RINO HUNTER%' or upper(SPE_NAM) like '%BRIGHTER FUTURE%'
group by 1,2 order by amt desc
