-- [q01_itis_kingdoms]
-- Confirm ITIS kingdoms is a 7-row lookup
select KINGDOM_ID, KINGDOM_NAME, UPDATE_DATE, _SOURCE_RUN_ID from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_KINGDOMS order by 1;

-- [q02_eu_entities_by_year]
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

-- [q03_opensanctions_eu_probe]
-- OpenSanctions merged list: how EU-listed entries look, how many also carry the US SDN or UK list, and the export date
select ID, ENTITY_TYPE, NAME, DATASETS, PROGRAM_IDS, left(IDENTIFIERS,200) ids, left(SANCTIONS,300) sanc, FIRST_SEEN, LAST_SEEN,
  count(*) over () n_eu, sum(iff(DATASETS ilike '%us_ofac_sdn%',1,0)) over () n_eu_ofac_sdn,
  sum(iff(DATASETS ilike '%gb_hmt%' or DATASETS ilike '%gb_fcdo%',1,0)) over () n_eu_gb, max(LAST_SEEN) over () max_last_seen,
  max(_INGESTED_AT) over () max_ingested
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
where DATASETS ilike '%eu_fsf%'
qualify row_number() over (order by iff(PROGRAM_IDS ilike '%UKR%' and ENTITY_TYPE not ilike 'Person%' and IDENTIFIERS is not null,0,1), ID) <= 6;

-- [q04_clusters_by_year]
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

-- [q05_oci_by_court]
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

-- [q06_fd_profile]
-- Judges' disclosure index: clean vs scrambled rows by report year, judge link, amended/extracted flags, page counts
select case when YEAR_COL is null then 'null' when YEAR_COL between 2000 and 2030 then to_char(YEAR_COL) else 'junk' end yr,
  count(*) n, sum(iff(try_to_number(ID) is not null,1,0)) n_id_num, sum(iff(regexp_like(SHA1,'[0-9a-f]{40}'),1,0)) n_sha_ok,
  sum(iff(PERSON_ID is not null,1,0)) n_person, count(distinct PERSON_ID) n_judges,
  sum(iff(IS_AMENDED='t',1,0)) n_amend_t, sum(iff(IS_AMENDED='f',1,0)) n_amend_f, sum(iff(IS_AMENDED not in ('t','f') or IS_AMENDED is null,1,0)) n_amend_other,
  sum(iff(HAS_BEEN_EXTRACTED='t',1,0)) n_extract_t, sum(iff(nullif(trim(ADDENDUM_CONTENT_RAW),'') is not null,1,0)) n_addendum,
  sum(iff(PAGE_COUNT is not null,1,0)) n_pages, median(PAGE_COUNT) med_pages, max(PAGE_COUNT) max_pages,
  approx_top_k(REPORT_TYPE, 5) top_report_type, min(DATE_CREATED) created_min, max(DATE_CREATED) created_max
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES group by 1 order by 1;
