-- FEC bulk (2024 committee file) candidate committees -> candidate's latest election year -> 2024 and 2026 money totals; plus whether the same name runs under another candidate ID (zombie-campaign test)
WITH b AS (SELECT FEC_CMTE_ID, CMTE_NM, TRES_NM, CMTE_DSGN, CMTE_TP, CMTE_FILING_FREQ, CMTE_ST, TRIM(FEC_CAND_ID) cand
           FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_BULK WHERE CMTE_DSGN IN ('P','A') AND NULLIF(TRIM(FEC_CAND_ID),'') IS NOT NULL)
, c AS (SELECT CAND_ID, MAX(TRY_TO_NUMBER(CAND_ELECTION_YR::varchar)) last_yr, MAX(CYCLE) last_cycle, MAX(CAND_NAME) cand_name,
               MAX(OFFICE) office, MAX(OFFICE_STATE) ost, LISTAGG(DISTINCT CAND_STATUS, ',') statuses
        FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1)
, other AS (SELECT UPPER(TRIM(CAND_NAME)) nm, CAND_ID, TRY_TO_NUMBER(CAND_ELECTION_YR::varchar) yr FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE)
, s AS (SELECT CAND_ID, CYCLE, TRY_TO_DOUBLE(TTL_RECEIPTS::varchar) rec, TRY_TO_DOUBLE(TTL_DISB::varchar) disb, TRY_TO_DOUBLE(TTL_INDIV_CONTRIB::varchar) indiv,
               TRY_TO_DOUBLE(CASH_ON_HAND_CLOSE::varchar) coh, TRY_TO_DOUBLE(TRANS_TO_AUTH::varchar) to_auth, INCUMBENT_CHALLENGER ic, COVERAGE_END_DATE::varchar cvg
        FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY)
SELECT b.*, c.last_yr, c.last_cycle, c.cand_name, c.office, c.ost, c.statuses,
       (SELECT MAX(o.yr) FROM other o WHERE o.nm = UPPER(TRIM(c.cand_name)) AND o.CAND_ID <> b.cand) other_id_max_yr,
       s24.rec rec24, s24.disb disb24, s24.indiv indiv24, s24.coh coh24, s24.to_auth to_auth24, s24.ic ic24, s24.cvg cvg24,
       s26.rec rec26, s26.disb disb26, s26.coh coh26, s26.ic ic26, s26.cvg cvg26
FROM b LEFT JOIN c ON c.CAND_ID = b.cand
LEFT JOIN s s24 ON s24.CAND_ID = b.cand AND s24.CYCLE = 2024
LEFT JOIN s s26 ON s26.CAND_ID = b.cand AND s26.CYCLE = 2026
