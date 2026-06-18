"""Checkpoint 4 -- DBT.

Claude turns the landing table into the standard layer stack:

    staging      stg_<source_id>__<entity>   (view; rename/cast/dedupe)
    intermediate int_<source_id>_<...>        (optional; joins/derived)
    mart         <domain>__<source_id>        (table; analytics-ready)

plus a schema.yml with descriptions and the standard test battery. Files are
written into the configured dbt project. Models read from
``source('ripple_raw', '<LANDING_TABLE>')`` and materialize into
LIBRARY_STAGING / LIBRARY_MARTS via your dbt profile.
"""

from __future__ import annotations

from typing import Optional

from config import ConfigError, settings
from llm import call_claude, extract_json, render_prompt


def _actual_landing_columns(landing_table: str) -> list:
    """The real, current columns of the landing table (minus the _meta columns).

    dbt models must be generated against what *actually landed*, not recon's schema
    guess -- a CSV/bulk source often lands different columns than predicted (the
    fed_cms_hcris failure: recon guessed PROVIDER_NUMBER; the data had PROVIDER_CCN,
    so the staging view wouldn't compile). Best-effort: [] if Snowflake is unreachable.
    """
    if not landing_table.strip() or settings.fake_llm or not settings.snowflake_ready():
        return []
    try:
        import snow

        conn = snow.connect()
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT COLUMN_NAME FROM {settings.raw_database}.INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION",
                (settings.raw_schema, landing_table),
            )
            cols = [r[0] for r in cur.fetchall()]
        finally:
            conn.close()
        return [c for c in cols if not str(c).startswith("_")]
    except Exception:
        return []


def generate_dbt_models(config: dict, feedback: Optional[str] = None) -> dict:
    # Prefer the real landed columns over recon's guess (see _actual_landing_columns).
    actual = _actual_landing_columns(config.get("landing_table", ""))
    ncols = len(actual)
    # WIDE TABLE guard: a 300+-column source (e.g. NPPES) makes enumerating every
    # column blow the JSON payload past max_tokens -> truncated -> "Unterminated
    # string". For wide tables, show only the key-identifier columns + a count, and
    # direct the model to emit a compact passthrough instead of 300 explicit casts.
    wide = ncols > 60
    keys = config.get("key_identifiers", []) or []
    if actual and wide:
        key_up = {k.upper() for k in keys}
        shown = [c for c in actual if c.upper() in key_up][:12] or actual[:10]
        schema_repr = "\n".join(f"  - {c} (TEXT): raw landing column" for c in shown)
        schema_repr += f"\n  ... (+{ncols - len(shown)} more TEXT columns -- WIDE TABLE, {ncols} total)"
    elif actual:
        schema_repr = "\n".join(f"  - {c} (TEXT): raw landing column" for c in actual)
    else:
        schema_repr = "\n".join(
            f"  - {f.get('name')} ({f.get('type')}): {f.get('description','')}"
            for f in config.get("schema_fields", [])
        ) or "  (schema unknown)"

    # Compact-output directive for wide tables, prepended to the feedback channel so
    # we don't touch the prompt template. Keeps staging/mart as passthroughs and the
    # schema.yml tests scoped to the keys -> small, untruncated JSON.
    eff_feedback = feedback or ""
    if wide:
        directive = (
            f"WIDE TABLE ({ncols} columns) -- keep the JSON output COMPACT, do NOT "
            "enumerate every column. staging_sql: a lightweight passthrough -- "
            "`select *` from the source, dedupe on the primary key with "
            "qualify row_number() over (partition by <pk> order by _ingested_at desc)=1, "
            "no per-column casts. mart_sql: `select * from {{ ref(staging) }}`. "
            "schema.yml: document the model + add not_null/unique tests ONLY on the key "
            "identifier column(s), not all columns."
        )
        eff_feedback = (directive + ("\n\n" + feedback if feedback else "")).strip()

    prompt = render_prompt(
        "generate_dbt",
        name=config["name"],
        source_id=config["source_id"],
        landing_table=config["landing_table"],
        raw_database=settings.raw_database,
        entity=config["entity"],
        staging_model=config["staging_model"],
        mart_model=config["mart_model"],
        identifiers=", ".join(keys) or "(none)",
        schema=schema_repr,
        feedback=eff_feedback or "(none)",
    )
    raw = call_claude(
        user=prompt,
        system=(
            "You are a dbt expert. Output strict JSON with keys staging_sql, "
            "intermediate_sql (may be empty), mart_sql, schema_yml. SQL must be "
            "valid dbt (Jinja + Snowflake) and reference the landing source."
        ),
        kind="dbt",
        fake_context=config,
        # Wide tables make staging_sql + mart_sql + schema_yml a long JSON payload;
        # 4096 truncated at ~25 cols (biorxiv), 117-col HCRIS needed more. Cap high --
        # it's a ceiling, not a target, so narrow sources still return small. The wide
        # directive above keeps even 300-col tables compact.
        max_tokens=24576,
    )
    models = extract_json(raw)
    for key in ("staging_sql", "intermediate_sql", "mart_sql", "schema_yml"):
        models.setdefault(key, "")
    return models


def write_dbt_models(config: dict, models: dict) -> dict:
    if not settings.dbt_project_path.strip():
        if settings.fake_llm:
            return {**models, "written": [], "note": "dry run -- DBT_PROJECT_PATH not set"}
        raise ConfigError(
            "DBT_PROJECT_PATH is not set. Point it at your dbt project root "
            "(the directory containing dbt_project.yml)."
        )

    project = settings.dbt_dir()
    models_dir = project / "models"
    src = config["source_id"]
    domain = config["mart_model"].split("__")[0]

    staging_dir = models_dir / "staging" / src
    int_dir = models_dir / "intermediate" / src
    mart_dir = models_dir / "marts" / domain
    for d in (staging_dir, mart_dir):
        d.mkdir(parents=True, exist_ok=True)

    written = []
    targets = [
        (staging_dir / f"{config['staging_model']}.sql", models.get("staging_sql", "")),
        (staging_dir / "schema.yml", models.get("schema_yml", "")),
        (mart_dir / f"{config['mart_model']}.sql", models.get("mart_sql", "")),
    ]
    if models.get("intermediate_sql", "").strip():
        int_dir.mkdir(parents=True, exist_ok=True)
        targets.append((int_dir / f"int_{src}_{config['entity']}.sql", models["intermediate_sql"]))

    for path, body in targets:
        if not body.strip():
            continue
        path.write_text(body.rstrip() + "\n", encoding="utf-8")
        written.append(str(path))

    return {**models, "written": written}


def run_dbt_scaffold(config: dict, models: Optional[dict] = None, feedback: Optional[str] = None) -> dict:
    models = models or generate_dbt_models(config, feedback=feedback)
    return write_dbt_models(config, models)
