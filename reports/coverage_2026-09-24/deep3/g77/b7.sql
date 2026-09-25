-- S17 Earthquakes: near-duplicate check - next event within 20 seconds and about 20 km of the previous one, by the two networks involved
WITH q AS (
  SELECT ID, TIME, NET, MAG, TRY_TO_DOUBLE(LATITUDE) lat, TRY_TO_DOUBLE(LONGITUDE) lon,
         LAG(TIME) OVER (ORDER BY TIME) pt, LAG(NET) OVER (ORDER BY TIME) pnet, LAG(MAG) OVER (ORDER BY TIME) pmag,
         LAG(TRY_TO_DOUBLE(LATITUDE)) OVER (ORDER BY TIME) plat, LAG(TRY_TO_DOUBLE(LONGITUDE)) OVER (ORDER BY TIME) plon
  FROM LIBRARY_MARTS.SCIENCE.SCIENCE__FED_USGS_EARTHQUAKES WHERE TYPE = 'earthquake')
SELECT LEAST(NET, pnet) || '+' || GREATEST(NET, pnet) nets, COUNT(*) pairs,
       COUNT_IF(DATEDIFF('millisecond', pt, TIME) <= 5000) within_5s, ROUND(AVG(ABS(MAG - pmag)),2) avg_mag_gap,
       ANY_VALUE(ID) eg_id
FROM q
WHERE DATEDIFF('millisecond', pt, TIME) <= 20000 AND ABS(lat - plat) <= 0.2 AND ABS(lon - plon) <= 0.2
GROUP BY 1 ORDER BY pairs DESC;

-- S18 Earthquakes: where the June-July 2018 spike sits - place suffix counts for those two months against the same months of 2017 and 2019
SELECT TRIM(REGEXP_SUBSTR(PLACE, '[^,]+$')) region, COUNT_IF(YEAR(TIME) = 2018) y2018, COUNT_IF(YEAR(TIME) = 2017) y2017, COUNT_IF(YEAR(TIME) = 2019) y2019,
       MAX(IFF(YEAR(TIME) = 2018, MAG, NULL)) max2018
FROM LIBRARY_MARTS.SCIENCE.SCIENCE__FED_USGS_EARTHQUAKES
WHERE MONTH(TIME) IN (6,7) AND YEAR(TIME) BETWEEN 2017 AND 2019
GROUP BY 1 ORDER BY y2018 DESC LIMIT 12;
