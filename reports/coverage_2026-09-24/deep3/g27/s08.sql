-- 13F info table: which filings/quarters it holds (join accession to the 13F filings table), units, and duplicate lines
WITH h AS (
  SELECT ACCESSION_NUMBER a, COUNT(*) n, COUNT(DISTINCT INFOTABLE_SK) n_sk,
         SUM(TRY_TO_DOUBLE(VALUE_COL)) v, COUNT_IF(TRY_TO_DOUBLE(VALUE_COL) IS NULL) v_bad,
         COUNT_IF(SSHPRNAMTTYPE = 'PRN') prn, COUNT_IF(NULLIF(TRIM(PUTCALL),'') IS NOT NULL) opt,
         SUM(SSHPRNAMT) sh
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSION GROUP BY 1
)
SELECT s.PERIODOFREPORT, s.SUBMISSIONTYPE, s._SRC_FILE,
       MIN(s.FILING_DATE) f0, MAX(s.FILING_DATE) f1,
       COUNT(*) filings, COUNT(DISTINCT s.CIK) ciks, SUM(h.n) lines, SUM(h.n - h.n_sk) dup_sk, SUM(h.v) value_sum, SUM(h.v_bad) v_bad, SUM(h.prn) prn, SUM(h.opt) opt
FROM h LEFT JOIN LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS s ON s.ACCESSION_NUMBER = h.a
GROUP BY ROLLUP(1, 2, 3) ORDER BY lines DESC NULLS LAST
