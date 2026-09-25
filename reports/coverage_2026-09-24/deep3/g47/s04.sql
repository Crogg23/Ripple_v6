-- S04 the two state lookups side by side: do CB_STATE and DIM_STATE hold the same 56 places with the same codes and names?
SELECT COALESCE(c.statefp, d.state_fips) fips, c.stusps, d.state_abbr, c.name cb_name, d.state_name dim_name,
       d.census_region, d.census_division, c.lsad, c.geoid, c.vintage,
       TRY_TO_NUMBER(c.aland) aland_m2, TRY_TO_NUMBER(c.awater) awater_m2,
       c._source_run_id, c._ingested_at, ST_NPOINTS(c.geometry) geom_points,
       LENGTH(d.state_fips) dim_fips_len
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_STATE c
FULL OUTER JOIN LIBRARY_MARTS.REFERENCE.REF__DIM_STATE d ON d.state_fips = c.statefp
ORDER BY 1
