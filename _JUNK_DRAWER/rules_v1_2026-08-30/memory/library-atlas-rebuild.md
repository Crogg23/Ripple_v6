---
name: library-atlas-rebuild
description: "The portfolio Atlas rebuild (2026-08-02) — files, commands, and the traps hit while building it"
metadata: 
  node_type: memory
  type: project
  originSessionId: 04077769-0957-40b5-bb95-8b7b55c5b8ef
  modified: 2026-08-02T18:29:57.426Z
---

Chris green-lit a full rebuild of the Library map as a portfolio piece
(2026-08-02): all 1,043 tables, presence-first, cinematic, Python/Plotly/Dash.
Shipped that day, both test suites green.

- Pipeline: `python -m viz.compile_library` → outputs/library.json →
  `python -m viz.library_app` (ATLAS_PORT env overrides 8050) →
  `python -m viz.export_html` for the standalone postcard.
- Tests: `python -m viz.test_compile` (determinism + invariants) and
  `python -m viz.test_library` (Playwright; CHECKS-registry style, not pytest).
- viz/compile_anatomy.py and viz/compile_atlas.py are DEPRECATED (docstrings
  say so) but kept while docs/*.html twins still read their JSONs.
- viz/atlas_app.py (368-table Dash app) is superseded by viz/library_app.py.

**Why:** traps found here will recur in any Dash work on this repo.

**How to apply:**
- Dash drops a callback whose Input id doesn't exist in the initial layout
  (ReferenceError in browser only; suppress_callback_exceptions does NOT
  cover it) — use pattern-matching ids for components born inside callbacks.
- Duplicate pattern ids (two dossier rows linking the same neighbour) break
  click delivery silently — include a row number in the id.
- A figure→…→figure dependency cycle makes the renderer drop the final
  update; clientside `set_props` is the reliable way to push state from a
  long-running clientside callback ([[loader-runtime-traps]] energy, UI edition).
- A stale server on port 8050 (old atlas_app) can answer smoke tests for the
  new app — always check who owns the port before trusting a green check.
