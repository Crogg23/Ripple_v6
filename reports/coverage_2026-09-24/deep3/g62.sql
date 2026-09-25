-- deep3 / g62: proper look at five glance-only tables, 2026-09-24
-- Tables: ENERGY__FED_EIA861_ENERGY_EFFICIENCY, ENERGY__FED_EIA860_2_PLANT, ENERGY__FED_EIA861_DELIVERY_COMPANIES,
--         ENERGY__FED_EIA860_3_1_GENERATOR, ENERGY__FED_EIA860_3_3_SOLAR
-- Door: Python (connect/db.py) via g62/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g62/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- EE: shape, key uniqueness, adjustment rows, lifetime-vs-first-year equality, sector sums vs total, and the 15 biggest spenders
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY),
p as (select 'profile' k, count(*)::text a, count(distinct UTILITY_NUMBER)::text b, count(distinct UTILITY_NUMBER||'|'||STATE)::text c,
  count(distinct STATE)::text d, listagg(distinct DATA_YEAR,'|') e, count_if(UTILITY_NUMBER=99999 or UTILITY_NAME ilike '%adjust%')::text f,
  count_if(TOTAL_LIFE_CYCLE_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS=TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS)::text||' of '||count(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS)::text g,
  count_if(TOTAL_LIFE_CYCLE_ALL_OTHER_COSTS_THOUSAND_DOLLARS=TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS)::text||' of '||count(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS)::text h,
  count_if(abs(coalesce(RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(COMMERCIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(INDUSTRIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TRANSPORTATION_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)-coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0))>1)::text i,
  count_if(coalesce(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH,0)=0 and coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)>0)::text j,
  count_if(coalesce(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH,0)>0 and coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)=0)::text l,
  sum(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS)::text m, sum(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS)::text n2, sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH)::text o
 from t),
top as (select 'top' k, UTILITY_NAME a, STATE b, UTILITY_NUMBER::text c, RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS::text d, TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS::text e,
  TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS::text f, RESIDENTIAL_INCREMENTAL_ENERGY_SAVINGS_MWH::text g, TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH::text h, TOTAL_LIFE_CYCLE_ENERGY_SAVINGS_MWH::text i,
  RESIDENTIAL_LIFE_CYCLE_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS::text j, RESIDENTIAL_WEIGHTED_AVERAGE_LIFE_YEARS::text l, WEBSITE m, TOTAL_INCREMENTAL_PEAK_DEMAND_SAVINGS_MW::text n2, BA_CODE o
 from t order by coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0) desc limit 15)
select * from p union all select * from top;

-- [q02] statement 2
-- Delivery companies: all 7 rows with per-customer and per-kWh math, and whether the same utility numbers also sit in the main sales table
with d as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DELIVERY_COMPANIES),
s as (select UTILITY_NUMBER, listagg(distinct SERVICE_TYPE||':'||STATE||':'||PART,'|') svc, sum(RESIDENTIAL_CUSTOMERS) s_res_cust, sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS) s_res_rev
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1)
select d.UTILITY_NUMBER, d.UTILITY_NAME, d.STATE, d.PART, d.SERVICE_TYPE, d.DATA_TYPE, d.OWNERSHIP, d.BA_CODE, d.DATA_YEAR,
 d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS res_rev_k, d.RESIDENTIAL_SALES_MWH res_mwh, d.RESIDENTIAL_CUSTOMERS res_cust,
 round(d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS*1000/nullif(d.RESIDENTIAL_CUSTOMERS,0),0) res_usd_per_cust,
 round(d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS*100/nullif(d.RESIDENTIAL_SALES_MWH,0),2) res_cents_kwh,
 round(d.RESIDENTIAL_SALES_MWH*1000/nullif(d.RESIDENTIAL_CUSTOMERS,0),0) kwh_per_cust,
 d.COMMERCIAL_REVENUES_THOUSAND_DOLLARS com_rev_k, d.COMMERCIAL_SALES_MWH com_mwh, d.COMMERCIAL_CUSTOMERS com_cust,
 d.INDUSTRIAL_REVENUES_THOUSAND_DOLLARS ind_rev_k, d.INDUSTRIAL_SALES_MWH ind_mwh, d.INDUSTRIAL_CUSTOMERS ind_cust,
 d.TOTAL_REVENUES_THOUSAND_DOLLARS tot_rev_k, d.TOTAL_SALES_MWH tot_mwh, d.TOTAL_CUSTOMERS tot_cust, d._SRC_FILE,
 s.svc, s.s_res_cust, s.s_res_rev
from d left join s on s.UTILITY_NUMBER=d.UTILITY_NUMBER order by d.RESIDENTIAL_REVENUES_THOUSAND_DOLLARS desc;

-- [q03] statement 3
-- Plant: shape, filler locations, and every combination of the ash-pond fields, regulatory status, sector, FERC flags, storage flags
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT)
select 'ash' k, ASH_IMPOUNDMENT a, ASH_IMPOUNDMENT_LINED b, ASH_IMPOUNDMENT_STATUS c, count(*)::text n, count(distinct STATE)::text x from t group by 1,2,3,4
union all select 'profile', count(*)::text, count(distinct PLANT_CODE)::text, count_if(LATITUDE is null or LATITUDE=0)::text, count_if(ZIP is null or ZIP in ('00000','UNKNO','-'))::text, listagg(distinct _SRC_FILE,'|') from t
union all select 'reg', REGULATORY_STATUS, SECTOR, SECTOR_NAME, count(*)::text, null from t group by 2,3,4
union all select 'ferc', FERC_COGENERATION_STATUS, FERC_SMALL_POWER_PRODUCER_STATUS, FERC_EXEMPT_WHOLESALE_GENERATOR_STATUS, count(*)::text, null from t group by 2,3,4
union all select 'storage', ENERGY_STORAGE, NATURAL_GAS_STORAGE, LIQUEFIED_NATURAL_GAS_STORAGE, count(*)::text, null from t group by 2,3,4;

-- [q04] statement 4
-- Generator: by fuel group and status, capacity, retirement dates (incl. dates already past), vintage, sanity traps, duplicate keys
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
fg as (select *, case when ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') then 'coal' when ENERGY_SOURCE_1='NG' then 'gas'
   when ENERGY_SOURCE_1 in ('DFO','RFO','KER','JF','WO','PC') then 'oil' when ENERGY_SOURCE_1='NUC' then 'nuclear' when ENERGY_SOURCE_1='SUN' then 'solar'
   when ENERGY_SOURCE_1='WND' then 'wind' when ENERGY_SOURCE_1='WAT' then 'hydro' when ENERGY_SOURCE_1='MWH' then 'battery' else 'other' end fuel from t)
select fuel, STATUS, count(*) gens, round(sum(NAMEPLATE_CAPACITY_MW)) mw, count(PLANNED_RETIREMENT_YEAR) w_ret, round(sum(iff(PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0))) ret_mw,
 count_if(PLANNED_RETIREMENT_YEAR<=2024) ret_past, min(PLANNED_RETIREMENT_YEAR) min_ry, max(PLANNED_RETIREMENT_YEAR) max_ry,
 min(OPERATING_YEAR) min_oy, median(OPERATING_YEAR) med_oy, count_if(SUMMER_CAPACITY_MW>NAMEPLATE_CAPACITY_MW*1.2) summer_gt, count_if(MINIMUM_LOAD_MW>NAMEPLATE_CAPACITY_MW) minload_gt,
 count_if(NAMEPLATE_CAPACITY_MW<=0 or NAMEPLATE_CAPACITY_MW is null) cap0, count(distinct PLANT_CODE) plants,
 (select count(*)-count(distinct PLANT_CODE||'|'||GENERATOR_ID) from t) dupkey_all, listagg(distinct _SRC_FILE,'|') src
from fg group by 1,2 order by mw desc;

-- [q05] statement 5
-- Solar: key match to the generator table, capacity agreement, sentinels in azimuth/tilt, DC-to-AC ratio, mount and net-metering fill
with s as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_3_SOLAR),
g as (select PLANT_CODE, GENERATOR_ID, NAMEPLATE_CAPACITY_MW from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where ENERGY_SOURCE_1='SUN')
select count(*) n, count(distinct s.PLANT_CODE||'|'||s.GENERATOR_ID) keys, count(g.PLANT_CODE) in_gen, (select count(*) from g) gen_solar_rows,
 listagg(distinct s.STATUS,'|') statuses, count_if(AZIMUTH_ANGLE=0) az0, count_if(AZIMUTH_ANGLE is null) aznull, count_if(AZIMUTH_ANGLE=180) az180,
 count_if(TILT_ANGLE=0) tilt0, count_if(TILT_ANGLE is null) tiltnull, count_if(DC_NET_CAPACITY_MW is null) dcnull,
 median(DC_NET_CAPACITY_MW/nullif(s.NAMEPLATE_CAPACITY_MW,0)) med_ilr, count_if(DC_NET_CAPACITY_MW/nullif(s.NAMEPLATE_CAPACITY_MW,0)>2) ilr_gt2,
 count_if(DC_NET_CAPACITY_MW/nullif(s.NAMEPLATE_CAPACITY_MW,0)<0.95) ilr_lt095,
 count_if(SINGLE_AXIS_TRACKING='Y') sat, count_if(FIXED_TILT='Y') fixed, count_if(DUAL_AXIS_TRACKING='Y') dual, count_if(EAST_WEST_FIXED_TILT='Y') ew,
 count_if(coalesce(SINGLE_AXIS_TRACKING,'N')<>'Y' and coalesce(FIXED_TILT,'N')<>'Y' and coalesce(DUAL_AXIS_TRACKING,'N')<>'Y' and coalesce(EAST_WEST_FIXED_TILT,'N')<>'Y') no_mount,
 count_if(NET_METERING_AGREEMENT='Y') nm_y, count_if(NET_METERING_AGREEMENT='X') nm_x, count_if(VIRTUAL_NET_METERING_AGREEMENT='Y') vnm_y,
 count_if(abs(s.NAMEPLATE_CAPACITY_MW-g.NAMEPLATE_CAPACITY_MW)>0.01) cap_mismatch, count_if(s.TECHNOLOGY<>'Solar Photovoltaic') non_pv, listagg(distinct s.PRIME_MOVER,'|') pms,
 count_if(BIFACIAL='Y') bifacial, count_if(THIN_FILM_CDTE='Y') cdte, count_if(CRYSTALLINE_SILICON='Y') csi
from s left join g on g.PLANT_CODE=s.PLANT_CODE and g.GENERATOR_ID=s.GENERATOR_ID;

-- [q06] statement 6
-- EE with denominators: join each utility-state row to its own 2024 retail sales (SALES_ULT_CUST, same utility number + state).
-- Cost per first-year MWh saved, savings as % of own sales, residential incentive $ per residential customer, each vs the state median.
-- Also the Delaware SEU row against the whole state's 2024 electricity revenue.
with e as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY),
s as (select UTILITY_NUMBER, STATE, sum(RESIDENTIAL_CUSTOMERS) rc, sum(TOTAL_SALES_MWH) tmwh, sum(TOTAL_REVENUES_THOUSAND_DOLLARS) trev
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1,2),
st as (select STATE, sum(TOTAL_REVENUES_THOUSAND_DOLLARS) st_rev_k, sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS) st_res_rev_k, sum(RESIDENTIAL_CUSTOMERS) st_rc
       from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1),
