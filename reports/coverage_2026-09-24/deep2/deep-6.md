# Deep pass 6: super PAC spending, audit partners, 13F holdings, Senate trade filings, Senate trades

2026-09-24. Python door, tag `coverage-r2-2026-09-24`. **35 of 35 statements**, all logged in `deep-6.sql`, none failed.
Every person, group or company named here is a data match. None is checked against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| FINANCE__FED_PCAOB_FORM_AP_FILINGS | **live** | One partner signed 84 to 165 public-company audits a year, 2019-2023. The median partner signs 1 | The data flagged B F Borgers years before the SEC shut the firm. His 218 clients scattered: 135 never filed a new audit, and the rest went to one-partner shops that now sign 19-39 audits a year |
| FINANCE__FED_SENATE_EFD_PTR | **live** | 701 of Armstrong's 703 trades were filed 112-119 days after the trade. The limit is 45 | Late STOCK Act filings are still happening in 2025-26: Armstrong, Mullin (46 trades over a year late), Britt, Sheehy |
| FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES | probed | Outside money beat the candidate's own spending in 104 of 637 House and Senate campaigns in 2024 | Real, but it's the famous Senate races. ⚠ $115B of crank filings sit in 29 rows |
| FINANCE__SENATE_TRADES | dead | Health: 73% of trades came from HELP/Finance members, against a 37% base. Per senator it's about 11% vs 9% | The committee overlap comes from trade volume, not stock picks. The 2012-20 banking finding doesn't hold for 2021-26 |
| FINANCE__FED_SEC_13F_HOLDINGS | dead | 3.1% of pre-2023 filings typed dollars into a thousands field. Those rows are 89% of the summed value | The "impossible wealth" is a units artifact. Five filing windows are also missing |

---

## 1. PCAOB Form AP: **live**

**Checked**
- 155,384 rows. Operating-company audits only (not funds, not benefit plans), newest version of each filing (`LATEST_FORM_AP_FILING = '1'`). Counted distinct issuers per lead-partner ID per audit-report year.
- Peers: 33,373 partner-years, 2017-2025. Median 1 issuer, p99 12. Only 134 partner-years reach 20+.
- **One partner ID, 0504100001, B F Borgers CPA PC:** 51 (2017), 78, 84, 95, 121, 162, **165 (2023)**, 88 (2024). The firm had one lead partner in 2024.
  - Background, not from the warehouse: the SEC charged Borgers in May 2024 and barred him.
- **Where his clients went.** 218 operating companies were audited by Borgers in 2023-24.
  - 135 (62%) have no Form AP from any other firm dated 2024 or later.
  - The 83 that moved went mostly to small shops:
    - Fruci & Associates: 9
    - Boladale Lawal & Co (Lagos): 9
    - Bush & Associates (Las Vegas): 7
    - Michael Gillespie: 6
    - M&K: 4
    - Victor Mokuolu, BCRG, Beckles: 3 each
- **The heavy one-partner shops, 2024-25.** 57 of 7,437 partner-years had 15+ audits:

```
partner            firm (city)                         yr    audits  firm's lead partners
Temitope Oyebola   Olayinka Oyebola & Co (Lagos)       2024    39      1
Victor Mokuolu     Victor Mokuolu CPA (Houston)        2025    36      2   (33 in 2024, 1 partner)
Chase Bush         Bush & Associates (Las Vegas)       2025    34      1   (28 in 2024)
Boladale Lawal     Boladale Lawal & Co (Lagos)         2025    34      1
Lateef Awojobi     LAO Professionals (Lagos)           2025    19      1
Xiaolu Li          YCM CPA (Irvine)                    2024    19      1
Benjamin Chung     BCRG Group (Irvine)                 2025    19      1
```

- **Trend.** Partner-years with 20+ audits at firms with 1-2 lead partners:
  - 2017-2022: 1 to 3 a year.
  - 2023-2025: 4 to 5 a year.
  - Audits signed by those partners: 87, 23, 21, 50, 30, 187, 235, 210, 124.
- **Rotation side-check.** 45 partner-company pairs ran 6+ straight fiscal years; the rule allows 5.
  - 18 of those 45 sit at firms too big for the small-firm exemption. They include EY/Vir 2018-23, PwC/Tenneco 2016-21 and PwC/J.Jill 2015-20.
  - Boring explanation for those 18: pre-IPO years, 52/53-week year ends and reissued reports. Small. Not chased.

