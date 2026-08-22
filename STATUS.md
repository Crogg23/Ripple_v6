# RIPPLE STATUS — 2026-08-22 (backend squared; all three pastes applied)

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE / SECURITY FIRST:**
- **The "read-only" session login is not actually read-only.** The PAT signs in
  as RIPPLE_READER but inherits ALL the user's roles as secondary roles —
  including ACCOUNTADMIN. Every session that believed it couldn't write, could
  have. Fix is staged (item 4, commented out, Chris's call) in
  outputs/BACKEND_SQUARE_AWAY_batch_2026-08-21.sql.
- **Roll-call marts still disagree (carried since 08-18), now DIAGNOSED:** the
  dbt full-history mart has 113,512 rows; the Python-built audited canonical
  has 3,364 (118th–119th congresses only). A standing guard correctly blocks
  dbt from overwriting the audited one. Open question for a session with the
  politics build context: is the small one "intended recent-only scope" (then
  add to the duplication test's known-divergent list with the reason) or stale?
- Carried: column-classifier substring cosmetic bug; count-question generator
  per-type caps; the physical mart rename for the water service-area table
  (model file + timeline wrappers live under the immigration schema — queued
  cleanup with regeneration steps, catalog label fix staged in the batch).

**FIXED THIS SESSION (backend square-away, Chris said "just go"):**
1. **~1,400 hidden tests un-hidden** (installed the missing charting library,
   fixed one bad tests.* import). Full suite now collects: 3,096 tests.
2. Of the 85 real failures that surfaced: **79 are one missing grant** (reader
   role can't see LIBRARY_RAW.LANDING — grants staged in the batch file);
   **4 chart-bench failures fixed in code** (pandas 2.x datetime arithmetic in
   the events chart; suite section now green); 1 is the roll-call finding above;
   1 KeyError on a spec table (FED_SAM_EXCLUSIONS_FULL_R2) in the same
   grant-blocked family.
3. **Queue triage pass shipped and run:** the 1,830-pair queue is now stamped
   62% MACRO (no entity exists — never wireable, macro/climate questions),
   31% WIREABLE, 6% GEO_ONLY. The honest wiring debt is 575 pairs, not "81%".
   scripts/ripples/queue_triage_pass.py + reports/ripples_queue_triage JSON.
4. **Wiring scout extended to all 147 dark tables** (same-day JSON updated).
   ARCOS name-match test: only 9/87 distributor names exact-match the corporate
   crosswalk — parked (needs fuzzy matching + human review).

**EARLIER SAME DAY (still true):** weather glossary chosen and written into
docs/RIPPLES.md (internal-brain only); machine-health artifact "The Station
Wall" (rebuilt plain after "not intuitive enough"); 5 politics edges APPLIED by
Chris and verified (edge table 4,904; first hard politics→FEC bridge, 66%);
wire-confirm re-ran: 72 pairs moved onto the map.

**Committed:** ae04b20a carries the day's scripts/reports/glossary; the bench
chart fix + final batch file additions are in the working tree, uncommitted.
Nothing pushed beyond origin's prior state unless Chris says push.

**PASTE 1 APPLIED by Chris (verified live):** catalog labels fixed, reader
grants in — live tests went 85 failures → 7 → after grants, only the 7
connect-layer/build-role ones remain. Wire-confirm now excludes the 1,139
MACRO pairs automatically: honest picture is 691 judgeable, 214 wired (31%).

**PASTE 2 APPLIED by Chris, verified:** edge table 4,908; wire-confirm now
57 direct / 171 one-hop of 691 judgeable. Test failures down to ONE (the
incremental backstop test, which needs the build role by design — expected
under reader creds, not a defect).

**PASTE 3 APPLIED, verified:** edge table 4,910; the whole federal court
family (civil, criminal, appellate) now hangs off the docket bridge; 17 more
queue pairs moved onto the map (off-spine 246→229). Bankruptcy stays refused
at 33%. The commented secondary-roles security fix still awaits Chris's
yes/no ("lock the key").
(2) Carried: 5th false-reading for the RIPPLES doc; healthcare pilot weak
signal; lens-catalogue sweep ($42–64) still awaiting go.

**NEXT (natural ticks):** wire-confirm triage awareness is DONE (this
session); still open: GEO-tier edges for the 6% state-keyed pairs; politics
roll-call scope ruling (above); per-entity drift; Indiana nursing-penalty
dead-air context; FJC criminal/appellate/bankruptcy docket wires (same
crosswalk pattern as the civil courts bridge).
