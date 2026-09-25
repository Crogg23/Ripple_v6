M = "LIBRARY_MARTS.HEALTH."
QUERIES = [
 ("q01_mdpp", "MDPP: whole table (1,037 rows), analysed locally", f"SELECT * FROM {M}HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM"),
 ("q02_ihs", "IHS facilities: whole table (1,006 rows), analysed locally", f"SELECT * FROM {M}HEALTH__FED_IHS_FACILITIES"),
 ("q03_cmsmain", "CMS dataset catalog: whole table (158 rows), lookup check", f"SELECT * FROM {M}HEALTH__FED_CMS_MAIN"),
 ("q04_vaapp", "VA suicide appendix: whole table (144 raw spreadsheet rows)", f"SELECT * FROM {M}HEALTH__FED_VA_SUICIDE_APPENDIX"),
 ("q05_pending", "Pending initial enrollment, non-physicians: whole table (6,880 rows)", f"SELECT * FROM {M}HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS"),
 ("q06_vanat", "VA suicide national (typed sibling, 690 rows): duplicate check and non-veteran peer", f"SELECT * FROM {M}HEALTH__FED_VA_SUICIDE_NATIONAL"),
 ("q07_landing", "When each source landed: landing table created / last altered / row count",
  """SELECT table_name, row_count, created, last_altered FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
     WHERE table_schema='LANDING' AND (table_name ILIKE '%PENDING_INITIAL%' OR table_name ILIKE '%DIABETES_PREVENTION%'
       OR table_name ILIKE '%IHS%' OR table_name = 'FED_CMS_MAIN' OR table_name ILIKE '%VA_SUICIDE%') ORDER BY 1"""),
]
