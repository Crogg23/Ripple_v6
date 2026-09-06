# Hunch 5 — Do people get worse loan terms right after a hurricane or flood?

**Short answer.** Not on price. A little on "no."
Hit counties saw denials fall 1.1 points less than the rest of their state. Higher-priced (rate-spread) loan share moved with the control. HOEPA flags rose, but rose the same way everywhere. And the whole denial gap sits in denials where the lender gave no reason.

## What was checked

| Piece | What | Number |
|---|---|---|
| Disasters | FEMA housing registrations, declared 2015-2017 | 47 disasters, 6,090,110 registrations — first pass reproduces exactly |
| Counties | distinct FIPS in those registrations | first pass said 636; **601 once FIPS is zero-padded** (see trap) |
| Loans | HMDA_HISTORIC 2015 / 2016 / 2017 | 14,374,184 / 16,332,987 / 14,285,496 — reproduces |
| Cohort | counties hit in 2016 and NOT in 2015 or 2017, so 2015 is a clean before and 2017 a clean after | 187 counties in 13 states (287 hit in 2016; 100 dropped for being hit again) |
| Control | counties in those 13 states with no 2015-2017 declaration, with applications in both 2015 and 2017 | 896 counties (897 across any year) |
| Measures | denial rate = denied ÷ (originated + approved-not-accepted + denied); rate-spread share and HOEPA share among originated loans | aggregated in SQL by county-year, 9,656 rows pulled, never row-level |

HMDA is the federal file where every mortgage lender reports each application and its outcome. HOEPA is the federal flag for a high-cost loan. Rate spread is the loan's APR minus the prime benchmark, reported only when it is 1.5+ points — so "rate-spread share" means share of loans that were higher-priced. HOEPA is a stricter, separate flag.

## The numbers

| | Hit 2015 | Hit 2017 | Ctrl 2015 | Ctrl 2017 | Diff-in-diff |
|---|---|---|---|---|---|
| Denial rate % | 23.08 | 21.89 | 23.33 | 21.06 | **+1.07 pts** |
| Higher-priced (rate-spread) share % | 6.80 | 7.52 | 6.66 | 7.58 | -0.19 pts |
| HOEPA per 10k loans | 3.2 (102 loans) | 8.4 (260) | 1.3 (161) | 4.7 (583) | +1.8 per 10k — stated separately; both tripled on a nationwide 2017 jump (1,464 → 3,603), not a disaster effect |

Applications: 431k / 417k hit, 1.66M / 1.65M control.

## The chain

- **Hit on denials:** control counties improved 2.27 pts, hit counties 1.19. Gap +1.07.
- **County by county:** 119 of 168 hit counties (200+ apps) fell behind their state's control. Median +1.17.
- **Robustness (skeptic's check):** put withdrawn and incomplete files in the denominator too → +0.95. Withdrawals rose less in hit counties (DiD -0.30 pts of files), so the gap is not withdrawals reclassified.
- **Placebo:** counties hit only in 2017, measured 2015→2016 when nothing had happened: -0.08. The method does not invent gaps.
- **Dose:** declared Jan-Jun 2016 → +0.87 in 2016, +1.92 in 2017. Declared Jul-Dec → +0.46, +0.65. Earlier hit, bigger gap.
- **States:** 10 of 13 positive. LA (49 counties) +1.73, NC (44) +1.62, TX (12) +1.78. VA -1.07, WV -0.34. AR is one county, 99 apps — ignore.
- **Miss on price:** rate-spread DiD -0.19; first-lien only -0.22. Hit counties did not get pricier loans.
- **HOEPA:** 102 → 260 hit, 161 → 583 control. Nationwide 1,464 → 3,603. A 2017 reporting jump, not a disaster effect.
- **Why the denials:** split by lender-stated reason, per 100 apps. Collateral -0.08. Credit history +0.13. Debt-to-income -0.12. **No reason given +1.14 — the whole +1.07 and then some; the coded reasons net to -0.07.** (A first cut read +1.02; 19,331 denials with no county code had leaked into the control. Filter added, rerun.)

## What a hit means / what a miss means

- Hit on price would have meant lenders charging disaster victims more. It did not happen.
- Hit on denials means fewer disaster-county applicants got a mortgage than their state's trend said they should. That is what shows, at about 1 in 100 applications.
- A miss on reasons would have meant the gap is reason-coded (collateral would be the damaged-house story). It is not.

## What a skeptic attacks

1. **No dates.** HMDA_HISTORIC has no application date, only year. "12 months before/after" is really calendar 2015 vs 2017. For an August 2016 flood that is 5-16 months before and 5-16 months after. The dose check is the best that can be done.
2. **The gap is unexplained denials.** Reporting a denial reason is optional for most lenders. +1.14 in "no reason" is consistent with (a) lenders declining more and not saying why, or (b) a shift in WHICH lenders wrote loans in hit counties — non-bank lenders who never code reasons. HMDA has RESPONDENT_ID; a lender-mix check is the next step and was not run.
3. **Parallel trends.** 2015→2016 DiD is already +0.58, but 2016 is half "after" for most of the cohort (dose check: early declarations +0.87, late +0.46). Not a clean pre-period; no 2014 in the table to get one.
4. **1.07 points is small.** Real, consistent, small. Not a headline about profiteering.
5. **The 2017 hurricanes are not in this.** Harvey, Irma, Maria (5.3M of the 6.1M registrations) have their "after" in 2018, which HISTORIC does not hold. This is a 2016 story.

## Answer

Lenders did not price disaster victims worse. They said no about 1 point more often than the state trend, and mostly did not say why.


## Trap found

- FEMA `FIPS` is TEXT and unpadded for states 01-09: `1097` and `01097` both appear. `count(distinct FIPS)` reads 636; `count(distinct lpad(FIPS,5,'0'))` reads 601. 69,662 rows have null FIPS. Pad before any county join.
- HMDA_HISTORIC `STATE_CODE`/`COUNTY_CODE` are also unpadded TEXT (`6`, `67`). Build the key as `lpad(STATE_CODE,2,'0')||lpad(COUNTY_CODE,3,'0')`.
- HMDA_HISTORIC has no application date column. Month-level before/after is impossible; year only.

STATUS: confirmed but reframed
HEADLINE: After 2016 disasters, hit counties saw 1.1 pts more mortgage denials than the rest of their state — all of it "no reason given" — and zero change in higher-priced (rate-spread) loan share (-0.2 pts); HOEPA +1.8 per 10k rides a nationwide 2017 jump.
