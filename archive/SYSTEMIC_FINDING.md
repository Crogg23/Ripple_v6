# SYSTEMIC FINDING — sba-7a-cliff-migration
VERIFIED_AT: 2026-07-13T21:45Z (all queries run live this session, role RIPPLE_READER, warehouse SERVE_WH)
GRADE: FACT (the migrating-bunching pattern and its alignment to the rule calendar) — with the attribution caveats in §4/§8 carried as part of the finding
ER_DEPENDENT: NO (headline mechanism lives inside one table; one secondary sub-check is ER-caveated and labeled)
NOVELTY: CHECKED — bunching at SBA fee/guarantee thresholds is a known class in the economics literature (Bachas–Kim–Yannelis documented it at the historical $150k line). No published analysis found (searched 2026-07-13) of the FY2022–26 waiver-cutoff **migration** at $350k/$500k/$1M/$2M. Known class, apparently-unpublished instance.

Data: `LIBRARY_RAW.LANDING.FED_SBA_LOANS` (2,174,502 rows, SBA 7(a)+504 FOIA file, single clean load, ASOFDATE 3/31/2026). All analysis: `TRIM(PROGRAM)='7A'`, `TRY_TO_NUMBER(GROSSAPPROVAL,18,2) > 0`, APPROVALFY 2019–2026.

---

## 1. MECHANISM (one sentence)

Because SBA's 7(a) rules put a cost-or-procedure cliff at a specific loan size that moved almost every fiscal year — zero-upfront-fee cutoffs at ≤$350k (FY22), ≤$500k (FY23), ≤$1M (FY24–25), a fee step at $2M (FY24 only), and streamlined-underwriting/program-cap cutoffs stacked at $350k/$500k — borrowers and lenders size loans to sit at or just below the currently-active cliff, which appears in `FED_SBA_LOANS` as below/above mass asymmetry in a ±$20k window that **migrates with the cliff**: appearing when a rule arrives at a line, and collapsing when it leaves.

Rule sources (verified 2026-07-13 against SBA notices 5000-818641 / FY23 schedule / 5000-848801 / 5000-858936 / 5000-872051, CRS R41146, SOP 50 10 7/8):

| FY | Zero-upfront-fee cutoff | Other cliffs at these lines |
|---|---|---|
| 2019–21 | none (FY21: universal Economic Aid Act waiver — no cliff, but contaminated era) | Express cap $350k (FY19–20, part 21) |
| 2022 | ≤ $350,000 | Express cap moves to $500k (permanent) |
| 2023 | ≤ $500,000 (then 0.55%→$700k, 1.05%→$1M, 3.5/3.75% >$1M) | fee **step** at $1M; 7(a) Small cutoff $500k from Aug 2023 |
| 2024 | ≤ $1,000,000 (1.45/1.70% $1–2M, 3.5/3.75% >$2M) | fee step at $2M (this year only); annual fee 0 ≤$1M |
| 2025 | ≤ $1,000,000 (3.5/3.75% >$1M) | annual fee 0 ≤$500k; SOP 50 10 8 (Jun 2025) moves Small cutoff back to $350k |
| 2026 | none (tiers 2/3/3.5/3.75% at $150k/$700k/$1M) | Small cutoff $350k |

## 2. PREDICTION / COUNTER-PREDICTION

If the mechanism is real: below/above asymmetry at each line should be elevated **exactly in the fiscal years that line carries a cliff** and at baseline otherwise; control round numbers that never carry a rule should stay flat across all years; the response should survive removing mechanically-capped products (SBA Express); and the at-line population should be the same product as just-above, merely re-sized.

If it's an artifact: round-number asymmetry would be era-stable (rounding doesn't read fee notices); control lines would move with the treated ones (pipeline/coverage shift); the asymmetry would be confined to capped products (rule restated); or the counts wouldn't reproduce.

Three predictions were tested blind this session (values never looked at before the test): the $350k line should spike in FY22 only (it did: see §4 row 1); FY26 should collapse at $500k/$1M (it did); and after the SOP 50 10 8 fact was found, the FY26 $350k re-spike was checked against the null design (it re-appeared exactly when the underwriting cutoff returned).

