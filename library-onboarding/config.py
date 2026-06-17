"""Central configuration for the Ripple Source Onboarding Agent.

Every credential and tunable lives here and is read from the environment
(optionally via a local ``.env`` file). Nothing is hard-coded as a secret -- see
``.env.example`` for the full list.

The agent targets the live Ripple v6 warehouse layout:

    LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>          raw landing tables
    LIBRARY_META.REGISTRY.SOURCE_REGISTRY           the source catalog
    LIBRARY_META.INGEST_LOGS.INGEST_RUNS            one row per ingest run
    LIBRARY_STAGING / LIBRARY_MARTS                  dbt outputs
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


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)).strip() or default)
    except ValueError:
        return default


@dataclass
class Config:
    """Resolved configuration, read once from the environment."""

    # --- Anthropic ------------------------------------------------------
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    )

    # --- Snowflake connection ------------------------------------------
    snowflake_account: str = field(
        default_factory=lambda: os.getenv("SNOWFLAKE_ACCOUNT", "ONEAFDA-UMB20733")
    )
    snowflake_user: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_USER", "CROGG23"))
    snowflake_password: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_PASSWORD", ""))
    # Programmatic Access Token (used in place of a password if set).
    snowflake_pat: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_PAT", ""))
    snowflake_authenticator: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_AUTHENTICATOR", ""))
    snowflake_warehouse: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_WAREHOUSE", ""))
    snowflake_role: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_ROLE", ""))

    # --- Ripple warehouse layout (rarely overridden) -------------------
    raw_database: str = field(default_factory=lambda: os.getenv("RIPPLE_RAW_DATABASE", "LIBRARY_RAW"))
    raw_schema: str = field(default_factory=lambda: os.getenv("RIPPLE_RAW_SCHEMA", "LANDING"))
    meta_database: str = field(default_factory=lambda: os.getenv("RIPPLE_META_DATABASE", "LIBRARY_META"))
    registry_schema: str = field(default_factory=lambda: os.getenv("RIPPLE_REGISTRY_SCHEMA", "REGISTRY"))
    registry_table: str = field(default_factory=lambda: os.getenv("RIPPLE_REGISTRY_TABLE", "SOURCE_REGISTRY"))
    ingest_log_schema: str = field(default_factory=lambda: os.getenv("RIPPLE_INGEST_LOG_SCHEMA", "INGEST_LOGS"))
    ingest_log_table: str = field(default_factory=lambda: os.getenv("RIPPLE_INGEST_LOG_TABLE", "INGEST_RUNS"))
    staging_database: str = field(default_factory=lambda: os.getenv("RIPPLE_STAGING_DATABASE", "LIBRARY_STAGING"))
    marts_database: str = field(default_factory=lambda: os.getenv("RIPPLE_MARTS_DATABASE", "LIBRARY_MARTS"))

    # --- dbt ------------------------------------------------------------
    dbt_project_path: str = field(default_factory=lambda: os.getenv("DBT_PROJECT_PATH", ""))

    # --- Agent behaviour ------------------------------------------------
    # Skip reloading a source whose content hash matches its last successful run.
    skip_if_unchanged: bool = field(
        default_factory=lambda: os.getenv("ONBOARD_SKIP_IF_UNCHANGED", "1").strip().lower()
        in ("1", "true", "yes", "on")
    )
    # ONBOARD_FAKE_LLM=1 short-circuits every Claude call AND Snowflake write with
    # deterministic fixtures so the flow runs offline (no API key / network / db).
    fake_llm: bool = field(default_factory=lambda: _flag("ONBOARD_FAKE_LLM"))
    # ONBOARD_AUTO_APPROVE=1 answers every checkpoint with "go" (smoke tests only).
    auto_approve: bool = field(default_factory=lambda: _flag("ONBOARD_AUTO_APPROVE"))
    # Unattended (auto-approve) self-repair: how many times to feed a stage error
    # back to Claude as feedback and retry before giving up on the source.
    auto_repair: int = field(default_factory=lambda: _int_env("ONBOARD_AUTO_REPAIR", 3))

    # --- Chunked load (C3 -- large files that won't fit in memory) ------
    # Rows per chunk written to Snowflake. The streamed download never holds more
    # than ~one chunk in memory, so peak RSS is bounded regardless of file size.
    chunk_rows: int = field(default_factory=lambda: _int_env("ONBOARD_CHUNK_ROWS", 50_000))
    # Optional safety/demo cap: stop a chunked load after this many rows (0 = no cap,
    # stream the whole file). Lets a proof land a bounded slice fast without changing
    # the (size-independent) memory profile.
    chunk_max_rows: int = field(default_factory=lambda: _int_env("ONBOARD_CHUNK_MAX_ROWS", 0))

    # --- Headless browser (C1b -- Playwright, for scrape_js sources) ----
    # Run the browser headless (set 0 only to watch it locally during debugging).
    browser_headless: bool = field(
        default_factory=lambda: os.getenv("ONBOARD_BROWSER_HEADLESS", "1").strip().lower()
        not in ("0", "false", "no", "off")
    )
    # Per-step timeout (navigation / selector wait), milliseconds.
    browser_timeout_ms: int = field(default_factory=lambda: _int_env("ONBOARD_BROWSER_TIMEOUT_MS", 45_000))
    # Navigation milestone for page.goto. domcontentloaded is reliable; a bounded
    # networkidle wait happens afterwards in browser.render().
    browser_wait_until: str = field(
        default_factory=lambda: os.getenv("ONBOARD_BROWSER_WAIT_UNTIL", "domcontentloaded").strip()
    )
    # Accept untrusted TLS certs. Default ON: this agent commonly runs behind a
    # TLS-intercepting proxy whose CA the bundled Chromium does not trust, and the
    # raw layer keeps a SHA-256 of every payload regardless.
    browser_ignore_https_errors: bool = field(
        default_factory=lambda: os.getenv("ONBOARD_BROWSER_IGNORE_HTTPS_ERRORS", "1").strip().lower()
        not in ("0", "false", "no", "off")
    )

    # ------------------------------------------------------------------
    def require(self, *keys: str) -> None:
        missing = [k for k in keys if not str(getattr(self, k, "")).strip()]
        if missing:
            env_names = ", ".join(_ATTR_TO_ENV.get(k, k.upper()) for k in missing)
            raise ConfigError(
                f"Missing required configuration: {env_names}. Set these in your "
                "environment or .env file (see .env.example)."
            )

    def snowflake_ready(self) -> bool:
        has_secret = bool(self.snowflake_pat.strip() or self.snowflake_password.strip())
        return has_secret and bool(self.snowflake_warehouse.strip())

    def dbt_dir(self) -> Path:
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


_ATTR_TO_ENV = {
    "anthropic_api_key": "ANTHROPIC_API_KEY",
    "anthropic_model": "ANTHROPIC_MODEL",
    "snowflake_account": "SNOWFLAKE_ACCOUNT",
    "snowflake_user": "SNOWFLAKE_USER",
    "snowflake_password": "SNOWFLAKE_PASSWORD",
    "snowflake_warehouse": "SNOWFLAKE_WAREHOUSE",
    "snowflake_role": "SNOWFLAKE_ROLE",
    "dbt_project_path": "DBT_PROJECT_PATH",
}


settings = Config()
