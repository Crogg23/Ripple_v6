-- deep3 / g82: proper look at five glance-only tables, 2026-09-24
-- Tables: LABOR__FED_MSHA_MINES, LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO, MARITIME__FED_NOAA_AIS,
--         MONEY__DEBT_REPAYMENT_CLIFF, REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
-- Door: Python (connect/db.py) via g82/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g82/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- MSHA mines: profile. Keys, status values, active flag agreement, coords, quoted-value trap, employees
select 'profile' k, count(*)::text a, count(distinct MINE_ID)::text b, count_if(MINE_ID like '"%')::text c,
  count_if(LATITUDE is null or LATITUDE=0)::text d, count_if(LONGITUDE>0)::text e,
  sum(NO_EMPLOYEES)::text f, count_if(IS_ACTIVE)::text g, min(CURRENT_STATUS_DT)::text h, max(CURRENT_STATUS_DT)::text i,
  count(distinct CURRENT_CONTROLLER_ID)::text j, count(distinct CURRENT_OPERATOR_ID)::text l
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES
union all
select 'status', CURRENT_MINE_STATUS, count(*)::text, count_if(IS_ACTIVE)::text, count_if(COAL_METAL_IND='C')::text,
  count_if(NO_EMPLOYEES>0)::text, sum(NO_EMPLOYEES)::text, count_if(DAYS_PER_WEEK>0)::text,
  min(CURRENT_STATUS_DT)::text, max(CURRENT_STATUS_DT)::text, median(datediff('day',CURRENT_STATUS_DT,'2026-07-17'::date))::text, null
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 2
union all
select 'type', CURRENT_MINE_TYPE, count(*)::text, count_if(IS_ACTIVE)::text, null,null,null,null,null,null,null,null
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 2
union all
select 'statusdt_top', CURRENT_STATUS_DT::text, count(*)::text, null,null,null,null,null,null,null,null,null
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 2 qualify row_number() over (order by count(*) desc) <= 6;

-- [q02] statement 2
-- BIA tribal geo: confirm shape, test whether GEOMETRY_JSON parses to a geography, sample head of the JSON
select LAR_ID, LAR_NAME, GIS_ACRES, SHAPE_AREA, left(GEOMETRY_JSON, 160) head, length(GEOMETRY_JSON) len,
  try_to_geography(GEOMETRY_JSON) is not null parses,
  round(st_area(try_to_geography(GEOMETRY_JSON))/4046.86) acres_from_geog,
  (select count(*) from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO) n,
  (select count_if(try_to_geography(GEOMETRY_JSON) is not null) from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO) n_parse,
  (select count(distinct LAR_ID) from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO) n_id
from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO
order by GIS_ACRES desc limit 8;

-- [q03] statement 3
-- Debt cliff: profile. Years, aggregates, cliff flag, peak flag, sample of the 22 cliff rows
select 'profile' k, count(*)::text a, count(distinct COUNTRY_CODE)::text b, min(DATA_YEAR)::text c, max(DATA_YEAR)::text d,
  count_if(IS_AGGREGATE)::text e, count_if(IS_REPAYMENT_CLIFF)::text f, count_if(IS_PEAK_SERVICE_YEAR)::text g,
  count_if(TOTAL_DEBT_SERVICE_USD is null)::text h, count_if(abs(TOTAL_DEBT_SERVICE_USD - PRINCIPAL_REPAYMENT_USD - INTEREST_PAYMENT_USD) > 1e6)::text i,
  count(distinct COUNTRY_YEAR_ID)::text j
from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF
union all
select 'year', DATA_YEAR::text, count(*)::text, count_if(IS_AGGREGATE)::text, count_if(IS_REPAYMENT_CLIFF)::text, count_if(IS_PEAK_SERVICE_YEAR)::text,
  round(sum(iff(IS_AGGREGATE,0,TOTAL_DEBT_SERVICE_USD))/1e9,1)::text, null,null,null,null
from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF group by 2
union all
select 'cliff', COUNTRY_CODE||' '||COUNTRY_NAME, DATA_YEAR::text, round(TOTAL_DEBT_SERVICE_USD/1e9,2)::text, round(PREV_YEAR_TOTAL_DEBT_SERVICE_USD/1e9,2)::text,
  round(YOY_CHANGE_PCT,2)::text, IS_AGGREGATE::text, IS_PEAK_SERVICE_YEAR::text, round(PRINCIPAL_SHARE_OF_SERVICE,2)::text, null, null
from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF where IS_REPAYMENT_CLIFF;

-- [q04] statement 4
-- Federal Register: profile. Uniqueness, type mix, fill rates of the flag and date columns, per-year counts
select 'profile' k, count(*)::text a, count(distinct DOCUMENT_NUMBER)::text b, count(distinct CITATION)::text c,
  count_if(IS_SIGNIFICANT is not null)::text d, count_if(IS_SIGNIFICANT)::text e, count_if(EFFECTIVE_ON is not null)::text f,
  count_if(COMMENTS_CLOSE_ON is not null)::text g, count_if(COMMENT_WINDOW_DAYS is not null)::text h,
  count(distinct PRESIDENT)::text i, count_if(PAGE_LENGTH<>DERIVED_PAGE_COUNT)::text j
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
union all
select 'year', PUBLICATION_YEAR::text, count(*)::text, count_if(TYPE='Rule')::text, count_if(TYPE='Proposed Rule')::text,
  count_if(TYPE='Notice')::text, count_if(TYPE='Presidential Document')::text, count_if(IS_SIGNIFICANT)::text,
  count_if(IS_SIGNIFICANT is not null)::text, count_if(COMMENT_WINDOW_DAYS is not null)::text, max(PUBLICATION_DATE)::text
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS group by 2
union all
select 'type', TYPE, count(*)::text, null,null,null,null,null,null,null,null
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS group by 2
union all
select 'president', PRESIDENT, count(*)::text, min(PUBLICATION_DATE)::text, max(PUBLICATION_DATE)::text,null,null,null,null,null,null
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS group by 2;

-- [q05] statement 5
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
from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 2;

-- [q06] statement 6
-- MSHA mines: how long idle mines have been idle, which coal controllers hold the most long-idle mines, and idle share by state (peer)
with m as (select *, datediff('day', CURRENT_STATUS_DT, '2026-07-17'::date)/365.25 yrs,
             CURRENT_MINE_STATUS in ('Temporarily Idled','NonProducing') idle
           from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES)
