-- deep3 / g40: proper look at five glance-only tables, 2026-09-24
-- Tables: ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS, ENVIRONMENT__FED_USGS_WBD_HUC8,
--         ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS, ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS,
--         ENVIRONMENT__XC_OWID_CO2
-- Door: Python (connect/db.py) via g40/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g40/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- column names and types for my 5 tables plus the ICIS-Air / RCRA tables I may join to
select table_name, listagg(column_name || ':' || data_type, ', ') within group (order by ordinal_position) cols, max(row_count) rc
from (select c.table_name, c.column_name, c.data_type, c.ordinal_position, t.row_count
      from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
      join LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t on t.table_schema=c.table_schema and t.table_name=c.table_name
      where c.table_schema='ENVIRONMENT' and c.table_name in (
        'ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS','ENVIRONMENT__FED_USGS_WBD_HUC8','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS',
        'ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS','ENVIRONMENT__XC_OWID_CO2','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES',
        'ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY',
        'ENVIRONMENT__FED_EPA_RCRA_FACILITIES','ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS'))
group by 1 order by 1;

-- [q02] statement 2
-- ICIS-Air informal actions: keys, flags, enforcement types, sentinel dates
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS)
select 'profile' k, count(*)::text a, count(distinct ACTIVITY_ID)::text b, count(distinct PGM_SYS_ID)::text c, count(distinct ENF_IDENTIFIER)::text d,
  count(distinct PGM_SYS_ID||'|'||ACTIVITY_ID)::text e,
  count_if(ACHIEVED_DATE is null)::text || ' null / ' || count_if(year(ACHIEVED_DATE)<1970)::text || ' pre1970 / ' || count_if(ACHIEVED_DATE>'2026-09-24')::text || ' future' f,
  min(iff(year(ACHIEVED_DATE)>=1970, ACHIEVED_DATE, null))::text || ' to ' || max(iff(ACHIEVED_DATE<='2026-09-24', ACHIEVED_DATE, null))::text g
from t
union all select 'flag', STATE_EPA_FLAG, count(*)::text, count(distinct PGM_SYS_ID)::text, null, null, null, null from t group by 2
union all select 'official', OFFICIAL_FLG, count(*)::text, null, null, null, null, null from t group by 2
union all select * from (select 'enftype', ENF_TYPE_CODE, count(*)::text, any_value(ENF_TYPE_DESC), count_if(STATE_EPA_FLAG='E')::text, null, null, null from t group by 2 order by count(*) desc limit 15)
union all select * from (select 'baddate', ACHIEVED_DATE::text, count(*)::text, null, null, null, null, null from t where year(ACHIEVED_DATE)<1970 or ACHIEVED_DATE>'2026-09-24' group by 2 order by count(*) desc limit 8)
union all select * from (select 'bigenf', ENF_IDENTIFIER, count(*)::text, count(distinct PGM_SYS_ID)::text, count(distinct ACHIEVED_DATE)::text, min(ACHIEVED_DATE)::text||'..'||max(ACHIEVED_DATE)::text, any_value(ENF_TYPE_DESC), count(distinct ACTIVITY_ID)::text from t group by 2 order by count(*) desc limit 8);

-- [q03] statement 3
-- Time: informal (ACHIEVED_DATE) and formal (SETTLEMENT_ENTERED_DATE) air actions per year by agency, full year and Jan-Jul only
with i as (select year(ACHIEVED_DATE) y, STATE_EPA_FLAG f, count(distinct ACTIVITY_ID) inf_acts, count(*) inf_rows,
             count(distinct iff(month(ACHIEVED_DATE)<=7, ACTIVITY_ID, null)) inf_jj
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
           where ACHIEVED_DATE between '2005-01-01' and '2026-07-31' group by 1,2),
fa as (select year(SETTLEMENT_ENTERED_DATE) y, STATE_EPA_FLAG f, count(distinct ACTIVITY_ID) f_acts,
             count(distinct iff(month(SETTLEMENT_ENTERED_DATE)<=7, ACTIVITY_ID, null)) f_jj,
             sum(iff(month(SETTLEMENT_ENTERED_DATE)<=7, PENALTY_AMOUNT, 0)) f_pen_jj, max(SETTLEMENT_ENTERED_DATE) fmax
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
           where SETTLEMENT_ENTERED_DATE between '2005-01-01' and '2026-09-24' group by 1,2)
select coalesce(i.y,fa.y) y, coalesce(i.f,fa.f) f, inf_acts, inf_rows, inf_jj, f_acts, f_jj, round(f_pen_jj) f_pen_jj, fmax
from i full outer join fa on i.y=fa.y and i.f=fa.f
order by 2,1;

-- [q04] statement 4
-- Peer comparison by state: per facility informal vs formal counts since 2010; how often 5+ informal actions end with zero formal actions
with inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf, count(distinct ACHIEVED_DATE) d_inf, min(ACHIEVED_DATE) f1, max(ACHIEVED_DATE) f2
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
             where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' group by 1),
frm as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_frm
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
        where SETTLEMENT_ENTERED_DATE between '2010-01-01' and '2026-09-24' group by 1),
