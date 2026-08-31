# Hunch Engine — Hand calibration on the hard-ID frontier (2026-08-01)

20 pairings scored live (seed 20260801, one distinct-join each on the read
lane; every pair measured the same way, graph edges used only as annotation).
Score: `S = log10((matched+1) / (E+1))`, `E = a_distinct × b_distinct /
KEY_DOMAIN[key]` — the independence null from the design note.

Frontier context: 148 hard-ID (STEEL/STRONG) pairs total, 120 already
verified by connect/ — the untested hard-ID frontier is only 28 pairs.
Sampled: 6 verified + 14 unverified.

| A | B | key | matched | E (chance) | S | coverage | verified |
|---|---|---|---:|---:|---:|---:|---|
| FED_CMS_OPEN_PAYMENTS | FED_CMS_OPEN_PAYMENTS_2023 | NPI | 714,130 | 91.0 | +3.89 | 76.4% | yes |
| FED_CMS_OPEN_PAYMENTS | FED_CMS_OPEN_PAYMENTS_2022 | NPI | 628,972 | 83.6 | +3.87 | 73.3% | yes |
| FED_CMS_FACILITY_AFFILIATION | FED_CMS_OPEN_PAYMENTS | NPI | 500,450 | 89.6 | +3.74 | 54.4% | yes |
| FED_CONGRESS_LEGISLATORS | FED_VOTEVIEW_MEMBERS | BIOGUIDE | 12,584 | 6.2 | +3.24 | 99.6% | yes |
| FED_CONGRESS_COMMITTEE_MEMBERSHIP | FED_GOVINFO_BILLSTATUS | BIOGUIDE | 528 | 0.01 | +2.72 | 99.1% | yes |
| FED_FAC_SINGLE_AUDIT | FED_SEC_EDGAR_FINANCIALS | EIN | 1 | 0.40 | +0.15 | ~0% | no |
| FED_CMS_NPPES | FED_DOL_FORM5500 | EIN | 0 | ~0 | −0.00 | 0% | no |
| FED_CMS_NPPES | FED_FAC_SINGLE_AUDIT | EIN | 0 | ~0 | −0.00 | 0% | no |
| FED_CMS_NPPES | FED_IRS_BMF | EIN | 0 | ~0 | −0.00 | 0% | no |
| FED_CMS_NPPES | FED_IRS_REVOCATION | EIN | 0 | ~0 | −0.00 | 0% | no |
| FED_IRS_990_EFILE_INDEX | FED_SEC_EDGAR_FINANCIALS | EIN | 2 | 5.2 | −0.31 | ~0% | no |
| FED_CMS_LTCH | FED_NURSINGHOME411 | CCN | 0 | 4.5 | −0.74 | 0% | no |
| FED_CMS_IRF | FED_NURSINGHOME411 | CCN | 0 | 17.5 | −1.27 | 0% | no |
| FED_CMS_HOME_HEALTH | FED_CMS_HOSPITAL_GENERAL | CCN | 0 | 68.8 | −1.84 | 0% | yes* |
| FED_CMS_HOSPICE | FED_NURSINGHOME411 | CCN | 0 | 97.5 | −1.99 | 0% | no |
| FED_CMS_DIALYSIS | FED_NURSINGHOME411 | CCN | 0 | 109.1 | −2.04 | 0% | no |
| FED_CMS_HOME_HEALTH | FED_NURSINGHOME411 | CCN | 0 | 182.9 | −2.26 | 0% | no |
| FED_CMS_POS_OTHER | FED_NURSINGHOME411 | CCN | 0 | 628.3 | −2.80 | 0% | no |
| FED_FEDERAL_REGISTER_DOCUMENTS | FED_SCDB | DOCKET | 0 | 348.4 | −2.54 | 0% | no |
| FED_FEDERAL_REGISTER_DOCUMENTS | FED_MSHA_VIOLATIONS | DOCKET | 0 | 1,960 | −3.29 | 0% | no |

*verified on a different key — their graph edge is not the CCN join.

## Verdict: separation is clean on the positive side; the negative side taught
## us exactly the lesson calibration exists to teach

1. **Real connections separate hard.** Every verified pair scores S ≥ +2.7;
   every chance-level pair sits at S ≈ 0. No overlap between the bands. The
   independence null works as designed for "more shared than chance."
2. **The NPPES-EIN trap did NOT produce a false positive.** The masked EIN
   column's tiny distinct count drives E to ~0, so m=0 lands at S ≈ 0
   (boring), not at a fake "surprising absence." The trap layer still flags
   it, but the score itself fails safe.
3. **The one real flaw found: structurally partitioned ID spaces.** All the
   strong NEGATIVE scores are CCN×CCN pairs across different facility types
   (hospice × nursing home, dialysis × nursing home…) and DOCKET×DOCKET
   across different courts. CCNs encode facility type in their ranges — two
   facility types can NEVER share a CCN, so "zero overlap" is by
   construction, not surprising. The naive null over the full key domain
   reads this as dramatic absence. **Fix before the sieve:** absence is only
   surprising when the two sides' observed value ranges actually overlap —
   the null must condition on the two sides actually occupying the same
   value sub-ranges. **Built same day, in two layers** (fmt-2 fingerprints):
   (a) min/max + leading 2-char prefix set per key column, collected in the
   same fingerprint scan — catches leading-prefix partitions (per-court
   dockets); (b) a bucket-histogram check at measure time for pairs landing
   in the absence band — because CCN's leading 2 digits turned out to be the
   STATE (56 shared prefixes between home health and hospitals), with the
   facility-type partition hiding in the middle digits as interleaved
   sub-ranges only a value histogram can see. Sparse/non-numeric histograms
   leave the absence flagged "unverified", never silently confirmed.

## What this buys

The surprise score's positive direction is calibrated and trustworthy today.
The absence direction (the "banned but still operating" shape) needs the
range-conditioning refinement first — which the dark-table fingerprint run
can collect in the same scan it's already doing.