select 'bucket' k, CURRENT_MINE_STATUS a, COAL_METAL_IND b,
  case when yrs<1 then '0-1' when yrs<3 then '1-3' when yrs<5 then '3-5' when yrs<10 then '5-10' else '10+' end c,
  count(*)::text d, sum(NO_EMPLOYEES)::text e, count_if(NO_EMPLOYEES>0)::text f, null g, null h
from m where idle group by 2,3,4
union all
select 'ctrl', CURRENT_CONTROLLER_NAME, CURRENT_CONTROLLER_ID, count_if(idle and yrs>=3)::text, count_if(idle)::text,
  count_if(CURRENT_MINE_STATUS='Active')::text, count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed'))::text,
  listagg(distinct STATE, ','), round(max(iff(idle, yrs, null)),1)::text
from m where COAL_METAL_IND='C' group by 2,3
qualify row_number() over (order by count_if(idle and yrs>=3) desc) <= 15
union all
select 'state', STATE, COAL_METAL_IND, count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed'))::text,
  count_if(idle)::text, count_if(idle and yrs>=3)::text, count_if(CURRENT_MINE_STATUS='Active')::text,
  round(100*count_if(idle and yrs>=3)/nullif(count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed')),0),1)::text, null
from m where COAL_METAL_IND='C' group by 2,3 having count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed')) >= 20;

-- [q07] statement 7
-- MSHA join: accidents and citations dated 30+ days AFTER a mine's current idle/abandoned status took effect
with m as (select MINE_ID, CURRENT_MINE_STATUS st, CURRENT_STATUS_DT sdt, CURRENT_MINE_NAME nm, CURRENT_CONTROLLER_NAME ctrl, STATE, COAL_METAL_IND cm
           from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES
           where CURRENT_MINE_STATUS in ('Abandoned','Abandoned and Sealed','Temporarily Idled','NonProducing') and CURRENT_STATUS_DT >= '2000-01-01'),
a as (select a.MINE_ID, count(*) n, count_if(a.IS_FATALITY) fat, sum(a.DAYS_LOST) dl, max(a.ACCIDENT_DATE) last_dt,
        count_if(a.ACCIDENT_DATE > dateadd(year,1,m.sdt)) n_1yr
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS a join m on a.MINE_ID=m.MINE_ID and a.ACCIDENT_DATE > dateadd(day,30,m.sdt) group by 1),
v as (select v.MINE_ID, count(*) n, count_if(v.IS_SIGNIFICANT_AND_SUBSTANTIAL) ss, max(v.VIOLATION_OCCUR_DATE) last_dt,
        count_if(v.VIOLATION_OCCUR_DATE > dateadd(year,1,m.sdt)) n_1yr
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v join m on v.MINE_ID=m.MINE_ID and v.VIOLATION_OCCUR_DATE > dateadd(day,30,m.sdt) group by 1),
j as (select m.*, a.n acc, a.fat, a.dl, a.last_dt acc_last, a.n_1yr acc_1yr, v.n viol, v.ss, v.last_dt viol_last, v.n_1yr viol_1yr
      from m left join a using (MINE_ID) left join v using (MINE_ID))
select 'status' k, st a, count(*)::text b, count_if(acc>0)::text c, sum(acc)::text d, sum(fat)::text e, sum(dl)::text f,
  count_if(viol>0)::text g, sum(viol)::text h, count_if(acc_1yr>0)::text i, count_if(viol_1yr>0)::text l, null o
from j group by 2
union all
select 'range', 'acc/viol dates', (select min(ACCIDENT_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS),
  (select max(ACCIDENT_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS),
  (select min(VIOLATION_OCCUR_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS),
  (select max(VIOLATION_OCCUR_DATE)::text from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS), null,null,null,null,null,null
union all
(select 'mine', MINE_ID||' '||nm, st||' '||sdt::text, ctrl, STATE||' '||cm, acc::text, fat::text, dl::text, acc_1yr::text, acc_last::text, viol::text, viol_last::text
 from j where acc_1yr>0 order by acc_1yr desc, acc desc limit 25);

-- [q08] statement 8
-- BIA x MSHA: parse the Esri rings one by one into polygons, check area against GIS_ACRES, then count mines whose point falls inside (odd ring count = inside)
with r as (select g.LAR_ID, g.LAR_NAME, g.GIS_ACRES, f.index ring_i,
             try_to_geography('{"type":"Polygon","coordinates":[' || to_json(f.value) || ']}') geo
           from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO g,
                lateral flatten(input => parse_json(g.GEOMETRY_JSON):rings) f),
rb as (select *, st_xmin(geo) x0, st_xmax(geo) x1, st_ymin(geo) y0, st_ymax(geo) y1 from r where geo is not null),
chk as (select LAR_ID, any_value(LAR_NAME) nm, any_value(GIS_ACRES) gis, count(*) rings, round(max(st_area(geo))/4046.86) biggest_ring_acres from rb group by 1),
mn as (select MINE_ID, CURRENT_MINE_NAME, CURRENT_MINE_STATUS, PRIMARY_SIC, COAL_METAL_IND, STATE, CURRENT_OPERATOR_NAME, NO_EMPLOYEES, LATITUDE, LONGITUDE,
         st_makepoint(LONGITUDE, LATITUDE) pt
       from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES where LATITUDE is not null and LATITUDE <> 0 and LONGITUDE is not null and LONGITUDE <> 0),
hits as (select mn.MINE_ID, rb.LAR_ID from mn join rb on mn.LONGITUDE between rb.x0 and rb.x1 and mn.LATITUDE between rb.y0 and rb.y1 and st_contains(rb.geo, mn.pt)
         group by 1,2 having mod(count(*),2)=1),
h as (select mn.*, hits.LAR_ID, chk.nm lar from hits join mn using (MINE_ID) join chk using (LAR_ID))
select 'parse' k, (select count(*) from r)::text a, (select count(*) from rb)::text b, (select count(distinct LAR_ID) from rb)::text c,
  (select round(sum(gis)) from chk)::text d, (select round(sum(biggest_ring_acres)) from chk)::text e, null f, null g, null i
union all
(select 'areachk', nm, round(gis)::text, biggest_ring_acres::text, rings::text, null, null, null, null from chk order by gis desc limit 5)
union all
select 'status', CURRENT_MINE_STATUS, count(*)::text, count(distinct LAR_ID)::text, count_if(PRIMARY_SIC ilike '%uranium%')::text, sum(NO_EMPLOYEES)::text, count_if(COAL_METAL_IND='C')::text, null, null
from h group by 2
union all
(select 'lar', lar, count(*)::text, count_if(CURRENT_MINE_STATUS='Active')::text, count_if(PRIMARY_SIC ilike '%uranium%')::text, sum(NO_EMPLOYEES)::text,
  listagg(distinct iff(CURRENT_MINE_STATUS='Active', CURRENT_OPERATOR_NAME, null), '; ') within group (order by iff(CURRENT_MINE_STATUS='Active', CURRENT_OPERATOR_NAME, null)), null, null
 from h group by lar order by count(*) desc limit 12)
union all
(select 'active', MINE_ID||' '||CURRENT_MINE_NAME, lar, CURRENT_OPERATOR_NAME, PRIMARY_SIC, NO_EMPLOYEES::text, STATE, null, null
 from h where CURRENT_MINE_STATUS='Active' order by NO_EMPLOYEES desc nulls last limit 15);
-- q08 RESULT: ERROR 100205 GeoJSON::Point: Invalid Lng/Lat pair '-180.999,90.9997' (a junk MSHA mine coordinate). Counted against the budget. Rerun below as q08b.

-- [q08b] statement 9
-- (rerun of q08 with junk mine coordinates filtered: MSHA holds points like 90.9997,-180.999) BIA x MSHA: parse the Esri rings one by one into polygons, check area against GIS_ACRES, then count mines whose point falls inside (odd ring count = inside)
with r as (select g.LAR_ID, g.LAR_NAME, g.GIS_ACRES, f.index ring_i,
             try_to_geography('{"type":"Polygon","coordinates":[' || to_json(f.value) || ']}') geo
           from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO g,
                lateral flatten(input => parse_json(g.GEOMETRY_JSON):rings) f),
rb as (select *, st_xmin(geo) x0, st_xmax(geo) x1, st_ymin(geo) y0, st_ymax(geo) y1 from r where geo is not null),
chk as (select LAR_ID, any_value(LAR_NAME) nm, any_value(GIS_ACRES) gis, count(*) rings, round(max(st_area(geo))/4046.86) biggest_ring_acres from rb group by 1),
mn as (select MINE_ID, CURRENT_MINE_NAME, CURRENT_MINE_STATUS, PRIMARY_SIC, COAL_METAL_IND, STATE, CURRENT_OPERATOR_NAME, NO_EMPLOYEES, LATITUDE, LONGITUDE,
         st_makepoint(LONGITUDE, LATITUDE) pt
       from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES where LATITUDE between 17 and 72 and LONGITUDE between -180 and -60), bad as (select count_if(LATITUDE > 72 or LATITUDE < 17 or LONGITUDE < -180 or LONGITUDE > -60) nbad from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES where LATITUDE <> 0),
hits as (select mn.MINE_ID, rb.LAR_ID from mn join rb on mn.LONGITUDE between rb.x0 and rb.x1 and mn.LATITUDE between rb.y0 and rb.y1 and st_contains(rb.geo, mn.pt)
         group by 1,2 having mod(count(*),2)=1),
h as (select mn.*, hits.LAR_ID, chk.nm lar from hits join mn using (MINE_ID) join chk using (LAR_ID))
select 'parse' k, (select count(*) from r)::text a, (select count(*) from rb)::text b, (select count(distinct LAR_ID) from rb)::text c,
  (select round(sum(gis)) from chk)::text d, (select round(sum(biggest_ring_acres)) from chk)::text e, (select nbad from bad)::text f, null g, null i
union all
(select 'areachk', nm, round(gis)::text, biggest_ring_acres::text, rings::text, null, null, null, null from chk order by gis desc limit 5)
union all
select 'status', CURRENT_MINE_STATUS, count(*)::text, count(distinct LAR_ID)::text, count_if(PRIMARY_SIC ilike '%uranium%')::text, sum(NO_EMPLOYEES)::text, count_if(COAL_METAL_IND='C')::text, null, null
from h group by 2
union all
(select 'lar', lar, count(*)::text, count_if(CURRENT_MINE_STATUS='Active')::text, count_if(PRIMARY_SIC ilike '%uranium%')::text, sum(NO_EMPLOYEES)::text,
  listagg(distinct iff(CURRENT_MINE_STATUS='Active', CURRENT_OPERATOR_NAME, null), '; ') within group (order by iff(CURRENT_MINE_STATUS='Active', CURRENT_OPERATOR_NAME, null)), null, null
 from h group by lar order by count(*) desc limit 12)
union all
(select 'active', MINE_ID||' '||CURRENT_MINE_NAME, lar, CURRENT_OPERATOR_NAME, PRIMARY_SIC, NO_EMPLOYEES::text, STATE, null, null
 from h where CURRENT_MINE_STATUS='Active' order by NO_EMPLOYEES desc nulls last limit 15);

-- [q09] statement 10
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
from m order by via, pings desc limit 150;

-- [q10] statement 11
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
(select 'multiname', MMSI, nn::text, n::text, vname, vname2, nimo::text, tc, vt::text from s order by nn desc limit 12);

-- [q11] statement 12
-- AIS identity check: one MMSI reported in two places 0.5+ degrees apart (~55 km) inside the same minute = two radios sharing one ID
with p as (select MMSI, date_trunc('minute', BASE_DATETIME) mi, max(LATITUDE)-min(LATITUDE) dlat, max(LONGITUDE)-min(LONGITUDE) dlon,
             max(VESSEL_NAME) vname, min(VESSEL_NAME) vname2
           from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS group by 1,2 having count(*) > 1),
q as (select MMSI, count(*) multi_minutes, count_if(dlat >= 0.5 or dlon >= 0.5) split_minutes, max(vname) vname, min(vname2) vname2, max(greatest(dlat,dlon)) maxd
      from p group by 1)
select 'sum' k, count(*)::text a, count_if(split_minutes>0)::text b, count_if(split_minutes>=60)::text c, sum(split_minutes)::text d, null e, null f, null g
from q
union all
(select 'mmsi', MMSI, split_minutes::text, multi_minutes::text, vname, vname2, round(maxd,1)::text, left(MMSI,3) from q where split_minutes > 0 order by split_minutes desc limit 25);

-- [q12] statement 13
-- Debt cliff source check: which World Bank IDS series carry 2026-2032 projections, Gabon values to match the mart, and denominators; plus rows where total <> principal + interest
select 'series' k, SERIES_CODE a, left(SERIES_NAME,90) b, count(*)::text c, count_if(try_to_double(C_2030) is not null)::text d,
  count_if(try_to_double(C_2024) is not null)::text e, count_if(try_to_double(C_2025) is not null)::text f,
  max(iff(COUNTRY_CODE='GAB', C_2031, null)) g, max(iff(COUNTRY_CODE='GAB', C_2024, null)) h
from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS
group by 2,3
having count_if(try_to_double(C_2030) is not null) > 0
   or SERIES_CODE in ('BX.GSR.TOTL.CD','NY.GNP.MKTP.CD','DT.TDS.DECT.EX.ZS','DT.TDS.DECT.GN.ZS','DT.TDS.DLXF.CD','DT.TDS.DECT.CD','DT.AMT.DLXF.CD','DT.INT.DLXF.CD')
union all
(select 'diff', COUNTRY_CODE||' '||DATA_YEAR, round(TOTAL_DEBT_SERVICE_USD/1e9,3)::text, round(PRINCIPAL_REPAYMENT_USD/1e9,3)::text, round(INTEREST_PAYMENT_USD/1e9,3)::text,
   round((TOTAL_DEBT_SERVICE_USD-PRINCIPAL_REPAYMENT_USD-INTEREST_PAYMENT_USD)/1e9,3)::text,
   round((TOTAL_DEBT_SERVICE_USD-PRINCIPAL_REPAYMENT_USD-INTEREST_PAYMENT_USD)/nullif(TOTAL_DEBT_SERVICE_USD,0),3)::text, IS_AGGREGATE::text, null
 from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF
 where COUNTRY_CODE in ('GAB','CHN','THA','IDN','MNE') and DATA_YEAR in (2026, 2030, 2031));

-- [q13] statement 14
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
 from j where hit order by fs);

-- [q14] statement 15
-- Debt cliff with denominators: projected peak (2026-32) vs the same country actual 2019-24 debt service and vs latest exports and GNI, from World Bank IDS
with h as (select COUNTRY_NAME, max(COUNTRY_CODE) ids_code,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2019), null)) t19, max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2020), null)) t20,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2021), null)) t21, max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2022), null)) t22,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2023), null)) t23, max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2024), null)) t24,
    max(iff(SERIES_CODE='DT.TDS.DECT.CD', try_to_double(C_2026), null)) p26,
    max(iff(SERIES_CODE='BX.GSR.TOTL.CD', coalesce(try_to_double(C_2024), try_to_double(C_2023)), null)) ex,
    max(iff(SERIES_CODE='NY.GNP.MKTP.CD', coalesce(try_to_double(C_2024), try_to_double(C_2023)), null)) gni
  from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS group by 1),
