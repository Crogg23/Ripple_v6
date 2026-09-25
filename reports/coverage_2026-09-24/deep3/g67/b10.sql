-- @google_fec_join
-- Google spend rolled up by the FEC ID advertisers gave, joined to the FEC committee list and to PAC/party money totals (all loaded cycles)
WITH g AS (
  SELECT REGEXP_SUBSTR(PUBLIC_IDS_LIST, 'C[0-9]{8}') fec, COUNT(*) accts, SUM(TRY_TO_NUMBER(SPEND_USD)) g_usd,
         LISTAGG(DISTINCT ADVERTISER_NAME, ' | ') WITHIN GROUP (ORDER BY ADVERTISER_NAME) names
  FROM LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS
  WHERE REGIONS LIKE '%US%' AND REGEXP_SUBSTR(PUBLIC_IDS_LIST, 'C[0-9]{8}') IS NOT NULL
  GROUP BY 1),
d AS (SELECT CMTE_ID, MAX(CMTE_NM) cmte_nm, MAX(CMTE_TP) cmte_tp, MAX(CMTE_DSGN) cmte_dsgn, MAX(CYCLE) last_cycle FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM GROUP BY 1),
p AS (SELECT CMTE_ID, COUNT(*) p_rows, COUNT(DISTINCT COVERAGE_END_DATE) p_periods, SUM(TRY_TO_DOUBLE(TOTAL_DISBURSEMENTS::string)) p_disb,
             MIN(COVERAGE_END_DATE::string) p_first, MAX(COVERAGE_END_DATE::string) p_last
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY GROUP BY 1)
SELECT g.*, d.cmte_nm, d.cmte_tp, d.cmte_dsgn, d.last_cycle, p.p_rows, p.p_periods, p.p_disb, p.p_first, p.p_last
FROM g LEFT JOIN d ON d.CMTE_ID = g.fec LEFT JOIN p ON p.CMTE_ID = g.fec
