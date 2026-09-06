# Hunch 2 — which nursing home owners get fined the most per home, and does it repeat

Words used once: **CCN** = CMS Certification Number, one per certified nursing home. **Tag** = the CMS rule number a survey cites (F0689 = accident hazards). **Chain** = the owner group CMS stamps on each home in the provider file.

## What was checked

| Step | Table | What | Number |
|---|---|---|---|
| Chain key | NURSINGHOME411 | Is CHAIN_ID a key? | 618 distinct values, **one is the blank string** on 4,551 homes. 617 real chains. Every id maps to exactly one name, every name to one id, and NUMBER_OF_FACILITIES_IN_CHAIN equals the home count on all 617. Numeric strings 1–825. It is a chain key. |
| Penalty window | PENALTIES | Date range, dupes | 16,180 rows: 13,710 Fine rows with 13,710 distinct FINE_ID, 2,470 Payment Denial rows with no id and no amount. 2023-06-17 to 2026-05-13, zero rows before the open. 6,829 of 6,831 penalty CCNs match the provider file. |
| Deficiency window | DEFICIENCIES | Date range, shape | 418,479 rows, 2017-03-23 to 2026-05-20. But 2017 has 40 homes, 2018 has 489, and complaint citations start in 2023. A rolling window with a thin tail, not a series. |
| Rebuild | PENALTIES → NH411 | Fines per chain, counted from distinct FINE_ID | Bria 88 fines / 15 homes = **5.87**, $5.44M. Genesis 215 / 202 = **1.06**, $9.90M. |
| First pass, second way | NH411 own columns | NUMBER_OF_FINES, TOTAL_AMOUNT_OF_FINES summed by chain | Bria 81 / 15 = **5.4**, $5.24M. Genesis 223 / 202 = 1.1, $10.3M. That is where the first-pass number came from. Two sources, within 4–8%. |
| Fairness floor | all chains | 10+ homes | 301 chains, 8,316 homes, 926,455 beds. |
| Per bed | 10+ chains | fines per 100 beds, $ per bed | Bria 3.51 fines/100 beds (3rd), **$2,172 per bed (1st)**. Genesis 0.90 and $417. All homes 0.87 and $292. |
| Repeat, raw | DEFICIENCIES since 2023-06-17 | (home, tag) pairs cited on 2+ survey dates | Bria 38.0% (162 of 426), 3rd of 301. Saba 43.9% first. Genesis 30.1%. All homes pooled 22.6%, no-chain homes 20.8%. |
| Repeat, normalized | same | survey dates per home, repeats per survey date | Bria homes surveyed **20.3 times each** in the window; everyone else 5.2. Repeats per survey date: Bria **0.53, rank 231 of 301**. Genesis 1.02. All homes 0.71. The raw rate is survey frequency (r=0.84 across 301 chains, skeptic's number). |
| Illinois peers | NH411 STATE='IL' | same rollup, chains with 10+ Illinois homes | Illinois 669 homes: 2.09 fines/home, **$825/bed**; rest of US 14,044 homes: 0.88, $261. Bria is 2.8x Illinois on fines/home, **2.6x Illinois on $/bed** (8.3x rest of US). First of 21 Illinois chains on all three measures. |
| Home by home | Bria | | 14 of 15 fined, 12 of 15 one-star, 11 with abuse icon, 2 SFF candidates, all 15 in Illinois. Bria of Geneva: five stars, zero fines. |

## Top 10 chains, 10+ homes, fines per home (penalty window)

| Chain | Homes | Beds | Fines | Fines/home | Fines/100 beds | $/bed |
|---|---|---|---|---|---|---|
| **Bria Health Services** | 15 | 2,505 | 88 | **5.87** | 3.51 | **2,172** |
| Saba Healthcare | 11 | 2,279 | 42 | 3.82 | 1.84 | 1,371 |
| Bayshire Senior Communities | 12 | 813 | 42 | 3.50 | **5.17** | 832 |
| Elevate Care | 12 | 2,819 | 38 | 3.17 | 1.35 | 574 |
| Bello / Maze / Swain families | 10 | 855 | 31 | 3.10 | 3.63 | 780 |
| Wellington Health Care Services | 14 | 1,943 | 43 | 3.07 | 2.21 | 662 |
| Vertical Health Services | 18 | 2,292 | 51 | 2.83 | 2.23 | 725 |
| Emerald Healthcare | 14 | 1,851 | 37 | 2.64 | 2.00 | 269 |
| Crest Healthcare Consulting | 13 | 1,177 | 34 | 2.62 | 2.89 | 1,692 |
| Helia Healthcare | 13 | 1,461 | 32 | 2.46 | 2.19 | 1,028 |
| Genesis Healthcare (reference) | 202 | 23,771 | 215 | 1.06 | 0.90 | 417 |
| No chain (reference) | 4,551 | 453,251 | 3,979 | 0.87 | 0.88 | 256 |

Chain size is not the signal: 10+ chains 0.96 fines/home, under-10 chains 0.94, no chain 0.87. The owner is.

## Illinois only, chains with 10+ Illinois homes (21 chains)

| Illinois chain | Homes | Fines/home | Fines/100 beds | $/bed |
|---|---|---|---|---|
| **Bria Health Services** | 15 | **5.87** | **3.51** | **2,172** |
| Goldwater Care | 11 | 2.18 | 2.28 | 1,874 |
| Crest Healthcare Consulting | 13 | 2.62 | 2.89 | 1,692 |
| Saba Healthcare | 11 | 3.82 | 1.84 | 1,371 |
| Arcadia Care | 19 | 2.47 | 2.02 | 1,341 |
| Tutera Senior Living | 13 | 2.77 | 2.59 | 1,287 |
| Helia Healthcare | 11 | 2.91 | 2.65 | 1,242 |
| Infinity Healthcare Consulting | 16 | 4.38 | 1.81 | 793 |
| Illinois, no chain | 196 | 1.71 | 1.57 | 711 |

## What a hit means, what a miss means
- Hit: one named owner sits first on fines per home and dollars per bed among 301 chains big enough to rank, and first again when held only to its own hard state. Bria is that owner. Fines are frequent AND large ($61,839 each vs $46,053 at Genesis).
- The repeat leg reframes: Bria is not a chain that repeats more per inspection (0.53 per visit, 231st). It is a chain inspectors visit four times as often as the rest, and every visit finds something. F0689 accident hazards cited and repeated at all 15 homes.
- Miss would be: the number came from one column nobody checked, or a two-home outlier, or a chain of tiny homes. None applies: rebuilt from the penalty file, 14 of 15 homes fined, Bria's homes are bigger than Genesis's (167 beds vs 117.7).

## What a skeptic attacks, and the answer
- "618 chains." It is 617. The blank string is a chain in count(distinct). First pass had the count off by one and the same 10,162 homes-in-chain figure, so nothing downstream moves.
- "Fines per home favors small homes." Yes; per bed Bria drops to 3rd on count but stays 1st on dollars. Bayshire (68-bed homes) tops count-per-bed.
- "Deficiencies 2017–26 is a nine-year record." It isn't; before 2022 the file is scraps (40 homes in 2017). Repeat rate is cut to 2023-06-17 on, matching the fines; on the full file Bria reads 43.2%, same rank.
- "Duplicate penalty rows." 255 groups of same-home, same-day, same-amount fines exist, but each row has its own FINE_ID; counted as separate fines. Payment denials have no id; deduped on (CCN, start, length): 2,470 = 2,470.
- "CMS's own column disagrees." Home by home yes (CMS's column is a different three-year window); chain level within 4% on dollars, 8% on count.
- "Is Bria a real single owner?" CMS's chain tag, id 88, 15 homes, all Illinois, several still named Nexus (a rebrand). Not checked against the ownership file here; that is hunch 30/13 territory.
- "Illinois surveys harder than most states." It does: $825 a bed vs $261 elsewhere, 3.2x. That is why the headline is the Illinois multiple (2.6x), not the national one (7x). Bria is first of 21 Illinois chains with 10+ Illinois homes on every measure.
- "Repeat rate is just survey frequency." Correct, and the skeptic caught it: r=0.84 between survey dates per home and raw repeat share across 301 chains. Bria at 20.3 survey dates per home vs 5.2 elsewhere. Normalized to repeats per survey date Bria is 0.53, below Genesis (1.02) and all homes (0.71). The repeat claim is withdrawn as a Bria distinguisher; the visit count replaces it.
- "The roster is a snapshot." NURSINGHOME411 is dated 2025-12-01 and its chain tag is applied to fines back to 2023-06-17. A home that joined Bria late carries its prior owner's fines under Bria; five of the 15 still carry Nexus names, the sign of a transfer or rebrand. The ownership-change file settles who owned what when; not done here.

## Traps found
- `CHAIN_ID` = '' on 4,551 rows; count(distinct) counts it. Say 617 chains, not 618.
- DEFICIENCIES is a rolling window with a tail: 2017–2021 hold 36,525 rows from a few thousand homes, complaint rows only from 2023. Never chart it as a trend from 2017.
- PENALTIES Payment Denial rows have blank FINE_ID and null FINE_AMOUNT; count(distinct FINE_ID) silently drops them, which is right for fines and wrong for "penalties".

STATUS: confirmed but reframed
HEADLINE: Bria Health Services, 15 Illinois homes, draws 5.9 fines per home and $2,172 per bed since June 2023, 2.6x its own hard state (Illinois $825 a bed, rest of US $261), first of 21 Illinois chains and of 301 nationally; its 38% repeat-tag share is survey frequency (20 visits per home vs 5), not a worse per-visit record.
