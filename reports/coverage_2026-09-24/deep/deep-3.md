# Deep pass 3: five tables, 2026-09-24

Agent: deep-3. Door: Python. Read-only. **31 of 35 statements used** (one failed on a regex typo and is counted). SQL: `deep-3.sql`.
Every person or company named here is a **data match, not verified against primary records**.

## The menu

| Table | Verdict | The one number |
|---|---|---|
| FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES | **live** | 19 police, fire, veteran and cancer 527s spent **$201.8M**: **74%** went to fundraising-type costs, **$0.2M** to candidates. Four of them share one Wisconsin address or its next-door town ($114.7M). |
| FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE | probed | 2024 Senate general: **$516.1M** of outside money backed the loser, against $675.2M that backed the winner (43% on the losing side). |
| ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS | probed | Forest County PA: **1,685 orphan wells per 10K people**. No operator column exists. |
| ENVIRONMENT__FED_USCG_NRC_INCIDENTS | probed | In 2015-17, CSX plus Norfolk Southern made **8.2x** the NRC calls of UP plus BNSF. By 2024-25 that was 1.8x. The table has no material, amount or spill location. |
| FCT_DATASET_SIZE_HISTORY | probed | Data set 10 fell from about 10,071 pager pages to **5,569** on 2026-03-11 and held for 10 snapshots. But DS9 and DS11 made drops just as big that came back. |

**Bad news for triage:** two of the "boring" explanations rested on fake numbers from `facts.tsv` (see Traps). The "SEQNOS 999999 sentinel" and the "434-row repeated API ids" don't exist.

---

## 1. IRS 527 Schedule B (payments by 527 groups): LIVE

**Headline:** The triage question was who gets the $13.3B. Mostly card processors, credit cards and party ad buyers, which is boring. The pivot is live: a cluster of police, firefighter, veteran and cancer 527s that spend on telemarketers, not candidates.

**Checked**
- 8,191,177 rows, SCHEDULE_ID unique, 40,715 forms, 3,313 EINs, $13.316B, 2001-01-01 to 2026-08-27.
- Amendment copies: grouped by EIN + payee + date + amount and counted forms. **$2.02B** sits in the same payment copied onto a second form. Dropping copies leaves **$11.269B** (-15.4%). Another $0.367B repeats within one form; I kept it, since it could be real repeat payments.
- The $1.47B lump-row trap is **Schedule A**, not B. On B, lump-named rows ("AGGREGATE", "TOTAL", "SUM OF TRANSACTIONS", "BELOW THRESHOLD") add up to about $0.3B.
- ActBlue Non-Federal: **6,703,918 rows (82% of the table)**, $976.3M, median $25, 91% with a "contribution" purpose. It's a pass-through to state candidates, and it's why the table median is $25.
- Top payees after dropping copies:

| Payee | $M | Who pays |
|---|---|---|
| Stripe | 173.8 | ActBlue Technical Services, 100% |
| American Express | 165.0 | 175 groups, both parties |
| Target Enterprises (2 spellings) | 152.3 | RGA, 97% and 78% |
| Great American Media | 141.8 | DGA is top payer, 17 groups |
| RGA Right Direction PAC | 130.7 | RGA's own affiliate |
| Worldpay | 101.9 | ActBlue Technical Services |
| Mentzer Media | 72.2 | GOP-side groups |
| Pinpoint Media | 61.8 | RGA 90% |

- Payee name = an officer of the same group: 1,257 pairs, **$79.7M (0.7%)**, all salary and expense reimbursement. Boring.
- **The pivot:** each group's spending (copies dropped) was split into fundraising-type purposes (keyword match) and contributions. Groups with $1M+ and over 50% fundraising were kept. Then I checked their raw purpose text and their Form 8872 custodians and addresses.

**What's there**
- 19 groups with police, firefighter, veteran or cancer names. **$201.8M spent 2014-2026. $149.5M (74%) to fundraising-type purposes. Each group 61-94%.** Candidate contributions: $0.2M total, 0-1% each.
- Raw purpose text agrees with the keyword match: "TELE FUNDRAISING", "TELEMARKETING", "CAGING AND ESCROW", "FUNDRAISING, DONOR MANAGEMENT, DATABASE SERVICES".
- Shared links on their own 8872 reports:

| Link | Groups | $M |
|---|---|---|
| 2301 Sun Valley Dr, Delafield WI (+ 200 S Executive Dr, Brookfield WI next door) | National Police Support Fund, American Veterans Honor Fund, Firefighters Support Fund, American Police Officers Alliance | 114.7 |
| Custodian Nile Porter | Firefighters Support Fund, Veterans Action Network | 41.1 |
| Custodian Matthew Greenlee | National Committee For Volunteer Firefighters, VF2024 PAC | 11.9 |
| Custodians Frank Pulciani / Albert Nizick | National Police & Sheriffs Coalition PAC, POSC PAC, American Coalition for Police & Sheriff's PAC | 10.8 |
| Same template: exactly 90% fundraising, BFTELECOM LLC as top payee, same purpose wording | 9 groups | 35.9 |

