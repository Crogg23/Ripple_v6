"""Checkpoint 1 -- RECON.

Fetch a source's docs page, hand the readable text to Claude, and turn the
response into a fully-resolved source config: access pattern, auth, schema,
identifiers, plus the Snowflake table and dbt model names downstream steps use.
"""

from __future__ import annotations

from typing import Optional

import requests

import naming
from llm import call_claude, extract_json, render_prompt

USER_AGENT = "LibraryOnboardingAgent/1.0 (+https://github.com/crogg23/ripple_v6)"
MAX_PAGE_CHARS = 18_000


def fetch_page(url: str, timeout: int = 30) -> str:
    """Fetch a URL and return readable text (scripts/styles stripped)."""
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "")

    # PDFs and other binaries: hand the model the URL + a note rather than bytes.
    if "html" not in content_type and "text" not in content_type and not url.endswith(
        (".html", ".htm", "/")
    ):
        return (
            f"[Non-HTML document at {url} (Content-Type: {content_type or 'unknown'}). "
            "Infer the access pattern and schema from the URL and source name.]"
        )

    try:
        from bs4 import BeautifulSoup
    except ImportError:  # pragma: no cover
        # Without BeautifulSoup, return raw text -- still usable by the model.
        return resp.text[:MAX_PAGE_CHARS]

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:MAX_PAGE_CHARS]


def run_recon(source: dict, feedback: Optional[str] = None) -> dict:
    """Run recon for a source dict and return a resolved config.

    ``source`` carries what we know up front: name, url, layer, identifiers.
    ``feedback`` is foreman text from an ``edit`` action, folded into the prompt.
    """
    name = source["name"]
    url = source["url"]
    layer = source.get("layer", "unknown")
    identifiers = source.get("identifiers", [])

    page_text = "[page not fetched -- fake mode]"
    fetch_error = None
    if not _fake_mode():
        try:
            page_text = fetch_page(url)
        except Exception as exc:  # surface as a note; recon can still proceed
            fetch_error = str(exc)
            page_text = f"[Could not fetch {url}: {exc}]"

    prompt = render_prompt(
        "recon",
        name=name,
        url=url,
        layer=layer,
        identifiers=", ".join(identifiers) or "(none known yet)",
        feedback=feedback or "(none)",
        page_text=page_text,
    )

    raw = call_claude(
        user=prompt,
        system="You are a meticulous data-engineering recon analyst. Output strict JSON only.",
        kind="recon",
        fake_context=source,
        max_tokens=3000,
    )
    extracted = extract_json(raw)

    return _resolve(source, extracted, fetch_error)


def _resolve(source: dict, extracted: dict, fetch_error: Optional[str]) -> dict:
    """Merge known queue metadata with Claude's output and derive names."""
    name = source["name"]
    layer = source.get("layer", "unknown")

    # Identifiers: prefer the queue's curated list, union anything Claude adds.
    identifiers = list(source.get("identifiers", []))
    for ident in extracted.get("key_identifiers", []) or []:
        if ident not in identifiers:
            identifiers.append(ident)

    entity = naming.slug(extracted.get("entity") or "records")
    domain = extracted.get("domain") or naming.LAYER_DOMAIN.get(layer, layer)

    auth = extracted.get("auth") or {}
    if isinstance(auth, str):  # tolerate a bare string from the model
        auth = {"type": auth, "notes": ""}

    parts = naming.raw_table_parts(name, entity)

    config = {
        "name": name,
        "url": source["url"],
        "layer": layer,
        "description": extracted.get("description", ""),
        "access_pattern": extracted.get("access_pattern", "unknown"),
        "auth": {"type": auth.get("type", "none"), "notes": auth.get("notes", "")},
        "format": extracted.get("format", "unknown"),
        "est_volume": extracted.get("est_volume", "unknown"),
        "update_frequency": extracted.get("update_frequency", "unknown"),
        "rate_limits": extracted.get("rate_limits", "unspecified"),
        "key_identifiers": identifiers,
        "schema_fields": extracted.get("schema_fields", []),
        "entity": entity,
        "raw_database": parts["database"],
        "raw_schema": parts["schema"],
        "raw_table": naming.qualified_raw_table(name, entity),
        "raw_table_short": parts["table"],
        "staging_model": naming.staging_model(name, entity),
        "mart_model": extracted.get("mart_model") or naming.mart_model(domain, name, entity),
        "joins_to": extracted.get("joins_to", []),
        "notes": extracted.get("notes", ""),
        "fetch_error": fetch_error,
    }
    return config


def _fake_mode() -> bool:
    from config import settings

    return settings.fake_llm
