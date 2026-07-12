-- Rollback for dedup_irs_eo_bmf (20260712_114615) -- restores the pre-retirement state.
-- INGEST_RUNS rows before demote: [('5e1fc4a8-d362-434a-a72f-a4fc212f39ca', 'success', 3949660, 'Chunked load: streamed 3,949,660 rows in batches of 50,000 -> LIBRARY_RAW.LANDING.FED_IRS_EO_BMF (table now 3,949,660 rows). Manifest sha a5fdae0177cb. density=93.31% (source_cols=28, all_blank_cols=0, rows_sampled=2000).')]
-- SOURCE_REGISTRY INCLUDE before: Y

-- 1. move the table back into LANDING
ALTER TABLE LIBRARY_RAW.RETIRED.FED_IRS_EO_BMF RENAME TO LIBRARY_RAW.LANDING.FED_IRS_EO_BMF;

-- 2. restore the ingest run to success (row count 3,949,660)
UPDATE LIBRARY_META.INGEST_LOGS.INGEST_RUNS SET STATUS='success', ROW_COUNT=3949660
  WHERE SOURCE_ID='fed_irs_eo_bmf' AND STATUS='empty';

-- 3. restore the registry include flag
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY SET INCLUDE='Y' WHERE SOURCE_ID='fed_irs_eo_bmf';
--    (NOTES was appended to; trim the [RETIRED ...] suffix by hand if desired)

-- 4. restore the 140 CONNECT edges from the backup table
INSERT INTO LIBRARY_META."CONNECT".CONNECT_EDGES SELECT * FROM LIBRARY_META."CONNECT".ZZ_RETIRED_EDGES_FED_IRS_EO_BMF;
