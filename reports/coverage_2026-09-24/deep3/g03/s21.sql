-- S21 Is the DOJ link table complete enough for a miss to mean anything? Size, date span, and known hospital cases
SELECT COUNT(*) n, COUNT(DISTINCT link_text) texts, MIN(captured_at) c0, MAX(captured_at) c1,
       COUNT_IF(link_text ILIKE '%hospital%') hospital_links, COUNT_IF(link_text ILIKE '%prime healthcare%') prime,
       COUNT_IF(link_text ILIKE '%community health systems%') chs, COUNT_IF(link_text ILIKE '%false claims%') fca,
       COUNT_IF(link_text ILIKE '%medically unnecessary%' OR link_text ILIKE '%unnecessary inpatient%') unnecessary
FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
