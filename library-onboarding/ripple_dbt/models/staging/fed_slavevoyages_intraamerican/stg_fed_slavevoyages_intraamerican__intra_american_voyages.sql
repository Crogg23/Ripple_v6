{{ config(materialized='view') }}

-- 2026-07-30 remediation: this model referenced friendly column names
-- (VOYAGE_ID, YEAR_OF_DEPARTURE, PORT_OF_DEPARTURE, COUNTRY_OF_DEPARTURE,
-- SLAVE_TRADE_COMPANY, DOCTYPE_HTML, ...) that have NEVER existed on the
-- current landing table. scripts/slavevoyages_intraamerican_load.py's own
-- docstring documents why: it replaced a prior dead-scrape load (201 rows of
-- captured HTML page chrome, finding #72) with the real SlaveVoyages I-Am 1.0
-- CSV, which lands under SlaveVoyages' own abbreviated codebook column names
-- (VOYAGEID, TSLAVESD, SLAARRIV, ...). Nobody updated this model after that
-- re-land -- the deployed view has been 100% broken (invalid identifier on
-- every query) since 2026-06-28, silently, because dbt test coverage on this
-- model was never actually run/checked (or its failures went unnoticed).
--
-- Renamed columns below are mapped from the OFFICIAL SlaveVoyages SPSS
-- codebook (legacy.slavevoyages.org/documents/download/SPSS_Codebook_2023-11-06.pdf),
-- not guessed from abbreviations -- this dataset records enslaved people;
-- guessing which column means "embarked" vs "disembarked" is not a risk
-- worth taking. Two fields from the old model are DROPPED rather than
-- reinvented:
--   country_of_departure / country_of_arrival -- the raw table only carries
--     numeric SlaveVoyages place/region codes (PORTDEP, ARRPORT, REGDIS*,
--     REGARR*), resolved to a name only via a separate geography-code
--     appendix that is not landed anywhere in this warehouse. Fabricating a
--     "country" string from an un-joined numeric code would be worse than
--     omitting the field -- carry the raw codes through instead (below) so a
--     real join can be added later if the code table gets landed.
--   doctype_html -- an artifact of the old HTML-chrome dead-scrape; the real
--     dataset never had this field.

with source as (

    select *
    from {{ source('ripple_raw', 'FED_SLAVEVOYAGES_INTRAAMERICAN') }}

),

renamed as (

    select
        -- surrogate / source keys
        VOYAGEID                                                         as voyage_id,

        -- dates (codebook: YEARAM = "Year of arrival at port of disembarkation";
        -- DATEDEPA/B/C = day/month/year the voyage began). Blank source cells
        -- arrive as '' OR a bare space (not a true SQL NULL, since the
        -- loader lands every column as TEXT) -- nullif(trim(x), '') below
        -- converts both to a real NULL so try_to_date/not_null tests aren't
        -- fooled by a blank-but-"populated" string (the same masked-value
        -- trap CLAUDE.md documents for other sources).
        try_to_number(nullif(trim(YEARAM), ''))                          as year_of_arrival,
        try_to_date(nullif(trim(DATEDEPC), '') || '-' ||
                    lpad(nullif(trim(DATEDEPB), ''), 2, '0') || '-' ||
                    lpad(nullif(trim(DATEDEPA), ''), 2, '0'))             as date_of_departure,

        -- geography: numeric SlaveVoyages place codes, NOT resolved names
        -- (see note above -- no code->name table is landed)
        nullif(trim(PORTDEP), '')                                        as port_of_departure_code,
        nullif(trim(ARRPORT), '')                                        as port_of_arrival_code,

        -- measures (codebook, unambiguous):
        --   TSLAVESD = "Total slaves on board at departure from last slaving port"
        --   SLAARRIV = "Total slaves arrived at first port of disembarkation"
        try_to_number(nullif(trim(TSLAVESD), ''))                        as num_enslaved_embarked,
        try_to_number(nullif(trim(SLAARRIV), ''))                        as num_enslaved_disembarked,

        -- descriptive
        nullif(trim(SHIPNAME), '')                                       as vessel_name,
        nullif(trim(CAPTAINA), '')                                       as captain_name,
        nullif(trim(OWNERA), '')                                         as first_owner_name,
        nullif(trim(SOURCEA), '')                                        as source_citation,

        -- raw / audit (real per-row provenance from the loader, not a
        -- current_timestamp() stamped at query time -- see the dedup note)
        INGESTED_AT                                                      as _ingested_at,
        SOURCE_RUN_ID                                                    as _source_run_id

    from source

),

deduped as (

    -- Deduplicates on the REAL per-row landing timestamp (a snapshot-replace
    -- load, so ties are not expected in practice, but this is now a genuine
    -- tiebreak instead of one computed at query time that's identical for
    -- every row in a run).
    select *,
        row_number() over (
            partition by voyage_id
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    voyage_id,
    year_of_arrival,
    date_of_departure,
    port_of_departure_code,
    port_of_arrival_code,
    num_enslaved_embarked,
    num_enslaved_disembarked,
    vessel_name,
    captain_name,
    first_owner_name,
    source_citation,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
