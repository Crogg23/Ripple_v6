-- S23 Every hospital's sepsis share (DRG 871/872) of its listed Medicare discharges, national, for the two-signal screen
SELECT rndrng_prvdr_ccn ccn, SUM(tot_dschrgs) dis_listed,
       SUM(IFF(drg_cd IN ('871','872'), tot_dschrgs, 0)) sepsis,
       SUM(IFF(drg_cd IN ('312','313'), tot_dschrgs, 0)) syncope_chestpain
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE
GROUP BY 1
