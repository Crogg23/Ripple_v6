-- [k1_link_integrity]
with vr as (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS),
  tu as (select distinct tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS),
  tua as (select distinct taxon_author_id from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS where taxon_author_id is not null and taxon_author_id <> 0),
  v as (select distinct vern_id, tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERNACULARS),
  os as (select distinct source_id from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES),
  pb as (select distinct publication_id from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_PUBLICATIONS),
  ex as (select distinct expert_id from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS),
  au as (select distinct taxon_author_id from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP),
  jr as (select distinct tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION),
  rl as (select distinct documentation_id from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS where trim(doc_id_prefix) = 'SRC')
select
  (select count(*) from vr where tsn not in (select tsn from tu)) vref_tsn_missing,
  (select count(*) from vr where (vern_id, tsn) not in (select vern_id, tsn from v)) vref_vern_tsn_missing,
  (select count(*) from vr where doc_id_prefix = 'SRC' and documentation_id not in (select source_id from os)) vref_src_missing,
  (select count(*) from vr where doc_id_prefix = 'PUB' and documentation_id not in (select publication_id from pb)) vref_pub_missing,
  (select count(*) from vr where doc_id_prefix = 'EXP' and documentation_id not in (select expert_id from ex)) vref_exp_missing,
  (select count(*) from jr where tsn not in (select tsn from tu)) jur_tsn_missing,
  (select count(*) from au) authors, (select count(*) from au where taxon_author_id not in (select taxon_author_id from tua)) authors_never_used,
  (select count(*) from tua where taxon_author_id not in (select taxon_author_id from au)) tu_author_ids_missing,
  (select count(*) from os) sources,
  (select count(*) from os where source_id not in (select documentation_id from rl)
     and source_id not in (select documentation_id from vr where doc_id_prefix = 'SRC')) sources_never_cited;
-- [j3_place_valid_species]
with j as (
  select j.jurisdiction_value place, j.origin, t.name_usage, t.rank_id
  from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION j
  join LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS t on t.tsn = j.tsn)
select upper(place) place, count(*) rows_all,
  count_if(name_usage not in ('valid','accepted')) rows_on_unaccepted_names,
  count_if(name_usage in ('valid','accepted') and rank_id = 220) valid_species,
  count_if(name_usage in ('valid','accepted') and rank_id = 220 and origin = 'Introduced') introduced_species,
  round(100 * introduced_species / nullif(valid_species, 0), 1) pct_introduced
from j group by 1 order by pct_introduced desc;
-- [t2_monthly_intake]
with a as (select date_trunc('month', update_date) m, update_date d from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
           where update_date >= '2019-01-01'),
  am as (select m, count(*) auth_rows, count(distinct d) auth_days from a group by 1),
  ad as (select m, max(c) auth_top_day from (select m, d, count(*) c from a group by 1,2) group by 1),
  t as (select try_to_timestamp(initial_time_stamp::varchar)::date d from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS),
  tm as (select date_trunc('month', d) m, count(*) new_tsns, count(distinct d) tsn_days from t where d >= '2019-01-01' group by 1),
  td as (select m, max(c) tsn_top_day from (select date_trunc('month', d) m, d, count(*) c from t where d >= '2019-01-01' group by 1,2) group by 1)
select coalesce(am.m, tm.m) month, auth_rows, auth_days, auth_top_day, new_tsns, tsn_days, tsn_top_day
from am full outer join tm on tm.m = am.m left join ad on ad.m = am.m left join td on td.m = tm.m
order by 1;
