-- roster: every certified hospice in Harris and Bexar counties TX, plus any TX hospice on the two cluster phones, with its enrollment row (CCN join) and a POS termination check (CCN join)
with h as (select CCN, FACILITY_NAME, ADDRESS_LINE_1, ADDRESS_LINE_2, CITY_TOWN, ZIP_CODE, upper(trim(COUNTY_PARISH)) county, regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') ph, OWNERSHIP_TYPE, CERTIFICATION_DATE
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE
  where STATE='TX' and (upper(trim(COUNTY_PARISH)) in ('HARRIS','BEXAR') or regexp_replace(TELEPHONE_NUMBER,'[^0-9]','') in ('7138741234','2814101013'))),
e as (select CCN, count(*) n_enr, max(NPI) npi, max(ASSOCIATE_ID) assoc, max(ORGANIZATION_NAME) org, max(DOING_BUSINESS_AS_NAME) dba, max(INCORPORATION_DATE) inc, max(PROPRIETARY_NONPROFIT) pnp, max(ADDRESS_LINE_1||' '||coalesce(ADDRESS_LINE_2,'')) eaddr
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS where STATE='TX' or ENROLLMENT_STATE='TX' group by 1),
pos as (select CCN, max(PRVDR_CTGRY_CD) cat, max(PGM_TRMNTN_CD) trm, max(TRMNTN_EXPRTN_DT) trm_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where STATE_CD='TX' group by 1)
select h.*, e.n_enr, e.npi, e.assoc, e.org, e.dba, e.inc, e.pnp, e.eaddr, pos.cat, pos.trm, pos.trm_dt
from h left join e on e.CCN=h.CCN left join pos on pos.CCN=h.CCN
order by h.county, h.ph
