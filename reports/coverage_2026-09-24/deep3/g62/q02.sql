-- Delivery companies: all 7 rows with per-customer and per-kWh math, and whether the same utility numbers also sit in the main sales table
with d as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DELIVERY_COMPANIES),
s as (select UTILITY_NUMBER, listagg(distinct SERVICE_TYPE||':'||STATE||':'||PART,'|') svc, sum(RESIDENTIAL_CUSTOMERS) s_res_cust, sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS) s_res_rev
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1)
select d.UTILITY_NUMBER, d.UTILITY_NAME, d.STATE, d.PART, d.SERVICE_TYPE, d.DATA_TYPE, d.OWNERSHIP, d.BA_CODE, d.DATA_YEAR,
 d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS res_rev_k, d.RESIDENTIAL_SALES_MWH res_mwh, d.RESIDENTIAL_CUSTOMERS res_cust,
 round(d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS*1000/nullif(d.RESIDENTIAL_CUSTOMERS,0),0) res_usd_per_cust,
 round(d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS*100/nullif(d.RESIDENTIAL_SALES_MWH,0),2) res_cents_kwh,
 round(d.RESIDENTIAL_SALES_MWH*1000/nullif(d.RESIDENTIAL_CUSTOMERS,0),0) kwh_per_cust,
 d.COMMERCIAL_REVENUES_THOUSAND_DOLLARS com_rev_k, d.COMMERCIAL_SALES_MWH com_mwh, d.COMMERCIAL_CUSTOMERS com_cust,
 d.INDUSTRIAL_REVENUES_THOUSAND_DOLLARS ind_rev_k, d.INDUSTRIAL_SALES_MWH ind_mwh, d.INDUSTRIAL_CUSTOMERS ind_cust,
 d.TOTAL_REVENUES_THOUSAND_DOLLARS tot_rev_k, d.TOTAL_SALES_MWH tot_mwh, d.TOTAL_CUSTOMERS tot_cust, d._SRC_FILE,
 s.svc, s.s_res_cust, s.s_res_rev
from d left join s on s.UTILITY_NUMBER=d.UTILITY_NUMBER order by d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS desc
