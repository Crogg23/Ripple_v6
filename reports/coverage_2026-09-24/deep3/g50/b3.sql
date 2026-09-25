-- S12 MDS: Missouri homes, share of residents coded with schizophrenia (I6000 Yes), to test whether registrant placement just tracks psychiatric specialization
SELECT CCN, MAX(OVERALL_PERCENT) sz_pct, MAX(TRY_TO_NUMBER(TOTAL_RESIDENTS)) sz_n, ANY_VALUE(PROVIDER_NAME) name
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY
WHERE STATE = 'MO' AND MDS_ITEM_QUESTION_DESCRIPTION LIKE 'I6000:%' AND MDS_ITEM_RESPONSE = 'Yes'
GROUP BY 1;