fac as (select PGM_SYS_ID, STATE, AIR_POLLUTANT_CLASS_CODE cls from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
j as (select coalesce(fac.STATE,'??') st, inf.*, coalesce(frm.n_frm,0) n_frm, fac.cls, fac.PGM_SYS_ID is not null landed
      from inf left join frm using (PGM_SYS_ID) left join fac using (PGM_SYS_ID))
select st, count(*) fac_inf, count_if(landed) landed, sum(n_inf) inf_acts, sum(n_frm) frm_acts_of_those,
  count_if(n_frm=0) fac_zero_formal, round(100*count_if(n_frm=0)/count(*),1) pct_zero,
  count_if(n_inf>=5) fac_5plus, count_if(n_inf>=5 and n_frm=0) fac_5plus_zero,
  round(100*count_if(n_inf>=5 and n_frm=0)/nullif(count_if(n_inf>=5),0),1) pct_5plus_zero,
  max(n_inf) max_inf, median(n_inf) med_inf,
  count_if(cls='MAJ') maj, count_if(cls='MAJ' and n_inf>=5 and n_frm=0) maj_5plus_zero
from j group by 1 order by fac_5plus desc;

-- [q05] statement 5
-- Facilities: most informal actions since 2010 with zero formal actions since 2010, plus the top 8 overall; with class, status, HPV, violation rows
with inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf, count(distinct ACHIEVED_DATE) d_inf, min(ACHIEVED_DATE) f1, max(ACHIEVED_DATE) f2,
               listagg(distinct STATE_EPA_FLAG,'') ag, count_if(ENF_TYPE_CODE='NOV') nov
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
             where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' group by 1),
frm as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_frm, count(distinct iff(SETTLEMENT_ENTERED_DATE>='2010-01-01', ACTIVITY_ID, null)) n_frm10,
          max(SETTLEMENT_ENTERED_DATE) last_frm
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
vh as (select PGM_SYS_ID, count(*) viol_rows, count(HPV_DAYZERO_DATE) hpv_rows, count_if(HPV_DAYZERO_DATE is not null and HPV_RESOLVED_DATE is null) hpv_open,
         max(EARLIEST_FRV_DETERM_DATE) last_frv
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY group by 1),
fac as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op, CURRENT_HPV, NAICS_CODES, LOCAL_CONTROL_REGION_NAME lcr
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
j as (select inf.*, coalesce(frm.n_frm10,0) n_frm10, coalesce(frm.n_frm,0) n_frm_all, frm.last_frm, vh.viol_rows, vh.hpv_rows, vh.hpv_open, vh.last_frv, fac.*
      from inf left join frm using (PGM_SYS_ID) left join vh using (PGM_SYS_ID) left join fac using (PGM_SYS_ID))
select * from (select 'zero_formal' k, * from j where n_frm_all=0 order by n_inf desc limit 30)
union all select * from (select 'top_all' k, * from j order by n_inf desc limit 8);

-- [q06] statement 6
-- Peer group: every Bay Area AQMD facility with 20+ informal actions since 2010; formal actions and penalties (one penalty per action) since 2010; HPV rows
with fac as (select PGM_SYS_ID, FACILITY_NAME, CITY, AIR_POLLUTANT_CLASS_CODE cls, NAICS_CODES
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where LOCAL_CONTROL_REGION_NAME like 'Bay Area%'),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf, count(distinct ACHIEVED_DATE) d_inf,
          count(distinct iff(ACHIEVED_DATE>='2019-01-01', ACTIVITY_ID, null)) n_inf19
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1),
fa1 as (select PGM_SYS_ID, ACTIVITY_ID, max(SETTLEMENT_ENTERED_DATE) d, max(PENALTY_AMOUNT) pen, any_value(STATE_EPA_FLAG) ag
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
        where SETTLEMENT_ENTERED_DATE between '2010-01-01' and '2026-09-24' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1,2),
frm as (select PGM_SYS_ID, count(*) n_frm, count_if(d>='2019-01-01') n_frm19, round(sum(pen)) pen, max(d) last_frm, listagg(distinct ag,'') ags from fa1 group by 1),
vh as (select PGM_SYS_ID, count(HPV_DAYZERO_DATE) hpv, count_if(HPV_DAYZERO_DATE is not null and HPV_RESOLVED_DATE is null) hpv_open
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1)
select fac.FACILITY_NAME, fac.CITY, fac.cls, fac.NAICS_CODES, inf.n_inf, inf.d_inf, inf.n_inf19, coalesce(frm.n_frm,0) n_frm, coalesce(frm.n_frm19,0) n_frm19,
  frm.pen, frm.last_frm, frm.ags, round(100*coalesce(frm.n_frm,0)/inf.n_inf,1) frm_per_100_inf, vh.hpv, vh.hpv_open
from inf join fac using (PGM_SYS_ID) left join frm using (PGM_SYS_ID) left join vh using (PGM_SYS_ID)
where inf.n_inf >= 20 order by inf.n_inf desc;

-- [q07] statement 7
-- Tesla Fremont check: NOVs by year, every formal action on file, any second air ID for the plant, EPA civil cases on its FRS registry ID
with ids as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, STREET_ADDRESS, AIR_POLLUTANT_CLASS_CODE cls
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
             where (FACILITY_NAME ilike '%TESLA%' and STATE='CA') or REGISTRY_ID='110000482898'),
inf as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from ids)),
frm as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from ids)),
vh as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where PGM_SYS_ID='CABAA00006001A1438')
select 'id' k, PGM_SYS_ID a, REGISTRY_ID b, FACILITY_NAME c, STREET_ADDRESS d, cls e,
  (select count(*) from inf where inf.PGM_SYS_ID=ids.PGM_SYS_ID)::text f, (select count(*) from frm where frm.PGM_SYS_ID=ids.PGM_SYS_ID)::text g from ids