j as (select e.UTILITY_NAME, e.UTILITY_NUMBER, e.STATE,
   coalesce(e.TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(e.TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0) cost_k,
   e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH sav, e.RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS rinc, s.rc, s.tmwh, s.trev, st.st_rev_k, st.st_res_rev_k, st.st_rc,
   iff(e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH>0 and cost_k>0, cost_k*1000/e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH, null) usd_per_mwh,
   iff(s.tmwh>0, 100*e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH/s.tmwh, null) sav_pct_sales,
   iff(s.rc>0, e.RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS*1000/s.rc, null) rinc_per_cust
  from e left join s on s.UTILITY_NUMBER=e.UTILITY_NUMBER and s.STATE=e.STATE left join st on st.STATE=e.STATE),
k as (select j.*, median(usd_per_mwh) over (partition by STATE) st_med_usd_mwh, count(usd_per_mwh) over (partition by STATE) st_n,
        median(usd_per_mwh) over () nat_med_usd_mwh, median(sav_pct_sales) over () nat_med_pct, median(rinc_per_cust) over () nat_med_rinc from j)
select 'summary' k, count(*)::text a, count(rc)::text b, count(usd_per_mwh)::text c, round(max(nat_med_usd_mwh),1)::text d, round(max(nat_med_pct),3)::text e,
  round(max(nat_med_rinc),2)::text f, count_if(sav_pct_sales>5)::text g, count_if(usd_per_mwh>5*st_med_usd_mwh and st_n>=3)::text h, count_if(usd_per_mwh<st_med_usd_mwh/5 and st_n>=3)::text i,
  null l, null m, null n2, null o from k
union all
select * from (select 'row' k, UTILITY_NAME a, STATE b, round(cost_k)::text c, round(sav)::text d, round(usd_per_mwh,1)::text e, round(st_med_usd_mwh,1)::text f, st_n::text g,
  round(sav_pct_sales,3)::text h, round(rinc_per_cust,2)::text i, rc::text l, round(tmwh)::text m, round(st_rev_k)::text n2, round(st_res_rev_k)::text o
 from k where STATE='DE' or sav_pct_sales>4 or (st_n>=3 and (usd_per_mwh>4*st_med_usd_mwh or usd_per_mwh<st_med_usd_mwh/4)) or rinc_per_cust>150
 order by usd_per_mwh desc nulls last limit 60);

-- [q07] statement 7
-- Ash ponds: every plant that says it has one, bucketed by lined / status / what its generators burn in 2024 / whether eGRID 2022 shows coal output.
-- Join 1: plant -> generator on PLANT_CODE. Join 2: plant -> eGRID 2022 on ORIS code (text, cast to number).
with p as (select PLANT_CODE, ASH_IMPOUNDMENT_LINED lined, ASH_IMPOUNDMENT_STATUS ast from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT where ASH_IMPOUNDMENT='Y'),
g as (select PLANT_CODE,
    sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC'),NAMEPLATE_CAPACITY_MW,0)) coal_mw,
    sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') and STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) coal_op_mw,
    sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') and STATUS='OP' and PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0)) coal_op_dated_mw,
    sum(NAMEPLATE_CAPACITY_MW) all_mw
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, count(*) n, max(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal_gen22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1)
select p.lined, p.ast,
  case when g.PLANT_CODE is null then 'no generator row' when g.coal_op_mw>0 then 'coal running' when g.coal_mw>0 then 'coal all SB/OS/OA' else 'no coal generator' end gen_class,
  count(*) plants, round(sum(g.coal_op_mw)) coal_op_mw, round(sum(g.coal_op_dated_mw)) coal_op_dated_mw, round(sum(g.all_mw)) all_mw,
  count(e.pc) in_egrid, count_if(e.coal_gen22>0) coal_gen_2022, round(sum(e.coal_gen22)/1e6,1) coal_twh_2022, max(e.n) egrid_dupes
from p left join g on g.PLANT_CODE=p.PLANT_CODE left join e on e.pc=p.PLANT_CODE
group by 1,2,3 order by 1,2,3;

-- [q08] statement 8
-- Generator time series: MW brought online per year (2000-2024) by fuel, and MW with a planned retirement per year (2025-2040) by fuel. Operable units only (this table).
with t as (select *, case when ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') then 'coal' when ENERGY_SOURCE_1='NG' then 'gas'
   when ENERGY_SOURCE_1 in ('DFO','RFO','KER','JF','WO','PC') then 'oil' when ENERGY_SOURCE_1='SUN' then 'solar'
   when ENERGY_SOURCE_1='WND' then 'wind' when ENERGY_SOURCE_1='MWH' then 'battery' else 'other' end fuel
   from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
b as (select 'built' k, OPERATING_YEAR yr, fuel, NAMEPLATE_CAPACITY_MW mw from t where OPERATING_YEAR>=2000
      union all select 'retire', PLANNED_RETIREMENT_YEAR, fuel, NAMEPLATE_CAPACITY_MW from t where PLANNED_RETIREMENT_YEAR is not null and PLANNED_RETIREMENT_YEAR<=2040)
select k, yr, round(sum(iff(fuel='gas',mw,0))) gas, round(sum(iff(fuel='coal',mw,0))) coal, round(sum(iff(fuel='oil',mw,0))) oil, round(sum(iff(fuel='solar',mw,0))) solar,
  round(sum(iff(fuel='wind',mw,0))) wind, round(sum(iff(fuel='battery',mw,0))) battery, round(sum(iff(fuel='other',mw,0))) other, count(*) gens
from b group by 1,2 order by 1,2;

-- [q09] statement 9
-- Delivery companies in context: Texas 2024 rows in the main sales table by part/service type (energy-only retailers, bundled utilities),
-- residential $ per customer and cents/kWh, so the wires-only charge can be set against the energy charge and against bundled Texas utilities outside ERCOT.
with s as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where STATE='TX')
select PART, SERVICE_TYPE, BA_CODE, OWNERSHIP, count(*) rows_, count(distinct UTILITY_NUMBER) utils,
  sum(RESIDENTIAL_CUSTOMERS) res_cust, round(sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS)) res_rev_k, sum(RESIDENTIAL_SALES_MWH) res_mwh,
  round(sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS)*1000/nullif(sum(RESIDENTIAL_CUSTOMERS),0)) usd_per_cust,
  round(sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS)*100/nullif(sum(RESIDENTIAL_SALES_MWH),0),2) cents_kwh,
  listagg(distinct DATA_TYPE,'|') dtypes, max(DATA_YEAR) yr
from s group by 1,2,3,4 order by res_cust desc nulls last;

-- [q10] statement 10
-- Solar sentinels and peers: azimuth 0 by mount type; DC-to-AC ratio by operating year and by mount (median); tilt 0 by mount.
with s as (select *, case when SINGLE_AXIS_TRACKING='Y' then 'single-axis' when DUAL_AXIS_TRACKING='Y' then 'dual-axis' when EAST_WEST_FIXED_TILT='Y' then 'east-west'
   when FIXED_TILT='Y' then 'fixed' else 'none said' end mount from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_3_SOLAR)
select 'mount' k, mount a, count(*) n, round(sum(NAMEPLATE_CAPACITY_MW)) mw, count_if(AZIMUTH_ANGLE=0) az0, count_if(AZIMUTH_ANGLE=180) az180, count_if(AZIMUTH_ANGLE is null) aznull,
  count_if(AZIMUTH_ANGLE between 1 and 89 or AZIMUTH_ANGLE between 271 and 359) az_northish, count_if(TILT_ANGLE=0) tilt0,
  round(median(DC_NET_CAPACITY_MW/nullif(NAMEPLATE_CAPACITY_MW,0)),3) med_ilr, count_if(NET_METERING_AGREEMENT='Y') nm_y, count_if(VIRTUAL_NET_METERING_AGREEMENT='Y') vnm_y
from s group by 2
union all
select 'year', OPERATING_YEAR::text, count(*), round(sum(NAMEPLATE_CAPACITY_MW)), count_if(AZIMUTH_ANGLE=0), count_if(AZIMUTH_ANGLE=180), count_if(AZIMUTH_ANGLE is null),
  count_if(SINGLE_AXIS_TRACKING='Y'), count_if(TILT_ANGLE=0), round(median(DC_NET_CAPACITY_MW/nullif(NAMEPLATE_CAPACITY_MW,0)),3), count_if(NET_METERING_AGREEMENT='Y'), count_if(VIRTUAL_NET_METERING_AGREEMENT='Y')
from s where OPERATING_YEAR>=2008 group by 2
order by 1, 2;

-- [q11] statement 11
-- Ash ponds, named: every ash-pond plant with coal generators still OP in 2024 (lined and unlined), coal MW, how much of it has any planned
-- retirement date, the latest such date, the oldest unit, eGRID 2022 coal output. Plus the state's lined/unlined split among these peers.
with p as (select PLANT_CODE, PLANT_NAME, UTILITY_NAME, STATE, COUNTY, SECTOR_NAME, REGULATORY_STATUS reg, ASH_IMPOUNDMENT_LINED lined, ASH_IMPOUNDMENT_STATUS ast
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT where ASH_IMPOUNDMENT='Y'),
g as (select PLANT_CODE,
    sum(iff(STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) coal_op_mw,
    sum(iff(STATUS='OP' and PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0)) coal_dated_mw,
    count_if(STATUS='OP') coal_units, count_if(STATUS='OP' and PLANNED_RETIREMENT_YEAR is null) undated_units,
    min(PLANNED_RETIREMENT_YEAR) first_ret, max(PLANNED_RETIREMENT_YEAR) last_ret, min(OPERATING_YEAR) oldest_unit
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') group by 1 having coal_op_mw>0),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal_gen22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1),
j as (select p.*, g.coal_op_mw, g.coal_dated_mw, g.coal_units, g.undated_units, g.first_ret, g.last_ret, g.oldest_unit, e.coal_gen22,
        count(*) over (partition by p.STATE) st_peers, count_if(p.lined='N' and p.ast='OP') over (partition by p.STATE) st_unlined_op
      from p join g on g.PLANT_CODE=p.PLANT_CODE left join e on e.pc=p.PLANT_CODE)
select lined, ast, PLANT_CODE, PLANT_NAME, UTILITY_NAME, STATE, COUNTY, SECTOR_NAME, reg, round(coal_op_mw) coal_mw, round(coal_dated_mw) dated_mw,
  coal_units, undated_units, first_ret, last_ret, oldest_unit, round(coal_gen22/1e3) coal_gwh_2022, st_peers, st_unlined_op
from j order by (lined='N' and ast='OP') desc, (coal_dated_mw=0) desc, coal_op_mw desc;

-- [q12] statement 12
-- EE unit check: each utility's reported program cost against its OWN 2024 retail revenue (same utility number + state).
-- A cost above ~10% of revenue is not an efficiency program, it is a units slip. Lists every row over 5%, plus the national spread.
with e as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY),
s as (select UTILITY_NUMBER, STATE, sum(TOTAL_REVENUES_THOUSAND_DOLLARS) trev_k, sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS) rrev_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1,2),
j as (select e.UTILITY_NAME, e.UTILITY_NUMBER, e.STATE,
   coalesce(e.TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(e.TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0) cost_k,
   e.RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS rinc_k, e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH sav, s.trev_k, s.rrev_k,
   iff(s.trev_k>0, 100*cost_k/s.trev_k, null) cost_pct_rev
  from e left join s on s.UTILITY_NUMBER=e.UTILITY_NUMBER and s.STATE=e.STATE)
select 'spread' k, null a, null b, count(cost_pct_rev)::text c, round(median(cost_pct_rev),3)::text d, round(percentile_cont(0.9) within group (order by cost_pct_rev),3)::text e,
  round(percentile_cont(0.99) within group (order by cost_pct_rev),3)::text f, count_if(cost_pct_rev>5)::text g, count_if(cost_pct_rev>10)::text h,
  round(sum(cost_k))::text i, round(sum(iff(cost_pct_rev>10 or UTILITY_NUMBER=58854,cost_k,0)))::text l from j
union all
select * from (select 'row', UTILITY_NAME, STATE, round(cost_k)::text, round(rinc_k)::text, round(sav)::text, round(trev_k)::text, round(rrev_k)::text,
  round(cost_pct_rev,2)::text, UTILITY_NUMBER::text, null from j where cost_pct_rev>5 or UTILITY_NUMBER=58854 order by cost_pct_rev desc nulls first);

-- [q13] statement 13
-- Generator x eGRID 2022: plants whose every 2024-operable unit was online by 2021, grouped by main fuel. How much "OP" capacity sat at plants
-- that made zero or negative net power in 2022, and the capacity factor spread per fuel. Land rate on the ORIS code first.
with g as (select PLANT_CODE, max(OPERATING_YEAR) newest_unit, sum(NAMEPLATE_CAPACITY_MW) mw,
    max_by(case when ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') then 'coal' when ENERGY_SOURCE_1='NG' then 'gas'
      when ENERGY_SOURCE_1 in ('DFO','RFO','KER','JF','WO','PC') then 'oil' when ENERGY_SOURCE_1='SUN' then 'solar' when ENERGY_SOURCE_1='WND' then 'wind'
      when ENERGY_SOURCE_1='NUC' then 'nuclear' when ENERGY_SOURCE_1='WAT' then 'hydro' when ENERGY_SOURCE_1='MWH' then 'battery' else 'other' end, NAMEPLATE_CAPACITY_MW) fuel,
    count_if(STATUS<>'OP') not_op_units, count(*) units
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_NET_GENERATION_MWH) gen22, max(try_to_double(PLANT_NAMEPLATE_CAPACITY_MW)) mw22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1),
j as (select g.*, e.pc, e.gen22, e.mw22, iff(e.mw22>0, e.gen22/(e.mw22*8760), null) cf from g left join e on e.pc=g.PLANT_CODE where g.newest_unit<=2021)
select fuel, count(*) plants, count(pc) in_egrid, round(sum(mw)) mw, count_if(pc is not null and coalesce(gen22,0)<=0) zero_gen_plants,
  round(sum(iff(pc is not null and coalesce(gen22,0)<=0, mw, 0))) zero_gen_mw, count_if(pc is not null and coalesce(gen22,0)<=0 and not_op_units=0) zero_gen_all_op,
  round(sum(iff(pc is not null and coalesce(gen22,0)<=0 and not_op_units=0, mw, 0))) zero_gen_all_op_mw,
  round(median(cf),3) med_cf, round(percentile_cont(0.1) within group (order by cf),3) p10_cf, count_if(abs(mw-mw22)/nullif(mw22,0)>0.2) mw_mismatch_20pct
