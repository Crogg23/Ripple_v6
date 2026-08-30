---
name: feedback-verify-done-claims-before-stating
description: "2026-08-27 crashout — declared \"depth is basically solved\" from one report's headline, then own sweep hours later found ~80x and ~14,000x truncations; never state \"you're good / done / solved\" until the check that could disprove it has actually run"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 89bc29c5-3610-45ad-ab1b-558f88cc7470
  modified: 2026-08-27T13:51:45.937Z
---

2026-08-27: Told Chris "depth is basically solved, you're good to move on" based
solely on the depth-triage report's headline — then his "make sure I'm not
missing anything" sweep immediately found: pension filings at 33k of ~2-3M
(~80x truncation), device injuries at 1,386 of ~20M, a loader stalled at 76%
for 5 days, and a whole never-finished FDA loader phase. The triage's method
(round-number flag only) had a documented blind spot I repeated without
checking. Chris: "stop giving me half-assed WRONG information... a third of
the picture. Lock the fuck in."

**Why:** A verdict like "you're done / it's solved / you're good" is a
green-light Chris acts on. Handing it over from a single artifact's summary —
without asking "what would this method have missed?" — is the same
repetition-isn't-verification failure as the stale registry notes and the
name-matched audit verdicts ([[audit-scripts-must-not-hardcode-verdicts]],
[[feedback-verify-inventory-before-computing]]). The prior artifact is a
sample of the possible, never the boundary of it.

**How to apply:** Before stating any completion/health verdict ("depth is
enough", "nothing is missing", "X is done"): (1) name the method that produced
the claim and its blind spot — a filter's misses are invisible by
construction (round-number flags miss odd-number truncations; name-greps miss
tests; typed-DATE scans miss real clocks); (2) run or commission the cheap
disconfirming check FIRST (e.g. "tables under 5k rows vs publisher size"), or
(3) if the check hasn't run, say "unverified — the sweep that would prove
this hasn't run" instead of the verdict. Never answer a yes/no green-light
question with confidence borrowed from someone else's summary.
