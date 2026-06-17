"""Thin wrapper around the Anthropic API plus prompt-template loading.

Every Claude-powered step -- recon, ingest codegen, dbt scaffolding, catalog
registration -- goes through :func:`call_claude`. Set ``ONBOARD_FAKE_LLM=1`` to
short-circuit the network call and return deterministic fixtures, which lets the
whole checkpoint flow be exercised offline (no API key, no outbound network).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Optional

from config import ConfigError, settings

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------
def load_prompt(name: str) -> str:
    """Load a prompt template from the ``prompts/`` directory."""
    path = PROMPTS_DIR / f"{name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_prompt(template_name: str, **kwargs: Any) -> str:
    """Load a prompt template and fill ``{placeholders}`` with kwargs."""
    template = load_prompt(template_name)
    # Use a forgiving formatter so stray braces in the template don't blow up.
    for key, value in kwargs.items():
        template = template.replace("{" + key + "}", str(value))
    return template


# ---------------------------------------------------------------------------
# The single entry point every module uses
# ---------------------------------------------------------------------------
def call_claude(
    user: str,
    system: str = "",
    kind: str = "generic",
    max_tokens: int = 4096,
    fake_context: Optional[dict] = None,
) -> str:
    """Call Claude (or the offline fake) and return the response text.

    ``kind`` lets the offline fixture return something shaped correctly for the
    calling step; the real API ignores it.
    """
    if settings.fake_llm:
        return _fake_response(kind, fake_context or {})

    return _real_call(user=user, system=system, max_tokens=max_tokens)


def _real_call(user: str, system: str, max_tokens: int) -> str:
    settings.require("anthropic_api_key")
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "The 'anthropic' package is not installed. Run "
            "`pip install -r requirements.txt`."
        ) from exc

    from tenacity import (
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    @retry(
        reraise=True,
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        retry=retry_if_exception_type(
            (
                anthropic.APIConnectionError,
                anthropic.RateLimitError,
                anthropic.InternalServerError,
            )
        ),
    )
    def _send() -> str:
        # Stream and reassemble: the Anthropic SDK REQUIRES streaming for requests
        # whose max_tokens is large enough to risk a >10-min generation (it raises
        # "Streaming is required for operations that may take longer than 10 minutes"
        # otherwise). dbt-gen for wide tables uses a high max_tokens ceiling, so we
        # always stream and accumulate -- identical text, no token-ceiling foot-gun.
        with client.messages.stream(
            model=settings.anthropic_model,
            max_tokens=max_tokens,
            system=system or "You are a precise data-engineering assistant.",
            messages=[{"role": "user", "content": user}],
        ) as stream:
            message = stream.get_final_message()
        return "".join(
            block.text for block in message.content if getattr(block, "type", "") == "text"
        )

    return _send()


# ---------------------------------------------------------------------------
# Response parsing helpers
# ---------------------------------------------------------------------------
def extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response.

    Robust to ```json fences, leading/trailing prose, dbt Jinja braces (``{{ }}``)
    inside string values, and literal newlines in embedded SQL/YAML. We match the
    fence greedily (so an inner ``}`` doesn't cut it short) and parse with
    ``strict=False`` so multi-line SQL / YAML values are tolerated.
    """
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        candidate = fenced.group(1)
    else:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise ValueError(f"No JSON object found in response:\n{text[:500]}")
        candidate = text[start : end + 1]
    try:
        return json.loads(candidate, strict=False)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse JSON ({exc}) from response:\n{text[:500]}")


def extract_code(text: str, language: str = "python") -> str:
    """Pull a fenced code block (defaulting to python) out of a response."""
    fenced = re.search(
        rf"```(?:{language})?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE
    )
    if fenced:
        return fenced.group(1).strip()
    return text.strip()


# ---------------------------------------------------------------------------
# Offline fixtures (ONBOARD_FAKE_LLM=1)
# ---------------------------------------------------------------------------
def _fake_response(kind: str, ctx: dict) -> str:
    if kind == "recon":
        return json.dumps(_fake_recon(ctx))
    if kind == "ingest":
        return _fake_ingest(ctx)
    if kind == "dbt":
        return json.dumps(_fake_dbt(ctx))
    if kind == "registry":
        return json.dumps(_fake_registry(ctx))
    return "{}"


