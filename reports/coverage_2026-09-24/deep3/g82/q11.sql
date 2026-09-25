-- AIS identity check: one MMSI reported in two places 0.5+ degrees apart (~55 km) inside the same minute = two radios sharing one ID
with p as (select MMSI, date_trunc('minute', BASE_DATETIME) mi, max(LATITUDE)-min(LATITUDE) dlat, max(LONGITUDE)-min(LONGITUDE) dlon,
             max(VESSEL_NAME) vname, min(VESSEL_NAME) vname2
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 1,2 having count(*) > 1),
q as (select MMSI, count(*) multi_minutes, count_if(dlat >= 0.5 or dlon >= 0.5) split_minutes, max(vname) vname, min(vname2) vname2, max(greatest(dlat,dlon)) maxd
      from p group by 1)
select 'sum' k, count(*)::text a, count_if(split_minutes>0)::text b, count_if(split_minutes>=60)::text c, sum(split_minutes)::text d, null e, null f, null g
from q
union all
(select 'mmsi', MMSI, split_minutes::text, multi_minutes::text, vname, vname2, round(maxd,1)::text, left(MMSI,3) from q where split_minutes > 0 order by split_minutes desc limit 25)
