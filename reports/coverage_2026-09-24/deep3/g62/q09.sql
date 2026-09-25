-- Delivery companies in context: Texas 2024 rows in the main sales table by part/service type (energy-only retailers, bundled utilities),
-- residential $ per customer and cents/kWh, so the wires-only charge can be set against the energy charge and against bundled Texas utilities outside ERCOT.
with s as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where STATE='TX')
select PART, SERVICE_TYPE, BA_CODE, OWNERSHIP, count(*) rows_, count(distinct UTILITY_NUMBER) utils,
  sum(RESIDENTIAL_CUSTOMERS) res_cust, round(sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS)) res_rev_k, sum(RESIDENTIAL_SALES_MWH) res_mwh,
  round(sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS)*1000/nullif(sum(RESIDENTIAL_CUSTOMERS),0)) usd_per_cust,
  round(sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS)*100/nullif(sum(RESIDENTIAL_SALES_MWH),0),2) cents_kwh,
  listagg(distinct DATA_TYPE,'|') dtypes, max(DATA_YEAR) yr
from s group by 1,2,3,4 order by res_cust desc nulls last
