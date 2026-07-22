# FEE SCHEDULE CHECK — 2026-07-21 (the real SBA 7(a) upfront fee rules vs. the parity grid)

**Task (Chris, 2026-07-21):** find the actual SBA 7(a) upfront guaranty fee schedule
FY2019–FY2026 from primary documents, then hold it against the ratios in
`outputs/RECEIPT_PARITY_2026-07-21.md`. Two specific questions: (1) can one moving
cutoff light $500k, $1M **and** $2M in FY24 at once, and (2) does the fee schedule
explain the exactly-$500k ratchet. **The page was not touched.**

**Method:** a research pass over the primary documents — the SBA Information Notice
for every fiscal year (all read this session except FY2019's, see caveats), the two
SOP 50 10 editions, and the Economic Aid Act implementation notice. Every rule cited
below was found in a named document this session; nothing is asserted from memory.

---

## 1. The verified schedule, year by year

Tiers are defined on **gross** loan size; the fee is charged on the guaranteed
portion. "Notice" = SBA Information Notice, the annual fee-setting document.

| FY | Upfront fee rule (term loans) | Zero-fee cutoff | Source |
|---|---|---|---|
| 2019 | ≤$150k: 2% · $150k–$700k: 3% · $700k–$5M: 3.5%/3.75% | **none** (rural/HUBZone ≤$150k reduced, not zero) | Notice 5000-180010, via CRS R41146 (see caveat) |
| 2020 | same 2% / 3% / 3.5%+3.75% | **none — explicitly no relief, veterans included** | Notices 5000-19021, 5000-19026 (read, archived copies) |
| 2021 | Oct–Dec: same schedule. **From 12/27/20: 0% for ALL sizes** (Economic Aid Act §327, funds-limited; ran out ~9/23/21) | whole program | Notices 5000-20048, 5000-20084 |
| 2022 | **≤$350k: 0%** · $350k–$700k: 2.77% · $700k–$1M: 3.27% · >$1M: 3.5%/3.75% | **$350,000** | Notice 5000-818641 |
| 2023 | **≤$500k: 0%** · $500k–$700k: 0.55% · $700k–$1M: 1.05% · >$1M: 3.5%/3.75% | **$500,000** | Notice 5000-836123 |
| 2024 | **≤$1M: 0%** · $1M–$2M: 1.45%/1.70% · **>$2M: 3.50%/3.75%** | **$1,000,000**, plus a second step at **$2,000,000** | Notice 5000-848801 |
| 2025 | Oct–3/26: **≤$1M: 0%**, >$1M: 3.5%/3.75% ($2M step REMOVED). **From 3/27/25: relief revoked**, full fees at all sizes | $1M for half the year, then none | Notices 5000-858936, 5000-865775 |
| 2026 | ≤$150k: 2% · $150k–$700k: 3% · >$700k: 3.5%/3.75% | **none** (one carve-out: manufacturers NAICS 31–33 ≤$950k: 0%) | Notice 5000-872051 |

Two non-fee rules that matter to the questions, both from primary docs:

- **SBA Express cap = exactly $500,000, permanent, effective Oct 1 2021** (Economic
  Aid Act §326; stated in notices 5000-20084 and 5000-818641). Every Express loan
  written at its cap is exactly $500,000. Before that: $350k through 3/2020, $1M
  under CARES through 9/30/21.
- **The underwriting line:** SOP 50 10 7 (effective Aug 1 2023 — i.e. the first day
  of late FY23 paperwork feeding FY24 approvals) redefined "7(a) Small" as
  **≤$500,000** — score-screened, no full cash-flow underwrite; >$500k = Standard
  7(a), full underwriting. SOP 50 10 8 (effective June 1 2025) moved that line back
  to **$350,000**. (Notice 5000-847027 and the SOP 8 text itself.)

## 2. Question 1 — FY24 spiking at $500k, $1M AND $2M at once

**Your instinct is right that one moving cutoff can't light three lines — and the
resolution is that FY24 is the one year the fee schedule itself carried TWO lines,
and the third line was never a fee line at all.**

- **$1M — the zero-fee cutoff. Fee schedule explains it.** $0 at $1,000,000;
  ~$10,900 upfront (plus a 0.55%/yr annual fee that also switched on above $1M) at
  $1,000,001. Grid: ratio 24.3, with 485 loans at exactly $1M.
- **$2M — a second, separate step in the SAME year's schedule. Fee schedule
  explains it, and only for FY24.** The FY24 notice priced $1M–$2M at 1.45%/1.70%
  but $2,000,001+ at the full 3.50%/3.75% — and crossing $2M reprices the **entire
  guaranteed portion**, not the marginal dollar: ~$23,000 at $2,000,000 vs
  ~$53,750 at $2,000,001. A ~$30,750 penalty for one dollar. FY23's schedule had
  no boundary at $2M and the FY25 notice deleted the middle tier. The grid agrees
  precisely: $2M ratio 26.5 in FY24, 3.2–5.1 in every other year, collapsing to
  3.8 in FY25 the year the tier vanished.
- **$500k — NOT in the FY24 fee schedule.** No upfront or annual step sits at
  $500k anywhere in notice 5000-848801. The FY24 $500k spike is carried by the two
  non-fee rules above: the Express cap (exactly $500k since FY22) and — new
  precisely in FY24 — the SOP 50 10 7 underwriting line making ≤$500k the
  no-full-underwrite zone. Note the grid's own tell: the $500k ratio **rose** from
  6.9 (FY23, the year $500k WAS the fee cutoff) to 13.4 (FY24, the year it
  wasn't). If fees were the only force at $500k, that number should have fallen
  when the cutoff moved to $1M. It doubled instead.

## 3. Question 2 — the exactly-$500k ratchet (285 → 3,407)

**The fee schedule alone cannot explain it — it puts a rule at $500k in exactly one
year (FY23). A second mechanism is confirmed at work, and it's really a stack of
rules that accumulate at $500,000 and never all leave at once:**

| FY | at-$500k | what sat at $500,000 that year (all document-verified) |
|---|---|---|
| 2019 | 285 | nothing — round-number baseline |
| 2020 | 313 | nothing (notices explicitly: no relief of any kind) |
| 2021 | 631 | no size cliff (fees were $0 at ALL sizes from 12/27/20) — the jump is the free-fee + 90%-guaranty demand surge landing on a round number |
| 2022 | 563 | **Express cap becomes exactly $500k** (permanent). Fee cliff that year was at $350k — yet $500k held its surge-year level |
| 2023 | 1,182 | **zero-fee cutoff = $500k** (upfront and annual) |
| 2024 | 2,394 | fee cutoff left for $1M, but: Express cap still $500k + **≤$500k became the no-full-underwriting zone** (SOP 50 10 7) + fees were $0 ≤$1M anyway, so nothing pushed loans off the number |
| 2025 | 3,407 | all of the above + the FY25a annual-fee schedule put a boundary back at $500k (0% ≤$500k vs 0.17% above — a lender-side incentive) |

- So: **not a cliff, a ratchet by accumulation** — the fee rule (one year) handed
  off to the size-cap and underwriting rules, which persisted. No single rule
  spans all seven years; the research found none and says so plainly.
- One honesty note on the premise: the series isn't strictly monotonic — it dips
  once, 631 → 563 into FY22, consistent with FY21 being a subsidy-surge outlier
  rather than a rule year.
- **The prediction this stack makes was already tested by the page's own FY26
  numbers:** SOP 50 10 8 (June 2025) moved the underwriting line to $350k and the
  FY26 notice restored fees everywhere — so $500k should deflate and $350k should
  re-spike. The parity file shows exactly that: FY26 $500k ratio 4.4 (from 14.7),
  $350k ratio 14.7. The last rule still standing at $500k is the Express/Export
  Express cap, which predicts a floor, not a collapse to baseline.

## 4. What this means for the page (nothing rewritten — your call)

I read `evidence/pages/sba-loan-cliff-migration.md` after the research. The page
already has the FY24 $2M step ("the only year a fee step ever sat there"), the
SOP 50 10 8 move for FY26, and an Express-exclusion robustness check — the primary
notices now **receipt-back those claims**; nothing on the page contradicts the
documents. Three wrinkles the schedule surfaced that the page does not currently
state:

1. **FY2025 is a split year.** The zero-fee regime was revoked MID-year (notice
   5000-865775, effective 3/27/2025, with a precise delegated/non-delegated
   cutover rule). The page's bold-year map says "$1M in FY23–25" — but the $1M
   cliff died six months into FY25, so FY25's ratio (10.2) blends a cliff
   half-year with a no-cliff half-year. That's a refinement, not a contradiction
   — and it's checkable: the FY25 bunching should concentrate in Oct–Mar
   approvals. A clean falsifier-strengthener if you ever want it.
2. **FY26 has a hidden carve-out:** manufacturers (NAICS 31–33) pay 0% upfront on
   loans ≤$950,000. Predicts FY26+ bunching at $950k *among manufacturers only* —
   a free blind prediction sitting in the data, and a small caveat on treating
   FY26 as fully rule-free between $350k and $700k.
3. **The FY25a annual-fee boundary at $500k** (0% ≤$500k / 0.17% above,
   lender-side) is one more documented reason the $500k line stayed hot in FY25
   specifically.

## 5. Caveats (stated, not papered over)

- **FY2019 is the one year not confirmed from its own notice** — the 5000-180010
  PDF could not be retrieved (sba.gov bot-blocks, not in the Wayback Machine).
  Its schedule is taken from CRS R41146 v.101 Table 1, which reproduces and cites
  the notice. High confidence, but CRS-mediated — say so if it ever matters.
- FY2020 has an unexamined continuing-resolution gap (11/22–12/20/2019); the
  notices on both sides are identical, so no conclusion rests on it.
- The exact September-2021 day the Economic Aid Act upfront-fee money ran out is
  corroborated (SBA's fee-history table, 9/23/2021) rather than separately
  documented for the upfront fee.
- Fee-cliff dollar figures above assume a 75% guaranty share; 85%-guaranteed
  smaller loans shift the arithmetic slightly, never the sign.

## 6. Primary sources (all opened this session)

- FY20 — Notice 5000-19021: `web.archive.org/web/20220221063116/https://www.sba.gov/sites/default/files/resource_files/7a_Fees_Effective_for_the_Period_October_1_2019_through_November_21_2019_0.pdf`
- FY20 — Notice 5000-19026: `web.archive.org/web/20230528181229/https://www.sba.gov/sites/default/files/articles/7a_Fees_Effective_for_the_Period_December_21_2019_through_September_30_2020.pdf`
- FY21 — Notice 5000-20048: `sba.gov/sites/default/files/2020-09/SBA%20Information%20Notice%205000-20048_7(a)%20Fees%20Effective%20October%201,%202020-508.pdf`
- Economic Aid Act — Notice 5000-20084 (lender-hosted copy; sba.gov page bot-blocked): `holtandmon.com/docs/Holtmeyer&Monson_SBA%20Information%20Notice%205000-20084_-7_a__Economic_Ai.pdf`
- FY22 — Notice 5000-818641: `sba.gov/sites/default/files/2021-09/SBA%20Information%20Notice%205000-818641-508_0.pdf`
- FY23 — Notice 5000-836123: `sba.gov/sites/sbagov/files/2022-09/5000-836123(R).pdf`
- FY24 — Notice 5000-848801: `sba.gov/sites/sbagov/files/2023-08/7(a)%20Fees%20Notice%20FY%2024%205000-848801.pdf`
- FY25 — Notice 5000-858936: `sba.gov/sites/default/files/2024-07/Information%20Notice%205000-858936%207a%20Fees%20for%20FY%202025%20(FINAL).pdf`
- FY25 revocation — Notice 5000-865775: `sba.gov/sites/default/files/2025-03/Info%20Notice%20-%20Revising%207(a)%20Fees%20(including%20the%207(a).pdf`
- FY26 — Notice 5000-872051: `sba.gov/sites/default/files/2025-08/Info%20Notice%20-%207(a)%20Fees%20FY%202026%20(FINAL%208-28-25).pdf`
- SOP 50 10 7 issuance — Notice 5000-847027 (≤$500k small-loan definition): `sba.gov/sites/sbagov/files/2023-05/2023.05.10%20Information%20Notice%205000-847027%20on%20Issuance%20of%20SOP%2050%2010%207.pdf`
- SOP 50 10 8 text (>$350k = Standard 7(a), eff. 6/1/2025): `partneresi.com/wp-content/uploads/2023/10/SOP-50-10-8-effective-6.1.2025-Final.pdf`
- SBA FTA fee-history table (relief-funds exhaustion date): `catran.sba.gov/ftadistapps/ftawiki/pdf/p.cfm?a=SBA+Annual+Servicing+Fee.pdf`
- Corroboration — CRS R41146 v.101 (FY2019 schedule): `congress.gov/crs_external_products/R/PDF/R41146/R41146.101.pdf`; 2019/2020/2021 editions via everycrsreport.com for cross-checks.
