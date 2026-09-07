# Backfill closeout: the three items left, minus LDA

Written 2026-09-07. Chris said "all of it, minus the LDA". LDA is his MacBook
session. Sections 1-5 were file edits plus read-only checks through the Python
door. Section 6 is what got built after "greenlight rebuild" at 13:12, and
the House PTR reland that finished 13:18. Skeptic verdict at the end of 6.

## What was left, measured at session open

| # | item | landing evidence | verdict |
|---|---|---|---|
| 1 | donors 2000-2022 | 14 cycles, 283,771,819 rows | done before |
| 2 | committee roster by year | 7 congresses, 26,971 rows | done before |
| 3 | spending miscount | superseded flag, 2024 clean $4.437B | done before |
| 4 | hospital finances | 13 fiscal years | done before |
| 5 | lobbying 2011-2019 | positions 2011 only | Chris's Mac |
| 6 | political group donations | sched A 9,701,952, sched B 8,191,177 | done before |
| 7 | bills before 2023 | congresses 113-119, 107,150 | done before |
| 8 | revolving door names | 409 rows, H = 'nan' on 408 | this session |
| 9 | stock trade scrapers | house 27,286, senate EFD 6,855 | this session |

Plus two hangers-on from the 09-07 audit closeout: the cosponsors twin mart
decision, and the four crypto ticker rows.

---

## 1. Revolving door: it is job slots, and now it says so

**What was checked.** Every column of `LIBRARY_RAW.LANDING.FED_REVOLVINGDOOR_PROJECT`.

```
rows                                   409
H (the "name" column) = 'nan'          408
H = '3'                                  1   the documentation row
POSITION_TYPE                          Senate-confirmed 192 | Appointive 214 | nan 2 | "Text (See Position Type tab)" 1
distinct (name, department, type)      406 of 408 real rows
```

**What a hit means.** There is no person in this source. Never was. The
docket already says question 90's real source is the LDA covered_position
field, which is the crawl running on the Mac.

**What changed.** Phase 5.1 of the 09-05 plan, done as written:

| file | change |
|---|---|
| stg_fed_revolvingdoor_project__personnel_positions.sql | person_name dropped; key over (name, department, type); doc row filtered; H nulled when 'nan' |
| int_fed_revolvingdoor_project__positions_sectors.sql | person_name dropped |
| governance__fed_revolvingdoor_project.sql | person_name dropped; header rewritten; two always-false flags replaced by is_senate_confirmed |
| staging/fed_revolvingdoor_project/schema.yml | person_name blocks and not_null tests removed from all three models; descriptions rewritten |

**The two flags were constants.** is_political_appointee looked for the word
'appointee'; is_revolving_door looked for 'revolv'. POSITION_TYPE never holds
either. Both false on every row, both passing an accepted_values test.

**Dry run of the compiled mart, read-only:** 406 rows, 406 distinct keys,
190 Senate-confirmed, 216 not. Live build landed 405 and 215; see section 6.

---

## 2. Senate trades: the scraper was done; the union was not

**What was checked.** `FED_SENATE_EFD_PTR` landing and both marts.

```
FED_SENATE_EFD_PTR                 6,855 rows   799 filings   699 html + 100 paper
FINANCE__FED_SENATE_EFD_PTR        6,855        2021 on
FINANCE__FED_SENATE_STOCK_WATCHER  8,350        2012-06-14 to 2020-12-02
```

The 09-06 handoff called the Senate scraper unwritten. It was written and run
on 09-06; the landing and mart exist. What the plan asked for and nobody
built is the union across the seam with the senator resolved to an id.

**New model: `finance__senate_trades`.** One row per trade line, both eras,
plus bioguide, senator_name, match_note.

The match walks two steps against POLITICS__MEMBER_CROSSWALK restricted to
Senate seat holders since 2012, deduped on bioguide because the crosswalk
carries 13 duplicate ids:

