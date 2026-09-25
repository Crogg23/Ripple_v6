-- [t1_approx_topk_vs_exact]
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
select * from x

-- [e2_eurostat_outliers_and_gap]
with s as (select geo, time, split_part(split_part(raw_xml_series_key, 'sex=', 2), ';', 1) sex, try_to_double(obs_value) v
  from LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EUROSTAT where dataflow_id = 'TESPN070'),
o as (select 'outlier' k, geo, time, sex, v, null::float f, null::float m from s where v > 1.2 or v < 0.1),
g as (select 'gap2023' k, geo, time, 'F/M' sex, null::float v,
    max(iff(sex='F', v, null)) f, max(iff(sex='M', v, null)) m
  from s where time = '2023' group by geo, time)
select * from o
union all select * from g
order by k, (f - m) nulls last

-- [h3_hifld_status_by_year]
select year(source_date) yr, count(*) n, sum(iff(status = 'IN SERVICE',1,0)) in_service, sum(iff(status = 'NOT AVAILABLE',1,0)) not_avail,
  count(distinct owner) owners
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_DHS_HIFLD group by 1 order by 1

-- [i3_itis_comment_contents]
select count(*) n,
  sum(iff(exp_comment ilike '%@%',1,0)) n_email,
  sum(iff(regexp_like(exp_comment, '.*\(?[0-9]{3}\)?[ .-][0-9]{3}[ .-][0-9]{4}.*', 's'),1,0)) n_phone,
  sum(iff(exp_comment ilike '%university%' or exp_comment ilike '%college%',1,0)) n_univ,
  sum(iff(exp_comment ilike '%museum%' or exp_comment ilike '%smithsonian%',1,0)) n_museum,
  sum(iff(exp_comment ilike '%usgs%' or exp_comment ilike '%geological survey%' or exp_comment ilike '%noaa%' or exp_comment ilike '%usda%' or exp_comment ilike '%fish and wildlife%',1,0)) n_fed,
  max(iff(exp_comment ilike '%@%', year(update_date), null)) newest_email_yr
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS
