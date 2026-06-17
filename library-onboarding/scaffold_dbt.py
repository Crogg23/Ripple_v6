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
    if actual:
        schema_repr = "\n".join(f"  - {c} (TEXT): raw landing column" for c in actual)
    else:
        schema_repr = "\n".join(
            f"  - {f.get('name')} ({f.get('type')}): {f.get('description','')}"
            for f in config.get("schema_fields", [])
        ) or "  (schema unknown)"

    prompt = render_prompt(
        "generate_dbt",
        name=config["name"],
        source_id=config["source_id"],
        landing_table=config["landing_table"],
        raw_database=settings.raw_database,
        entity=config["entity"],
        staging_model=config["staging_model"],
        mart_model=config["mart_model"],
        identifiers=", ".join(config.get("key_identifiers", [])) or "(none)",
        schema=schema_repr,
        feedback=feedback or "(none)",
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
        # 4096 truncated at ~25 cols (biorxiv), and HCRIS has 117 cols. Cap high --
        # it's a ceiling, not a target, so narrow sources still return small.
        max_tokens=16384,
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
