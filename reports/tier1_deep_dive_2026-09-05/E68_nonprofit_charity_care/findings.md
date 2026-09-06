# E68 — Do rich nonprofit hospitals give almost no free care?

**Short answer:** yes, and the first pass undercounted. 37 reproduces to the digit. The honest count is 89.

## What was checked

- **Table:** `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS` — the Medicare cost report every hospital files. 6,103 reports, 6,040 hospitals (CCN = CMS Certification Number, the hospital's Medicare ID). Fiscal years end Nov 2022 to Sep 2024. One file, one snapshot.
- **Profit:** `NET_INCOME`. **Charity:** `COST_OF_CHARITY_CARE` (Worksheet S-10) divided by `TOTAL_COSTS`.
- **Nonprofit, two ways:**
  - **CMS control code** `TYPE_OF_CONTROL` 1-2 = voluntary nonprofit; 3-6 = for-profit; 7-13 = government. Self-reported on the cost report.
  - **IRS leg** (the first pass's way): name-match hospital to `CORPORATE_REGISTRY__FED_IRS_EO_BMF` on city + state, NTEE code E20-E22 (hospitals), auxiliaries/foundations/guilds excluded. My own normalizer, not the first pass's.
- **Clean rows:** profit, costs and charity all parse (the mart stores NaN, not null), costs > 0, profit <= costs (31 broken rows, Holy Family Memorial WI among them), fiscal year 350-380 days, latest report per hospital. Leaves 2,583 nonprofit, 635 for-profit, 856 government.

## The numbers

| | nonprofit | for-profit | government |
|---|---|---|---|
| clean hospitals | 2,583 | 635 | 856 |
| median charity share | **1.61%** | 2.32% | 1.09% |
| dollar-weighted share | 2.42% | 4.29% | 4.93% |
| under 1% | 808 (31%) | 178 (28%) | 413 (48%) |
| over $50M profit | 399 | 123 | 70 |
| over $50M AND under 1% | **89** | 10 | 11 |
| ...of which IRS name-matched | **37** | 2 | 2 |
| over $50M AND under 1% of operating expense | 124 | | |

**Profit barely buys charity among nonprofits.** Median share by profit tier: loss 1.49%, $0-10M 1.39%, $10-50M 1.83%, $50-100M 2.03%, $100M+ 1.80%. The richest tier gives 21% more than the loss-makers (p25 rises too), a third of a point. For-profits climb: 6.54% median in the $100M+ tier. Government $100M+: 3.60%.

**89 is itself a floor.** Swap `TOTAL_COSTS` for `TOTAL_OPERATING_EXPENSE` as the denominator and 124 nonprofits clear both bars; 89 is the conservative count, 124 the upper bound.

**The 89:** $13.85B net income against $516M charity care, 0.68% dollar-weighted. Their median bad debt is also half the rest (2.7% vs 4.3%), so the wider "uncompensated care" measure does not rescue them.

**The 37 (IRS name-matched):** $6.56B net income, $256M charity. Stanford $1,055M at 0.45%; Cedars-Sinai $825M at 0.80%; Willis-Knighton $438M at 0.98%; Miami Valley $325M at 0.61%; Hoag $303M at 0.89%. Full list with EINs in `story.html`, chart 4, and `results.json` key `irs_tail`.

**The 52 the IRS leg drops** are the most famous names on the list: nine Kaiser Foundation hospitals in California (0.11% to 0.28% charity, $62M to $206M profit each), UK Lexington ($554M, 0.92%), Hospital of the University of Pennsylvania ($317M, 0.93%), Mayo Clinic Phoenix ($268M, 0.70%), Brigham and Women's ($128M, 0.64%), four Advocate hospitals. They miss because the BMF lists the parent under a different city or NTEE code. Full list: `results.json` key `tail_not_irs_matched`.

## What a hit means / what a miss means

- **Hit (this):** the exemption is not buying charity care at the top. One in five nonprofits over $50M profit gives under 1%; the richest tier gives no more than the loss-makers.
- **Miss would have been:** charity share rising with profit, or the tail being a handful of data-entry rows. Neither.

## What a skeptic would attack

1. **"For-profits give more" is selection.** Only 672 of 1,792 for-profit reports with readable total costs (37.5%) carry a readable charity number; the missing 1,120 are small (median $20M costs, 54 beds). Nonprofits report it 88% of the time. The comparison is nonprofits vs the larger for-profits that filled S-10. Stated in the story, not hidden.
2. **S-10 charity is self-reported and one measure.** No 990 Schedule H is landed to cross-check. Bad debt and total uncompensated care were checked as alternates; the tail is low on those too.
3. **Name-join errors.** The normalizer strips HOSPITAL, MEDICAL, CENTER, HEALTH, SYSTEM before matching, so about 5 of the 37 EINs land on a parent or physician group rather than the hospital: Cedars-Sinai paired with CEDARS-SINAI HEALTH SYSTEM, The Queen's Medical Center with QUEENS UNIVERSITY MEDICAL GROUP, Corewell Grand Rapids pulled 37 EINs, Carilion 7. 1,476 pairs for 1,047 hospitals overall. The join identifies exempt status; it does not prove which EIN. 23 for-profit-control hospitals matched a nonprofit BMF name (2.2% wrong-pair floor). That is why the CMS control code is the primary count and the IRS leg is a floor.
4. **"FY2023" is loose.** Fiscal years end Sep 2023 to Aug 2024 across the 37; 15 of 37 end in 2024. Say "the latest cost report," not "FY2023."
5. **Denominator choice.** Share of total costs, not of revenue or of net income. On costs the number is smaller and less flattering to the hospital than share-of-profit would be; either way the ordering holds.
6. **No trend.** One HCRIS file, one BMF snapshot. Nothing here says it got better or worse.

## The answer

The first pass's 37 is real and reproduces with an independent normalizer, but it is a floor set by a name-join that misses Kaiser, Brigham, Penn and Mayo. By the cost report's own ownership code, 89 nonprofit hospitals cleared $50M profit while spending under 1% of costs on charity care (124 on operating expense), and the richest nonprofits give barely more than the ones losing money and a quarter of what the richest for-profits give.

STATUS: confirmed but reframed
HEADLINE: 89 nonprofit hospitals made over $50M and spent under 1% of costs on charity care in their latest cost report; the IRS name-join identifies 37 of them, and the richest nonprofit tier gives a median 1.8%, barely above the 1.5% of hospitals losing money, and a quarter of what the richest for-profits give
