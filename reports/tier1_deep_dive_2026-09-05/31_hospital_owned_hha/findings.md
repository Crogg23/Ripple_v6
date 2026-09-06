# 31. Hospital-owned home health agencies: worse but pricier?

Snapshot. Three mart tables, all Python door. Every query in `queries.py`, log in `queries.log`.

## Words, once
- **CCN**: the Medicare certification number every facility carries. The join key here.
- **PECOS**: Medicare's enrollment roster. Its **ASSOCIATE_ID** is the organisation that did the enrolling.
- **Hospital-owned**: the home health agency's ASSOCIATE_ID also sits on a hospital enrollment. 475 organisations, 530 agencies, 519 of them in Care Compare.
- **Independent**: in PECOS, no hospital on the same ASSOCIATE_ID. 10,694.
- **Not in PECOS**: in Care Compare, no enrollment row at all. 1,179.

## What was checked
| Check | Number | Hit means | Miss means |
|---|---|---|---|
| CCN is a key in Care Compare | 12,392 rows, 12,392 distinct, all 6 chars | safe join | fan-out |
| Star blank, owned vs independent | **5.2% vs 32.6%** (first pass said 5 vs 37) | comparison is biased | fair fight |
| Why blank | 100% carry "too few episodes to report" | it is volume | it is something else |
| Blank by volume band | under 100 episodes: 29% owned / 56% indep. 250+: under 5% both | blanks are small agencies | blanks are owned agencies |
| Mean star, everyone rated | 3.16 owned vs 3.26 indep; median 3.0 vs 3.5 | owned scores lower | no gap |
| Mean star, 100+ episode cohort (313 vs 4,158 rated) | **3.06 vs 3.17**, about 2 SE; median 3.0 both | owned a hair lower | no gap |
| Spend per episode vs national, same cohort, per agency | **0.996 vs 0.965**, about 4 SE | owned costs 3% more per agency | no gap |
| Same, weighted by episodes | **0.9945 vs 0.9755**, 1.9% | owned costs 1.9% more per episode | no gap |
| Spend gap by size band, per agency | 100-249: 6.2 pts. 250-499: 2.9. 500-998: 0.7 | gap shrinks as agencies grow | flat |
| Blanks still inside the cohort | 294 independents, 1 owned. Blank indep DTC 59.7 vs rated 79.6 | cohort still flatters independents | cohort is clean |
| Discharge to community, same cohort | **83.7% vs 78.6%**, about 8 SE | owned better outcome | worse |
| Preventable hospitalization, same cohort | 10.6% vs 11.0% | owned better | worse |
| For-profit only, same cohort | 3.05 vs 3.17 star, 0.996 vs 0.964 spend | tax status is not the driver | it is |
| Patient survey star (HHCAHPS) | **not landed**, searched every table name | — | — |

## The first-pass number, rebuilt
37% reproduces only if "not in PECOS" (78% blank) is lumped into independent: (3,488 + 916) / (10,694 + 1,179) = 37.1%. Split out, real independents are 32.6% blank.

## The answer
- **Worse?** Barely. A tenth of a star on the fair cohort, and the claims outcomes go the other way: owned agencies send 5 more patients per hundred home.
- **Costs more?** Yes. 3% per agency, 1.9% per episode once weighted by volume. The gap lives in the small agencies: 6.2 points at 100-249 episodes, 0.7 at 500-998. Solid but small, and shrinking with size.
- **Missingness:** it biased the first pass, but toward the independents looking good, not the owned. Blank agencies are small independents; their rated survivors skew high. Volume-matching shrinks it, does not remove it: 294 independents in the 100+ cohort are still blank, and they are the worst ones (discharge-to-community 59.7 vs 79.6 for rated). So 3.17 flatters independents and the tenth of a star is an upper bound on the gap.
- **Shape:** owned is a narrow middle. 61% of owned rated agencies sit at 2.5 to 3.5 stars. 20% reach 4+ vs 36% of independents; 12% sit at 2 or under vs 20%.

## States
Gap flips sign. Alabama owned 2.92 vs 4.01 indep, Arkansas 2.76 vs 3.62, Nebraska 2.86 vs 3.56, Louisiana 3.08 vs 3.76. California 3.37 vs 3.16 and owned spends 0.836 vs 0.943. Most states hold 10 to 43 owned agencies; single-state gaps are leads.

## What a skeptic attacks
- **The owned flag.** Shared ASSOCIATE_ID means same enrolling organisation, not a deed. Second check: 140 of 519 owned carry HOSPITAL / MEDICAL CENTER / HEALTH SYSTEM in the name vs 77 of 10,694 independents. The flag is real. Those 77 say it undercounts: a system can enroll its agency under a separate entity. Undercount dilutes the gap, it does not fake one.
- **The star is a composite**, mostly OASIS-reported functional improvement. Self-reported by the agency. The claims outcomes (discharge to community, preventable hospitalization) are not, and they favour owned.
- **Spend per episode is blind to episode count.** Same caveat as the Frank report. A 3% pricier episode says nothing about how many episodes.
- **2 SE on the star** is one bad draw from nothing. The spend and outcome gaps are not.
- **Case mix.** Hospital agencies take post-acute discharges; independents take community referrals. The rates are risk-standardized, the star is not. Not separable here.
- **The episode column tops out at 998.** One agency sits at exactly 998; the 500+ band is 500-998. Nothing above is visible.
- **Not in PECOS** is 1,179 agencies of unknown ownership, 78% blank, dropped from the fair fight. They are small; nothing else is known.

## Traps found
- 95 enrollment rows carry a 7-char CCN (6 digits plus a letter, e.g. 397012A): branch offices. All 95 have their 6-char parent in Care Compare. Stripping the suffix changes nothing here (530 either way) but a bare CCN join drops them.
- Lumping "not in PECOS" into independent inflates the blank rate from 32.6% to 37%. Three groups, not two.

STATUS: confirmed but reframed
HEADLINE: Among 4,766 agencies with 100+ episodes, hospital-owned home health costs 3% more per agency and 1.9% more per episode (0.9945 vs 0.9755), and on the 4,471 rated ones scores a tenth of a star lower (3.06 vs 3.17, median 3.0 both, an upper bound), but sends 5 more patients per hundred home; the 37% blank-star gap was small independents, not a bias against owned.
