    with source as (
        select * from {{ source('ripple_raw', 'INT_UK_COMPANIES_HOUSE') }}
    )

    select
        "CompanyNumber" as UK_COMPANY_NUMBER,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    -- 2026-08-25: exactly 1 of 5,734,780 raw rows has a null CompanyNumber
    -- and every other field blank (CompanyName='', all remaining columns
    -- null, only loader metadata populated) -- a single blank/stray row in
    -- the Companies House bulk CSV dump, not a real company record.
    -- CompanyNumber is Companies House's own primary key and is populated
    -- on every genuine record, so this one row is dropped here.
    where "CompanyNumber" is not null
    qualify row_number() over (
        partition by UK_COMPANY_NUMBER
        order by _INGESTED_AT desc
    ) = 1