union all select 'inf_year', PGM_SYS_ID, year(ACHIEVED_DATE)::text, count(distinct ACTIVITY_ID)::text, count(distinct ACHIEVED_DATE)::text, listagg(distinct ENF_TYPE_CODE,'|'), listagg(distinct STATE_EPA_FLAG,''), null from inf group by 2,3
union all select 'formal', PGM_SYS_ID, SETTLEMENT_ENTERED_DATE::text, ENF_TYPE_DESC, PENALTY_AMOUNT::text, STATE_EPA_FLAG, ENF_IDENTIFIER, ACTIVITY_ID from frm
union all select 'hpv_year', 'CABAA00006001A1438', year(HPV_DAYZERO_DATE)::text, count(*)::text, count_if(HPV_RESOLVED_DATE is null)::text, listagg(distinct ENF_RESPONSE_POLICY_CODE,'|'), left(listagg(distinct POLLUTANT_DESCS,'|'),120), left(listagg(distinct PROGRAM_CODES,'|'),120) from vh group by 3
union all select 'fec_case', CASE_NUMBER, ACTIVITY_ID, FACILITY_NAME, LOCATION_ADDRESS, CITY, REGISTRY_ID, null
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES where REGISTRY_ID='110000482898' or (FACILITY_NAME ilike '%TESLA%' and STATE_CODE='CA');

-- [q08] statement 8
-- Hostile check on "many NOVs, zero formal": for facilities with 10+ informal actions since 2010 and no formal action on their own air ID,
-- look for formal air actions on a sibling air ID with the same FRS registry ID, and EPA civil cases on that registry ID
with fac as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' group by 1 having count(distinct ACTIVITY_ID)>=10),
frm_id as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n, max(SETTLEMENT_ENTERED_DATE) last_d, sum(PENALTY_AMOUNT) pen
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
zero as (select inf.PGM_SYS_ID, inf.n_inf, fac.REGISTRY_ID, fac.FACILITY_NAME, fac.CITY, fac.STATE, fac.cls
         from inf join fac using (PGM_SYS_ID) left join frm_id using (PGM_SYS_ID) where frm_id.PGM_SYS_ID is null),
sib as (select z.PGM_SYS_ID, count(distinct f2.PGM_SYS_ID) sib_ids, sum(fr.n) sib_formal, max(fr.last_d) sib_last, sum(fr.pen) sib_pen
        from zero z join fac f2 on f2.REGISTRY_ID=z.REGISTRY_ID and f2.PGM_SYS_ID<>z.PGM_SYS_ID
        left join frm_id fr on fr.PGM_SYS_ID=f2.PGM_SYS_ID group by 1),
fec as (select z.PGM_SYS_ID, count(distinct c.CASE_NUMBER) cases, listagg(distinct c.CASE_NUMBER, ' ') case_list
        from zero z join LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES c on c.REGISTRY_ID=z.REGISTRY_ID group by 1)
select 'summary' k, count(*)::text a, count_if(sib.sib_formal>0)::text b, count_if(fec.cases>0)::text c,
  count_if(coalesce(sib.sib_formal,0)=0 and coalesce(fec.cases,0)=0)::text d, count_if(z.REGISTRY_ID is null)::text e, null f, null g, null h
from zero z left join sib using (PGM_SYS_ID) left join fec using (PGM_SYS_ID)
union all
select * from (select 'row', z.FACILITY_NAME, z.STATE, z.n_inf::text, z.cls, coalesce(sib.sib_formal,0)::text, sib.sib_last::text, coalesce(fec.cases,0)::text, left(fec.case_list,80)
from zero z left join sib using (PGM_SYS_ID) left join fec using (PGM_SYS_ID) order by z.n_inf desc limit 30);

-- [q09] statement 9
-- Program subparts: keys, duplicates, land rate, and how completely each state fills subparts for its major sources
with s as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS),
fac as (select PGM_SYS_ID, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
sp as (select distinct PGM_SYS_ID from s)
select 'profile' k, count(*)::text a, count(distinct PGM_SYS_ID)::text b, count(distinct AIR_PROGRAM_SUBPART_CODE)::text c,
  count(distinct PGM_SYS_ID||'|'||AIR_PROGRAM_SUBPART_CODE)::text d, count_if(AIR_PROGRAM_SUBPART_CODE is null or trim(AIR_PROGRAM_SUBPART_CODE)='')::text e,
  count_if(not startswith(AIR_PROGRAM_SUBPART_CODE, PROGRAM_CODE))::text f,
  (select count(*) from sp join fac using (PGM_SYS_ID))::text g
from s
union all
select * from (select 'state_maj_op', STATE, count(*)::text, count_if(sp.PGM_SYS_ID is not null)::text,
  round(100*count_if(sp.PGM_SYS_ID is not null)/count(*),1)::text, null, null, null
from fac left join sp using (PGM_SYS_ID) where cls='MAJ' and op='OPR' group by 2 order by round(100*count_if(sp.PGM_SYS_ID is not null)/count(*),1) asc limit 60)
union all
select * from (select 'top_sub', AIR_PROGRAM_SUBPART_CODE, count(distinct PGM_SYS_ID)::text, left(any_value(AIR_PROGRAM_SUBPART_DESC),90), null, null, null, null
from s group by 2 order by count(distinct PGM_SYS_ID) desc limit 12);

-- [q10] statement 10
-- Industry peers from the subparts table: every facility tagged with the auto/light-truck surface coating rule (MACT IIII),
-- NOVs and formal actions since 2019 (formal counted across all air IDs sharing the FRS registry ID); plus Tesla's own tags
with sub as (select distinct PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS
             where AIR_PROGRAM_SUBPART_CODE like 'CAAMACTIIII%'),
fac as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
grp as (select f.* from fac f where f.PGM_SYS_ID in (select PGM_SYS_ID from sub) or f.REGISTRY_ID='110000482898'),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf19 from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from grp) group by 1),
frm_reg as (select f.REGISTRY_ID, count(distinct a.ACTIVITY_ID) n_frm19, sum(a.PENALTY_AMOUNT) pen19
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join fac f using (PGM_SYS_ID)
            where a.SETTLEMENT_ENTERED_DATE >= '2019-01-01' and f.REGISTRY_ID in (select REGISTRY_ID from grp) group by 1)
