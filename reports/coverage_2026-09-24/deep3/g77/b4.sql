-- S14 Earthquakes: lower-48 M3+ by half-degree cell and year, full year and the Jan 1 - Jun 13 window the 2026 data covers - peer set for the New Mexico cluster
SELECT FLOOR(TRY_TO_DOUBLE(LATITUDE)*2)/2 lat0, FLOOR(TRY_TO_DOUBLE(LONGITUDE)*2)/2 lon0, YEAR(TIME) yr,
       COUNT(*) m3, COUNT_IF(TO_CHAR(TIME,'MMDD') <= '0613') m3_win, COUNT_IF(MAG >= 4) m4, MAX(MAG) max_mag,
       COUNT(DISTINCT TO_DATE(TIME)) days, ANY_VALUE(PLACE) place_eg
FROM LIBRARY_MARTS.SCIENCE.SCIENCE__FED_USGS_EARTHQUAKES
WHERE TYPE = 'earthquake' AND MAG >= 3
  AND TRY_TO_DOUBLE(LATITUDE) BETWEEN 24 AND 50 AND TRY_TO_DOUBLE(LONGITUDE) BETWEEN -125 AND -66
GROUP BY 1,2,3 ORDER BY 1,2,3;
