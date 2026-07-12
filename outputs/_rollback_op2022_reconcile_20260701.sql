-- Rollback for fed_cms_open_payments_2022 reconciliation (2026-07-01)
-- INGEST_RUNS rows before the UPDATE:
--   ('bff7f164b2d74015', 'error', 0, 'PY2022 load failed: ValueError: I/O operation on closed file')
--   ('60f19a4a53054596', 'error', 0, 'PY2022 load failed: ValueError: I/O operation on closed file')
UPDATE LIBRARY_META.INGEST_LOGS.INGEST_RUNS SET STATUS='error', ROW_COUNT=0,
  MESSAGE='PY2022 load failed: ValueError: I/O operation on closed file.'
  WHERE SOURCE_ID='fed_cms_open_payments_2022' AND RUN_ID='60f19a4a53054596';
-- To un-register:
-- DELETE FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE SOURCE_ID='fed_cms_open_payments_2022';
