-- S19 HCRIS cost reports, California hospitals, every fiscal year: beds, all discharges, Medicare (Title XVIII) discharges and days
--     Time check for the Oroville lead: was its Medicare admission rate always high, or did it jump?
SELECT provider_ccn ccn, hospital_name, fiscal_year_end_date fye, source_file_year, number_of_beds beds,
       total_discharges_all dis_all, total_discharges_title_xviii dis_mcr, total_days_title_xviii days_mcr, total_days_all days_all
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS
WHERE state_code = 'CA'
