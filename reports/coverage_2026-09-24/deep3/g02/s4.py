from q import run
M = "LIBRARY_MARTS.HEALTH."
P = f"{M}HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT"
N = f"{M}HEALTH__FED_CMS_NPPES"
RISK = "('12-69','00-08','00-06','12-59','12-47','12-A5','12-D6','12-D5','12-63','12-73','53-D1','12-31')"
run("S12", "PECOS high-risk org enrollments -> NPPES practice address; addresses stacking 4+ new (2023+) enrollments",
    f"""WITH p AS (
          SELECT NPI, ENRLMT_ID, PROVIDER_TYPE_CD, PROVIDER_TYPE_DESC, STATE_CD, ORG_NAME,
                 TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD') d
          FROM {P}
          WHERE LEFT(ENRLMT_ID,1) = 'O' AND (PROVIDER_TYPE_CD LIKE '30-%' OR PROVIDER_TYPE_CD IN {RISK})),
        n AS (
          SELECT NPI,
                 UPPER(REGEXP_REPLACE(PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS,'[^A-Za-z0-9]','')) a1,
                 UPPER(TRIM(PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS)) a2,
                 LEFT(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE,5) z,
                 UPPER(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME) city,
                 PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st,
                 UPPER(AUTHORIZED_OFFICIAL_LAST_NAME || ', ' || AUTHORIZED_OFFICIAL_FIRST_NAME) ao,
                 PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER tel
          FROM {N} WHERE NPI IN (SELECT NPI FROM p))
        SELECT n.a1, n.z, ANY_VALUE(n.city) city, ANY_VALUE(n.st) st,
               COUNT(DISTINCT p.NPI) npis_all,
               COUNT(DISTINCT IFF(p.d >= '2023-01-01', p.NPI, NULL)) npis_new,
               COUNT(DISTINCT IFF(p.d >= '2023-01-01', p.ORG_NAME, NULL)) orgs_new,
               COUNT(DISTINCT IFF(p.d >= '2023-01-01', n.ao, NULL)) officials_new,
               COUNT(DISTINCT IFF(p.d >= '2023-01-01', n.a2, NULL)) suites_new,
               COUNT(DISTINCT IFF(p.d >= '2023-01-01', n.tel, NULL)) phones_new,
               ARRAY_AGG(DISTINCT IFF(p.d >= '2023-01-01', p.PROVIDER_TYPE_DESC, NULL)) types_new,
               ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(p.d >= '2023-01-01', p.ORG_NAME, NULL)), 0, 12) names_new,
               ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(p.d >= '2023-01-01', n.ao, NULL)), 0, 12) aos_new,
               ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(p.d >= '2023-01-01', p.NPI, NULL)), 0, 40) npi_list_new,
               MIN(p.d) d0, MAX(p.d) d1
        FROM p JOIN n ON n.NPI = p.NPI
        GROUP BY n.a1, n.z
        HAVING COUNT(DISTINCT IFF(p.d >= '2023-01-01', p.NPI, NULL)) >= 3
        ORDER BY npis_new DESC""")
