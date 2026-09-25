-- g45 deep pass 3, 2026-09-24. Every statement run, in order. Python door (connect/db.py). Read-only.
-- Tables (all LIBRARY_MARTS.REFERENCE): REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP, REFERENCE__CALENDAR,
--   REFERENCE__FED_ITIS_JURISDICTION, REFERENCE__FED_ITIS_OTHER_SOURCES, REFERENCE__FED_ITIS_VERN_REF_LINKS.
-- Join tables read: REFERENCE__FED_ITIS_TAXONOMIC_UNITS, _VERNACULARS, _PUBLICATIONS, _EXPERTS, _KINGDOMS, _REFERENCE_LINKS.
-- Budget: 26 of 35 = 18 SELECTs + 8 session-setup statements (4 connections x 2).
-- Note: x1_join_cols returned 0 rows, cause not checked; join-table column names were taken from outputs/catalog/plain.json instead.

-- ===== connection: b0.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_cols] (1.0s)
select table_name, column_name, data_type
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'REFERENCE'
  and table_name in ('REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP','REFERENCE__CALENDAR','REFERENCE__FED_ITIS_JURISDICTION',
    'REFERENCE__FED_ITIS_OTHER_SOURCES','REFERENCE__FED_ITIS_VERN_REF_LINKS')
order by table_name, ordinal_position;

-- [q02_samples] (2.0s)
select 'AUTH' t, object_construct(*)::varchar o from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP limit 2)
union all select 'CAL', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__CALENDAR where date_day = '2025-10-01')
union all select 'JUR', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION limit 2)
union all select 'OSRC', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES limit 2)
union all select 'VREF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS limit 2);

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [a1_auth_profile] (0.7s)
select count(*) n, count(distinct taxon_author_id) ids, count(distinct taxon_author_id, kingdom_id) id_kingdom,
  count(distinct taxon_author) author_strings, count(distinct taxon_author, kingdom_id) author_kingdom,
  count(distinct _source_run_id) runs, count(distinct _src_sha256) shas, min(_loaded_at) first_load, max(_loaded_at) last_load,
  count_if(taxon_author is null or taxon_author = '') blank_author, count_if(short_author is null or short_author = '') blank_short,
  count_if(taxon_author_id = 0) id_zero, min(update_date) min_upd, max(update_date) max_upd,
  (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP group by taxon_author)) max_rows_one_author
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP;

-- [a2_auth_kingdom_top] (0.2s)
select 'kingdom' k, kingdom_id::varchar v, count(*) n from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP group by 1,2
union all
select * from (select 'top_author', taxon_author, count(*) n from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP group by 1,2 order by n desc limit 6)
order by 1, 3 desc;

-- [t1_itis_update_years] (0.6s)
select t, y, count(*) total, count_if(m <= 7) jan_jul from (
  select 'AUTH' t, year(update_date) y, month(update_date) m from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
  union all select 'JUR', year(update_date), month(update_date) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
  union all select 'VREF', year(update_date), month(update_date) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS
  union all select 'OSRC', year(update_date), month(update_date) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES)
where y >= 2012
group by 1,2 order by 1,2;

-- [c1_cal_checks] (0.4s)
with c as (
  select *, iff(mod(year_num,2)=1 and date_day < date_from_parts(year_num,1,3), year_num-1, year_num) adj_y
  from LIBRARY_MARTS.REFERENCE.REFERENCE__CALENDAR)
select count(*) n, count(distinct date_day) days, min(date_day) d0, max(date_day) d1,
  count_if(day_of_week_iso <> dayofweekiso(date_day)) bad_dow,
  count_if(iso_week <> weekiso(date_day)) bad_isoweek,
  count_if(iso_year <> yearofweekiso(date_day)) bad_isoyear,
  count_if(is_weekend <> (dayofweekiso(date_day) in (6,7))) bad_weekend,
  count_if(is_month_end <> (date_day = last_day(date_day))) bad_month_end,
  count_if(week_start <> date_trunc('week', date_day)) bad_week_start,
  count_if(federal_fiscal_year <> year_num + iff(month_num >= 10, 1, 0)) bad_fy_oct_rule,
  count_if(federal_fiscal_year is null) null_fy,
  count_if(election_cycle <> year_num + mod(year_num, 2)) bad_cycle,
  count_if(is_election_year <> (mod(year_num,2)=0)) bad_elect_flag,
  count_if(congress_number is null) null_congress,
  count_if(date_day >= '1935-01-03' and congress_number <> floor((adj_y - 1789)/2) + 1) bad_congress_post1935,
  count_if(date_day < '1789-03-04' and congress_number is not null) congress_before_1789,
  count_if(date_day between '1789-03-04' and '1935-01-02'
           and congress_number <> floor((iff(mod(year_num,2)=1 and date_day < date_from_parts(year_num,3,4), year_num-1, year_num) - 1789)/2) + 1) bad_congress_march4_era,
  count_if(date_day < '1976-10-01' and federal_fiscal_year <> year_num + iff(month_num >= 7, 1, 0) and date_day >= '1842-07-01') bad_fy_under_july_rule_1842_1976
