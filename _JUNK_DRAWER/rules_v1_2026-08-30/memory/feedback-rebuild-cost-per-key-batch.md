---
name: feedback-rebuild-cost-per-key-batch
description: "2026-08-29 crashout — Chris ran a full spine rebuild on 08-28 after being told \"don't wait for all the joins, it won't matter\"; next day a new key batch needed ANOTHER full rebuild. Always attach the recurring rebuild price to any \"rebuild now\" advice."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ae3d683b-a240-40da-be51-79975a87c0ff
  modified: 2026-08-29T15:08:24.566Z
---

On 2026-08-28 Chris asked whether to wait until all potential joins were flushed out
before a full spine rebuild. A session said don't wait, it won't matter. On 2026-08-29
eight new key families were wired (behind the freeze flag) and the spine needs another
full rebuild (~$10–15, ~4.5h) to include them. Chris felt lied to.

**Why:** "Don't wait" was right (the join list is never finished), but "it won't matter"
hid a real recurring cost: every new key batch re-keys entities, trips the config guard,
and requires a full rebuild. That is the freeze-flag design ([[courtlistener-key-registration-2026-08-17]]).
The price tag was owed under CLAUDE.md §8.7 and wasn't shown.

**RESOLVED the same day:** (1) the 4.5h/$10–15 figure was stale — the 08-28 rebuild was
~50 busy-minutes on X-Small (~$2–3), the 08-11 one 25 min; (2) the freeze is gone —
`python -m connect apply-config` applies any key/spec change as bounded per-table
reslices (see `reports/recon/apply_config_design_2026-08-29.md`). Never quote the
rebuild without pulling its real duration from query history first.

**How to apply:**
- Any "rebuild now" or "don't wait" advice must carry: *"and expect ~$12 / ~4.5h again
  each time we add a key batch."*
- When staging keys dark, say in the same breath that the LAST rebuild does not include
  them — never let Chris believe a rebuild he just ran covers work staged after it.
- Batch key additions before a rebuild where possible; if a batch is coming within a day,
  say so before he spends.
- Related: [[feedback-cost-runaway-alert]], [[spine-full-rebuild-2026-08-08]].
