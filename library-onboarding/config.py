"""Central configuration for the Source Onboarding Agent.

Every credential and tunable lives here and is read from the environment
(optionally via a local ``.env`` file loaded with python-dotenv). Nothing in
this repository ever hard-codes a secret -- see ``.env.example`` for the full
list of variables the agent understands.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:  # python-dotenv is convenient but not strictly required
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - dotenv missing is fine
    pass


class ConfigError(RuntimeError):
    """Raised when a required piece of configuration is missing."""


def _flag(name: str, default: str = "") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


@dataclass
class Config:
    """Resolved configuration, read once from the environment."""

    # --- Anthropic -------------------------------------------------------
    anthropic_api_key: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", "")
    )
    # Defaults to a current, capable model. Override with ANTHROPIC_MODEL to
    # trade cost for capability (a larger model gives better recon/codegen).
    anthropic_model: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    )

    # --- Snowflake -------------------------------------------------------
    snowflake_account: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_ACCOUNT", "ONEAFDA-UMB20733")
    )
    snowflake_user: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_USER", "CROGG23")
    )
    snowflake_password: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_PASSWORD", "")
    )
    snowflake_database: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_DATABASE", "DISASTER_IMPACT")
    )
    # The flat "raw" schema used when SNOWFLAKE_RAW_LAYOUT=single_schema.
    snowflake_schema: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_SCHEMA", "RAW")
    )
    snowflake_warehouse: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_WAREHOUSE", "")
    )
    snowflake_role: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_ROLE", "")
    )
    # How raw tables are laid out. The build plan writes to "RAW.<SOURCE>.<TABLE>";
    # interpreting the middle token as a Snowflake schema gives a clean
    # schema-per-source layout under the configured database. The alternative
    # keeps everything in one schema with a source-prefixed table name.
    #   schema_per_source -> <DATABASE>.<SOURCE>.<TABLE>            (default)
    #   single_schema     -> <DATABASE>.<SCHEMA>.<SOURCE>_<TABLE>
    snowflake_raw_layout: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_RAW_LAYOUT", "schema_per_source")
    )

    # --- OpenMetadata ----------------------------------------------------
    openmetadata_host: str = field(
        default_factory=lambda: os.getenv("OPENMETADATA_HOST", "http://localhost:8585")
    )
    openmetadata_token: str = field(
        default_factory=lambda: os.getenv("OPENMETADATA_TOKEN", "")
    )

    # --- dbt -------------------------------------------------------------
    dbt_project_path: str = field(
        default_factory=lambda: os.getenv("DBT_PROJECT_PATH", "")
    )

    # --- Agent behaviour -------------------------------------------------
    # ONBOARD_FAKE_LLM=1 short-circuits every Claude call with deterministic
    # fixtures so the checkpoint flow can be exercised offline (no API key, no
    # outbound network). Intended for testing/demos only.
    fake_llm: bool = field(default_factory=lambda: _flag("ONBOARD_FAKE_LLM"))
    # ONBOARD_AUTO_APPROVE=1 answers every checkpoint with "go" without reading
    # stdin -- handy for non-interactive smoke tests. Never use for real loads.
    auto_approve: bool = field(default_factory=lambda: _flag("ONBOARD_AUTO_APPROVE"))

    # ------------------------------------------------------------------
    def require(self, *keys: str) -> None:
        """Raise ConfigError if any of the named attributes are empty."""
        missing = [k for k in keys if not str(getattr(self, k, "")).strip()]
        if missing:
            env_names = ", ".join(_ATTR_TO_ENV.get(k, k.upper()) for k in missing)
            raise ConfigError(
                "Missing required configuration: "
                f"{env_names}. Set these in your environment or .env file "
                "(see .env.example)."
            )

    def dbt_dir(self) -> Path:
        """Return the configured dbt project directory, validated to exist."""
        if not self.dbt_project_path.strip():
            raise ConfigError(
                "DBT_PROJECT_PATH is not set. Point it at the directory that "
                "contains your dbt_project.yml."
            )
        path = Path(self.dbt_project_path).expanduser()
        if not (path / "dbt_project.yml").exists():
            raise ConfigError(
                f"No dbt_project.yml found in {path}. Set DBT_PROJECT_PATH to a "
                "valid dbt project root."
            )
        return path


# Map attribute names back to the env var the user actually sets, for messages.
_ATTR_TO_ENV = {
    "anthropic_api_key": "ANTHROPIC_API_KEY",
    "anthropic_model": "ANTHROPIC_MODEL",
    "snowflake_account": "SNOWFLAKE_ACCOUNT",
    "snowflake_user": "SNOWFLAKE_USER",
    "snowflake_password": "SNOWFLAKE_PASSWORD",
    "snowflake_database": "SNOWFLAKE_DATABASE",
    "snowflake_schema": "SNOWFLAKE_SCHEMA",
    "snowflake_warehouse": "SNOWFLAKE_WAREHOUSE",
    "openmetadata_host": "OPENMETADATA_HOST",
    "openmetadata_token": "OPENMETADATA_TOKEN",
    "dbt_project_path": "DBT_PROJECT_PATH",
}


# A single shared instance is convenient; tests can build their own Config().
settings = Config()
