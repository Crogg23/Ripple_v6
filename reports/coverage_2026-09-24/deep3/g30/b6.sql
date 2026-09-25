-- S21 Mechanism test: leadership vs non-connected PACs with $250K+ spending, split by how much of their money came straight from individual donors (75%+ or not), by cycle
WITH p AS (SELECT CMTE_ID, IFF(COMMITTEE_DESIGNATION = 'D', 'leadership', 'nonconnected') grp,
                  YEAR(COVERAGE_END_DATE) + MOD(YEAR(COVERAGE_END_DATE), 2) cyc, TOTAL_DISBURSEMENTS disb, INDIVIDUAL_CONTRIBUTIONS indiv, TOTAL_RECEIPTS rcpt,
                  (COALESCE(CONTRIBUTIONS_TO_OTHER_COMMITTEES,0) + COALESCE(INDEPENDENT_EXPENDITURES,0) + COALESCE(TRANSFERS_TO_AFFILIATES,0)) to_others
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
           WHERE COVERAGE_END_DATE IS NOT NULL AND CMTE_ID NOT IN ('C00828541','C00762591') AND TOTAL_DISBURSEMENTS >= 250000
             AND (COMMITTEE_DESIGNATION = 'D' OR (COMMITTEE_DESIGNATION = 'U' AND COMMITTEE_TYPE IN ('N','Q'))))
SELECT grp, cyc, IFF(indiv / NULLIF(rcpt,0) >= 0.75, 'indiv75', 'other') funding, COUNT(*) pacs,
       ROUND(MEDIAN(to_others / disb),3) med_share, ROUND(SUM(to_others)/SUM(disb),3) wshare,
       ROUND(SUM(disb)/1e6,1) disb_m, ROUND(SUM(indiv)/1e6,1) indiv_m, ROUND(SUM(to_others)/1e6,1) to_others_m
FROM p GROUP BY 1,2,3 ORDER BY 1,2,3;

-- S22 Same leadership PACs 2022 to 2024: did the ones that switched to individual-donor money drop their giving share more? Plus the insider-trade table's date coverage (for the S16 join)
WITH p AS (SELECT CMTE_ID, YEAR(COVERAGE_END_DATE) + MOD(YEAR(COVERAGE_END_DATE), 2) cyc, TOTAL_DISBURSEMENTS disb,
                  INDIVIDUAL_CONTRIBUTIONS / NULLIF(TOTAL_RECEIPTS,0) ish,
                  (COALESCE(CONTRIBUTIONS_TO_OTHER_COMMITTEES,0) + COALESCE(INDEPENDENT_EXPENDITURES,0) + COALESCE(TRANSFERS_TO_AFFILIATES,0)) / NULLIF(TOTAL_DISBURSEMENTS,0) share
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
           WHERE COMMITTEE_DESIGNATION = 'D' AND COVERAGE_END_DATE IS NOT NULL AND CMTE_ID NOT IN ('C00828541','C00762591')),
pr AS (SELECT a.CMTE_ID, a.share s0, b.share s1, a.ish i0, b.ish i1 FROM p a JOIN p b ON a.CMTE_ID = b.CMTE_ID AND a.cyc = 2022 AND b.cyc = 2024
       WHERE a.disb >= 250000 AND b.disb >= 250000)
SELECT CASE WHEN i1 - i0 >= 0.25 THEN 'indiv share up 25+ pts' WHEN i1 - i0 <= -0.25 THEN 'indiv share down 25+ pts' ELSE 'about the same' END funding_shift,
       COUNT(*) pacs, ROUND(MEDIAN(s0),3) med_s22, ROUND(MEDIAN(s1),3) med_s24, ROUND(MEDIAN(s1 - s0),3) med_change, ROUND(MEDIAN(i0),3) med_i22, ROUND(MEDIAN(i1),3) med_i24,
       (SELECT MIN(TRANSACTION_DATE) || ' to ' || MAX(TRANSACTION_DATE) || ', rows since 2025-04-01: ' || COUNT_IF(TRANSACTION_DATE >= '2025-04-01')
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS WHERE TRANSACTION_DATE BETWEEN '2000-01-01' AND '2026-12-31') insider_dates
FROM pr GROUP BY 1 ORDER BY 1;
