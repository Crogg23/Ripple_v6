-- AIS: profile in one pass. Days, ships, sentinels (SOG 102.3, COG >= 360, heading null), IMO filler, bad coordinates, MMSI shape
select 'profile' k, count(*)::text a, count(distinct MMSI)::text b, count_if(SPEED_OVER_GROUND >= 102.2)::text c,
  count_if(COURSE_OVER_GROUND >= 360)::text d, count_if(HEADING is null)::text e,
  count_if(IMO_NORMALIZED is null or IMO_NORMALIZED='')::text f, count(distinct IMO_NORMALIZED)::text g,
  count_if(LATITUDE not between -90 and 90 or LONGITUDE not between -180 and 180)::text h,
  count_if(not regexp_like(MMSI, '[2-7][0-9]{8}'))::text i, count(distinct SOURCE_FILE)::text j, count(distinct _SOURCE_RUN_ID)::text l
from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS
union all
select 'day', DATE::text, count(*)::text, count(distinct MMSI)::text, count_if(SPEED_OVER_GROUND >= 102.2)::text, min(BASE_DATETIME)::text, max(BASE_DATETIME)::text,
  count(distinct SOURCE_FILE)::text, null,null,null,null
from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 2