m as (select COUNTRY_CODE, COUNTRY_NAME, max(IS_AGGREGATE) agg, max(TOTAL_DEBT_SERVICE_USD) peak, max_by(DATA_YEAR, TOTAL_DEBT_SERVICE_USD) peak_yr,
    max(iff(DATA_YEAR=2026, TOTAL_DEBT_SERVICE_USD, null)) d26, max(iff(DATA_YEAR=2027, TOTAL_DEBT_SERVICE_USD, null)) d27,
    listagg(iff(IS_REPAYMENT_CLIFF, DATA_YEAR::text, null), ',') cliff_yrs
  from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF group by 1,2)
select m.COUNTRY_CODE, m.COUNTRY_NAME, h.ids_code, m.agg, m.cliff_yrs, m.peak_yr, round(m.peak/1e9,2) peak_bn, round(m.d26/1e9,2) d26_bn, round(h.p26/1e9,2) ids26_bn,
  round(greatest(coalesce(t19,0),coalesce(t20,0),coalesce(t21,0),coalesce(t22,0),coalesce(t23,0),coalesce(t24,0))/1e9,2) hist_max_bn,
  round(h.t24/1e9,2) t24_bn, round(h.ex/1e9,1) ex_bn, round(h.gni/1e9,1) gni_bn,
  round(100*m.peak/nullif(h.ex,0),1) peak_pct_ex, round(100*m.d26/nullif(h.ex,0),1) d26_pct_ex, round(100*m.peak/nullif(h.gni,0),1) peak_pct_gni,
  round(m.peak/nullif(greatest(coalesce(t19,0),coalesce(t20,0),coalesce(t21,0),coalesce(t22,0),coalesce(t23,0),coalesce(t24,0)),0),2) peak_vs_histmax
