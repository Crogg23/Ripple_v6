{#
    staging_casts.sql -- the casts scripts/generate_staging_models.py emits.

    The generator decides WHICH cast from reports/landing_column_profile_*.tsv
    (a 10,000-row sample per landing table, scripts/profile_landing_columns.py).
    These macros are HOW. Every one is a try_ cast: a value that does not parse
    becomes NULL, never an error and never a wrong value. A NULL where the raw
    column was filled is countable, so a bad cast can be found afterwards.

    Conventions match clean.sql: each returns a SQL expression, no trailing comma.
#}


{#- Chris's ruling 2026-09-19: '' and 'nan' become NULL everywhere. Both are
    loader artifacts ('nan' is pandas writing an empty cell), never data. Other
    null words ('n/a', 'none', 'NA') are left alone in text columns -- 'NA' is
    also Namibia, 'none' can be the real answer. The value itself is NOT
    trimmed; only the test is. -#}
{% macro null_junk(col) -%}
    iff(trim({{ col }}) = '' or lower(trim({{ col }})) = 'nan', null, {{ col }})
{%- endmacro %}


{#- Whole numbers, including the '13925.0' shape a float-typed loader leaves
    behind. The regex guard matters: a bare try_to_number(v, 38, 0) ROUNDS
    '1.5' to 2. Anything that is not a whole number goes NULL instead. -#}
{% macro stg_int(col) -%}
    iff(regexp_like(trim({{ col }}), '[+-]?[0-9]+([.]0+)?'), try_to_number(trim({{ col }}), 38, 0), null)
{%- endmacro %}


{#- Chris's ruling 2026-09-19: a whole-number column where over 90% of the
    filled values are different from each other is an ID, not a measure (FDIC
    CERT, not NUMBER_OF_PATIENTS). It stays TEXT so a join to a text ID
    elsewhere never errors on junk -- but the float-loader tail comes off:
    '13925.0' reads '13925'. -#}
{% macro stg_id_text(col) -%}
    regexp_replace(trim({{ null_junk(col) }}), '^([+-]?[0-9]+)[.]0+$', '\\1')
{%- endmacro %}


{#- 'nan' is excluded first: Snowflake parses the STRING 'nan' to the float NaN,
    which then poisons every sum and average it touches. -#}
{% macro stg_float(col) -%}
    try_to_double(iff(lower(trim({{ col }})) = 'nan', null, trim({{ col }})))
{%- endmacro %}


{#- fmt 'auto' needs a - or / BETWEEN two characters. A bare run of digits is
    read by Snowflake as seconds since 1970, so '2015' would parse to January
    1970 -- and '-7' parses to 1969-12-31 (checked live 2026-09-19), so a
    leading minus sign must not count as a date separator.
    An explicit fmt needs exactly 8 digits: try_to_date('2015', 'MMDDYYYY')
    is a day in the year 5 (also checked live). -#}
{#- Year-first slash dates: Snowflake's auto-detect reads '2018-06-23' and
    '6/23/2018' but NOT '2018/06/23' (checked live 2026-09-19; one portal table
    was loaded twice, once in each shape, and half its dates went NULL). The
    slashes become dashes first. -#}
{% macro _stg_ymd_dashes(col) -%}
    regexp_replace(trim({{ col }}), '^([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})', '\\1-\\2-\\3')
{%- endmacro %}


{% macro stg_date(col, fmt='auto') -%}
{%- if fmt == 'auto' -%}
    iff(regexp_like(trim({{ col }}), '.*[0-9A-Za-z][-/][0-9A-Za-z].*'), try_to_date({{ _stg_ymd_dashes(col) }}), null)
{%- else -%}
    iff(regexp_like(trim({{ col }}), '[0-9]{8}'), try_to_date(trim({{ col }}), '{{ fmt }}'), null)
{%- endif -%}
{%- endmacro %}


{#- A value that carries its own offset ('...09:00:00+05:30', '...Z') is moved
    to UTC. A bare try_to_timestamp_ntz keeps the wall clock and throws the
    offset away without a sound -- 12 columns, about 41,000 rows, found by the
    skeptic pass 2026-09-19. A value with no offset is kept as written; nobody
    knows its zone. The offset must follow a time, or the '-15' at the end of
    '2024-03-15' would read as one. -#}
{% macro stg_ts(col) -%}
{%- set v = _stg_ymd_dashes(col) -%}
    iff(regexp_like(trim({{ col }}), '.*[0-9A-Za-z][-/][0-9A-Za-z].*'),
        iff(regexp_like(trim({{ col }}), '.*[0-9]:[0-9]{2}([.][0-9]+)?\\s*([+-][0-9]{2}(:?[0-9]{2})?|Z)'),
            convert_timezone('UTC', try_to_timestamp_tz({{ v }}))::timestamp_ntz,
            try_to_timestamp_ntz({{ v }})), null)
{%- endmacro %}


{#- Same epoch guard as stg_ts, but the value keeps its own offset and its
    TIMESTAMP_TZ type. For a source that writes LOCAL midnight with an offset
    (GLEIF: '2012-07-25T00:00:00+02:00'), moving to UTC pushes the calendar
    date back a day -- 1,070,259 of 3,382,301 GLEIF creation dates, measured
    live 2026-09-21. Use this where the local date is the fact. -#}
{% macro stg_ts_tz(col) -%}
    iff(regexp_like(trim({{ col }}), '.*[0-9A-Za-z][-/][0-9A-Za-z].*'), try_to_timestamp_tz({{ _stg_ymd_dashes(col) }}), null)
{%- endmacro %}


{#- Only the words true / false get here (the profile keeps y/n apart on
    purpose; INCLUDE is a 'Y'/'N' string and stays one). -#}
{% macro stg_bool(col) -%}
    try_to_boolean(trim({{ col }}))
{%- endmacro %}
