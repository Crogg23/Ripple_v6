-- AIS join: ships in U.S. waters Jan 1-8 2024 whose IMO (checksum-valid) or MMSI appears on OFAC SDN or OpenSanctions vessel lists
with a as (select MMSI, regexp_replace(IMO_NORMALIZED,'[^0-9]','') imo, count(*) pings, count(distinct VESSEL_NAME) nnames, max(VESSEL_NAME) vname,
             min(BASE_DATETIME) t0, max(BASE_DATETIME) t1, round(min(LATITUDE),1) la0, round(max(LATITUDE),1) la1,
             round(min(LONGITUDE),1) lo0, round(max(LONGITUDE),1) lo1, max(VESSEL_TYPE_CODE) vt, max(LENGTH_METERS) len, max(CALL_SIGN) cs
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 1,2),
av as (select *, length(imo)=7 and imo <> '0000000' and
         mod(7*try_to_number(substr(imo,1,1)) + 6*try_to_number(substr(imo,2,1)) + 5*try_to_number(substr(imo,3,1)) + 4*try_to_number(substr(imo,4,1))
             + 3*try_to_number(substr(imo,5,1)) + 2*try_to_number(substr(imo,6,1)), 10) = try_to_number(substr(imo,7,1)) imo_ok
       from a),
ofac as (select regexp_replace(IMO_NUMBER,'[^0-9]','') imo, SDN_NAME, PROGRAM, VESSEL_FLAG from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN where IS_VESSEL),
os as (select o.NAME, o.DATASETS, o.FIRST_SEEN, regexp_replace(t.value::string,'[^0-9]','') d
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o, lateral flatten(input => split(o.IDENTIFIERS, ';')) t
       where o.ENTITY_TYPE = 'Vessel' and o.IDENTIFIERS is not null and o.IDENTIFIERS <> ''),
m as (
  select 'ofac_imo' via, av.*, ofac.SDN_NAME lname, ofac.PROGRAM prog, ofac.VESSEL_FLAG flag, null::text ds, null::text fs from av join ofac on av.imo = ofac.imo where av.imo_ok
  union all
  select 'os_imo', av.*, os.NAME, null, null, left(os.DATASETS,160), os.FIRST_SEEN::text from av join os on av.imo = os.d where av.imo_ok and length(os.d) = 7
  union all
  select 'os_mmsi', av.*, os.NAME, null, null, left(os.DATASETS,160), os.FIRST_SEEN::text from av join os on av.MMSI = os.d where length(os.d) = 9)
select via, count(*) over (partition by via) n_via, (select count_if(imo_ok) from av) n_imo_ok, (select count_if(length(imo)=7 and not imo_ok) from av) n_imo_bad,
  MMSI, imo, vname, lname, nnames, pings, t0, t1, la0, la1, lo0, lo1, vt, len, cs, prog, flag, ds, fs
from m order by via, pings desc limit 150
