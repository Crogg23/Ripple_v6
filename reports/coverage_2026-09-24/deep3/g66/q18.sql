-- CFTC peer + time: electricity futures (commodity code 064) by hub family and year, 2016 - Aug 2026.
-- Open-interest-weighted share of the short side and the long side held by the 4 biggest traders.
-- Question: is PJM's rise in top-4 short concentration PJM-only, or every power hub?
with f as (select upper(MARKET_AND_EXCHANGE_NAMES) nm, year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) yr, AS_OF_DATE_IN_FORM_YYYY_MM_DD d,
             try_to_number(trim(OPEN_INTEREST_ALL)) oi, try_to_number(trim(TRADERS_TOTAL_ALL)) tr,
             CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL g4s, CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL g4l, trim(CFTC_CONTRACT_MARKET_CODE) code
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
           where CFTC_COMMODITY_CODE = '064' and AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2016-01-01' and greatest(g4s, g4l) <= 100),
h as (select *, case when nm like '%PJM%' then 'PJM' when nm like '%ISO NE%' or nm like '%MASS HUB%' then 'ISO-NE'
                     when nm like '%ERCOT%' then 'ERCOT' when nm like '%MISO%' or nm like '%INDIANA%' then 'MISO'
                     when nm like '%NYISO%' or nm like '%NY ZONE%' or nm like '%ZONE G%' or nm like '%ZONE J%' or nm like '%ZONE A%' then 'NYISO'
                     when nm like '%SP15%' or nm like '%NP15%' or nm like '%CAISO%' or nm like '%PALO VERDE%' or nm like '%MID-C%' or nm like '%MID C%' or nm like '%MIDC%' then 'WEST'
                     else 'OTHER' end hub
      from f)
select hub, yr, count(distinct code) contracts, count(*) contract_weeks,
  round(sum(g4s*oi)/nullif(sum(oi),0),1) w_g4s, round(sum(g4l*oi)/nullif(sum(oi),0),1) w_g4l,
  round(median(g4s),1) med_g4s, round(avg(oi)*count(distinct code)/1000,0) approx_oi_k, round(median(tr),0) med_traders
from h group by 1,2 order by 1,2
