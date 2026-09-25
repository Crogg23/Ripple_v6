-- g60: deep pass 3, 2026-09-24. Python door (connect/db.py), QUERY_TAG deep3-2026-09-24. Read-only: SELECT/WITH only.
-- Tables: ECONOMICS__FED_SEC_EDGAR, ECONOMICS__INTL_FAO_FAOSTAT, ENERGY__INTL_EMBER_ELEC, ENERGY__FED_EIA860_3_2_WIND, ENERGY__FED_EIA860_3_4_ENERGY_STORAGE.
-- 21 statements of the 35 budget: 3 connections x 2 session-setup lines + 15 SELECTs. Every SELECT is below, in run order, with runtime and row count.
-- The small tables (wind 1,563 rows, storage 786, Ember pivot 5,726) were pulled whole by S10-S12 and analysed locally in pandas; no extra warehouse statements.

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- S01 SEC_EDGAR: per company rows, forms, filing-date range, EIN shape, duplicate accessions (0.4s, 20 rows)
select CIK, ENTITYNAME, count(*) n, count(distinct ACCESSIONNUMBER) n_acc, min(FILEDAT) filed_min, max(FILEDAT) filed_max,
  listagg(distinct FORM, ',') within group (order by FORM) forms, max(EIN) ein, max(length(EIN)) ein_len,
  max(STATEOFINCORPORATION) inc, max(SICDESCRIPTION) sic,
  (select count(*) - count(distinct ACCESSIONNUMBER) from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR) dup_acc_total
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR
group by 1, 2 order by 1;

-- S02 FAO_FAOSTAT: the whole 69-row catalog, oldest update first (0.4s, 69 rows)
select DATASETCODE, DATASETNAME, DATEUPDATE, FILEROWS, FILESIZE, left(TOPIC, 40) topic40
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT
order by try_to_timestamp(DATEUPDATE::string) nulls first, DATASETCODE;

-- S03 EMBER shape by year and area type: rows, areas, series, runs, flag fill (0.8s, 52 rows)
select left(DATE::string, 4) yr, AREA_TYPE, count(*) n, count(distinct COUNTRY) n_areas,
  count(distinct CATEGORY || '|' || SUBCATEGORY || '|' || VARIABLE || '|' || UNIT) n_series,
  count(distinct _SOURCE_RUN_ID) n_runs, count(IS_EU) n_is_eu, count(IS_OECD) n_is_oecd, count(IS_G20) n_is_g20,
  count(*) - count(distinct COUNTRY || '|' || DATE::string || '|' || CATEGORY || '|' || SUBCATEGORY || '|' || VARIABLE || '|' || UNIT) n_dup_keys
from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC
group by 1, 2 order by 1, 2;

-- S04 EMBER series list: every category/subcategory/variable/unit with rows, areas, year range, duplicate keys (0.4s, 66 rows)
select CATEGORY, SUBCATEGORY, VARIABLE, UNIT, count(*) n, count(distinct COUNTRY) n_areas,
  min(left(DATE::string, 4)) y0, max(left(DATE::string, 4)) y1,
  count(*) - count(distinct COUNTRY || '|' || DATE::string) n_dup,
  sum(iff(try_to_double(VALUE::string) is null, 1, 0)) n_val_null, max(try_to_double(VALUE::string)) vmax
from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC
group by 1, 2, 3, 4 order by 1, 2, 3, 4;

-- S05 WIND shape: status x technology, generators, MW, year range, source files, sentinels in hub height and design speed (0.5s, 4 rows)
select STATUS, TECHNOLOGY, count(*) n, count(distinct PLANT_CODE::string || '|' || GENERATOR_ID::string) n_gen_keys,
  round(sum(try_to_double(NAMEPLATE_CAPACITY_MW::string)), 1) mw, min(OPERATING_YEAR) y0, max(OPERATING_YEAR) y1,
  count(distinct _SRC_FILE) n_files, max(_SRC_FILE) a_file,
  sum(iff(try_to_double(TURBINE_HUB_HEIGHT_FEET::string) is null, 1, 0)) n_hub_null,
  sum(iff(try_to_double(TURBINE_HUB_HEIGHT_FEET::string) <= 0, 1, 0)) n_hub_le0,
  sum(iff(try_to_double(DESIGN_WIND_SPEED_MPH::string) is null, 1, 0)) n_speed_null,
  sum(iff(try_to_double(NUMBER_OF_TURBINES::string) is null or try_to_double(NUMBER_OF_TURBINES::string) <= 0, 1, 0)) n_turb_bad,
  count(distinct PREDOMINANT_TURBINE_MANUFACTURER) n_makers, count(distinct WIND_QUALITY_CLASS) n_wqc
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_2_WIND
group by 1, 2 order by 1, 2;

