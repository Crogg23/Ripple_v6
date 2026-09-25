-- S07 = S06 rerun without _SOURCE_RUN_ID (TopoView carries no lineage columns)
SELECT COUNT(*) n, COUNT(DISTINCT sourceid) ids, COUNT(DISTINCT title) titles, COUNT(DISTINCT downloadurl) urls,
       COUNT(DISTINCT sourceid, title, downloadurl, boundingbox) distinct_rows_4col,
       COUNT_IF(NULLIF(TRIM(mpdesc),'') IS NOT NULL) mpdesc_filled, COUNT_IF(NULLIF(TRIM(fileformat),'') IS NOT NULL) fmt_filled,
       COUNT_IF(NULLIF(TRIM(counties),'') IS NOT NULL) counties_filled, COUNT_IF(NULLIF(TRIM(mapscale),'') IS NOT NULL) scale_filled,
       COUNT_IF(NULLIF(TRIM(fips),'') IS NOT NULL) fips_filled, COUNT_IF(NULLIF(TRIM(state),'') IS NOT NULL) state_filled,
       COUNT_IF(NULLIF(TRIM(datasets),'') IS NOT NULL) datasets_filled,
       COUNT(DISTINCT state) states, COUNT(DISTINCT LEFT(publicationdate,4)) pub_years,
       MIN(LEFT(publicationdate,4)) pub0, MAX(LEFT(publicationdate,4)) pub1,
       MIN(datecreated) created0, MAX(datecreated) created1,
       ARRAY_AGG(DISTINCT LEFT(publicationdate,4)) WITHIN GROUP (ORDER BY LEFT(publicationdate,4)) pub_year_list,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.TIMELINE.REFERENCE__FED_USGS_TOPOVIEW) timeline_rows,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('id', sourceid, 'k', k, 'titles', t)) FROM
          (SELECT sourceid, COUNT(*) k, ARRAY_AGG(DISTINCT title) t FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
           GROUP BY 1 HAVING COUNT(*)>1)) dup_ids,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('st', state, 'k', k)) FROM
          (SELECT state, COUNT(*) k FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW GROUP BY 1 ORDER BY 2 DESC LIMIT 8)) top_states,
       ANY_VALUE(title) sample_title
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
