---
name: feedback-workflow-warehouse-restriction-every-phase
description: "Multi-phase Workflow scripts need \"no warehouse access\" restated in every phase's prompt, not just phase 1 — it does not carry over"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e9775a6d-b65a-444b-92e3-901f0dc9e654
  modified: 2026-08-07T15:30:36.742Z
---

On 2026-08-07, a multi-phase Workflow (draft a fix, then independently verify it) was scoped as offline/file-edit-only. The "do not run dbt, do not connect to any warehouse" instruction was written into the draft-phase prompt only. The verify-phase prompt had no such restriction, and those agents — quite reasonably, given they had warehouse-query tools available and were told to independently confirm correctness — ran ~89 live read-only queries against Snowflake without it ever being priced or approved first, a real CLAUDE.md §8.7 violation (real compute needs a price tag shown BEFORE it happens, not after).

**Why this happened:** restrictions written into one stage of a pipeline() do not implicitly apply to later stages — each agent() call gets exactly the prompt text it's given, nothing inherited from a sibling stage.

**How to apply:** any constraint that must hold for the whole workflow (no warehouse access, no writes outside a given directory, no external network calls, etc.) has to be restated explicitly in every single phase's prompt text, not stated once and assumed to carry through pipeline()/parallel() stages. When drafting a multi-phase Workflow script, do a final pass checking that every phase's prompt independently states every hard constraint that matters — don't rely on "I already said that in phase 1."

Side note on this specific incident: the unpriced spend was genuinely small (89 queries, ~0.35 credits, ~$1 at the account's confirmed $3/credit rate — verified via `INFORMATION_SCHEMA.QUERY_HISTORY()` and `WAREHOUSE_METERING_HISTORY` after the fact, not guessed) and it caught 44 real wrong keys before they shipped, plus surfaced several genuine data-quality bugs (masked columns from bad casts, an EPA ICIS-AIR ingestion-duplication bug, a false "unique" claim on a DEA ARCOS 178M-row table). The productive outcome does not excuse the process miss — Chris was told about it plainly as the first thing in the next report, per [[interaction-contract]] and the no-publish-nudging-style rule that bad news is never softened or buried under good outcomes.

Related: [[interaction-contract]], [[warehouse-data-traps]], [[bridge-fuel-reality]]
