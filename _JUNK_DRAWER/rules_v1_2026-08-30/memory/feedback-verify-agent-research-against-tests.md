---
name: feedback-verify-agent-research-against-tests
description: "Independently re-verify a research agent's \"low risk\" / \"zero references found\" claim against the FULL test suite before implementing, especially for structural assertions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8a4dfc42-8efc-418c-a5a6-4c32ffe6c25e
  modified: 2026-08-05T01:27:53.414Z
---

Before implementing an optimization or refactor a research agent flagged as
"low risk" based on a grep for symbol references, independently run the full
test suite for every touched file — don't trust the grep alone.

**Why:** during the 2026-08-04 [[bench-plotly-workbench]] perf sweep, a
parallel research workflow proposed two changes and rated both "low risk"
after grepping for direct references to the changed names. Both turned out to
break real tests the grep missed, because the tests asserted on *structural
properties* (an id count > 200, a specific id shape like
`{"bench": "knob", "part": "row"}`) rather than referencing any function or
variable name by string. Running the actual test files caught both:
- Deferring an eager module-level pre-build broke a test asserting
  `len(ids) > 200` in the very first `app.layout` — the test never mentions
  the variable being deferred, so a name-based grep found "zero references."
- Renaming an id family broke ~15 assertions across one test file that all
  hardcoded the old id shape — again, no reference to the changed code by name.

A second, subtler case in the same sweep: a proposed cache added a layer
*underneath* an existing cache that the benchmark's own "cold" test cleared —
the benchmark kept passing and reporting a huge win, but the "cold" row had
silently stopped measuring a cold path. Passing tests and a good-looking
number are not proof of correctness or of an honest measurement.

**How to apply:** treat "grep found nothing" as necessary, not sufficient.
Before acting on an agent's risk assessment for anything touching shared
state, IDs, layout structure, or a benchmark's own methodology, run the real
test suite (or the real benchmark, checking what it actually re-measures)
yourself. If it breaks, that's the answer — don't try to argue the agent's
reasoning was directionally fine; check whether a narrower version of the
change survives, and if not, reject it and say why with the specific
assertion that blocks it.