from j group by 1 order by mw desc;

-- [q14] statement 14
-- Solar x eGRID 2022: solar-only plants (every 2024 unit is solar, all online by 2021, 2024 MW within 5% of eGRID 2022 MW), capacity factor
-- vs peers in the same state and mount type. Lists plants of 20 MW+ under half their peer median. Peer medians need 5+ plants.
with s as (select PLANT_CODE, max(PLANT_NAME) pname, max(UTILITY_NAME) op, max(STATE) st, sum(NAMEPLATE_CAPACITY_MW) mw, max(OPERATING_YEAR) newest,
    max_by(case when SINGLE_AXIS_TRACKING='Y' then 'single-axis' when DUAL_AXIS_TRACKING='Y' then 'dual-axis' when FIXED_TILT='Y' or EAST_WEST_FIXED_TILT='Y' then 'fixed' else 'none' end, NAMEPLATE_CAPACITY_MW) mount
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_3_SOLAR group by 1),
g as (select PLANT_CODE, sum(NAMEPLATE_CAPACITY_MW) all_mw, count_if(STATUS<>'OP') not_op from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_NET_GENERATION_MWH) gen22, max(try_to_double(PLANT_NAMEPLATE_CAPACITY_MW)) mw22,
      max(PLANT_ANNUAL_SOLAR_NET_GENERATION_MWH) sol22 from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1),
j as (select s.*, g.not_op, e.gen22, e.mw22, e.gen22/(e.mw22*8760) cf from s join g on g.PLANT_CODE=s.PLANT_CODE and abs(g.all_mw-s.mw)<0.01
      join e on e.pc=s.PLANT_CODE where s.newest<=2021 and e.mw22>0 and abs(s.mw-e.mw22)/e.mw22<=0.05),
k as (select j.*, median(cf) over (partition by st, mount) peer_cf, count(*) over (partition by st, mount) peer_n, median(cf) over () nat_cf from j)
select 'summary' k, count(*)::text a, round(max(nat_cf),3)::text b, count_if(peer_n>=5 and cf<peer_cf/2)::text c, count_if(peer_n>=5 and cf<peer_cf/2 and mw>=20)::text d,
  count_if(cf<=0)::text e, count_if(cf<=0 and mw>=20)::text f, round(sum(iff(peer_n>=5 and cf<peer_cf/2 and mw>=20, mw, 0)))::text g, null h, null i, null l, null m from k
union all
select * from (select 'row', pname, op, st, mount, round(mw,1)::text, newest::text, round(cf,3)::text, round(peer_cf,3)::text, peer_n::text, round(gen22)::text, not_op::text
  from k where peer_n>=5 and cf<peer_cf/2 and mw>=20 order by mw desc limit 40);

-- [q15] statement 15
-- Dull-explanation test for the ash-pond status: what burns at the plants whose UNLINED pond is 'OP' but that have no coal unit running in 2024?
-- If OP meant "receiving coal ash now", these plants should not exist. Grouped by main 2024 fuel, with eGRID 2022 coal output and names.
with p as (select PLANT_CODE, PLANT_NAME, UTILITY_NAME, STATE from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT
           where ASH_IMPOUNDMENT='Y' and ASH_IMPOUNDMENT_LINED='N' and ASH_IMPOUNDMENT_STATUS='OP'),
