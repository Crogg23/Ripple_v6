{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2d).
  FULL DATASET as of 2026-08-11: all 27,836 FDIC-insured institutions, active and
  historical, loaded by scripts/fdic_institutions_load.py. Row count matches the
  API's own advertised total exactly, and CERT is unique across all 27,836 rows.
  This replaced a 10,000-row API slice that had carried a sample-only label.

  The full pull also widened the raw table from 24 fields to 164. The columns
  added below are the ones that carry identity or supervision meaning; the rest
  (PRIORNAME1..10 former names, CHANGEC1..15 structure-change codes) are still in
  the raw table if anyone needs them.

  LEI is the one worth knowing about, WITH A CATCH that was checked, not assumed.
  It is the global Legal Entity Identifier, the same key GLEIF is built on -- but
  FDIC publishes it TRUNCATED. Every value here is exactly 16 characters; a real
  LEI is exactly 20. A straight equality join to GLEIF therefore matches ZERO
  rows. Verified 2026-08-11: FDIC's value is the first 16 characters of the full
  LEI, so the join that works is

      on LEFT(gleif.LEI, 16) = fdic.lei

  which matches 2,224 of the 2,252 banks that carry one. Note the scale before
  leaning on it: only 2,252 of 27,836 institutions have an LEI at all (~8%), and
  they skew large -- most small banks have never been issued one. Absence of an
  LEI here says nothing about a bank.

  Grain: one row = one insured institution (CERT unique).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FDIC_BANK_DATA') }}
),

renamed as (
    select
        nullif(trim(CERT), '')                                     as cert,
        nullif(trim(NAME), '')                                     as name,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(STNAME), '')                                   as stname,
        nullif(trim(STALP), '')                                    as stalp,
        nullif(trim(ZIP), '')                                      as zip,
        -- the full API returns the state-county FIPS as STCNTY; the old 10,000-row
        -- slice had requested it under the name FIPS. Same value, kept under the
        -- original output name so nothing downstream has to change.
        nullif(trim(STCNTY), '')                                   as fips,
        nullif(trim(BKCLASS), '')                                  as bkclass,
        nullif(trim(ACTIVE), '')                                   as active,
        try_to_date(left(nullif(trim(DATEUPDT), ''), 10))          as dateupdt,
        try_to_date(left(nullif(trim(ESTYMD), ''), 10))            as estymd,
        try_to_date(left(nullif(trim(ENDEFYMD), ''), 10))          as endefymd,
        try_to_number(nullif(trim(ASSET), ''), 18, 4)              as asset,
        try_to_number(nullif(trim(DEP), ''), 18, 4)                as dep,
        try_to_number(nullif(trim(DEPDOM), ''), 18, 4)             as depdom,
        try_to_number(nullif(trim(NETINC), ''), 18, 4)             as netinc,
        try_to_date(left(nullif(trim(REPDTE), ''), 10))            as repdte,
        -- likewise RSSDID -> FED_RSSD: the Federal Reserve's RSSD identifier under
        -- the name the full API uses.
        nullif(trim(FED_RSSD), '')                                 as rssdid,
        nullif(trim(CHRTAGNT), '')                                 as chrtagnt,
        -- INSTCAT (institution category) is NOT returned by the full institutions
        -- endpoint and has no equivalent field, so it is dropped rather than faked.
        -- Nothing in the project referenced it. BKCLASS and SPECGRP below carry the
        -- charter-class and specialisation grouping that it approximated.
        nullif(trim(SPECGRP), '')                                  as specgrp,
        nullif(trim(HCTMULT), '')                                  as hctmult,
        try_to_number(nullif(trim(LATITUDE), ''), 18, 4)           as latitude,
        try_to_number(nullif(trim(LONGITUDE), ''), 18, 4)          as longitude,
        -- identity / cross-dataset keys (new with the 2026-08-11 full pull)
        nullif(trim(LEI), '')                                      as lei,
        nullif(trim(DOCKET), '')                                   as docket,
        nullif(trim(ID), '')                                       as fdic_id,
        -- holding company
        nullif(trim(NAMEHCR), '')                                  as holding_company_name,
        nullif(trim(CITYHCR), '')                                  as holding_company_city,
        -- location beyond city/state
        nullif(trim(ADDRESS), '')                                  as address,
        nullif(trim(COUNTY), '')                                   as county,
        nullif(trim(CBSA), '')                                     as cbsa,
        nullif(trim(CBSA_METRO_NAME), '')                          as cbsa_metro_name,
        -- charter, supervision and insurance status
        nullif(trim(CHARTER), '')                                  as charter,
        nullif(trim(CLCODE), '')                                   as clcode,
        nullif(trim(FDICREGN), '')                                 as fdic_region,
        nullif(trim(FDICSUPV), '')                                 as fdic_supervisor,
        nullif(trim(OCCDISTDESC), '')                              as occ_district,
        nullif(trim(CONSERVE), '')                                 as in_conservatorship,
        try_to_date(left(nullif(trim(INSDATE), ''), 10))           as insured_date,
        try_to_date(left(nullif(trim(INSDROPDATE), ''), 10))       as insurance_dropped_date,
        -- minority depository institution status
        nullif(trim(MDI_STATUS_CODE), '')                          as mdi_status_code,
        nullif(trim(MDI_STATUS_DESC), '')                          as mdi_status_desc,
        -- merger lineage: where a closed institution's cert went, and its parent
        nullif(trim(NEWCERT), '')                                  as successor_cert,
        nullif(trim(PARCERT), '')                                  as parent_cert,
        -- office counts
        try_to_number(nullif(trim(OFFICES), ''), 18, 0)            as offices,
        try_to_number(nullif(trim(OFFDOM), ''), 18, 0)             as offices_domestic,
        -- try_to_timestamp_ntz, not to_timestamp_ntz(x, 6): the second argument is a
        -- SCALE only for numeric input, and a FORMAT STRING for text. This loader
        -- writes the ingest stamp as an ISO text value, so passing 6 is a compile
        -- error ("format argument needs to be a string"). try_ also means a single
        -- malformed stamp yields NULL instead of failing the whole build.
        try_to_timestamp_ntz(_INGESTED_AT)                         as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
