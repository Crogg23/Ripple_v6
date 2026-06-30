{#
    generate_schema_name.sql -- additive schema routing for domain-isolated models.

    WHY THIS IS SAFE FOR EXISTING MODELS:
    dbt's DEFAULT macro returns `target.schema` when a model sets NO custom schema,
    and `target.schema ~ '_' ~ custom` when it does. NONE of the existing Ripple
    models set a custom schema (`+schema`), so today they ALL resolve to
    `target.schema` (DBT_CROGERS in the dev profile).

    This macro keeps that EXACT behaviour for the no-custom case (returns
    target.schema), and ONLY changes models that explicitly opt in with a
    `+schema` / `config(schema=...)` -- for those it returns the custom schema
    VERBATIM (e.g. 'POLITICS' -> LIBRARY_MARTS.POLITICS) instead of the default
    concatenation (DBT_CROGERS_POLITICS).

    Net effect: every existing model resolves to the same schema as before; the
    politics-domain models (the only ones that set +schema) land in a clean,
    isolated POLITICS schema that matches the Python-built canonical tables.
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