g as (select PLANT_CODE, sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') and STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) coal_op_mw,
        max_by(ENERGY_SOURCE_1, NAMEPLATE_CAPACITY_MW) main_fuel, sum(iff(STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) op_mw
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal22, max(PLANT_PRIMARY_FUEL) pf22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1)
select coalesce(g.main_fuel,'(no generator row)') main_fuel_2024, count(*) plants, round(sum(g.op_mw)) op_mw, count_if(e.coal22>0) coal_in_2022,
  listagg(distinct e.pf22, ',') egrid_fuel_2022, listagg(p.PLANT_NAME||' ('||p.STATE||')', '; ') within group (order by p.PLANT_NAME) names
from p left join g on g.PLANT_CODE=p.PLANT_CODE left join e on e.pc=p.PLANT_CODE
where coalesce(g.coal_op_mw,0)=0
group by 1 order by plants desc;

-- [q16] statement 16
-- Enforcement join: coal-running plants by ash-pond group -> CAMD program ID (= EIA plant code) in the combined-emissions table -> FRS registry ID -> ECHO.
-- Peer groups: unlined OP pond with no coal retirement date / unlined OP with dates / lined OP / pond not OP / no pond reported. Land rate at each hop.
with pl as (select PLANT_CODE, STATE, ASH_IMPOUNDMENT ash, ASH_IMPOUNDMENT_LINED lined, ASH_IMPOUNDMENT_STATUS ast from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT),
g as (select PLANT_CODE, sum(NAMEPLATE_CAPACITY_MW) coal_mw, sum(iff(PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0)) dated_mw
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where STATUS='OP' and ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') group by 1),
grp as (select g.PLANT_CODE, pl.STATE, g.coal_mw,
          case when pl.ash='Y' and pl.lined='N' and pl.ast='OP' and g.dated_mw=0 then 'a unlined OP, no coal ret date'
               when pl.ash='Y' and pl.lined='N' and pl.ast='OP' then 'b unlined OP, some dated'
               when pl.ash='Y' and pl.lined='Y' and pl.ast='OP' then 'c lined OP'
               when pl.ash='Y' then 'd pond not OP' else 'e no pond reported' end grp
        from g join pl on pl.PLANT_CODE=g.PLANT_CODE),
c as (select try_to_number(PGM_SYS_ID) oris, min(to_varchar(REGISTRY_ID)) reg, count(distinct REGISTRY_ID) nreg
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS where PGM_SYS_ACRNM='CAMDBS' group by 1),
e as (select to_varchar(FRS_ID) reg, max(STATE) st, max(QUARTERS_WITH_NONCOMPLIANCE) q, max(FORMAL_ACTION_COUNT) fa, max(TOTAL_PENALTIES) pen,
        max(PENALTY_COUNT) pcount, max(HAS_WATER_PROGRAM::int) water, max(INFORMAL_ACTION_COUNT) ia, count(*) echo_rows
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where to_varchar(FRS_ID) in (select reg from c) group by 1)
select grp.grp, count(*) plants, round(sum(grp.coal_mw)) coal_mw, count(c.reg) with_reg, max(c.nreg) max_nreg, count(e.reg) in_echo, count_if(e.st=grp.STATE) state_agrees,
  max(e.echo_rows) max_echo_rows, round(median(e.q),1) med_q_noncomp, round(avg(e.q),2) avg_q_noncomp, count_if(e.q>=4) q4plus, count_if(e.q>=12) q12,
  count_if(e.fa>0) any_formal_5yr, round(avg(e.ia),2) avg_informal, count_if(e.pen>0) any_penalty, round(sum(e.pen)) penalties_usd, round(median(iff(e.pen>0,e.pen,null))) med_penalty, sum(e.water) water_program
from grp left join c on c.oris=grp.PLANT_CODE left join e on e.reg=c.reg
group by 1 order by 1;

-- [q17] statement 17
-- FERC qualifying-facility flags vs the plant's own generators. (1) Small power producer = Y but operable nameplate over 80 MW.
-- (2) Cogeneration = Y but no generator flagged combined heat and power and a non-CHP sector. (3) One FERC docket number on several plants.
with p as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT),
g as (select PLANT_CODE, sum(iff(STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) op_mw, count_if(ASSOCIATED_WITH_COMBINED_HEAT_AND_POWER_SYSTEM='Y') chp_units, count(*) units,
        max_by(ENERGY_SOURCE_1, NAMEPLATE_CAPACITY_MW) fuel, min(OPERATING_YEAR) first_yr
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
j as (select p.PLANT_CODE, p.PLANT_NAME, p.UTILITY_NAME, p.STATE, p.SECTOR_NAME, p.FERC_SMALL_POWER_PRODUCER_STATUS spp, p.FERC_SMALL_POWER_PRODUCER_DOCKET_NUMBER spp_dk,
        p.FERC_COGENERATION_STATUS cog, p.FERC_COGENERATION_DOCKET_NUMBER cog_dk, g.op_mw, g.chp_units, g.units, g.fuel, g.first_yr
      from p left join g on g.PLANT_CODE=p.PLANT_CODE),
d as (select dk, count(distinct PLANT_CODE) plants from (select PLANT_CODE, spp_dk dk from j where spp='Y' and spp_dk is not null and upper(spp_dk) not like '%PEND%'
        union all select PLANT_CODE, cog_dk from j where cog='Y' and cog_dk is not null and upper(cog_dk) not like '%PEND%') group by 1)
select 'spp_summary' k, count_if(spp='Y')::text a, count_if(spp='Y' and op_mw>80)::text b, round(sum(iff(spp='Y' and op_mw>80, op_mw, 0)))::text c,
  count_if(spp='Y' and op_mw>80 and fuel='WND')::text d, count_if(spp='Y' and op_mw>80 and fuel='SUN')::text e, count_if(spp='Y' and op_mw>80 and fuel not in ('WND','SUN'))::text f,
  count_if(spp='Y' and spp_dk is null)::text g, null h, null i from j
union all
select 'cog_summary', count_if(cog='Y')::text, count_if(cog='Y' and coalesce(chp_units,0)=0 and units>0)::text, count_if(cog='Y' and coalesce(chp_units,0)=0 and SECTOR_NAME ilike '%Non-CHP%')::text,
  round(sum(iff(cog='Y' and coalesce(chp_units,0)=0 and SECTOR_NAME ilike '%Non-CHP%', op_mw, 0)))::text, count_if(cog='Y' and units is null)::text, null, null, null, null from j
union all
select 'docket_summary', count(*)::text, count_if(plants>1)::text, max(plants)::text, null, null, null, null, null, null from d
union all
select * from (select 'spp_big', PLANT_NAME, UTILITY_NAME, STATE, fuel, round(op_mw)::text, first_yr::text, spp_dk, (select max(plants) from d where d.dk=j.spp_dk)::text, SECTOR_NAME
  from j where spp='Y' and op_mw>80 order by op_mw desc limit 25)
union all
select * from (select 'cog_nochp', PLANT_NAME, UTILITY_NAME, STATE, fuel, round(op_mw)::text, first_yr::text, cog_dk, (select max(plants) from d where d.dk=j.cog_dk)::text, SECTOR_NAME
  from j where cog='Y' and coalesce(chp_units,0)=0 and SECTOR_NAME ilike '%Non-CHP%' order by op_mw desc nulls last limit 25)
union all
select * from (select 'docket_multi', dk, null, null, null, plants::text, null, null, null, null from d where plants>1 order by plants desc limit 10);

-- [q18] statement 18
-- Delivery companies x 2024 reliability (same utility number, TX): what each wires company charges per customer vs outage minutes per customer,
-- with and without major events (Hurricane Beryl hit Houston July 2024 - outside knowledge). Plus the Texas median of every other reliability reporter.
with d as (select UTILITY_NUMBER, UTILITY_NAME, RESIDENTIAL_CUSTOMERS rc, TOTAL_CUSTOMERS tc, RESIDENTIAL_REVENUES_THOUSAND_DOLLARS rrev_k, TOTAL_REVENUES_THOUSAND_DOLLARS trev_k
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DELIVERY_COMPANIES),
r as (select UTILITY_NUMBER, STATE, coalesce(IEEE_SAIDI_WITH_MED_MINUTES, OTHER_SAIDI_WITH_MED_MINUTES) saidi_med, coalesce(IEEE_SAIDI_WITHOUT_MED_MINUTES, OTHER_SAIDI_WITHOUT_MED_MINUTES) saidi_nomed,
        coalesce(IEEE_SAIFI_WITH_MED, OTHER_SAIFI_WITH_MED) saifi_med, coalesce(IEEE_NUMBER_OF_CUSTOMERS, OTHER_NUMBER_OF_CUSTOMERS) rel_cust,
        iff(IEEE_SAIDI_WITH_MED_MINUTES is not null,'IEEE','other') std
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_RELIABILITY where STATE='TX')
select 'tdsp' k, d.UTILITY_NAME, d.tc::text tc, round(d.rrev_k*1000/nullif(d.rc,0))::text res_usd_cust, round(d.trev_k*1000/nullif(d.tc,0))::text all_usd_cust,
  round(r.saidi_med)::text saidi_with_major, round(r.saidi_nomed)::text saidi_without_major, round(r.saifi_med,2)::text saifi, round(r.rel_cust)::text rel_cust, r.std
from d left join r on r.UTILITY_NUMBER=d.UTILITY_NUMBER
union all
select 'tx_others', 'median of TX reporters not in the delivery table', count(*)::text, null, null, round(median(saidi_med))::text, round(median(saidi_nomed))::text, round(median(saifi_med),2)::text, round(sum(rel_cust))::text, null
from r where UTILITY_NUMBER not in (select UTILITY_NUMBER from d);

-- [q19] statement 19
-- EE per customer, properly: the 45 biggest utility-state rows by residential customers (all parts of the sales table), with or without an EE row.
-- Residential incentive $ per residential customer, total program $ per customer, first-year savings as % of own sales. Peer = every utility-state row with 500K+ homes (energy-only retailers, part B, left out).
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, listagg(distinct OWNERSHIP,'|') own, sum(RESIDENTIAL_CUSTOMERS) rc, sum(TOTAL_CUSTOMERS) tc, sum(TOTAL_SALES_MWH) tmwh
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' group by 1,2),
e as (select UTILITY_NUMBER, STATE, count(*) ee_rows,
        sum(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) cost_k,
        sum(RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS) rinc_k, sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1,2),
j as (select s.*, e.ee_rows, e.cost_k, e.rinc_k, e.sav, e.cost_k*1000/nullif(s.tc,0) usd_per_cust, e.rinc_k*1000/nullif(s.rc,0) rinc_per_home, 100*e.sav/nullif(s.tmwh,0) sav_pct
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE where s.rc>=500000)
select 'peer' k, null uname, null st, count(*)::text n, count(ee_rows)::text with_ee, round(median(usd_per_cust),2)::text med_usd_cust, round(median(rinc_per_home),2)::text med_rinc_home,
  round(median(sav_pct),3)::text med_sav_pct, null a, null b, null c from j
union all
select * from (select 'row', uname, STATE, round(rc)::text, own, round(cost_k)::text, round(usd_per_cust,2)::text, round(rinc_per_home,2)::text, round(sav_pct,3)::text, round(sav)::text, ee_rows::text
  from j order by usd_per_cust desc nulls last limit 60);

-- [q20] statement 20
-- Generator eyeball: the big units not in plain OP status (nuclear OS/OA, coal/gas over 300 MW), every carbon-capture Y unit,
-- and hydro units with summer capacity over 1.2x nameplate (trap check: 5 biggest).
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR)
select * from (select 'not_op' k, PLANT_NAME, UTILITY_NAME, STATE, GENERATOR_ID, TECHNOLOGY, STATUS, round(NAMEPLATE_CAPACITY_MW)::text mw, OPERATING_YEAR::text oy,
   PLANNED_RETIREMENT_YEAR::text ry, SUMMER_CAPACITY_MW::text summer from t
 where STATUS<>'OP' and (ENERGY_SOURCE_1='NUC' or NAMEPLATE_CAPACITY_MW>=300) order by NAMEPLATE_CAPACITY_MW desc limit 25)
union all
select 'ccs', PLANT_NAME, UTILITY_NAME, STATE, GENERATOR_ID, TECHNOLOGY, STATUS, round(NAMEPLATE_CAPACITY_MW)::text, OPERATING_YEAR::text, PLANNED_RETIREMENT_YEAR::text, SUMMER_CAPACITY_MW::text
 from t where CARBON_CAPTURE_TECHNOLOGY='Y'
union all
select * from (select 'hydro_summer', PLANT_NAME, UTILITY_NAME, STATE, GENERATOR_ID, TECHNOLOGY, STATUS, NAMEPLATE_CAPACITY_MW::text, OPERATING_YEAR::text, round(SUMMER_CAPACITY_MW/NAMEPLATE_CAPACITY_MW,2)::text, SUMMER_CAPACITY_MW::text
 from t where ENERGY_SOURCE_1='WAT' and SUMMER_CAPACITY_MW>1.2*NAMEPLATE_CAPACITY_MW order by SUMMER_CAPACITY_MW desc limit 5);

-- [q21] statement 21
-- Dull-explanation test for the low EE spenders: maybe they spend through demand response (load control) instead.
-- Same 62 big utility-state rows; EE $ per customer, demand-response $ per customer (EIA-861 DR file, same utility number + state), combined, peer medians.
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, sum(RESIDENTIAL_CUSTOMERS) rc, sum(TOTAL_CUSTOMERS) tc
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' group by 1,2 having sum(RESIDENTIAL_CUSTOMERS)>=500000),
e as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) ee_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1,2),
d as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) dr_k,
        sum(RESIDENTIAL_CUSTOMERS_ENROLLED) dr_res_enrolled, sum(TOTAL_ACTUAL_PEAK_DEMAND_SAVINGS_MW) dr_actual_mw, sum(TOTAL_POTENTIAL_PEAK_DEMAND_SAVINGS_MW) dr_pot_mw
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE group by 1,2),
j as (select s.*, e.ee_k, d.dr_k, d.dr_res_enrolled, d.dr_actual_mw, d.dr_pot_mw, e.ee_k*1000/s.tc ee_cust, d.dr_k*1000/s.tc dr_cust,
        (coalesce(e.ee_k,0)+coalesce(d.dr_k,0))*1000/s.tc both_cust
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE left join d on d.UTILITY_NUMBER=s.UTILITY_NUMBER and d.STATE=s.STATE)
select 'peer' k, null uname, null st, count(*)::text n, count(dr_k)::text with_dr, round(median(ee_cust),2)::text, round(median(dr_cust),2)::text, round(median(both_cust),2)::text, null, null, null from j
union all
select * from (select 'row', uname, STATE, round(rc)::text, round(ee_k)::text, round(ee_cust,2)::text, round(dr_cust,2)::text, round(both_cust,2)::text,
   round(dr_res_enrolled)::text, round(dr_actual_mw)::text, (rank() over (order by both_cust desc))::text
 from j order by both_cust asc limit 20);

