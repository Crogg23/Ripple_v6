-- AIS traps: duplicate pings, flag country by MMSI prefix, malformed MMSIs, MMSIs broadcasting several ship names
with s as (select MMSI, count(*) n, count(distinct BASE_DATETIME) nt, count(distinct VESSEL_NAME) nn, max(TRANSCEIVER_CLASS) tc,
             max(VESSEL_TYPE_CODE) vt, max(VESSEL_NAME) vname, min(VESSEL_NAME) vname2, count(distinct regexp_replace(IMO_NORMALIZED,'[^0-9]','')) nimo
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 1)
select 'dup' k, count(*)::text a, sum(n)::text b, sum(n-nt)::text c, count_if(n>nt)::text d, count_if(nn>1)::text e, count_if(nimo>1)::text f, median(n)::text g, null h
from s
union all
(select 'mid', left(MMSI,3), count(*)::text, sum(n)::text, count_if(tc='A')::text, max(vname), null, null, null from s where regexp_like(MMSI,'[2-7][0-9]{8}')
 group by 2 order by count(*) desc limit 25)
union all
(select 'bad', left(MMSI,2)||' len'||length(MMSI), count(*)::text, sum(n)::text, max(vname), min(vname), null, null, null from s where not regexp_like(MMSI,'[2-7][0-9]{8}')
 group by 2 order by sum(n) desc limit 10)
union all
(select 'multiname', MMSI, nn::text, n::text, vname, vname2, nimo::text, tc, vt::text from s order by nn desc limit 12)
