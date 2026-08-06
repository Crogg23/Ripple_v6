{#
    test_key_is_real -- the platform's signature-bug catcher (audit 2026-08-05
    critical #4: 0 of 3,801 tests could detect a masked-blank sentinel column).

    A join-key column that "passes not_null" can still be 100% garbage: empty
    strings, a repeated placeholder ('0000000000' NPI, all-zero IMO), or one
    sentinel value stamped on every row (NPPES EIN, NOAA_AIS imo_number).
    This test fails when a column's REAL population -- after trimming blanks
    and declared sentinels -- falls below a distinct-count floor or above a
    blank fraction ceiling.

    Usage in schema.yml:
      - name: ein
        data_tests:
          - key_is_real:
              min_distinct: 1000          # a real EIN column has thousands
              max_blank_fraction: 0.5     # >50% blank/sentinel = not a key
              sentinels: ['000000000']    # column-specific placeholders
#}
{% test key_is_real(model, column_name, min_distinct=100, max_blank_fraction=0.5, sentinels=[]) %}

with cleaned as (

    select
        nullif(trim(cast({{ column_name }} as varchar)), '') as v
    from {{ model }}

),

scrubbed as (

    select
        case
            when v is null then null
            {%- if sentinels | length > 0 %}
            when v in (
                {%- for s in sentinels -%}'{{ s }}'{%- if not loop.last -%}, {% endif -%}{%- endfor -%}
            ) then null
            {%- endif %}
            else v
        end as v
    from cleaned

),

stats as (

    select
        count(*)                                          as n_rows,
        count(distinct v)                                 as n_distinct,
        sum(case when v is null then 1 else 0 end)        as n_blank
    from scrubbed

)

select
    n_rows,
    n_distinct,
    n_blank,
    round(n_blank / nullif(n_rows, 0), 4) as blank_fraction
from stats
where n_rows > 0
  and (
        n_distinct < {{ min_distinct }}
     or n_blank / nullif(n_rows, 0) > {{ max_blank_fraction }}
  )

{% endtest %}
