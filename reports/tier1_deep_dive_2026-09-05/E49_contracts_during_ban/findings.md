# E49 — Did banned companies win government contracts during their ban?

**What was checked.** SAM is the federal do-not-do-business list. USAspending is the ledger of every federal contract action. Joined them on UEI (the 12-character company id both carry), then kept every contract action whose date falls between the ban's start and its end (open bans end today). Each action counted once: a company with several overlapping listings is matched to its earliest covering window.

## The chain

| Step | Number |
|---|---|
| SAM mart rows | 168,328 — every one is `RECORD_STATUS='Active'` |
| Rows with a UEI | 47,686 (38,427 distinct) |
| Ban windows (UEI x activation, 2000..today) | 40,680 across 32,998 company ids |
| Those ids ever in USAspending contracts | 382 ids, 128,649 actions, $5.19B lifetime |
| Actions dated inside a ban | **1,762 actions, 1,390 awards, 136 companies** |
| Net obligation inside bans | **-$102.0M** |
| Actions at $0 | 507 |
| Actions taking money back | 1,037 (-$118.0M) |
| Actions putting new money in | 218 actions, 197 awards, 45 companies, **+$16.0M** |
| ...on awards that BEGAN inside the ban | **172 awards, 37 companies, $8.35M**, median award $4.3k |
| ...on pre-ban awards (modifications) | 25 awards, 15 companies, $7.62M |

**What a hit means.** A contracting officer obligated money to a company while it sat on the exclusion list. For the 172 awards that started inside the ban, that is new work handed to a listed company — the thing the rule (FAR 9.405) says not to do. For the 25 modifications, the rules allow continuing a pre-ban contract, so those are weaker.

**What a miss means.** Zero or negative money inside a ban is the system working: stop-work, terminate, de-obligate. That is 88% of the in-ban actions (1,544 of 1,762).

## The distribution, on ONE denominator: the 172 awards ($8.35M)

- Nova Datacom: 4 awards, $5.59M = **67%**. Next: Bonus Environmental, 14 awards, $839k (10%). Strip Nova: **$2.76M over 168 awards, 36 companies.**
- Size: 60 awards under $1k, 60 at $1k-10k, 45 at $10k-100k, 6 at $100k-1M, 1 over $1M. **120 of 172 under $10k.**
- Timing (each award once, at its first in-ban action): 26 within 7 days, 15 at 8-30 days, 16 at 31-90, 32 at 91-365, **83 over a year in (48%)**. Not paperwork lag.
- Agencies (all in-ban actions): DoD 1,396 joined rows, VA 252, DHS 254 before dedupe; Treasury's net is -$52M, the ATI clawback, not awards.

The wider all-positive set ($16.0M, 197 awards, 45 companies) adds ATI Government Solutions at $6.8M, all on contracts that predate its listing; its biggest line is a $4.6M termination settlement. ATI is not in the 172.

## Straddlers, disclosed
11 awards have in-ban actions that report a period-of-performance start both before and after the ban start (USAspending restates the start date on modifications). All 11 are classed "started before ban" using the earliest date. One carries positive money: Consummate Computer Consultants, $100,375 (net $7,065). The other 10 are Quantell (7), Consummate (2), Nova Datacom (1), all net zero or negative. Moving all 11 into the 172 would add $100k.

## Rebuilt a different way
Joined on CAGE code instead of UEI (only 435 SAM rows carry one): 700 actions, 540 awards, 74 companies, net -$23.3M, +$1.7M new. Same shape — mostly clawback, small positive tail.

**The first pass does not reproduce.** "17 awards, $43k plus one big one" — no UEI or CAGE cut here gives 17 awards. The 2008 slice alone is 48 awards, $42,941, which smells like the same $43k under a narrower join. Treat the first-pass count as superseded.

**Skeptic pass, round 1, and the fix.** First build joined each action to every matching window: 2,289 joined rows were 1,762 distinct actions, so -$115.8M was really -$102.0M and $16.2M was $15.97M. Fixed with a `qualify row_number() ... = 1` per landing row. The 172 / 37 / $8.35M held. (Skeptic counted 1,758 distinct; this build's 1,762 keys on the full landing row, so 4 exact-duplicate landing rows survive. Difference is 0.2%, noted not chased.)

## What a skeptic would attack, and the answer
- **"Proceedings Pending" is not a ban.** True for Nova (SBA proposed debarment). FAR 9.405 still says do not award to proposed debarred contractors without a compelling-reason finding. Reported as such.
- **EPA "Prohibition/Restriction" listings are facility-scoped**, not government-wide. Bonus Environmental (14 Army awards, $839k), MFA Inc (17 awards) and Target Corporation (46 awards, $32k) ride that type. Caveated, not removed; not verified from data here.
- **SAM mart is a current snapshot.** All 168,328 rows are Active; bans that ended and were purged are invisible. Every count here is a floor for history.
- **Parse risk.** 0 of 128,655 candidate rows failed `try_to_number` on obligation or `try_to_date` on action date.
- **Junk dates.** ACTIVATION_DATE runs 1908..2099; cut to 2000..today.

## Traps found
- `FED_USASPENDING_CONTRACTS_FULL_R2` columns are **UPPERCASE**; the traps.md line about lowercase USAspending columns does not apply to the R2 copy.
- The SAM **mart has no DUNS column** (UEI, CAGE, NPI only). A DUNS join needs the raw landing table.
- **SAM windows overlap per UEI**: 1,798 UEIs carry 3+ rows. A plain action-to-window join fans out 30% (2,289 rows for 1,762 actions). Dedupe per action before summing.
- `FEDERAL_ACTION_OBLIGATION` is signed; 88% of in-ban actions are zero or negative. "Contracts during the ban" summed raw reads -$102M. Filter `obl > 0` or the story flips.
- SAM mart is Active-only (`RECORD_STATUS` has one value): a history question gets a snapshot answer.
- USAspending restates PERIOD_OF_PERFORMANCE_START_DATE on modifications; 11 awards here carry two different start dates. Use min() per award.

STATUS: confirmed but reframed
HEADLINE: 172 awards worth $8.35M began while the company was on the SAM ban list, and one company, Nova Datacom, holds 67% of that; strip it and $2.76M is spread over 168 awards to 36 companies.