from c;

-- [c2_cal_edges] (0.3s)
select date_day, day_name, federal_fiscal_year fy, federal_fiscal_quarter fq, election_cycle, is_election_year, congress_number, iso_year, iso_week, week_of_year
from LIBRARY_MARTS.REFERENCE.REFERENCE__CALENDAR
where date_day in ('1700-01-01','1776-07-04','1789-03-03','1789-03-04','1933-02-01','1933-03-04','1960-08-01',
  '1976-08-01','1976-10-01','2025-01-02','2025-01-03','2026-09-24','2027-01-01','2027-01-03','2125-12-31')
order by date_day;

-- [j1_jur_profile] (1.0s)
select count(*) n, count(distinct itis_jurisdiction_key) keys, count(distinct tsn, jurisdiction_value) tsn_place,
  count(distinct tsn) tsns, count(distinct jurisdiction_value) places, count(distinct origin) origins,
  count(distinct _source_run_id) runs, count_if(origin is null or origin = '') blank_origin,
  min(update_date) min_upd, max(update_date) max_upd
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION;

-- [j2_jur_place_origin] (1.9s)
select jurisdiction_value, origin, count(*) n
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
group by 1,2 order by 1, 3 desc;

-- [o1_osrc_profile] (0.4s)
select 'all' k, null v, count(*) n, count(distinct source_id) ids, count(distinct itis_other_sources_key) keys,
  count_if(source_comment = 'None') comment_none_text, count_if(source_comment is null or source_comment = '') comment_blank,
  count_if(version in ('undefined','None','')) version_junk, count_if(acquisition_date is null) acq_null,
  count_if(source_name like '(%') name_parens, count(distinct lower(source_type)) types_lower
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all
select 'type', source_type, count(*), null, null, null, null, null, null, null, null
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES group by 2
order by 1, 3 desc;

-- [v1_vref_profile] (0.4s)
select count(*) n, count(distinct itis_vern_ref_links_key) keys, count(distinct tsn, doc_id_prefix, documentation_id, vern_id) natural_keys,
  count(distinct vern_id) verns, count(distinct tsn) tsns, count(distinct _source_run_id) runs,
  count_if(update_date = '1900-01-01') upd_1900, count_if(update_date < '1996-01-01') upd_pre1996,
  count_if(doc_id_prefix = 'SRC') src, count_if(doc_id_prefix = 'PUB') pub, count_if(doc_id_prefix = 'EXP') exp,
  count_if(doc_id_prefix not in ('SRC','PUB','EXP') or doc_id_prefix is null) other_prefix
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS;

-- [x1_join_cols] (1.0s)
select table_name, column_name, data_type
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'REFERENCE'
  and table_name in ('REFERENCE__FED_ITIS_TAXONOMIC_UNITS','REFERENCE__FED_ITIS_VERNACULARS','REFERENCE__FED_ITIS_PUBLICATIONS','REFERENCE__FED_ITIS_EXPERTS')
  and column_name not like '\_%'
order by table_name, ordinal_position;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [k1_link_integrity] (2.2s)
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

-- [j3_place_valid_species] (0.6s)
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

-- [t2_monthly_intake] (1.2s)
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

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [j4_jur_kingdom] (0.5s)
select k.kingdom_name, upper(j.jurisdiction_value) place,
  count_if(t.name_usage in ('valid','accepted') and t.rank_id = 220) valid_species,
  count_if(t.name_usage in ('valid','accepted') and t.rank_id = 220 and j.origin = 'Introduced') introduced_species
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION j
join LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS t on t.tsn = j.tsn
left join LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_KINGDOMS k on k.kingdom_id = t.kingdom_id
group by 1,2 order by 2, 3 desc;

-- [n1_none_text] (0.2s)
select 'AUTH.TAXON_AUTHOR' col, count_if(taxon_author in ('None','nan','NULL','null')) n from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
union all select 'AUTH.SHORT_AUTHOR', count_if(short_author in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
union all select 'OSRC.SOURCE_COMMENT', count_if(source_comment in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all select 'OSRC.VERSION', count_if(version in ('None','nan','NULL','null','undefined')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all select 'OSRC.SOURCE_NAME', count_if(source_name in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all select 'JUR.ORIGIN', count_if(origin in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
union all select 'OSRC.comment_len_lt_5', count_if(length(source_comment) < 5) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES;

-- [v2_vref_orphans] (1.6s)
with v as (select distinct vern_id, tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERNACULARS),
  o as (select r.* from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS r
        left join v on v.vern_id = r.vern_id and v.tsn = r.tsn where v.vern_id is null)
select count(*) orphans,
  count_if(vern_id in (select vern_id from v)) vern_id_exists_on_other_tsn,
  count_if(tsn in (select tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS where name_usage in ('valid','accepted'))) orphan_on_valid_tsn,
  min(update_date) u0, max(update_date) u1,
  (select count(*) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS where update_date = '1900-01-01' and doc_id_prefix = 'PUB') upd1900_pub
from o;
