-- [q14_eu_vs_us_by_cohort]
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

-- [q15_eu_sample_2025]
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

-- [q16_courts_opinions_by_year]
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

-- [q17_fd_admit_judges]
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
