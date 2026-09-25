-- all TX certified hospices (roster) with their enrollment row, full outer so enrollment-only rows show too
with h as (select CCN, FACILITY_NAME, ADDRESS_LINE_1, CITY_TOWN, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, OWNERSHIP_TYPE, CERTIFICATION_DATE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE where STATE='TX'),
e as (select CCN, NPI, ASSOCIATE_ID, ORGANIZATION_NAME, DOING_BUSINESS_AS_NAME, INCORPORATION_DATE, ADDRESS_LINE_1 e_a1, CITY e_city
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS where STATE='TX')
select coalesce(h.CCN,e.CCN) ccn, h.FACILITY_NAME, h.ADDRESS_LINE_1, h.CITY_TOWN, h.county, h.ph, h.OWNERSHIP_TYPE, h.CERTIFICATION_DATE,
  e.NPI, e.ASSOCIATE_ID, e.ORGANIZATION_NAME, e.DOING_BUSINESS_AS_NAME, e.INCORPORATION_DATE, e.e_a1, e.e_city, iff(h.CCN is null,'enr_only',iff(e.CCN is null,'roster_only','both')) side
from h full outer join e on e.CCN=h.CCN
