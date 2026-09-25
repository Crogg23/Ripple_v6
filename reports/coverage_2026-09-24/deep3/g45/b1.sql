-- [a1_auth_profile]
select count(*) n, count(distinct taxon_author_id) ids, count(distinct taxon_author_id, kingdom_id) id_kingdom,
  count(distinct taxon_author) author_strings, count(distinct taxon_author, kingdom_id) author_kingdom,
  count(distinct _source_run_id) runs, count(distinct _src_sha256) shas, min(_loaded_at) first_load, max(_loaded_at) last_load,
  count_if(taxon_author is null or taxon_author = '') blank_author, count_if(short_author is null or short_author = '') blank_short,
  count_if(taxon_author_id = 0) id_zero, min(update_date) min_upd, max(update_date) max_upd,
  (select max(c) from (select count(*) c from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP group by taxon_author)) max_rows_one_author
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP;
-- [a2_auth_kingdom_top]
select 'kingdom' k, kingdom_id::varchar v, count(*) n from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP group by 1,2
union all
select * from (select 'top_author', taxon_author, count(*) n from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP group by 1,2 order by n desc limit 6)
order by 1, 3 desc;
-- [t1_itis_update_years]
select t, y, count(*) total, count_if(m <= 7) jan_jul from (
  select 'AUTH' t, year(update_date) y, month(update_date) m from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
  union all select 'JUR', year(update_date), month(update_date) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
  union all select 'VREF', year(update_date), month(update_date) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS
  union all select 'OSRC', year(update_date), month(update_date) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES)
where y >= 2012
group by 1,2 order by 1,2;
-- [c1_cal_checks]
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
-- [c2_cal_edges]
select date_day, day_name, federal_fiscal_year fy, federal_fiscal_quarter fq, election_cycle, is_election_year, congress_number, iso_year, iso_week, week_of_year
from LIBRARY_MARTS.REFERENCE.REFERENCE__CALENDAR
where date_day in ('1700-01-01','1776-07-04','1789-03-03','1789-03-04','1933-02-01','1933-03-04','1960-08-01',
  '1976-08-01','1976-10-01','2025-01-02','2025-01-03','2026-09-24','2027-01-01','2027-01-03','2125-12-31')
order by date_day;
-- [j1_jur_profile]
select count(*) n, count(distinct itis_jurisdiction_key) keys, count(distinct tsn, jurisdiction_value) tsn_place,
  count(distinct tsn) tsns, count(distinct jurisdiction_value) places, count(distinct origin) origins,
  count(distinct _source_run_id) runs, count_if(origin is null or origin = '') blank_origin,
  min(update_date) min_upd, max(update_date) max_upd
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION;
-- [j2_jur_place_origin]
select jurisdiction_value, origin, count(*) n
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
group by 1,2 order by 1, 3 desc;
-- [o1_osrc_profile]
select 'all' k, null v, count(*) n, count(distinct source_id) ids, count(distinct itis_other_sources_key) keys,
  count_if(source_comment = 'None') comment_none_text, count_if(source_comment is null or source_comment = '') comment_blank,
  count_if(version in ('undefined','None','')) version_junk, count_if(acquisition_date is null) acq_null,
  count_if(source_name like '(%') name_parens, count(distinct lower(source_type)) types_lower
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all
select 'type', source_type, count(*), null, null, null, null, null, null, null, null
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES group by 2
order by 1, 3 desc;
-- [v1_vref_profile]
select count(*) n, count(distinct itis_vern_ref_links_key) keys, count(distinct tsn, doc_id_prefix, documentation_id, vern_id) natural_keys,
  count(distinct vern_id) verns, count(distinct tsn) tsns, count(distinct _source_run_id) runs,
  count_if(update_date = '1900-01-01') upd_1900, count_if(update_date < '1996-01-01') upd_pre1996,
  count_if(doc_id_prefix = 'SRC') src, count_if(doc_id_prefix = 'PUB') pub, count_if(doc_id_prefix = 'EXP') exp,
  count_if(doc_id_prefix not in ('SRC','PUB','EXP') or doc_id_prefix is null) other_prefix
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS;
-- [x1_join_cols]
select table_name, column_name, data_type
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'REFERENCE'
  and table_name in ('REFERENCE__FED_ITIS_TAXONOMIC_UNITS','REFERENCE__FED_ITIS_VERNACULARS','REFERENCE__FED_ITIS_PUBLICATIONS','REFERENCE__FED_ITIS_EXPERTS')
  and column_name not like '\_%'
order by table_name, ordinal_position;
