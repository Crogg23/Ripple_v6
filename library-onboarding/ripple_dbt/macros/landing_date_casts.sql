{#
    landing_date_casts.sql -- casts for every date/time-shaped LANDING column,
    warehouse-wide. Built 2026-09-03 from a full-warehouse inventory of the
    2,208 content-recon'd landing tables (reports/recon/date_cast_inventory_*.csv,
    reports/recon/date_derive_rules_*.csv).

    HOW THIS RELATES TO macros/ripple_time.sql
    -------------------------------------------
    ripple_time.sql answers a narrower, curated question: for each of the 669
    MART tables, which ONE column is the canonical real-world clock, so the
    cross-warehouse timeline feature has a single trustworthy axis per source.
    Its registry (seeds/ripple_time_registry.csv) makes an editorial call --
    FED_USGS_WBD_HUC8 is correctly marked clock='none' there, because its only
    time-shaped column is Ripple's own download stamp, not a real-world event.

    This file answers a different, blanket question: is every date/time-shaped
    column in the RAW warehouse -- landing and staging, whether or not it ever
    becomes a mart, whether or not it is anyone's canonical clock -- stored as
    a proper typed value instead of raw text or a bare epoch integer. That
    download stamp still deserves a real TIMESTAMP_NTZ type, even though it
    will never be the mart's canonical clock.

    The two files do not compete: apply these macros in staging, let
    ripple_time.sql keep making the editorial canonical-clock call on top.

    Every cast expression below was validated against Snowflake with a
    zero-table constant SELECT before being written here (2026-09-03 session).

    Conventions match clean.sql / ripple_time.sql: every macro returns a SQL
    *expression* with no trailing comma, so it drops into a SELECT list, and
    the raw column is never overwritten -- these sit beside it.
#}