select 'peer' k, g.FACILITY_NAME, g.CITY, g.STATE, g.cls, g.op, coalesce(inf.n_inf19,0) n_inf19, coalesce(fr.n_frm19,0) n_frm19_registry, round(fr.pen19) pen19_registry,
  iff(g.PGM_SYS_ID in (select PGM_SYS_ID from sub),'IIII','not tagged') tag
from grp g left join inf using (PGM_SYS_ID) left join frm_reg fr on fr.REGISTRY_ID=g.REGISTRY_ID
order by n_inf19 desc;

-- [q11] statement 11
-- RCRA NAICS: keys, duplicates, code lengths, and what share of each state's RCRA sites carry any industry code
with n as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS),
f as (select ACTIVITY_LOCATION st, ID_NUMBER from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES group by 1,2),
ns as (select distinct ID_NUMBER from n)
select 'profile' k, count(*)::text a, count(distinct ID_NUMBER)::text b, count(distinct FACILITY_NAICS_ID)::text c,
  count(distinct ID_NUMBER||'|'||NAICS_CODE)::text d, count(distinct _SOURCE_RUN_ID)::text e,
  count_if(NAICS_CODE is null or trim(NAICS_CODE)='')::text f, count_if(ACTIVITY_LOCATION <> left(ID_NUMBER,2))::text g,
  (select count(*) from ns where ID_NUMBER in (select ID_NUMBER from f))::text h
from n
union all select 'len', length(NAICS_CODE)::text, count(*)::text, count(distinct NAICS_CODE)::text, left(listagg(distinct NAICS_CODE,' '),60), null, null, null, null from n group by 2
union all select * from (select 'state', f.st, count(*)::text, count_if(ns.ID_NUMBER is not null)::text,
  round(100*count_if(ns.ID_NUMBER is not null)/count(*),1)::text, null, null, null, null
  from f left join ns using (ID_NUMBER) group by 2 order by count(*) desc limit 25)
union all select * from (select 'codes_per_site', c::text, count(*)::text, null, null, null, null, null, null
  from (select ID_NUMBER, count(*) c from n group by 1) group by 2 order by 2::int limit 8);

-- [q12] statement 12
-- WBD HUC8: confirm it is a one-row-per-watershed lookup; check units (acres vs sq km vs map-software area) and cross-border rows
with h as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WBD_HUC8)
select 'profile' k, count(*)::text a, count(distinct HUC8)::text b, listagg(distinct length(HUC8)::text,',')::text c,
  count_if(STATES ilike '%CN%' or STATES ilike '%MX%')::text d, count(distinct _SOURCE_RUN_ID)::text e,
  count_if(SOURCE_FEATURE_ID=0)::text f,
  round(min(AREA_ACRES/nullif(AREA_SQ_KM,0)),3)::text||'..'||round(max(AREA_ACRES/nullif(AREA_SQ_KM,0)),3)::text g,
  round(min(SHAPE_AREA/nullif(AREA_SQ_KM*1e6,0)),2)::text||'..'||round(max(SHAPE_AREA/nullif(AREA_SQ_KM*1e6,0)),2)::text h
from h
union all select * from (select 'by_region', left(HUC8,2), count(*)::text, round(median(SHAPE_AREA/nullif(AREA_SQ_KM*1e6,0)),2)::text,
  count_if(STATES ilike '%CN%' or STATES ilike '%MX%')::text, left(any_value(STATES),20), null, round(sum(AREA_SQ_KM))::text, null from h group by 2 order by 2);

-- [q13] statement 13
-- OWID CO2: duplicates, text-number parse, zeros, repeated values, which rows are regions not countries
with o as (select ENTITY, CODE, YEAR, ANNUAL_CO_EMISSIONS v, try_to_number(YEAR) y, try_to_double(ANNUAL_CO_EMISSIONS) x from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2)
select 'profile' k, count(*)::text a, count(distinct ENTITY)::text b, count(distinct ENTITY||'|'||YEAR)::text c,
  min(y)::text||'..'||max(y)::text d, count_if(y is null)::text e, count_if(x is null and v is not null)::text f,
  count_if(x=0)::text||' zero / '||count_if(x<0)::text||' neg' g, count_if(CODE is null or trim(CODE)='')::text h, count_if(CODE like 'OWID%')::text i
from o
union all select * from (select 'repeat', v, count(*)::text, count(distinct ENTITY)::text, min(y)::text||'..'||max(y)::text, left(listagg(distinct ENTITY,'|'),80), null, null, null, null
  from o group by 2 order by count(*) desc limit 6)
union all select * from (select 'nocode', ENTITY, count(*)::text, min(y)::text||'..'||max(y)::text, null, null, null, null, null, null from o where CODE is null or trim(CODE)='' group by 2 order by 2 limit 40)
union all select * from (select 'owid', ENTITY, CODE, count(*)::text, null, null, null, null, null, null from o where CODE like 'OWID%' group by 2,3 order by 2);

-- [q14] statement 14
-- OWID CO2 time check: countries only (3-letter code), top 20 emitters in 2024, change vs 2019 and 2023; world and sum-of-countries for the double-count test
with o as (select ENTITY, CODE, try_to_number(YEAR) y, try_to_double(ANNUAL_CO_EMISSIONS) x from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2),
c as (select ENTITY, CODE, max(iff(y=2024,x,null)) e24, max(iff(y=2023,x,null)) e23, max(iff(y=2019,x,null)) e19, max(iff(y=2005,x,null)) e05
      from o where length(CODE)=3 group by 1,2)