-- S06 WIND by operating year: generators, MW, turbines, median hub height, median MW per turbine, makers (0.2s, 41 rows)
select try_to_number(OPERATING_YEAR::string) oy, count(*) n, round(sum(try_to_double(NAMEPLATE_CAPACITY_MW::string)), 0) mw,
  sum(try_to_double(NUMBER_OF_TURBINES::string)) turbines,
  median(try_to_double(TURBINE_HUB_HEIGHT_FEET::string)) hub_med, max(try_to_double(TURBINE_HUB_HEIGHT_FEET::string)) hub_max,
  round(median(try_to_double(NAMEPLATE_CAPACITY_MW::string) / nullif(try_to_double(NUMBER_OF_TURBINES::string), 0)), 2) mw_per_turb_med,
  round(max(try_to_double(NAMEPLATE_CAPACITY_MW::string) / nullif(try_to_double(NUMBER_OF_TURBINES::string), 0)), 2) mw_per_turb_max,
  count(distinct PREDOMINANT_TURBINE_MANUFACTURER) n_makers
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_2_WIND
group by 1 order by 1;

-- S07 WIND vs 3_1 GENERATOR: wind-turbine generators in the master list by status, and whether each lands in the wind sheet; plus wind-sheet rows missing from the master (0.9s, 7 rows)
with g as (
  select try_to_number(PLANT_CODE::string) p, trim(GENERATOR_ID::string) gid, STATUS, PRIME_MOVER, try_to_double(NAMEPLATE_CAPACITY_MW::string) mw
  from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where PRIME_MOVER in ('WT', 'WS')),
w as (
  select try_to_number(PLANT_CODE::string) p, trim(GENERATOR_ID::string) gid, STATUS, try_to_double(NAMEPLATE_CAPACITY_MW::string) mw
  from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_2_WIND)
select 'master_to_wind' dir, g.PRIME_MOVER pm, g.STATUS st, count(*) n, sum(iff(w.p is not null, 1, 0)) n_land, round(sum(g.mw), 0) mw,
  round(sum(iff(w.p is not null, g.mw, 0)), 0) mw_land, sum(iff(w.p is not null and abs(w.mw - g.mw) > 0.5, 1, 0)) n_mw_disagree
from g left join w on w.p = g.p and w.gid = g.gid group by 1, 2, 3
union all
select 'wind_to_master', null, w.STATUS, count(*), sum(iff(g.p is not null, 1, 0)), round(sum(w.mw), 0), round(sum(iff(g.p is not null, w.mw, 0)), 0), null
from w left join g on g.p = w.p and g.gid = w.gid group by 1, 2, 3
order by 1, 2, 3;

-- S08 STORAGE shape: status x technology, MW, MWh, duration, charge vs nameplate, duplicates, year range (0.5s, 12 rows)
select STATUS, STORAGE_TECHNOLOGY_1 tech, count(*) n, count(distinct PLANT_CODE::string || '|' || GENERATOR_ID::string) n_keys,
  round(sum(try_to_double(NAMEPLATE_CAPACITY_MW::string)), 0) mw, round(sum(try_to_double(NAMEPLATE_ENERGY_CAPACITY_MWH::string)), 0) mwh,
  sum(iff(coalesce(try_to_double(NAMEPLATE_ENERGY_CAPACITY_MWH::string), 0) <= 0, 1, 0)) n_mwh_le0,
  round(median(try_to_double(NAMEPLATE_ENERGY_CAPACITY_MWH::string) / nullif(try_to_double(NAMEPLATE_CAPACITY_MW::string), 0)), 2) dur_med,
  sum(iff(try_to_double(MAXIMUM_CHARGE_RATE_MW::string) > 1.05 * try_to_double(NAMEPLATE_CAPACITY_MW::string), 1, 0)) n_charge_gt_np,
  sum(iff(try_to_double(MAXIMUM_DISCHARGE_RATE_MW::string) > 1.05 * try_to_double(NAMEPLATE_CAPACITY_MW::string), 1, 0)) n_dis_gt_np,
  min(OPERATING_YEAR) y0, max(OPERATING_YEAR) y1, count(distinct _SRC_FILE) n_files, max(_SRC_FILE) a_file
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_4_ENERGY_STORAGE
group by 1, 2 order by 1, 2;

