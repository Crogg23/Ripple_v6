-- [q07_clusters_status_by_year]
-- What is the non-Published/Unpublished status that jumps in 2019, and which sources carry it; plus blank names and dispositions
select year(DATE_FILED) yr, coalesce(PRECEDENTIAL_STATUS,'(null)') status, count(*) n,
  sum(iff(nullif(trim(CASE_NAME),'') is null or CASE_NAME='None',1,0)) n_noname,
  sum(iff(nullif(trim(DISPOSITION),'') is not null and DISPOSITION <> 'None',1,0)) n_disp,
  sum(iff(coalesce(CITATION_COUNT,0)=0,1,0)) n_cit0, approx_top_k(SOURCE, 3) top_source
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
where DATE_FILED >= '2016-01-01' and DATE_FILED < '2026-09-25'
group by 1,2 order by 1,3 desc;

-- [q08_clusters_2019_by_court]
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

-- [q09_oci_tx_top_judges]
-- Texas appeals: top 3 trial judges per appellate court, with example lower-court cause numbers
with x as (select d.COURT_ID, d.DATE_FILED, o.ASSIGNED_TO_STR j, o.DOCKET_NUMBER ldn
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d
           join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO o on o.ID = d.ORIGINATING_COURT_INFORMATION_ID
           where d.COURT_ID like 'txctapp%' or d.COURT_ID in ('tex','texcrimapp'))
select COURT_ID, j, count(*) n, count(distinct ldn) n_ldn, min(year(DATE_FILED)) y0, max(year(DATE_FILED)) y1,
  min(ldn) ex1, max(ldn) ex2, sum(count(*)) over (partition by COURT_ID) court_n
from x where nullif(trim(j),'') is not null
group by 1,2 qualify row_number() over (partition by COURT_ID order by n desc) <= 3 order by COURT_ID, n desc;

-- [q10_oci_travis_shift]
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

-- [q11_fd_addendum_words]
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

-- [q12_os_format_probe]
-- OpenSanctions: what the dataset field holds (merged default table and 71K sanctions table), using one known target
select 'default' src, ID, ENTITY_TYPE typ, NAME, DATASETS ds, PROGRAM_IDS, left(IDENTIFIERS,160) ids, LAST_SEEN
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT where NAME ilike '%bank rossiya%' or NAME ilike 'rossiya bank%'
union all
select 'sanctions', ID, SCHEMA, NAME, DATASET, PROGRAM_IDS, left(IDENTIFIERS,160), LAST_SEEN
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS where NAME ilike '%bank rossiya%' or NAME ilike 'rossiya bank%'
limit 12;

-- [q13_eu_id_tags]
-- EU ID lines: which kinds of numbers the list carries, for how many entities, and how many older company listings hide the number in the remark
select 'iden_tag' kind, coalesce(regexp_substr(IDEN_NUMBER, '\\(([a-z]+)-', 1, 1, 'e', 1), '(none)') k, count(*) n_lines, count(distinct ENTITY_LOGICAL_ID) n_ent,
  count(distinct iff(SUBJECT_TYPE='E', ENTITY_LOGICAL_ID, null)) n_ent_company, min(IDEN_NUMBER) ex
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS where nullif(trim(IDEN_NUMBER),'') is not null group by 1,2
union all
select 'remark_digits', iff(regexp_like(ENTITY_REMARK, '.*[0-9]{10,13}.*', 's'), 'has 10-13 digit run', 'no'), count(*), count(distinct ENTITY_LOGICAL_ID),
  count(distinct iff(SUBJECT_TYPE='E', ENTITY_LOGICAL_ID, null)), min(left(ENTITY_REMARK,160))
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SANCTIONS where SUBJECT_TYPE='E' and PROGRAMME in ('UKR','RUS','RUSDA','BLR') group by 1,2
order by 1, 3 desc;
