{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per insider filing (accession_number is unique)
-- Answers: What insider trading filings have been made, for which companies?
-- Source: SEC EDGAR Form 3/4/5 â€” Submissions (~1.77M filings)
-- Key joins: issuercik â†’ SEC EDGAR companies; accession_number â†’ transactions + owners
--
-- KEY RE-PROOF (2026-09-20 -- same hole f41ebff9 closed in staging: 289 views
-- deduped on a key proven unique ONCE, at generation time, that silently stopped
-- identifying a row after a reload while `unique` stayed green forever, because
-- the test only ever checked the ALREADY-DEDUPED output). key_proof below re-runs
-- scripts/generate_staging_models.py's key_is_unique_within_each_load() math live,
-- every build: COUNT(*) vs COUNT(DISTINCT HASH(accession_number)), grouped by
-- _SOURCE_RUN_ID when that column is a genuine load id (>= 100 rows/run average --
-- some CMS tables stamp a per-ROW uuid there instead, which would make ANY key
-- "prove" unique; MIN_ROWS_PER_LOAD=100 mirrors the generator exactly). The
-- staging ref this model reads from is a pure passthrough (no filter, no dedup),
-- so this checks the LANDING table directly -- same row set, and the only place
-- _SOURCE_RUN_ID survives (the staging passthrough drops it).
-- Live-verified 2026-09-20: 1,772,088 rows, 1,772,088 distinct ACCESSION_NUMBER,
-- 1 load to date, zero collision -- proven, so the QUALIFY below partitions by
-- accession_number alone. If a future reload ever breaks that, would_collapse > 0
-- and the SAME QUALIFY automatically falls back to a whole-row partition (every
-- data column, so only exact copies collapse) -- schema.yml's `unique` test
-- should be dropped the day this ever shows would_collapse > 0.

with key_load_shape as (

    select count(*) as total_rows, count(distinct _SOURCE_RUN_ID) as n_runs
    from {{ source('ripple_raw', 'FED_SEC_INSIDER_SUBMISSION') }}

),

key_proof as (

    select coalesce(sum(n - d), 0) as would_collapse
    from (
        select
            case when ls.n_runs > 0 and ls.total_rows / ls.n_runs >= 100
                 then s._SOURCE_RUN_ID else '__ALL__' end    as _load_id,
            count(*)                                          as n,
            count(distinct hash(s.ACCESSION_NUMBER))          as d
        from {{ source('ripple_raw', 'FED_SEC_INSIDER_SUBMISSION') }} s
        cross join key_load_shape ls
        group by 1
    )

),

renamed as (

    select
        trim(accession_number)                           as accession_number,
        try_to_date(filing_date, 'DD-MON-YYYY')           as filing_date,
        try_to_date(period_of_report, 'DD-MON-YYYY')     as period_of_report,
        try_to_date(date_of_orig_sub, 'DD-MON-YYYY')     as date_of_original_submission,
        trim(document_type)                              as document_type,
        trim(issuercik)                                  as issuer_cik,
        trim(issuername)                                 as issuer_name,
        trim(issuertradingsymbol)                        as issuer_ticker,
        (trim(no_securities_owned) = '1') as no_securities_owned,
        (trim(not_subject_sec16) = '1') as not_subject_to_section16,
        trim(remarks)                                    as remarks,
        _loaded_at
    from {{ ref('stg_fed_sec_insider_submission__records') }}

)

select
    r.accession_number, r.filing_date, r.period_of_report, r.date_of_original_submission,
    r.document_type, r.issuer_cik, r.issuer_name, r.issuer_ticker, r.no_securities_owned,
    r.not_subject_to_section16, r.remarks, r._loaded_at
from renamed r
cross join key_proof kp
-- partition: accession_number is unconditional; every other column only engages
-- (goes non-null) when kp.would_collapse != 0, i.e. the key is NOT proven -- at
-- that point this IS a whole-row partition, same shape as
-- generate_staging_models.py's fallback.
qualify row_number() over (
    partition by
        r.accession_number,
        case when kp.would_collapse != 0 then r.filing_date else null end,
        case when kp.would_collapse != 0 then r.period_of_report else null end,
        case when kp.would_collapse != 0 then r.date_of_original_submission else null end,
        case when kp.would_collapse != 0 then r.document_type else null end,
        case when kp.would_collapse != 0 then r.issuer_cik else null end,
        case when kp.would_collapse != 0 then r.issuer_name else null end,
        case when kp.would_collapse != 0 then r.issuer_ticker else null end,
        case when kp.would_collapse != 0 then r.no_securities_owned else null end,
        case when kp.would_collapse != 0 then r.not_subject_to_section16 else null end,
        case when kp.would_collapse != 0 then r.remarks else null end
    order by r._loaded_at desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             r.filing_date nulls last, r.period_of_report nulls last, r.date_of_original_submission nulls last,
             r.document_type nulls last, r.issuer_cik nulls last, r.issuer_name nulls last,
             r.issuer_ticker nulls last, r.no_securities_owned nulls last, r.not_subject_to_section16 nulls last,
             r.remarks nulls last
) = 1
