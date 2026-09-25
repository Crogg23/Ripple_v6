-- one row per SCDB case, every term; within-case consistency counts for the fields the lead leans on
select TERM, CASE_ID, any_value(CASE_NAME) CASE_NAME, count(*) N_ROWS, count(distinct DOCKET_ID) N_DOCKET,
  count(distinct PETITIONER_CODE) ND_PET, count(distinct CASE_SOURCE_CODE) ND_SRC, count(distinct DECISION_TYPE_CODE) ND_DT,
  count(distinct PARTY_WINNING) ND_PW, count(distinct TERM) ND_TERM,
  any_value(PETITIONER_CODE) PET, any_value(PETITIONER_STATE_CODE) PET_ST, any_value(RESPONDENT_CODE) RESP,
  any_value(CASE_SOURCE_CODE) SRC, any_value(CASE_SOURCE_STATE_CODE) SRC_ST,
  any_value(CASE_ORIGIN_CODE) ORIG, any_value(CASE_ORIGIN_STATE_CODE) ORIG_ST,
  any_value(DECISION_TYPE_CODE) DT, any_value(PARTY_WINNING) PW, any_value(CERT_REASON_CODE) CERT,
  any_value(JURISDICTION_CODE) JUR, any_value(LC_DISAGREEMENT) LCD, any_value(CASE_DISPOSITION_CODE) DISP,
  min(DATE_ARGUMENT) DARG, min(DATE_DECISION) DDEC, any_value(ISSUE_AREA_CODE) IA, count(distinct _SOURCE_RUN_ID) N_RUNS
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
group by 1,2
