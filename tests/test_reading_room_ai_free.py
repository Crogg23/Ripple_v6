"""The AI-free gate (Reading Room plan, phase 2.4): no LLM anywhere in any
analyst-facing code path — not at build time, not at read time. This offline
lock greps the Reading Room surfaces for provider tokens so the guarantee can
never regress silently.

Scanned: reading_room/ (the app, once it exists) and the review mart models.
Comments are NOT excepted — the target is zero matches, period.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SURFACES = [
    REPO / "reading_room",
    REPO / "library-onboarding/ripple_dbt/models/marts/review",
    REPO / "library-onboarding/ripple_dbt/tests/assert_lead_queue_reconciles.sql",
]

FORBIDDEN = re.compile(
    r"anthropic|openai|claude|gpt|llm|api\.anthropic|completion",
    re.IGNORECASE,
)

SCAN_SUFFIXES = {".py", ".sql", ".yml", ".yaml", ".toml", ".txt", ".md", ".sh",
                 ".js", ".ts", ".tsx", ".svelte", ".json", ".html", ".css"}


def _files():
    for surface in SURFACES:
        if surface.is_file():
            yield surface
        elif surface.is_dir():
            for path in sorted(surface.rglob("*")):
                if path.is_file() and path.suffix in SCAN_SUFFIXES:
                    yield path


def test_reading_room_surfaces_are_ai_free():
    hits = []
    scanned = 0
    for path in _files():
        scanned += 1
        for lineno, line in enumerate(
                path.read_text(errors="replace").splitlines(), 1):
            if FORBIDDEN.search(line):
                hits.append(f"{path.relative_to(REPO)}:{lineno}: {line.strip()[:120]}")
    assert scanned > 0, "no Reading Room surfaces found to scan"
    assert not hits, (
        "AI-provider tokens found in analyst-facing surfaces "
        "(the Reading Room must run air-gapped from every AI company):\n"
        + "\n".join(hits))
