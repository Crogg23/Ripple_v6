{#
    ripple_time.sql -- the Ripple datetime standard. One set of rules, one place.

    WHY THIS EXISTS
    ---------------
    The 2026-08-20 time-index scan measured every date-shaped column in all 686
    mart tables (2,223 columns, 1.195B rows). What it found:

      * Most of Ripple's time data is NOT dates. Of 2,223 columns, 414 carry a
        bare year, 34 a year-month, 21 a year-quarter. Only ~1,074 are day-grain.
        A standard that only handles dates covers less than half the warehouse.
      * The recurring corruption is always the same shape: a value that is not a
        day-grain date gets handed to a bare TRY_TO_DATE(). Snowflake reads a
        small number as epoch SECONDS (a fiscal year '2012' collapsed 20M rows
        onto 1970-01-01) and reads a 2-digit year literally (EPA ships
        '02-JUN-16' and 8.1M facility dates landed in the year 16).
      * Publishers encode "not applicable" AS A DATE. 1900-01-01 appears on 30.9M
        rows -- e.g. 5.26M criminal defendants have a "date they stopped being a
        fugitive" of 1900-01-01 because they were never fugitives. 9999-12-31
        means "no end date." These are blanks wearing a date costume.

    THE RULES (see also: the same rules are enforced by
    tests/assert_ripple_time_standard.sql, which fails the build on a violation)

      1. One canonical column per table, always TIMESTAMP_NTZ.
      2. Coarse grains snap to the START of their period: a month becomes the 1st
         at 00:00, a quarter the first day of the quarter, a year Jan 1.
      3. The grain travels WITH the value. Without it, an annual figure snapped
         to Jan 1 is indistinguishable from a real January 1st event, and every
         yearly series grows a fake New Year's Day spike.
      4. The clock kind travels with it too: did it HAPPEN then, was it REPORTED
         then, or did an authority DECIDE then. Same axis, different meanings.
      5. Times are naive/UTC. A calendar date is a calendar date, not midnight in
         somebody's timezone.
      6. Unknown is NULL. Never a sentinel. Ever.
      7. A value outside the trusted window becomes NULL and is COUNTED. The count
         is a quality measure that gets kept, not a deletion that gets hidden.
      8. The raw column is never overwritten. Canonical sits BESIDE it, so a
         mis-parse (day-first vs month-first is unknowable from values alone) is
         always recoverable.

    Conventions match macros/clean.sql: every macro returns a SQL *expression*
    with no trailing comma, so it drops straight into a SELECT list.
#}


{#- The trusted window. Floor is well before any public record Ripple holds.
    Ceiling is generous because span-END columns are legitimately in the future:
    a Section 8 contract expiring in 2045 is correct data, not corruption. Event
    clocks get a tighter ceiling via ripple_event_ts(). -#}
{% macro ripple_time_floor() -%}1700{%- endmacro %}
{% macro ripple_time_ceiling() -%}2125{%- endmacro %}


{#- ============================ THE PARSER ============================
    Shape-guarded parsing. Every format is applied ONLY to values that already
    proved they match it, so nothing can fall through to an epoch reading.

    fmt:
      'auto'        try every known shape, widest net (default)
      'iso'         2026-03-15 / 2026-03-15T09:00:00
      'us'          3/15/2026
      'us2'         3/15/26        <- 2-digit year, century-pivoted
      'dmon'        15-MAR-2026
      'dmon2'       15-MAR-26      <- 2-digit year, century-pivoted
      'yyyymmdd'    20260315

    pivot: for 2-digit years, the last year that reads as 20xx. '26' with
    pivot=2069 is 2026; '85' is 1985. Pick it per source: facility create dates
    never predate the 1990s, but a birth date obviously can.

    blanks: source values meaning "not applicable" -- nulled before parsing.
-#}
{% macro ripple_parse_date(col, fmt='auto', pivot=2069, blanks=[]) -%}
{%- set v -%}nullif(trim(to_varchar({{ col }})), ''){%- endset -%}
{%- set base -%}
    {%- if blanks -%}
        nullif(nullif({{ v }},
            {%- for b in blanks %}'{{ b }}'{% if not loop.last %}), nullif({{ v }}, {% endif %}{% endfor -%}
        ), '')
    {%- else -%}{{ v }}{%- endif -%}
{%- endset -%}
{%- set iso    = "regexp_like(" ~ base ~ ", '^[0-9]{4}-[0-9]{2}-[0-9]{2}.*')" -%}
{%- set us     = "regexp_like(" ~ base ~ ", '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$')" -%}
{%- set us2    = "regexp_like(" ~ base ~ ", '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}$')" -%}
{%- set dmon   = "regexp_like(" ~ base ~ ", '^[0-9]{1,2}-[A-Za-z]{3}-[0-9]{4}$')" -%}
{%- set dmon2  = "regexp_like(" ~ base ~ ", '^[0-9]{1,2}-[A-Za-z]{3}-[0-9]{2}$')" -%}
{%- set ymd    = "regexp_like(" ~ base ~ ", '^[0-9]{8}$')" -%}
{#- 2-digit years: pivot arithmetically rather than trusting a session parameter
    that a later session could change underneath the data. -#}
{%- set p2 = pivot % 100 -%}
{%- set c_hi = (pivot // 100) * 100 -%}
{%- set c_lo = c_hi - 100 -%}
{%- set yy = "try_to_number(right(" ~ base ~ ", 2))" -%}
{%- set yy_full = "(iff(" ~ yy ~ " <= " ~ p2 ~ ", " ~ c_hi ~ ", " ~ c_lo ~ ") + " ~ yy ~ ")" -%}
coalesce(
    {%- if fmt in ('auto','iso') %}
    iff({{ iso }}, try_to_date(left({{ base }}, 10), 'YYYY-MM-DD'), null),
    {%- endif %}
    {%- if fmt in ('auto','us') %}
    iff({{ us }}, try_to_date({{ base }}, 'MM/DD/YYYY'), null),
    {%- endif %}
    {%- if fmt in ('auto','us2') %}
    iff({{ us2 }}, try_to_date(
        left({{ base }}, length({{ base }}) - 2) ||
        to_varchar({{ yy_full }}), 'MM/DD/YYYY'), null),
    {%- endif %}
    {%- if fmt in ('auto','dmon') %}
    iff({{ dmon }}, try_to_date(upper({{ base }}), 'DD-MON-YYYY'), null),
    {%- endif %}
    {%- if fmt in ('auto','dmon2') %}
    iff({{ dmon2 }}, try_to_date(
        upper(left({{ base }}, length({{ base }}) - 2)) ||
        to_varchar({{ yy_full }}), 'DD-MON-YYYY'), null),
    {%- endif %}
    {%- if fmt in ('auto','yyyymmdd') %}
    iff({{ ymd }} and left({{ base }}, 4)
            between '{{ ripple_time_floor() }}' and '{{ ripple_time_ceiling() }}',
        try_to_date({{ base }}, 'YYYYMMDD'), null),
    {%- endif %}
    null)
{%- endmacro %}


{#- Clamp to the trusted window. Rule 7: out-of-window becomes NULL, and the
    matching test counts what was dropped. -#}
{% macro ripple_window(expr) -%}
    iff(year({{ expr }}) between {{ ripple_time_floor() }} and {{ ripple_time_ceiling() }},
        {{ expr }}, null)
{%- endmacro %}


{#- ======================== THE CANONICAL COLUMNS ========================
    Each returns TIMESTAMP_NTZ snapped to the start of its period (rule 2).
-#}

{#- Day-grain source: a real date. -#}
{% macro ripple_ts_from_date(col, fmt='auto', pivot=2069, blanks=[]) -%}
    {{ ripple_window(ripple_parse_date(col, fmt, pivot, blanks)) }}::timestamp_ntz
{%- endmacro %}

{#- Year-grain source: '2024' or 2024. NEVER goes near a date parser -- that is
    the exact bug that collapsed 20M contract rows onto 1970-01-01. -#}
{% macro ripple_ts_from_year(col) -%}
{%- set v -%}nullif(trim(to_varchar({{ col }})), ''){%- endset -%}
    iff(regexp_like({{ v }}, '^[0-9]{4}$')
        and try_to_number({{ v }})
            between {{ ripple_time_floor() }} and {{ ripple_time_ceiling() }},
        date_from_parts(try_to_number({{ v }}), 1, 1), null)::timestamp_ntz
{%- endmacro %}

{#- Month-grain source: '202403' or '2024-03'. -#}
{% macro ripple_ts_from_yyyymm(col) -%}
{%- set v -%}replace(nullif(trim(to_varchar({{ col }})), ''), '-', ''){%- endset -%}
    iff(regexp_like({{ v }}, '^[0-9]{6}$')
        and try_to_number(left({{ v }}, 4))
            between {{ ripple_time_floor() }} and {{ ripple_time_ceiling() }}
        and try_to_number(right({{ v }}, 2)) between 1 and 12,
        date_from_parts(try_to_number(left({{ v }}, 4)),
                        try_to_number(right({{ v }}, 2)), 1), null)::timestamp_ntz
{%- endmacro %}

{#- Quarter-grain source: '2004q1', '2004Q1', '2004-1', '20041'. Snaps to the
    first day of the quarter. 20.6M adverse-event rows arrive in this shape and
    the previous census scored them as having no clock at all. -#}
{% macro ripple_ts_from_yearquarter(col) -%}
{%- set v -%}upper(replace(replace(nullif(trim(to_varchar({{ col }})), ''), '-', ''), ' ', '')){%- endset -%}
{%- set y -%}try_to_number(left({{ v }}, 4)){%- endset -%}
{%- set q -%}try_to_number(right({{ v }}, 1)){%- endset -%}
    iff(regexp_like({{ v }}, '^[0-9]{4}Q?[1-4]$')
        and {{ y }} between {{ ripple_time_floor() }} and {{ ripple_time_ceiling() }},
        date_from_parts({{ y }}, ({{ q }} - 1) * 3 + 1, 1), null)::timestamp_ntz
{%- endmacro %}


{#- An EVENT clock cannot be in the future (rule 7 applied to "happened"
    clocks). Span-end and expiry columns must NOT use this -- their future dates
    are correct. Anything ahead of today plus a year's slack is nulled. -#}
{% macro ripple_event_ts(expr) -%}
    iff({{ expr }} <= dateadd(year, 1, current_timestamp()::timestamp_ntz), {{ expr }}, null)
{%- endmacro %}


{#- The grain and clock tags that must ride alongside every canonical column
    (rules 3 and 4). Emitted as literals so they survive into the mart and can
    be asserted by the standard's test. -#}
{% macro ripple_grain(grain) -%}
    {%- if grain not in ('day','month','quarter','year') -%}
        {{ exceptions.raise_compiler_error("ripple_grain: '" ~ grain ~ "' is not day/month/quarter/year") }}
    {%- endif -%}
    '{{ grain }}'::varchar
{%- endmacro %}

{% macro ripple_clock(kind) -%}
    {%- if kind not in ('happened','reported','decided','span_start','span_end') -%}
        {{ exceptions.raise_compiler_error("ripple_clock: '" ~ kind ~ "' is not happened/reported/decided/span_start/span_end") }}
    {%- endif -%}
    '{{ kind }}'::varchar
{%- endmacro %}


{#- ==================== INGEST-STAMP RECOVERY ====================
    Two shapes of the same bug, both found by the 2026-08-20 time-index scan.

    (a) The landing column is a NUMBER of MICROSECONDS and a bare to_timestamp
        read it as seconds. Fix at the cast: to_timestamp_ntz(col, 6).

    (b) The landing column is ALREADY a corrupted TIMESTAMP -- the loader did the
        bad cast before writing, so the damage is baked into raw and dbt cannot
        prevent it. It is still exactly recoverable: the stored timestamp's epoch
        SECONDS equal the original MICROSECONDS, so dividing by a million
        restores it. Verified live: the consumer-injury file's stamp of
        56569708-12-11 recovers to 2026-07-26, and the research-grant file's
        56608739-01-16 to 2026-08-10 -- both matching their real load dates.

    This macro handles (b). Anything already sane passes through untouched, so it
    is safe to leave in place after the loader itself is fixed.
-#}
{% macro ripple_recover_ingest_ts(col) -%}
    iff(year({{ col }}) > {{ ripple_time_ceiling() }},
        to_timestamp_ntz(date_part(epoch_second, {{ col }}) / 1000000),
        {{ col }})
{%- endmacro %}
