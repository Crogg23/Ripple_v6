-- S09 ITIS rank types: pull all 182 rows to confirm it is a rank lookup and check key, parent links and update dates
SELECT itis_taxon_unit_types_key, kingdom_id, rank_id, rank_name, dir_parent_rank_id, req_parent_rank_id, update_date,
       _source_run_id, _src_sha256, _loaded_at::string loaded_txt
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_UNIT_TYPES
ORDER BY kingdom_id, rank_id
