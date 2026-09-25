-- S01 SEC_EDGAR: per company rows, forms, filing-date range, EIN shape, duplicate accessions
select CIK, ENTITYNAME, count(*) n, count(distinct ACCESSIONNUMBER) n_acc, min(FILEDAT) filed_min, max(FILEDAT) filed_max,
  listagg(distinct FORM, ',') within group (order by FORM) forms, max(EIN) ein, max(length(EIN)) ein_len,
  max(STATEOFINCORPORATION) inc, max(SICDESCRIPTION) sic,
  (select count(*) - count(distinct ACCESSIONNUMBER) from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR) dup_acc_total
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR
group by 1, 2 order by 1;

-- S02 FAO_FAOSTAT: the whole 69-row catalog, oldest update first
select DATASETCODE, DATASETNAME, DATEUPDATE, FILEROWS, FILESIZE, left(TOPIC, 40) topic40
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT
order by try_to_timestamp(DATEUPDATE::string) nulls first, DATASETCODE;

-- S03 EMBER shape by year and area type: rows, areas, series, runs, flag fill
select left(DATE::string, 4) yr, AREA_TYPE, count(*) n, count(distinct COUNTRY) n_areas,
  count(distinct CATEGORY || '|' || SUBCATEGORY || '|' || VARIABLE || '|' || UNIT) n_series,
  count(distinct _SOURCE_RUN_ID) n_runs, count(IS_EU) n_is_eu, count(IS_OECD) n_is_oecd, count(IS_G20) n_is_g20,
  count(*) - count(distinct COUNTRY || '|' || DATE::string || '|' || CATEGORY || '|' || SUBCATEGORY || '|' || VARIABLE || '|' || UNIT) n_dup_keys
from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC
group by 1, 2 order by 1, 2;

-- S04 EMBER series list: every category/subcategory/variable/unit with rows, areas, year range, duplicate keys
select CATEGORY, SUBCATEGORY, VARIABLE, UNIT, count(*) n, count(distinct COUNTRY) n_areas,
  min(left(DATE::string, 4)) y0, max(left(DATE::string, 4)) y1,
  count(*) - count(distinct COUNTRY || '|' || DATE::string) n_dup,
  sum(iff(try_to_double(VALUE::string) is null, 1, 0)) n_val_null, max(try_to_double(VALUE::string)) vmax
from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC
group by 1, 2, 3, 4 order by 1, 2, 3, 4;

-- S05 WIND shape: status x technology, generators, MW, year range, source files, sentinels in hub height and design speed
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

-- S06 WIND by operating year: generators, MW, turbines, median hub height, median MW per turbine, makers
select try_to_number(OPERATING_YEAR::string) oy, count(*) n, round(sum(try_to_double(NAMEPLATE_CAPACITY_MW::string)), 0) mw,
  sum(try_to_double(NUMBER_OF_TURBINES::string)) turbines,
  median(try_to_double(TURBINE_HUB_HEIGHT_FEET::string)) hub_med, max(try_to_double(TURBINE_HUB_HEIGHT_FEET::string)) hub_max,
  round(median(try_to_double(NAMEPLATE_CAPACITY_MW::string) / nullif(try_to_double(NUMBER_OF_TURBINES::string), 0)), 2) mw_per_turb_med,
  round(max(try_to_double(NAMEPLATE_CAPACITY_MW::string) / nullif(try_to_double(NUMBER_OF_TURBINES::string), 0)), 2) mw_per_turb_max,
  count(distinct PREDOMINANT_TURBINE_MANUFACTURER) n_makers
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_2_WIND
group by 1 order by 1;

-- S07 WIND vs 3_1 GENERATOR: wind-turbine generators in the master list by status, and whether each lands in the wind sheet; plus wind-sheet rows missing from the master
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

-- S08 STORAGE shape: status x technology, MW, MWh, duration, charge vs nameplate, duplicates, year range
select STATUS, STORAGE_TECHNOLOGY_1 tech, count(*) n, count(distinct PLANT_CODE::string || '|' || GENERATOR_ID::string) n_keys,
  round(sum(try_to_double(NAMEPLATE_CAPACITY_MW::string)), 0) mw, round(sum(try_to_double(NAMEPLATE_ENERGY_CAPACITY_MWH::string)), 0) mwh,
  sum(iff(coalesce(try_to_double(NAMEPLATE_ENERGY_CAPACITY_MWH::string), 0) <= 0, 1, 0)) n_mwh_le0,
  round(median(try_to_double(NAMEPLATE_ENERGY_CAPACITY_MWH::string) / nullif(try_to_double(NAMEPLATE_CAPACITY_MW::string), 0)), 2) dur_med,
  sum(iff(try_to_double(MAXIMUM_CHARGE_RATE_MW::string) > 1.05 * try_to_double(NAMEPLATE_CAPACITY_MW::string), 1, 0)) n_charge_gt_np,
  sum(iff(try_to_double(MAXIMUM_DISCHARGE_RATE_MW::string) > 1.05 * try_to_double(NAMEPLATE_CAPACITY_MW::string), 1, 0)) n_dis_gt_np,
  min(OPERATING_YEAR) y0, max(OPERATING_YEAR) y1, count(distinct _SRC_FILE) n_files, max(_SRC_FILE) a_file
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_4_ENERGY_STORAGE
group by 1, 2 order by 1, 2;

-- S09 STORAGE vs 3_1 GENERATOR: storage prime movers in the master list by status, and whether each lands in the storage sheet; plus the reverse
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
