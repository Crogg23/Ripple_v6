{#
    guard_politics_mirror.sql -- turns the STANDING POLICY no_selectorless_dbt_build
    (build-state.md, 2026-06-30) from a code comment into something dbt itself
    enforces.

    POLITICS__* marts are canonical: built and reconciled to the penny against
    OpenFEC/GovTrack by hand-written Python (politics/loaders/*.py), NOT by dbt.
    A handful of dbt models in models/marts/politics/ exist ONLY so `dbt test`
    can run data tests against those already-correct tables. Nothing else in
    the project depends on these models -- their SQL is dbt's own (separately
    maintained, never reconciled against an outside source) reconstruction of
    the same tables.

    Before this guard: nothing but a code comment stopped `dbt build` (with no
    --select, or any selection that happens to sweep these models in) from
    running these models' CREATE OR REPLACE TABLE and silently overwriting the
    audited numbers with dbt's own untested version. No error, no warning --
    the table would just start holding different numbers than the ones the
    smoke tests (politics/loaders/smoke_*.py) proved correct. Flagged in
    build-state.md's defect ledger as "never verified" until 2026-07-30.

    This macro is wired in as a +pre-hook on the whole models.ripple.marts.politics
    folder (dbt_project.yml). Pre-hooks run at MODEL-EXECUTION time (dbt run /
    dbt build), so `dbt test` -- which only queries the already-materialized
    table, never re-runs the model -- is completely unaffected: the one real
    job these models exist to do (let tests run against Python-built tables)
    still works with zero friction, every time.

    To deliberately rebuild one of these models (a real, considered decision,
    not an accident): `dbt build --select <model> --vars '{"allow_politics_rebuild": true}'`.
#}
{% macro guard_politics_mirror() %}
{%- if not var('allow_politics_rebuild', false) -%}
{{ exceptions.raise_compiler_error(
    "BLOCKED: " ~ this.identifier ~ " is a dbt MIRROR of a Python-built canonical "
    "POLITICS table (STANDING POLICY no_selectorless_dbt_build, build-state.md). "
    "Running dbt build/run against it would silently overwrite audited, "
    "OpenFEC/GovTrack-reconciled numbers with dbt's own untested SQL -- no error, "
    "no warning, just different numbers. `dbt test` is unaffected by this guard "
    "and still runs normally. To deliberately rebuild this one model on purpose, "
    "pass --vars '{\"allow_politics_rebuild\": true}' and be sure that's really "
    "what you mean to do."
) }}
{%- endif -%}
{% endmacro %}
