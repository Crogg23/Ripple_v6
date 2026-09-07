{#
  Name normalizers shared by the Provider Relief Fund staging model and the
  nursing-home match. Both sides of a name join must go through the SAME
  function or the join lies, so they live here and nowhere else.

  prf_name_norm: upper, every non-alphanumeric to a space, single-spaced, trimmed.
  prf_name_key:  prf_name_norm with a trailing run of legal suffixes removed.
                 'ROSE MOUNTAIN CARE CENTER, INC.' -> 'ROSE MOUNTAIN CARE CENTER'
                 'WELLBRIDGE OF FENTON LLC'        -> 'WELLBRIDGE OF FENTON'
#}
{% macro prf_name_norm(col) -%}
trim(regexp_replace(regexp_replace(upper({{ col }}), '[^A-Z0-9 ]', ' '), '\\s+', ' '))
{%- endmacro %}

{% macro prf_name_key(col) -%}
trim(regexp_replace({{ prf_name_norm(col) }},
     '(\\s+(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LP|L P|LTD|PC|P C|LLP|OPCO|OPERATIONS|OPERATING|HOLDINGS|THE))+$', ''))
{%- endmacro %}