## 3. PROOF

Master table — my query, reproduced cell-for-cell by an independent re-derivation with separately-written SQL (zero discrepancies in 64 cells + 8 totals):

```sql
WITH loans AS (SELECT APPROVALFY fy, TRY_TO_NUMBER(GROSSAPPROVAL,18,2) g
  FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS
  WHERE TRIM(PROGRAM)='7A' AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) > 0
    AND APPROVALFY BETWEEN '2019' AND '2026')
SELECT fy, COUNT(*) n_total,
 COUNT_IF(g>330000 AND g<=350000) b350, COUNT_IF(g>350000 AND g<=370000) a350, COUNT_IF(g=350000) at350,
 COUNT_IF(g>480000 AND g<=500000) b500, COUNT_IF(g>500000 AND g<=520000) a500, COUNT_IF(g=500000) at500,
 COUNT_IF(g>980000 AND g<=1000000) b1000, COUNT_IF(g>1000000 AND g<=1020000) a1000, COUNT_IF(g=1000000) at1000,
 COUNT_IF(g>1980000 AND g<=2000000) b2000, COUNT_IF(g>2000000 AND g<=2020000) a2000, COUNT_IF(g=2000000) at2000
FROM loans GROUP BY 1 ORDER BY 1;
```

Below/above ratio (window (L−20k, L] vs (L, L+20k]) by FY. **Bold** = a cliff was in force at that line that year:

| Line | FY19 | FY20 | FY21 | FY22 | FY23 | FY24 | FY25 | FY26* |
|---|---|---|---|---|---|---|---|---|
| $350k | 7.2 | 6.7 | 4.7 | **16.2** | 7.7 | 3.1 | 4.9 | **14.6** |
| $500k | 1.9 | 2.1 | 2.5 | 2.8 | **6.9** | **13.4** | **14.7** | 4.7 |
| $1M | 3.2 | 3.4 | 3.9 | 2.8 | **12.6** | **24.3** | **10.2** | 2.8 |
| $2M | 4.4 | 4.1 | 3.5 | 3.2 | 5.1 | **26.5** | 3.8 | 4.2 |