select * from (select 'top' k, ENTITY, round(e24/1e6,1) mt24, round(100*(e24/e19-1),1) pct_vs19, round(100*(e24/e23-1),1) pct_vs23, round(100*(e24/e05-1),1) pct_vs05 from c where e24 is not null order by e24 desc limit 20)
union all select 'sum_countries', count(*)::text, round(sum(e24)/1e6,1), null, null, null from c where e24 is not null
union all select 'world', 'OWID_WRL', round(max(iff(y=2024,x,null))/1e6,1), round(100*(max(iff(y=2024,x,null))/max(iff(y=2019,x,null))-1),1), round(100*(max(iff(y=2024,x,null))/max(iff(y=2023,x,null))-1),1), null from o where CODE='OWID_WRL'
union all select 'bunkers', ENTITY, round(max(iff(y=2024,x,null))/1e6,1), round(100*(max(iff(y=2024,x,null))/max(iff(y=2019,x,null))-1),1), null, null from o where ENTITY in ('International aviation','International shipping','Kuwaiti Oil Fires (GCP)') group by 2;

-- [q15] statement 15
-- (rerun of q14 after a divide-by-zero on zero-emission base years) OWID CO2 time check: countries only (3-letter code), top 20 emitters in 2024, change vs 2019 and 2023; world and sum-of-countries for the double-count test
with o as (select ENTITY, CODE, try_to_number(YEAR) y, try_to_double(ANNUAL_CO_EMISSIONS) x from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2),
c as (select ENTITY, CODE, max(iff(y=2024,x,null)) e24, max(iff(y=2023,x,null)) e23, max(iff(y=2019,x,null)) e19, max(iff(y=2005,x,null)) e05
      from o where length(CODE)=3 group by 1,2)
select * from (select 'top' k, ENTITY, round(e24/1e6,1) mt24, round(100*(e24/nullif(e19,0)-1),1) pct_vs19, round(100*(e24/nullif(e23,0)-1),1) pct_vs23, round(100*(e24/nullif(e05,0)-1),1) pct_vs05 from c where e24 is not null order by e24 desc limit 20)
union all select 'sum_countries', count(*)::text, round(sum(e24)/1e6,1), null, null, null from c where e24 is not null
union all select 'world', 'OWID_WRL', round(max(iff(y=2024,x,null))/1e6,1), round(100*(max(iff(y=2024,x,null))/max(iff(y=2019,x,null))-1),1), round(100*(max(iff(y=2024,x,null))/max(iff(y=2023,x,null))-1),1), null from o where CODE='OWID_WRL'
union all select 'bunkers', ENTITY, round(max(iff(y=2024,x,null))/1e6,1), round(100*(max(iff(y=2024,x,null))/max(iff(y=2019,x,null))-1),1), null, null from o where ENTITY in ('International aviation','International shipping','Kuwaiti Oil Fires (GCP)') group by 2;

-- [q16] statement 16
-- (second rerun of q14: Kuwaiti Oil Fires has a zero base year; every division now zero-safe) OWID CO2 time check:
-- countries only (3-letter code), top 20 emitters in 2024, change vs 2019, 2023 and 2005; world and sum-of-countries for the double-count test
with o as (select ENTITY, CODE, try_to_number(YEAR) y, try_to_double(ANNUAL_CO_EMISSIONS) x from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2),
c as (select ENTITY, CODE, max(iff(y=2024,x,null)) e24, max(iff(y=2023,x,null)) e23, max(iff(y=2019,x,null)) e19, max(iff(y=2005,x,null)) e05
      from o where length(CODE)=3 group by 1,2),
w as (select ENTITY, max(iff(y=2024,x,null)) e24, max(iff(y=2023,x,null)) e23, max(iff(y=2019,x,null)) e19, max(iff(y=2005,x,null)) e05
      from o where CODE='OWID_WRL' or ENTITY in ('International aviation','International shipping','Kuwaiti Oil Fires (GCP)') group by 1)
select * from (select 'top' k, ENTITY, round(e24/1e6,1) mt24, round(100*(e24/nullif(e19,0)-1),1) pct_vs19, round(100*(e24/nullif(e23,0)-1),1) pct_vs23, round(100*(e24/nullif(e05,0)-1),1) pct_vs05 from c where e24 is not null order by e24 desc limit 20)
union all select 'sum_countries', count(*)::text, round(sum(e24)/1e6,1), null, null, null from c where e24 is not null
union all select 'world_or_bunker', ENTITY, round(e24/1e6,1), round(100*(e24/nullif(e19,0)-1),1), round(100*(e24/nullif(e23,0)-1),1), round(100*(e24/nullif(e05,0)-1),1) from w;

