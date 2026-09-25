M = "LIBRARY_MARTS.HEALTH."
QUERIES = [
 ("q21_posbeds", "Bed counts for every Care Compare hospital from the Provider of Services file, joined on CCN, to size-match the IHS hospital peer group",
  f"""SELECT p.CCN, p.PRVDR_CTGRY_CD, p.PRVDR_CTGRY_SBTYP_CD, p.STATE_CD, p.BED_CNT, p.CRTFD_BED_CNT, p.GNRL_CNTL_TYPE_CD
  FROM {M}HEALTH__FED_CMS_POS_OTHER p WHERE p.CCN IN (SELECT CCN FROM {M}HEALTH__FED_CMS_HOSPITAL_GENERAL)"""),
]
