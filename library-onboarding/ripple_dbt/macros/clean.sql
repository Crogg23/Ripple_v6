{#
    clean.sql -- reusable cleaning macros for Ripple staging models.

    The landing layer stores every column as TEXT, so the recurring traps the
    2026-06-27 discovery sweep surfaced (epoch-overflow dates, placeholder NPIs,
    numeric sentinels, OFAC's '-0-' null token, IMO prefixes) all show up as
    string-shaped landmines. These macros are the DRY home for fixing them once.

    Conventions:
      * Each macro returns a SQL *expression* (no trailing comma) so it drops
        straight into a SELECT list: `{{ clean_npi('NPI') }} as npi,`
      * Inputs are the raw TEXT landing column name (unquoted, UPPER as landed).
      * `try_*` variants never raise -- bad input becomes NULL, not an error.
#}


{#- LEIE EXCLDATE etc.: 'YYYYMMDD' text. TRY_CAST(... AS DATE) reads it as an
    epoch-day integer and collapses everything to garbage 1970 dates (#1). -#}
{% macro parse_yyyymmdd(col) -%}
    try_to_date(nullif(trim({{ col }}), ''), 'YYYYMMDD')
{%- endmacro %}


{#- LEIE NPI is the literal placeholder '0000000000' on ~90% of rows; a naive
    [0-9]{10} regex passes it and falsely FACT-grades name-only matches (#1/#15).
    Null both the placeholder and blanks so a real NPI means a real NPI. -#}
{% macro clean_npi(col) -%}
    nullif(nullif(trim({{ col }}), ''), '0000000000')
{%- endmacro %}


{#- Generic numeric/text sentinel scrubber. Pass one value or a list; trimmed
    text matches are nulled. Used for -999 (#12), 'nan' (#41/#78), 511 heading
    (#66, but prefer clean_heading), '-0- ' OFAC (#9, after trim). -#}
{% macro null_sentinel(col, sentinels, do_trim=true) -%}
    {%- set vals = sentinels if (sentinels is sequence and sentinels is not string) else [sentinels] -%}
    {%- set base = ("trim(" ~ col ~ ")") if do_trim else (col | string) -%}
    case
        when {{ base }} in (
            {%- for v in vals -%}'{{ v }}'{%- if not loop.last -%}, {% endif -%}{%- endfor -%}
        ) then null
        else {{ base }}
    end
{%- endmacro %}


{#- OFAC stores '-0- ' (trailing space!) as its null token across SDN_TYPE,
    TITLE, REMARKS, VESS_TYPE... TRIM first, then map '-0-' -> NULL (#9). -#}
{% macro clean_ofac_token(col) -%}
    nullif(nullif(trim({{ col }}), ''), '-0-')
{%- endmacro %}


{#- IMO normalization (#3/#66). AIS stores 'IMO8851273' (+2.24M junk pings),
    OFAC/OpenSanctions store bare 7-digit. Strip an 'IMO' prefix and keep only
    a valid 7-digit number; everything else (placeholders, blanks) -> NULL.
    2026-07-28 fix: the 7-digit regex alone let the all-zero placeholder
    'IMO0000000' -> '0000000' through as "valid" -- confirmed live on
    FED_NOAA_AIS, 13,868,433 of 58,106,517 rows (23.9%) were silently getting
    this fake-but-well-formed hull number instead of NULL, exactly the AIS
    junk-ping pattern this macro's own docstring already said to null. -#}
{% macro normalize_imo(col) -%}
    case
        when regexp_like(regexp_replace(trim({{ col }}), '^IMO', ''), '^[0-9]{7}$')
             and regexp_replace(trim({{ col }}), '^IMO', '') != '0000000'
        then regexp_replace(trim({{ col }}), '^IMO', '')
    end
{%- endmacro %}


{#- AIS HEADING uses 511 (and anything >= 360) as 'not available' on 52% of
    rows; a naive AVG returns 356.9 instead of 186.8 (#66). -#}
{% macro clean_heading(col) -%}
    case when try_to_double(trim({{ col }})) < 360 then try_to_double(trim({{ col }})) end
{%- endmacro %}


{#- MSHA pipe-delimited CSVs retain literal quote characters inside text values
    (e.g. |"Y"| lands as the 3-char string "Y" instead of bare Y). Pandas
    read_csv with sep='|' doesn't always strip these. This macro strips embedded
    double-quotes and trims whitespace, nulling empty strings. -#}
{% macro strip_quotes(col) -%}
    nullif(trim(replace({{ col }}, '"', '')), '')
{%- endmacro %}
