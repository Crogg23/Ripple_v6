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
 from h where CURRENT_MINE_STATUS='Active' order by NO_EMPLOYEES desc nulls last limit 15)