-- [q17] statement 17
-- Time by jurisdiction: informal actions (distinct activities) per year 2019-2025 and Jan-May 2024/2025/2026, top 25 issuers; Tesla Fremont share inside Bay Area AQMD
with f as (select PGM_SYS_ID, STATE, LOCAL_CONTROL_REGION_NAME lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
i as (select a.ACTIVITY_ID, a.ACHIEVED_DATE d, year(a.ACHIEVED_DATE) y, month(a.ACHIEVED_DATE) m, a.PGM_SYS_ID,
        case when a.STATE_EPA_FLAG='E' then 'EPA' when a.STATE_EPA_FLAG='L' then coalesce(f.lcr, 'local ' || f.STATE) else 'state ' || f.STATE end jur
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a left join f using (PGM_SYS_ID)
      where a.ACHIEVED_DATE between '2019-01-01' and '2026-07-31')
select * from (select left(jur,45) jur,
  count(distinct iff(y=2019,ACTIVITY_ID,null)) y19, count(distinct iff(y=2020,ACTIVITY_ID,null)) y20, count(distinct iff(y=2021,ACTIVITY_ID,null)) y21,
  count(distinct iff(y=2022,ACTIVITY_ID,null)) y22, count(distinct iff(y=2023,ACTIVITY_ID,null)) y23, count(distinct iff(y=2024,ACTIVITY_ID,null)) y24,
  count(distinct iff(y=2025,ACTIVITY_ID,null)) y25,
  count(distinct iff(y=2024 and m<=5,ACTIVITY_ID,null)) jm24, count(distinct iff(y=2025 and m<=5,ACTIVITY_ID,null)) jm25, count(distinct iff(y=2026 and m<=5,ACTIVITY_ID,null)) jm26,
  count(distinct iff(y=2026 and m in (6,7),ACTIVITY_ID,null)) jj26, count(distinct iff(y=2025 and m in (6,7),ACTIVITY_ID,null)) jj25,
  count(distinct iff(PGM_SYS_ID='CABAA00006001A1438',ACTIVITY_ID,null)) tesla_all, count(distinct ACTIVITY_ID) all_n
from i group by 1 order by all_n desc limit 25)
union all
select 'ALL', count(distinct iff(y=2019,ACTIVITY_ID,null)), count(distinct iff(y=2020,ACTIVITY_ID,null)), count(distinct iff(y=2021,ACTIVITY_ID,null)),
  count(distinct iff(y=2022,ACTIVITY_ID,null)), count(distinct iff(y=2023,ACTIVITY_ID,null)), count(distinct iff(y=2024,ACTIVITY_ID,null)), count(distinct iff(y=2025,ACTIVITY_ID,null)),
  count(distinct iff(y=2024 and m<=5,ACTIVITY_ID,null)), count(distinct iff(y=2025 and m<=5,ACTIVITY_ID,null)), count(distinct iff(y=2026 and m<=5,ACTIVITY_ID,null)),
  count(distinct iff(y=2026 and m in (6,7),ACTIVITY_ID,null)), count(distinct iff(y=2025 and m in (6,7),ACTIVITY_ID,null)),
  count(distinct iff(PGM_SYS_ID='CABAA00006001A1438',ACTIVITY_ID,null)), count(distinct ACTIVITY_ID) from i;

-- [q18] statement 18
-- The series that stops: San Joaquin Valley APCD informal actions by month 2023-2026, vs its formal actions and compliance evaluations by year;
-- and every California air district: operating majors, informal and formal actions by period (is the district in the file at all?)
with f as (select PGM_SYS_ID, STATE, LOCAL_CONTROL_REGION_NAME lcr, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where STATE='CA'),
inf as (select a.ACTIVITY_ID, a.ACHIEVED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.ACHIEVED_DATE between '2019-01-01' and '2026-07-31'),
frm as (select a.ACTIVITY_ID, a.SETTLEMENT_ENTERED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.SETTLEMENT_ENTERED_DATE between '2019-01-01' and '2026-09-24'),
ev as (select a.ACTIVITY_ID, coalesce(try_to_date(a.ACTUAL_END_DATE::text), try_to_date(a.ACTUAL_END_DATE::text,'MM/DD/YYYY')) d, a.STATE_EPA_FLAG ag, f.lcr
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES a join f using (PGM_SYS_ID))
select 'sjv_inf_month' k, to_char(date_trunc('month',d),'YYYY-MM') a, count(distinct ACTIVITY_ID)::text b, listagg(distinct ag,'') c, null d, null e, null f, null g
  from inf where lcr like 'San Joaquin%' and d>='2023-07-01' group by 2
union all select 'sjv_year', y::text, sum(nf)::text, sum(nfr)::text, sum(nev)::text, null, null, null from (
  select year(d) y, count(distinct ACTIVITY_ID) nf, 0 nfr, 0 nev from inf where lcr like 'San Joaquin%' group by 1
  union all select year(d), 0, count(distinct ACTIVITY_ID), 0 from frm where lcr like 'San Joaquin%' group by 1
  union all select year(d), 0, 0, count(distinct ACTIVITY_ID) from ev where lcr like 'San Joaquin%' and d between '2019-01-01' and '2026-09-24' group by 1) group by 1
union all select 'ca_district', left(coalesce(lcr,'(no district)'),50),
  (select count(*) from f f2 where coalesce(f2.lcr,'')=coalesce(x.lcr,'') and f2.cls='MAJ' and f2.op='OPR')::text,
  count(distinct iff(src='i' and year(d) between 2019 and 2023, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2024, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='f' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='e' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text
from (select 'i' src, ACTIVITY_ID, d, lcr from inf union all select 'f', ACTIVITY_ID, d, lcr from frm union all select 'e', ACTIVITY_ID, d, lcr from ev where d between '2019-01-01' and '2026-09-24') x
group by x.lcr;

-- [q19] statement 19
-- (rerun of q18 after a GROUP BY slip) The series that stops: San Joaquin Valley APCD informal actions by month 2023-2026, vs its formal actions
-- and compliance evaluations by year; and every California air district: operating majors, informal and formal actions by period
with f as (select PGM_SYS_ID, STATE, LOCAL_CONTROL_REGION_NAME lcr, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where STATE='CA'),
maj as (select coalesce(lcr,'(no district)') lcr, count(*) n_maj from f where cls='MAJ' and op='OPR' group by 1),
inf as (select a.ACTIVITY_ID, a.ACHIEVED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.ACHIEVED_DATE between '2019-01-01' and '2026-07-31'),
frm as (select a.ACTIVITY_ID, a.SETTLEMENT_ENTERED_DATE d, a.STATE_EPA_FLAG ag, f.lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join f using (PGM_SYS_ID)
        where a.SETTLEMENT_ENTERED_DATE between '2019-01-01' and '2026-09-24'),
ev as (select a.ACTIVITY_ID, coalesce(try_to_date(a.ACTUAL_END_DATE::text), try_to_date(a.ACTUAL_END_DATE::text,'MM/DD/YYYY')) d, a.STATE_EPA_FLAG ag, f.lcr
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES a join f using (PGM_SYS_ID)),
allx as (select 'i' src, ACTIVITY_ID, d, coalesce(lcr,'(no district)') lcr from inf
         union all select 'f', ACTIVITY_ID, d, coalesce(lcr,'(no district)') from frm
         union all select 'e', ACTIVITY_ID, d, coalesce(lcr,'(no district)') from ev where d between '2019-01-01' and '2026-09-24')
select 'sjv_inf_month' k, to_char(date_trunc('month',d),'YYYY-MM') a, count(distinct ACTIVITY_ID)::text b, listagg(distinct ag,'') c, null d, null e, null f, null g
  from inf where lcr like 'San Joaquin%' and d>='2023-07-01' group by 2
union all select 'sjv_year', year(d)::text, count(distinct iff(src='i',ACTIVITY_ID,null))::text, count(distinct iff(src='f',ACTIVITY_ID,null))::text,
  count(distinct iff(src='e',ACTIVITY_ID,null))::text, max(iff(src='i',d,null))::text, max(iff(src='f',d,null))::text, max(iff(src='e',d,null))::text
  from allx where lcr like 'San Joaquin%' group by 2
union all select 'ca_district', left(x.lcr,50), max(maj.n_maj)::text,
  count(distinct iff(src='i' and year(d) between 2019 and 2023, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2024, ACTIVITY_ID, null))::text,
  count(distinct iff(src='i' and year(d)=2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='f' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text,
  count(distinct iff(src='e' and year(d) between 2019 and 2025, ACTIVITY_ID, null))::text
from allx x left join maj on maj.lcr=x.lcr group by 2;

-- [q20] statement 20
-- Subparts trap + clean industry peer group: who carries the auto-coating tag (MACT IIII) by industry code;
-- operating auto/truck assembly plants (NAICS 33611x/336120) with the tag: NOVs since 2019, median and max without Tesla
with sub as (select distinct PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS where AIR_PROGRAM_SUBPART_CODE like 'CAAMACTIIII%'),
fac as (select PGM_SYS_ID, FACILITY_NAME, STATE, NAICS_CODES, AIR_OPERATING_STATUS_CODE op from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where PGM_SYS_ID in (select PGM_SYS_ID from sub)),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from sub) group by 1),
j as (select fac.*, coalesce(inf.n,0) n, (NAICS_CODES like '%33611%' or NAICS_CODES like '%336120%') auto from fac left join inf using (PGM_SYS_ID))
select 'tag_by_industry' k, case when auto then 'auto assembly 33611x/336120' when NAICS_CODES like '%3363%' or NAICS_CODES like '%3362%' then 'auto parts/bodies 3362-3363'
  when NAICS_CODES like '%211%' or NAICS_CODES like '%486%' or NAICS_CODES like '%2212%' then 'oil and gas wells, pipelines, gas utilities'
  when NAICS_CODES like '%2211%' then 'power plants' else 'other' end a, count(*)::text b, null c, null d
from j group by 2
union all select 'auto_peers_operating', count(*)::text, median(iff(PGM_SYS_ID<>'CABAA00006001A1438', n, null))::text,
  max(iff(PGM_SYS_ID<>'CABAA00006001A1438', n, null))::text, sum(iff(PGM_SYS_ID<>'CABAA00006001A1438', n, 0))::text
from j where auto and op='OPR'
union all select * from (select 'auto_top', FACILITY_NAME, STATE, n::text, NAICS_CODES from j where auto and op='OPR' order by n desc limit 5);

-- [q21] statement 21
-- Hostile check on the San Joaquin stop and the South Coast blank: violations (federally reportable, by determination date) and HPVs (by day zero)
-- logged per year for the three biggest California districts, 2019-2026
with f as (select PGM_SYS_ID, LOCAL_CONTROL_REGION_NAME lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
           where STATE='CA' and (LOCAL_CONTROL_REGION_NAME like 'San Joaquin%' or LOCAL_CONTROL_REGION_NAME like 'South Coast%' or LOCAL_CONTROL_REGION_NAME like 'Bay Area%')),
v as (select left(f.lcr,12) d, year(coalesce(v.EARLIEST_FRV_DETERM_DATE, v.HPV_DAYZERO_DATE)) y, count(*) rows_all, count(v.HPV_DAYZERO_DATE) hpv,
        count(distinct v.PGM_SYS_ID) facs
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join f using (PGM_SYS_ID)
      where coalesce(v.EARLIEST_FRV_DETERM_DATE, v.HPV_DAYZERO_DATE) between '2019-01-01' and '2026-09-24' group by 1,2)
select * from v order by 1,2;

-- [q22] statement 22
-- South Coast blank, checked by county not by district label: LA, Orange, Riverside, San Bernardino facilities, all-time enforcement records and last dates
with f as (select PGM_SYS_ID, coalesce(LOCAL_CONTROL_REGION_NAME,'(none)') lcr, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
           where STATE='CA' and upper(COUNTY_NAME) in ('LOS ANGELES','ORANGE','RIVERSIDE','SAN BERNARDINO')),
i as (select PGM_SYS_ID, count(*) n, max(ACHIEVED_DATE) mx from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1),
fo as (select PGM_SYS_ID, count(*) n, max(SETTLEMENT_ENTERED_DATE) mx, listagg(distinct STATE_EPA_FLAG,'') ag from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1),
v as (select PGM_SYS_ID, count(*) n, max(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE)) mx from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1)
select left(f.lcr,40) lcr, count(*) facs, count_if(cls='MAJ' and op='OPR') maj_opr,
  sum(coalesce(i.n,0)) inf_all, max(i.mx) inf_last, sum(coalesce(fo.n,0)) frm_all, max(fo.mx) frm_last, listagg(distinct fo.ag,'') frm_agencies,
  sum(coalesce(v.n,0)) viol_all, max(v.mx) viol_last
from f left join i using (PGM_SYS_ID) left join fo using (PGM_SYS_ID) left join v using (PGM_SYS_ID)
group by 1 order by facs desc;

-- [q23] statement 23
-- National sweep for blind spots: per air jurisdiction (district if any, else state), inspections still logged in 2025
-- but violations / informal actions stopped or collapsed vs their 2021-2023 average
with f as (select PGM_SYS_ID, coalesce(LOCAL_CONTROL_REGION_NAME, 'state ' || STATE) jur, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
i as (select f.jur, count(distinct iff(year(ACHIEVED_DATE) between 2021 and 2023, ACTIVITY_ID, null))/3 inf_avg2123,
        count(distinct iff(year(ACHIEVED_DATE)=2025, ACTIVITY_ID, null)) inf25, max(ACHIEVED_DATE) inf_last
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a join f using (PGM_SYS_ID)
      where ACHIEVED_DATE between '1990-01-01' and '2026-07-31' group by 1),
v as (select f.jur, count_if(year(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE)) between 2021 and 2023)/3 v_avg2123,
        count_if(year(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE))=2025) v25, max(coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE)) v_last
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY a join f using (PGM_SYS_ID)
      where coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE) <= '2026-09-24' group by 1),
