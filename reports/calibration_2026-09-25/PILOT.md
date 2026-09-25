# Calibration pilot, 2026-09-25

19 of 20 pilot stories searched; S174 wasn't, because the session's 200 web searches ran out. Rules and history: `RUBRIC.md`, change log v1 to v3.
Every person or company named is a data match, not verified. Nothing is published.

## Final verdicts, rules v3

Two fresh judges on every story (`judge_v3a/`, `judge_v3b/`); they agreed on 18 of 19. A third settled S195 (`judge_v3c/`). Final set: `judge_final/`. Scores: `python score.py pilot judge_final`.

| Story | Lead, short | Novelty guess | Final bin | What we add |
|---|---|---|---|---|
| S001 | Sands Texas lobby media $20.6M | none | Matched + more | the 62-report total, the 70% share |
| S007 | San Antonio hospice farms | none | Matched + more | 11% vs 0.5% base rate; only a law-firm blog names Loop 410 |
| S024 | Borgers clients, 27 at Nigerian firms | 3 | Matched + more | the 27 at four firms, partner-size split |
| S032 | NP Kim Hinojosa, $24.9M specialty drugs | 4 | Unreported | |
| S044 | FDA 30-day notices 19% to 64% | 2 | Matched + more | the rise by period; Medtronic P980016 |
| S055 | HMDA 2017 Black denial 2x at big lenders | 1 | Matched | nothing countable beyond Urban's 2.0x |
| S075 | White Birch Section 8, 3.5x median rent | 3 | Known pattern | |
| S092 | Redlined areas, 6x toxic-release plants | 1 | Matched + more | plants per 100 km² by HOLC grade |
| S103 | Teva, Actavis, Mutual lawyer-sourced FAERS | 2 | Known pattern | the drug surge is known; the makers as filers aren't |
| S105 | Medicare ordering list clears deactivated NPIs | 4 | Known pattern | |
| S106 | New-operator nursing homes, 0.28 stars lower | 2 | Known pattern | |
| S116 | Duffy fund $0 raised, $1.5M out | 3 | Matched + more | $0 from donors |
| S124 | 5th Circuit, federal-government appeals | 2 | Matched + more | 16 of 38 vs 1 of 26 |
| S139 | Tesla Fremont 356 notices, no district order | 2 | **Contradicted** | the notice count matches; "no order" is wrong |
| S140 | 438 "Negro" place names left | 3 | Matched + more | the Squaw vs Negro renaming pace |
| S168 | Atlantic City public housing 23% empty | 3 | Matched + more | the unexcused 23%, peer rank |
| S171 | Ecuador Los Ríos one-bidder tenders | 4 | Known pattern | |
| S192 | Foreign insiders missed the March 2026 deadline | none | Unreported | |
| S195 | 189 old campaign funds, $8.57M in 2024 | none | Not comparable | |

## Rates

| Rate | Pilot |
|---|---|
| Any source | 10/19 |
| News or trade press | 7/19 |
| Blind: not pre-known, not a control | 7/15 |
| Earliest match after 2026-06-30 | 0 |
| Matches with something countable the press lacks | 9/10 |

## Novelty guess vs result

The guess is the headline lead's own. S001 and S007 lead with join dossiers, which carry no guess.

| Guess | Stories | Matched | Not matched |
|---|---|---|---|
| 1, famous | 2 | 2 | 0 |
| 2 | 5 | 2 | 3 |
| 3 | 5 | 4 | 1 |
| 4, nobody has it | 3 | 0 | 3 |
| none | 4 | 2 | 2 |

## What the pilot changed

- **v2:** bot-walled pages fall back to the Internet Archive. It recovered 5 of 8. This came after control S007 failed; that's on the record.
- **v3:** after the skeptic: headline subject is the entity, "more" must be countable, a contradicted claim beats a matched one, copies count once, judges see page context, quote check splits letters from digits.
- **Judge agreement:** 11 of 16 before v3, 18 of 19 after.

## The skeptic's call vs the final

| Story | Skeptic, on v2 | Final, v3 | Why they differ |
|---|---|---|---|
| S044 | Not comparable | Matched + more | v3 judges saw page context: JAMA's 67.3% is 2008-21, near our 64% since 2010. Chris's call 2026-09-25: count it as a match; the skeptic's no stays on record |
| S103 | leaned Known pattern | Known pattern | agree |
| S124 | leaned Matched + more | Matched + more | agree |
| S139 | Contradicted | Contradicted | agree |
| S055 | Matched | Matched | agree |

## Data trap found

- S139: EPA's ICIS-Air file lacks the Bay Area district's 2021 $1M Tesla settlement and 2024 Hearing Board order. Saved to memory as a trap.

## Cost

- Web searches: 200, the session's whole allowance.
- Agent tokens: about 2.1M across 4 searchers, 13 judges, 1 skeptic and 1 docs check.
- Warehouse: none.