**Hit means:** the Borgers shape is still out there: one partner signing 30-40 public-company audits a year. Some of those firms took Borgers' own former clients.

**Miss means:** these would be normal-size practices. They aren't: every name above is a firm with one lead partner, against a peer median of 1 audit a year.

**Boring:**
- Tiny shell companies legally use cheap auditors, and nothing caps how many audits one partner signs. **Not ruled out.** That's the hinge.
- Marcum and Withum partners hit 50-111 in 2020-21. That's the SPAC boom. **Ruled out** as a lead: big firms, and known.
- "No later Form AP" for 135 Borgers clients could mean they went dark, deregistered, or haven't filed yet. **Never build on absence.** The load itself looks complete: 2025 has 8,616 issuer rows against 8,734 in 2024.
- No PCAOB or SEC enforcement table is in the warehouse, so none of these firms was checked for sanctions.

**Traps**
- One partner ID carries three spellings: "Ben Borgers", "Borgers Ben", "Borges Ben". Group on `ENGAGEMENT_PARTNER_ID`, never on names.
- Rows dated 2014-2016 are reissued old reports. Form AP starts in 2017.

---

## 2. Senate eFD trade filings: **live**

**Checked**
- 6,855 lines, 799 filings, trades 2020-02 to 2026-08.
  - 1,030 lines are amendments, which re-file old trades and look late.
  - 100 lines are paper filings with no trade detail. 69 of them are Blumenthal's.
- Only original online filings, trades from 2021 on: **5,679 lines, 637 filings.** Of those, 1,023 lines (18.0%) in 52 filings (8.2%) were filed more than 45 days after the trade.
- Most heavy filers take a median of 20-35 days, which fits a real filing date.
- Late lines by year filed:

```
filed   lines   late>45d   late without Armstrong   late filings
2021     614      159            159                    14     (Tuberville's 132-line filing)
2022     907       31             31                    11
2023   1,029       11             11                     4
2024     943       43             43                     7
2025     850       59             59                    10
2026   1,383      739             38                    10
```

- **Named, one filing each unless noted:**
  - **Armstrong:** one filing, 2026-07-21, with 703 lines.
    - 654 buys of about 346 tickers, March 27-31, 2026.
    - 47 full sales, March 24-27.
    - 701 of the 703 lines were filed 112-119 days after the trade, worth $3.2M to $16.1M.
    - The 2 on-time lines are June sales of Williams (WMB): $5M-$25M of stock and $250K-$500K of options.
  - **Mullin:** three filings on 2025-07-30, 08-12 and 08-13, covering 48 trades from 2023-24. 46 lines are more than a year late, up to 953 days. At least $1.74M in late lines.
  - **Britt:** 22 of her spouse's stock trades, April-November 2025, filed 2026-01-26. Up to 287 days late.
  - **Sheehy:** 5 lines of non-public stock, at least $553K, June-November 2025, filed 2026-08-13. Up to 423 days late.
  - **Fetterman:** 31 lines for his child's bonds and stock from 2023, filed 2024-08-13. Up to 567 days late, at least $59K.
  - **Hickenlooper:** 20 late lines, at least $1.7M, 8 of them over a year late.
  - **Lummis:** 4 late lines, at least $3.05M.
- **Method check:** Tuberville's 132-line filing (2021-07-23, trades January-May 2021) is the case the press reported in 2021. The query finds it exactly.

**Hit means:** named senators disclosed trades months past the STOCK Act's 45-day limit in 2025-26, and the data dates each one.

**Miss means:** FILED_DATE would be a scrape date, not the filing date. The 20-35 day medians and the Tuberville match argue against that.

**Boring:**
- **Armstrong is unresolved.** If he was sworn in after March 31, 2026, the March trades belong on his entry report, not a PTR, and nothing is late. The deeper pass checks his TERM_START first.
- Late filing is a known genre. Tuberville 2021 and Lummis are already reported. The fresh names are 2025-26: Mullin's batch, Britt, Sheehy, Armstrong.
- The usual penalty is small, a $200 late fee. That's general knowledge, not from the warehouse.