e as (select f.jur, count(distinct iff(year(coalesce(try_to_date(ACTUAL_END_DATE::text), try_to_date(ACTUAL_END_DATE::text,'MM/DD/YYYY')))=2025, ACTIVITY_ID, null)) ev25
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES a join f using (PGM_SYS_ID) group by 1),
m as (select jur, count_if(cls='MAJ' and op='OPR') maj from f group by 1)
select left(m.jur,45) jur, m.maj, e.ev25, round(i.inf_avg2123,1) inf_avg2123, coalesce(i.inf25,0) inf25, i.inf_last, round(v.v_avg2123,1) v_avg2123, coalesce(v.v25,0) v25, v.v_last
from m left join e using (jur) left join i using (jur) left join v using (jur)
where m.maj >= 10 and coalesce(e.ev25,0) >= 50
  and (coalesce(v.v25,0) <= 0.25*coalesce(v.v_avg2123,0) or coalesce(v.v_last,'1900-01-01') < '2021-01-01' or coalesce(i.inf_last,'1900-01-01') < '2021-01-01')
order by m.maj desc;

-- [q24] statement 24
-- Subparts as a peer group with a public-health edge: ethylene oxide sterilizers (Part 63 Subpart O, major or area source tag);
-- NOVs, violations and formal actions since 2019 per plant (formal counted across air IDs sharing the FRS registry ID)
with sub as (select PGM_SYS_ID, listagg(distinct AIR_PROGRAM_SUBPART_CODE,'|') codes from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS
             where AIR_PROGRAM_SUBPART_CODE in ('CAAMACTO','CAAGACTMO') group by 1),
