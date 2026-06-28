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
    a valid 7-digit number; everything else (placeholders, blanks) -> NULL. -#}
{% macro normalize_imo(col) -%}
    case
        when regexp_like(regexp_replace(trim({{ col }}), '^IMO', ''), '^[0-9]{7}$')
        then regexp_replace(trim({{ col }}), '^IMO', '')
    end
{%- endmacro %}


{#- AIS HEADING uses 511 (and anything >= 360) as 'not available' on 52% of
    rows; a naive AVG returns 356.9 instead of 186.8 (#66). -#}
{% macro clean_heading(col) -%}
    case when try_to_double(trim({{ col }})) < 360 then try_to_double(trim({{ col }})) end
{%- endmacro %}
