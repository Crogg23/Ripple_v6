---
name: stale-commands-are-live-ammo
description: "2026-08-09 incident — a queued demote command clobbered same-day rebuilds; re-verify any handed-off command against CURRENT state, and guard batch write-tools against acting on changed worlds"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 23b5ae7a-7c36-469b-92d9-94eaa7fa0af3
  modified: 2026-08-09T19:27:03.166Z
---

2026-08-09: I handed Chris a demote command (written when 19 sources were dead)
and told him it was "safe as-is" AFTER I had rebuilt 3 of those sources under the
same names that same day. The script demotes the LATEST success run per source
— so it buried the fresh 821k-row Irish CRO load, the CDC mortality grid, and the
VA all-cause rebuild. Caught and re-promoted within minutes, but Chris ruled:
"don't ever let a mistake like this happen again."

**Why:** a command is generated against a snapshot of the world; every action
between generation and execution can invalidate it. "It was safe when I wrote
it" is not safety. Especially deadly when a rebuild reuses a dead source's ID —
"latest run" flips meaning from junk to gold silently.

**How to apply:**
- Before handing Chris ANY queued/stored command (or re-running one), re-derive
  what it will touch NOW, not what it touched when written. If my own session
  changed the relevant state since, that's a mandatory re-check.
- Batch write-tools must carry state guards: `propose_dead_scrape_demote.py` now
  REFUSES latest-success runs that are big (>5k rows) or fresh (<7 days) — a
  dead scrape is by definition small and old. No override flag on purpose.
- When rebuilding a dead source, prefer reusing its source_id (history stays
  linked) but IMMEDIATELY treat every stale cleanup list naming that ID as
  poisoned.

Related: [[feedback-verify-agent-research-against-tests]] (same root: verify
against live state, not cached conclusions).
