-- q06 (rerun after a reserved-word compile error) GNIS: slur and derogatory terms, official vs variant. Word-start match (Squaw also catches Squawbush); JAP/COON/CHINK need a word end.
WITH t(term, pat) AS (
  SELECT * FROM VALUES
   ('SQUAW','(^|[^A-Z])SQUAW.*'),
   ('NEGRO','(^|[^A-Z])NEGRO.*'),
   ('NIGGER','(^|[^A-Z])NIGGER.*'),
   ('JAP','(^|[^A-Z])JAPS?([^A-Z].*|$)'),
   ('CHINAMAN','(^|[^A-Z])CHINAM[AE]N.*'),
   ('CHINK','(^|[^A-Z])CHINKS?([^A-Z].*|$)'),
   ('REDSKIN','(^|[^A-Z])REDSKIN.*'),
   ('HALFBREED','(^|[^A-Z])HALF[- ]?BREED.*'),
   ('INJUN','(^|[^A-Z])INJUNS?([^A-Z].*|$)'),
   ('DARKEY','(^|[^A-Z])DARK(E)?YS?([^A-Z].*|$)'),
   ('PICKANINNY','(^|[^A-Z])PICKANINN.*'),
   ('COON (ambiguous: raccoon)','(^|[^A-Z])COONS?([^A-Z].*|$)'),
   ('WOP','(^|[^A-Z])WOPS?([^A-Z].*|$)'),
   ('DAGO','(^|[^A-Z])DAGOS?([^A-Z].*|$)'),
   ('KIKE','(^|[^A-Z])KIKES?([^A-Z].*|$)'),
   ('SPIC','(^|[^A-Z])SPICS?([^A-Z].*|$)'),
   ('GOOK','(^|[^A-Z])GOOKS?([^A-Z].*|$)'),
   ('SAMBO','(^|[^A-Z])SAMBOS?([^A-Z].*|$)')
)
SELECT t.term, g.FEATURE_NAME_OFFICIAL, COUNT(*) n, COUNT(DISTINCT g.FEATURE_ID) features,
       MIN(g.DATE_CREATED) c0, MAX(g.DATE_CREATED) c1,
       COUNT_IF(g.DATE_CREATED >= '2022-09-01') created_since_sep22,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT g.FEATURE_NAME), 0, 6) name_sample,
       COUNT_IF(YEAR(g.PUBLICATION_DATE) >= 2021) pub_since_2021, ARRAY_SLICE(ARRAY_AGG(DISTINCT g.SOURCE_ORIGINATOR), 0, 5) originators
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES g
JOIN t ON REGEXP_LIKE(UPPER(g.FEATURE_NAME), t.pat)
GROUP BY 1,2 ORDER BY 1,2