def _fake_recon(ctx: dict) -> dict:
    name = ctx.get("name", "Unknown Source")
    identifiers = ctx.get("identifiers", [])
    is_fred = "fred" in name.lower()
    return {
        "jurisdiction": "federal",
        "category": "Economy" if is_fred else "unknown",
        "subcategory": "Macroeconomic indicators" if is_fred else "",
        "publisher": "Federal Reserve Bank of St. Louis" if is_fred else name,
        "description": "Federal Reserve Economic Data" if is_fred else f"{name} data source",
        "unit_of_observation": "one row = one series observation" if is_fred else "one row = one record",
        "temporal_coverage": "1947-present" if is_fred else "unknown",
        "geographic_scope": "US (national + regional)" if is_fred else "unknown",
        "access_pattern": "paginated_api" if is_fred else "bulk_csv",
        "access_method": "API" if is_fred else "bulk download",
        "auth": {
            "type": "free API key" if is_fred else "none",
            "notes": "free -- register at fredaccount.stlouisfed.org" if is_fred else "no auth required",
        },
        "format": "JSON" if is_fred else "CSV",
        "cost": "free",
        "update_cadence": "daily" if is_fred else "unknown",
        "est_volume": "~845,000 series" if is_fred else "unknown",
        "license_terms": "public domain",
        "key_identifiers": identifiers,
        "accountability_relevance": "Macroeconomic baseline for follow-the-money analysis." if is_fred else "",
        "priority_tier": "2",
        "schema_fields": [
            {"name": "series_id", "type": "TEXT", "description": "FRED series identifier"},
            {"name": "date", "type": "TEXT", "description": "Observation date (raw string)"},
            {"name": "value", "type": "TEXT", "description": "Observation value (raw string)"},
        ]
        if is_fred
        else [
            {"name": "id", "type": "TEXT", "description": "Record identifier"},
            {"name": "value", "type": "TEXT", "description": "Record value"},
        ],
        "entity": "series" if is_fred else "records",
        "joins_to": [{"source": "fed_census_acs", "on": "FIPS"}] if "FIPS" in identifiers else [],
        "notes": "[FAKE_LLM fixture -- not real recon output]",
    }


def _fake_ingest(ctx: dict) -> str:
    return (
        "```python\n"
        "import pandas as pd\n"
        "\n"
        "def fetch_data(context):\n"
        '    """[FAKE_LLM fixture] Return a tiny synthetic frame for offline demo.\n'
        "\n"
        "    Real scripts also stash the raw source bytes for content hashing:\n"
        '        context["source_bytes"] = resp.content\n'
        '        context["source_file"] = "all_month.csv"\n'
        '    """\n'
        '    rows = [\n'
        '        {"series_id": "GDP", "date": "2024-01-01", "value": "27000.0"},\n'
        '        {"series_id": "GDP", "date": "2024-04-01", "value": "27200.0"},\n'
        '        {"series_id": "UNRATE", "date": "2024-01-01", "value": "3.7"},\n'
        "    ]\n"
        '    context["source_bytes"] = repr(rows).encode("utf-8")\n'
        '    context["source_file"] = "fixture.csv"\n'
        "    return pd.DataFrame(rows)\n"
        "```\n"
    )


def _fake_dbt(ctx: dict) -> dict:
    sid = ctx.get("source_id", "fed_fred")
    table = ctx.get("landing_table", sid.upper())
    entity = ctx.get("entity", "records")
    stg = f"stg_{sid}__{entity}"
    return {
        "staging_sql": (
            "{{ config(materialized='view') }}\n\n"
            f"with source as (\n    select * from {{{{ source('ripple_raw', '{table}') }}}}\n),\n"
            "renamed as (\n    select\n        series_id::varchar     as series_id,\n"
            "        try_to_date(date)      as observation_date,\n"
            "        try_to_double(value)   as value,\n"
            "        _ingested_at,\n        _source_run_id\n    from source\n"
            ")\nselect * from renamed\n"
        ),
        "intermediate_sql": "",
        "mart_sql": (
            "{{ config(materialized='table') }}\n\n"
            f"select series_id, observation_date, value\nfrom {{{{ ref('{stg}') }}}}\n"
        ),
        "schema_yml": (
            "version: 2\n\nmodels:\n"
            f"  - name: {stg}\n"
            "    description: '[FAKE_LLM fixture] staged rows.'\n"
            "    columns:\n"
            "      - name: series_id\n        description: Series identifier.\n"
            "        data_tests: [not_null]\n"
        ),
    }


def _fake_registry(ctx: dict) -> dict:
    return {
        "accountability_relevance": "[FAKE_LLM fixture] relevance note.",
        "epstein_relevant": "no",
        "notes": "[FAKE_LLM fixture] registered by agent.",
    }