from m left join h using (COUNTRY_NAME)
order by m.agg, peak_pct_ex desc nulls last;

-- [q15] statement 16
-- Federal Register midnight rules: final rules in the Nov 8 - Jan 19 window of every year, vs the same year Feb-Oct daily pace
with d as (select PUBLICATION_DATE dt, TYPE, IS_SIGNIFICANT sig, PAGE_LENGTH pg
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS where TYPE in ('Rule','Proposed Rule')),
w as (select *, case when dt >= date_from_parts(year(dt),11,8) then year(dt) when dt <= date_from_parts(year(dt),1,19) then year(dt)-1 end wy from d),
win as (select wy, count_if(TYPE='Rule') rules, count_if(TYPE='Rule' and sig) sig_rules, count_if(TYPE='Rule' and sig is not null) sig_filled,
          sum(iff(TYPE='Rule', pg, 0)) rule_pages, count_if(TYPE='Proposed Rule') props, count(distinct dt) pubdays
        from w where wy between 2009 and 2025 group by 1),
base as (select year(dt) y, count_if(TYPE='Rule') rules, count_if(TYPE='Rule' and sig) sig_rules, sum(iff(TYPE='Rule', pg, 0)) rule_pages, count(distinct dt) pubdays
         from d where month(dt) between 2 and 10 group by 1)
