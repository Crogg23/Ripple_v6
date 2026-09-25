-- q13 GNIS FIX: q06/q08/q10/q12 used REGEXP_LIKE patterns anchored at the start of the name, so they only caught names that BEGIN with the term
-- ("Big Squaw Creek", "Cerro Negro" were missed). This extract pulls every row (official and variant) for every feature where ANY name
-- has one of the terms anywhere as a word start; all counts are redone locally from this file.
WITH hit AS (
  SELECT DISTINCT FEATURE_ID
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
  WHERE REGEXP_LIKE(UPPER(FEATURE_NAME),
    '.*(^|[^A-Z])(SQUAW|NIGGER|NEGRO|JAPS?([^A-Z]|$)|CHINAM[AE]N|CHINKS?([^A-Z]|$)|DAGOS?([^A-Z]|$)|DARKE?YS?([^A-Z]|$)|HALF[- ]?BREED|REDSKIN|SAMBOS?([^A-Z]|$)|INJUNS?([^A-Z]|$)|WOPS?([^A-Z]|$)|GOOKS?([^A-Z]|$)|PICKANINN).*')
)
SELECT g.FEATURE_ID, g.FEATURE_NAME, g.FEATURE_NAME_OFFICIAL, g.SOURCE_ORIGINATOR, g.SOURCE_REF_TYPE,
       g.PUBLICATION_DATE, g.DATE_CREATED, LEFT(g.CITATION, 160) citation
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES g JOIN hit ON hit.FEATURE_ID = g.FEATURE_ID