*FY26 is a partial year (26,467 loans through the 3/31/2026 snapshot's coverage) — provisional.

- Treated: the 8 cliff-year line-FY pairs above. Observed mass in treated below-windows = 13,221 loans; expected under the null (FY19–21 mean share of each window, projected on treated-FY volume) = 6,957. **Ratio 1.90× null.**
- Control: six centers that never carry a rule (400k/600k/750k/800k/900k/1.5M, plus skeptic's independent 300k/450k/650k/1.25M): ratio-of-ratios vs their own FY19–21 baseline never exceeds 1.52 (author's set) / 2.9 absolute (skeptic's set), with no rule-year spikes. Treated ratio-of-ratios: 2.91–6.94. **No overlap.**
- Effect size (cleanest single instrument, $2M — no cap, no underwriting rule, no other threshold ever at that value): 26.5× in FY24, the only year a fee step sat there, vs 3.2–5.1× in every other year.
- Dose-response: when the waiver died (FY26), non-Express bunching at $500k collapsed 11.5× → 2.0× and the $1M ratio fell to its FY19 level (2.8).
- The response survives excluding SBA Express entirely (its $500k cap is mechanical: zero Express loans above $500k): non-Express $500k ratio 1.57 (FY22) → 4.09 (FY23, waiver arrives) → 9.43 (FY24) → ~11.5 (FY25) → 2.0 (FY26). SQL in Appendix C.2.
- The shape is a plateau **level shift**, not a round-number spike: at $1M in FY24, median of $10k bins 2–9 below vs 2–9 above (adjacent bins excluded) = 2.65, vs 1.26 in FY20 control. SQL in Appendix C.3.
- Economic stake (why actors move): crossing $1M in FY24 cost a median $11,571 in upfront fee (1.45% × the 75% guaranteed portion) vs $0 at exactly $1M — a ~23% effective surcharge on the marginal $50k of borrowing. The corroborating "hole" sits just above the line: 381 loans in ($1M, $1.1M] vs 551 in ($1.1M, $1.2M]. SQL in Appendix C.4.

## 4. GAUNTLET

| Killer | Test run | Result |
|---|---|---|
| 1. Is it the rule (cap restated / rounding)? | Blind $350k era test; product mix at $500k; above-line population at $1M; plateau-shift vs spike (App. C.1–C.3) | **PASSED.** Express-cap years (FY19–21, cap AT $350k) show baseline ratios (~1.5 excl-at-line); the spike (3.85 excl-at-line, 16.2 incl) lands only in FY22, the fee-cliff year. At-line $500k mass is 64% un-capped PLP. Thousands of loans sit above $1M every year (nothing caps there). FY24 $1M is a level shift (2.65 vs 1.26 control), not a spike. Round-number mass is real but era-stable — it cannot migrate. |
| 2. Is it the pipeline? | Load provenance; exact-dup tuples; per-FY counts | **PASSED.** One `_SOURCE_RUN_ID`, one SHA-256, one `_INGESTED_AT`, one ASOFDATE (3/31/2026). Dup tuples 0.32% (small-dollar fintech repeats), near-absent in cliff windows. All eras come from the same single file — a load artifact cannot produce a temporal migration. |
| 3. Is it the schema? | Parse health; FY-from-date consistency; code stability; guaranty-share mix | **PASSED.** Zero GROSSAPPROVAL parse failures; APPROVALFY matches the Oct–Sep FY derived from APPROVALDATE for 100% of rows; PROCESSINGMETHOD/SUBPROGRAM labels stable FY19–26; guaranty mix evolves smoothly except the documented FY21 CARES 90% episode. |
| 4. Is it the base rate? | 6 + 4 control centers × 8 FYs, ratio-of-ratios (App. C.5) | **PASSED.** Controls max 1.52 (ratio-of-ratios) vs treated 2.91–6.94 — clean separation, no overlap, and no control spikes in a rule year. Mild secular drift at 400k (→1.9 by FY25) is an order of magnitude short of treated. |
| 5. Is it entity resolution / grain? | Tuple uniqueness; same-day multi-rows at the cliff | **PASSED.** 99.53% unique on (BORRNAME, APPROVALDATE, GROSSAPPROVAL, BANKNAME); zero exact dups on either side of the FY24 $1M window; the headline arithmetic uses only GROSSAPPROVAL + APPROVALFY — no matching anywhere. |
| 6. Is it coverage? | Status/maturity/revolver mix by FY; >$5M scan | **PASSED.** No status class exists only in some FYs; excluding cancelled loans makes the FY24 $1M ratio slightly larger (25.6); ≤12-month-maturity loans (different fee rule) are <1.1% and don't move the ratio; zero loans above the $5M statutory max; revolvers are UNDER-represented at the line (7.7% vs 30.3% FY-wide). |
| 7. Is it already known? | Web search (2026-07-13): SBA bunching literature + FY23/24 waiver coverage | **PASSED with label.** The class is known (Bachas–Kim–Yannelis at the historical $150k guarantee/fee lines). No published quantification of the FY22–26 waiver-cutoff migration found. Also confirmed in-repo: PR #48 and Lead 6 cover USASpending SAT bunching — different dataset, different rule; no overlap. |

Adversarial pass (three hostile skeptics, same warehouse, §5F): all three report the finding survives. The re-deriver reproduced every number exactly from independently-written SQL. The alternative-story hunter refuted macro drift (the size distribution shifted LEFT during peak bunching years) and lender-mix (migration survives excluding the top-3 at-line lenders: $500k ex-3 ratios 2.9→6.7→10.7→10.1→4.3), and resolved both admitted puzzles as corroboration: the $1M-FY23 "no below-excess" is the predicted signature of a fee *step without a waiver* (above-side collapses 95→38 while the pile-up goes to the actual zero-fee line at $500k, 835→1,615), and FY25's $1M above-window share (0.092%) is still roughly half the FY19 baseline (0.177%) — the cliff still binds. The stakes auditor found the notch math strengthens the claim and that fee-splitting (ER-caveated name+zip check) **declined** under the waivers (67.6 → 44.1 bps of borrowers), so the behavior sits on the legal margin.

**Required attribution widening (part of this finding, not a footnote):** the migrating component is the fee schedule, and it is cleanly identified at $500k (FY23 timing — ten months before the underwriting cutoff moved there), $1M, and $2M. The $350k line is multi-caused (round-number magnet + Express-cap legacy + 7(a) Small underwriting cutoff, which returned to $350k in June 2025 and produced the FY26 re-spike). Small marginal tier steps do NOT bunch (the new FY26 $700k 3%→3.5% boundary shows ratio 1.30, inside its historical 1.2–1.8 band): the mechanism is **zero-fee cliffs and large steps**, not any fee boundary whatsoever.

## 5. CLASS OF CASES

Pre-registered sizing (logged before results computed): numerator = observed minus expected loans in (L−20k, L], expected = mean FY19–21 share of that window × treated-FY volume. Denominator = all 7(a) approvals in the treated FYs.

| Treated line-FY | Observed | Expected (null) | Excess |
|---|---|---|---|
| $350k · FY22 | 2,453 | 2,070 | **+383** |
| $500k · FY23 | 1,615 | 824 | **+791** |
| $500k · FY24 | 2,885 | 1,010 | **+1,875** |
| $500k · FY25 | 4,008 | 1,122 | **+2,886** |
| $1M · FY23 | 480 | 481 | ~0 (response = above-side collapse, see §4) |
| $1M · FY24 | 752 | 589 | **+163** |
| $1M · FY25 | 737 | 655 | **+82** |
| $2M · FY24 | 291 | 205 | **+86** |

- **Numerator: ≈ 6,265 excess loans** parked in the 20k windows below active cliffs, FY22–25.
- **Denominator: 253,360** 7(a) approvals FY22–25 (could all have been sized anywhere).
- **Rate: 2.47%** of all 7(a) approvals in the treated years; treated windows hold **1.90×** their null-expected mass.
- Expected under null: 6,957 loans in those windows; observed 13,221.
- Back-of-envelope dollar scale (labeled estimate, not a query result): ~6,300 loans × ~$0.5–1M ≈ $3–5B of loan volume sized to rule lines.
- These are **floors**: every control-era contamination (Express cap at $350k in FY19–21, at $1M during FY21; universal FY21 fee waiver) inflates the baseline and shrinks measured excess, and the below-window numerator doesn't count above-side collapse (the entire $1M-FY23 response) at all.
- Query: the master SQL in §3 (all cells), arithmetic as stated. FY21-contamination caveat: the skeptics recommend never using FY21 alone as control; the pre-registered FY19–21 mean was kept because the contamination is conservative in direction.

## 6. RECEIPT (one case)

Selection rule applied: **MEDIAN** (pre-registered in PROGRESS_LOG at 20:48Z, before the gauntlet finished: median GROSSAPPROVAL of the FY24 (980k, $1M] class → exactly $1,000,000 (median verified by query); tie-break earliest APPROVALDATE then alphabetical BORRNAME; must be fully populated).

Entity (identifier): **Montrose Deli, Inc., Mount Prospect, IL — $1,000,000 7(a) loan via Byline Bank, approved 10/1/2023.** (The 7(a) FOIA file carries no EIN/UEI; the row is uniquely identified by the tuple BORRNAME + APPROVALDATE + GROSSAPPROVAL + BANKNAME, which is 99.53% unique in this file and unique for this row.)

The case, in five sentences: A grocery business in suburban Chicago borrowed exactly $1,000,000 — to the dollar — on the first day of fiscal year 2024, the day SBA's zero-fee cutoff moved from $500,000 up to $1,000,000. At $1,000,001 the loan would have owed roughly $10,900 in upfront guaranty fee (1.45% of the $740,000 guaranteed portion); at $1,000,000 it owed nothing. It is a standard Preferred Lenders Program guaranty loan — 120-month term, 11.25% initial rate, 90 jobs supported, currently in regular servicing — statistically indistinguishable from the loans sitting just above the line except for its size. It is the *median* member of the 752-loan class that landed in the $20k window under the cliff that year, not an outlier: 485 of those loans sit at exactly $1,000,000. Nothing about this loan is improper — that is the point of the finding: the rule moved, and the market's loan sizes moved with it, ~6,300 times.

```sql
SELECT MEDIAN(g) FROM (SELECT TRY_TO_NUMBER(GROSSAPPROVAL,18,2) g
 FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS
 WHERE TRIM(PROGRAM)='7A' AND APPROVALFY='2024'
   AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) > 980000 AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) <= 1000000);
-- returns 1000000.00000

SELECT BORRNAME, BORRCITY, BORRSTATE, BANKNAME, APPROVALDATE, GROSSAPPROVAL, SBAGUARANTEEDAPPROVAL,
       PROCESSINGMETHOD, SUBPROGRAM, TERMINMONTHS, NAICSCODE, INITIALINTERESTRATE, JOBSSUPPORTED, LOANSTATUS
FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS
WHERE TRIM(PROGRAM)='7A' AND APPROVALFY='2024' AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2)=1000000
  AND TRIM(COALESCE(BORRNAME,''))<>'' AND TRIM(COALESCE(BANKNAME,''))<>''
  AND TRIM(COALESCE(APPROVALDATE,''))<>'' AND TRIM(COALESCE(NAICSCODE,''))<>''
ORDER BY TRY_TO_DATE(APPROVALDATE,'MM/DD/YYYY') ASC, BORRNAME ASC LIMIT 1;
```

## 7. WHAT WOULD FALSIFY THIS

1. A future FY whose fee schedule places a zero-fee cliff at a new value with **no** bunching migration to it within the year (the FY26 $350k underwriting return and the FY24 $2M step both confirmed on schedule; a clean miss would break the pattern).
2. Evidence that SBA's FOIA extract re-states GROSSAPPROVAL after approval (e.g. recording post-approval increases) in a way correlated with fiscal year — this would poison the era comparison. (Checked indirectly: single snapshot, parse-clean, FY-date mapping 100%; a definitive check needs SBA's raw E-Tran approvals.)
3. A lender-side product catalog showing that "$1M loan" products existed at scale before FY24 with the same at-line share — i.e., proof the at-line mass predates the incentive (the exact-hit series 55/74/122/118→206→341/436→164 per 10k loans says otherwise).
4. Reproduction failure: any of the §3 numbers not reproducing from the verbatim SQL against `FED_SBA_LOANS` (independently reproduced once already this session).

## 8. WHAT I COULD NOT VERIFY

- **Who moves — borrower or lender.** The data cannot distinguish borrowers trimming their ask from lenders steering loan sizes (marketing "$1M no-fee" products). The mechanism statement covers both; the lender-concentration analysis (Northeast Bank 0→510 at-line, ReadyCap 43→438) shows lenders *amplify* but don't create the pattern.
- **Annual-service-fee schedules for every year** were verified only for FY23–26; FY19–22 annual tiers were not independently confirmed (upfront-fee cutoffs, which carry the finding, were all verified against primary notices).
- **Whether SBA enforced the 90-day aggregation rule** on the ~510 FY24–25 exact name+zip split-pattern borrowers (ER-CAVEAT: exact-string match, no EIN in file; misses affiliates and name variants; the *rate* declined under the waivers, direction robust).
- **FY26 completeness** — partial year (26,467 loans at the 3/31/2026 snapshot); all FY26 numbers provisional.
- **The receipt case's motive.** Montrose Deli's loan is consistent with fee-aware sizing; no document proves intent. The finding is about the class, not the case.

---

## Appendix A — The funnel (for the record)

Candidates generated (14): Form 5500 100-participant audit bunching · OP NPI-missingness by manufacturer · OP third-party routing · FEC itcont employer-missingness · SBA 7(a) cliff migration · PPP $2M safe harbor · FEC IE 24/48-hr lateness · clinical-trials FDAAA lateness · HMDA partial exemption · FFIEC $10B Durbin bunching · NSF end-of-FY · FCA relator-share bunching · EPA ECHO FY-end inspections · USASpending Sept surge.

Killed at probe/triage (with killer): 5500 (flat histogram 85–115, no signal) · OP NPI-missingness (max 0.6% — CMS validation works) · OP third-party (disclosure working as intended) · IE lateness (bulk file can't separate 24/48-hr reports from scheduled filings — schema) · clinical trials (500-row sample) · HMDA (28k-row 2022 slice) · FFIEC (302 rows, dead scrape) · NSF (125 rows) · FCA (19 rows) · ECHO (snapshot grain, no event dates) · USASpending Sept surge (known lit + mined table).

Entered the Gauntlet (3): **SBA cliff migration — SURVIVED (this file)**. **PPP $2M — killed by killer #7**: data-side tests passed, but the pooled exact-$2M spike decomposed to 96.7% second-draw statutory cap (mechanical), leaving a modest first-draw excess (1.32 vs 1.04 at the $3M control) that is already published — replication value only. **FEC employer-missingness — survived data killers, demoted to secondary hypothesis** (Appendix B) on partial novelty.

## Appendix B — Secondary hypothesis (survived the gauntlet, not the headline)

GRADE: HYPOTHESIS · ER_DEPENDENT: NO · NOVELTY: partially known (2019–20 CLC complaints / journalism on Trump-committee employer disclosure; this 2023–25 committee-level measurement appears fresh).

On $200+ direct, non-memo, type-15 receipts — exactly where the FEC best-efforts rule (11 CFR 104.7) applies — non-conduit committees show 10–40% blank donor EMPLOYER, vs ~1–2% for conduit platforms and a misleading 3.17% pooled baseline: SEAL PAC 39.9%, Trump National Committee JFC 34.6%, SFA Action 33.5%, Senate Conservatives Fund 33.1%, Never Surrender 26.8%, DNC 19.8%, Harris Victory Fund 19.2%, NRCC 19.1%. On 81–100% of those rows OCCUPATION is also blank (not "RETIRED" — the retiree convention is dead as an explanation). The original flagship (WinRed, 31.9%) was an artifact — 97.6% of its blanks are refund rows that are 100% blank by structure; on actual receipts WinRed is 1.10%, better than baseline. Caveat: best-efforts is legally satisfied by soliciting plus one follow-up, so these rates evidence collection failure, not automatically violations. Queries: gauntlet workflow journal (wf_2a07559e-1a6, agent G3), reproducible against `FED_FEC_INDIV_CONTRIBUTIONS` + `FED_FEC_BULK_COMMITTEES`.

## Appendix C — Supporting verbatim SQL (run this session; agent-run queries reproduced from workflow journals wf_2a07559e-1a6 / wf_9815f4ee-f14)

C.1 Blind $350k era test (G1:rule):
```sql
SELECT APPROVALFY,
 SUM(CASE WHEN g > 330000 AND g <= 350000 THEN 1 ELSE 0 END) below_incl,
 SUM(CASE WHEN g > 330000 AND g <  350000 THEN 1 ELSE 0 END) below_excl_at,
 SUM(CASE WHEN g = 350000 THEN 1 ELSE 0 END) at_350k,
 SUM(CASE WHEN g > 350000 AND g <= 370000 THEN 1 ELSE 0 END) above
FROM (SELECT APPROVALFY, TRY_TO_NUMBER(GROSSAPPROVAL,18,2) g
      FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS WHERE TRIM(PROGRAM)='7A')
WHERE g > 0 AND APPROVALFY BETWEEN '2019' AND '2026' GROUP BY 1 ORDER BY 1;
-- excl-at ratios: FY19 1.49, FY20 1.58, FY21 1.45, FY22 3.85, FY23 1.73, FY24 0.78, FY25 1.11, FY26 2.10
```

C.2 Non-Express $500k check (G1:rule; Express = name match or ~50% guaranty share):
```sql
SELECT APPROVALFY,
 SUM(CASE WHEN g > 480000 AND g <= 500000 AND NOT is_exp THEN 1 ELSE 0 END) below_nonexp,
 SUM(CASE WHEN g > 500000 AND g <= 520000 AND NOT is_exp THEN 1 ELSE 0 END) above_nonexp
FROM (SELECT APPROVALFY, TRY_TO_NUMBER(GROSSAPPROVAL,18,2) g,
       (PROCESSINGMETHOD ILIKE '%express%' OR SUBPROGRAM ILIKE '%express%'
        OR (TRY_TO_NUMBER(SBAGUARANTEEDAPPROVAL,18,2)/NULLIF(TRY_TO_NUMBER(GROSSAPPROVAL,18,2),0) BETWEEN 0.45 AND 0.55)) is_exp
      FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS WHERE TRIM(PROGRAM)='7A')
WHERE g > 0 AND APPROVALFY IN ('2022','2023','2024') GROUP BY 1 ORDER BY 1;
-- FY22 461/293 = 1.57; FY23 956/234 = 4.09; FY24 2027/215 = 9.43
```

C.3 Plateau shift at $1M, FY20 control vs FY24 (G1:rule):
```sql
WITH b AS (SELECT APPROVALFY fy, FLOOR(TRY_TO_NUMBER(GROSSAPPROVAL,18,2)/10000) bin, COUNT(*) n
 FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS
 WHERE TRIM(PROGRAM)='7A' AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) > 0 AND APPROVALFY IN ('2020','2024')
   AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) >= 900000 AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) < 1100000
 GROUP BY 1,2)
SELECT fy, MEDIAN(CASE WHEN bin BETWEEN 91 AND 98 THEN n END) med_below,
       MEDIAN(CASE WHEN bin BETWEEN 101 AND 108 THEN n END) med_above
FROM b GROUP BY 1 ORDER BY 1;
-- FY20: 61.5/49.0 = 1.26 · FY24: 83.5/31.5 = 2.65
```

C.4 FY24 $1M notch stakes + the hole above the line (S3:stakes):
```sql
WITH l AS (SELECT TRY_TO_NUMBER(GROSSAPPROVAL,18,2) g, TRY_TO_NUMBER(SBAGUARANTEEDAPPROVAL,18,2) guar
 FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS WHERE TRIM(PROGRAM)='7A' AND TRIM(APPROVALFY)='2024')
SELECT CASE WHEN g=1000000 THEN '1_exact_1M' WHEN g>980000 AND g<1000000 THEN '0_below'
            WHEN g>1000000 AND g<=1100000 THEN '2_above_1M_1.1M'
            WHEN g>1100000 AND g<=1200000 THEN '3_above_1.1_1.2M' END bucket,
       COUNT(*) n, ROUND(MEDIAN(0.0145*guar),0) med_fee
FROM l WHERE g>980000 AND g<=1200000 GROUP BY 1 HAVING bucket IS NOT NULL ORDER BY 1;
-- below 267 · exact-1M 485 · (1M,1.1M] 381 (med fee $11,571) · (1.1,1.2M] 551 (med fee $12,523)
```

C.5 Control-center matrix (G1:baserate + S1 independent set): six centers 400k/600k/750k/800k/900k/1.5M and four centers 300k/450k/650k/1.25M, same window design as §3 — max ratio-of-ratios 1.52; skeptic's absolute ratios 0.96–2.9, flat across FYs. Full SQL in workflow journals (same CASE-bucket pattern as §3 with the control center values substituted).

C.6 Splitting check, ER-CAVEAT exact BORRNAME+BORRZIP (S3:stakes): split-pattern borrowers (2+ loans ≤$1M within 90 days summing >$1M) = 67.6 bps of borrowers FY19–20 → 44.1 bps FY24–25. Full SQL in workflow journal wf_9815f4ee-f14.