select win.wy, win.rules, win.sig_rules, win.sig_filled, win.rule_pages, win.props, win.pubdays,
  base.rules base_rules, base.sig_rules base_sig, base.pubdays base_days,
  round((win.rules/win.pubdays)/(base.rules/base.pubdays),2) rule_pace_ratio,
  round((win.sig_rules/win.pubdays)/nullif(base.sig_rules/base.pubdays,0),2) sig_pace_ratio,
  round((win.rule_pages/win.pubdays)/nullif(base.rule_pages/base.pubdays,0),2) page_pace_ratio
from win left join base on base.y = win.wy order by 1;

-- [q16] statement 17
-- Federal Register: which issuing offices went quiet. Documents Feb-Aug by year 2021-2026, most specific agency (last name in the list)
with d as (select PUBLICATION_DATE dt, TYPE,
             coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
           where month(PUBLICATION_DATE) between 2 and 8 and year(PUBLICATION_DATE) >= 2021),
g as (select ag, count_if(year(dt)=2021) y21, count_if(year(dt)=2022) y22, count_if(year(dt)=2023) y23, count_if(year(dt)=2024) y24,
        count_if(year(dt)=2025) y25, count_if(year(dt)=2026) y26, count_if(year(dt)=2024 and TYPE='Rule') r24, count_if(year(dt)=2025 and TYPE='Rule') r25,
        count_if(year(dt)=2026 and TYPE='Rule') r26
      from d group by 1)
select 'total' k, null ag, sum(y21) y21, sum(y22) y22, sum(y23) y23, sum(y24) y24, sum(y25) y25, sum(y26) y26, sum(r24) r24, sum(r25) r25, sum(r26) r26, null pct from g
union all
(select 'drop', ag, y21, y22, y23, y24, y25, y26, r24, r25, r26, round(100*(y25+y26)/(2.0*((y21+y22+y23+y24)/4.0))) from g
 where (y21+y22+y23+y24)/4.0 >= 100 order by (y25+y26)/((y21+y22+y23+y24)/4.0) asc limit 30)
union all
(select 'rise', ag, y21, y22, y23, y24, y25, y26, r24, r25, r26, round(100*(y25+y26)/(2.0*((y21+y22+y23+y24)/4.0))) from g
 where (y21+y22+y23+y24)/4.0 >= 100 order by (y25+y26)/((y21+y22+y23+y24)/4.0) desc limit 10);

-- [q17] statement 18
-- Federal Register procedure by year, Feb-Aug only: interim/direct final rules, delays, repeal titles, comment windows, days until effective
select PUBLICATION_YEAR yr, count_if(TYPE='Rule') rules,
  count_if(TYPE='Rule' and ACTION ilike '%interim final%') ifr,
  count_if(TYPE='Rule' and ACTION ilike '%direct final%') dfr,
  count_if(TYPE='Rule' and (ACTION ilike '%delay%' or ACTION ilike '%postpone%')) delay_rules,
  count_if(TYPE='Rule' and (TITLE ilike '%rescission%' or TITLE ilike '%rescind%' or TITLE ilike '%repeal%' or TITLE ilike '%removal of%' or TITLE ilike '%removing%')) repeal_title,
  count_if(TYPE='Rule' and DAYS_UNTIL_EFFECTIVE is not null) eff_filled,
  count_if(TYPE='Rule' and DAYS_UNTIL_EFFECTIVE <= 0) eff_now,
  count_if(TYPE='Rule' and DAYS_UNTIL_EFFECTIVE between 1 and 29) eff_lt30,
  count_if(TYPE='Proposed Rule') props,
  count_if(TYPE='Proposed Rule' and COMMENT_WINDOW_DAYS is not null) prop_cw,
  median(iff(TYPE='Proposed Rule', COMMENT_WINDOW_DAYS, null)) prop_cw_med,
  count_if(TYPE='Proposed Rule' and COMMENT_WINDOW_DAYS < 30) prop_lt30,
  count_if(TYPE='Proposed Rule' and COMMENT_WINDOW_DAYS >= 60) prop_ge60,
  count_if(TYPE='Rule' and IS_SIGNIFICANT) sig_rules, count_if(TYPE='Rule' and IS_SIGNIFICANT is not null) sig_filled
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where PUBLICATION_MONTH between 2 and 8
group by 1 order by 1;

-- [q18] statement 19
-- Debt cliff dull-explanation test: split projected debt service into public (PPG), private non-guaranteed (PNG), IMF, bonds, multilateral, bilateral; 2024 actual vs 2026-2030 projection
select trim(COUNTRY_CODE) cc, SERIES_CODE sc,
  round(try_to_double(C_2023)/1e9,3) y23, round(try_to_double(C_2024)/1e9,3) y24, round(try_to_double(C_2025)/1e9,3) y25,
  round(try_to_double(C_2026)/1e9,3) y26, round(try_to_double(C_2027)/1e9,3) y27, round(try_to_double(C_2028)/1e9,3) y28,
  round(try_to_double(C_2029)/1e9,3) y29, round(try_to_double(C_2030)/1e9,3) y30
from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS
where trim(COUNTRY_CODE) in ('MOZ','SEN','BTN','PAK','GMB','MNE','BEN','TGO','GNB','MDG','PRY','LAO','MNG')
  and SERIES_CODE in ('DT.TDS.DECT.CD','DT.TDS.DPPG.CD','DT.TDS.DPNG.CD','DT.TDS.DIMF.CD','DT.TDS.PBND.CD','DT.TDS.MLAT.CD','DT.TDS.BLAT.CD')
order by 1, 2;

-- [q19] statement 20
-- Federal Register mechanism check: for the offices that went quiet, what kind of notice disappeared. Feb-Aug, 2021-2026, by title pattern
with d as (select PUBLICATION_YEAR y, TITLE,
             coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
           where PUBLICATION_MONTH between 2 and 8 and PUBLICATION_YEAR >= 2021)
