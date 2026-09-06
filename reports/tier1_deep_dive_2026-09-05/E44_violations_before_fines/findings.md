# E44. Did Bria's violations get worse right before the fines hit?

Bria Health Services, CHAIN_ID 88, 15 nursing homes, all Illinois. A CCN is the six-digit number CMS gives each home; every join is on it.

## What was checked

| Step | Number | Hit means | Miss means |
|---|---|---|---|
| Is Bria one chain, is CCN a key | CHAIN_ID 88 = 15 homes, 15 distinct 6-char CCNs. NH411 14,713 rows / 14,713 CCNs. Deficiencies 418,479 rows / 14,632 CCNs. Penalties 16,180 / 6,831. | joins cannot fan out | chain-level rates would be wrong |
| Rolling window | 6 of Bria's 15 homes and 6,265 of 14,632 national homes have no retained survey before 2023 | raw counts inflate 2023-to-2025 rises; denominators must be per-month homes-in-window | counts would have been fine |
| Rebuild the first-pass number a different way (per-home rows summed, letter range G..L instead of an IN list) | 2023: 49 of 228 = **21.5%**. 2024: 70 of 345 = 20.3%. 2025: 76 of 227 = **33.5%** | reproduces to the digit | first pass was wrong |
| Deficiencies per home per month, Bria vs national | Bria **1.38 / 1.92 / 1.26** (2023/24/25). National **0.67 / 0.71 / 0.61** | Bria 2-3x the country every year | Bria looks average |
| Harm (G+) citations per home per month | Bria **0.30 / 0.39 / 0.42**. National 0.038 / 0.044 / 0.038 | roughly 10x national every year (7.8x, 8.8x, 11.2x), up 42% over 2023 but only 9% over 2024 | harm rate flat or falling |
| Immediate jeopardy (J-L) per home per month | Bria **0.042 / 0.028 / 0.094** = 7, 5, 17 events. National 0.016 / 0.019 / 0.016, flat | 2025 is 2.4x 2023, 2.7x the pooled 2023-24 rate (12 events over 345 home-months), 6x the country; 12 of 17 came Jul-Dec 2025 | no escalation |
| Fine dollars per home per month (penalty file starts 2023-06-17) | Bria **$17,168 / $8,425 / $11,247**. National $1,155 / $1,073 / $836 | 13x national in 2025, and down from 2023 H2 | fines climbing |
| Fines (count) per home per month | Bria 0.19 / 0.17 / 0.19. National 0.049 / 0.030 / 0.021 | flat, while the country's fell | rising count |
| Lag: G+ per home in month t vs fine $ per home in month t+lag, Jun 2023-Dec 2025 | National r = **0.67 at lag 0**, then 0.61, 0.60, 0.54, 0.44, 0.50, 0.36. Bria r = 0.32 at lag 0, then -0.15, -0.05, -0.01, -0.23, 0.34, -0.33 | nationally, fines are dated with the citation, not after; Bria's series is too noisy to date the lag | fines would peak months later |

## What it means

- **Bria is worse than the country every single month**, not just lately. That is the real headline.
- The first pass's **21.5% to 33.5%** is right but mostly a denominator move: 2025 total citations fell 345 to 227 while harm citations held 70 to 76. The harm *rate* per home rose 9% year on year.
- What actually escalated is **immediate jeopardy**: 17 events in 2025 against 7 and 5, concentrated in the second half. Small counts; national IJ was flat.
- **Fines did not follow the violations, they arrived with them.** Nationally correlation peaks at lag 0 (0.67) and decays. Bria's own series cannot date the lag (0.32 at lag 0, 0.34 at lag 5, sign flips between). Both series carry a trend, so every lag r is inflated; read the ranking of lags, not the size. Bria's fine rate was highest in 2023 H2 and never got back there. "Worse before the fines hit" has no window in this data.
- 2024 is the year the first pass skipped, and it breaks the tidy story: most citations, lowest harm share, lowest fines.

## What a skeptic would attack

- **15 homes make monthly noise.** Answer: the 3-month rolling lines and the yearly rates agree; the lag test is also run nationally, where 14,000 homes give the same lag-0 shape.
- **Rolling window bias.** Answer: denominators are homes-in-window each month on both sides; 2023 H1 rates are the least trusted numbers here and no conclusion rests on them.
- **Chain roster is a 2025-12-01 snapshot with no history.** The 12-month ownership-change flag (N on all 15) says nothing about 2023, so pre-2025 attribution to Bria is assumed, not shown. Six of the 15 are named "Nexus", possibly a rebrand. Not checked outside the warehouse.
- **Fine date is not survey date.** True, and that is the finding: the penalty date moves with the survey month, so a lead-lag reading is impossible from these two files alone.
- **Oct 2025 national dip** (2,425 citations vs ~10,000 typical) is consistent with the federal shutdown; Bria's own October had 7 citations, 6 harm-level. The 2025 IJ rise does not depend on that month.
- **The first pass's complaint-mix standardisation** used a flag that is 'N' on every row before April 2023 (see traps). Its 2023 complaint share of 62.7% is a floor, so the adjusted 31.0% is not reliable either way.

## Traps found

- `CHAIN_NAME ilike '%bria%'` also catches **BRIAR HILL MANAGEMENT** (chain 89, 6 Mississippi homes). Pin on CHAIN_ID = '88'.
- `COMPLAINT_DEFICIENCY` is **'N' on 100% of rows surveyed before 2023-04**; it switches on in Q2 2023. Any complaint-vs-standard split that includes early 2023 reads as all-standard.
- Only PENALTY_TYPE = 'Fine' carries FINE_AMOUNT; 2,470 Payment Denial rows (15%) are penalties with no dollars.

STATUS: confirmed but reframed
HEADLINE: Bria's homes draw roughly 10x the national harm-citation rate (7.8x to 11.2x) and 13x the fine rate per home every year; immediate jeopardy went 7, 5, 17 events (2.4x 2023) while national was flat; nationally fines land in the same month as the citations (r = 0.67 at lag 0), and Bria's own series is too noisy to date the lag.
