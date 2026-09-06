# Executive brief: 21 public-records investigations, checked twice

2026-09-05. Source: a Snowflake warehouse of ~2,900 federal and state public-records tables. Every number below was run, then rebuilt a second way by a fresh reviewer who was told to break it, then fixed. Full chain per finding is in each folder's findings.md; the visual story is story.html, standalone, no internet needed.

## The one-line result

Of 21 leads that had a "confirmed" first number, 1 held as written, 19 held but had to be reframed, 1 died. The numbers almost always reproduced. The sentences around them usually did not.

## Five findings that lead

| # | finding | number | what it really means |
|---|---|---|---|
| E39 | Opioid-maker meals mark heavy opioid prescribers | 6,477 clinicians, 38.7% opioid share vs 15.8% matched peers | targeting, not causation; carried by nurse practitioners and physician assistants |
| E40 | Brand-new billing numbers in the skin-graft business | $452M strict, DY2024, 114 NPIs, 85 over $1M | the graft wave is the anomaly, 200x per patient; new NPIs bill like veterans in it |
| 23 | Eight DME suppliers took 13% of all Medicare DME dollars | $1.43B, one Florida firm $860M | banned in June 2026, after the money; three unbanned suppliers bill the same way |
| 30 | Fined nursing homes change hands more | 7.9% vs 5.1% next year, 1.5x, rising to 12.6% at $100k+ | distressed homes turn over; a shell game is not proven, the buyer identity is not in the data |
| 22 | Redlined neighborhoods hold the toxic plants | 17x the release pounds per km² of grade A | association; ungraded industrial land is worse still |

## Five that reframed hardest

| # | first pass said | now says |
|---|---|---|
| 15 | $169M to banned disaster contractors | $12,232 once ban dates are checked; dead |
| E49 | contracts won during bans | 172 awards, $8.35M, one firm 67%; government net clawed back $102M |
| E57 | 79% of overlap money is royalties | 19%; 53% is consulting and speaking |
| E38 | $70.8M to opted-out doctors | reproduces, but 53% is ten surgeons' royalties; recurring money fell 13% |
| 2 | one chain fined 5x a peer | true, and 2.6x its own hard state; Illinois fines 3x the rest of the US |

## Three structural limits, stated once

- Cost reports: one vintage in the warehouse, so hospital findings E43, E47, E48 are cross-sections, not trends. Landing FY2019-22 turns them into timelines.
- Exclusion list: only 10.6% of banned-provider rows carry an NPI. Every "banned but still active" count is a floor.
- Open Payments: one program year per table. Any "trend" needs a three-table union and a fixed cohort.

## What it cost

0.78 warehouse credits. 2,295 read-only queries. 1.36 TB scanned. Nothing written to the warehouse, nothing published.

## Where to look

INDEX.md links all 21. Each folder: story.html, findings.md, skeptic.md, queries.py, queries.log.
