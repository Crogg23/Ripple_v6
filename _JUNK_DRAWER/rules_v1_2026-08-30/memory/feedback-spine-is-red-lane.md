---
name: feedback-spine-is-red-lane
description: "ID spine is deprioritized (2026-08-29) — any spine-touching command is RED lane, ask first every time, even for routine-sounding asks like \"wire it up\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3eeac94-389f-4ecc-be3a-a1812c354077
  modified: 2026-08-30T07:19:47.678Z
---

Never run a spine-registering/reslicing command (`apply-config`, `connect spine`, `connect-one`,
`connect-changed`, or anything that touches the persisted entity spine) without asking Chris first —
no matter how bounded, dry-run-checked, or routine it looks.

**Why:** Chris decided 2026-08-29 the ID spine is deprioritized in favor of time/place joins, and that
he drives spine work step by step ([[time-and-place-are-joins]]). On 2026-08-30, "wire it up" — said
about the Join Handbook doc — got expanded into running the full staged spine batch (8 key families,
~2.8M rows). Chris had to shout STOP to kill it. The instruction was about a document, not the live
system, and the escalation from doc to spine happened silently.

**How to apply:** Any plain-English ask ("wire it up," "hook it in," "make it live," "connect it")
that could plausibly mean either "update this report/doc" or "touch the spine" — assume the smaller,
safer reading (the doc) unless Chris names the spine explicitly. If a task genuinely requires a spine
command, stop and ask, even after a clean dry-run. This is now flagged at the top of STATUS.md every
session so it can't be missed on boot.