fac as (select f.PGM_SYS_ID, f.REGISTRY_ID, f.FACILITY_NAME, f.CITY, f.STATE, f.AIR_POLLUTANT_CLASS_CODE cls, f.AIR_OPERATING_STATUS_CODE op, f.NAICS_CODES, sub.codes
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES f join sub using (PGM_SYS_ID)),
allf as (select PGM_SYS_ID, REGISTRY_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where REGISTRY_ID in (select REGISTRY_ID from fac)),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1),
vh as (select PGM_SYS_ID, count(*) n, count(HPV_DAYZERO_DATE) hpv from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
       where coalesce(EARLIEST_FRV_DETERM_DATE,HPV_DAYZERO_DATE) >= '2019-01-01' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1),
fr as (select allf.REGISTRY_ID, count(distinct a.ACTIVITY_ID) n, sum(a.PENALTY_AMOUNT) pen from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join allf using (PGM_SYS_ID)
       where a.SETTLEMENT_ENTERED_DATE >= '2019-01-01' group by 1)
select 'summary' k, count(*)::text a, count_if(op='OPR')::text b, count_if(coalesce(inf.n,0)>0)::text c, count_if(coalesce(vh.n,0)>0)::text d, count_if(coalesce(fr.n,0)>0)::text e,
  median(coalesce(inf.n,0))::text f, null g, null h
from fac left join inf using (PGM_SYS_ID) left join vh using (PGM_SYS_ID) left join fr on fr.REGISTRY_ID=fac.REGISTRY_ID
union all select * from (select 'plant', FACILITY_NAME, CITY||' '||STATE, op||' '||coalesce(cls,''), coalesce(inf.n,0)::text, coalesce(vh.n,0)::text||' viol / '||coalesce(vh.hpv,0)::text||' hpv',
  coalesce(fr.n,0)::text, round(fr.pen)::text, NAICS_CODES
from fac left join inf using (PGM_SYS_ID) left join vh using (PGM_SYS_ID) left join fr on fr.REGISTRY_ID=fac.REGISTRY_ID
order by coalesce(inf.n,0)+coalesce(vh.n,0) desc limit 15);

-- Footer: 24 SELECT/WITH statements ran, all counted against the 35 budget.
-- Three of them errored and returned nothing: q14 and q15 (divide by zero on zero-emission base years, fixed in q16)
-- and q18 (GROUP BY slip, fixed in q19). 24 connections, each with the 2 required ALTER SESSION lines.
