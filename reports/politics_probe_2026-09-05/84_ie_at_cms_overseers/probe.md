# 84 — Independent expenditures at the CMS overseers

REWRITTEN 2026-09-06. Both blockers this probe named are gone, and the old
headline was wrong. Keep reading for what changed and why.

- **Checked:** IE mart, now 276,183 rows over cycles 2018 to 2026 → CAND_ID =
  legislators' FEC_IDS, a JSON list, flattened → members of HSIF, HSWM and SSFI,
  now per congress rather than current-only. Both junk flags filtered to 'False'.
  SUP_OPP from the IE file is the for/against.

- **First number, congress-matched:** $586.0M against, $191.4M for, across 157
  candidates. A member counts only for the cycles they actually sat on the
  committee. This is the number to quote.

- **Second number, ever-served:** $998.9M against, $341.5M for, 194 candidates.
  Anyone who sat on one of the three committees in any congress from the 113th
  on, counted across every cycle. Wider, looser, and it answers a different
  question.

- **Hit means:** the chain closes end to end with real dollars, and the ratio is
  the finding. Money against these members runs about three times money for them,
  in both framings and in every single cycle.

- **Miss means:** n/a, it hit.

## What was wrong before

| | old probe | today |
|---|---|---|
| IE mart | 261,033 rows, 2018-2024 | 276,183 rows, 2018-2026 |
| national 2022 total | $47B, called "20x high" | $2.26B clean |
| roster | current only, 126 members | per congress, 255 members |
| headline | $773M, $564M against | $586.0M against, $191.4M for |

The 20x inflation was never amendments. It is 35 prank filings carrying $91.0B,
every one both web-filed and over $20M, the largest a $9.98B claim from THE
COURT OF DIVINE JUSTICE. The IE mart now carries IS_SUSPECT_FILING and
IS_SUPERSEDED so the junk is flagged rather than dropped.

## The trap that ate the first rewrite

The roster carries one row per congress. Joining it to the IE mart without a
dedupe multiplies every expenditure by the number of congresses that member
served. On Ways and Means plus Senate Finance in 2024 that turned $252.1M into
$1,431.9M, a 5.7x fan-out that looks completely plausible.

Making the join congress-aware does NOT fix it. That only moves $252.1M to
$249.1M. The fix is `select distinct` on the roster before the join. Do both:
distinct for correctness, congress-matched for meaning.

## Still thin

- CAND_ID is blank on 33,937 rows, 12.3%. On clean 2024 alone that is 8,151
  rows carrying $541.9M that cannot be attributed to any candidate.
- The industry-of-spender leg has not improved. CONNECTED_ORG_NM is blank or
  junk on most big spenders.
- Junk under the $20M floor survives, about $44M, which is 2.3% of the 2026
  cycle. Kurt Cobain is in the clean total.

STATUS: lit
HEADLINE: $586.0M in independent expenditures hit members of E&C, Ways & Means
and Senate Finance while they sat on those committees, 2018 to 2026. Three
quarters of it was spent against them.