- Residential Programs Inc is the top payee of National Police Support Fund (38%, $12.7M). It is also a top payee of Committee for Police Officers Defense, Firefighters Support Fund and American Veterans Honor Fund.
- EINs came in batches: 843763242 / 843763411 / 843763606 and 923489519 / 923489713.

**Hit means:** a network of charity-sounding 527s, tied by shared addresses, custodians and vendors, sending most of $200M to telemarketers. On IRS forms, which is outside the FEC filings most trackers read.
**Miss means:** if the groups turn out to be already-covered FEC scam PACs under new names, it's a known story with fresh numbers.
**Boring:** "scam PACs" are a known genre. CNN (2020), The Daily Beast ("$140 million scam PAC network"), Jacobin (2024) and The Lever covered it, mostly from FEC data. Telemarketing-heavy spending is legal. "Bill Davis" as a shared custodian is too common a name to count. **Not ruled out** that some of these groups are already named in that coverage.

---

## 2. FEC committee to candidate: probed

**Headline:** the money is real and huge, but it sits with the super PACs the press already scores. The House half of "did it work" is blocked by a data gap.

**Checked**
- 866,730 rows, cycles 2024 and 2026, SUB_ID unique. Memo rows (MEMO_CD = 'X'): 18,643, all dropped.
- 2024, memo rows dropped: **24A against $2.535B** (17,682 rows), **24E for $1.888B** (51,571 rows), 24K direct contributions $508.6M.
- Top 2024 spenders: FF PAC $502.6M for (10% of the cycle, 3 candidates). MAGA Inc $319.3M against. WinSenate $287.1M against. CLF $200.7M against. SLF PAC $200.4M against. HMP $178.3M against. America PAC $99.6M for plus $74.2M against.
- Joined IE by CAND_ID → FEC candidate file (2024) → POLITICS__WHO_WON on state + office + district + surname. Second field: party matched on 30 of 32 winners and 24 of 25 runners-up.
- **WHO_WON stops early: House ends 2018, President ends 2016, Senate reaches 2024.** So the scoring below is Senate only.

**What's there (2024 Senate general, 24E + 24A, memo rows dropped)**
- **$675.2M backed the winning side, $516.1M backed the losing side, $30.2M unscored.** Denominator: scored Senate general IE, $1,191.3M. 43% was on the loser.
- By group: WinSenate put 59% on the losing side ($177.9M of $302.4M). SLF PAC: 29% ($60.7M). Last Best Place PAC 100% ($29.1M), Maryland's Future 100% ($27.0M), NRSC 99% ($21.2M), American Crossroads 0%.
- Most spent against a candidate who won anyway: McCormick $79.2M, Moreno $76.4M, Sheehy $58.6M, Slotkin $54.0M. Most against a candidate who lost: Sherrod Brown $115.1M, Casey $102.8M, Tester $61.1M.

**Hit means:** a per-group "money on the losing side" scorecard, which could extend to 2026.
**Miss means:** House can't be scored until WHO_WON gets 2020-2024 House results.
**Boring:** money goes to toss-up races, so a near 50/50 split is expected. OpenSecrets-style scorecards already exist. **Holds.**

---

## 3. USGS orphaned oil and gas wells: probed

**Headline:** county density per person is big and real. The "which bankrupt operators" angle is dead: no operator column exists.

**Checked**
- 117,672 rows, **117,669 distinct WELL_IDENTIFIER**. Only 3 IDs repeat, twice each (2 in Illinois, 1 in Missouri). The triage's "434-row repeats" don't exist.
- 27 states, one state file each, dated 2019-07-01 to 2022-12-10. It's one old snapshot.
- Distinct wells by county, share of own state, joined to DIM_COUNTY 2020 population. The join landed 116,636 of 117,669 wells (99.1%).
- Operator: the only mentions are notes. "Operator Unknown" on 3,594 rows (all West Virginia), "Orphan-No Responsible Operator" on 70.
- STATUS by state (see Traps): the list is not all orphans.

**What's there**

| County | Wells | Share of own state | Per 10K people |
|---|---|---|---|
| Venango PA | 4,786 | 25% of 19,160 | 949 |
| McKean PA | 3,299 | 17% | 816 |
| Allegany NY | 3,047 | 43% of 7,029 | 656 |
| Washington OH | 2,786 | 14% of 20,557 | 466 |
| Monroe OH | 1,996 | 10% | 1,491 |
| Forest PA | 1,175 | 6% | **1,685** |
| Nowata OK | 1,343 | 8% | 1,441 |
| Jackson MO (Kansas City) | 1,711 | 35% of 4,892 | 24 |

**Hit means:** a per-person orphan-well map. Rural Appalachian and Oklahoma counties carry more than one orphan well for every 10 residents.
**Miss means:** no operator names, and the snapshot predates most federal plugging money. No "who left them" story from this table.
**Boring:** counts reflect how hard each state looked. Appalachian orphan wells are widely reported. **Not ruled out.**

---

## 4. Coast Guard NRC incidents: probed

**Headline:** company repeat counts exist and peer outliers show. But this is only the call header: no material, no amount, no spill location, and half the rows have no company.

