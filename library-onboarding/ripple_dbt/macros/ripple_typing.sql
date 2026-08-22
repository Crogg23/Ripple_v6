{#
    ripple_typing.sql -- the canonical number/date casts for the typing layer
    (2026-08-22, Chris-approved clock-style rollout; see the clock precedent in
    ripple_time.sql). Applied by scripts/typing/apply_rulings.py, driven by
    reports/typing_index/typing_rulings.csv -- never applied on column name
    alone; every ruled column was value-checked against live data first.

    ripple_num(expr): guarded numeric cast. Empty string -> NULL, anything
    unparseable -> NULL (verified <=1% of non-empty values per ruling).

    ripple_dt(expr): guarded date cast, three lanes because digit-only strings
    are treacherous BOTH ways on this platform (the epoch trap, hit live on
    2026-08-18: a bare auto-parse reads small integers as epoch SECONDS and
    collapses them onto 1970 -- inside any naive range guard):
      1. exactly 8 digits  -> explicit YYYYMMDD parse
      2. any other pure-digit value -> NULL (a number is not a date we guess at)
      3. everything else -> timestamp_tz first (ISO with offsets), date second
    Then the 1800-2100 range guard: year-typos (5, 1008, 3008) and open-ended
    sentinels (9999-12-31) null out instead of poisoning min/max.
#}

{% macro ripple_num(expr) %}
try_to_double(nullif(trim({{ expr }}), ''))
{%- endmacro %}

{% macro ripple_dt(expr) %}
{%- set v = "nullif(trim(" ~ expr ~ "), '')" -%}
case
  when {{ v }} rlike '^[0-9]{8}$'
    then iff(try_to_date({{ v }}, 'YYYYMMDD') between '1800-01-01' and '2100-01-01',
             try_to_date({{ v }}, 'YYYYMMDD'), null)
  when {{ v }} rlike '^[0-9]+$'
    then null
  else iff(coalesce(to_date(try_to_timestamp_tz({{ v }})), try_to_date({{ v }}))
             between '1800-01-01' and '2100-01-01',
           coalesce(to_date(try_to_timestamp_tz({{ v }})), try_to_date({{ v }})), null)
end
{%- endmacro %}
