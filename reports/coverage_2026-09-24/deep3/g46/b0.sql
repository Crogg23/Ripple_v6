-- [q01_tables]
select t.table_catalog, t.table_schema, t.table_name, t.row_count, t.last_altered,
  listagg(c.column_name || ':' || c.data_type, ', ') within group (order by c.ordinal_position) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t
join LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
  on c.table_schema = t.table_schema and c.table_name = t.table_name
where t.table_name in ('REFERENCE__INTL_GDELT','REFERENCE__FED_DHS_HIFLD','REFERENCE__INTL_EUROSTAT',
  'REFERENCE__XC_CROSSREF_FUNDER_REGISTRY','REFERENCE__FED_ITIS_EXPERTS')
group by 1,2,3,4,5

-- [q02_samples]
select 'GDELT' t, object_construct(*)::varchar o from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT limit 1)
union all select 'HIFLD', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD limit 2)
union all select 'EURO', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EUROSTAT limit 2)
union all select 'XREF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY where replaced_by_uri is not null limit 1)
union all select 'XREF2', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY limit 1)
union all select 'ITIS', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS limit 2)

-- [g1_gdelt_shape]
select count(*) n_rows, count(distinct globaleventid) n_event_ids, count(distinct hash(*)) n_distinct_rows,
  count(distinct extra_col_19) n_dateadded, min(extra_col_19) min_added, max(extra_col_19) max_added,
  count(distinct extra_col_20) n_urls, min(sqldate) min_sqldate, max(sqldate) max_sqldate,
  sum(iff(sqldate = '20260702',1,0)) n_jul2,
  count(distinct extra_col_13) n_action_countries,
  sum(iff(extra_col_16 is null or extra_col_16 = '',1,0)) n_no_action_lat
from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT

-- [g2_gdelt_eventid_repeats]
with e as (select globaleventid, count(*) n, count(distinct hash(*)) h, count(distinct extra_col_20) u
  from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT group by 1)
select n rows_per_id, count(*) ids, sum(iff(h = 1,1,0)) ids_all_rows_identical, max(u) max_urls_per_id
from e group by 1 order by 1

-- [h1_hifld_shape]
select count(*) n_rows, count(distinct objectid) n_objectid,
  count(distinct hash(objectid, name, address, city, state, zip, county, fips, latitude, longitude, naics_code, layer_name, status, owner, source_date)) n_distinct_content,
  count(distinct _source_run_id) n_runs, count(distinct _ingested_at) n_ingest_ts, min(_ingested_at) first_ing, max(_ingested_at) last_ing,
  min(source_date) min_src, max(source_date) max_src, count(distinct owner) n_owners, count(distinct state) n_states,
  sum(iff(latitude is null,1,0)) n_null_lat,
  sum(iff(name is null or name in ('','NOT AVAILABLE'),1,0)) n_name_blank_na,
  sum(iff(address is null or address in ('','NOT AVAILABLE'),1,0)) n_addr_blank_na,
  sum(iff(naics_code is null or naics_code in ('','NOT AVAILABLE'),1,0)) n_naics_blank_na,
  min(objectid::number) min_oid, max(objectid::number) max_oid
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD

-- [h2_hifld_status_owner]
select status, owner, count(distinct objectid) lines, count(*) n_rows, min(source_date) min_src, max(source_date) max_src
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD group by 1,2 order by lines desc limit 25

-- [e1_eurostat_shape]
select dataflow_id, unit, freq, count(*) n, count(distinct geo) n_geo, min(time) min_t, max(time) max_t,
  count(distinct geo||'|'||time) n_geo_time, count(distinct raw_xml_series_key) n_series,
  listagg(distinct obs_status, ',') statuses, sum(iff(obs_status is not null and obs_status <> '',1,0)) n_flagged,
  min(try_to_double(obs_value)) min_v, max(try_to_double(obs_value)) max_v, sum(iff(try_to_double(obs_value) is null,1,0)) n_nonnum,
  any_value(raw_xml_series_key) ex_key, count(distinct indicator) n_ind
from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EUROSTAT group by 1,2,3 order by n desc

-- [x1_crossref_shape]
select count(*) n_rows, count(distinct funder_uri) n_uri, count(distinct upper(trim(funder_name))) n_names,
  sum(iff(funder_uri not like 'http://dx.doi.org/10.13039/%',1,0)) n_bad_uri,
  count(distinct replaced_by_uri) n_replaced_vals, sum(iff(replaced_by_uri is not null and replaced_by_uri <> '',1,0)) n_replaced,
  listagg(distinct left(replaced_by_uri,10), ',') replaced_vals,
  count(distinct _source_run_id) n_runs, min(_loaded_at) first_load, max(_loaded_at) last_load,
  sum(iff(funder_name is null or funder_name = '',1,0)) n_blank_name
from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY

-- [x2_crossref_dup_names]
select upper(trim(funder_name)) nm, count(*) n, count(distinct funder_uri) n_uri,
  listagg(funder_uri, ' ; ') within group (order by funder_uri) uris,
  sum(iff(replaced_by_uri is not null and replaced_by_uri <> '',1,0)) n_replaced
from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY
group by 1 having count(*) > 1 order by n desc limit 15

-- [i1_itis_shape]
select count(*) n_rows, count(distinct expert_id) n_ids, count(distinct upper(trim(expert))) n_names,
  count(distinct expert_id_prefix) n_prefix, min(update_date) min_upd, max(update_date) max_upd,
  sum(iff(exp_comment is null or exp_comment in ('','None'),1,0)) n_no_comment,
  count(distinct _source_run_id) n_runs,
  sum(iff(year(update_date) >= 2020,1,0)) n_upd_2020_plus
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS

-- [i2_itis_dups_and_years]
select 'dup' k, upper(trim(expert)) v, count(*) n, listagg(expert_id || ' @' || update_date || ': ' || left(coalesce(exp_comment,''),60), ' || ') detail
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS group by 1,2 having count(*) > 1
union all
select 'year', year(update_date)::varchar, count(*), null
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS group by 1,2
order by 1, 2