-- S09 STORAGE vs 3_1 GENERATOR: storage prime movers in the master list by status, and whether each lands in the storage sheet; plus the reverse (0.5s, 12 rows)
with g as (
  select try_to_number(PLANT_CODE::string) p, trim(GENERATOR_ID::string) gid, STATUS, PRIME_MOVER, try_to_double(NAMEPLATE_CAPACITY_MW::string) mw
  from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where PRIME_MOVER in ('BA', 'ES', 'FW', 'CE', 'PS')),
s as (
  select try_to_number(PLANT_CODE::string) p, trim(GENERATOR_ID::string) gid, STATUS, try_to_double(NAMEPLATE_CAPACITY_MW::string) mw
  from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_4_ENERGY_STORAGE)
select 'master_to_storage' dir, g.PRIME_MOVER pm, g.STATUS st, count(*) n, sum(iff(s.p is not null, 1, 0)) n_land, round(sum(g.mw), 0) mw,
  round(sum(iff(s.p is not null, g.mw, 0)), 0) mw_land
from g left join s on s.p = g.p and s.gid = g.gid group by 1, 2, 3
union all
select 'storage_to_master', null, s.STATUS, count(*), sum(iff(g.p is not null, 1, 0)), round(sum(s.mw), 0), round(sum(iff(g.p is not null, s.mw, 0)), 0)
from s left join g on g.p = s.p and g.gid = s.gid group by 1, 2, 3
order by 1, 2, 3;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- S10 EMBER country-year pivot: generation by fuel, shares, CO2, demand, imports, capacity, and coal YoY columns (all areas, all years) (1.3s, 5726 rows)
with e as (
  select COUNTRY, ISO_3_CODE, AREA_TYPE, CONTINENT, EMBER_REGION, YEAR, VALUE, YOY_ABSOLUTE_CHANGE, YOY_PCT_CHANGE,
    CATEGORY || '|' || SUBCATEGORY || '|' || VARIABLE || '|' || UNIT k
  from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC)
