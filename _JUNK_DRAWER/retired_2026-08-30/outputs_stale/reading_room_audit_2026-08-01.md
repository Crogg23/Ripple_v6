# Reading Room Contents Audit — 2026-08-01

Full-queue audit of LIBRARY_MARTS.REVIEW.LEAD_QUEUE (17,306 leads) run on the
RIPPLE_READER lane, zero writes anywhere. Method: structural sweep on 100% of
leads, adversarial re-verification per detector (attacking the mart's known
blind spots rather than re-running its own logic), stratified case-file
reading. All SQL batches preserved in the session scratchpad (rr_audit.py +
pass*.json).

## Scorecard

| Detector | Leads | Verification possible | Result |
|---|---|---|---|
| banned_but_paid | 773 | Full (3-source + timeline) | Clean except 6 name-conflict leads + mojibake (below) |
| excluded_but_billing | 236 | Partial (no billing-year in Part D) | Clean |
| banned_but_operating | 10 | Full (live recompute vs frozen evidence) | 9/10 match; 1 undercounts (below) |
| debarred_but_funded | 53 | Partial (SAM activation dates all blank) | 53/53 UEIs still in SAM; totals clean |
| sanctioned_vessel_broadcasting (v1) | 4 | Full | 4/4 duplicate v2 leads — retire |
| sanctioned_vessel_broadcasting_v2 | 12 | Full | 12/12 in sanction lists + AIS; all broadcast under different names (disclosed in headline — that's the story) |
| sec_filer_in_irs_bmf | 3 | Full | 3/3 reconfirmed in both source tables |
| osha_cohort_outlier_2024 | 16,215 | Arithmetic + shape (inputs self-reported) | 0 arithmetic errors in 15,220 rejoinable rows; see EIN drift + flat scoring |

Confirmed clean across the board: queue↔safe-view parity exact (0 orphans
either direction), evidence arrays present and count-consistent on all 17,306
leads, all key formats valid (no sentinels/all-zero), no epoch-1970 or future
dates anywhere, zero reinstated providers in the queue (LEIE REINDATE is 100%
sentinel '00000000' — reinstatement is only detectable via row-vanishing, i.e.
the LEIE_ROW_MISSING tier, currently 0).

## Flagged — the worklist

### F1. Encoding corruption in every em-dash text field (systemic, cosmetic-but-everywhere)
Every string the mart built from a template containing an em-dash is stored as
mojibake (`â€”`): 792 headlines (all 773 banned_but_paid, all 16 vessel, all 3
sec_filer) and **all 16,530 caveats**. Analysts see `totaling $71 â€” latest
payment` on screen. Root cause: dbt on Windows compiled the UTF-8
`lead_queue.sql` as cp1252. Fix is Chris-adjacent because headline wording is
pending the Checkpoint-1 edit anyway: either go ASCII-only in the model's
string literals or force UTF-8 for dbt (PYTHONUTF8=1), then rebuild
`marts.review` (gated on the A00 write PAT).

### F2. OSHA priority is flat — 94% of the queue is unranked
All 16,215 OSHA leads score exactly 3.25, so their priority_rank is lead_id
order — meaningless. The extreme tail (132 leads at >15× cohort rate, max ~62×)
sorts no higher than a 2.0× case. Fix: feed `fold_vs_pooled` (already in
evidence) into the score. Weights are draft v1 / Checkpoint-1 territory —
Chris's call on the shape, the wiring is green-lane.

### F3. Retire the 4 v1 vessel leads
All 4 `sanctioned_vessel_broadcasting` leads cover IMOs also present as v2
leads. Pure duplicates of a detector the caveat itself marks SUPERSEDED.

### F4. Six FACT_GRADE leads with hard first-name conflicts
Tier logic corroborates on surname only. These six have completely different
first names in LEIE vs NPPES (different first letter, not initials):
LEAD_bf68b61ba848c978 (Kyung/William Yu), LEAD_71aa91d2a5d77925 (Keith/Chi Fei
Chung), LEAD_2a4c19accfcae63a (Duttala/Obul Reddy), LEAD_e967a2f807fcd12e
(Seyed/Hamid Tofigh), LEAD_e58f0cadae4a42cc (Brian/Cuong Bui),
LEAD_0ca589a84e35bb4b (Gibson/Chuma Osuji). Reading them, most look like
same-person alternate/anglicized names, and all have trivial payment totals
($13–$256) — but "FACT_GRADE_3_SOURCE" oversells the corroboration and the
conflict is invisible in the case file. Suggest surfacing the first-name pair,
or a first-initial check in the tier logic.

### F5. Frozen facility evidence now provably stale for 1 of 10 leads
Live recompute against the restored FED_CMS_FACILITY_AFFILIATION:
LEAD_181e668dfbe08b9a (NPI 1184685281) shows 3 facilities frozen vs 6 live —
the headline undersells it. Other 9 match exactly. The caveat already promises
a live recompute is pending; the table is back, so the mart can drop the
frozen path.

### F6. OSHA lead keys don't rejoin to their own source on EIN (995 leads, 6%)
The `EIN|EST_KEY` key's EIN half fails to match the raw 300A table for 995
leads — establishment_id matches, EIN doesn't (leading-zero / normalization
drift between detection-time key and today's raw column). Arithmetic on the
matched 15,220 was perfect (0 rate or case-count errors), so this is key
hygiene, not math. Normalize EIN the same way on both sides.

### F7. 96 OSHA leads carry physically implausible DART rates (>50)
Max observed ~85 (a NY hospital: 38 DART cases in 89k hours). Almost certainly
employer data-entry errors (hours understated or cases overstated) — the
self-reported caveat covers it, but a rate ceiling or "implausible" flag would
keep them from masquerading as the best leads once F2 fixes ranking.

### F8. 179 people appear in multiple detectors
1,019 NPI leads across only 831 distinct NPIs. Not a defect — different claims
about the same person — but the front end should group by entity or Chris
reviews the same person up to three times.

### F9. Stale docs
reading_room/README.md says "~1,030 leads" (real: 17,306 — OSHA landed since);
lead_queue.sql/yml call sec_filer_in_irs_bmf "dormant, 0 leads" (real: 3).

## What this audit could NOT verify (honest limits)
- OSHA inputs are self-reported Form 300A — arithmetic verified, truth not verifiable from this warehouse.
- debarred_but_funded timelines: SAM ACTIVATION_DATE blank on all rows — "funded after debarment" remains unprovable.
- excluded_but_billing timelines: Part D has no program-year column.
- AIS is the fixed Jan 1–8 2024 snapshot — vessel "activity" is historical presence only (caveats already say so).
- Decisions table is empty (nothing reviewed yet), so decision-suppression logic is untested against real data.