-- [q22] statement 22
-- State peers: efficiency + demand-response program dollars per electricity customer, every reporter in the state (third-party administrators
-- like Efficiency Maine or Energy Trust count under their state). Two units slips corrected /1000: Delaware SEU (58854) and West River (20401).
-- Denominator: all customers in the sales table except energy-only retailers (part B) so no customer is counted twice.
with c as (select STATE, sum(TOTAL_CUSTOMERS) cust, sum(RESIDENTIAL_CUSTOMERS) homes from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' group by 1),
e as (select STATE, count(*) ee_rows,
        sum((coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) / iff(UTILITY_NUMBER in (58854,20401),1000,1)) ee_k,
        sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1),
d as (select STATE, sum(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) dr_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE group by 1),
s as (select STATE, sum(TOTAL_SALES_MWH) mwh from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1),
j as (select c.STATE, c.cust, c.homes, e.ee_rows, e.ee_k, d.dr_k, e.sav, s.mwh,
        coalesce(e.ee_k,0)*1000/c.cust ee_cust, (coalesce(e.ee_k,0)+coalesce(d.dr_k,0))*1000/c.cust both_cust, 100*e.sav/nullif(s.mwh,0) sav_pct
      from c left join e on e.STATE=c.STATE left join d on d.STATE=c.STATE left join s on s.STATE=c.STATE where c.cust>0)
select STATE, round(cust) cust, ee_rows, round(ee_k) ee_k, round(dr_k) dr_k, round(ee_cust,2) ee_per_cust, round(both_cust,2) ee_dr_per_cust, round(sav_pct,3) sav_pct_sales,
  rank() over (order by both_cust desc) rnk, round(median(both_cust) over (),2) nat_median, count(*) over () states
from j order by both_cust desc;

-- [q23] statement 23
-- Inside-the-group test for Ohio: every utility with 20K+ customers in OH and its neighbors (MI, IN, PA, KY, WV) plus IL,
-- EE $ and DR $ per own customer, savings % of own sales. Median utility per state, so one or two big rows can't carry the gap.
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, listagg(distinct OWNERSHIP,'|') own, sum(TOTAL_CUSTOMERS) tc, sum(TOTAL_SALES_MWH) mwh
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' and STATE in ('OH','MI','IN','PA','KY','WV','IL') group by 1,2 having sum(TOTAL_CUSTOMERS)>=20000),
e as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) ee_k,
        sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1,2),
d as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) dr_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE group by 1,2),
j as (select s.*, e.ee_k, d.dr_k, e.sav, coalesce(e.ee_k,0)*1000/s.tc ee_cust, coalesce(d.dr_k,0)*1000/s.tc dr_cust, 100*coalesce(e.sav,0)/nullif(s.mwh,0) sav_pct
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE left join d on d.UTILITY_NUMBER=s.UTILITY_NUMBER and d.STATE=s.STATE)
select 'state' k, STATE, null uname, count(*)::text utils, count(ee_k)::text with_ee, round(median(ee_cust),2)::text med_ee_cust, round(median(ee_cust+dr_cust),2)::text med_both,
  round(median(sav_pct),3)::text med_sav_pct, round(sum(tc))::text cust, null a from j group by 2
union all
select * from (select 'util', STATE, uname, round(tc)::text, own, round(ee_cust,2)::text, round(ee_cust+dr_cust,2)::text, round(sav_pct,3)::text, round(ee_k)::text, round(dr_k)::text
  from j where STATE in ('OH','MI') order by STATE, tc desc);
