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
from s left join g on g.PLANT_CODE=s.PLANT_CODE and g.GENERATOR_ID=s.GENERATOR_ID