select ag,
  case when ag = 'Federal Emergency Management Agency' and TITLE ilike '%Amendment No%' then 'fema amendment'
       when ag = 'Federal Emergency Management Agency' and TITLE ilike '%Major Disaster and Related Determinations%' then 'fema NEW major disaster'
       when ag = 'Federal Emergency Management Agency' and TITLE ilike '%Emergency and Related Determinations%' then 'fema NEW emergency'
       when ag = 'Federal Emergency Management Agency' and TITLE ilike '%flood%' then 'fema flood map'
       when TITLE ilike '%meeting%' then 'meeting'
       when TITLE ilike '%information collection%' or TITLE ilike '%data collection%' or TITLE ilike '%paperwork%' or TITLE ilike '%submission for OMB%' then 'info collection'
       else 'other' end cat,
  count_if(y=2021) y21, count_if(y=2022) y22, count_if(y=2023) y23, count_if(y=2024) y24, count_if(y=2025) y25, count_if(y=2026) y26
from d
where ag in ('Federal Emergency Management Agency','National Institutes of Health','Centers for Disease Control and Prevention','Environmental Protection Agency',
             'Education Department','Fish and Wildlife Service','Veterans Affairs Department','National Science Foundation')
group by 1, 2 order by 1, 2;

-- [q20] statement 21
-- FEMA independent source: distinct disaster numbers by declaration year in the FEMA Individual Assistance registrations table (Feb-Aug and full year), to test whether fewer disasters were declared
select year(DECLARATION_DATE) y, count(distinct DISASTER_NUMBER) disasters_all,
  count(distinct iff(month(DECLARATION_DATE) between 2 and 8, DISASTER_NUMBER, null)) disasters_feb_aug,
  count(*) registrations, min(DECLARATION_DATE) first_decl, max(DECLARATION_DATE) last_decl, max(APPLIED_DATE) last_applied
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where DECLARATION_DATE >= '2019-01-01'
group by 1 order by 1;

-- [q21] statement 22
-- MSHA join: operator churn. Violations since 2010 by violator (operator-format IDs only), per mine; how many operators each working mine has cycled through, and what earlier operators left unpaid
with mines as (select MINE_ID, CURRENT_OPERATOR_ID cop, CURRENT_CONTROLLER_ID cid, CURRENT_CONTROLLER_NAME cname, CURRENT_MINE_NAME mname,
                 CURRENT_MINE_STATUS st, COAL_METAL_IND cm, STATE, NO_EMPLOYEES emp
               from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES),
v as (select v.MINE_ID, v.VIOLATOR_ID, max(v.VIOLATOR_NAME) vname, min(v.VIOLATION_OCCUR_DATE) d0, max(v.VIOLATION_OCCUR_DATE) d1, count(*) n,
        sum(iff(v.VIOLATION_OCCUR_DATE < '2024-01-01', coalesce(v.AMOUNT_DUE,0) - coalesce(v.AMOUNT_PAID,0), 0)) unpaid_old
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v join mines m on v.MINE_ID = m.MINE_ID
      where v.VIOLATION_OCCUR_DATE >= '2010-01-01' and length(v.VIOLATOR_ID) = length(m.cop) and left(v.VIOLATOR_ID,1) = left(m.cop,1)
      group by 1, 2),
pm as (select m.MINE_ID, any_value(m.cop) cop, any_value(m.cid) cid, any_value(m.cname) cname, any_value(m.mname) mname, any_value(m.st) st, any_value(m.cm) cm,
         any_value(m.STATE) state, any_value(m.emp) emp, count(*) nops, count_if(v.VIOLATOR_ID <> m.cop) n_prior,
         sum(iff(v.VIOLATOR_ID <> m.cop, v.unpaid_old, 0)) unpaid_prior, sum(v.unpaid_old) unpaid_all, sum(v.n) nviol,
         listagg(v.vname || ' ' || year(v.d0) || '-' || year(v.d1), ' > ') within group (order by v.d0) chain
       from mines m join v on v.MINE_ID = m.MINE_ID group by m.MINE_ID),
w as (select * from pm where st in ('Active','Intermittent','Temporarily Idled','NonProducing'))
select 'peer' k, cm a, count(*)::text b, median(nops)::text c, count_if(nops >= 3)::text d, count_if(nops >= 4)::text e,
  round(sum(unpaid_prior)/1e6,2)::text f, round(sum(unpaid_all)/1e6,2)::text g, null h, null i
from w group by cm
union all
(select 'ctrl', cname, cid, count(*)::text, count_if(nops >= 3)::text, round(avg(nops),2)::text, round(sum(unpaid_prior)/1e6,2)::text,
   round(sum(unpaid_all)/1e6,2)::text, listagg(distinct state, ','), sum(emp)::text
 from w group by cname, cid order by count_if(nops >= 3) desc, sum(unpaid_prior) desc limit 15)
union all
(select 'ctrl_unpaid', cname, cid, count(*)::text, count_if(nops >= 3)::text, round(avg(nops),2)::text, round(sum(unpaid_prior)/1e6,2)::text,
   round(sum(unpaid_all)/1e6,2)::text, listagg(distinct state, ','), sum(emp)::text
 from w group by cname, cid order by sum(unpaid_prior) desc limit 12)
union all
(select 'mine', MINE_ID || ' ' || mname, st || ' ' || cm || ' ' || state, cname, nops::text, round(unpaid_prior/1e3,1)::text, nviol::text, emp::text, left(chain, 300), null
 from w order by nops desc, unpaid_prior desc limit 15);

-- [q22] statement 23
-- FEMA gap verification: join FEMA disaster numbers (IA registrations table) to Federal Register notices by the FEMA-####-DR docket tag; land rate and publication lag by half-year; plus title search across all agencies
with ia as (select regexp_substr(DISASTER_NUMBER::text, '[0-9]+') dn, min(DECLARATION_DATE) dd, max(DAMAGED_STATE_ABBREVIATION) st, max(INCIDENT_TYPE_CODE) typ
            from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS where DECLARATION_DATE >= '2023-01-01' group by 1),
fr as (select d.PUBLICATION_DATE pd, d.TITLE, f.value::string tag
       from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS d,
            lateral flatten(input => regexp_substr_all(d.DOCKET_IDS, 'FEMA-[0-9]{4}-(DR|EM)')) f
       where d.DOCKET_IDS ilike '%FEMA-%' and d.PUBLICATION_DATE >= '2023-01-01'),
