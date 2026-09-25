M = "LIBRARY_MARTS.HEALTH."
PB = f"{M}HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"
PBS = f"{M}HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI"
TOPNP = f"""SELECT RNDRNG_NPI npi FROM {PB} WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'
            QUALIFY RANK() OVER (ORDER BY TOT_MDCR_PYMT_AMT DESC) <= 60"""
QUERIES = [
 ("q15_huntly", "Pending-list NP 1760952360: her Part B 2024 provider row (drug vs medical split, address) plus every surviving service line",
  f"""SELECT 'PROV' lvl, RNDRNG_PRVDR_LAST_ORG_NAME nm, RNDRNG_PRVDR_CRDNTLS cred, RNDRNG_PRVDR_CITY city, RNDRNG_PRVDR_ZIP5 zip,
         NULL hcpcs, NULL descr, NULL pos, TOT_BENES benes, TOT_SRVCS srvcs, TOT_MDCR_PYMT_AMT pay, DRUG_MDCR_PYMT_AMT drug_pay,
         MED_MDCR_PYMT_AMT med_pay, BENE_AVG_AGE avg_age
  FROM {PB} WHERE RNDRNG_NPI='1760952360'
  UNION ALL
  SELECT 'SVC', RNDRNG_PRVDR_LAST_ORG_NAME, NULL, NULL, NULL, HCPCS_CD, HCPCS_DESC, PLACE_OF_SRVC, TOT_BENES, TOT_SRVCS,
         EST_MDCR_PYMT_AMT, AVG_MDCR_PYMT_AMT, NULL, NULL
  FROM {PBS} WHERE RNDRNG_NPI='1760952360'"""),
 ("q16_nppeer", "Peer group: every nurse practitioner in Part B 2024. National and Nevada medians, count over $1M/$5M, and the top 60 plus 1760952360 with current enrollment (PECOS), order/refer, pending-list and OIG-exclusion flags",
  f"""WITH np AS (SELECT RNDRNG_NPI npi, RNDRNG_PRVDR_LAST_ORG_NAME nm, RNDRNG_PRVDR_STATE_ABRVTN st, TRY_TO_DOUBLE(TOT_BENES) benes,
                     TOT_MDCR_PYMT_AMT pay, DRUG_MDCR_PYMT_AMT drug_pay
              FROM {PB} WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'),
  stats AS (SELECT COUNT(*) n_np, MEDIAN(pay) med_pay, PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY pay) p99_pay,
                   COUNT_IF(pay > 1e6) n_over_1m, COUNT_IF(pay > 5e6) n_over_5m, MEDIAN(pay / NULLIF(benes,0)) med_per_bene FROM np),
  nv AS (SELECT COUNT(*) n_nv, MEDIAN(pay) med_nv, COUNT_IF(pay > 1e6) nv_over_1m FROM np WHERE st='NV'),
  top AS (SELECT np.*, RANK() OVER (ORDER BY pay DESC) rk, RANK() OVER (PARTITION BY st ORDER BY pay DESC) rk_state FROM np
          QUALIFY rk <= 60 OR npi='1760952360'),
  pec AS (SELECT DISTINCT NPI FROM {M}HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT WHERE NPI IN (SELECT npi FROM top)),
  orf AS (SELECT DISTINCT NPI FROM {M}HEALTH__FED_CMS_ORDER_AND_REFERRING WHERE NPI IN (SELECT npi FROM top)),
  pen AS (SELECT NPI FROM {M}HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
          UNION SELECT NPI FROM {M}HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
  lei AS (SELECT NPI, MIN(EXCLUSION_DATE) excl_date FROM {M}HEALTH__FED_HHS_OIG_LEIE WHERE NPI IN (SELECT npi FROM top) GROUP BY 1)
  SELECT top.*, stats.*, nv.*, IFF(pec.NPI IS NULL, 0, 1) in_pecos, IFF(orf.NPI IS NULL, 0, 1) in_orf,
         IFF(top.npi IN (SELECT NPI FROM pen), 1, 0) pending, lei.excl_date
  FROM top CROSS JOIN stats CROSS JOIN nv LEFT JOIN pec ON pec.NPI=top.npi LEFT JOIN orf ON orf.NPI=top.npi LEFT JOIN lei ON lei.NPI=top.npi
  ORDER BY top.rk"""),
 ("q17_skinsub", "Top 60 NPs plus 1760952360: share of surviving service-line payment on skin-substitute codes (Q41xx-Q43xx, A20xx) vs all lines",
  f"""SELECT RNDRNG_NPI, SUM(EST_MDCR_PYMT_AMT) svc_pay,
         SUM(IFF(HCPCS_CD LIKE 'Q41%' OR HCPCS_CD LIKE 'Q42%' OR HCPCS_CD LIKE 'Q43%' OR HCPCS_CD LIKE 'A20%', EST_MDCR_PYMT_AMT, 0)) skin_pay,
         MAX(IFF(HCPCS_CD LIKE 'Q41%' OR HCPCS_CD LIKE 'Q42%' OR HCPCS_CD LIKE 'Q43%' OR HCPCS_CD LIKE 'A20%', HCPCS_DESC, NULL)) a_skin_desc,
         LISTAGG(DISTINCT PLACE_OF_SRVC, ',') pos
  FROM {PBS} WHERE RNDRNG_NPI IN ({TOPNP}) OR RNDRNG_NPI='1760952360' GROUP BY 1"""),
]
