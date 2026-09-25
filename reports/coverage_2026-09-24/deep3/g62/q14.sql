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
  from k where peer_n>=5 and cf<peer_cf/2 and mw>=20 order by mw desc limit 40)
