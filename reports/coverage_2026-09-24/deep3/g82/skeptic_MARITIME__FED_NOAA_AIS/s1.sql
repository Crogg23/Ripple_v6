-- Re-derive headline at hull (IMO) level, not MMSI+IMO pair. Variants: age cut 93/94/95, length>=150m, drop US-flag MIDs, binding lists only (drop UA-only)
with a as (select MMSI, regexp_replace(IMO_NORMALIZED,'[^0-9]','') imo, max(VESSEL_TYPE_CODE) vt, max(LENGTH_METERS) len, count(*) pings
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS where IMO_NORMALIZED is not null and IMO_NORMALIZED <> '' group by 1,2),
av as (select * from a where length(imo)=7 and imo <> '0000000' and
         mod(7*try_to_number(substr(imo,1,1)) + 6*try_to_number(substr(imo,2,1)) + 5*try_to_number(substr(imo,3,1)) + 4*try_to_number(substr(imo,4,1))
             + 3*try_to_number(substr(imo,5,1)) + 2*try_to_number(substr(imo,6,1)), 10) = try_to_number(substr(imo,7,1))),
os as (select regexp_replace(t.value::string,'[^0-9]','') d,
         max(iff(o.DATASETS ilike '%OFAC%' or o.DATASETS ilike '%EU %' or o.DATASETS ilike '%EU Council%' or o.DATASETS ilike '%UK %' or o.DATASETS ilike '%OFSI%'
                 or o.DATASETS ilike '%UK FCDO%' or o.DATASETS ilike '%Canad%' or o.DATASETS ilike '%Australia%', 1, 0)) gov
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o, lateral flatten(input => split(o.IDENTIFIERS, ';')) t
       where o.ENTITY_TYPE = 'Vessel' and (o.DATASETS ilike '%sanction%' or o.DATASETS ilike '%OFAC%' or o.DATASETS ilike '%Specially Designated%')
         and length(regexp_replace(t.value::string,'[^0-9]','')) = 7 group by 1),
ofac as (select distinct regexp_replace(IMO_NUMBER,'[^0-9]','') d from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN where IS_VESSEL),
j as (select av.*, iff(os.d is not null or ofac.d is not null,1,0) hit, iff(coalesce(os.gov,0)=1 or ofac.d is not null,1,0) govhit,
        case when vt between 80 and 89 then 'tanker' when vt between 70 and 79 then 'cargo' else 'other' end grp,
        iff(left(MMSI,3) in ('338','366','367','368','369'),1,0) usflag
      from av left join os on av.imo = os.d left join ofac on av.imo = ofac.d),
i as (select imo, count(distinct MMSI) n_mmsi, count(distinct grp) n_grp, max(grp) grp, max(len) len, max(hit) hit, max(govhit) govhit, max(usflag) usflag
      from j group by imo),
cuts as (select column1 cut from values (9300000),(9400000),(9500000))
select 'meta' k, 'pairs' grp, null cut, null band, count(*) n, sum(hit) hits, sum(govhit) gov, count(distinct imo) extra from j
union all select 'meta', 'imo_with_2plus_mmsi', null, null, count_if(n_mmsi>1), count_if(n_mmsi>1 and hit=1), count_if(n_grp>1), count(*) from i
union all select 'imo_band', grp, cut, iff(to_number(imo) < cut, 'old', 'new'), count(*), sum(hit), sum(govhit), null from i, cuts group by 2,3,4
union all select 'tanker_len150_nonUS', grp, 9400000, iff(to_number(imo) < 9400000, 'old', 'new'), count(*), sum(hit), sum(govhit), null
  from i where len >= 150 and usflag = 0 group by 2,3,4
union all select 'tanker_usflag', grp, 9400000, iff(to_number(imo) < 9400000, 'old', 'new'), count(*), sum(hit), sum(govhit), null
  from i where usflag = 1 and grp='tanker' group by 2,3,4
order by 1,2,3,4
