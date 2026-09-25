-- g48: deep pass 3, 2026-09-24. Python door, QUERY_TAG deep3-2026-09-24. Read-only: SELECT/WITH only.
-- Tables: REFERENCE__FED_ITIS_KINGDOMS, JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS, JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES,
--         JUSTICE__INTL_EU_SANCTIONS, JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO.
-- Every statement run is below, in order, with its runtime.

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_itis_kingdoms] (0.2s)
-- Confirm ITIS kingdoms is a 7-row lookup
select KINGDOM_ID, KINGDOM_NAME, UPDATE_DATE, _SOURCE_RUN_ID from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_KINGDOMS order by 1;

-- [q02_eu_entities_by_year] (1.4s)
-- EU list: one row per detail line? Entities by first-listing year (earliest regulation date on any of their lines), type and programme
with r as (
  select ENTITY_LOGICAL_ID id, SUBJECT_TYPE st, PROGRAMME prog,
    iff(nullif(trim(NAAL_LOGICAL_ID),'') is not null,1,0) + iff(nullif(trim(ADDR_LOGICAL_ID),'') is not null,1,0)
    + iff(nullif(trim(BIRT_LOGICAL_ID),'') is not null,1,0) + iff(nullif(trim(IDEN_LOGICAL_ID),'') is not null,1,0)
    + iff(nullif(trim(CITI_LOGICAL_ID),'') is not null,1,0) n_detail,
    try_to_date(LEBA_PUBLICATION_DATE) ent_dt,
    least(coalesce(try_to_date(LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(NAAL_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
          coalesce(try_to_date(ADDR_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(BIRT_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
          coalesce(try_to_date(IDEN_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(CITI_LEBA_PUBLICATION_DATE),'9999-12-31'::date)) row_min_dt,
    iff(nullif(trim(IDEN_NUMBER),'') is not null and IDEN_NUMBER ilike '%taxid%', 1, 0) has_taxid
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS),
e as (
  select id, max(st) st, max(prog) prog, count(distinct st) n_st, count(distinct prog) n_prog, count(*) n_rows,
    min(ent_dt) ent_dt, max(ent_dt) ent_dt_max, min(row_min_dt) first_dt,
    sum(iff(n_detail > 1,1,0)) n_multi, sum(iff(n_detail = 0,1,0)) n_zero, max(has_taxid) has_taxid
  from r group by 1)
select year(first_dt) yr, count(*) n_ent, sum(iff(st='P',1,0)) n_person, sum(iff(st='E',1,0)) n_entity,
  sum(iff(prog in ('UKR','RUS','RUSDA'),1,0)) n_russia_progs, sum(iff(prog='BLR',1,0)) n_blr, sum(iff(prog='IRN',1,0)) n_irn,
  sum(iff(prog in ('TAQA','TERR','AFG'),1,0)) n_terror, sum(has_taxid) n_with_taxid,
  sum(iff(year(ent_dt) <> year(first_dt),1,0)) n_entity_line_later, sum(iff(ent_dt <> ent_dt_max,1,0)) n_entity_dt_varies,
  sum(n_multi) rows_multi_detail, sum(n_zero) rows_zero_detail, sum(iff(n_st>1 or n_prog>1,1,0)) n_mixed, sum(n_rows) n_rows
from e group by 1 order by 1;

-- [q03_opensanctions_eu_probe] (0.8s)
-- OpenSanctions merged list: how EU-listed entries look, how many also carry the US SDN or UK list, and the export date
select ID, ENTITY_TYPE, NAME, DATASETS, PROGRAM_IDS, left(IDENTIFIERS,200) ids, left(SANCTIONS,300) sanc, FIRST_SEEN, LAST_SEEN,
  count(*) over () n_eu, sum(iff(DATASETS ilike '%us_ofac_sdn%',1,0)) over () n_eu_ofac_sdn,
  sum(iff(DATASETS ilike '%gb_hmt%' or DATASETS ilike '%gb_fcdo%',1,0)) over () n_eu_gb, max(LAST_SEEN) over () max_last_seen,
  max(_INGESTED_AT) over () max_ingested
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
where DATASETS ilike '%eu_fsf%'
qualify row_number() over (order by iff(PROGRAM_IDS ilike '%UKR%' and ENTITY_TYPE not ilike 'Person%' and IDENTIFIERS is not null,0,1), ID) <= 6;

-- [q04_clusters_by_year] (1.5s)
-- Opinion clusters by filing year: status mix, never-cited share, disposition fill, blocked, fake names, load dates
select case when DATE_FILED is null then 'null' when year(DATE_FILED) < 1900 then 'pre1900' when year(DATE_FILED) < 1990 then to_char(floor(year(DATE_FILED)/10)*10)||'s'
            when DATE_FILED > '2026-09-24'::date then 'future' else to_char(year(DATE_FILED)) end bucket,
  count(*) n, sum(iff(PRECEDENTIAL_STATUS='Published',1,0)) n_pub, sum(iff(PRECEDENTIAL_STATUS='Unpublished',1,0)) n_unpub,
  sum(iff(PRECEDENTIAL_STATUS not in ('Published','Unpublished') or PRECEDENTIAL_STATUS is null,1,0)) n_other_status,
  sum(iff(coalesce(CITATION_COUNT,0)=0,1,0)) n_cit0, sum(iff(PRECEDENTIAL_STATUS='Published' and coalesce(CITATION_COUNT,0)=0,1,0)) n_pub_cit0,
  sum(iff(nullif(trim(DISPOSITION),'') is not null and DISPOSITION <> 'None',1,0)) n_disp, sum(iff(BLOCKED='t',1,0)) n_blocked,
  sum(iff(DATE_FILED_IS_APPROXIMATE='t',1,0)) n_approx, sum(iff(nullif(trim(CASE_NAME),'') is null or CASE_NAME='None',1,0)) n_noname,
  count(distinct DOCKET_ID) n_dockets, min(DATE_CREATED) created_min, max(DATE_CREATED) created_max
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS group by 1 order by 1;

-- [q05_oci_by_court] (3.1s)
-- Originating-court rows: which appeals courts they hang off (via dockets), what is filled, and whether an opinion with a disposition exists
with d as (select ID docket_id, COURT_ID, ORIGINATING_COURT_INFORMATION_ID oci_id, DATE_FILED
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS where nullif(trim(ORIGINATING_COURT_INFORMATION_ID),'') is not null),
cl as (select DOCKET_ID, count(*) n_cl, max(iff(nullif(trim(DISPOSITION),'') is not null and DISPOSITION <> 'None',1,0)) has_disp
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS where DOCKET_ID in (select docket_id from d) group by 1)
select d.COURT_ID, count(*) n_dockets, count(o.ID) n_oci_hit,
  sum(iff(nullif(trim(o.ASSIGNED_TO_STR),'') is not null,1,0)) n_assigned_str, sum(iff(nullif(trim(o.ASSIGNED_TO_ID),'') is not null,1,0)) n_assigned_id,
  sum(iff(nullif(trim(o.ORDERING_JUDGE_STR),'') is not null,1,0)) n_ordering_str, sum(iff(nullif(trim(o.COURT_REPORTER),'') is not null,1,0)) n_reporter,
  sum(iff(o.DATE_JUDGMENT is not null,1,0)) n_dt_judgment, sum(iff(o.DATE_FILED_NOA is not null,1,0)) n_dt_noa, sum(iff(nullif(trim(o.DOCKET_NUMBER),'') is not null,1,0)) n_lower_docket,
  count(cl.DOCKET_ID) n_with_opinion, sum(cl.has_disp) n_opinion_disp,
  min(year(d.DATE_FILED)) yr_min, max(year(d.DATE_FILED)) yr_max, min(o.DATE_CREATED) oci_created_min, max(o.DATE_CREATED) oci_created_max,
  (select count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO) oci_total
from d left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO o on o.ID = d.oci_id
left join cl on cl.DOCKET_ID = d.docket_id
group by 1 order by 2 desc limit 45;

-- [q06_fd_profile] (0.5s)
-- Judges' disclosure index: clean vs scrambled rows by report year, judge link, amended/extracted flags, page counts
select case when YEAR_COL is null then 'null' when YEAR_COL between 2000 and 2030 then to_char(YEAR_COL) else 'junk' end yr,
  count(*) n, sum(iff(try_to_number(ID) is not null,1,0)) n_id_num, sum(iff(regexp_like(SHA1,'[0-9a-f]{40}'),1,0)) n_sha_ok,
  sum(iff(PERSON_ID is not null,1,0)) n_person, count(distinct PERSON_ID) n_judges,
  sum(iff(IS_AMENDED='t',1,0)) n_amend_t, sum(iff(IS_AMENDED='f',1,0)) n_amend_f, sum(iff(IS_AMENDED not in ('t','f') or IS_AMENDED is null,1,0)) n_amend_other,
  sum(iff(HAS_BEEN_EXTRACTED='t',1,0)) n_extract_t, sum(iff(nullif(trim(ADDENDUM_CONTENT_RAW),'') is not null,1,0)) n_addendum,
  sum(iff(PAGE_COUNT is not null,1,0)) n_pages, median(PAGE_COUNT) med_pages, max(PAGE_COUNT) max_pages,
  approx_top_k(REPORT_TYPE, 5) top_report_type, min(DATE_CREATED) created_min, max(DATE_CREATED) created_max
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES group by 1 order by 1;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q07_clusters_status_by_year] (0.8s)
-- What is the non-Published/Unpublished status that jumps in 2019, and which sources carry it; plus blank names and dispositions
select year(DATE_FILED) yr, coalesce(PRECEDENTIAL_STATUS,'(null)') status, count(*) n,
  sum(iff(nullif(trim(CASE_NAME),'') is null or CASE_NAME='None',1,0)) n_noname,
  sum(iff(nullif(trim(DISPOSITION),'') is not null and DISPOSITION <> 'None',1,0)) n_disp,
  sum(iff(coalesce(CITATION_COUNT,0)=0,1,0)) n_cit0, approx_top_k(SOURCE, 3) top_source
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
where DATE_FILED >= '2016-01-01' and DATE_FILED < '2026-09-25'
group by 1,2 order by 1,3 desc;

-- [q08_clusters_2019_by_court] (1.7s)
-- 2019-2026 opinions by court (via dockets): who produces the Unknown status and the blank case names
with c as (select DOCKET_ID, PRECEDENTIAL_STATUS st, CASE_NAME, CITATION_COUNT, DATE_FILED
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS where DATE_FILED >= '2019-01-01' and DATE_FILED < '2026-09-25'),
d as (select ID, COURT_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS where ID in (select DOCKET_ID from c))
select d.COURT_ID, count(*) n, sum(iff(c.st='Published',1,0)) n_pub, sum(iff(c.st='Unpublished',1,0)) n_unpub, sum(iff(c.st='Unknown',1,0)) n_unknown,
  sum(iff(c.st not in ('Published','Unpublished','Unknown') or c.st is null,1,0)) n_other,
  sum(iff(nullif(trim(c.CASE_NAME),'') is null or c.CASE_NAME='None',1,0)) n_noname,
  sum(iff(year(c.DATE_FILED) between 2019 and 2020,1,0)) n_1920, sum(iff(year(c.DATE_FILED) between 2024 and 2025,1,0)) n_2425,
  sum(iff(year(c.DATE_FILED) between 2019 and 2020 and c.st='Unpublished',1,0)) unpub_1920, sum(iff(year(c.DATE_FILED) between 2024 and 2025 and c.st='Unpublished',1,0)) unpub_2425,
  sum(iff(year(c.DATE_FILED) between 2019 and 2020 and c.st='Published',1,0)) pub_1920, sum(iff(year(c.DATE_FILED) between 2024 and 2025 and c.st='Published',1,0)) pub_2425,
  count(*) - count(d.ID) n_no_docket
from c left join d on d.ID = c.DOCKET_ID
group by 1 order by 2 desc limit 60;

-- [q09_oci_tx_top_judges] (1.2s)
-- Texas appeals: top 3 trial judges per appellate court, with example lower-court cause numbers
with x as (select d.COURT_ID, d.DATE_FILED, o.ASSIGNED_TO_STR j, o.DOCKET_NUMBER ldn
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d
           join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO o on o.ID = d.ORIGINATING_COURT_INFORMATION_ID
           where d.COURT_ID like 'txctapp%' or d.COURT_ID in ('tex','texcrimapp'))
select COURT_ID, j, count(*) n, count(distinct ldn) n_ldn, min(year(DATE_FILED)) y0, max(year(DATE_FILED)) y1,
  min(ldn) ex1, max(ldn) ex2, sum(count(*)) over (partition by COURT_ID) court_n
from x where nullif(trim(j),'') is not null
group by 1,2 qualify row_number() over (partition by COURT_ID order by n desc) <= 3 order by COURT_ID, n desc;

-- [q10_oci_travis_shift] (1.2s)
-- Travis County civil appeals (cause numbers D-1-GN / C-1-CV) by filing year and which appeals court got them; 15th Court opened Sept 2024
with x as (select d.COURT_ID, d.DATE_FILED, upper(o.DOCKET_NUMBER) ldn
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d
           join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO o on o.ID = d.ORIGINATING_COURT_INFORMATION_ID
           where d.COURT_ID like 'txctapp%')
select year(DATE_FILED) yr, count(*) n_all_txctapp,
  sum(iff(ldn like 'D-1-GN%' or ldn like 'C-1-CV%',1,0)) n_travis_civil,
  sum(iff((ldn like 'D-1-GN%' or ldn like 'C-1-CV%') and COURT_ID='txctapp3',1,0)) travis_to_3rd,
  sum(iff((ldn like 'D-1-GN%' or ldn like 'C-1-CV%') and COURT_ID='txctapp15',1,0)) travis_to_15th,
  sum(iff((ldn like 'D-1-GN%' or ldn like 'C-1-CV%') and COURT_ID not in ('txctapp3','txctapp15'),1,0)) travis_to_other,
  sum(iff(COURT_ID='txctapp3',1,0)) all_3rd, sum(iff(COURT_ID='txctapp15',1,0)) all_15th,
  sum(iff(COURT_ID='txctapp15' and not (ldn like 'D-1-GN%' or ldn like 'C-1-CV%'),1,0)) n15_not_travis
from x where DATE_FILED >= '2014-01-01' group by 1 order by 1;

-- [q11_fd_addendum_words] (0.4s)
-- Clean disclosure reports: how often the judge's own addendum admits an omission or error, by report year
select YEAR_COL yr, count(*) n_reports, sum(iff(nullif(trim(ADDENDUM_CONTENT_RAW),'') is not null,1,0)) n_addendum,
  sum(iff(ADDENDUM_CONTENT_RAW ilike '%inadvertent%',1,0)) n_inadvertent,
  sum(iff(regexp_like(ADDENDUM_CONTENT_RAW, '.*(omitted|failed to (report|list|include|disclose)|not previously (reported|disclosed)|should have been (reported|listed|disclosed)).*', 'is'),1,0)) n_omitted,
  sum(iff(ADDENDUM_CONTENT_RAW ilike '%recus%',1,0)) n_recus,
  sum(iff(ADDENDUM_CONTENT_RAW ilike '%amend%',1,0)) n_amend_word,
  sum(iff(IS_AMENDED='t',1,0)) n_amended_flag, count(distinct PERSON_ID) n_judges
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
where YEAR_COL between 2003 and 2022 and try_to_number(ID) is not null
group by 1 order by 1;

-- [q12_os_format_probe] (1.2s)
-- OpenSanctions: what the dataset field holds (merged default table and 71K sanctions table), using one known target
select 'default' src, ID, ENTITY_TYPE typ, NAME, DATASETS ds, PROGRAM_IDS, left(IDENTIFIERS,160) ids, LAST_SEEN
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT where NAME ilike '%bank rossiya%' or NAME ilike 'rossiya bank%'
union all
select 'sanctions', ID, SCHEMA, NAME, DATASET, PROGRAM_IDS, left(IDENTIFIERS,160), LAST_SEEN
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS where NAME ilike '%bank rossiya%' or NAME ilike 'rossiya bank%'
limit 12;

-- [q13_eu_id_tags] (0.6s)
-- EU ID lines: which kinds of numbers the list carries, for how many entities, and how many older company listings hide the number in the remark
select 'iden_tag' kind, coalesce(regexp_substr(IDEN_NUMBER, '\\(([a-z]+)-', 1, 1, 'e', 1), '(none)') k, count(*) n_lines, count(distinct ENTITY_LOGICAL_ID) n_ent,
  count(distinct iff(SUBJECT_TYPE='E', ENTITY_LOGICAL_ID, null)) n_ent_company, min(IDEN_NUMBER) ex
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS where nullif(trim(IDEN_NUMBER),'') is not null group by 1,2
union all
select 'remark_digits', iff(regexp_like(ENTITY_REMARK, '.*[0-9]{10,13}.*', 's'), 'has 10-13 digit run', 'no'), count(*), count(distinct ENTITY_LOGICAL_ID),
  count(distinct iff(SUBJECT_TYPE='E', ENTITY_LOGICAL_ID, null)), min(left(ENTITY_REMARK,160))
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS where SUBJECT_TYPE='E' and PROGRAMME in ('UKR','RUS','RUSDA','BLR') group by 1,2
order by 1, 3 desc;

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q14_eu_vs_us_by_cohort] (0.2s, ERROR)
-- EU entities joined to OpenSanctions (71K sanctions table) by exact name/alias or ID number; share also on US SDN / UK FCDO, by programme family and EU first-listing year
with eu as (select * from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS),
ent as (select ENTITY_LOGICAL_ID eid, max(SUBJECT_TYPE) st, max(PROGRAMME) prog,
          min(least(coalesce(try_to_date(LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(NAAL_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(ADDR_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(BIRT_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(IDEN_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(CITI_LEBA_PUBLICATION_DATE),'9999-12-31'::date))) first_dt
        from eu group by 1),
eu_nm as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(upper(trim(NAAL_WHOLENAME)),'\\s+',' ') nm from eu where nullif(trim(NAAL_WHOLENAME),'') is not null),
eu_id as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(split_part(IDEN_NUMBER,' (',1),'[^0-9A-Za-z]','') tok from eu where nullif(trim(IDEN_NUMBER),'') is not null),
os as (select ID osid, NAME, ALIASES, IDENTIFIERS,
         iff(DATASETS ilike '%EU Financial Sanctions Files%',1,0) is_eu, iff(DATASETS ilike '%US OFAC Specially Designated Nationals%',1,0) is_us,
         iff(DATASETS ilike '%UK FCDO Sanctions List%',1,0) is_uk
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS
       where DATASETS ilike '%EU Financial Sanctions Files%' or DATASETS ilike '%US OFAC Specially Designated Nationals%' or DATASETS ilike '%UK FCDO Sanctions List%'),
os_nm as (select osid, regexp_replace(upper(trim(NAME)),'\\s+',' ') nm from os where NAME is not null
          union
          select osid, regexp_replace(upper(trim(f.value::string)),'\\s+',' ') from os, lateral split_to_table(os.ALIASES, ';') f where nullif(trim(f.value::string),'') is not null),
os_id as (select distinct osid, regexp_replace(f.value::string,'[^0-9A-Za-z]','') tok from os, lateral split_to_table(os.IDENTIFIERS, ';') f),
nm_hits as (select e.eid, o.osid, count(*) n from eu_nm e join os_nm o on o.nm = e.nm group by 1,2),
id_hits as (select e.eid, o.osid, count(*) n from eu_id e join os_id o on o.tok = e.tok where length(e.tok) >= 7 group by 1,2),
hits as (select eid, osid, sum(n) n from (select * from nm_hits union all select * from id_hits) group by 1,2),
hx as (select h.eid, h.osid, h.n, os.is_eu, os.is_us, os.is_uk from hits h join os on os.osid = h.osid),
best as (select eid, osid, is_us, is_uk from hx where is_eu = 1 qualify row_number() over (partition by eid order by n desc, osid) = 1),
anyx as (select eid, max(is_us) us_any, max(is_uk) uk_any, count(distinct iff(is_eu=1,osid,null)) n_eu_cand from hx group by 1),
idx as (select i.eid, max(os.is_us) us_by_id from id_hits i join os on os.osid = i.osid group by 1)
select case when ent.prog in ('UKR','RUS','RUSDA') then 'RUS' when ent.prog='BLR' then 'BLR' when ent.prog='IRN' then 'IRN' else 'other' end fam,
  case when year(first_dt) < 2014 then '<2014' when year(first_dt) <= 2021 then '2014-21' else to_char(year(first_dt)) end cohort,
  count(*) n_ent, sum(iff(ent.st='E',1,0)) n_company, count(best.eid) landed, sum(iff(ent.st='E' and best.eid is not null,1,0)) landed_company,
  sum(coalesce(best.is_us,0)) us_best, sum(iff(ent.st='E',coalesce(best.is_us,0),0)) us_best_company, sum(iff(ent.st='P',coalesce(best.is_us,0),0)) us_best_person,
  sum(coalesce(best.is_uk,0)) uk_best, sum(coalesce(anyx.us_any,0)) us_any_name_or_id, sum(coalesce(idx.us_by_id,0)) us_by_id,
  sum(iff(anyx.n_eu_cand > 1,1,0)) n_multi_cand
from ent left join best on best.eid = ent.eid left join anyx on anyx.eid = ent.eid left join idx on idx.eid = ent.eid
group by 1,2 order by 1,2;

-- [q15_eu_sample_2025] (0.2s, ERROR)
-- Eyeball: 2025-26 Russia-programme companies the EU listed, matched to OpenSanctions; 6 not on US SDN and 6 on it
with eu as (select * from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS),
ent as (select ENTITY_LOGICAL_ID eid, max(SUBJECT_TYPE) st, max(PROGRAMME) prog, max(EU_REF_NUM) ref,
          min(least(coalesce(try_to_date(LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(NAAL_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(ADDR_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(BIRT_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(IDEN_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(CITI_LEBA_PUBLICATION_DATE),'9999-12-31'::date))) first_dt,
          max(iff(NAAL_LANGUAGE='EN', NAAL_WHOLENAME, null)) en_name, max(ADDR_COUNTRY) addr_cty
        from eu group by 1),
eu_nm as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(upper(trim(NAAL_WHOLENAME)),'\\s+',' ') nm from eu where nullif(trim(NAAL_WHOLENAME),'') is not null),
os as (select ID osid, NAME, ALIASES, DATASETS, PROGRAM_IDS, iff(DATASETS ilike '%US OFAC Specially Designated Nationals%',1,0) is_us
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS where DATASETS ilike '%EU Financial Sanctions Files%'),
os_nm as (select osid, regexp_replace(upper(trim(NAME)),'\\s+',' ') nm from os where NAME is not null
          union select osid, regexp_replace(upper(trim(f.value::string)),'\\s+',' ') from os, lateral split_to_table(os.ALIASES, ';') f where nullif(trim(f.value::string),'') is not null),
best as (select e.eid, o.osid, count(*) n from eu_nm e join os_nm o on o.nm = e.nm group by 1,2 qualify row_number() over (partition by e.eid order by count(*) desc, o.osid) = 1)
select ent.eid, ent.ref, ent.first_dt, ent.prog, ent.addr_cty, left(ent.en_name,70) eu_name, left(os.NAME,70) os_name, os.is_us, os.PROGRAM_IDS,
  (select count(*) from ent e2 where e2.st='E' and e2.prog in ('UKR','RUS','RUSDA') and year(e2.first_dt) >= 2025) n_pool
from ent join best on best.eid = ent.eid join os on os.osid = best.osid
where ent.st = 'E' and ent.prog in ('UKR','RUS','RUSDA') and year(ent.first_dt) >= 2025
qualify row_number() over (partition by os.is_us order by hash(ent.eid)) <= 6
order by os.is_us, ent.first_dt;

-- [q16_courts_opinions_by_year] (1.6s)
-- Appeals courts: opinions per year and status 2010-2025 (13 federal circuits + 4 Texas courts), plus Texas dockets filed per year as the coverage check
with c as (select DOCKET_ID, year(DATE_FILED) yr, PRECEDENTIAL_STATUS st from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
           where DATE_FILED >= '2010-01-01' and DATE_FILED < '2026-01-01'),
d as (select ID, COURT_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cadc','cafc','txctapp1','txctapp4','txctapp5','txctapp14'))
select 'opinions' kind, d.COURT_ID court, c.yr, count(*) n, sum(iff(c.st='Published',1,0)) n_pub, sum(iff(c.st='Unpublished',1,0)) n_unpub
from c join d on d.ID = c.DOCKET_ID group by 1,2,3
union all
select 'dockets', COURT_ID, year(DATE_FILED), count(*), null, null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where COURT_ID in ('txctapp1','txctapp4','txctapp5','txctapp14') and DATE_FILED >= '2010-01-01' and DATE_FILED < '2026-01-01' group by 1,2,3
order by 1,2,3;

-- [q17_fd_admit_judges] (1.1s)
-- Judges whose own report addenda admit an omission in the most years; peer median; amended vs not
with f as (select PERSON_ID pid, YEAR_COL yr, ADDENDUM_CONTENT_RAW a, IS_AMENDED am,
             iff(ADDENDUM_CONTENT_RAW ilike '%inadvertent%' or regexp_like(ADDENDUM_CONTENT_RAW, '.*(omitted|failed to (report|list|include|disclose)|not previously (reported|disclosed)).*', 'is'),1,0) admit
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
           where YEAR_COL between 2003 and 2020 and try_to_number(ID) is not null and PERSON_ID is not null),
j as (select pid, count(*) n_rep, count(distinct yr) n_yrs, count(distinct iff(admit=1, yr, null)) n_admit_yrs, sum(iff(am='t',1,0)) n_amended,
        listagg(distinct iff(admit=1, yr, null), ',') within group (order by iff(admit=1, yr, null)) admit_years,
        max(iff(admit=1, left(regexp_replace(a,'\\s+',' '), 260), null)) ex
      from f group by 1)
select j.pid, p.NAME_FIRST||' '||p.NAME_LAST judge, j.n_rep, j.n_yrs, j.n_admit_yrs, j.n_amended, j.admit_years, j.ex,
  (select count(*) from j where n_yrs >= 8) n_judges_8plus, (select count(*) from j where n_yrs >= 8 and n_admit_yrs >= 1) n_8plus_any_admit,
  (select median(n_admit_yrs) from j where n_yrs >= 8) med_admit_yrs_8plus,
  (select round(avg(admit)*100,1) from f where yr between 2011 and 2018 and am='t') pct_admit_amended_1118,
  (select round(avg(admit)*100,1) from f where yr between 2011 and 2018 and am='f') pct_admit_orig_1118
from j left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES p on p.ID = j.pid
where j.n_yrs >= 5 order by j.n_admit_yrs desc, j.n_rep desc limit 15;

-- ===== connection: b4.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q18_eu_vs_us_by_cohort] (2.0s)
-- EU entities joined to OpenSanctions (71K sanctions table) by exact name/alias or ID number; share also on US SDN / UK FCDO, by programme family and EU first-listing year
with eu as (select * from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS),
ent as (select ENTITY_LOGICAL_ID eid, max(SUBJECT_TYPE) st, max(PROGRAMME) prog,
          min(least(coalesce(try_to_date(LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(NAAL_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(ADDR_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(BIRT_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(IDEN_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(CITI_LEBA_PUBLICATION_DATE),'9999-12-31'::date))) first_dt
        from eu group by 1),
eu_nm as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(upper(trim(NAAL_WHOLENAME)),'\\s+',' ') nm from eu where nullif(trim(NAAL_WHOLENAME),'') is not null),
eu_id as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(split_part(IDEN_NUMBER,' (',1),'[^0-9A-Za-z]','') tok from eu where nullif(trim(IDEN_NUMBER),'') is not null),
os as (select ID osid, NAME, ALIASES, IDENTIFIERS,
         iff(DATASET ilike '%EU Financial Sanctions Files%',1,0) is_eu, iff(DATASET ilike '%US OFAC Specially Designated Nationals%',1,0) is_us,
         iff(DATASET ilike '%UK FCDO Sanctions List%',1,0) is_uk
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS
       where DATASET ilike '%EU Financial Sanctions Files%' or DATASET ilike '%US OFAC Specially Designated Nationals%' or DATASET ilike '%UK FCDO Sanctions List%'),
os_nm as (select osid, regexp_replace(upper(trim(NAME)),'\\s+',' ') nm from os where NAME is not null
          union
          select osid, regexp_replace(upper(trim(f.value::string)),'\\s+',' ') from os, lateral split_to_table(os.ALIASES, ';') f where nullif(trim(f.value::string),'') is not null),
os_id as (select distinct osid, regexp_replace(f.value::string,'[^0-9A-Za-z]','') tok from os, lateral split_to_table(os.IDENTIFIERS, ';') f),
nm_hits as (select e.eid, o.osid, count(*) n from eu_nm e join os_nm o on o.nm = e.nm group by 1,2),
id_hits as (select e.eid, o.osid, count(*) n from eu_id e join os_id o on o.tok = e.tok where length(e.tok) >= 7 group by 1,2),
hits as (select eid, osid, sum(n) n from (select * from nm_hits union all select * from id_hits) group by 1,2),
hx as (select h.eid, h.osid, h.n, os.is_eu, os.is_us, os.is_uk from hits h join os on os.osid = h.osid),
best as (select eid, osid, is_us, is_uk from hx where is_eu = 1 qualify row_number() over (partition by eid order by n desc, osid) = 1),
anyx as (select eid, max(is_us) us_any, max(is_uk) uk_any, count(distinct iff(is_eu=1,osid,null)) n_eu_cand from hx group by 1),
idx as (select i.eid, max(os.is_us) us_by_id from id_hits i join os on os.osid = i.osid group by 1)
select case when ent.prog in ('UKR','RUS','RUSDA') then 'RUS' when ent.prog='BLR' then 'BLR' when ent.prog='IRN' then 'IRN' else 'other' end fam,
  case when year(first_dt) < 2014 then '<2014' when year(first_dt) <= 2021 then '2014-21' else to_char(year(first_dt)) end cohort,
  count(*) n_ent, sum(iff(ent.st='E',1,0)) n_company, count(best.eid) landed, sum(iff(ent.st='E' and best.eid is not null,1,0)) landed_company,
  sum(coalesce(best.is_us,0)) us_best, sum(iff(ent.st='E',coalesce(best.is_us,0),0)) us_best_company, sum(iff(ent.st='P',coalesce(best.is_us,0),0)) us_best_person,
  sum(coalesce(best.is_uk,0)) uk_best, sum(coalesce(anyx.us_any,0)) us_any_name_or_id, sum(coalesce(idx.us_by_id,0)) us_by_id,
  sum(iff(anyx.n_eu_cand > 1,1,0)) n_multi_cand
from ent left join best on best.eid = ent.eid left join anyx on anyx.eid = ent.eid left join idx on idx.eid = ent.eid
group by 1,2 order by 1,2;

-- [q19_eu_sample_2025] (0.2s, ERROR)
-- Eyeball: 2025-26 Russia-programme companies the EU listed, matched to OpenSanctions; 6 not on US SDN and 6 on it
with eu as (select * from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS),
ent as (select ENTITY_LOGICAL_ID eid, max(SUBJECT_TYPE) st, max(PROGRAMME) prog, max(EU_REF_NUM) ref,
          min(least(coalesce(try_to_date(LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(NAAL_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(ADDR_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(BIRT_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(IDEN_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(CITI_LEBA_PUBLICATION_DATE),'9999-12-31'::date))) first_dt,
          max(iff(NAAL_LANGUAGE='EN', NAAL_WHOLENAME, null)) en_name, max(ADDR_COUNTRY) addr_cty
        from eu group by 1),
eu_nm as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(upper(trim(NAAL_WHOLENAME)),'\\s+',' ') nm from eu where nullif(trim(NAAL_WHOLENAME),'') is not null),
os as (select ID osid, NAME, ALIASES, DATASET, PROGRAM_IDS, iff(DATASET ilike '%US OFAC Specially Designated Nationals%',1,0) is_us
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS where DATASET ilike '%EU Financial Sanctions Files%'),
os_nm as (select osid, regexp_replace(upper(trim(NAME)),'\\s+',' ') nm from os where NAME is not null
          union select osid, regexp_replace(upper(trim(f.value::string)),'\\s+',' ') from os, lateral split_to_table(os.ALIASES, ';') f where nullif(trim(f.value::string),'') is not null),
best as (select e.eid, o.osid, count(*) n from eu_nm e join os_nm o on o.nm = e.nm group by 1,2 qualify row_number() over (partition by e.eid order by count(*) desc, o.osid) = 1),
ofac as (select regexp_replace(upper(trim(SDN_NAME)),'\\s+',' ') nm, count(*) n from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN group by 1)
select ent.eid, ent.ref, ent.first_dt, ent.prog, ent.addr_cty, left(ent.en_name,70) eu_name, left(os.NAME,70) os_name, os.is_us, os.PROGRAM_IDS,
  coalesce(o1.n,0) + coalesce(o2.n,0) ofac_table_exact_name,
  (select count(*) from ent e2 where e2.st='E' and e2.prog in ('UKR','RUS','RUSDA') and year(e2.first_dt) >= 2025) n_pool,
  (select max(_INGESTED_AT) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN) ofac_loaded, (select max(LAST_SEEN) from os) os_last_seen
from ent join best on best.eid = ent.eid join os on os.osid = best.osid
left join ofac o1 on o1.nm = regexp_replace(upper(trim(os.NAME)),'\\s+',' ')
left join ofac o2 on o2.nm = regexp_replace(upper(trim(ent.en_name)),'\\s+',' ') and o2.nm <> regexp_replace(upper(trim(os.NAME)),'\\s+',' ')
where ent.st = 'E' and ent.prog in ('UKR','RUS','RUSDA') and year(ent.first_dt) >= 2025
qualify row_number() over (partition by os.is_us order by hash(ent.eid)) <= 6
order by os.is_us, ent.first_dt;

-- [q20_cluster_status_by_source] (1.5s)
-- Is the pre-2018 Published count inflated by Harvard (source U/CU) imports? 4th and 9th Circuits, 2014-2020, by source and status
with c as (select DOCKET_ID, year(DATE_FILED) yr, SOURCE, PRECEDENTIAL_STATUS st from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
           where DATE_FILED >= '2014-01-01' and DATE_FILED < '2021-01-01'),
d as (select ID, COURT_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS where COURT_ID in ('ca4','ca9'))
select d.COURT_ID, c.yr, c.SOURCE, count(*) n, sum(iff(c.st='Published',1,0)) n_pub, sum(iff(c.st='Unpublished',1,0)) n_unpub
from c join d on d.ID = c.DOCKET_ID group by 1,2,3 order by 1,2,4 desc;

-- [q21_oci_judge_join] (0.1s, ERROR)
-- One join: originating-court ASSIGNED_TO_ID to CourtListener judges; land rate and name agreement
with o as (select ASSIGNED_TO_ID aid, ASSIGNED_TO_STR s from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO
           where nullif(trim(ASSIGNED_TO_ID),'') is not null),
j as (select ID, NAME_FIRST, NAME_LAST from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES)
select o.aid, j.NAME_FIRST||' '||j.NAME_LAST judge, count(*) n, min(o.s) str_example,
  sum(iff(o.s ilike '%'||j.NAME_LAST||'%',1,0)) n_str_has_lastname,
  sum(count(*)) over () rows_with_id, count(*) over () n_ids,
  sum(iff(j.ID is not null, count(*), 0)) over () rows_landed,
  sum(sum(iff(o.s ilike '%'||j.NAME_LAST||'%',1,0))) over () rows_name_agree
from o left join j on j.ID = o.aid group by 1,2 order by n desc limit 8;

-- ===== connection: b5.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q22_circuit_published_dedupe] (1.4s)
-- Dull-explanation test for the 4th Circuit rise: published opinions per circuit 2018-2025 as rows, distinct dockets, distinct name+date, and source
with c as (select DOCKET_ID, year(DATE_FILED) yr, CASE_NAME, DATE_FILED, SOURCE from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
           where DATE_FILED >= '2018-01-01' and DATE_FILED < '2026-01-01' and PRECEDENTIAL_STATUS = 'Published'),
d as (select ID, COURT_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cadc','cafc'))
select d.COURT_ID, c.yr, count(*) n_pub, count(distinct c.DOCKET_ID) n_pub_dockets, count(distinct c.CASE_NAME||'|'||to_char(c.DATE_FILED)) n_pub_name_date,
  sum(iff(c.SOURCE='C',1,0)) n_src_c
from c join d on d.ID = c.DOCKET_ID group by 1,2 order by 1,2;

-- [q23_eu_sample_2025] (1.8s)
-- Eyeball: 2025-26 Russia-programme companies the EU listed, matched to OpenSanctions; 6 not on US SDN and 6 on it; cross-check against the warehouse OFAC SDN table by exact name
with eu as (select * from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS),
ent as (select ENTITY_LOGICAL_ID eid, max(SUBJECT_TYPE) st, max(PROGRAMME) prog, max(EU_REF_NUM) ref,
          min(least(coalesce(try_to_date(LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(NAAL_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(ADDR_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(BIRT_LEBA_PUBLICATION_DATE),'9999-12-31'::date),
              coalesce(try_to_date(IDEN_LEBA_PUBLICATION_DATE),'9999-12-31'::date), coalesce(try_to_date(CITI_LEBA_PUBLICATION_DATE),'9999-12-31'::date))) first_dt,
          max(iff(NAAL_LANGUAGE='EN', NAAL_WHOLENAME, null)) en_name, max(ADDR_COUNTRY) addr_cty
        from eu group by 1),
eu_nm as (select distinct ENTITY_LOGICAL_ID eid, regexp_replace(upper(trim(NAAL_WHOLENAME)),'\\s+',' ') nm from eu where nullif(trim(NAAL_WHOLENAME),'') is not null),
os as (select ID osid, NAME, ALIASES, DATASET, PROGRAM_IDS, LAST_SEEN, iff(DATASET ilike '%US OFAC Specially Designated Nationals%',1,0) is_us
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS where DATASET ilike '%EU Financial Sanctions Files%'),
os_nm as (select osid, regexp_replace(upper(trim(NAME)),'\\s+',' ') nm from os where NAME is not null
          union select osid, regexp_replace(upper(trim(f.value::string)),'\\s+',' ') from os, lateral split_to_table(os.ALIASES, ';') f where nullif(trim(f.value::string),'') is not null),
best as (select e.eid, o.osid, count(*) n from eu_nm e join os_nm o on o.nm = e.nm group by 1,2 qualify row_number() over (partition by e.eid order by count(*) desc, o.osid) = 1),
ofac as (select regexp_replace(upper(trim(SDN_NAME)),'\\s+',' ') nm, count(*) n from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN group by 1)
select ent.eid, ent.ref, ent.first_dt, ent.prog, ent.addr_cty, left(ent.en_name,70) eu_name, left(os.NAME,70) os_name, os.is_us, os.PROGRAM_IDS,
  coalesce(o1.n,0) + coalesce(o2.n,0) ofac_table_exact_name,
  (select count(*) from ent e2 where e2.st='E' and e2.prog in ('UKR','RUS','RUSDA') and year(e2.first_dt) >= 2025) n_pool,
  (select max(_INGESTED_AT) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN) ofac_loaded, (select max(LAST_SEEN) from os) os_last_seen
from ent join best on best.eid = ent.eid join os on os.osid = best.osid
left join ofac o1 on o1.nm = regexp_replace(upper(trim(os.NAME)),'\\s+',' ')
left join ofac o2 on o2.nm = regexp_replace(upper(trim(ent.en_name)),'\\s+',' ') and o2.nm <> regexp_replace(upper(trim(os.NAME)),'\\s+',' ')
where ent.st = 'E' and ent.prog in ('UKR','RUS','RUSDA') and year(ent.first_dt) >= 2025
qualify row_number() over (partition by os.is_us order by hash(ent.eid)) <= 6
order by os.is_us, ent.first_dt;

-- [q24_oci_judge_join] (0.5s)
-- One join: originating-court ASSIGNED_TO_ID to CourtListener judges; land rate and whether the free-text name agrees
with o as (select ASSIGNED_TO_ID aid, ASSIGNED_TO_STR s from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO
           where nullif(trim(ASSIGNED_TO_ID),'') is not null),
j as (select ID, NAME_FIRST, NAME_LAST from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES),
g as (select o.aid, max(j.ID) jid, max(j.NAME_FIRST||' '||j.NAME_LAST) judge, count(*) n, min(o.s) ex,
        sum(iff(o.s ilike '%'||j.NAME_LAST||'%',1,0)) n_agree
      from o left join j on j.ID = o.aid group by 1)
select aid, judge, n, ex, n_agree, sum(n) over () rows_with_id, count(*) over () n_ids,
  sum(iff(jid is not null, n, 0)) over () rows_landed, sum(n_agree) over () rows_name_agree
from g order by n desc limit 8;

-- ===== totals
-- 24 SELECT/WITH statements (4 failed to compile and were fixed in a later batch: q14 and q15 used DATASETS where the 71K OpenSanctions table has DATASET; q19 read LAST_SEEN from a CTE that lacked it; q21 had a bad GROUP BY)
-- + 10 session-setup statements (5 connections x 2) = 34 of the 35-statement budget.