select COUNTRY, ISO_3_CODE, AREA_TYPE, CONTINENT, EMBER_REGION, YEAR,
  max(iff(k = 'Electricity generation|Total|Total Generation|TWh', VALUE, null)) gen_twh,
  max(iff(k = 'Electricity generation|Fuel|Coal|TWh', VALUE, null)) coal_twh,
  max(iff(k = 'Electricity generation|Fuel|Gas|TWh', VALUE, null)) gas_twh,
  max(iff(k = 'Electricity generation|Fuel|Other Fossil|TWh', VALUE, null)) othfos_twh,
  max(iff(k = 'Electricity generation|Fuel|Hydro|TWh', VALUE, null)) hydro_twh,
  max(iff(k = 'Electricity generation|Fuel|Nuclear|TWh', VALUE, null)) nuclear_twh,
  max(iff(k = 'Electricity generation|Fuel|Wind|TWh', VALUE, null)) wind_twh,
  max(iff(k = 'Electricity generation|Fuel|Solar|TWh', VALUE, null)) solar_twh,
  max(iff(k = 'Electricity generation|Fuel|Bioenergy|TWh', VALUE, null)) bio_twh,
  max(iff(k = 'Electricity generation|Aggregate fuel|Fossil|TWh', VALUE, null)) fossil_twh,
  max(iff(k = 'Electricity generation|Aggregate fuel|Clean|TWh', VALUE, null)) clean_twh,
  max(iff(k = 'Electricity generation|Aggregate fuel|Wind and Solar|TWh', VALUE, null)) ws_twh,
  max(iff(k = 'Electricity generation|Fuel|Coal|%', VALUE, null)) coal_pct,
  max(iff(k = 'Electricity generation|Fuel|Gas|%', VALUE, null)) gas_pct,
  max(iff(k = 'Electricity generation|Fuel|Hydro|%', VALUE, null)) hydro_pct,
  max(iff(k = 'Electricity generation|Fuel|Nuclear|%', VALUE, null)) nuclear_pct,
  max(iff(k = 'Electricity generation|Aggregate fuel|Fossil|%', VALUE, null)) fossil_pct,
  max(iff(k = 'Electricity generation|Aggregate fuel|Clean|%', VALUE, null)) clean_pct,
  max(iff(k = 'Electricity generation|Aggregate fuel|Wind and Solar|%', VALUE, null)) ws_pct,
  max(iff(k = 'Power sector emissions|CO2 intensity|CO2 intensity|gCO2/kWh', VALUE, null)) co2_int,
  max(iff(k = 'Power sector emissions|Total|Total emissions|mtCO2', VALUE, null)) co2_mt,
  max(iff(k = 'Electricity demand|Demand|Demand|TWh', VALUE, null)) demand_twh,
  max(iff(k = 'Electricity demand|Demand per capita|Demand per capita|MWh', VALUE, null)) demand_pc,
  max(iff(k = 'Electricity imports|Electricity imports|Net Imports|TWh', VALUE, null)) net_imp,
  max(iff(k = 'Capacity|Fuel|Coal|GW', VALUE, null)) cap_coal,
  max(iff(k = 'Capacity|Fuel|Gas|GW', VALUE, null)) cap_gas,
  max(iff(k = 'Capacity|Fuel|Solar|GW', VALUE, null)) cap_solar,
  max(iff(k = 'Capacity|Fuel|Wind|GW', VALUE, null)) cap_wind,
  max(iff(k = 'Capacity|Fuel|Hydro|GW', VALUE, null)) cap_hydro,
  max(iff(k = 'Capacity|Aggregate fuel|Fossil|GW', VALUE, null)) cap_fossil,
  max(iff(k = 'Capacity|Aggregate fuel|Clean|GW', VALUE, null)) cap_clean,
  max(iff(k = 'Electricity generation|Fuel|Coal|TWh', YOY_ABSOLUTE_CHANGE, null)) coal_yoy_abs,
  max(iff(k = 'Electricity generation|Fuel|Coal|TWh', YOY_PCT_CHANGE, null)) coal_yoy_pct,
  max(iff(k = 'Electricity generation|Total|Total Generation|TWh', YOY_ABSOLUTE_CHANGE, null)) gen_yoy_abs,
  count(*) n_rows
from e
group by 1, 2, 3, 4, 5, 6
order by 3, 1, 6;

-- S11 WIND full extract, with the master generator row (plans, ownership, RTO node) and the plant row (balancing authority, location) (1.6s, 1563 rows)
select w.*, g.OWNERSHIP g_ownership, g.PLANNED_RETIREMENT_YEAR g_ret_year, g.PLANNED_REPOWER_YEAR g_repower_year,
  g.OTHER_MODIFICATIONS_YEAR g_othmod_year, g.OTHER_PLANNED_MODIFICATIONS g_othmod, g.YEAR_UPRATE_OR_DERATE_COMPLETED g_uprate_year,
  g.PLANNED_NEW_NAMEPLATE_CAPACITY_MW g_new_np, g.TURBINES_OR_HYDROKINETIC_BUOYS g_turbines, g.RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC g_rto,
  p.BALANCING_AUTHORITY_CODE p_ba, p.NERC_REGION p_nerc, p.LATITUDE p_lat, p.LONGITUDE p_lon, p.CITY p_city, p.ZIP p_zip
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_2_WIND w
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g on g.PLANT_CODE = w.PLANT_CODE and trim(g.GENERATOR_ID) = trim(w.GENERATOR_ID)
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT p on p.PLANT_CODE = w.PLANT_CODE
order by w.PLANT_CODE, w.GENERATOR_ID;