{#- ==================== CONTENT-DETECTED TEXT/NUMBER DATES ====================
    fmt matches date_cast_inventory.py's classifier exactly:
      iso       2026-03-15(T09:00:00)?
      us        3/15/2026, with or without a trailing time -- COALESCE both,
                a bare HH12 format returns NULL on a date-only value (verified live)
      ymd8      20260315
      mdy8      03152026          <- FEC's TRANSACTION_DT shape
      dmon      15-MAR-2026 / 15-MAR-26
      epochms   epoch MILLISECONDS, text ('...000.0') or numeric
      epochs    epoch SECONDS, text or numeric

    typ is the landing column's data_type ('TEXT', 'NUMBER', 'FLOAT') --
    string-pattern formats need TO_VARCHAR() first on a numeric column.
-#}
{% macro landing_parse_date(col, fmt, typ='TEXT') -%}
{%- set c = col -%}
{%- set numeric = typ in ('NUMBER', 'FLOAT') -%}
{%- if fmt == 'iso' -%}
    {%- if numeric %}TRY_TO_TIMESTAMP_NTZ(TO_VARCHAR({{ c }}))
    {%- else %}TRY_TO_TIMESTAMP_NTZ({{ c }}){% endif -%}
{%- elif fmt == 'us' -%}
    {%- set v = ("TO_VARCHAR(" ~ c ~ ")") if numeric else c -%}
    COALESCE(TRY_TO_TIMESTAMP_NTZ({{ v }}, 'MM/DD/YYYY HH12:MI:SS AM'), TRY_TO_TIMESTAMP_NTZ({{ v }}, 'MM/DD/YYYY'))
{%- elif fmt == 'ymd8' -%}
    {%- if numeric %}TRY_TO_DATE(TO_VARCHAR({{ c }}), 'YYYYMMDD')
    {%- else %}TRY_TO_DATE({{ c }}, 'YYYYMMDD'){% endif -%}
{%- elif fmt == 'mdy8' -%}
    {%- if numeric %}TRY_TO_DATE(TO_VARCHAR({{ c }}), 'MMDDYYYY')
    {%- else %}TRY_TO_DATE({{ c }}, 'MMDDYYYY'){% endif -%}
{%- elif fmt == 'dmon' -%}
    {%- set v = ("TO_VARCHAR(" ~ c ~ ")") if numeric else c -%}
    COALESCE(TRY_TO_DATE({{ v }}, 'DD-MON-YY'), TRY_TO_DATE({{ v }}, 'DD-MON-YYYY'))
{%- elif fmt == 'epochms' -%}
    {%- set n = ("FLOOR(" ~ c ~ ")") if numeric else ("TRY_TO_NUMBER(SPLIT_PART(" ~ c ~ ", '.', 1))") -%}
    DATEADD('millisecond', {{ n }}, '1970-01-01'::timestamp_ntz)
{%- elif fmt == 'epochs' -%}
    {%- set n = ("FLOOR(" ~ c ~ ")") if numeric else ("TRY_TO_NUMBER(" ~ c ~ ")") -%}
    DATEADD('second', {{ n }}, '1970-01-01'::timestamp_ntz)
{%- else -%}
    {{ exceptions.raise_compiler_error("landing_parse_date: unknown fmt '" ~ fmt ~ "'") }}
{%- endif -%}
{%- endmacro %}


{#- ==================== AUDIT/INGEST EPOCH COLUMNS ====================
    _INGESTED_AT and friends (483 columns, all NUMBER, found 2026-09-03): the
    loader stamps epoch time but the UNIT varies by table -- seconds,
    milliseconds, or microseconds, with no reliable way to know which without
    looking. This detects the unit from the value's own digit width at query
    time, so one macro call is correct for every table, present and future,
    with no per-table configuration to maintain.

    10 digits or fewer  -> seconds       (~1.7B today)
    11-13 digits        -> milliseconds  (~1.7T today)
    14-16 digits        -> microseconds  (~1.7Q today)  <- the common bug shape
    17-19 digits        -> nanoseconds
-#}
{% macro landing_parse_audit_epoch(col) -%}
{%- set n = "TRUNC(" ~ col ~ ")" -%}
{%- set digits = "LENGTH(TO_VARCHAR(ABS(" ~ n ~ ")))" -%}
    CASE
        WHEN {{ col }} IS NULL THEN NULL
        WHEN {{ digits }} <= 10 THEN DATEADD('second', {{ n }}, '1970-01-01'::timestamp_ntz)
        WHEN {{ digits }} <= 13 THEN DATEADD('millisecond', {{ n }}, '1970-01-01'::timestamp_ntz)
        WHEN {{ digits }} <= 16 THEN DATEADD('microsecond', {{ n }}, '1970-01-01'::timestamp_ntz)
        WHEN {{ digits }} <= 19 THEN DATEADD('nanosecond', {{ n }}, '1970-01-01'::timestamp_ntz)
        ELSE NULL
    END
{%- endmacro %}


{#- ==================== RANGE-IN-ONE-FIELD ====================
    Two verified shapes (2026-09-03, 12 columns total). Anything else stays
    unresolved rather than guessed -- e.g. "Aug 20 - Sep 16, 2024" is NOT safe
    to split, because the year only appears once and belongs to both halves.

    ddmonyyyy: '01Jan2023-31Dec2024' (FED_CMS_DIALYSIS, 10 columns) -- exactly
               one dash, no separator inside each 9-char date, safe to split on it.
    monthyyyy: 'February, 2025 to January, 2026' (1 column) -- split on ' to '.
-#}
{% macro landing_range_start(col, fmt) -%}
{%- if fmt == 'ddmonyyyy' -%}
    TRY_TO_DATE(SPLIT_PART({{ col }}, '-', 1), 'DDMONYYYY')
{%- elif fmt == 'monthyyyy' -%}
    TRY_TO_DATE(SPLIT_PART({{ col }}, ' to ', 1), 'MMMM, YYYY')
{%- else -%}
    {{ exceptions.raise_compiler_error("landing_range_start: unknown fmt '" ~ fmt ~ "'") }}
{%- endif -%}
{%- endmacro %}

{% macro landing_range_end(col, fmt) -%}
{%- if fmt == 'ddmonyyyy' -%}
    TRY_TO_DATE(SPLIT_PART({{ col }}, '-', 2), 'DDMONYYYY')
{%- elif fmt == 'monthyyyy' -%}
    TRY_TO_DATE(SPLIT_PART({{ col }}, ' to ', 2), 'MMMM, YYYY')
{%- else -%}
    {{ exceptions.raise_compiler_error("landing_range_end: unknown fmt '" ~ fmt ~ "'") }}
{%- endif -%}
{%- endmacro %}


{#- ==================== GRANULARITY CODE TRANSLATION ====================
    COURTLISTENER's DATE_GRANULARITY_* columns hold a raw strftime code
    describing how precise the paired date column is, not a date themselves.
    Closed vocabulary -- every value across all 6 columns checked 2026-09-03,
    only 3 codes exist. -#}
{% macro landing_translate_granularity(col) -%}
    CASE {{ col }}
        WHEN '%Y-%m-%d' THEN 'day'
        WHEN '%Y-%m' THEN 'month'
        WHEN '%Y' THEN 'year'
        ELSE NULL
    END
{%- endmacro %}


{#- ==================== TIME-OF-DAY + SIBLING DATE ====================
    A time-only column (STOP_TIME '4:02 AM') has no date of its own -- the
    date lives in a sibling column in the same table (STOP_DATE), found by
    exact name match (TIME token -> DATE token) at inventory time, never
    guessed. date_expr is the sibling's OWN cast expression (e.g. from
    landing_parse_date or ripple_ts_from_date), passed in unevaluated so the
    date only needs to be parsed once.

    Tries every time shape actually seen in the 21 resolved pairs (2026-09-03):
    'HH24:MI:SS', 'HH12:MI:SS AM', 'HH24:MI', 'HH12:MI AM' -- in that order,
    most-specific first. TRIM handles Houston's leading-whitespace values. -#}
{% macro landing_combine_time_date(time_col, date_expr) -%}
{%- set d -%}TO_VARCHAR(({{ date_expr }}), 'YYYY-MM-DD'){%- endset -%}
{%- set t -%}TRIM({{ time_col }}){%- endset -%}
    COALESCE(
        TRY_TO_TIMESTAMP_NTZ({{ d }} || ' ' || {{ t }}, 'YYYY-MM-DD HH24:MI:SS'),
        TRY_TO_TIMESTAMP_NTZ({{ d }} || ' ' || {{ t }}, 'YYYY-MM-DD HH12:MI:SS AM'),
        TRY_TO_TIMESTAMP_NTZ({{ d }} || ' ' || {{ t }}, 'YYYY-MM-DD HH24:MI'),
        TRY_TO_TIMESTAMP_NTZ({{ d }} || ' ' || {{ t }}, 'YYYY-MM-DD HH12:MI AM')
    )
{%- endmacro %}
