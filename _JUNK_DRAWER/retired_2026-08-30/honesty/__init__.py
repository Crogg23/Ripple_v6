"""The honesty engine — machine-checked provenance for the mart layer.

Extracted from ROADMAP_2026-07-14 §3.5 and shipped standalone per the 2026-07-20
sprint brief §5.2 (beta decision B9). Three axes, all decided at BUILD TIME from
the committed dbt manifest — no AI, no warehouse, no runtime dependency:

  PROVENANCE  a mart earns 'fact' only if a mechanical walk of its dbt lineage
              shows exclusively hard-ID joins back to landing. Name-joins or
              un-walkable SQL fail closed to 'unverified'; ancestry through the
              leads/claims layer grades 'lead'. Agent judgment is never the
              certifier — the walker is.
  WEAKEST-LINK a measure inherits the weakest grade of everything it touches,
              and the composer REFUSES to blend fact-grade and lead-grade rows
              into one scalar (refusal at compose time, not a badge after).
  FRESHNESS/TRAP the standing POLICY data traps travel with every grade — a
              clean-looking number over a poisoned source is worse than trivia.

Public API:
    load_manifest(path)             -> manifest dict
    grade_model(manifest, node_id)  -> Grade
    grade_marts(manifest)           -> {node_id: Grade}
    assert_composable(inputs)       -> (grade, traps)  or raises BlendRefusal

CLI:  python -m honesty            (writes honesty/mart_grades.json + MART_GRADES.md)
"""

from .grading import Grade, grade_marts, grade_model, load_manifest  # noqa: F401
from .compose import BlendRefusal, MeasureInput, assert_composable, effective_grade  # noqa: F401
from .traps import TRAPS, traps_for_source  # noqa: F401