**Traps**
- Drop `IS_AMENDMENT = 'True'` before measuring lateness. With amendments in, every Perdue line reads "late": 271 lines, all 2020 trades re-filed.
- Armstrong's filing comment says every trade is held jointly with his spouse, but `OWNER` says Self on 701 lines.

---

## 3. FEC independent expenditures: probed

**Checked**
- 276,183 rows, one file per cycle, 2018-2026.
  - 35,141 rows are superseded.
  - 33,937 rows have a blank CAND_ID.
  - `EXP_AMO` is text.
- ⚠ **Crank filings.** 29 rows of $100M or more carry **$115.4B**, which is 90% of all non-superseded dollars.
  - The filers are named "The Committee of 300", "The Court of Divine Justice", "Warren Buffet Apple Inc.", "Tanking", "Republican Emo Girl", and "Gus Associates" (for Walter White). One row lists SpongeBob SquarePants as the candidate.
  - `IS_SUSPECT_FILING = 'True'` marks every one of them.
  - Totals after dropping those rows: 2018 $1.30B, 2020 $3.33B, 2022 $2.31B, 2024 $4.44B, 2026 so far $1.05B.
- **Outside money vs the candidate's own spending, 2024 House and Senate.** Built from non-superseded lines under $50M, deduped on group + candidate + amount + dates + payee.
  - 702 candidates had outside money.
  - 637 (90.7%) matched the FEC candidate summary. 624 of those 637 (98%) agree on last name.
  - For 104 of the 637 (16%), outside money beat the campaign's own spending. For 82 of them, the outside money was over $1M.

```
candidate          outside for / against    own spend   ratio
Moreno (OH-S)        $66.5M / $85.5M          $26.4M     5.8x
Rogers (MI-S)        $24.1M / $39.1M          $13.0M     4.9x
McCormick (PA-S)     $29.1M / $77.4M          $35.4M     3.0x
Mackenzie (PA-H)      $0.5M /  $9.8M           $1.7M     6.0x
Coughlin (OH-H)       $0.6M /  $7.4M           $1.6M     5.0x
```

- **Losing bets.** $921M of the $2,104M (44%) either backed someone not in Congress now or opposed someone who is.
  - WinSenate: $177M of $310M lost.
  - HMP: $89M of $196M.
  - Last Best Place PAC: $33.8M, all lost. It spent $32.0M against Sheehy, who won.
  - Maryland's Future: $27.0M, all lost. It spent $26.7M against Alsobrooks, who won.
  - Second-field check: candidate names and sides agree with the IDs for all four groups checked.
- **Own-party primary attacks, 2020-26:**
  - Win It Back PAC, which leans Republican by its own money: $7.9M against 5 Republicans in 2026 primaries (Barr, Burks, Cain, Carter, Collins).
  - Women Vote!: $2.55M against Trone in 2024.

**Hit means:** there are real outside-vs-inside ratios per race, and a clean join through the FEC candidate summary and the legislators' FEC IDs.

**Miss means:** the join would fail. It doesn't: 90.7% land and 98% of those agree on name. The numbers just aren't news.

**Boring:**
- The famous Senate races top every list, and OpenSecrets publishes outside-vs-candidate spending. **Not ruled out.** That's why it's probed.
- Every race has money on both sides, so a 44% loss rate says nothing on its own.
- "In Congress now" stands in for "won" and blurs primary losses with general losses.

**Traps**
- ⚠ Filter on `IS_SUSPECT_FILING = 'False'` or cap the line amount, or every total is 10-30x too high.
- Superseded rows also carry $16.1B, mostly crank refilings.
- Name style varies: Bob Casey appears as "Robert, P.".

---

## 4. Senate trades, 2012-2026: dead

**Checked**
- 15,205 rows. 8,350 come from the Stock Watcher feed (2012-2020). 6,855 come from eFD (2020-2026), the same rows as table 2 with BIOGUIDE added.
- **Names:**
  - 2021 on: all 55 raw-name-to-senator pairs are correct.
  - Stock Watcher era: the 427 rows where the raw name doesn't contain the matched first name are all nicknames (John F Reed = Jack Reed, William Cassidy = Bill Cassidy, Rafael E Cruz = Ted Cruz).
  - Zero same-surname mixups found.
- **Committee join, 2021-26.** Original filings, 3,902 ticker trades. 3,038 (77.9%) got a SIC code through the EDGAR tickers and financials tables. Committee rosters cover the 117th-119th Congress.