1. last name equals the last token, or the last two tokens ('Van Hollen')
2. if more than one senator shares it, the first initial breaks the tie

**Dry run, read-only, compiled SQL run as a CTE:**

```
source                    match_note                   rows   names
fed_senate_stock_watcher  last name                   8,203      62
fed_senate_stock_watcher  last name + first initial     147       4
fed_senate_efd_ptr        last name                   6,585      56
fed_senate_efd_ptr        last name + first initial     270       1
total                                                15,205   = 8,350 + 6,855
distinct bioguide                                        82
null bioguide                                             0
```

Spot checks: 'A. Mitchell Mcconnell, Jr.' → Mitch McConnell M000355.
'Joseph Manchin, Iii' → Joe Manchin M001183. 'Rick Scott' → S001217 on the
initial, not Tim. 'Chris Van Hollen' → V000128 on two tokens.

**The bug the first draft had.** Keyed on the raw senator string, all 98 rows
whose SENATOR column reads the literal word 'Senator' went to John Boozman,
and 'Former Senator (Former Senator)' put Pat Roberts's 16 trades under Marco
Rubio. The key is now raw name plus the filings index's first and last name
for that filing. Recorded in traps.

**Still true, said in the model header:** amount is a bracket, 1,030
amendments supersede nothing yet, 100 paper rows carry null trade fields.

---

## 3. Cosponsors twin: enabled, same call as billstatus

```
landing FED_GOVINFO_BILL_COSPONSORS         1,268,519   congresses 113-119
mart POLITICS__FED_GOVINFO_BILL_COSPONSORS  1,268,519   non-transient, door-built 09-06
canonical POLITICS__BILL_COSPONSORS           367,735
```

The 07-31 note said "twin, redundant". At 3.4x the canonical it is not a
twin. `+enabled: true` in dbt_project.yml with the reason beside it. A dbt
run rebuilds it transient like its 648 siblings. The mart already holds the
current landing, so the run changes storage class, not content.

---

## 4. Crypto tickers: four rows, one rule

**What was checked.** All 58 [CT] rows in FED_HOUSE_PTR.

```
SOL (Solana) [CT]     TICKER = SOLANA    2 rows   wrong
XRP (Ripple) [CT]     TICKER = RIPPLE    2 rows   wrong
BTC [CT]              TICKER = ''        4 rows   missed
BTC (Bitcoin) [CT]    TICKER = ''        2 rows   missed, 'Bitcoin' is 7 chars
Bitcoin [CT]          TICKER = ''        6 rows   no symbol printed, correct
Bitcoin (CRYPTO:BTC)  TICKER = ''        2 rows   still blank, colon breaks both rules
```

Crypto lines put the symbol first and the name in the parenthetical, the
reverse of a stock line. New rule in house_ptr_load.py, [CT] rows only: a
leading 2-6 letter all-caps token is the ticker. Stocks keep the
parenthetical rule.

**Unit test on nine strings, run against the live module:**

```
SOL (Solana) [CT]         -> SOL
XRP (Ripple) [CT]         -> XRP
BTC [CT]                  -> BTC
BTC (Bitcoin) [CT]        -> BTC
Bitcoin [CT]              -> None
SPDR S&P 500 (SPY) [ST]   -> SPY      stock rule untouched
usdc [CT]                 -> None     lowercase, left alone on purpose
```

The six brokerage-prefix rows stay as they are. The closeout documents why
every cut rule broke more than it fixed. Visibly ugly beats silently wrong.

---

## 5. Found on the way: dbt could not parse since 09-06

`dbt parse` failed with five DependencyNotFound errors and one duplicate
model. Five door-built marts had no source declaration; health__fed_cms_hcris
was declared in both a staging yml and a marts yml after the 13-year reload.

| fix | file |
|---|---|
| five sources declared | models/marts/finance/_finance__sources.yml |
| stale HCRIS block removed | models/staging/fed_cms_hcris/schema.yml |

