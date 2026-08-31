# Wire-confirm, region fix, and the first wave-break traces (2026-08-21, late)

Three deepenings of the day's time-interaction work, run back-to-back on
Chris's "go for all." Warehouse cost: small read-only aggregates throughout.

---

## 1. Wire-confirm — the lead-lag queue meets the spine

Script: `scripts/ripples/wire_confirm_pass.py`
Raw: `reports/ripples_wire_confirm_2026-08-21.json`

The 1,830 co-moving stream pairs were checked against the live connection
graph (4,899 edges, rebuilt 2026-08-18):

| bucket | pairs |
|---|---:|
| direct wire between the two tables | 54 (22 on hard IDs) |
| wired at one remove via a shared third table | 158 (8 hard the whole path) |
| both on the spine, no wire | 134 |
| **at least one table not in the spine at all** | **1,484 (81%)** |

**The 81% is landmine 3 measured for real:** most of what co-moves cannot
be judged, because most time-streams touch tables the spine has never
wired. The wiring gap, not the statistics, is now the binding constraint on
the whole lead-lag program.

Of the hard-wired survivors, almost all are sibling tables of one source
system (the drinking-water family, the campaign-finance family, the IRS
revocation twins) — they co-move because they are one machine, which
validates the method (it finds real plumbing unprompted) but adds no new
story. **One genuinely new candidate:** federal research-grant activity
leading charity e-filings by ~9 months over a hard EIN-to-UEI bridge —
plausible (grant money -> nonprofit paperwork), queued for a human look.

## 2. The region fix — inspector's calendar vs. owner's behavior, settled

Script: `scripts/ripples/neighbor_spike_rule.py` (same-state control added)
Raw: `reports/ripples_neighbor_rule_regionfix_2026-08-21.json`

The same-owner co-spike gap, now against BOTH controls:

| domain | vs strangers anywhere | vs strangers in the SAME STATE | verdict |
|---|---:|---:|---|
| mine safety | +34.4% | **+21.8% (z 41.8)** | survives strongly — ownership signal is real |
| nursing homes | +12.7% | **+5.9% (z 9.9)** | survives, halved — about half WAS the inspector's shared calendar |
| toxic release sites | +12.2% | **−9.2%** | DEAD as an ownership story — same-state strangers co-spike MORE than same-owner siblings; the signal was geography/regional enforcement all along |

This is the rule working as designed: the confound was measured, not
assumed, and it rewrote one of three headlines. The environment result
should never again be quoted as an ownership pattern.

## 3. First wave-break traces (flow ladder Box 5, first bites)

Three harm->consequence hand-offs, each measured with a coverage check
first (which caught a false finding — see the correction note below).

**Drinking water: violation -> any enforcement.** Nationally healthy,
97–99% every year since 2000. The break is territorial and state-level
(2019–2024 window): American Samoa 39%, Northern Marianas 74%, Puerto Rico
77%, Wyoming 85%, Florida 85% — against a 98% national norm. The wave
flows almost everywhere and visibly dies in the territories.

**Mine safety: violation -> penalty -> payment.** No break: ~98.6%
penalized, 92–96% of penalized violations paid, stable for 13 years. The
2025 payment dip (87%) is the not-done-yet tail, not a change.

**Nursing homes: actual-harm deficiency -> any penalty within 18 months.**
CORRECTION FIRST: the first run said 62% nationally with Ohio at 42% —
wrong. The penalty file only covers June 2023 onward (a rolling CMS
window), so older surveys could not find their fines by construction; the
defensibility check caught it before it left the session. On the honest
window (surveys 2023-07 to 2024-11, whose full 18-month follow-up sits
inside penalty coverage): **85.9% nationally; the real laggards are
Indiana 54%, Ohio 75%, California 78%** (min 100 harm surveys). A
one-in-two chance of no fine after an actual-harm finding in Indiana is a
genuine break candidate — needs the state-agency context before a human
reads it as negligence.

---

## Standing limits

- All three chains join on hard IDs; no name-matching anywhere.
- "No penalty in the file" and "no penalty" are different claims — every
  break number above is a floor bounded by that file's coverage, now
  checked per file.
- Per resolution doctrine: everything here is measurement, not finding;
  human sign-off gates any external use.
