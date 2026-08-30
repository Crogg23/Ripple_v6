---
name: feedback-breadth-first-surface-pass
description: 2026-08-12 crashout — breadth-first surface passes with a parking lot are now mandatory; depth-first diving is the banned failure mode; wired into the per-prompt hook
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f9ae8e11-5610-49a3-9670-51a0ef1f586a
  modified: 2026-08-12T20:53:55.396Z
---

Chris had to interrogate range out of a session three separate times in one
afternoon (harm findings → question shapes → cross-domain instruments → the
measurement grammar). Each push moved the answer up an altitude. He named the
failure himself: **"dipping a 5 gallon bucket in the ocean and then saying we
didn't catch a whale, must be nothing out there."**

**The method he wants, in his words: start from the tippy top.**
1. Simplest statement about a thing first — "number of X" — then every way X can
   be displayed/cut/expressed.
2. **Bright line:** a surface item uses only columns on the thing itself plus its
   own dimensions. Needs a second fact table, a different granularity, or a new
   thing → PARKED.
3. Park = write ONE LINE naming the branch, then return to the surface. Do not
   explore, evaluate, or solve it.
4. Cover every thing at the surface before deepening any of it.
5. **The parking lot is the prize** — a branch parked forty times across forty
   things is the ranked build list, by vote count instead of instinct.

**Why:** depth-first spends expensive effort before there's anything to compare
against, and it anchors on whatever got dived into first — the same bias the
whole exercise exists to defeat. Coverage is the deliverable, not answers.

**How to apply:** three altitudes on any open ask (literal / wider / ceiling) in
ONE message so he collapses it by picking. Caveats capped and at the END while
exploring; caveats are the whole job only when publishing. Before sending an
exploratory answer, check: is this the biggest true version of this? Never treat
a prior artifact (a question ladder, an old report) as the ceiling of what's
askable.

**Enforcement:** written into `.claude/contract-reminder.md`, which the
UserPromptSubmit hook injects on EVERY prompt, because this same feedback already
existed three times in memory ([[feedback-avoid-narrow-fixation]],
[[feedback-open-brief-means-range]], [[feedback-grilling-calibration]]) and did
not fire. Memory that only works when Chris enforces it is not a system.

Do NOT edit CLAUDE.md to add this — that file is Chris's ([[feedback-open-brief-means-range]]).
Related: [[warehouse-measurement-grammar-2026-08-12]]
