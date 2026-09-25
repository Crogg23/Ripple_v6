-- S06 Inpatient by provider AND DRG, California only: DRG mix of Oroville vs its state peers
SELECT rndrng_prvdr_ccn ccn, rndrng_prvdr_org_name nm, drg_cd, drg_desc, tot_dschrgs, avg_mdcr_pymt_amt
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE
WHERE rndrng_prvdr_state_abrvtn = 'CA'
