-- S19 NASA open data: is the API key in REQUEST_URL NASA's public DEMO_KEY (count only, key not printed); hazardous asteroid count
SELECT API_NAME, COUNT(*) n, COUNT_IF(REQUEST_URL ILIKE '%api_key=DEMO_KEY%') demo_key, COUNT_IF(REQUEST_URL ILIKE '%api_key=%') any_key,
       COUNT_IF(DESCRIPTION ILIKE 'Hazardous: True%') hazardous, COUNT(DISTINCT REQUEST_URL) urls
FROM LIBRARY_MARTS.SCIENCE.SCIENCE__FED_NASA_OPEN_DATA GROUP BY 1;
