-- S18 raw landing job dates for every FracFocus disclosure (the mart's JOB_START_DATE is empty), parsed locally
SELECT DISCLOSUREID, JOBSTARTDATE, JOBENDDATE FROM LIBRARY_RAW.LANDING.FED_FRACFOCUS_DISCLOSURE_LIST
