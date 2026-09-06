# Skeptic pass: IE and committee loaders, 2026-09-06

Verdict: DISAGREE. The load is real and the arithmetic reproduces. Two claims
overstated, one flag dead on arrival.

## Confirmed by the skeptic

| Check | Result |
|---|---|
| Landing rows | 276,183 |
| Per-cycle clean totals | 1.2997 / 3.3017 / 2.2583 / 4.4371 / 1.0546 $B |
| Suspect count | 2018:0 2020:4 2022:8 2024:7 = 19, plus 2026:16 = 35 |
| Nothing lost on overwrite | mart raw $104.253B vs landing 2018-2024 raw $104.252B |
| Money shaping | EXP_AMO lands as raw text; to_numeric touches only the flag test |
| Supersede chains | 590 file_nums both superseded and amending; set test handles it |
| Suspect false positives | all 35 read by eye, every one junk, no real filer caught |

## What was wrong, now fixed

The docstring's walked-out 2024 example was stale and unreproducible.

| 2024 | was written | measured |
|---|---|---|
| raw | 49.68 | 49.679 |
| suspect | 43.95 | 43.899 |
| superseded | 1.75 | 1.343 |
| clean | 3.99 | 4.437 |

The old number read as $0.4B short of the FEC's figure. The truth is a near hit.
The docstring now carries the measured walk and the known gaps.

"The pair catches the junk and nothing else" was false. It is a floor, not a test.

## Junk still inside the clean total

Web-filed rows over $100k that survive the $20M floor:

| amount | rows | candidate | spender |
|---|---|---|---|
| 22,000,000 | 4 | Keener, Logan | DODO COMMITTEE |
| 12,401,000 | 2 | Cobain, Kurt | NIRVANA, LLC. |
| 10,000,000 | 1 | Kim, Jason | SPIRIT OF AMERICAN REFORM |
| 8,849,403 | 13 | Stratton, Juliana | ILLINOIS FUTURE PAC — real |
| 5,141,657 | 8 | McCaskill, Claire | NRSC — real |

Top three are prank, about $44M. Below them the web-filed rows are real money.
That is 0.4% of the five-cycle total and 2.3% of 2026, the cycle still filling.

## Open, not fixed

1. `--cycles` cannot run. `land()` refuses under 98% of the last good run, and one
   cycle is 5% of five. Working around it means `expect_rows=0`, which disarms the
   truncation guard. That is a deliberate call, not a silent patch.
2. Only 2024 is checked against an outside figure. The other four are internally
   consistent and unverified.
3. Cross-cycle amendments move $16.2M out of 2024 into 2026.
4. 2,467 unlinked duplicate rows worth about $31M are invisible to a pointer test.
5. 424 rows carry a negative EXP_AMO. Refunds. They net correctly in a SUM.

## Doors

Python door open, ACCOUNTADMIN on COMPUTE_WH. The chat plug-in was not tested;
its MCP server rejected the configured token at session start.
