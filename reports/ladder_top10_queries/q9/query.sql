-- Q9: original question (years between last Form 5500 filing and PBGC failure, joined on EIN) is BLOCKED:
-- ECONOMICS__FED_PBGC_DATA is the PBGC Pension Insurance Data Book (aggregate statistical tables S-*/M-*/GLANCE,
-- METRIC_NAME/METRIC_VALUE rows, NO EIN, NO plan-level records). No trusteed-plans or Schedule SB table exists in the catalog.
-- The Form 5500 table is a Jan-Jun 2026 received-date slice with plan-year dates 100% NULL.
-- Closest honest charts below.

-- Chart A (result.csv):

-- cumulative plans PBGC has taken over ('trusteed or pending'), per fiscal year, from the Data Book 'GLANCE' pages
-- messy scrape: same figure appears multiple times per year across editions; take MAX (the total incl. single+multiemployer)
SELECT DATA_YEAR fiscal_year, MAX(METRIC_VALUE) plans_trusteed_cumulative
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_PBGC_DATA
WHERE TABLE_NAME='GLANCE' AND METRIC_NAME ILIKE 'Plans Trusteed or Pending Trusteeship%' AND METRIC_VALUE > 100
GROUP BY 1 ORDER BY 1


-- Chart B (form5500_final_filings_by_state.csv):

-- Form 5500 slice (filings RECEIVED Jan-Jun 2026 only): plans marking this as their FINAL filing
-- dedupe to one row per sponsor-EIN + plan number (plan-number trap: PLAN_NUM sometimes empty, fall back to SPONS_DFE_PN)
WITH f AS (
  SELECT REGEXP_REPLACE(COALESCE(NULLIF(SPONS_DFE_EIN,''),EIN),'[^0-9]','') ein,
         COALESCE(NULLIF(PLAN_NUM,''), NULLIF(SPONS_DFE_PN,''), '?') pn,
         MAX(COALESCE(SPONS_DFE_MAIL_US_STATE,'')) state,
         MAX(IFF(TYPE_PENSION_BNFT_CODE<>'' AND TYPE_PENSION_BNFT_CODE IS NOT NULL,1,0)) is_pension,
         MAX(TOT_PARTCP_BOY_CNT) participants,
         MAX(TOTAL_ASSETS_EOY_AMT) assets_eoy
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500
  WHERE FINAL_FILING_IND='1'
  GROUP BY 1,2
)
SELECT COALESCE(NULLIF(state,''),'(none)') state,
       IFF(is_pension=1,'pension','welfare/other') plan_kind,
       COUNT(*) final_filings, SUM(participants) participants, SUM(assets_eoy) assets_eoy
FROM f GROUP BY 1,2 ORDER BY final_filings DESC
