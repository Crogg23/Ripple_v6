-- Debt cliff source check: which World Bank IDS series carry 2026-2032 projections, Gabon values to match the mart, and denominators; plus rows where total <> principal + interest
select 'series' k, SERIES_CODE a, left(SERIES_NAME,90) b, count(*)::text c, count_if(try_to_double(C_2030) is not null)::text d,
  count_if(try_to_double(C_2024) is not null)::text e, count_if(try_to_double(C_2025) is not null)::text f,
  max(iff(COUNTRY_CODE='GAB', C_2031, null)) g, max(iff(COUNTRY_CODE='GAB', C_2024, null)) h
from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS
group by 2,3
having count_if(try_to_double(C_2030) is not null) > 0
   or SERIES_CODE in ('BX.GSR.TOTL.CD','NY.GNP.MKTP.CD','DT.TDS.DECT.EX.ZS','DT.TDS.DECT.GN.ZS','DT.TDS.DLXF.CD','DT.TDS.DECT.CD','DT.AMT.DLXF.CD','DT.INT.DLXF.CD')
union all
(select 'diff', COUNTRY_CODE||' '||DATA_YEAR, round(TOTAL_DEBT_SERVICE_USD/1e9,3)::text, round(PRINCIPAL_REPAYMENT_USD/1e9,3)::text, round(INTEREST_PAYMENT_USD/1e9,3)::text,
   round((TOTAL_DEBT_SERVICE_USD-PRINCIPAL_REPAYMENT_USD-INTEREST_PAYMENT_USD)/1e9,3)::text,
   round((TOTAL_DEBT_SERVICE_USD-PRINCIPAL_REPAYMENT_USD-INTEREST_PAYMENT_USD)/nullif(TOTAL_DEBT_SERVICE_USD,0),3)::text, IS_AGGREGATE::text, null
 from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF
 where COUNTRY_CODE in ('GAB','CHN','THA','IDN','MNE') and DATA_YEAR in (2026, 2030, 2031))
