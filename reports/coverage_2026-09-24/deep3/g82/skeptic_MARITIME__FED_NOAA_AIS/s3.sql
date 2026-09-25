-- For the 16 hit MMSIs: moored/anchored pings and where, draft first vs last (loading or discharging), nav status mix
select MMSI, max(VESSEL_NAME) vname, count(*) pings,
  count_if(NAV_STATUS in ('1','5')) anch_moored, count_if(NAV_STATUS = '5') moored, count_if(SPEED_OVER_GROUND < 0.5) still,
  round(median(iff(NAV_STATUS in ('1','5'), LATITUDE, null)),2) am_lat, round(median(iff(NAV_STATUS in ('1','5'), LONGITUDE, null)),2) am_lon,
  round(median(iff(NAV_STATUS = '5', LATITUDE, null)),2) m_lat, round(median(iff(NAV_STATUS = '5', LONGITUDE, null)),2) m_lon,
  min_by(DRAFT_METERS, BASE_DATETIME) draft_first, max_by(DRAFT_METERS, BASE_DATETIME) draft_last, min(DRAFT_METERS) dmin, max(DRAFT_METERS) dmax,
  min_by(LATITUDE, BASE_DATETIME)||','||min_by(LONGITUDE, BASE_DATETIME) first_pos, max_by(LATITUDE, BASE_DATETIME)||','||max_by(LONGITUDE, BASE_DATETIME) last_pos,
  listagg(distinct NAV_STATUS, ',') statuses
from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS
where MMSI in ('636017265','538008370','236728000','538006916','240575000','249577000','538008235','538008759','538006203','311000138','636016274','229903000','538090308','636017066','241326000','215193000')
group by 1 order by anch_moored desc