```
sector        trades   by members of overseeing cmte   base: trading senators on it
health          311          73.3%                          36.6%
defense          67          41.8%                          28.7%
energy          126          41.3%                          39.6%
agriculture     102          29.4%                          22.8%
tech/telecom    766          24.7%                          32.7%
transport       102           5.9%                          32.7%
banking         236           4.7%                          23.8%
```

- **Health per senator.** Health's share of each senator's own coded trades:
  - HELP/Finance members, median about 11.6%: Tuberville 9.6%, Armstrong 13.3%, Mullin 11.3%, Carper 7.5%, Whitehouse 11.9%.
  - Non-members, median about 9.2%: Capito 8.0%, Boozman 9.8%, Sullivan 14.3%, King 9.3%.

**Hit means:** committee members would pick their own turf's stocks.

**Miss means (this is what we got):**
- The 73% comes from heavy traders who happen to sit on HELP or Finance, not from stock picking. Tuberville alone has 1,028 coded trades.
- Banking members made 4.7% of bank trades against a 23.8% base, so the 2012-20 banking finding doesn't carry forward.
- The one outlier is Tina Smith: 12 of 16 coded trades are health, mostly medical devices. Tiny, and probably her home state's industry.

**Boring:**
- Armstrong's 48 "health" trades were part of a 654-stock buying spree in one week.
- The LDA same-quarter lobbying angle was not run. It needs a fuzzy issuer-name join.

**Traps**
- ⚠ **2020 is double-counted.** 482 of the 537 eFD rows from 2020 also sit in the Stock Watcher feed: same senator, date, ticker and amount band.
- `MATCH_NOTE = 'last name'` describes the matching method. It doesn't flag an error.

---

## 5. SEC 13F holdings: dead

**Checked**
- 101.3M rows.
  - The quarterly zips 2013q2-2022q3 are in thousands.
  - 10 date-range zips, January 2024 to May 2026, are in dollars.
  - `VALUE_USD` is already converted to dollars.
- **Missing filing windows:** 2021q3, 2021q4, 2022q4 and all of 2023.
- **Units errors.** 174,191 filings from the thousands era.
  - 5,323 of them (3.1%) have a row whose value implies a share price over $20,000. Berkshire A is excluded.
  - Those rows sum to **$13,876T of the era's $15,513T (89%)**.
  - Biggest offenders:
    - Schroder, 2013q4: one filing, $2,895T.
    - UBS Asset Management Americas: every quarter 2019q2-2022q3, $128-253T each.
    - MFS: 2013-2015, $142-194T each.
- The dollars era looks sane: no row over $1T, and the biggest is $553B.

**Hit means:** nothing. The triage's "impossible values" angle is this data error.

**Miss means:** n/a.

**Boring:** a filer typed dollars into a thousands field. That's the whole story. "Who held what before big moves" needs a price table. That wasn't checked.

**Traps**
- ⚠ Flag any row with value ÷ shares over $20,000 in the thousands era before summing anything.
- `SRC_FILE` is the filing window, not the report quarter. UBS's 2020q4 report shows up again in the 2021q1 zip under a new accession number, with identical rows. Dedupe restatements through `FINANCE__FED_SEC_13F_SUBMISSIONS`.
- Five filing windows are missing. Any time series across 2021-2023 has holes.

---

## New data traps (for the trap file)

1. **FEC independent expenditures:** 29 crank rows carry $115B, 90% of all dollars. `IS_SUSPECT_FILING = 'True'` marks every one.
2. **Senate trades:** 2020 is double-counted across the two feeds (482 of 537 eFD rows).
3. **13F:** 3.1% of thousands-era filings typed dollars, and they hold 89% of summed value. Filing windows 2021q3, 2021q4, 2022q4 and all of 2023 are not loaded.
4. **Senate eFD:** amendment lines re-file old trades and fake lateness. Drop them first.
5. **PCAOB:** one partner ID carries several name spellings. Group on the ID.

## Open for the deeper pass

- Armstrong's swearing-in date (`POLITICS__FED_CONGRESS_LEGISLATORS.TERM_START`). This decides whether 701 lines are late at all.
- The one-partner audit shops: pull their 2024-25 client lists and check how many are shells or former Borgers clients. Then check PCAOB sanctions outside the warehouse.
