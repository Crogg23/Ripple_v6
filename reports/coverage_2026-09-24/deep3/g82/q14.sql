-- Debt cliff with denominators: projected peak (2026-32) vs the same country actual 2019-24 debt service and vs latest exports and GNI, from World Bank IDS
with h as (select COUNTRY_NAME, max(COUNTRY_CODE) ids_code,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2019), null)) t19, max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2020), null)) t20,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2021), null)) t21, max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2022), null)) t22,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2023), null)) t23, max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2024), null)) t24,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2026), null)) p26,
    max(iff(SERIES_CODE='BX.GSR.TOTL.CD', coalesce(try_to_double(C_2024), try_to_double(C_2023)), null)) ex,
    max(iff(SERIES_CODE='NY.GNP.MKTP.CD', coalesce(try_to_double(C_2024), try_to_double(C_2023)), null)) gni
  from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS group by 1),
m as (select COUNTRY_CODE, COUNTRY_NAME, max(IS_AGGREGATE) agg, max(TOTAL_DEBT_SERVICE_USD) peak, max_by(DATA_YEAR, TOTAL_DEBT_SERVICE_USD) peak_yr,
    max(iff(DATA_YEAR=2026, TOTAL_DEBT_SERVICE_USD, null)) d26, max(iff(DATA_YEAR=2027, TOTAL_DEBT_SERVICE_USD, null)) d27,
    listagg(iff(IS_REPAYMENT_CLIFF, DATA_YEAR::text, null), ',') cliff_yrs
  from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF group by 1,2)
select m.COUNTRY_CODE, m.COUNTRY_NAME, h.ids_code, m.agg, m.cliff_yrs, m.peak_yr, round(m.peak/1e9,2) peak_bn, round(m.d26/1e9,2) d26_bn, round(h.p26/1e9,2) ids26_bn,
  round(greatest(coalesce(t19,0),coalesce(t20,0),coalesce(t21,0),coalesce(t22,0),coalesce(t23,0),coalesce(t24,0))/1e9,2) hist_max_bn,
  round(h.t24/1e9,2) t24_bn, round(h.ex/1e9,1) ex_bn, round(h.gni/1e9,1) gni_bn,
  round(100*m.peak/nullif(h.ex,0),1) peak_pct_ex, round(100*m.d26/nullif(h.ex,0),1) d26_pct_ex, round(100*m.peak/nullif(h.gni,0),1) peak_pct_gni,
  round(m.peak/nullif(greatest(coalesce(t19,0),coalesce(t20,0),coalesce(t21,0),coalesce(t22,0),coalesce(t23,0),coalesce(t24,0)),0),2) peak_vs_histmax
from m left join h using (COUNTRY_NAME)
order by m.agg, peak_pct_ex desc nulls last
