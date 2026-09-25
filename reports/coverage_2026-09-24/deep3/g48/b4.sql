-- [q18_eu_vs_us_by_cohort]
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

-- [q19_eu_sample_2025]
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


-- [q20_cluster_status_by_source]
-- Is the pre-2018 Published count inflated by Harvard (source U/CU) imports? 4th and 9th Circuits, 2014-2020, by source and status
with c as (select DOCKET_ID, year(DATE_FILED) yr, SOURCE, PRECEDENTIAL_STATUS st from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
           where DATE_FILED >= '2014-01-01' and DATE_FILED < '2021-01-01'),
d as (select ID, COURT_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS where COURT_ID in ('ca4','ca9'))
select d.COURT_ID, c.yr, c.SOURCE, count(*) n, sum(iff(c.st='Published',1,0)) n_pub, sum(iff(c.st='Unpublished',1,0)) n_unpub
from c join d on d.ID = c.DOCKET_ID group by 1,2,3 order by 1,2,4 desc;

-- [q21_oci_judge_join]
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
