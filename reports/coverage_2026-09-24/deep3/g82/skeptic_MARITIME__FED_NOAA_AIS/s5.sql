-- Tankers: hit rate for ships that moored/anchored vs only passed through; tankers lost from the denominator for lacking a valid IMO; MMSI-route hits the builder never saw (q09 LIMIT 150 cut them)
with a as (select MMSI, max(regexp_replace(IMO_NORMALIZED,'[^0-9]','')) imo, max(VESSEL_TYPE_CODE) vt, max(LENGTH_METERS) len,
             count_if(NAV_STATUS = '5') moored, count_if(NAV_STATUS in ('1','5')) am
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 1),
b as (select *, coalesce(length(imo)=7 and imo <> '0000000' and
         mod(7*try_to_number(substr(imo,1,1)) + 6*try_to_number(substr(imo,2,1)) + 5*try_to_number(substr(imo,3,1)) + 4*try_to_number(substr(imo,4,1))
             + 3*try_to_number(substr(imo,5,1)) + 2*try_to_number(substr(imo,6,1)), 10) = try_to_number(substr(imo,7,1)), false) imo_ok
      from a where vt between 80 and 89),
os as (select regexp_replace(t.value::string,'[^0-9]','') d,
         max(iff(o.DATASETS ilike '%OFAC%' or o.DATASETS ilike '%EU Council%' or o.DATASETS ilike '%UK FCDO%' or o.DATASETS ilike '%Canad%' or o.DATASETS ilike '%Australia%', 1, 0)) gov
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o, lateral flatten(input => split(o.IDENTIFIERS, ';')) t
       where o.ENTITY_TYPE = 'Vessel' and (o.DATASETS ilike '%sanction%' or o.DATASETS ilike '%OFAC%') group by 1),
j as (select b.*, iff(oi.d is not null, 1, 0) hit, coalesce(oi.gov, 0) gov, iff(om.d is not null, 1, 0) mmsi_hit, coalesce(om.gov,0) mmsi_gov
      from b left join os oi on b.imo_ok and b.imo = oi.d left join os om on b.MMSI = om.d)
select iff(imo_ok, iff(imo < '9400000', 'old', 'new'), 'no_valid_imo') band,
  case when moored > 0 then 'moored' when am > 0 then 'anchored_only' else 'passing' end stop,
  count(*) n, count_if(len >= 150) n_150m, sum(hit) hits, sum(gov) gov_hits, sum(mmsi_hit) mmsi_hits, sum(mmsi_gov) mmsi_gov_hits
from j group by 1, 2 order by 1, 2