frd as (select regexp_substr(tag, '[0-9]{4}') dn, min(pd) first_pub, count(*) notices from fr where tag like '%-DR' group by 1),
j as (select ia.*, frd.first_pub, frd.notices, datediff(day, ia.dd, frd.first_pub) lag from ia left join frd using (dn))
select 'byhalf' k, year(dd) || '-H' || iff(month(dd) <= 6, 1, 2) a, count(*)::text b, count(first_pub)::text c, median(lag)::text d, max(lag)::text e, sum(notices)::text f, null g
from j group by 2
union all
select 'frmonth', to_char(date_trunc(month, pd), 'YYYY-MM'), count(distinct tag)::text, count(*)::text, count_if(TITLE ilike '%Major Disaster%')::text, null, null, null
from fr group by 2
union all
select 'title', year(PUBLICATION_DATE)::text, count(*)::text, count_if(DOCKET_IDS ilike '%FEMA-%')::text, count_if(month(PUBLICATION_DATE) between 2 and 8)::text,
  max(PUBLICATION_DATE)::text, count(distinct AGENCY_NAMES)::text, null
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where (TITLE ilike '%major disaster%' or TITLE ilike '%Emergency and Related Determinations%') and PUBLICATION_DATE >= '2021-01-01'
group by 2
union all
(select 'decl2025', dn, dd::text, st, typ, first_pub::text, lag::text, notices::text from j where dd >= '2025-01-01' order by dd);

-- [q23] statement 24
-- FEMA gap, peer check: every disaster-declaration notice by month and issuing agency list, Jul 2024 - Sep 2026. Does SBA keep publishing while FEMA stops?
select to_char(date_trunc(month, PUBLICATION_DATE), 'YYYY-MM') m, AGENCY_NAMES ag, count(*) n, count_if(DOCKET_IDS ilike '%FEMA-%') fema_docket,
  count(distinct PUBLICATION_DATE) pub_days, min(TITLE) sample_title
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where (TITLE ilike '%major disaster%' or TITLE ilike '%Emergency and Related Determinations%' or TITLE ilike '%emergency declaration%'
       or TITLE ilike '%Declaration of a Disaster%' or TITLE ilike '%Declaration of an Economic Injury Disaster%')
  and PUBLICATION_DATE >= '2024-07-01'
group by 1, 2 order by 1, 2;

-- [q24] statement 25
-- MSHA churn, tested inside the group: do mines that cycle operators leave more assessed penalties unpaid? Plus the operator-by-operator chain at the top three mines
with mines as (select MINE_ID, CURRENT_OPERATOR_ID cop, CURRENT_MINE_STATUS st, COAL_METAL_IND cm from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES),
v as (select v.MINE_ID, v.VIOLATOR_ID, max(v.VIOLATOR_NAME) vname, min(v.VIOLATION_OCCUR_DATE) d0, max(v.VIOLATION_OCCUR_DATE) d1, count(*) n,
        count_if(v.IS_SIGNIFICANT_AND_SUBSTANTIAL) ss, sum(iff(v.VIOLATION_OCCUR_DATE < '2024-01-01', v.AMOUNT_DUE, 0)) due_old,
        sum(iff(v.VIOLATION_OCCUR_DATE < '2024-01-01', v.AMOUNT_PAID, 0)) paid_old, sum(v.PROPOSED_PENALTY) prop
      from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v join mines m on v.MINE_ID = m.MINE_ID
      where v.VIOLATION_OCCUR_DATE >= '2010-01-01' and length(v.VIOLATOR_ID) = length(m.cop) and left(v.VIOLATOR_ID,1) = left(m.cop,1)
      group by 1, 2),
pm as (select m.MINE_ID, any_value(m.cm) cm, any_value(m.st) st, count(*) nops, sum(v.due_old) due_old, sum(v.paid_old) paid_old, sum(v.n) nviol, sum(v.ss) ss
       from mines m join v on v.MINE_ID = m.MINE_ID group by 1)
select 'bucket' k, cm a, iff(nops >= 3, '3+', nops::text) b, count(*)::text c, round(sum(due_old)/1e6,2)::text d, round(sum(paid_old)/1e6,2)::text e,
  round(100*(1 - sum(paid_old)/nullif(sum(due_old),0)),1)::text f,
  round(100*median(iff(due_old > 0, 1 - paid_old/due_old, null)),1)::text g,
  count_if(due_old > 0 and paid_old/due_old < 0.5)::text h, round(100.0*sum(ss)/nullif(sum(nviol),0),1)::text i
from pm where st in ('Active','Intermittent','Temporarily Idled','NonProducing') group by 2, 3
union all
(select 'chain', MINE_ID, vname, year(d0) || '-' || year(d1), n::text, ss::text, round(prop)::text, round(due_old)::text, round(paid_old)::text, VIOLATOR_ID
 from v where MINE_ID in ('1518001','4407150','1518973') order by MINE_ID, d0);

-- [q25] statement 26
-- Debt cliff, public debt only (PPG, strips out private project finance): 2026-28 peak vs 2024 exports and vs the same country 2019-24 max; all countries so the median peer is visible
with ids as (select trim(COUNTRY_CODE) cc, max(COUNTRY_NAME) nm,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', greatest(coalesce(try_to_double(C_2026),0), coalesce(try_to_double(C_2027),0), coalesce(try_to_double(C_2028),0)), null)) ppg_peak,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', try_to_double(C_2026), null)) ppg26,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', try_to_double(C_2024), null)) ppg24,
    max(iff(SERIES_CODE='DT.TDS.DPPG.CD', greatest(coalesce(try_to_double(C_2019),0), coalesce(try_to_double(C_2020),0), coalesce(try_to_double(C_2021),0),
        coalesce(try_to_double(C_2022),0), coalesce(try_to_double(C_2023),0), coalesce(try_to_double(C_2024),0)), null)) ppg_hist,
    max(iff(SERIES_CODE='DT.TDS.PBND.CD', greatest(coalesce(try_to_double(C_2026),0), coalesce(try_to_double(C_2027),0), coalesce(try_to_double(C_2028),0)), null)) bond_peak,
    max(iff(SERIES_CODE='BX.GSR.TOTL.CD', coalesce(try_to_double(C_2024), try_to_double(C_2023)), null)) ex
  from LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS group by 1),