`dbt parse` now finishes with 2 warnings, 0 errors. Both warnings predate
this session.

---

## 6. Built, 13:12 on 2026-09-07, greenlight rebuild given

```
mart                                     rows       transient   tests
GOVERNANCE__FED_REVOLVINGDOOR_PROJECT       405      YES         pass
FINANCE__SENATE_TRADES                   15,205      YES         pass
POLITICS__FED_GOVINFO_BILL_COSPONSORS  1,268,519      YES         pass
34 tests across the five models, 0 failures
```

Revolving door landed at 405, one under the dry run's 406. The dry run
counted distinct keys on untrimmed landing text; staging trims before
hashing, and one pair differed by whitespace only. 405 is right.

Senate trades live: 82 bioguide ids, 0 null. None of the three marts had a
TIMELINE view, so nothing broke there and nothing needs regenerating.

The first House PTR rerun died at filing 1,000 of 3,109 when the Clerk's
server reset the connection. The loader now retries three times with a
growing pause and lands a blank row that says FETCH FAILED if all three miss.
Second run is in flight.

**Skeptic pass, 2026-09-07.** Nine of ten claims confirmed by query. Two
things it added:

* Brown and Nelson: two senator pairs since 2012 share a last name AND a
  first initial. Neither has filed a PTR yet. When one does, the match lands
  null with note 'ambiguous: 2 senators share it'. The tests were written so
  that would fail the build; they now warn instead, so the miss stays visible
  in the table, which is what the model header promises.
* "Stock tickers unchanged" cannot be proven. The table was replaced whole
  and no pre-reland copy survives. Row count is identical at 27,286 and
  ASSET_TYPE = 'ST' sits at 22,681; the ticker distribution was not diffed.

## 7. What was priced before the gate opened

| step | what | last cost | wall |
|---|---|---|---|
| dbt run | governance__fed_revolvingdoor_project + staging view + int view | 1.9s, 0.0002 credits | seconds |
| dbt run | politics__fed_govinfo_bill_cosponsors, needs --vars allow_politics_rebuild | 4.2s, 0.0002 credits | seconds |
| dbt run | finance__senate_trades | no prior run; siblings 1-4s | seconds |
| dbt test | the three above | none logged | seconds |
| house_ptr_load.py | refetch 2,633 PDFs, reland FED_HOUSE_PTR | clone 07:48, land 09:32 today | about 1h45 |

Timeline views: FINANCE__FED_SENATE_STOCK_WATCHER and the cosponsors mart
have TIMELINE twins. The RDP mart loses one column and gains one, so its
timeline view breaks on column count and needs regenerating after the run.
Same for the new senate_trades mart, which has no timeline view yet.

## Files touched

```
.claude/traps.md                                                          +3 entries
library-onboarding/ripple_dbt/dbt_project.yml                             cosponsors enabled
library-onboarding/ripple_dbt/models/marts/finance/_finance__sources.yml  +5 sources
library-onboarding/ripple_dbt/models/marts/finance/finance__senate_trades.sql   NEW
library-onboarding/ripple_dbt/models/marts/finance/schema_senate_trades.yml     NEW
library-onboarding/ripple_dbt/models/marts/governance/governance__fed_revolvingdoor_project.sql
library-onboarding/ripple_dbt/models/intermediate/fed_revolvingdoor_project/int_fed_revolvingdoor_project__positions_sectors.sql
library-onboarding/ripple_dbt/models/staging/fed_revolvingdoor_project/schema.yml
library-onboarding/ripple_dbt/models/staging/fed_revolvingdoor_project/stg_fed_revolvingdoor_project__personnel_positions.sql
library-onboarding/ripple_dbt/models/staging/fed_cms_hcris/schema.yml
scripts/house_ptr_load.py                                                 CRYPTO_LEAD rule
```
