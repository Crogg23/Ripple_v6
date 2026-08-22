# RIPPLE STATUS — 2026-08-21 (evening) — canonical clock rollout finished

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new this session.** Carried, untouched: (1) roll-call vote mart
still disagrees with its Python-built twin — standing since 2026-08-18. (2) Twelve
Python test modules fail to COLLECT for a missing charting library, hiding ~1,400
tests. (3) Column-classifier substring cosmetic bug. (4) Count-question generator
per-type caps.

**Correction to this morning's handoff, found before any work started:** the
canonical-clock-rollout plan (`reports/handoff_canonical_clock_rollout.md`)
believed two of its three gaps were still open. Both were wrong.
- **"253 of 482 tables never got classified" — false.** The classification file
  (`clock_index.csv`) was complete for all 482 tables the whole time. Only the
  narrative write-up (`CLOCK_FINDINGS.md`) undersold it — it was composed from a
  truncated read of its own source. Verified directly this session (2,089 rows,
  482 unique tables, real per-column reasoning in every domain including the
  "unreviewed" ones). Corrected numbers: 46 clock-less tables (not 35/53), 74
  reporting-lag tables (not 33), 75 span tables (not 35).
- **"The canonical column is not rolled out" — also false.** A different branch
  had already built it (403 tables, one shared timeline, view-based not a mart
  rebuild) and merged into main this morning, before the handoff session wrote
  that line. `reports/time_index/README.md` still said "NOT done" because it
  predated its own project's later commit. Fixed the stale note.

**What this session actually built: the one real gap, "planned" dates.** A
happened/reported/decided clock whose value sits in the future — a proposed
rule's effective date, a scheduled hearing, a not-yet-final enforcement date —
used to either get silently read as an ordinary past event (wrong) or get
dropped once more than a year out (data loss). Now every canonical timestamp is
checked per row: future values get tagged `planned` instead and are kept, not
nulled. Deployed live and verified against real warehouse data — 633 rows
across ~20 tables now correctly separated out (biggest: EPA drinking-water
compliance milestones, FEC candidate-cycle placeholders reaching to 2106).
Added a guard test that fails the build if a `planned` tag and its timestamp
ever disagree — it passed clean on the first live run.

**Full detail:** `reports/time_index/TIMELINE_LAYER.md` (the layer, updated),
`reports/time_index/CLOCK_FINDINGS.md` (corrected counts, correction note at
top), `library-onboarding/ripple_dbt/macros/ripple_time.sql` (the new
`ripple_row_clock` macro), `scripts/census/gen_time_views.py` (regenerator).

**Not committed.** 370 files changed (macro, generator, guard test, 3 docs, 358
regenerated view models — only the future-guarded ones actually changed
content). Sitting in the working tree; Chris hasn't asked for a commit.

**YOUR MOVE (Chris):** two open decisions carried from this morning, either can
wait: (1) is the RIPPLES.md 5th-landmine addition (shared inspector scheduling
can fake a neighbor signal) worth making, (2) whether/when to chase the
healthcare pilot rule's weak signal further. Neither touched this session.

**NEXT:** nothing queued. The date-correctness foundation the mission's
timeline/lead-lag rules depend on is now actually finished — the rules layer
(health, environment, labor domains, per the neighbor-coverage map) is fair
game whenever Chris wants the next pilot.
