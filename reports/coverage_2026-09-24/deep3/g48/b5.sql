-- [q22_circuit_published_dedupe]
-- Dull-explanation test for the 4th Circuit rise: published opinions per circuit 2018-2025 as rows, distinct dockets, distinct name+date, and source
with c as (select DOCKET_ID, year(DATE_FILED) yr, CASE_NAME, DATE_FILED, SOURCE from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
           where DATE_FILED >= '2018-01-01' and DATE_FILED < '2026-01-01' and PRECEDENTIAL_STATUS = 'Published'),
d as (select ID, COURT_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cadc','cafc'))
select d.COURT_ID, c.yr, count(*) n_pub, count(distinct c.DOCKET_ID) n_pub_dockets, count(distinct c.CASE_NAME||'|'||to_char(c.DATE_FILED)) n_pub_name_date,
  sum(iff(c.SOURCE='C',1,0)) n_src_c
from c join d on d.ID = c.DOCKET_ID group by 1,2 order by 1,2;

-- [q23_eu_sample_2025]
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

-- [q24_oci_judge_join]
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
