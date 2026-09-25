-- Debt cliff, public debt only (PPG, strips out private project finance): 2026-28 peak vs 2024 exports and vs the same country 2019-24 max; all countries so the median peer is visible
with ids as (select trim(COUNTRY_CODE) cc, max(COUNTRY_NAME) nm,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', greatest(coalesce(try_to_double(C_2026),0), coalesce(try_to_double(C_2027),0), coalesce(try_to_double(C_2028),0)), null)) ppg_peak,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', try_to_double(C_2026), null)) ppg26,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', try_to_double(C_2024), null)) ppg24,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', greatest(coalesce(try_to_double(C_2019),0), coalesce(try_to_double(C_2020),0), coalesce(try_to_double(C_2021),0),
        coalesce(try_to_double(C_2022),0), coalesce(try_to_double(C_2023),0), coalesce(try_to_double(C_2024),0)), null)) ppg_hist,
    max(iff(SERIES_CODE='DT.TDS.PBND.CD', greatest(coalesce(try_to_double(C_2026),0), coalesce(try_to_double(C_2027),0), coalesce(try_to_double(C_2028),0)), null)) bond_peak,
    max(iff(SERIES_CODE='BX.GSR.TOTL.CD', coalesce(try_to_double(C_2024), try_to_double(C_2023)), null)) ex
  from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS group by 1),
m as (select COUNTRY_CODE cc, max(IS_AGGREGATE) agg from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF group by 1),
j as (select ids.*, 100*ppg_peak/nullif(ex,0) peak_pct_ex, 100*ppg24/nullif(ex,0) y24_pct_ex, ppg_peak/nullif(ppg_hist,0) vs_hist
      from ids join m using (cc) where not m.agg and cc <> 'LDC' and ex > 0)
select 'median' k, null cc, null nm, count(*)::text a, round(median(peak_pct_ex),1)::text b, round(median(y24_pct_ex),1)::text c, round(median(vs_hist),2)::text d,
  count_if(peak_pct_ex >= 30)::text e, count_if(vs_hist >= 1.5)::text f, count_if(peak_pct_ex >= 30 and vs_hist >= 1.5)::text g
from j
union all
(select 'top', cc, nm, round(ppg_peak/1e9,2)::text, round(peak_pct_ex,1)::text, round(y24_pct_ex,1)::text, round(vs_hist,2)::text,
   round(ppg24/1e9,2)::text, round(ex/1e9,1)::text, round(bond_peak/1e9,2)::text
 from j order by peak_pct_ex desc limit 15)
union all
(select 'jump', cc, nm, round(ppg_peak/1e9,2)::text, round(peak_pct_ex,1)::text, round(y24_pct_ex,1)::text, round(vs_hist,2)::text,
   round(ppg24/1e9,2)::text, round(ex/1e9,1)::text, round(bond_peak/1e9,2)::text
 from j where peak_pct_ex >= 15 order by vs_hist desc limit 10)
