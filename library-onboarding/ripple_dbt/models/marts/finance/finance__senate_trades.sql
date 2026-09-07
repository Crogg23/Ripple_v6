{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per reported Senate trade line, 2012 to now, both eras.
-- Row count is exactly old + new. The name match never adds or drops a row.
--
-- Two sources that never overlap, glued at the seam:
--   finance__fed_senate_stock_watcher   2012-06-14 .. 2020-12-02   8,350 rows
--   finance__fed_senate_efd_ptr         2021-01 .. now              6,855 rows
-- The old one is a third-party re-parse that stopped publishing. The new one
-- is scraped straight off efdsearch.senate.gov. No dedupe across the seam is
-- needed because no date appears in both.
--
-- WHAT THIS ADDS over a plain union: the senator is resolved to a BIOGUIDE id
-- so the trades join to committees, votes and FEC money. Neither source
-- carries an id, only a name, and the names are ugly on both sides:
--   old: 'A. Mitchell Mcconnell, Jr.', 'David A Perdue , Jr', 'Jerry Moran,'
--   new: 'Scott' with the first name only in the filings index
-- The match is done once per distinct name_key (raw name + the index's first
-- and last name for that filing), then joined back, so it can never multiply
-- or lose a trade. The raw string alone is not a person: 'Senator' covers 98
-- rows from four people and 'Former Senator (Former Senator)' is two. It walks two steps against
-- POLITICS__MEMBER_CROSSWALK restricted to people who held a Senate seat
-- since 2012:
--   1. last name, as the last token OR the last two tokens ('Van Hollen')
--   2. if that hits more than one senator, the first initial breaks the tie
--      ('Scott' -> Rick vs Tim)
-- match_note says which step landed it, or why it did not. A null bioguide is
-- a visible miss, never a silent one.
--
-- THREE THINGS THAT ARE STILL TRUE:
--   * amount is a RANGE ('$1,001 - $15,000'), never a number, in both eras.
--   * is_amendment = 'True' on 1,030 new-era rows and NOTHING supersedes the
--     original yet. Old-era rows carry null because the source never said.
--   * 100 new-era rows are filing_kind = 'paper': scanned, unreadable, null
--     trade fields. Filter them from any count and say how many you dropped.

with old_era as (

    select
        null                                        as filing_id,
        senator                                     as senator_raw,
        null                                        as filer_first,
        null                                        as filer_last_clean,
        transaction_date,
        null::date                                  as filed_date,
        owner,
        ticker,
        asset_description,
        asset_type,
        type                                        as transaction_type,
        amount                                      as amount_range,
        comment,
        ptr_link,
        null                                        as filing_kind,
        null                                        as is_amendment,
        'fed_senate_stock_watcher'                  as source_id
    from {{ ref('finance__fed_senate_stock_watcher') }}

),

new_era as (

    -- the PTR mart's senator column is sometimes the literal word 'Senator';
    -- the filings index carries the real first and last name per filing.
    select
        p.filing_id,
        coalesce(nullif(f.filer_full, ''), p.senator) as senator_raw,
        f.filer_first,
        p.filer_last_clean,
        p.transaction_date,
        p.filed_date,
        p.owner,
        p.ticker,
        p.asset_description,
        p.asset_type,
        p.transaction_type,
        p.amount_range,
        p.comment,
        p.ptr_link,
        p.filing_kind,
        p.is_amendment,
        p.source_id
    from {{ ref('finance__fed_senate_efd_ptr') }} p
    left join {{ ref('politics__fed_senate_efd_filings') }} f
        on f.filing_id = p.filing_id

),

trades as (
    -- name_key is what the match is done on. The raw string alone is NOT a
    -- person: 'Senator' covers 98 rows from many filers and 'Former Senator
    -- (Former Senator)' is both Roberts and Rubio. The index's first and last
    -- name per filing make it one.
    select *,
        senator_raw || '|' || coalesce(filer_last_clean, '') || '|' || coalesce(filer_first, '') as name_key
    from (
        select * from old_era
        union all
        select * from new_era
    )
),

-- one parse per distinct raw name. Suffix off (any case), trailing comma off,
-- then the last token and the last two tokens, plus a first initial.
names as (

    -- new era: the index writes 'Last, First (Senator)', so the parse below
    -- would land 'SENATOR)'. The loader already stripped a clean last name;
    -- use it there, and only parse the old era's 'First M Last, Jr' strings.
    select
        name_key,
        coalesce(upper(nullif(filer_last_clean, '')),
                 upper(regexp_substr(cleaned, '[^[:space:]]+$')))                as last_token,
        coalesce(upper(nullif(filer_last_clean, '')),
                 upper(regexp_substr(cleaned, '[^[:space:]]+[[:space:]]+[^[:space:]]+$'))) as last_two_tokens,
        upper(left(coalesce(
            nullif(filer_first, ''),
            -- old era: 'A. Mitchell Mcconnell' -> skip a lone initial
            regexp_replace(cleaned, '^[A-Za-z][.][[:space:]]+', '')
        ), 1))                                                                   as first_init
    from (
        select distinct
            name_key,
            filer_first,
            filer_last_clean,
            regexp_replace(
                regexp_replace(senator_raw, '[[:space:]]*,?[[:space:]]*(Jr[.]?|Sr[.]?|II|III|IV)[[:space:]]*$', '', 1, 0, 'i'),
                '[[:space:],]+$', '')                                            as cleaned
        from trades
    )

),

-- one row per senator who held a seat since 2012: 188 rows, 188 ids. The
-- full crosswalk carries 13 duplicated bioguide rows; none fall in this
-- subset today, the qualify is a belt for the day one does.
-- KNOWN HOLE: Brown (Scott P. / Sherrod) and Nelson (Bill / Ben) share a
-- last name and a first initial. A PTR from either lands null bioguide with
-- match_note 'ambiguous: 2 senators share it'. Neither has filed yet.
senators as (

    select
        bioguide,
        full_name,
        upper(name_last)            as name_last,
        upper(left(name_first, 1))  as first_init
    from {{ ref('politics__member_crosswalk') }}
    where last_term_type = 'sen'
      and last_term_end >= '2012-01-03'
    qualify row_number() over (partition by bioguide order by last_term_end desc) = 1

),

candidates as (

    select
        n.name_key,
        s.bioguide,
        s.full_name,
        (s.first_init = n.first_init)                                as init_hit,
        count(s.bioguide)            over (partition by n.name_key) as n_last,
        count_if(s.first_init = n.first_init)
                                     over (partition by n.name_key) as n_init
    from names n
    left join senators s
        on s.name_last = n.last_token
        or s.name_last = n.last_two_tokens

),

name_map as (

    select
        name_key,
        case when n_last = 1 or (n_last > 1 and n_init = 1 and init_hit) then bioguide  end as bioguide,
        case when n_last = 1 or (n_last > 1 and n_init = 1 and init_hit) then full_name end as senator_name,
        case
            when n_last = 1                   then 'last name'
            when n_last > 1 and n_init = 1    then 'last name + first initial'
            when n_last = 0                   then 'no senator with that last name'
            else 'ambiguous: ' || n_last || ' senators share it'
        end                                                           as match_note
    from candidates
    -- keep the winning candidate row, or any one row when nothing won
    qualify row_number() over (
        partition by name_key
        order by case when n_last = 1 or (n_last > 1 and n_init = 1 and init_hit) then 0 else 1 end
    ) = 1

)

select
    t.filing_id,
    t.senator_raw,
    m.bioguide,
    m.senator_name,
    m.match_note,
    t.transaction_date,
    t.filed_date,
    t.owner,
    t.ticker,
    t.asset_description,
    t.asset_type,
    t.transaction_type,
    t.amount_range,
    t.comment,
    t.ptr_link,
    t.filing_kind,
    t.is_amendment,
    t.source_id
from trades t
left join name_map m
    on m.name_key = t.name_key
