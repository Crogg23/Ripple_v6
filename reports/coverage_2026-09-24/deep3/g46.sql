-- g46 deep pass 3, 2026-09-24. Every statement run, in order. Python door (connect/db.py). Read-only.
-- Tables: REFERENCE__INTL_GDELT, REFERENCE__FED_DHS_HIFLD, REFERENCE__INTL_EUROSTAT,
--   REFERENCE__XC_CROSSREF_FUNDER_REGISTRY, REFERENCE__FED_ITIS_EXPERTS (all LIBRARY_MARTS.REFERENCE).
-- Also read, for the glance-method check (t2): FINANCE__FED_SEC_INSIDER_DERIV_TRANS, ECONOMICS__FED_IRS_FATCA_FFI_LIST,
--   HEALTH__FED_FDA_GUDID, HEALTH__FED_CDC_OVERDOSE.
-- Budget: 23 of 35 = 17 SELECTs (one errored on a regex and was rerun) + 6 session-setup statements (3 connections x 2).

-- ===== connection: b0.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_tables] (7.1s)
select t.table_catalog, t.table_schema, t.table_name, t.row_count, t.last_altered,
  listagg(c.column_name || ':' || c.data_type, ', ') within group (order by c.ordinal_position) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t
join LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
  on c.table_schema = t.table_schema and c.table_name = t.table_name
where t.table_name in ('REFERENCE__INTL_GDELT','REFERENCE__FED_DHS_HIFLD','REFERENCE__INTL_EUROSTAT',
  'REFERENCE__XC_CROSSREF_FUNDER_REGISTRY','REFERENCE__FED_ITIS_EXPERTS')
group by 1,2,3,4,5;

-- [q02_samples] (1.8s)
select 'GDELT' t, object_construct(*)::varchar o from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT limit 1)
union all select 'HIFLD', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD limit 2)
union all select 'EURO', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EUROSTAT limit 2)
union all select 'XREF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY where replaced_by_uri is not null limit 1)
union all select 'XREF2', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY limit 1)
union all select 'ITIS', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS limit 2);

-- [g1_gdelt_shape] (0.3s)
select count(*) n_rows, count(distinct globaleventid) n_event_ids, count(distinct hash(*)) n_distinct_rows,
  count(distinct extra_col_19) n_dateadded, min(extra_col_19) min_added, max(extra_col_19) max_added,
  count(distinct extra_col_20) n_urls, min(sqldate) min_sqldate, max(sqldate) max_sqldate,
  sum(iff(sqldate = '20260702',1,0)) n_jul2,
  count(distinct extra_col_13) n_action_countries,
  sum(iff(extra_col_16 is null or extra_col_16 = '',1,0)) n_no_action_lat
from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT;

-- [g2_gdelt_eventid_repeats] (0.4s)
with e as (select globaleventid, count(*) n, count(distinct hash(*)) h, count(distinct extra_col_20) u
  from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT group by 1)
select n rows_per_id, count(*) ids, sum(iff(h = 1,1,0)) ids_all_rows_identical, max(u) max_urls_per_id
from e group by 1 order by 1;

-- [h1_hifld_shape] (0.3s)
select count(*) n_rows, count(distinct objectid) n_objectid,
  count(distinct hash(objectid, name, address, city, state, zip, county, fips, latitude, longitude, naics_code, layer_name, status, owner, source_date)) n_distinct_content,
  count(distinct _source_run_id) n_runs, count(distinct _ingested_at) n_ingest_ts, min(_ingested_at) first_ing, max(_ingested_at) last_ing,
  min(source_date) min_src, max(source_date) max_src, count(distinct owner) n_owners, count(distinct state) n_states,
  sum(iff(latitude is null,1,0)) n_null_lat,
  sum(iff(name is null or name in ('','NOT AVAILABLE'),1,0)) n_name_blank_na,
  sum(iff(address is null or address in ('','NOT AVAILABLE'),1,0)) n_addr_blank_na,
  sum(iff(naics_code is null or naics_code in ('','NOT AVAILABLE'),1,0)) n_naics_blank_na,
  min(objectid::number) min_oid, max(objectid::number) max_oid
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD;

