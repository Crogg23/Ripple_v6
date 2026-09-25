-- AIS x sanctions, sharpened: IMO matches only (checksum-valid), sanctions datasets only, with the denominator: every ship type and IMO age band seen that week
with a as (select MMSI, regexp_replace(IMO_NORMALIZED,'[^0-9]','') imo, count(*) pings, max(VESSEL_NAME) vname, max(VESSEL_TYPE_CODE) vt, max(LENGTH_METERS) len,
             min(BASE_DATETIME) t0, max(BASE_DATETIME) t1, count_if(SPEED_OVER_GROUND < 0.5) still,
             round(avg(iff(SPEED_OVER_GROUND < 0.5, LATITUDE, null)),2) still_lat, round(avg(iff(SPEED_OVER_GROUND < 0.5, LONGITUDE, null)),2) still_lon,
             round(min(LATITUDE),1) la0, round(max(LATITUDE),1) la1, round(min(LONGITUDE),1) lo0, round(max(LONGITUDE),1) lo1
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 1,2),
av as (select * from a where length(imo)=7 and imo <> '0000000' and
         mod(7*try_to_number(substr(imo,1,1)) + 6*try_to_number(substr(imo,2,1)) + 5*try_to_number(substr(imo,3,1)) + 4*try_to_number(substr(imo,4,1))
             + 3*try_to_number(substr(imo,5,1)) + 2*try_to_number(substr(imo,6,1)), 10) = try_to_number(substr(imo,7,1))),
os as (select regexp_replace(t.value::string,'[^0-9]','') d, min(o.FIRST_SEEN) fs, max(o.NAME) lname,
         max(iff(o.DATASETS ilike '%OFAC%', 'US', '')) || max(iff(o.DATASETS ilike '%EU %' or o.DATASETS ilike '%EU Council%', ' EU', '')) ||
         max(iff(o.DATASETS ilike '%UK %' or o.DATASETS ilike '%OFSI%' or o.DATASETS ilike '%UK FCDO%', ' UK', '')) || max(iff(o.DATASETS ilike '%Canad%', ' CA', '')) ||
         max(iff(o.DATASETS ilike '%Australia%', ' AU', '')) || max(iff(o.DATASETS ilike '%Ukraine War%', ' UA', '')) lists
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o, lateral flatten(input => split(o.IDENTIFIERS, ';')) t
       where o.ENTITY_TYPE = 'Vessel' and (o.DATASETS ilike '%sanction%' or o.DATASETS ilike '%OFAC%' or o.DATASETS ilike '%Specially Designated%')
         and length(regexp_replace(t.value::string,'[^0-9]','')) = 7
       group by 1),
ofac as (select regexp_replace(IMO_NUMBER,'[^0-9]','') d, max(SDN_NAME) sdn, max(PROGRAM) prog from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN where IS_VESSEL group by 1),
j as (select av.*, os.fs, os.lname, os.lists, ofac.sdn, ofac.prog, (os.d is not null or ofac.d is not null) hit,
        case when vt between 80 and 89 then 'tanker' when vt between 70 and 79 then 'cargo' else 'other' end grp, iff(imo < '9400000', 'IMO<94', 'IMO>=94') age
      from av left join os on av.imo = os.d left join ofac on av.imo = ofac.d)
select 'denom' k, grp a, age b, count(*)::text c, count_if(hit)::text d, round(100*count_if(hit)/count(*),2)::text e, null f, null g, null h, null i, null l, null o
from j group by 2,3
union all
(select 'hit', MMSI||' '||imo, vname, coalesce(sdn, lname), grp||' '||vt||' '||len||'m', pings::text, t0::text||' to '||t1::text,
   la0||','||lo0||' to '||la1||','||lo1, still::text||' still @'||still_lat||','||still_lon, fs::text, lists, prog
 from j where hit order by fs)
