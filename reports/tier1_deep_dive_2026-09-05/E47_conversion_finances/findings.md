# E47 — Were REH converters already broke?

**REH** = Rural Emergency Hospital, a Medicare status since 2023: drop inpatient beds, keep the ER, get a monthly federal payment. 48 hospitals have flipped. **CCN** = CMS Certification Number, the hospital's Medicare ID. **HCRIS** = the annual Medicare cost report, one per CCN per fiscal year.

## What was checked
- `HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS`: 48 rows with `REH_CONVERSION_FLAG='Y'`, 45 dated (2023-02-10 to 2026-03-14), 45 with an old CCN in `CAH_OR_HOSPITAL_CCN`. 17 of those are pipe-joined (`041304|04Z304`); first piece is the hospital, the rest are swing-bed / unit sub-IDs.
- Old CCN -> `HEALTH__FED_CMS_HCRIS`: **35 of 48** have a report. Full-year (350-380 days): 25. Revenue line readable: 24. Report closed before the conversion date: 23.
- Base rate on the same file, same filters, latest report per CCN, REH predecessors removed.
- Old CCN -> `HEALTH__FED_CMS_POS_OTHER`: 43 of 48 found, 40 terminated, all code 07 (voluntary), 38 of 40 terminated within 180 days before the conversion date. Same hospital, not a sub-unit.

## The numbers (raw counts beside every percentage)
| group | losing money | % | median margin of cost | negative net worth |
|---|---|---|---|---|
| **REH converters, last full year** | **20 of 24** | **83.3%** | **-9.5%** | 5 of 24 (21%) |
| rural CAH + short-term, not REH | 807 of 2,418 | 33.4% | +4.7% | 230 (9.5%) |
| rural, 25 beds or fewer | 404 of 1,257 | 32.1% | +5.2% | 107 (8.5%) |
| rural, every type | 849 of 2,508 | 33.9% | +4.6% | 245 (9.8%) |
| all US hospitals | 1,842 of 5,582 | 33.0% | +5.6% | 775 (13.9%) |

Depth: 10 of 24 converters below -10% of cost, 4 below -20%. Rural base: 271 of 2,418 (11.2%) below -10%, 88 (3.6%) below -20%.
Converter median beds 20; rural base median 25. Bed size does not explain it.
Urban hospitals: 993 of 3,074 (32.3%) negative, rural 33.4%. The contrast is converters vs all hospitals, not rural vs urban.
Chart 2 shows 23 converters, not 24: Covington County MS carries RURAL_VERSUS_URBAN='U' and falls out of the rural-only bucket query.

## Rebuilt a different way
- Sign of the mart's own `NET_MARGIN_RATIO` column instead of my `NET_INCOME / TOTAL_COSTS`: 20 of 24 negative, zero sign disagreements. Rural base 806 vs 807, 3 disagreements.
- First pass said 21 of 25 (84%). Reproduces exactly when the EAMC-Lanier row is left in; that row has NaN revenue and NET_INCOME = -operating expense, so it is an artifact. Clean it is 20 of 24. Loose (all 35 reports, stubs included): 28 of 35 (80%), median -12.25%, also reproduced.

## What a hit means / what a miss means
- Hit (what we got): the REH program is catching hospitals as they fail. 5 in 6 converters were losing money the year before, at 2.5x the rural base rate, and half were losing more than a dime on every dollar of cost.
- Miss would have meant: converters look like the rural mix (~1 in 3 negative) and REH is a strategic choice, not a rescue.

## After the switch
14 of 48 already filed under the new REH CCN. 7 have a readable report on both sides: **4 of 7 went from negative to positive** (Irwin County GA -51% to +77%, South Central Kansas -19% to +14%, both Stillwater OK sites -29%/-18% to +8%). Our Lady of the Lake Assumption LA was already profitable (+16% to +51%). Sturgis MI stayed at -38%, Five Rivers AR at -16%. All 7 involve a stub period; direction only.

## The 3-year trend Chris asked for
**Cannot be built from what is landed.** `HEALTH__FED_CMS_HCRIS` is one vintage: 6,103 reports, FY ends 2022-2024, and after the full-year + revenue filter every CCN has exactly one report (5,582 CCNs, 5,582 reports). The 61 CCNs with two raw reports are a stub plus a full year, not two years. Needs the HCRIS 2019-2022 annual files landed. Best one-snapshot proxy for "years of losses" is negative net worth: 5 of 24 converters vs 9.5% rural.

## What a skeptic would attack, and the answer
- *n=24.* Yes. Counts are shown everywhere; the gap (83% vs 33%) is far outside what 24 draws could do by chance from a 33% pool (binomial p < 1e-6).
- *Late converters measured on stale reports.* True: 2025-2026 converters sit on 2023 reports, gap up to 804 days (Garden County NE). The 2023-2024 converters alone: 10 of 13 negative (77%) on the 23-row cut. Same direction.
- *Is the old CCN the same hospital?* POS: 40 of 43 terminated voluntarily, 38 within 180 days before conversion, names match by eye. Yes.
- *Cost-report net income includes county tax subsidies and one-offs.* It does, in both groups equally. Margin of net patient revenue tells the same story: converter median -10.4% vs rural +4.2%.
- *Urban rows in the cohort.* Covington County MS is flagged U; 1 of 24. Dropping it: 19 of 23.

## Traps found
- `CAH_OR_HOSPITAL_CCN` splits on **`|`**, not `/`. The first-pass writeup and its trap note say `/`; `split_part(...,'/',1)` returns the whole string and silently matches 21 instead of 35. Same in landing and mart.
- The mart `HEALTH__FED_CMS_HCRIS` typed the text `'nan'` into a FLOAT **NaN**, not NULL: 237 revenue rows, 89 net-income rows, 82 total-cost rows. `count(col)` counts them, `col is not null` passes them, `col < 0` is false on them. Filter with `col <> 'NaN'::float`.
- 243 rows have NET_INCOME exactly equal to -TOTAL_OPERATING_EXPENSE: blank revenue side. EAMC-Lanier's -138% is one.
- `CASH_ON_HAND_AND_IN_BANKS` goes negative (Adair County OK -537 days cash). Do not build a days-cash measure off it without a look.
- Rural base rate moves by fiscal year: FY2023 496 of 1,385 (35.8%), FY2024 311 of 1,033 (30.1%). The converter reports are mostly FY2023-ended; compare against 35.8% if you want the strictest cut — still 2.3x.

STATUS: confirmed but reframed
HEADLINE: 20 of the 24 Rural Emergency Hospital converters with a readable cost report (83%, of 48 converters total; floor 20 of 48 = 42% if every unmeasured one was profitable) were losing money in their last full year before switching, against 807 of 2,418 rural hospitals (33%); median margin -9.5% of cost vs +4.7%.
