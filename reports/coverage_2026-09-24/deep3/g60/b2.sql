-- S10 EMBER country-year pivot: generation by fuel, shares, CO2, demand, imports, capacity, and coal YoY columns (all areas, all years)
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

-- S11 WIND full extract, with the master generator row (plans, ownership, RTO node) and the plant row (balancing authority, location)
select w.*, g.OWNERSHIP g_ownership, g.PLANNED_RETIREMENT_YEAR g_ret_year, g.PLANNED_REPOWER_YEAR g_repower_year,
  g.OTHER_MODIFICATIONS_YEAR g_othmod_year, g.OTHER_PLANNED_MODIFICATIONS g_othmod, g.YEAR_UPRATE_OR_DERATE_COMPLETED g_uprate_year,
  g.PLANNED_NEW_NAMEPLATE_CAPACITY_MW g_new_np, g.TURBINES_OR_HYDROKINETIC_BUOYS g_turbines, g.RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC g_rto,
  p.BALANCING_AUTHORITY_CODE p_ba, p.NERC_REGION p_nerc, p.LATITUDE p_lat, p.LONGITUDE p_lon, p.CITY p_city, p.ZIP p_zip
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_2_WIND w
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g on g.PLANT_CODE = w.PLANT_CODE and trim(g.GENERATOR_ID) = trim(w.GENERATOR_ID)
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT p on p.PLANT_CODE = w.PLANT_CODE
order by w.PLANT_CODE, w.GENERATOR_ID;

-- S12 STORAGE full extract, with its own master row, the master row of the unit it directly supports, and the plant row
select s.*, g.PRIME_MOVER g_pm, g.TECHNOLOGY g_tech, g.OWNERSHIP g_ownership, g.PLANNED_RETIREMENT_YEAR g_ret_year,
  g.RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC g_rto,
  t.TECHNOLOGY t1_tech, t.PRIME_MOVER t1_pm, t.ENERGY_SOURCE_1 t1_fuel, t.NAMEPLATE_CAPACITY_MW t1_mw, t.OPERATING_YEAR t1_year, t.STATUS t1_status,
  p.BALANCING_AUTHORITY_CODE p_ba, p.NERC_REGION p_nerc, p.LATITUDE p_lat, p.LONGITUDE p_lon, p.CITY p_city, p.ZIP p_zip, p.ENERGY_STORAGE p_storage_flag
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_4_ENERGY_STORAGE s
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g on g.PLANT_CODE = s.PLANT_CODE and trim(g.GENERATOR_ID) = trim(s.GENERATOR_ID)
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR t on t.PLANT_CODE = s.DIRECT_SUPPORT_PLANT_ID_1 and trim(t.GENERATOR_ID) = trim(s.DIRECT_SUPPORT_GEN_ID_1)
left join LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT p on p.PLANT_CODE = s.PLANT_CODE
order by s.PLANT_CODE, s.GENERATOR_ID;

-- S13 GENERATOR master rollup by state, technology, status: denominators and which EIA sheets were loaded
select STATE, TECHNOLOGY, PRIME_MOVER, STATUS, count(*) n, round(sum(NAMEPLATE_CAPACITY_MW), 1) mw, round(sum(SUMMER_CAPACITY_MW), 1) summer_mw,
  min(OPERATING_YEAR) y0, max(OPERATING_YEAR) y1, count(PLANNED_RETIREMENT_YEAR) n_ret_planned, count(distinct _SRC_FILE) n_files, max(_SRC_FILE) a_file
from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR
group by 1, 2, 3, 4
order by 1, 2, 4;
