-- S01 GUDID shape: duplicate check on the device barcode, load runs, status, dates
SELECT COUNT(*) n, COUNT(DISTINCT primary_di) dis, COUNT(DISTINCT public_device_record_key) keys,
       COUNT(DISTINCT primary_di, public_version_date) di_ver, COUNT(DISTINCT _source_run_id) runs,
       COUNT(DISTINCT labeler_duns_number) duns, COUNT(DISTINCT company_name) cos,
       MIN(publish_date) p0, MAX(publish_date) p1, MIN(public_version_date) v0, MAX(public_version_date) v1,
       COUNT_IF(primary_di IS NULL OR primary_di='') di_blank,
       ARRAY_AGG(DISTINCT record_status) rs, ARRAY_AGG(DISTINCT commercial_distribution_status) cds,
       ARRAY_AGG(DISTINCT is_kit) kit, ARRAY_AGG(DISTINCT is_combination_product) combo,
       SYSTEM$TYPEOF(MAX(publish_date)) ptype, SYSTEM$TYPEOF(MAX(_ingested_at)) itype,
       COUNT(DISTINCT _ingested_at) ingest_stamps
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID
