-- deep3 / g78: proper look at five glance-only tables, 2026-09-24
-- Tables: TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD, TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS,
--         TRANSPORT__FED_DOT_BTS, TRANSPORT__FED_FRA_SAFETY, HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
-- Door: Python (connect/db.py) via g78/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g78/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- FRA_SAFETY: the whole table (1 row), to confirm it is a failed load
select * from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_SAFETY;

-- [q02] statement 2
-- DOT_BTS: confirm it is a 21-row catalog; are the data columns all empty; list names
select count(*) n, count(distinct DATABASE_NAME) names,
  count_if(nullif(trim(MODE::varchar),'') is not null) mode_filled, count_if(nullif(trim(SUBJECT::varchar),'') is not null) subj_filled,
  count_if(nullif(trim(YEAR::varchar),'') is not null) year_filled, count_if(nullif(trim(CARRIER_CODE::varchar),'') is not null) carrier_filled,
  count_if(nullif(trim(ORIGIN::varchar),'') is not null) origin_filled, count_if(nullif(trim(STATE_FIPS::varchar),'') is not null) fips_filled,
  listagg(DATABASE_NAME, ' | ') within group (order by DATABASE_NAME) names_list
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_DOT_BTS;

-- [q03] statement 3
-- Private airports: is each airport repeated? distinct codes, copies per code, states, status values
with t as (select PRIVATE_AIRPORT_LIST_FOR_WHICH_INFORMATION_HAS_NOT_BEEN_UPDATED_IN_THE_LAST_3_YEARS code, UNNAMED_1 nm, UNNAMED_2 site, UNNAMED_3 city, UNNAMED_4 st, UNNAMED_5 status
           from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS),
c as (select code, count(*) k from t group by 1)
select 'profile' k, count(*)::varchar a, count(distinct code)::varchar b, count(distinct code||'|'||nm||'|'||site||'|'||city||'|'||st||'|'||status)::varchar c,
  (select min(k)||'-'||max(k)||' median '||median(k) from c) d, listagg(distinct status, ',') e from t
union all select 'state', st, count(*)::varchar, count(distinct code)::varchar, null, null from t group by st
union all select 'sample', code, nm, site, city, st from (select * from t order by code limit 8);

-- [q04] statement 4
-- FRA deaths by railroad: grain check, years, person types with death totals
with t as (select * from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD)
select 'profile' k, count(*)::varchar a, count(distinct RAILROAD_CODE||'|'||INCIDENT_YEAR||'|'||TYPE_OF_PERSON)::varchar b,
  count(distinct RAILROAD_CODE)::varchar c, min(INCIDENT_YEAR)||'-'||max(INCIDENT_YEAR) d, sum(DEATHS)::varchar e,
  count(distinct _INGESTED_AT)::varchar f, count_if(DEATHS<=0)::varchar g from t
union all select 'type', TYPE_OF_PERSON, count(*)::varchar, sum(DEATHS)::varchar, min(INCIDENT_YEAR)||'-'||max(INCIDENT_YEAR), null, null, null from t group by 2
union all select 'year', INCIDENT_YEAR::varchar, count(*)::varchar, sum(DEATHS)::varchar, sum(iff(TYPE_OF_PERSON ilike 'trespass%',DEATHS,0))::varchar, count(distinct RAILROAD_CODE)::varchar, null, null from t group by 2
order by 1,2;

-- [q05] statement 5
-- Slave voyages: grain check. Distinct voyage ids, copies per id, are copies identical rows, flag and status values
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC),
c as (select VOYAGEID, count(*) k from t group by 1)
select 'profile' k, count(*)::varchar a, count(distinct VOYAGEID)::varchar b, (select count_if(k>1)||' ids repeat; max '||max(k) from c) c,
  count(distinct hash(*))::varchar d, listagg(distinct INTRAAMER::varchar, ',') e, listagg(distinct STATUS::varchar, ',') f,
  min(try_to_number(YEARAM))||'-'||max(try_to_number(YEARAM)) g from t
union all select 'topid', VOYAGEID, k::varchar, null, null, null, null, null from (select * from c order by k desc limit 5)
union all select 'idlen', length(VOYAGEID)::varchar, count(*)::varchar, min(VOYAGEID), max(VOYAGEID), null, null, null from t group by 2;

-- [q06] statement 6
-- FRA deaths: who carries the rise in trespasser deaths? Per railroad, yearly average 2015-2017 vs 2023-2025, sorted by change.
-- Plus: how many railroads went up / down, and code-name drift (codes with 2+ names, names with 2+ codes).
with t as (select * from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD where TYPE_OF_PERSON = 'Trespassers'),
r as (select RAILROAD_CODE code, max(RAILROAD_NAME) nm, max(PARENT_RAILROAD_CODE) parent,
        sum(iff(INCIDENT_YEAR between 2015 and 2017, DEATHS, 0))/3 a, sum(iff(INCIDENT_YEAR between 2023 and 2025, DEATHS, 0))/3 b,
        sum(iff(INCIDENT_YEAR = 2025, DEATHS, 0)) y25, min(INCIDENT_YEAR) first_yr
      from t group by 1),
tot as (select sum(a) ta, sum(b) tb, count_if(b>a) up, count_if(b<a) down, count_if(a>0 and b=0) gone, count_if(a=0 and b>0) new_ from r)
select 'total' k, null code, null nm, round(ta,1) a, round(tb,1) b, round(tb-ta,1) d, up||' up / '||down||' down / '||gone||' gone / '||new_||' new' note from tot
union all select * from (select 'rr', code, nm, round(a,1), round(b,1), round(b-a,1), 'parent '||parent||'; 2025 '||y25||'; first yr '||first_yr from r order by b-a desc limit 15)
union all select * from (select 'rr_down', code, nm, round(a,1), round(b,1), round(b-a,1), 'parent '||parent from r order by b-a asc limit 6)
union all select 'drift_code', RAILROAD_CODE, listagg(distinct RAILROAD_NAME, ' | '), count(distinct RAILROAD_NAME), null, null, null
  from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD group by RAILROAD_CODE having count(distinct RAILROAD_NAME) > 1
union all select 'drift_name', listagg(distinct RAILROAD_CODE, ' | '), RAILROAD_NAME, count(distinct RAILROAD_CODE), null, null, null
  from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD group by RAILROAD_NAME having count(distinct RAILROAD_CODE) > 1;

-- [q07] statement 7
-- FRA casualties (the source file): do fatalities reconcile with the deaths table by year, and are suicides flagged?
-- Fatality rows by year x COVERED_DATA_REASON x CASUALTY_OCCURRENCE_CODE for trespassers, 2008-2025
select INCIDENT_YEAR, TYPE_OF_PERSON ilike 'Trespass%' tresp, COVERED_DATA_CODE, COVERED_DATA_REASON, CASUALTY_OCCURRENCE_CODE, count(*) n
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
where FATALITY = 'Yes' and INCIDENT_YEAR between 2008 and 2025
group by 1,2,3,4,5 order by 1,2,3,4,5;

-- [q08] statement 8
-- FRA deaths table: yearly series 2010-2026 for the big railroads, trespassers and everyone else, to see where UP's jump starts
select INCIDENT_YEAR yr,
  sum(iff(RAILROAD_CODE='UP' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) up_tr,
  sum(iff(RAILROAD_CODE='UP' and TYPE_OF_PERSON<>'Trespassers', DEATHS, 0)) up_other,
  sum(iff(RAILROAD_CODE='BNSF' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) bnsf_tr,
  sum(iff(RAILROAD_CODE='CSX' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) csx_tr,
  sum(iff(RAILROAD_CODE='NS' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) ns_tr,
  sum(iff(RAILROAD_CODE='ATK' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) atk_tr,
  sum(iff(RAILROAD_CODE='BLF' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) blf_tr,
  sum(iff(TYPE_OF_PERSON='Trespassers', DEATHS, 0)) all_tr,
  sum(iff(RAILROAD_CODE='UP' and TYPE_OF_PERSON like 'Worker%', DEATHS, 0)) up_worker,
  sum(iff(TYPE_OF_PERSON like 'Worker%', DEATHS, 0)) all_worker
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD
where INCIDENT_YEAR >= 2010 group by 1 order by 1;

-- [q09] statement 9
-- FRA casualties (source): where did UP's and BNSF's trespasser deaths rise? State split, yearly avg 2015-2017 vs 2023-2025
-- Also the last date on file, to size the 2026 partial year
with f as (select RAILROAD_CODE rr, STATE_NAME st, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS') and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
s as (select rr, st, count_if(y<=2017)/3 a, count_if(y>=2023)/3 b from f group by 1,2),
tot as (select rr, sum(a) ta, sum(b) tb, count(*) states, count_if(b>a) up_states from s group by 1)
select 'tot' k, rr, null st, round(ta,1) a, round(tb,1) b, round(tb-ta,1) d, states||' states, '||up_states||' up' note from tot
union all select * from (select 'st', rr, st, round(a,1), round(b,1), round(b-a,1), round((b-a)/nullif((select tb-ta from tot where tot.rr=s.rr),0),2)::varchar from s
  qualify row_number() over (partition by rr order by b-a desc) <= 6)
union all select 'maxdate', null, null, null, null, null, (select max(DATE)::varchar from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES)
order by 1, 2, 6 desc;

-- [q09b] statement 10
-- RERUN of q09 with the share computed by a join (q09 failed to compile on a correlated subquery)
-- FRA casualties (source): where did UP's and BNSF's trespasser deaths rise? State split, yearly avg 2015-2017 vs 2023-2025; plus last date on file
with f as (select RAILROAD_CODE rr, STATE_NAME st, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS') and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
s as (select rr, st, count_if(y<=2017)/3 a, count_if(y>=2023)/3 b from f group by 1,2),
tot as (select rr, sum(a) ta, sum(b) tb, count(*) states, count_if(b>a) up_states from s group by 1),
j as (select s.*, round((s.b-s.a)/nullif(tot.tb-tot.ta,0),2) share from s join tot on s.rr=tot.rr)
select 'tot' k, rr, null st, round(ta,1) a, round(tb,1) b, round(tb-ta,1) d, states||' states, '||up_states||' up' note from tot
union all select * from (select 'st', rr, st, round(a,1), round(b,1), round(b-a,1), share::varchar from j
  qualify row_number() over (partition by rr order by b-a desc) <= 6)
union all select 'maxdate', null, null, null, null, null, (select max(DATE)::varchar from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES)
order by 1, 2, 6 desc;

-- [q10] statement 11
-- FRA casualties: is UP's jump a reporting change? For trespasser deaths, 2015-2017 vs 2023-2025, UP vs BNSF/CSX/NS:
-- narratives that say found / body / discovered (unwitnessed), that say suicide, blank narratives, unknown event, median age, top event
with f as (select RAILROAD_CODE rr, iff(INCIDENT_YEAR<=2017,'A_2015_17','B_2023_25') p, upper(coalesce(NARRATIVE,'')) nar, EVENT, PHYSICAL_ACT_CIRCUMSTANCES pac, AGE_OF_PERSON age, GENERAL_LOCATION_OF_PERSON loc
           from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS')
             and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025))
select rr, p, count(*) n,
  count_if(nar like any ('%FOUND%','%DISCOVERED%','%BODY%','%REMAINS%','%DECEASED%')) found_like,
  count_if(nar like any ('%SUICID%','%INTENTIONAL%')) suicide_word,
  count_if(trim(nar)='') blank_nar,
  count_if(EVENT ilike '%unknown%' or EVENT is null) event_unknown,
  median(age) med_age, count_if(age is null or age=0) age_missing,
  mode(EVENT) top_event, mode(pac) top_act, mode(loc) top_loc
from f group by 1,2 order by 1,2;

-- [q11] statement 12
-- FRA casualties: UP trespasser deaths in California by county, 2015-2017 vs 2023-2025 (yearly avg), and BNSF in the same counties
with f as (select RAILROAD_CODE rr, COUNTY_NAME cty, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and STATE_NAME='CALIFORNIA' and RAILROAD_CODE in ('UP','BNSF','ATK','SCAX','PCJX','PCMZ')
             and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025))
select cty, round(count_if(rr='UP' and y<=2017)/3,1) up_a, round(count_if(rr='UP' and y>=2023)/3,1) up_b,
  round(count_if(rr='BNSF' and y<=2017)/3,1) bnsf_a, round(count_if(rr='BNSF' and y>=2023)/3,1) bnsf_b,
  round(count_if(rr not in ('UP','BNSF') and y<=2017)/3,1) pass_a, round(count_if(rr not in ('UP','BNSF') and y>=2023)/3,1) pass_b
from f group by 1 order by up_b - up_a desc limit 12;

-- [q12] statement 13
-- FRA casualties: trespasser deaths by what the person was doing (lying, walking, sitting/standing), by railroad and year, 2010-2025
-- To see whether UP's rise is people lying on the track, and when it started
select RAILROAD_CODE rr, INCIDENT_YEAR yr, count(*) n,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Lay%' or PHYSICAL_ACT_CIRCUMSTANCES ilike 'Ly%') laying,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Walk%') walking,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Sit%' or PHYSICAL_ACT_CIRCUMSTANCES ilike 'Stand%') sit_stand,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES is null or PHYSICAL_ACT_CIRCUMSTANCES ilike '%other%' or PHYSICAL_ACT_CIRCUMSTANCES ilike '%unknown%') other_unk,
  listagg(distinct iff(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Lay%' or PHYSICAL_ACT_CIRCUMSTANCES ilike 'Ly%', PHYSICAL_ACT_CIRCUMSTANCES, null), ',') lay_label
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS') and INCIDENT_YEAR between 2010 and 2025
group by 1,2 order by 1,2;

-- [q13] statement 14
-- Slave voyages: trap check. Fill rates of the columns a story would lean on, totals of the editors' estimates,
-- impossible values (more landed than embarked, death share outside 0-1), non-numeric text in number columns
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC)
select count(*) n,
  count_if(try_to_number(SLAXIMP) is not null) slaximp_n, sum(try_to_number(SLAXIMP)) slaximp_sum,
  count_if(try_to_number(SLAMIMP) is not null) slamimp_n, sum(try_to_number(SLAMIMP)) slamimp_sum,
  count_if(try_to_number(TSLAVESD) is not null) tslavesd_n, count_if(try_to_number(SLAARRIV) is not null) slaarriv_n,
  count_if(try_to_double(VYMRTRAT) is not null) vymrtrat_n, count_if(try_to_double(VYMRTRAT) < 0 or try_to_double(VYMRTRAT) > 1) vymrtrat_bad,
  count_if(try_to_number(SLAMIMP) > try_to_number(SLAXIMP)) landed_gt_embarked,
  count_if(nullif(trim(SLAXIMP),'') is not null and try_to_number(SLAXIMP) is null) slaximp_nonnum,
  listagg(distinct iff(nullif(trim(SLAXIMP),'') is not null and try_to_number(SLAXIMP) is null, SLAXIMP, null), '|') slaximp_nonnum_vals,
  count_if(nullif(trim(PTDEPIMP),'') is not null) ptdep_n, count_if(nullif(trim(MJSLPTIMP),'') is not null) mjslpt_n,
  count_if(nullif(trim(NATINIMP),'') is not null) natinimp_n, count_if(nullif(trim(OWNERA),'') is not null) ownera_n,
  count_if(nullif(trim(YEARDEP),'') is not null) yeardep_n, count_if(nullif(trim(YEARAM),'') is not null) yearam_n,
  count_if(try_to_number(YEARAM) >= 1808) yearam_1808on,
  listagg(distinct FATE4, ',') fate4_vals, listagg(distinct XMIMPFLAG, ',') xmimpflag_vals, count(distinct _INGESTED_AT) ingests
from t;

-- [q14] statement 15
-- Slave voyages: label the North American departure ports (codes need a lookup that is not in the warehouse).
-- Each port code that starts with 2 (mainland North America): voyages, years, flags, commonest owner and captain, captives embarked
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC where left(PTDEPIMP,1)='2')
select PTDEPIMP port, max(DEPTREGIMP) reg, count(*) voyages, min(try_to_number(YEARAM)) y0, max(try_to_number(YEARAM)) y1,
  count_if(try_to_number(YEARAM) >= 1808) v_1808on, mode(NATINIMP) flag, mode(OWNERA) top_owner, mode(CAPTAINA) top_captain,
  round(sum(try_to_number(SLAXIMP))) embarked, count_if(OWNERA ilike '%wolf%' or OWNERB ilike '%wolf%') dewolf_like, count_if(OWNERA ilike 'Brown,%' or OWNERB ilike 'Brown,%') brown_like
from t group by 1 order by voyages desc limit 20;

-- [q13b] statement 16
-- RERUN of q13 without _INGESTED_AT (this table has no lineage column; q13 failed on it)
-- Slave voyages: trap check. Fill rates of the columns a story would lean on, totals of the editors' estimates,
-- impossible values (more landed than embarked, death share outside 0-1), non-numeric text in number columns
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC)
select count(*) n,
  count_if(try_to_number(SLAXIMP) is not null) slaximp_n, sum(try_to_number(SLAXIMP)) slaximp_sum,
  count_if(try_to_number(SLAMIMP) is not null) slamimp_n, sum(try_to_number(SLAMIMP)) slamimp_sum,
  count_if(try_to_number(TSLAVESD) is not null) tslavesd_n, count_if(try_to_number(SLAARRIV) is not null) slaarriv_n,
  count_if(try_to_double(VYMRTRAT) is not null) vymrtrat_n, count_if(try_to_double(VYMRTRAT) < 0 or try_to_double(VYMRTRAT) > 1) vymrtrat_bad,
  count_if(try_to_number(SLAMIMP) > try_to_number(SLAXIMP)) landed_gt_embarked,
  count_if(nullif(trim(SLAXIMP),'') is not null and try_to_number(SLAXIMP) is null) slaximp_nonnum,
  listagg(distinct iff(nullif(trim(SLAXIMP),'') is not null and try_to_number(SLAXIMP) is null, SLAXIMP, null), '|') slaximp_nonnum_vals,
  count_if(nullif(trim(PTDEPIMP),'') is not null) ptdep_n, count_if(nullif(trim(MJSLPTIMP),'') is not null) mjslpt_n,
  count_if(nullif(trim(NATINIMP),'') is not null) natinimp_n, count_if(nullif(trim(OWNERA),'') is not null) ownera_n,
  count_if(nullif(trim(YEARDEP),'') is not null) yeardep_n, count_if(nullif(trim(YEARAM),'') is not null) yearam_n,
  count_if(try_to_number(YEARAM) >= 1808) yearam_1808on,
  listagg(distinct FATE4, ',') fate4_vals, listagg(distinct XMIMPFLAG, ',') xmimpflag_vals
from t;

-- [q15] statement 17
-- Slave voyages: time. Voyages that sailed from mainland North American ports (codes starting 2), by decade of arrival 1780-1869,
-- where they took the captives (broad landing region), captives embarked (editors' estimate); US-flag voyages; voyages landing in mainland North America
with t as (select floor(try_to_number(YEARAM)/10)*10 dec, left(PTDEPIMP,1)='2' us_dep, NATINIMP='9' us_flag, MJSELIMP1 land1,
             try_to_number(SLAXIMP) emb, try_to_number(SLAMIMP) lan
           from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC where try_to_number(YEARAM) >= 1780)
select dec, count(*) all_voy, count_if(us_dep) us_dep_voy, round(sum(iff(us_dep, emb, 0))) us_dep_emb,
  count_if(us_dep and land1='30000') us_to_carib, count_if(us_dep and land1='20000') us_to_na, count_if(us_dep and land1='50000') us_to_brazil,
  count_if(us_dep and land1='40000') us_to_spmain, count_if(us_dep and (land1 is null or land1 not in ('20000','30000','40000','50000'))) us_to_other,
  count_if(us_flag) usflag_voy, count_if(us_flag and not us_dep) usflag_not_usdep,
  count_if(land1='20000') land_na_voy, round(sum(iff(land1='20000', lan, 0))) land_na_captives
from t group by 1 order by 1;

-- [q16] statement 18
-- Slave voyages: peer comparison inside the same era. Voyages arriving 1850-1866, by where they sailed from (broad region):
-- captives per voyage, share whose owners' goal was thwarted by people (FATE4=3, mostly captures), share delivered (FATE4=1), recorded death share
with t as (select case left(PTDEPIMP,1) when '2' then 'N America' when '3' then 'Caribbean' when '5' then 'Brazil' when '1' then 'Europe' else 'other/unknown' end dep,
             try_to_number(SLAXIMP) emb, try_to_number(SLAMIMP) lan, FATE4, try_to_double(VYMRTRAT) mort, MJSELIMP1 land1
           from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC where try_to_number(YEARAM) between 1850 and 1866)
select dep, count(*) voy, round(sum(emb)) emb, round(avg(emb)) emb_per_voy, round(median(emb)) med_emb, round(sum(lan)) landed,
  count_if(FATE4='1') delivered, count_if(FATE4='3') thwarted_people, count_if(FATE4='2') thwarted_nature, count_if(FATE4='4' or FATE4 is null) unknown,
  count_if(mort is not null) mort_n, round(avg(mort),3) mort_avg, count_if(land1='30000') to_carib, count_if(land1='50000') to_brazil
from t group by 1 order by voy desc;

-- [q17] statement 19
-- Slave voyages: name the 1850s-60s US departure ports. Famous late voyages (Erie, Wanderer, Clotilda, Nightingale) show which code is which port;
-- plus every North American port code with voyages arriving 1850-1866
select 'famous' k, SHIPNAME, CAPTAINA, YEARAM, PTDEPIMP, MJSLPTIMP, SLAXIMP, SLAMIMP, FATE4, VOYAGEID
from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
where try_to_number(YEARAM) >= 1850 and (SHIPNAME ilike any ('Erie%','Wanderer%','Clotild%','Nightingale%') or CAPTAINA ilike any ('Gordon, Nath%','Foster, Wil%','Corrie%'))
union all
select 'port', PTDEPIMP, max(DEPTREGIMP), count(*)::varchar, round(sum(try_to_number(SLAXIMP)))::varchar, min(YEARAM), max(YEARAM), count_if(FATE4='3')::varchar, count_if(FATE4='1')::varchar, listagg(distinct SHIPNAME, ', ')
from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
where try_to_number(YEARAM) between 1850 and 1866 and left(PTDEPIMP,1)='2' group by PTDEPIMP
order by 1, 4 desc;

-- [q18] statement 20
-- FRA casualties: same months across years. Trespasser deaths January-May, 2019-2026, for UP, BNSF, CSX, NS and everyone
select INCIDENT_YEAR yr, count_if(RAILROAD_CODE='UP') up, count_if(RAILROAD_CODE='BNSF') bnsf, count_if(RAILROAD_CODE='CSX') csx, count_if(RAILROAD_CODE='NS') ns,
  count_if(RAILROAD_CODE='ATK') atk, count(*) all_rr
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and INCIDENT_YEAR between 2019 and 2026 and month(DATE) between 1 and 5
group by 1 order by 1;

-- [q19] statement 21
-- Slave voyages: after the US ban (voyage began 1808 or later by YEARDEP; also arrival 1809 or later), voyages that sailed from mainland North American ports:
-- count, captives embarked and landed (editors' estimates), how they ended (FATE4), and voyages that landed captives in mainland North America, split by FATE4
with t as (select try_to_number(YEARDEP) yd, try_to_number(YEARAM) ya, left(PTDEPIMP,1)='2' us_dep, MJSELIMP1 land1, FATE4,
             try_to_number(SLAXIMP) emb, try_to_number(SLAMIMP) lan
           from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC)
select 'usdep_yd1808' k, count(*) voy, round(sum(emb)) emb, round(sum(lan)) lan, count_if(FATE4='1') f1, count_if(FATE4='2') f2, count_if(FATE4='3') f3, count_if(FATE4='4') f4, min(yd) y0, max(yd) y1 from t where us_dep and yd >= 1808
union all select 'usdep_ya1809', count(*), round(sum(emb)), round(sum(lan)), count_if(FATE4='1'), count_if(FATE4='2'), count_if(FATE4='3'), count_if(FATE4='4'), min(ya), max(ya) from t where us_dep and ya >= 1809
union all select 'usdep_1700_1807', count(*), round(sum(emb)), round(sum(lan)), count_if(FATE4='1'), count_if(FATE4='2'), count_if(FATE4='3'), count_if(FATE4='4'), min(ya), max(ya) from t where us_dep and ya between 1700 and 1807
union all select 'landNA_ya1809', count(*), round(sum(emb)), round(sum(lan)), count_if(FATE4='1'), count_if(FATE4='2'), count_if(FATE4='3'), count_if(FATE4='4'), min(ya), max(ya) from t where land1='20000' and ya >= 1809
union all select 'yd_vs_ya', count_if(yd is null), count_if(yd > ya), count_if(ya - yd > 2), null, null, null, null, null, null from t;

-- [q20] statement 22
-- FRA casualties: UP vs BNSF inside the same states. States where both report trespasser deaths; yearly avg 2015-2017 vs 2023-2025
with f as (select RAILROAD_CODE rr, STATE_NAME st, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF') and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
s as (select st, count_if(rr='UP' and y<=2017)/3 up_a, count_if(rr='UP' and y>=2023)/3 up_b, count_if(rr='BNSF' and y<=2017)/3 bn_a, count_if(rr='BNSF' and y>=2023)/3 bn_b from f group by 1),
shared as (select * from s where up_a+up_b > 0 and bn_a+bn_b > 0)
select 'shared_total' k, count(*)::varchar st, round(sum(up_a),1) up_a, round(sum(up_b),1) up_b, round(sum(bn_a),1) bn_a, round(sum(bn_b),1) bn_b,
  count_if(up_b-up_a > bn_b-bn_a) up_rose_more, round(median(up_b-up_a),2) med_up_change, round(median(bn_b-bn_a),2) med_bn_change from shared
union all select * from (select 'state', st, round(up_a,1), round(up_b,1), round(bn_a,1), round(bn_b,1), null, null, null from shared order by up_b+bn_b desc limit 14);
