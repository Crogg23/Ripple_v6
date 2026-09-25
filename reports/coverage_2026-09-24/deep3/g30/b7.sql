-- S23 2024 cycle, per PAC: leadership and non-connected PACs with $250K+ spending and 75%+ of money straight from individuals; itemized individual dollars from the FEC contributions file (memo rows out) to split small-dollar money from big
WITH p AS (SELECT CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, IFF(COMMITTEE_DESIGNATION = 'D', 'leadership', 'nonconnected') grp, COVERAGE_END_DATE,
                  TOTAL_RECEIPTS rcpt, INDIVIDUAL_CONTRIBUTIONS indiv, TOTAL_DISBURSEMENTS disb, CASH_CLOSE_OF_PERIOD cash_close,
                  (COALESCE(CONTRIBUTIONS_TO_OTHER_COMMITTEES,0) + COALESCE(INDEPENDENT_EXPENDITURES,0) + COALESCE(TRANSFERS_TO_AFFILIATES,0)) to_others
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
           WHERE COVERAGE_END_DATE BETWEEN '2023-01-01' AND '2024-12-31' AND CMTE_ID NOT IN ('C00828541','C00762591') AND TOTAL_DISBURSEMENTS >= 250000
             AND INDIVIDUAL_CONTRIBUTIONS / NULLIF(TOTAL_RECEIPTS,0) >= 0.75
             AND (COMMITTEE_DESIGNATION = 'D' OR (COMMITTEE_DESIGNATION = 'U' AND COMMITTEE_TYPE IN ('N','Q')))),
it AS (SELECT CMTE_ID, SUM(TRANSACTION_AMT) itemized, COUNT(*) item_rows, MEDIAN(TRANSACTION_AMT) med_item
       FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
       WHERE CYCLE_FILE = 2024 AND COALESCE(MEMO_CD,'') <> 'X' AND CMTE_ID IN (SELECT CMTE_ID FROM p)
       GROUP BY 1)
SELECT p.grp, p.CMTE_ID, p.COMMITTEE_NAME, p.COMMITTEE_TYPE, p.COVERAGE_END_DATE, ROUND(p.rcpt) rcpt, ROUND(p.indiv) indiv, ROUND(it.itemized) itemized,
       ROUND(1 - it.itemized / NULLIF(p.indiv,0), 3) unitemized_share, it.item_rows, it.med_item,
       ROUND(p.disb) disb, ROUND(p.to_others) to_others, ROUND(p.to_others / p.disb, 3) share, ROUND(p.cash_close) cash_close
FROM p LEFT JOIN it ON it.CMTE_ID = p.CMTE_ID
ORDER BY p.grp, p.disb DESC;
