# Threshold-Bunching Detector — Innocent Explanations List

Written 2026-07-12, BEFORE any analysis query was run (Phase 0 recon only: table/column/grain
confirmation on `LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS`).

If a cliff appears at the center point, these are the boring reasons it could be there.
None of them are resolved here — this list exists so they can't be rationalized away after
a chart looks exciting.

1. **Rounding.** Humans price at round numbers. $250,000 is itself a round number, so mass
   at/just-below it can be round-number pricing with no connection to the line. (This is also
   why the control center is a round number — the control must absorb the same rounding
   behavior.)

2. **Officer authority limits.** Contracting-officer warrant ceilings are commonly set AT the
   Simplified Acquisition Threshold. Awards stopping there can be pure approval-chain procedure.

3. **Rule-change dates.** The SAT has moved over time ($100k → $150k in 2010 → $250k in
   2018–2020). A cliff at a stale value, or a smeared cliff, can be an artifact of mixing eras.
   Residual clustering at the OLD value ($150k) can persist from stale agency-internal rules.

4. **Award-type mix.** Different instruments (purchase order / delivery order / BPA call /
   definitive contract) have different natural size distributions — a cliff can be a
   composition effect. Purchase orders in particular are *capped* at the SAT by rule, so any
   pooled distribution has a mechanical cliff built in.

5. **Modifications vs. base awards.** The table is action-grain (6.33M rows, 5.72M distinct
   award keys): modifications and deobligations (negative amounts, min −$4.29B) sit in the same
   table as base awards. An unfiltered distribution is not a distribution of award decisions.

6. **Denominator / coverage.** Reporting rules differ by size: micro-purchases (≤$10k) largely
   ride purchase cards and are under-represented in FPDS; small actions can be reported in
   aggregate. The shape of the low end is partly a *reporting* shape.

Spotted in the data during Phase 0 (additions):

7. **Left-censoring (single-FY window).** The table covers exactly FY2025 (2024-10-01 →
   2025-09-30). The earliest visible action for an award key may actually be a *modification*
   of an award made before FY2025 — the true base action is outside the table. ~2.4% of
   "first actions" are negative and ~2.7% are zero, consistent with this.

8. **Bin-edge placement of exact-threshold awards.** "Not exceeding the SAT" means an award of
   exactly $250,000.00 is *within* simplified procedures. Whether the exact-value mass lands in
   the below-bin or above-bin changes the cliff ratio. (Handled by right-closed bins:
   ($245k, $250k] — stated, not hidden.)

9. **Same-day ties.** ~0.3% of award keys have multiple rows on their first action date; the
   tie-break rule (largest same-day obligation taken as base) shapes those few observations.

10. **Exclusion rules.** Dropping negative and zero base amounts is necessary but is itself a
    filter that shapes the distribution.

11. **Base obligation ≠ total value.** For delivery orders the base action obligation may fund
    only the first increment/year; the decision variable ("size of the order") is approximated,
    not observed.

12. **Subset-specific ceilings.** Some acquisition lanes have different ceilings (e.g.
    commercial products under FAR 13.5 up to $7.5M), so the population near $250k is a blend of
    lanes for which the line does and does not bind.

---

## Rule-out annotations (added after the 2026-07-12 calibration run)

Which of the above the data could and could not rule out. The list itself is unchanged.

| # | Explanation | Status after this run |
|---|---|---|
| 1 | Rounding | **Not ruled out — quantified.** Round-number spikes appear at $200k/$300k/$400k/$500k in the same distributions. Exactly-$250,000.00 awards are 294 of the 1,816 below-bin (16%); removing them leaves ratio 1,522/869 = 1.75, so the below-bin excess is not only the exact value. But: pointed at $500k (not a center in this test), the same single-bin metric returns 849/324 = 2.62 — *higher than at the real line*. The one-number metric cannot distinguish a large round number's shape from a line's shape. Documented detector limitation. |
| 2 | Officer authority limits | **Cannot be ruled out.** The table has no approving-authority column. |
| 3 | Rule-change dates | **Ruled out for this run.** Data spans exactly FY2025; the SAT was $250,000 for the whole span ($350,000 change effective 2025-10-01, after the data ends). Single era, no mixing. |
| 4 | Award-type mix | **Ruled out for this run** (single type: DELIVERY ORDER). Not ruled out for any pooled version of the detector. |
| 5 | Mods vs base | **Mitigated, not ruled out.** Earliest-action-per-key + positive-amounts filter applied; left-censoring (#7) means some residual mods remain. |
| 6 | Denominator / coverage | **Not ruled out**, but both windows sit far above the micro-purchase reporting zone and inside the same reporting regime, so it should hit both panels alike. |
| 7 | Left-censoring | **Cannot be ruled out with this table** (single-FY snapshot). Affects both panels equally. |
| 8 | Bin-edge placement | **Addressed by explicit rule** (right-closed bins), and quantified via #1. |
| 9 | Same-day ties | **Immaterial** (~0.3% of keys). |
| 10 | Exclusion rules | **Stated, not resolved** (negative/zero bases dropped: 2.4% / 2.7%). |
| 11 | Base obligation ≠ total value | **Not resolved.** Addressable later: CURRENT_TOTAL_VALUE_OF_AWARD exists in the table for a robustness rerun. |
| 12 | Subset ceilings | **Not resolved.** Addressable later: NAICS/PSC columns exist for lane splits. |

Note on the fire line: the metric definition (bin just below ÷ bin just above, right-closed
$5k bins) was fixed before the analysis queries ran. The numeric fire threshold (≥ 2.0 in the
harness) was set *after* seeing both values — it is provisional until more known positives and
negatives are run.

