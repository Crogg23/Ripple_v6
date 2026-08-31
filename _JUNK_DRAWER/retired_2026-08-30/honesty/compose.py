"""The refusal — weakest-link inheritance, enforced at compose time.

ROADMAP §3.5: "the composer refuses to emit SQL blending fact-grade and
lead-grade rows into one scalar — refusal at compose time, not a badge after
the fact." This module is that refusal, pure and offline-testable. Any surface
that composes measures (a future Atlas, a report script, evidence.dev build
tooling) calls assert_composable() BEFORE emitting SQL.
"""

from __future__ import annotations

from dataclasses import dataclass

from .grading import FACT, LEAD, UNVERIFIED, _STRENGTH
from .traps import TRAPS


class BlendRefusal(Exception):
    """Raised when a single scalar would silently blend fact- and lead-grade rows."""


@dataclass(frozen=True)
class MeasureInput:
    """One thing a composed scalar touches: a mart, a view, a measure."""
    name: str
    grade: str                 # fact | lead | unverified
    traps: tuple[str, ...] = ()

    def __post_init__(self):
        if self.grade not in _STRENGTH:
            raise ValueError(f"unknown grade {self.grade!r} for {self.name!r}")


def effective_grade(inputs: list[MeasureInput] | tuple[MeasureInput, ...]) -> str:
    """A measure inherits the WEAKEST provenance of everything it touches."""
    if not inputs:
        raise ValueError("effective_grade needs at least one input")
    return min((i.grade for i in inputs), key=lambda g: _STRENGTH[g])


def assert_composable(
    inputs: list[MeasureInput] | tuple[MeasureInput, ...],
    single_scalar: bool = True,
) -> tuple[str, tuple[str, ...]]:
    """Gate a composition. Returns (effective_grade, sorted trap keys).

    Refuses (raises BlendRefusal) when a SINGLE SCALAR would mix fact-grade
    inputs with lead/unverified ones — that number would wear fact's face on
    a claim's body. Same-grade blends pass; non-fact blends pass at the
    weakest grade (they never pretended to be fact). Pass
    single_scalar=False for side-by-side renders (small multiples, separate
    tiles), where each input keeps its own badge and no blending occurs.
    """
    grade = effective_grade(inputs)
    grades = {i.grade for i in inputs}
    if single_scalar and FACT in grades and (grades & {LEAD, UNVERIFIED}):
        offenders = ", ".join(f"{i.name}={i.grade}" for i in inputs if i.grade != FACT)
        anchors = ", ".join(i.name for i in inputs if i.grade == FACT)
        raise BlendRefusal(
            "REFUSED: one scalar would blend fact-grade rows "
            f"({anchors}) with claim-grade rows ({offenders}). Render them "
            "side by side with their own badges, or upgrade the weak input's "
            "lineage — never average a fact with a claim."
        )
    traps = tuple(sorted({t for i in inputs for t in i.traps}))
    return grade, traps


def disclosures(trap_keys: tuple[str, ...]) -> list[str]:
    """The mandatory on-chart/on-page texts for a set of trap keys."""
    return [f"{k}: {TRAPS[k]}" for k in trap_keys if k in TRAPS]


def measure_input_for_mart(mart: str, grades_path=None) -> MeasureInput:
    """Build a MeasureInput from the COMMITTED grades file — the safe way in.

    Hand-typing grade='fact' bypasses everything the walker derived (the
    2026-07-21 review's one caveat on this module). Callers should use this,
    so the label a composition trusts is always the label the machine earned.
    """
    import json
    from pathlib import Path

    path = Path(grades_path) if grades_path else Path(__file__).resolve().parent / "mart_grades.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for node_id, g in data["grades"].items():
        if node_id == mart or node_id.split(".")[-1] == mart:
            return MeasureInput(mart, g["grade"], tuple(g["traps"]))
    raise KeyError(f"mart {mart!r} not found in {path} — regenerate with `python -m honesty`")
