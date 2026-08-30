---
name: playground-and-two-desk-state
description: "Current front-end state (2026-08-01) - Playground app + two-desk Reading Room, what's live and what remains"
metadata: 
  node_type: memory
  type: project
  originSessionId: afbdf0c0-8d90-4e4c-bbba-d73c60bd0b93
  modified: 2026-08-01T20:16:48.531Z
---

As of 2026-08-01 the front end is TWO apps, both live and verified:
- **Reading Room v2** (port 8890, `reading_room/`): Case Desk (person-grouped
  hard-ID leads, per-lead decisions) + Pattern Desk (OSHA cohorts,
  TARGET_KIND='cohort' verdicts inheriting to members via
  LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS, specific-beats-general).
  Chris ran provision_pattern_desk.sql + build_review; v1 vessel leads retired.
- **Playground** (port 8502, `playground/`): Chris's daily driver. Question
  packs (`playground/packs.py`, data-only) -> tailored dictionary (tables/
  columns/joins/traps) -> Chris writes SQL -> editable Plotly -> save card.
  NO SQL generation, ever ([[feedback-chris-drives-analysis]]). 9 packs,
  politician-focused.
- Shared plain-English `glossary/` package feeds both apps (tier/verdict
  wording + column glosses in glossary/column_gloss.py).
- COLUMN_CATALOG (LIBRARY_META.REGISTRY.COLUMN_CATALOG) holds per-column
  dictionary rows for the 25 pack tables ONLY; the full ~2,300-table run
  (`python scripts/build_column_catalog.py --apply`) has NOT been run.
- Review-mart rebuilds: ONLY via `library-onboarding/ripple_dbt/build_review.bat`
  (PYTHONUTF8=1 — bare dbt build on Windows mojibakes em-dashes; guard test
  assert_no_mojibake.sql fails such builds).
- Mission focus Chris stated: large systemic US patterns, US-politician
  accountability first. Reading Room = last-step sign-off; Playground = the lab.

**Why:** a new session should extend packs/glossary, not rebuild surfaces or
re-litigate the no-SQL-generation call.
**How to apply:** new investigative question = add a pack to playground/packs.py
(validated by tests/test_playground_offline.py against
tests/fixtures/playground_inventory.json); new column wording = glossary/column_gloss.py
then `build_column_catalog.py --only <FQN> --apply`.
