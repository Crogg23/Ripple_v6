"""Checkpoint 1 -- RECON.

Fetch a source's docs page, hand the readable text to Claude, and turn the
response into a fully-resolved profile: a SOURCE_REGISTRY-shaped record plus the
SOURCE_ID, the LIBRARY_RAW.LANDING table, and the dbt model names downstream
steps use.
"""

from __future__ import annotations

from typing import Optional

import requests

import browser
import naming
from config import settings
from llm import call_claude, extract_json, render_prompt

USER_AGENT = "RippleOnboardingAgent/1.0 (+https://github.com/Crogg23/Ripple_v6)"
MAX_PAGE_CHARS = 18_000


def fetch_page(url: str, timeout: int = 30) -> tuple[str, bool]:
    """Fetch a URL and return ``(readable_text, browser_required)``.

    ``browser_required`` is True when a plain HTTP GET hit a bot-challenge / empty
    SPA shell and we had to render the page in a headless browser to read it -- the
    signal recon uses to set ``access_pattern=scrape_js``.
    """
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "")

    if "html" not in content_type and "text" not in content_type and not url.endswith(
        (".html", ".htm", "/")
    ):
        return (
            f"[Non-HTML document at {url} (Content-Type: {content_type or 'unknown'}). "
            "Infer the access pattern and schema from the URL and source name.]",
            False,
        )

    try:
        from bs4 import BeautifulSoup
    except ImportError:  # pragma: no cover
        return resp.text[:MAX_PAGE_CHARS], False

    html = resp.text
    browser_required = False
    # If the static fetch hit a bot-challenge ("Just a moment...") or an empty SPA
    # shell, the readable text we'd hand Claude is a wall, not the source -- recon
    # would mis-profile it. Escalate to the headless browser (C1b) to get the real,
    # JS-rendered page, and remember that we HAD to -- so recon flags scrape_js.
    # Best-effort: if Playwright/Chromium isn't installed we fall back to the static
    # HTML and recon notes the gap.
    if browser.looks_blocked(html):
        try:
            rendered = browser.render(url)
            if rendered and not browser.looks_blocked(rendered):
                html = rendered
                browser_required = True
        except Exception:
            pass  # browser unavailable -- recon profiles from the static shell

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:MAX_PAGE_CHARS], browser_required


def run_recon(source: dict, feedback: Optional[str] = None) -> dict:
    """Run recon for a source dict and return a resolved profile."""
    name = source["name"]
    url = source["url"]
    layer = source.get("layer", "unknown")
    identifiers = source.get("identifiers", [])

    page_text = "[page not fetched -- fake mode]"
    fetch_error = None
    browser_required = False
    if not settings.fake_llm:
        try:
            page_text, browser_required = fetch_page(url)
        except Exception as exc:
            fetch_error = str(exc)
            page_text = f"[Could not fetch {url}: {exc}]"

    # Tell recon when the static fetch was blocked and only a headless browser could
    # read the page -- that is exactly the scrape_js signal.
    access_note = (
        "A plain HTTP GET of this URL returned a bot-challenge / JS-required shell "
        "(no usable data); the readable text below was obtained by RENDERING the page "
        "in a headless browser. This source needs a browser to access -- set "
        "access_pattern = scrape_js."
        if browser_required
        else "(A plain HTTP GET returned the page directly -- no headless browser was needed.)"
    )

    prompt = render_prompt(
        "recon",
        name=name,
        url=url,
        layer=layer,
        identifiers=", ".join(identifiers) or "(none known yet)",
        feedback=feedback or "(none)",
        access_note=access_note,
        page_text=page_text,
    )
    raw = call_claude(
        user=prompt,
        system="You are a meticulous data-engineering recon analyst for an investigative-journalism data platform. Output strict JSON only.",
        kind="recon",
        fake_context=source,
        max_tokens=3000,
    )
    return _resolve(source, extract_json(raw), fetch_error, browser_required)


def _resolve(source: dict, extracted: dict, fetch_error: Optional[str],
             browser_required: bool = False) -> dict:
    name = source["name"]
    layer = source.get("layer", "unknown")

    # A foreman-pinned jurisdiction / source_id on the input wins over recon's
    # guess -- lets us onboard a specific slice without colliding with (and
    # overwriting) an existing SOURCE_REGISTRY row.
    jurisdiction = (
        source.get("jurisdiction")
        or extracted.get("jurisdiction")
        or naming.LAYER_JURISDICTION.get(layer, "cross-cutting")
    ).strip().lower()
    if jurisdiction not in naming.JURISDICTION_PREFIX:
        jurisdiction = "cross-cutting"

    sid = naming.source_id(source.get("source_id") or extracted.get("source_id") or name, jurisdiction)
    entity = naming.slug(extracted.get("entity") or "records")
    domain = extracted.get("domain") or naming.JURISDICTION_DOMAIN.get(jurisdiction, jurisdiction)

    identifiers = list(source.get("identifiers", []))
    for ident in extracted.get("key_identifiers", []) or []:
        if ident not in identifiers:
            identifiers.append(ident)

    auth = extracted.get("auth") or {}
    if isinstance(auth, str):
        auth = {"type": auth, "notes": ""}

    # access_pattern: a foreman pin wins; otherwise recon's guess. But if fetching
    # the page EMPIRICALLY required a headless browser (the static GET was a
    # bot-challenge / empty JS shell), that's ground truth, not a guess -- force
    # scrape_js regardless of what the LLM proposed (it sees the rendered HTML and
    # often mistakes it for plain scrape). This is the autonomous scrape_js trigger.
    access_pattern = source.get("access_pattern") or extracted.get("access_pattern", "unknown")
    if browser_required and not source.get("access_pattern"):
        access_pattern = "scrape_js"

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
        "access_pattern": access_pattern,
        # Incremental load (huge / daily-growing sources): a foreman-pinned value
        # wins; else recon's guess; else snapshot (the default mirror).
        "load_mode": (source.get("load_mode") or extracted.get("load_mode") or "snapshot").strip().lower(),
        "cursor_field": source.get("cursor_field") or extracted.get("cursor_field") or "",
        "primary_key": source.get("primary_key") or extracted.get("primary_key") or "",
        "rate_limits": extracted.get("rate_limits", "unspecified"),
        "schema_fields": extracted.get("schema_fields", []),
        "staging_model": naming.staging_model(sid, entity),
        "mart_model": extracted.get("mart_model") or naming.mart_model(domain, sid),
        "joins_to": extracted.get("joins_to", []),
        "notes": extracted.get("notes", ""),
        "fetch_error": fetch_error,
    }
