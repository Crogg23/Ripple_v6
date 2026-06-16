"""Checkpoint 4 -- DBT.

Claude turns the raw schema into a staging model (rename/cast/dedupe), a mart
model (analytics-ready), and a schema.yml (descriptions + tests). Files are
written directly into the configured dbt project.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from config import ConfigError, settings
from llm import call_claude, extract_json, render_prompt


def generate_dbt_models(config: dict, feedback: Optional[str] = None) -> dict:
    schema_repr = "\n".join(
        f"  - {f.get('name')} ({f.get('type')}): {f.get('description','')}"
        for f in config.get("schema_fields", [])
    ) or "  (schema unknown)"

    prompt = render_prompt(
        "generate_dbt",
        name=config["name"],
        raw_table=config["raw_table"],
        source_schema=config["raw_schema"],
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
            "mart_sql, schema_yml. SQL must be valid dbt (Jinja + Snowflake)."
        ),
        kind="dbt",
        fake_context=config,
        max_tokens=4096,
    )
    models = extract_json(raw)
    for key in ("staging_sql", "mart_sql", "schema_yml"):
        models.setdefault(key, "")
    return models


def write_dbt_models(config: dict, models: dict) -> dict:
    """Write the generated models into the dbt project. Returns paths written."""
    if not settings.dbt_project_path.strip():
        if settings.fake_llm:
            return {**models, "written": [], "note": "dry run -- DBT_PROJECT_PATH not set"}
        raise ConfigError(
            "DBT_PROJECT_PATH is not set. Point it at your dbt project root "
            "(the directory containing dbt_project.yml)."
        )

    project = settings.dbt_dir()
    models_dir = project / "models"

    src_slug = config["staging_model"].split("__")[0].replace("stg_", "", 1)
    domain = config["mart_model"].split("__")[0]

    staging_dir = models_dir / "staging" / src_slug
    mart_dir = models_dir / "marts" / domain
    staging_dir.mkdir(parents=True, exist_ok=True)
    mart_dir.mkdir(parents=True, exist_ok=True)

    written = []
    targets = [
        (staging_dir / f"{config['staging_model']}.sql", models.get("staging_sql", "")),
        (mart_dir / f"{config['mart_model']}.sql", models.get("mart_sql", "")),
        (staging_dir / "schema.yml", models.get("schema_yml", "")),
    ]
    for path, body in targets:
        if not body.strip():
            continue
        path.write_text(body.rstrip() + "\n", encoding="utf-8")
        written.append(str(path))

    return {**models, "written": written}


def run_dbt_scaffold(config: dict, models: Optional[dict] = None, feedback: Optional[str] = None) -> dict:
    models = models or generate_dbt_models(config, feedback=feedback)
    return write_dbt_models(config, models)
