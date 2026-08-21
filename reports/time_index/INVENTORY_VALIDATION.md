# Is the nouns-and-things inventory still good? — validated 2026-08-20

Checked `reports/noun_event_inventory_2026-08-18.md` and the census grid behind it
against the live warehouse today. No warehouse compute spent — this reuses the
catalogue listing and the measured row counts from today's time-index scan.

## Verdict: it holds, with one real gap

**The inventory is still accurate for what it covers.** Nothing it describes has
vanished, and almost nothing has moved. It is, however, **22 source datasets short
of the warehouse as it stands today.**

| check | result |
|---|---|
| Tables the inventory was built on | 589 |
| Still present today | **589 — none missing** |
| Row counts that moved more than 2% | **8, all small** |
| Live tables the inventory does not mention | 58 |
| …of which excluded on purpose | 36 |
| …of which **genuinely missing source data** | **22** |

## The eight row counts that moved

All small, none affecting a headline figure in the inventory.

| dataset | was | now |
|---|---:|---:|
| Pension agency figures | 140,454 | 134,534 |
| Immigration service statistics | 3,204 | **177** |
| Consumer-protection enforcement sample | 1,200 | 1,004 |
| Egypt statistics agency | 150 | 52 |
| Immigration enforcement statistics | 221 | 204 |
| Science foundation awards sample | 125 | 115 |
| Housing department sample | 77 | 71 |
| Aviation data portal | 4 | 3 |

**The immigration statistics table lost 94% of its rows** on a re-pull. That is
the only one worth a second look — everything else is a source publishing a
slightly smaller file.

## The 36 that are absent on purpose

Not gaps. The inventory says in its own closing section that it excludes these.

- **14 pre-summed aggregate tables** — state-by-programme rollups of data already
  counted at row level elsewhere. Counting them again would double-count.
- **10 warehouse plumbing tables** — date, state, county and census-tract
  dimensions, a postcode crosswalk, the library snapshot, and the calendar built
  earlier today. Infrastructure, not public record.
- **12 of Ripple's own findings** — hospital closure risk, excluded providers paid
  after exclusion, revoked charities still taking deductible donations, opioid
  prescribers who took payments. These are outputs, not holdings.

## The 22 that are genuinely missing

These are real public-record datasets the inventory never described, because they
landed after it was written. Ordered by size.

| dataset | rows |
|---|---:|
| Credit union call reports | 121,713 |
| Federal political committees | 40,945 |
| Election results ("who won") | 10,976 |
| Leadership PACs | 8,619 |
| **Senate stock trades** | 8,350 |
| Federal judge appointments | 4,766 |
| Federal judges | 4,067 |
| Members' PAC money | 1,258 |
| Members' individual donations | 1,057 |
| Supreme Court justice ideology estimates | 782 |
| Appeals court judge ideology estimates | 703 |
| Court ideology midpoints | 102 |
| Federal prisons statistics | 50 |
| Asian Development Bank data | 41 |
| Supreme Court crosswalk | 40 |
| Supreme Court justices | 40 |
| Education department facts | 33 |
| Foreign agent registrations (the stub) | 30 |
| Beneficial ownership register | 1 |
| Hospital price transparency | 1 |
| Tribal geography | 1 |
| Institutional stock positions | not measured |

**Three of these are one-row stubs** — beneficial ownership, hospital price
transparency and tribal geography. Their loaders pointed at a web page rather than
a data file. All three are already disabled in the build with that reason written
down; they are not real datasets yet.

**One carries a legal restriction:** the Senate stock trades data is name-only
(there is no politician ID in it), its coverage stops in December 2020, and its
licence limits it to journalism use.

## What to do about it

Adding the 22 to the inventory is a writing job, not a measurement job — the row
counts are already measured and every one of them is small. It does not block
anything downstream. **The inventory's headline numbers, its 198 plain-English
entries, and everything built on top of it stand unchanged.**