-- [h2_hifld_status_owner] (0.3s)
select status, owner, count(distinct objectid) lines, count(*) n_rows, min(source_date) min_src, max(source_date) max_src
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD group by 1,2 order by lines desc limit 25;

-- [e1_eurostat_shape] (0.4s)
select dataflow_id, unit, freq, count(*) n, count(distinct geo) n_geo, min(time) min_t, max(time) max_t,
  count(distinct geo||'|'||time) n_geo_time, count(distinct raw_xml_series_key) n_series,
  listagg(distinct obs_status, ',') statuses, sum(iff(obs_status is not null and obs_status <> '',1,0)) n_flagged,
  min(try_to_double(obs_value)) min_v, max(try_to_double(obs_value)) max_v, sum(iff(try_to_double(obs_value) is null,1,0)) n_nonnum,
  any_value(raw_xml_series_key) ex_key, count(distinct indicator) n_ind
from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EUROSTAT group by 1,2,3 order by n desc;

-- [x1_crossref_shape] (0.3s)
select count(*) n_rows, count(distinct funder_uri) n_uri, count(distinct upper(trim(funder_name))) n_names,
  sum(iff(funder_uri not like 'http://dx.doi.org/10.13039/%',1,0)) n_bad_uri,
  count(distinct replaced_by_uri) n_replaced_vals, sum(iff(replaced_by_uri is not null and replaced_by_uri <> '',1,0)) n_replaced,
  listagg(distinct left(replaced_by_uri,10), ',') replaced_vals,
  count(distinct _source_run_id) n_runs, min(_loaded_at) first_load, max(_loaded_at) last_load,
  sum(iff(funder_name is null or funder_name = '',1,0)) n_blank_name
from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY;

-- [x2_crossref_dup_names] (0.3s)
select upper(trim(funder_name)) nm, count(*) n, count(distinct funder_uri) n_uri,
  listagg(funder_uri, ' ; ') within group (order by funder_uri) uris,
  sum(iff(replaced_by_uri is not null and replaced_by_uri <> '',1,0)) n_replaced
from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY
group by 1 having count(*) > 1 order by n desc limit 15;

-- [i1_itis_shape] (0.3s)
select count(*) n_rows, count(distinct expert_id) n_ids, count(distinct upper(trim(expert))) n_names,
  count(distinct expert_id_prefix) n_prefix, min(update_date) min_upd, max(update_date) max_upd,
  sum(iff(exp_comment is null or exp_comment in ('','None'),1,0)) n_no_comment,
  count(distinct _source_run_id) n_runs,
  sum(iff(year(update_date) >= 2020,1,0)) n_upd_2020_plus
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS;

-- [i2_itis_dups_and_years] (0.3s)
select 'dup' k, upper(trim(expert)) v, count(*) n, listagg(expert_id || ' @' || update_date || ': ' || left(coalesce(exp_comment,''),60), ' || ') detail
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS group by 1,2 having count(*) > 1
union all
select 'year', year(update_date)::varchar, count(*), null
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS group by 1,2
order by 1, 2;

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [t1_approx_topk_vs_exact] (0.8s)
with x as (select 'XREF FUNDER_URI' col, approx_top_k(funder_uri, 3)::varchar approx_top3,
    (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY group by funder_uri)) exact_max
  from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY
  union all select 'XREF FUNDER_NAME', approx_top_k(funder_name, 3)::varchar,
    (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY group by funder_name))
  from LIBRARY_MARTS.REFERENCE.REFERENCE__XC_CROSSREF_FUNDER_REGISTRY
  union all select 'GDELT GLOBALEVENTID', approx_top_k(globaleventid, 3)::varchar,
    (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT group by globaleventid))
  from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_GDELT
  union all select 'HIFLD OBJECTID', approx_top_k(objectid, 3)::varchar,
    (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD group by objectid))
  from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD
  union all select 'ITIS EXPERT', approx_top_k(expert, 3)::varchar,
    (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS group by expert))
  from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS)