m as (select COUNTRY_CODE cc, max(IS_AGGREGATE) agg from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF group by 1),
j as (select ids.*, 100*ppg_peak/nullif(ex,0) peak_pct_ex, 100*ppg24/nullif(ex,0) y24_pct_ex, ppg_peak/nullif(ppg_hist,0) vs_hist
      from ids join m using (cc) where not m.agg and cc <> 'LDC' and ex > 0)
select 'median' k, null cc, null nm, count(*)::text a, round(median(peak_pct_ex),1)::text b, round(median(y24_pct_ex),1)::text c, round(median(vs_hist),2)::text d,
  count_if(peak_pct_ex >= 30)::text e, count_if(vs_hist >= 1.5)::text f, count_if(peak_pct_ex >= 30 and vs_hist >= 1.5)::text g
from j
union all
(select 'top', cc, nm, round(ppg_peak/1e9,2)::text, round(peak_pct_ex,1)::text, round(y24_pct_ex,1)::text, round(vs_hist,2)::text,
   round(ppg24/1e9,2)::text, round(ex/1e9,1)::text, round(bond_peak/1e9,2)::text
 from j order by peak_pct_ex desc limit 15)
union all
(select 'jump', cc, nm, round(ppg_peak/1e9,2)::text, round(peak_pct_ex,1)::text, round(y24_pct_ex,1)::text, round(vs_hist,2)::text,
   round(ppg24/1e9,2)::text, round(ex/1e9,1)::text, round(bond_peak/1e9,2)::text
 from j where peak_pct_ex >= 15 order by vs_hist desc limit 10);

-- [q26] statement 27
-- Federal Register: meeting notices government-wide, Feb-Aug by year 2017-2026, and the offices with the biggest drop (advisory committees, study sections)
with d as (select PUBLICATION_YEAR y, coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
           where TYPE = 'Notice' and TITLE ilike '%meeting%' and PUBLICATION_MONTH between 2 and 8 and PUBLICATION_YEAR >= 2017)
select 'all' k, null ag, count_if(y=2017) y17, count_if(y=2018) y18, count_if(y=2019) y19, count_if(y=2020) y20, count_if(y=2021) y21, count_if(y=2022) y22,
  count_if(y=2023) y23, count_if(y=2024) y24, count_if(y=2025) y25, count_if(y=2026) y26 from d
union all
(select 'ag', ag, count_if(y=2017), count_if(y=2018), count_if(y=2019), count_if(y=2020), count_if(y=2021), count_if(y=2022),
   count_if(y=2023), count_if(y=2024), count_if(y=2025), count_if(y=2026)
 from d group by ag having count_if(y between 2021 and 2024) >= 80
 order by (count_if(y=2025) + count_if(y=2026)) / (count_if(y between 2021 and 2024)/2.0) asc limit 25);

-- [q27] statement 28
-- FEMA gap, the dull explanation: did FEMA announce a new way of publishing declarations? Every FEMA disaster-type notice since Jan 2025 that is not a single-state declaration or amendment, with its abstract
select PUBLICATION_DATE, DOCUMENT_NUMBER, TITLE, left(ABSTRACT, 700) abstract, left(DOCKET_IDS, 200) dockets, left(EXCERPTS, 300) excerpts
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where AGENCY_NAMES ilike '%Federal Emergency Management Agency%' and PUBLICATION_DATE >= '2025-01-01'
  and (TITLE ilike '%declaration%' or TITLE ilike '%disaster%' or ABSTRACT ilike '%declaration%')
  and TITLE not ilike '%Amendment No%' and TITLE not ilike '%; Major Disaster and Related Determinations%' and TITLE not ilike '%; Emergency and Related Determinations%'
order by PUBLICATION_DATE;

-- [q28] statement 29
-- Federal Register trap check: the comment-window median is exactly 45 every year. Is COMMENT_WINDOW_DAYS real? Top values, and a recompute from the two date columns
select 'top' k, COMMENT_WINDOW_DAYS::text v, count(*) n,
  count_if(datediff(day, PUBLICATION_DATE, COMMENTS_CLOSE_ON) = COMMENT_WINDOW_DAYS) agrees, null x
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where TYPE = 'Proposed Rule' and COMMENT_WINDOW_DAYS is not null
group by 2 qualify row_number() over (order by count(*) desc) <= 12
union all
select 'recompute', PUBLICATION_YEAR::text, count(*), median(datediff(day, PUBLICATION_DATE, COMMENTS_CLOSE_ON)),
  count_if(datediff(day, PUBLICATION_DATE, COMMENTS_CLOSE_ON) < 30)
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where TYPE = 'Proposed Rule' and COMMENTS_CLOSE_ON is not null and PUBLICATION_YEAR >= 2022
group by 2;

-- [q29] statement 30
-- Federal Register midnight rules by agency: final rules in the Nov 8 - Jan 19 window of the three handover years vs the same agency average over 11 ordinary windows
with d as (select PUBLICATION_DATE dt, IS_SIGNIFICANT sig,
             coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS where TYPE = 'Rule'),
w as (select *, case when dt >= date_from_parts(year(dt),11,8) then year(dt) when dt <= date_from_parts(year(dt),1,19) then year(dt)-1 end wy from d),
g as (select ag, count_if(wy=2016) r16, count_if(wy=2020) r20, count_if(wy=2024) r24,
        count_if(wy=2016 and sig) s16, count_if(wy=2020 and sig) s20, count_if(wy=2024 and sig) s24,
        count_if(wy in (2010,2011,2013,2014,2015,2017,2018,2019,2021,2022,2023)) / 11.0 r_base,
        count_if(wy in (2010,2011,2013,2014,2015,2017,2018,2019,2021,2022,2023) and sig) / 11.0 s_base
      from w where wy is not null group by 1)
(select 'sig24' k, ag, r16, r20, r24, round(r_base,1) r_base, s16, s20, s24, round(s_base,1) s_base from g order by s24 - s_base desc limit 12)
union all
(select 'sig16', ag, r16, r20, r24, round(r_base,1), s16, s20, s24, round(s_base,1) from g order by s16 - s_base desc limit 8)
union all
(select 'sig20', ag, r16, r20, r24, round(r_base,1), s16, s20, s24, round(s_base,1) from g order by s20 - s_base desc limit 8);
