{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  FDA Global Substance Registration System (GSRS) substance registry: the UNII
  code with crosswalks to CAS RN, RXCUI, PubChem, InChIKey, NCIt, ITIS, NCBI
  and more — a join-key hub for chemical/drug substance linkage.
  Grain: one row = one substance (UNII verified exactly unique).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FDA_UNII_GSRS_SUBSTANCES') }}
),

renamed as (
    select
        -- identifiers / crosswalks
        nullif(trim(UNII), '')                                     as unii,
        nullif(trim(UUID), '')                                     as gsrs_uuid,
        nullif(trim(RN), '')                                       as cas_rn,
        EC                                                         as ec_number,
        nullif(trim(NCIT), '')                                     as ncit_code,
        nullif(trim(RXCUI), '')                                    as rxcui,
        nullif(trim(PUBCHEM), '')                                  as pubchem_cid,
        nullif(trim(SMSID), '')                                    as smsid,
        nullif(trim(EPA_COMPTOX), '')                              as epa_comptox_id,
        nullif(trim(CATALOGUE_OF_LIFE), '')                        as catalogue_of_life_id,
        nullif(trim(ITIS), '')                                     as itis_tsn,
        nullif(trim(NCBI), '')                                     as ncbi_taxon_id,
        nullif(trim(PLANTS), '')                                   as usda_plants_id,
        nullif(trim(POWO), '')                                     as powo_id,
        nullif(trim(GRIN), '')                                     as grin_id,
        nullif(trim(MPNS), '')                                     as mpns_id,
        nullif(trim(INN_ID), '')                                   as inn_id,
        nullif(trim(USAN_ID), '')                                  as usan_id,
        nullif(trim(DAILYMED), '')                                 as dailymed_name,

        -- substance profile
        nullif(trim(DISPLAY_NAME), '')                             as display_name,
        nullif(trim(MF), '')                                       as molecular_formula,
        nullif(trim(INCHIKEY), '')                                 as inchikey,
        nullif(trim(SMILES), '')                                   as smiles,
        nullif(trim(INGREDIENT_TYPE), '')                          as ingredient_type,
        nullif(trim(SUBSTANCE_TYPE), '')                           as substance_type,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from source
)

select * from renamed