-- S12 STORAGE full extract, with its own master row, the master row of the unit it directly supports, and the plant row (1.2s, 786 rows)
select s.*, g.PRIME_MOVER g_pm, g.TECHNOLOGY g_tech, g.OWNERSHIP g_ownership, g.PLANNED_RETIREMENT_YEAR g_ret_year,
  g.RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC g_rto,
  t.TECHNOLOGY t1_tech, t.PRIME_MOVER t1_pm, t.ENERGY_SOURCE_1 t1_fuel, t.NAMEPLATE_CAPACITY_MW t1_mw, t.OPERATING_YEAR t1_year, t.STATUS t1_status,
  p.BALANCING_AUTHORITY_CODE p_ba, p.NERC_REGION p_nerc, p.LATITUDE p_lat, p.LONGITUDE p_lon, p.CITY p_city, p.ZIP p_zip, p.ENERGY_STORAGE p_storage_flag
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_4_ENERGY_STORAGE s
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g on g.PLANT_CODE = s.PLANT_CODE and trim(g.GENERATOR_ID) = trim(s.GENERATOR_ID)
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR t on t.PLANT_CODE = s.DIRECT_SUPPORT_PLANT_ID_1 and trim(t.GENERATOR_ID) = trim(s.DIRECT_SUPPORT_GEN_ID_1)
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT p on p.PLANT_CODE = s.PLANT_CODE
order by s.PLANT_CODE, s.GENERATOR_ID;

-- S13 GENERATOR master rollup by state, technology, status: denominators and which EIA sheets were loaded (0.6s, 1214 rows)
select STATE, TECHNOLOGY, PRIME_MOVER, STATUS, count(*) n, round(sum(NAMEPLATE_CAPACITY_MW), 1) mw, round(sum(SUMMER_CAPACITY_MW), 1) summer_mw,
  min(OPERATING_YEAR) y0, max(OPERATING_YEAR) y1, count(PLANNED_RETIREMENT_YEAR) n_ret_planned, count(distinct _SRC_FILE) n_files, max(_SRC_FILE) a_file
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR
group by 1, 2, 3, 4
order by 1, 2, 4;

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- S14 SEC_EDGAR vs the bigger ECONOMICS__FED_US_SEC_EDGAR: do the 200 sample filings and 20 companies already sit in the 49K-row table; state of incorporation agreement (0.8s, 20 rows)
with s as (
  select replace(ACCESSIONNUMBER, '-', '') acc, try_to_number(CIK) cik, ENTITYNAME, STATEOFINCORPORATION inc, EIN
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR),
b as (
  select replace(ACCESSION_NUMBER, '-', '') acc, try_to_number(CIK) cik, max(STATE_OF_INCORPORATION) over (partition by try_to_number(CIK)) inc_b,
    max(EIN) over (partition by try_to_number(CIK)) ein_b, FILED_AT
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_US_SEC_EDGAR),
bc as (select cik, max(inc_b) inc_b, max(ein_b) ein_b, count(*) n_b, min(FILED_AT) b_min, max(FILED_AT) b_max from b group by 1)
select s.cik, max(s.ENTITYNAME) name, count(*) n_sample, sum(iff(b.acc is not null, 1, 0)) n_acc_in_big,
  max(bc.n_b) n_big_rows, max(bc.b_min) big_min, max(bc.b_max) big_max, max(s.inc) inc_sample, max(bc.inc_b) inc_big, max(s.EIN) ein_sample, max(bc.ein_b) ein_big
from s
left join (select distinct acc from b) b on b.acc = s.acc
left join bc on bc.cik = s.cik
group by 1 order by 1;

-- S15 EMBER raw rows behind the lead: US and World coal, gas, total generation and power CO2, 2023-2025, straight from the table (0.2s, 30 rows)
select COUNTRY, YEAR, CATEGORY, SUBCATEGORY, VARIABLE, UNIT, VALUE, YOY_ABSOLUTE_CHANGE, YOY_PCT_CHANGE
from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC
where COUNTRY in ('United States of America', 'World') and YEAR between 2023 and 2025
  and ((CATEGORY = 'Electricity generation' and VARIABLE in ('Coal', 'Gas', 'Total Generation', 'Wind and Solar') and UNIT = 'TWh')
    or (CATEGORY = 'Power sector emissions' and VARIABLE = 'Total emissions'))
order by COUNTRY, VARIABLE, YEAR;
