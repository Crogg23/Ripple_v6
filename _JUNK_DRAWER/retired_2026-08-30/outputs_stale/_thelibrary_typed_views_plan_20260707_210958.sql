-- Generated typed-view DDL (preview). Apply with scripts/thelibrary_typed_views.py --apply.

CREATE OR REPLACE VIEW THE_LIBRARY.CAMPAIGN_FINANCE.CANDIDATE_FINANCE_SUMMARY COPY GRANTS COMMENT='One row per federal candidate per election cycle: total money raised, total spent, cash on hand, individual contributions, loans, and debts. This is the ONLY FEC bulk file that carries dollar amounts, so it''s the source of every ''candidate raised $X'' number. Keyed by FEC candidate ID (CAND_ID) to link back to the campaigns and committees. Raw landing, values stored as text; 7,933 rows.' AS
SELECT
    "CAND_ID",
    "CAND_NAME",
    "CAND_ICI",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("PTY_CD"),'nan'),'NaN'),'NAN'),'')) AS "PTY_CD",
    "CAND_PTY_AFFILIATION",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("TTL_RECEIPTS"),'nan'),'NaN'),'NAN'),'')) AS "TTL_RECEIPTS",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("TRANS_FROM_AUTH"),'nan'),'NaN'),'NAN'),'')) AS "TRANS_FROM_AUTH",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("TTL_DISB"),'nan'),'NaN'),'NAN'),'')) AS "TTL_DISB",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("TRANS_TO_AUTH"),'nan'),'NaN'),'NAN'),'')) AS "TRANS_TO_AUTH",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("COH_BOP"),'nan'),'NaN'),'NAN'),'')) AS "COH_BOP",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("COH_COP"),'nan'),'NaN'),'NAN'),'')) AS "COH_COP",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_CONTRIB"),'nan'),'NaN'),'NAN'),'')) AS "CAND_CONTRIB",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_LOANS"),'nan'),'NaN'),'NAN'),'')) AS "CAND_LOANS",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("OTHER_LOANS"),'nan'),'NaN'),'NAN'),'')) AS "OTHER_LOANS",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_LOAN_REPAY"),'nan'),'NaN'),'NAN'),'')) AS "CAND_LOAN_REPAY",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("OTHER_LOAN_REPAY"),'nan'),'NaN'),'NAN'),'')) AS "OTHER_LOAN_REPAY",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("DEBTS_OWED_BY"),'nan'),'NaN'),'NAN'),'')) AS "DEBTS_OWED_BY",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("TTL_INDIV_CONTRIB"),'nan'),'NaN'),'NAN'),'')) AS "TTL_INDIV_CONTRIB",
    "CAND_OFFICE_ST",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_OFFICE_DISTRICT"),'nan'),'NaN'),'NAN'),'')) AS "CAND_OFFICE_DISTRICT",
    "SPEC_ELECTION",
    "PRIM_ELECTION",
    "RUN_ELECTION",
    "GEN_ELECTION",
    "GEN_ELECTION_PRECENT",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("OTHER_POL_CMTE_CONTRIB"),'nan'),'NaN'),'NAN'),'')) AS "OTHER_POL_CMTE_CONTRIB",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("POL_PTY_CONTRIB"),'nan'),'NaN'),'NAN'),'')) AS "POL_PTY_CONTRIB",
    CASE WHEN TRIM("CVG_END_DT") LIKE '%-%' OR TRIM("CVG_END_DT") LIKE '%/%' THEN TRY_TO_DATE(TRIM("CVG_END_DT")) END AS "CVG_END_DT",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("INDIV_REFUNDS"),'nan'),'NaN'),'NAN'),'')) AS "INDIV_REFUNDS",
    TRY_TO_DOUBLE(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CMTE_REFUNDS"),'nan'),'NaN'),'NAN'),'')) AS "CMTE_REFUNDS",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CYCLE"),'nan'),'NaN'),'NAN'),'')) AS "CYCLE",
    "_INGESTED_AT",
    "_SOURCE_RUN_ID",
    "_SRC_SHA256"
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_SUMMARY;

