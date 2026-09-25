-- Is the 13F info table the same zip window already inside FINANCE__FED_SEC_13F_HOLDINGS? Compare accessions and lines
WITH s AS (SELECT ACCESSION_NUMBER a, COUNT(*) n, SUM(TRY_TO_DOUBLE(VALUE_COL)) v FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSION GROUP BY 1),
     h AS (SELECT ACCESSION_NUMBER a, SRC_FILE, COUNT(*) n, SUM(VALUE_USD) v, MAX(VALUE_UNIT) unit
           FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS
           WHERE ACCESSION_NUMBER IN (SELECT a FROM s) OR SRC_FILE ILIKE '%2026%'
           GROUP BY 1, 2)
SELECT h.SRC_FILE, h.unit, COUNT(*) h_accessions, SUM(h.n) h_lines, SUM(h.v) h_value,
       COUNT(s.a) matched_accessions, SUM(s.n) s_lines_matched, SUM(s.v) s_value_matched,
       COUNT_IF(s.a IS NOT NULL AND s.n <> h.n) line_count_mismatch,
       (SELECT COUNT(*) FROM s) s_accessions_total, (SELECT SUM(n) FROM s) s_lines_total
FROM h LEFT JOIN s ON s.a = h.a
GROUP BY 1, 2 ORDER BY 1
