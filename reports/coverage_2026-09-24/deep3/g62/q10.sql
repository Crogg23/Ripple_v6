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
order by 1, 2