CREATE OR REPLACE VIEW THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATES_FED_FEC_BULK_CANDIDATES COPY GRANTS COMMENT='The FEC candidate master: one row per registered federal candidate per cycle (17,900 rows) -- FEC candidate ID, name, office sought, party, state, district, and incumbent/challenger/open-seat status. The anchor that ties a candidate ID to a name and office across the whole money-in-politics stack. Links to committees and donations via CAND_ID. Raw text landing (FEC bulk cn.txt).' AS
SELECT
    "CAND_ID",
    "CAND_NAME",
    "CAND_PTY_AFFILIATION",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_ELECTION_YR"),'nan'),'NaN'),'NAN'),'')) AS "CAND_ELECTION_YR",
    "CAND_OFFICE_ST",
    "CAND_OFFICE",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_OFFICE_DISTRICT"),'nan'),'NaN'),'NAN'),'')) AS "CAND_OFFICE_DISTRICT",
    "CAND_ICI",
    "CAND_STATUS",
    "CAND_PCC",
    "CAND_ST1",
    "CAND_ST2",
    "CAND_CITY",
    "CAND_ST",
    "CAND_ZIP",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CYCLE"),'nan'),'NaN'),'NAN'),'')) AS "CYCLE",
    "_INGESTED_AT",
    "_SOURCE_RUN_ID",
    "_SRC_SHA256"
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_CANDIDATES;

CREATE OR REPLACE VIEW THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATE_COMMITTEE_LINKS COPY GRANTS COMMENT='The FEC candidate-to-committee linkage table (ccl.txt): 16,327 rows connecting each candidate ID to the committee IDs authorized by or linked to them, with committee type and designation. This is the clean join that lets you roll individual donations up from a committee to the actual candidate who benefits. Raw landing, all text.' AS
SELECT
    "CAND_ID",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CAND_ELECTION_YR"),'nan'),'NaN'),'NAN'),'')) AS "CAND_ELECTION_YR",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("FEC_ELECTION_YR"),'nan'),'NaN'),'NAN'),'')) AS "FEC_ELECTION_YR",
    "CMTE_ID",
    "CMTE_TP",
    "CMTE_DSGN",
    "LINKAGE_ID",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CYCLE"),'nan'),'NaN'),'NAN'),'')) AS "CYCLE",
    "_INGESTED_AT",
    "_SOURCE_RUN_ID",
    "_SRC_SHA256"
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_LINKAGES;

CREATE OR REPLACE VIEW THE_LIBRARY.CAMPAIGN_FINANCE.FEC_COMMITTEES_2026 COPY GRANTS COMMENT='Every committee registered with the FEC for the 2026 cycle: committee ID, name, treasurer, address, type, party, and the candidate it''s linked to. This is the committee dimension that candidate-to-money links resolve against. Landed alongside the 2024 committee master to close a 2026 gap (2026 linkages resolved only ~57% before this vs. ~98% for 2024). Keyed by FEC committee ID and candidate ID. Raw landing, stored as text; 20,007 rows.' AS
SELECT
    "FEC_CMTE_ID",
    "CMTE_NM",
    "TRES_NM",
    "CMTE_ST1",
    "CMTE_ST2",
    "CMTE_CITY",
    "CMTE_ST",
    "CMTE_ZIP",
    "CMTE_DSGN",
    "CMTE_TP",
    "CMTE_PTY_AFFILIATION",
    "CMTE_FILING_FREQ",
    "ORG_TP",
    "CONNECTED_ORG_NM",
    "FEC_CAND_ID",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("CYCLE"),'nan'),'NaN'),'NAN'),'')) AS "CYCLE",
    "_INGESTED_AT",
    "_SOURCE_RUN_ID",
    "_SRC_SHA256"
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_COMMITTEES;