**Checked**
- 1,029,020 rows, 1990-01-01 to 2026-08-02, **one row per SEQNOS**. SEQNOS runs 1 to 1,469,629 in order. '999999' and its two neighbours appear on 3 rows total, all from 2012. **No sentinel.**
- Blank company: 378,690 rows overall, and **47.5% since 2015** (132,073 of 277,988). The blank share climbed from 19.4% (1990) to 49.8% (2025).
- Columns: company, the company's own city/state/zip, org type, time, source. The "linked material table" is not in the warehouse. The other NRC table is a 2020-2024 copy with the same columns.
- Grouped company names into families by name prefix, 2015-2025, compared within peer groups.

**What's there (calls 2015-2025)**
- Rail: CSX 1,806 · Norfolk Southern 1,690 · Union Pacific 396 · BNSF 271. Per year, CSX + NS made 511 calls vs 63 for UP + BNSF in 2015-17 (8.2x). In 2024-25 it was 140 vs 76.5 (1.8x). CSX went from 331 a year to 82 a year.
- Gulf offshore: Taylor Energy 1,079 (608 in 2015-17, 1 in 2024-25). Cox 797 (726 in 2018-23, 20 in 2024-25). Fieldwood 461 (1 in 2024-25). In 2021-23, Cox's 404 calls beat Chevron's 283 across 21 states.
- Majors: Shell 1,334 · Chevron 1,174 (79 spellings; the triage's 6.7K + 4.1K counts all years back to 1990) · Exxon 1,014.
- Pipelines: Targa 1,551 · Kinder Morgan 1,289.

**Hit means:** named peer outliers to chase: eastern railroads' call rate, and Cox Operating's 2018-23 surge.
**Miss means:** without the material and amount sheets, a call can't be sized. A sheen and a 10,000-barrel spill count the same.
**Boring:** these are self-reported calls, and reporting habits differ by company. CSX's 75% drop could be a change in who phones it in. Taylor's MC-20 leak is a famous story. **Not ruled out.**

---

## 5. DOJ Epstein page size history: probed

**Headline:** the pager count is too noisy to prove any file came down. One drop is unresolved.

**Checked**
- 339 snapshots, 12 pages (data sets 1-12), 2025-12-19 to 2026-06-03, 339 distinct page digests. Pulled every row and ordered it by page and time.
- APPROX_FILES_FROM_PAGER = PAGER_PAGES x 50 on every filled row. 57 are blank; DS6 and DS7 have no pager.
- The "533.9K max" is DS9 at 10,678 pages.

**What's there**
- **The pager glitches.** A reading of "2 pages" turns up at random on 10 of 12 pages. DS1 read 51 → 102 → 2 → 63 in one day. DS9 read 10,678 → 4,980 → 10,675 → 770 → 10,675. DS11 read 5,549 for a month, then 6,634 again.
- FILES_ON_PAGE_ONE fell by exactly one on 9 of 12 pages between 2026-02-03 and 02-09. On a list that runs past one page, a removed file is replaced by the next one, so page one can't shrink that way. That points to a site template change, not files removed.
- **Unresolved:** DS10 went from 10,071 pages (~503.6K files) to 5,569 (~278.5K) on 2026-03-11. It held on 10 snapshots through 2026-05-09. After that, only glitch readings ("2") came in.
- Tiny: DS6, a single page of 12-14 files, lost one more file on 2026-02-10 and got it back on 2026-03-19.

**Hit means:** if a real re-crawl confirms DS10 lost about 225K files, that's a disappearance on the record.
**Miss means:** it's the same glitch that hit DS11, which held a month and then reverted.
**Boring:** pager parse glitches. **Confirmed** on DS9 and DS11, and they explain the synchronized one-file drop. The next step is counting file links on every DS10 page, not more pager math.

---

## New traps

1. **`facts.tsv` "top" lines lie on unique columns.** facts.py uses APPROX_TOP_K, which invents counts when a column is nearly unique. NRC SEQNOS "999999 4.0K" is really 1 row. Wells WELL_IDENTIFIER "434 each" is really at most 2. Triage built two boring explanations on these.
2. **POLITICS__WHO_WON is not current for House or President.** House ends 2018, President 2016, Senate 2024.
3. **Orphan-well STATUS is not "orphan."** California: 3,173 of 3,338 are "Idle", plus 126 Plugged and 36 Active. New York: 2,085 "Unknown Not Found". Ohio: 15,493 of 20,557 are "HP" (historic production), only 877 "OR". Colorado: 186 of 409 are "PA" (plugged and abandoned). Texas: blank on all 5,854.
4. **527 Schedule B has $2.02B of cross-form copies** (amendments). ActBlue Non-Federal is 82% of its rows and is a pass-through. The $1.47B lump trap belongs to Schedule A.
5. **The NRC tables are call headers only.** No material, quantity or incident location was loaded.
6. **Epstein pager:** a reading of "2" is a glitch value, and the approximate count is pages x 50. Page-one counts shifted site-wide the week of 2026-02-03.

## Statement count
31 read-only statements (30 returned results; [27] failed on regex syntax and [28] reran it), plus two ALTER SESSION lines per connection.
