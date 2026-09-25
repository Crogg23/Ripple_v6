-- [j4_jur_kingdom]
select k.kingdom_name, upper(j.jurisdiction_value) place,
  count_if(t.name_usage in ('valid','accepted') and t.rank_id = 220) valid_species,
  count_if(t.name_usage in ('valid','accepted') and t.rank_id = 220 and j.origin = 'Introduced') introduced_species
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION j
join LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS t on t.tsn = j.tsn
left join LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_KINGDOMS k on k.kingdom_id = t.kingdom_id
group by 1,2 order by 2, 3 desc;
-- [n1_none_text]
select 'AUTH.TAXON_AUTHOR' col, count_if(taxon_author in ('None','nan','NULL','null')) n from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
union all select 'AUTH.SHORT_AUTHOR', count_if(short_author in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
union all select 'OSRC.SOURCE_COMMENT', count_if(source_comment in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all select 'OSRC.VERSION', count_if(version in ('None','nan','NULL','null','undefined')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all select 'OSRC.SOURCE_NAME', count_if(source_name in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
union all select 'JUR.ORIGIN', count_if(origin in ('None','nan','NULL','null')) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
union all select 'OSRC.comment_len_lt_5', count_if(length(source_comment) < 5) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES;
-- [v2_vref_orphans]
with v as (select distinct vern_id, tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERNACULARS),
  o as (select r.* from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS r
        left join v on v.vern_id = r.vern_id and v.tsn = r.tsn where v.vern_id is null)
select count(*) orphans,
  count_if(vern_id in (select vern_id from v)) vern_id_exists_on_other_tsn,
  count_if(tsn in (select tsn from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS where name_usage in ('valid','accepted'))) orphan_on_valid_tsn,
  min(update_date) u0, max(update_date) u1,
  (select count(*) from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS where update_date = '1900-01-01' and doc_id_prefix = 'PUB') upd1900_pub
from o;
