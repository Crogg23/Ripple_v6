# E48 — Were their financial reports already bad beforehand?

**Question.** Hospitals whose Medicare participation ended 2024-26: did the last cost report already show a loss? And can a simple loss threshold pick closures out of the crowd?

**Words once.** CCN = the Medicare certification number for one hospital. POS = CMS's Provider of Services file, which stamps each CCN with a termination date and a reason code. HCRIS = the Medicare hospital cost report: income statement and balance sheet.

## What was checked

| Step | What | Result |
|---|---|---|
| Rebuild the 68% | Different rule from the first pass: latest 350-380 day report ending on or before the termination date; NaN floats dropped | **95 of 141 = 67.4%** terminated vs 1,889 of 5,579 = 33.9% active. First pass: 96 of 142 = 67.6%. One hospital differs: its report ends after its termination date, so it was excluded |
| Split by POS termination code | 01 closure/merger, 07 status change, 05 involuntary | 01: 54 of 79 = **68.4%** in the red, median -8.5%. 07: 40 of 58 = **69.0%**, median -8.3%. 05: 1 of 4 |
| Successor CCN | CROSS_REF_PROVIDER_NUMBER as the "sold/absorbed" marker | With a successor: 47 of 68 = 69% negative. Without: 48 of 73 = 66%. No difference |
| Margin distribution | Percentiles of net income / total cost | Terminated p10/p50/p90 = -33.6 / -8.1 / +21.1. Active = -14.6 / +5.3 / +31.1. A quarter of the terminated were profitable |
| Years of losses | Count 12-month reports per CCN | **5,812 hospitals have exactly one 350-380 day report; no hospital has two.** Not measurable |
| Threshold test | Termination rate by margin bin, cross-section | margin < 0: 4.8% (2.8% closure-type). < -10%: 6.8%. < -20%: **8.4%** (5.5% closure-type). Per bin: -30 to -20 = 10.1%, below -30 = 7.6% (n=301). +10 to +20%: 0.5% |
| Stacked flags (stand-in for a streak) | net loss + operating loss + negative fund balance + current ratio < 1 | 0 flags: 1.1% terminated. 4 flags: **8.5%** (29 of 341), 6.5% closure-type |
| Negative equity | TOTAL_FUND_BALANCES < 0 = accumulated losses ate the equity | Terminated 45 of 138 = 32.6%; active 728 of 5,366 = 13.6%. Code 01: 43%; code 07: 17% |
| Time order | Report end vs termination date | Lag 0-90d: 82% negative; 91-365d: 69%; 366-730d: 62%; >730d: 75% (n=12) |
| Missing | Terminated in POS but no usable report | 192 terminated 2024-26; 141 usable, 16 no report, 32 stub-only, 3 other |

## What a hit means

The last cost report is a real early warning: a loss roughly quadruples the odds of leaving Medicare within two years, a deep loss about 7x (8.4% over the 1.2% profitable base). The curve reverses at the bottom: -30 to -20 terminates 10.1%, below -30 only 7.6% on n=301. It fires on sales and status changes exactly as hard as on closures, so "sold" is not a cleaner story than "closed"; the hospitals that changed hands were just as broke.

## What a miss means

It is a weak predictor on its own. 92% of hospitals below -20% and 91% of hospitals with all four flags were still open at snapshot. The signal picks a watch list of a few hundred; it does not name the 141.

## What a skeptic would attack

- **"Years of losses" was asked and not delivered.** True. The file holds one report per hospital. The four-flag stack and negative equity are the honest stand-ins; they say "losses long enough to wipe equity," not "three straight years."
- **The active group is contaminated.** POS snapshot's latest hospital (category 01) termination is 2026-03-05; hospitals that failed after that sit in "active." That pulls the active loss share up and the threshold rates down. Direction only helps the hunch.
- **Code 07 is not closure.** Agreed, and it is split out everywhere. The headline holds on code 01 alone (68.4%).
- **Cost denominator.** Margin on net patient revenue gives the same medians (-8.3% vs +5.1%). NET_MARGIN_RATIO in the mart is over gross charges and was not used.
- **Small bins.** Code 05 is 4 hospitals; the >730-day lag bucket is 12. Neither carries a claim.
- **Survivorship in HCRIS.** 48 of 192 terminated hospitals have no 12-month report; the ones that collapsed mid-year are likeliest to be missing, so 67% is probably a floor.

## Traps found

- The mart's FLOAT columns hold real NaN where the landing text said 'nan' (NET_INCOME 89, TOTAL_FUND_BALANCES 309, NET_MARGIN_RATIO 245 rows). `count()` counts them, `< 0` is false on them. Guard with `iff(x = 'NaN'::float, null, x)`.
- HEALTH__FED_CMS_HCRIS.NET_MARGIN_RATIO = NET_INCOME / TOTAL_PATIENT_REVENUE (gross charges), matched on 5,858 of 5,858 rows. It is not a margin on net revenue or cost and reads 2-3x smaller; 164 rows flip sign against NET_INCOME.
- HCRIS holds no hospital with two 350-380 day reports (5,812 with one, 0 with two). Anything phrased "N straight years" is untestable until a second vintage lands.
- HEALTH__FED_CMS_POS_OTHER has no _INGESTED_AT column; HCRIS's is epoch microseconds (1781673011749547 = 2026-06-16).

## Answer

Yes. Two thirds of the hospitals that left Medicare in 2024-26 were already losing money on their last full-year report, against one third of everyone else, and the whole margin distribution sits about 13 points lower. Sales look the same as closures. As a screening rule it is loud but blunt: the worst bin terminates at 8%, not 50%.

STATUS: confirmed but reframed
HEADLINE: 67.4% of the 141 hospitals terminated 2024-26 lost money on their last cost report (33.9% of active); below -20% margin, 8.4% terminated within two years — a loss streak can't be measured, no hospital has two 350-380 day reports.
