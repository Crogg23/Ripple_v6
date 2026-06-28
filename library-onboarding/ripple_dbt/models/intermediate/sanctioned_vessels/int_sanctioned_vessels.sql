{{ config(materialized='view') }}

{#
    Union of sanctioned VESSELS across OFAC SDN + OpenSanctions, keyed on a clean
    7-digit IMO -- the left side of sanctioned_vessel_broadcasting v2.

    OpenSanctions catches ~3x the broadcasting hulls OFAC does and only 1,486 of
    OFAC's 1,942 vessel IMOs overlap (discovery sweep #16/#17), so this is a UNION,
    not a replace. OFAC stores a bare IMO column; OpenSanctions buries it in a
    semicolon-delimited IDENTIFIERS string (e.g. '352002470;3E2311;IMO9253325'),
    so we regexp the 'IMO#######' token out first, then normalize_imo() both sides
    to a bare 7-digit hull number the leads engine can join to AIS.
#}

with ofac as (

    select
        'ofac'                                  as sanction_source,
        trim(ENT_NUM)                           as source_id,
        {{ clean_ofac_token('SDN_NAME') }}      as vessel_name,
        {{ clean_ofac_token('PROGRAM') }}       as program,
        {{ clean_ofac_token('VESS_FLAG') }}     as flag,
        {{ normalize_imo('IMO') }}              as imo
    from {{ source('ripple_raw', 'FED_OFAC_SDN') }}
    where {{ normalize_imo('IMO') }} is not null

),

opensanctions_raw as (

    select
        trim(ID)                                  as source_id,
        trim(NAME)                                as vessel_name,
        trim(PROGRAM_IDS)                         as program,
        regexp_substr(IDENTIFIERS, 'IMO[0-9]{7}') as imo_token
    from {{ source('ripple_raw', 'INTL_OPENSANCTIONS') }}
    where SCHEMA = 'Vessel'

),

opensanctions as (

    select
        'opensanctions'                  as sanction_source,
        source_id,
        vessel_name,
        program,
        cast(null as varchar)            as flag,
        {{ normalize_imo('imo_token') }} as imo
    from opensanctions_raw
    where {{ normalize_imo('imo_token') }} is not null

)

select * from ofac
union all
select * from opensanctions
