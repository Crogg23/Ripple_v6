{{ config(materialized='table', schema='JUSTICE') }}

-- Source: ATF Federal Firearms Licensees list (77,514 rows)
-- Landed via the ArcGIS FeatureServer that hosts ATF's FFL layer -- atf.gov
-- itself site-wide-blocks automated fetches (403 on plain requests/curl,
-- even with a browser user-agent). See scripts/atf_ffl_load.py.
-- FFL number is not a single source column; it's the 6-part license number
-- ATF prints as REGN-DIST-CNTY-TYPE-XPRDTE-SEQN. Verified unique across all
-- 77,514 rows (COUNT(*) = COUNT(DISTINCT composite) = 77,514).

-- Zips: the ArcGIS layer serves them as numbers, so leading zeros are gone at
-- source -- 3,333 of 77,514 rows (2026-09-23 catalog audit): New England and NJ
-- as 4 digits ('1001'), Puerto Rico and USVI as 3 ('602'), their ZIP+4s as 8 and
-- 7. Zero-fill back to 5, or to 9 for a ZIP+4. A 5- or 9-digit value is untouched.

with source as (
    select * from {{ source('ripple_raw', 'FED_ATF_FFL') }}
)

select
    USER_LIC_REGN || '-' || USER_LIC_DIST || '-' || USER_LIC_CNTY || '-'
        || USER_LIC_TYPE || '-' || USER_LIC_XPRDTE || '-' || USER_LIC_SEQN
        as ffl_number,
    USER_LIC_REGN as lic_region,
    USER_LIC_DIST as lic_district,
    USER_LIC_CNTY as lic_county,
    USER_LIC_TYPE as lic_type,
    USER_LIC_XPRDTE as lic_expiration_code,
    USER_LIC_SEQN as lic_sequence,
    USER_LICENSE_NAME as license_name,
    USER_BUSINESS_NAME as business_name,
    USER_PREMISE_STREET as premise_street,
    USER_PREMISE_CITY as premise_city,
    USER_PREMISE_STATE as premise_state,
    iff(length(USER_PREMISE_ZIP_CODE) in (3, 4, 7, 8),
        lpad(USER_PREMISE_ZIP_CODE, iff(length(USER_PREMISE_ZIP_CODE) > 5, 9, 5), '0'),
        USER_PREMISE_ZIP_CODE) as premise_zip_code,
    USER_MAIL_STREET as mail_street,
    USER_MAIL_CITY as mail_city,
    USER_MAIL_STATE as mail_state,
    iff(length(USER_MAIL_ZIP_CODE) in (3, 4, 7, 8),
        lpad(USER_MAIL_ZIP_CODE, iff(length(USER_MAIL_ZIP_CODE) > 5, 9, 5), '0'),
        USER_MAIL_ZIP_CODE) as mail_zip_code,
    USER_VOICE_PHONE as voice_phone,
    {{ stg_float('X') }} as longitude,
    {{ stg_float('Y') }} as latitude
from source
