"""Checkpoint 1 -- RECON.

Fetch a source's docs page, hand the readable text to Claude, and turn the
response into a fully-resolved profile: a SOURCE_REGISTRY-shaped record plus the
SOURCE_ID, the RIPPLE_RAW.LANDING table, and the dbt model names downstream
steps use.
"""

from __future__ import annotations

from typing import Optional

import requests

import naming
from config import settings
from llm import call_claude, extract_json, render_prompt

USER_AGENT = "RippleOnboardingAgent/1.0 (+https://github.com/Crogg23/Ripple_v6)"
MAX_PAGE_CHARS = 18_000


def fetch_page(url: str, timeout: int = 30) -> str:
    """Fetch a URL and return readable text (scripts/styles stripped)."""
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "")

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
        return resp.text[:MAX_PAGE_CHARS]

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:MAX_PAGE_CHARS]


def run_recon(source: dict, feedback: Optional[str] = None) -> dict:
    """Run recon for a source dict and return a resolved profile."""
    name = source["name"]
    url = source["url"]
    layer = source.get("layer", "unknown")
    identifiers = source.get("identifiers", [])

    page_text = "[page not fetched -- fake mode]"
    fetch_error = None
    if not settings.fake_llm:
        try:
            page_text = fetch_page(url)
        except Exception as exc:
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
        system="You are a meticulous data-engineering recon analyst for an investigative-journalism data platform. Output strict JSON only.",
        kind="recon",
        fake_context=source,
        max_tokens=3000,
    )
    return _resolve(source, extract_json(raw), fetch_error)


def _resolve(source: dict, extracted: dict, fetch_error: Optional[str]) -> dict:
    name = source["name"]
    layer = source.get("layer", "unknown")

    jurisdiction = (extracted.get("jurisdiction") or naming.LAYER_JURISDICTION.get(layer, "cross-cutting")).strip().lower()
    if jurisdiction not in naming.JURISDICTION_PREFIX:
        jurisdiction = "cross-cutting"

    sid = naming.source_id(extracted.get("source_id") or name, jurisdiction)
    entity = naming.slug(extracted.get("entity") or "records")
    domain = extracted.get("domain") or naming.JURISDICTION_DOMAIN.get(jurisdiction, jurisdiction)

    identifiers = list(source.get("identifiers", []))
    for ident in extracted.get("key_identifiers", []) or []:
        if ident not in identifiers:
            identifiers.append(ident)

    auth = extracted.get("auth") or {}
    if isinstance(auth, str):
        auth = {"type": auth, "notes": ""}

    return {
        # identity
        "name": name,
        "url": source["url"],
        "layer": layer,
        "source_id": sid,
        "landing_table": naming.landing_table(sid),
        "entity": entity,
        # registry fields
        "jurisdiction": jurisdiction,
        "category": extracted.get("category", "unknown"),
        "subcategory": extracted.get("subcategory", ""),
        "publisher": extracted.get("publisher", ""),
        "description": extracted.get("description", ""),
        "unit_of_observation": extracted.get("unit_of_observation", ""),
        "temporal_coverage": extracted.get("temporal_coverage", "unknown"),
        "geographic_scope": extracted.get("geographic_scope", "unknown"),
        "access_method": extracted.get("access_method", "unknown"),
        "format": extracted.get("format", "unknown"),
        "auth": {"type": auth.get("type", "none"), "notes": auth.get("notes", "")},
        "cost": extracted.get("cost", ""),
        "update_cadence": extracted.get("update_cadence", "unknown"),
        "volume": extracted.get("est_volume", extracted.get("volume", "unknown")),
        "license_terms": extracted.get("license_terms", ""),
        "key_identifiers": identifiers,
        "join_keys": ", ".join(identifiers),
        "accountability_relevance": extracted.get("accountability_relevance", ""),
        "priority_tier": str(extracted.get("priority_tier", "2")),
        # ingest + dbt
        "access_pattern": extracted.get("access_pattern", "unknown"),
        "rate_limits": extracted.get("rate_limits", "unspecified"),
        "schema_fields": extracted.get("schema_fields", []),
        "staging_model": naming.staging_model(sid, entity),
        "mart_model": extracted.get("mart_model") or naming.mart_model(domain, sid),
        "joins_to": extracted.get("joins_to", []),
        "notes": extracted.get("notes", ""),
        "fetch_error": fetch_error,
    }
