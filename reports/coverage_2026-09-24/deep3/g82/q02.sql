-- BIA tribal geo: confirm shape, test whether GEOMETRY_JSON parses to a geography, sample head of the JSON
select LAR_ID, LAR_NAME, GIS_ACRES, SHAPE_AREA, left(GEOMETRY_JSON, 160) head, length(GEOMETRY_JSON) len,
  try_to_geography(GEOMETRY_JSON) is not null parses,
  round(st_area(try_to_geography(GEOMETRY_JSON))/4046.86) acres_from_geog,
  (select count(*) from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO) n,
  (select count_if(try_to_geography(GEOMETRY_JSON) is not null) from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO) n_parse,
  (select count(distinct LAR_ID) from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO) n_id
from LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO
order by GIS_ACRES desc limit 8