select * from x;

-- [e2_eurostat_outliers_and_gap] (0.3s)
with s as (select geo, time, split_part(split_part(raw_xml_series_key, 'sex=', 2), ';', 1) sex, try_to_double(obs_value) v
  from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EUROSTAT where dataflow_id = 'TESPN070'),
o as (select 'outlier' k, geo, time, sex, v, null::float f, null::float m from s where v > 1.2 or v < 0.1),
g as (select 'gap2023' k, geo, time, 'F/M' sex, null::float v,
    max(iff(sex='F', v, null)) f, max(iff(sex='M', v, null)) m
  from s where time = '2023' group by geo, time)
select * from o
union all select * from g
order by k, (f - m) nulls last;

-- [h3_hifld_status_by_year] (0.3s)
select year(source_date) yr, count(*) n, sum(iff(status = 'IN SERVICE',1,0)) in_service, sum(iff(status = 'NOT AVAILABLE',1,0)) not_avail,
  count(distinct owner) owners
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD group by 1 order by 1;

-- [i3_itis_comment_contents] (0.2s, ERROR)
select count(*) n,
  sum(iff(exp_comment ilike '%@%',1,0)) n_email,
  sum(iff(regexp_like(exp_comment, '.*\(?[0-9]{3}\)?[ .-][0-9]{3}[ .-][0-9]{4}.*', 's'),1,0)) n_phone,
  sum(iff(exp_comment ilike '%university%' or exp_comment ilike '%college%',1,0)) n_univ,
  sum(iff(exp_comment ilike '%museum%' or exp_comment ilike '%smithsonian%',1,0)) n_museum,
  sum(iff(exp_comment ilike '%usgs%' or exp_comment ilike '%geological survey%' or exp_comment ilike '%noaa%' or exp_comment ilike '%usda%' or exp_comment ilike '%fish and wildlife%',1,0)) n_fed,
  max(iff(exp_comment ilike '%@%', year(update_date), null)) newest_email_yr
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [i3_itis_comment_contents] (0.3s)
select count(*) n,
  sum(iff(exp_comment ilike '%@%',1,0)) n_email,
  sum(iff(regexp_like(exp_comment, '.*[0-9]{3}[) .-]+[0-9]{3}[ .-][0-9]{4}.*', 's'),1,0)) n_phone,
  sum(iff(exp_comment ilike '%univ%' or exp_comment ilike '%college%',1,0)) n_univ,
  sum(iff(exp_comment ilike '%museum%' or exp_comment ilike '%smithsonian%',1,0)) n_museum,
  sum(iff(exp_comment ilike '%usgs%' or exp_comment ilike '%geological survey%' or exp_comment ilike '%noaa%' or exp_comment ilike '%usda%' or exp_comment ilike '%fish and wildlife%' or exp_comment ilike '%national marine fisheries%',1,0)) n_fed,
  max(iff(exp_comment ilike '%@%', year(update_date), null)) newest_email_yr,
  min(iff(exp_comment ilike '%@%', year(update_date), null)) oldest_email_yr
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS;

-- [t2_battery_flat_topk_exact_check] (2.3s)
select 'SEC DERIV_TRANS_SK (battery top 2,102)' col, count(*) n_rows, count(distinct v) n_distinct, max(c) exact_max
  from (select deriv_trans_sk v, count(*) over (partition by deriv_trans_sk) c from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS)
union all select 'FATCA GIIN (battery top 3,797)', count(*), count(distinct v), max(c)
  from (select giin v, count(*) over (partition by giin) c from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_FATCA_FFI_LIST)
union all select 'GUDID PRIMARY_DI (battery top 4,909)', count(*), count(distinct v), max(c)
  from (select primary_di v, count(*) over (partition by primary_di) c from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID)
union all select 'control: CDC_OVERDOSE STATE (battery top 1,596)', count(*), count(distinct v), max(c)
  from (select state v, count(*) over (partition by state) c from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_OVERDOSE);
