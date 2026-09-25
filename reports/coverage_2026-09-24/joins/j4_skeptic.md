# j4 skeptic, 2026-09-24

**Verdict:** the county half holds. The distributor hook breaks. Grade B -> **B-** (county story only; drop or rewrite the AmerisourceBergen line).

10 read-only statements, tag `joins-skeptic-2026-09-24`. SQL in `j4/skeptic/skeptic.sql`, results `j4/skeptic/s*.tsv`, local math `j4/skeptic/loc.py`.

## Per claim

| Claim | Verdict | What I ran | Number I got |
|---|---|---|---|
| Staircase 20.2 -> 40.8, 2.02x, 1,832 counties 20K+ | CONFIRMED | re-ran deciles from builder panel | 20.2 / 40.8 / 2.02x exact |
| Mail-order exclusion rule | CONFIRMED (harmless), sloppy | S7: listed all 82 excluded buyers + 90 kept LTC/Kaiser/Omnicare/corrections >5M | no exclusion 1.99x; also drop the 90 kept LTC-like 2.02x |
| Fill of 5 per suppressed year | NARROWED (fine, but premise half-wrong) | S5, S6, S9: CDC modeled RATE on suppressed rows; landing COUNT_SUP values | fill with CDC modeled rate: 2.07x. 24 landing rows are "10-50", not "1-9" (10 in 20K set), filled as 5 |
| Population denominator years | CONFIRMED | re-cut with 2006-12 pop for deaths; 20K cut on 2020 pop | 1.92x; 2.01x (1,811 counties) |
| Slope 0.457 -> 0.133 with baseline | CONFIRMED (numbers), t overstated | re-ran an3 regression | 0.457 / 0.133 exact; t uses plain OLS SEs, no robust/spatial SEs |
| Knox #27 of 1,832 at 74.5 | CONFIRMED | re-ranked | #27, 74.5 (2,141 deaths / 478,971 x 6) |
| AB shipped 86.9% of cluster's 30mg+ | CONFIRMED arithmetic, **empty as evidence** | q06 rollup, all TN Food City | AB ships ~87% of ALL pills to TN Food City (65.1M of 74.7M). 86.9% is just "primary wholesaler" |
| 61% mix to cluster vs 12.0% to other TN stores | **BROKEN as framed** | per-store AB vs non-AB mix | circular: stores were picked for high strong share. In 5 of 6 cluster stores the *other* distributors shipped a HIGHER strong mix than AB |
| Six-store cutoff | NARROWED | store list | #674 alone = 13.82M of 19.78M (70%). #632 Loudon is 116,800 pills total. It's one store plus five |
| 77 Food City stores | NARROWED | S8: name search incl. K-VA-T | 7 more stores filed as "K-VA-T FOOD STORES INC" (2 TN: Powell in Knox, White Pine). Missed from peer group |

## The blocker

**"Same wholesaler, same chain, five times the strong share."**
- What was checked: AB's mix to the six high-mix stores vs to the rest.
- Why it can't fail: the six were chosen *because* their mix is high, and AB supplies ~87% of every store. So AB's mix to them must be high.
- The test that could fail: within each cluster store, AB mix vs other distributors' mix.

| Store | AB 30mg+ mix | Non-AB 30mg+ mix |
|---|---|---|
| #616 | 71.5% | 54.3% |
| #674 | 64.2% | 62.3% |
| #694 | 53.6% | 75.2% |
| #644 | 33.3% | 78.1% |
| #682 | 36.1% | 52.9% |
| #632 | 37.3% | 51.4% |

- Hit means: the mix follows the **store's demand**, not the distributor. Every supplier that shipped there shipped strong.
- Masters: 72.1% to cluster vs 23.7% to other TN stores. McKesson: 59.4% vs 17.4%. Same 3-5x gap as AB.

## Smaller holes

- "30mg+" is two products: 13.99M are 30mg (IR, the pill-mill pill), 5.79M are 40/60/80 (mostly ER). Say "30mg" or split it.
- `%MAIL%` also drops ISMAIL / SMAILI / MAILLE practitioners. Trivial pills, but it's a name rule catching surnames.
- Kept LTC pharmacies sit in the top decile (Specialized Pharmacy Services, Ogemaw MI; PruittHealth, Toccoa GA). Don't move the ratio.
- Memory trap `trap-cdc-injury-count-sup-is-the-count` says NULL = 1-9 only. Landing shows 27 "10-50" rows. The mart NULLs both.
- Baseline top-coded at 30: under-controls the worst counties, so 0.133 is if anything high, not low.

## Corrected one-line story

Counties that got the most pills per person in 2006-12 had 2.0x the overdose death rate in 2019-24 (40.8 vs 20.2 per 100k, robust 1.9-2.1x to every fill, filter and denominator tried), but most of that gap was already there in 2006-12. Knox County TN ranks #27 of 1,832 at 74.5. One Knoxville Food City pharmacy, #674, took 31% of the county's 30mg+ oxycodone. Every distributor that shipped it, and its five nearby sister stores, sent a heavy strong mix. AmerisourceBergen was the chain's normal wholesaler, not the outlier.

## Chart rows

- Chart A, B: unchanged. Optional footnote: modeled-rate fill gives D10 41.7, 2.07x.
- Chart C: numbers right. Retitle to a per-store chart. Or add a non-AB mix line so the chart can't be read as "AB pushed strong pills."

## Grade

**B-.** Staircase, control and Knox numbers reproduce exactly and survive every attack. The portfolio hook named in the builder's grade (AB's 61% vs 12%) is circular and gets broken by a per-store check.

DISAGREE with the builder's B: the named-distributor hook is circular, so the dossier's lead finding can't carry it.
