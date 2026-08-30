---
name: feedback-pre-response-checks
description: "2026-08-18 — silent 8-point checklist added to the per-prompt hook (specificity, contradiction, real intent, confidence, repackaging, scope-creep, defensibility, dead-weight); runs before every open-ended/analytical answer, never shown to Chris"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 75ddcc17-4310-418a-a376-5a723352377c
  modified: 2026-08-18T16:23:17.239Z
---

Every open-ended or analytical response now runs an 8-point silent checklist before sending, wired into [[interaction-contract]]'s per-prompt hook (`.claude/contract-reminder.md`), alongside [[feedback-breadth-first-surface-pass]] and [[feedback-two-knobs-not-one-blanket-brief]].

The 8 checks: specificity (would this answer fit any other conversation — if yes, rewrite with real project specifics), contradiction (does this drift past something already established in-session/STATUS.md/memory — flag it, don't drift), real intent (literal words vs. what Chris probably meant — state the gap, let him correct), confidence (fact vs. inferred/assumed/guessed — label it), repackaging (new info or Chris's own words dressed as insight — cut if repackaged), scope-creep (did I quietly answer an easier version of the ask), defensibility (can every claim survive a challenge right now), dead-weight (does this caveat change what Chris does — if not, cut it).

**Why:** Chris runs Ripple solo and burnt out — he needs every answer optimized for that reality, not generic-playbook or padded. The confidence check is directly named for the pension-table incident: stating "I looked and it's not there" as fact without saying where/how was verified.

**How to apply:** These are silent checks, not visible process — they change the content and shape of the answer, never add "let me check my checklist" narration or preamble. Applies to open-ended/analytical responses specifically, not every mechanical task-status update.
