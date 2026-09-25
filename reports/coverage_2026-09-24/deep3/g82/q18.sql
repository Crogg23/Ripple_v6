-- Debt cliff dull-explanation test: split projected debt service into public (PPG), private non-guaranteed (PNG), IMF, bonds, multilateral, bilateral; 2024 actual vs 2026-2030 projection
select trim(COUNTRY_CODE) cc, SERIES_CODE sc,
  round(try_to_double(C_2023)/1e9,3) y23, round(try_to_double(C_2024)/1e9,3) y24, round(try_to_double(C_2025)/1e9,3) y25,
  round(try_to_double(C_2026)/1e9,3) y26, round(try_to_double(C_2027)/1e9,3) y27, round(try_to_double(C_2028)/1e9,3) y28,
  round(try_to_double(C_2029)/1e9,3) y29, round(try_to_double(C_2030)/1e9,3) y30
from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS
where trim(COUNTRY_CODE) in ('MOZ','SEN','BTN','PAK','GMB','MNE','BEN','TGO','GNB','MDG','PRY','LAO','MNG')
  and SERIES_CODE in ('DT.TDS.DECT.CD','DT.TDS.DPPG.CD','DT.TDS.DPNG.CD','DT.TDS.DIMF.CD','DT.TDS.PBND.CD','DT.TDS.MLAT.CD','DT.TDS.BLAT.CD')
order by 1, 2
