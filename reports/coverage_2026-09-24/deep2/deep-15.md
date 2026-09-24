# Deep pass 15: IRS 527 officers, and Texas lobby covers, entertainment, meals and trips

2026-09-24. Python door, tag `coverage-r2-2026-09-24`. **34 of 35 statements**, all logged in `deep-15.sql`. Each connection also ran the two ALTER SESSION lines; those aren't counted. One statement ([25]) failed on a column name and was rerun as [26]. It still counts.
Every person or company named here is a data match. None is checked against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| POLITICS__TX_LOBBY_TRANSPORTATION | **live** | $79,647.58: one April 2026 report. A private jet flew 8 people, including Sen. Angela Paxton and Reps. Brad Buckley and Caroline Fairly, to New York on March 30-31, 2026. Clients on the report: Success Academy and Kleinheinz Capital Partners | That's the 3rd-biggest transport total of 3,448 Texas lobby reports with any transport since 1991. The median is $188. The state bank commissioner also flew on the bank lobby's private planes in 2016, 2019 and 2022 |
| POLITICS__TX_LOBBY_COVER | **live** | Las Vegas Sands: $20.58M in "media" spending through one lobbyist, 2021-2026. That's 68.8% of all Texas lobby media dollars in those years ($29.9M) | Casino ad money dwarfs every other filer. 2025 alone: $9.50M, 67.9% of that year. Earlier ad blitzes of the same size came from the TXU buyout group ($11.58M in 2007) and cable companies ($10.74M in 2005) |
| POLITICS__TX_LOBBY_FOOD_BEVERAGE | probed | Hedge funds and banks paid for 2,114 of 14,448 itemized meals (14.6%). One man, Brad Gilbert, got 70 meals from 11 funds, $10.2K-$14.4K | The $78.7K "biggest meal" is a typo: the Austin ZIP 78701 went into the amount box. Otherwise it's small money, and the diners' jobs aren't in the table |
| POLITICS__IRS527_DIRECTORS_OFFICERS | probed | Noreen Fenner is an officer of 420 political groups (any spelling). 419 of them (99.8%) told the IRS they don't file money reports | The officer pile-up is real, but it's a treasurer-service job. The Schedule B join lands 3.0% at her address, against 5.3% for all 527s. Their money trail lives with Florida, not the IRS |
| POLITICS__TX_LOBBY_ENTERTAINMENT | dead | Top named official: John Whitmire, 35 outings worth $6,617-$8,367 over 2005-2021 | The whole table is $456K-$605K over 22 years. It itemizes only 6.9% of the entertainment dollars on the cover sheets |

---

## 1. Texas lobby transportation: **live**

**Checked**
- 3,697 travel lines, 621 reports, 281 lobbyists, 2004-2026. A recipient is named on 99.5% of lines.
- **This table has no dollar column.** You can't sum trips from it. The dollars sit on the cover sheet (`TOTAL_EXPEND_TRANSPORTATION`), one total per report. So I joined each trip's REPORT_ID to the cover's REPORT_INFO_IDENT for the dollars, and to `TX_LOBBY_INDIVIDUAL_REPORTING` for the client names.
- Private-air lines: 111 of 3,697.
- **The New York trip.** Report 101046715, Julie Linn Minnehan, LOBBYACTAPR 2026. It holds 15 private-air lines:
  - The dates: flew Austin or Fort Worth to New York on 2026-03-30, and back on 03-31. Everyone stayed at the New York Hilton Midtown for one night.
  - Stated purpose: "Educational tour and meetings."
  - The filing's titles: SENATOR Angela Paxton, REPRESENTATIVE Brad Buckley, REPRESENTATIVE Caroline Fairly. REPRESENTATIVE Jeff Leach has one leg and a note: "Did not fly."
  - Four more names have no title: Chris Duke, Jessica Diem, Marc Salvato, Sarah Harrington.
  - The report's transport total is $79,647.58. That's about $10K a head across 8 names, but the report doesn't split it.
  - Client lines on the report: KLEINHEINZ CAPITAL PARTNERS | SUCCESS ACADEMY. Clients are listed per report, not per line, so which client paid for the jet isn't shown.
- **Peers.** 3,448 cover reports ever show transport over $0. The median is $188. This report ranks **3rd**. Above it:
  - #1: Christian Bionat, March 2024, $156,254. It has zero itemized trip lines and no client line. Open question.
  - #2: Jeffrey Mendelsohn, 2011, $130,592. An AIPAC / American Israel Education Foundation "fact finding mission to Israel" for one official, Ms. Gonzalez.
- **The bank regulator.** Charles Cooper, titled COMMISSNR on some rows, flew on private planes paid by lobbyists:
  - 2016, Christopher Williston V: 15 lines on 3 reports. The client line reads IBAT. Report totals were $455, $4,157 and $4,695.
  - 2016, J. Eric T. Sandberg Jr.: 5 lines, $1,695.
  - 2019, Williston: 3 lines, $1,611, "IBAT regional meetings."
  - 2022, Stephen Scurlock: 1 line, $1,256.
  - Kurt Purdom, 2018, Williston: 21 private-air lines on 2 reports. It was a tour of the association's regional meetings, with reports of $2,622 and $2,738.
- **Resort conferences.** AGC of Texas lobbyists flew legislators and spouses to its yearly management conference:
  - Maui 2010: 12 people, a $69,860 report.
  - Banff 2007: 19 people, a $67,149 report.
  - Palm Beach 2019: Nichols and Whitmire by private air, a $50,962 report.
- **Also 2026:** Matthew Bentley's report flew Kelly Hancock and James Dyer by private plane from Fort Worth to Amarillo, to "tour the Fermi America site," then on to San Angelo. The report total is $7,922, with no client line.

**Hit means:** A Texas school-choice-era trip, in 2026, is the third-costliest lobby travel report in 35 years. It carries a senator, the reps on the filing and a charter network's name. A deeper pass would ask:
- Did the trip get reported in the news?
- Who owned the plane?
- What did these members vote on or carry afterward?

Separately, a bank regulator on the bank lobby's planes is its own small, clean story.

**Miss means:** If the $79.6K is a typo or covers more than this trip, the rank falls. That's ruled out as far as the table allows: the report's only transport lines are these 15 private-air legs.

**Boring explanation:** Texas lets lobbyists pay travel and lodging for officials who speak at or attend an event, as long as it's reported. This was reported. "Educational tour" trips are routine, and the AGC resort trips have run for decades. **Not ruled out:** the legality. What's news is the size and the client, not a broken rule.

---

## 2. Texas lobby cover sheets: **live**

**Checked**
- 283,803 reports, 1991-2026, from 8,952 lobbyists.
- REPORT_INFO_IDENT is unique: 283,803 of 283,803. The facts line said "10250 1.0K," which is a display artifact.
- Category totals are text. Parsed, they come to:

| Category | Total, all years |
|---|---|
| Media | $100.08M |
| Food | $64.19M |
| Entertainment | $10.50M |
| Gift | $5.11M |
| Transport | $4.25M |
| Event | $1.90M |
| Award | $0.60M |

- **Deduped** to the last-filed report per filer + year + report type. Raw and deduped differ by at most $0.02M in any year, so corrections don't double-count here.
- **Session cycle (food):** odd-year sessions run about 2-2.5x the off years. That's what a session calendar should do; it isn't a finding.

| Year | Food |
|---|---|
| 2021 | $3.02M |
| 2022 | $1.68M |
| 2023 | $4.27M |
| 2024 | $1.69M |
| 2025 | $4.21M |

- **Media is lumpy:** one filer-year often holds most of a whole year's media dollars.
- The **client join** (cover REPORT_INFO_IDENT to client-line REPORT_ID) on the big media filers:

| Lobbyist | Media $ | Years | Client (land rate) |
|---|---|---|---|
| Andy Abboud | $20.58M | 2021-26 | LAS VEGAS SANDS CORPORATION (62 of 62) |
| Clifford Angelo | $11.58M | 2007 | TEXAS ENERGY FUTURE HOLDINGS LP (4 of 4) |
| Kathy Grant | $10.74M | 2005 | Cox, Time Warner, Comcast, Charter, TX Cable & Telecom Assn (4 of 4) |
| Jeffrey Robinson | $10.50M | 1995-99 | none (0 of 13; client lines start in 2000) |
| Leslie Ward | $7.32M | 2005-06 | SBC / AT&T (8 of 13) |

- **Sands by year:**

| Year | Sands media $ | Share of that year's media |
|---|---|---|
| 2021 | $1.71M | 47.0% |
| 2022 | $3.33M | 96.6% |
| 2023 | $4.49M | 64.2% |
| 2024 | $1.47M | 89.5% |
| 2025 | $9.50M | 67.9% |

- **Second field:** every 2021-2026 report with media over $0, grouped by filer with its clients. Only Abboud's reports carry Sands, so the same ad buy isn't reported twice by two lobbyists.
- Next largest filers 2021-26: Google via Katharine McAden $2.12M, Texas Trial Lawyers Association $1.23M, Sarah Walker $1.20M (no client line), Americans for Prosperity via Samuel Sheetz $0.75M.

**Hit means:** One company's casino push is about two-thirds of all Texas lobby ad money for five years: $20.6M, mostly in the 2023 and 2025 sessions. The number sits in public filings. A deeper pass asks whether anyone has published the five-year TEC total, and lines it up against the casino bills' fate.

**Miss means:** If "media" meant something else, like a per-lobbyist salary share, the number would mislead. The category is the lobbyist's reported media and advertising spend. 12 of 12 Abboud reports in 2025 carry it.

**Boring explanation:** Sands' Texas casino push and its ads were covered by Texas press during both sessions. The biggest past spikes (TXU buyout 2007, cable franchising 2005) are also known fights. **Partly ruled out:** the idea that Sands is just one of many; it's 68.8%. Whether the total is already published is not checked.

---

## 3. Texas lobby meals: **probed**

**Checked**
- 14,452 itemized meals, 2004-2026. 71% give only a range; 4,207 give an exact amount.
- **The $78.7K meal is a ZIP code.** Report 604419, Tedrah Hutchins-Robertson, 2014-01-26, Levy Restaurant, Austin. It lists 11 guests on the same day:
  - Ten guests show $35.00 each.
  - One guest, Hunter Thompson, shows $78,701.00.
  - The restaurant's ZIP is 78701. Among rows of $10K or more, it's the only one where amount = ZIP.
  - Dropping it takes the exact-amount sum from $442,409 to $363,708.
- The next biggest rows are events filed under one name, not one person's meal:
  - $17,432 with the lobbyist himself as the recipient.
  - $16,399 for a "TPCA Legislative Barbeque."
  - $14,518 under Rick Perry's name at the Intercontinental.
- **Top officials** (rows under $10K; the exact amount, else the range low-high):
  - A blank last name tops the list at $32.9K-$42.6K.
  - Brad Gilbert: $11.0K-$16.1K.
  - Larry Taylor: $6.8K-$12.4K.
  - Lulu Llano: $10.2K-$12.3K.
  - John Whitmire: $7.6K-$11.2K.
- **Firm-paid meals.** Filers whose names end in LLC, L.P., Capital, Securities, Management and the like paid for 2,114 of 14,448 meals (14.6%). Using the range high, that's $390K of about $1.80M (roughly 22%).
  - Brad Gilbert: 70 of his 84 meals, $10.2K-$14.4K, from 11 firms, 2011-2026. The firms include Halcyon, Pershing Square, Magnetar, BlueMountain, Carlson and Credit Suisse.
  - Lulu Llano: 42 of 46 meals, most often in Palm Beach, from 8 firms.
  - Then a run of people fed by JPMorgan, Morgan Stanley, Barclays and BofA in New York, San Francisco and Boston: Peot, Cassens, Watkins, Lambropoulos.
- **Coverage, years lined up (2005-2026):** the itemized table holds $1.06M-$1.85M against $52.17M of food on the cover sheets. **That's 3.5%.**

**Hit means:** Wall Street firms that registered as Texas lobbyists feed a small set of people over years, often outside Texas. If those people choose the funds for state pension or endowment money, that's a pay-to-play thread.

**Miss means:** Without the diners' employers, this is a list of names. Their jobs aren't in the table and weren't checked.

**Boring explanation:** Firms that pitch state investment offices have to register and report, and the dollars are small ($14K over 15 years for the top name). Itemized meals are only 3.5% of reported food money, so any "who ate most" ranking ranks what was itemized. **Not ruled out.**

---

## 4. IRS 527 directors and officers: **probed**

**Checked**
- 189,593 officer rows on 77,443 Form 8871 filings for 58,882 groups (EINs). One load.
- **Most groups per person** (letters-only name). Fenner's two spellings together come to 420 groups:

| Person | Groups | Address |
|---|---|---|
| Noreen A. Fenner | 301 | 1103 Hays St, Tallahassee |
| Noreen Fenner | 125 | 1103 Hays St, Tallahassee |
| Shawnda Deane | 270 | Sacramento |
| J. Richard Eichman | 252 | Sacramento |
| Laura Ann Stephen | 240 | Sacramento |
| Nancy H. Watkins | 218 | Tampa; 220 with both spellings |

- Nearly every top title is Treasurer or Assistant Treasurer.
- **Most groups per address:**

| Address | Groups |
|---|---|
| 1103 Hays St, Tallahassee | 297 |
| 527 East Park Ave, Tallahassee | 275 |
| 455 Capitol Mall Ste 600, Sacramento | 256 |
| 610 S. Boulevard, Tampa | 214 |
| 1787 Tribute Rd Ste K, Sacramento | 203 |

- **Join to Schedule B spending.** I deduped Schedule B on EIN + date + recipient + amount first (see the trap below). The land rate against all 527s is 5.3% (3,118 of 58,882):

| Address | Groups with spending on file | Land rate | Spending |
|---|---|---|---|
| 1103 Hays St | 9 of 297 | 3.0% | $2.1M |
| 527 East Park Ave | 1 of 275 | 0.4% | |
| 455 Capitol Mall | 11 of 256 | 4.3% | $10.3M |
| 610 S. Boulevard | 20 of 214 | 9.3% | $85.7M |
| 2350 Kerner Blvd | 0 of 97 | 0% | |

- **Why it misses:** the 8871 flag `EXEMPT_8872_IND` (values 1, 0, blank). "Exempt" means the group reports its money to a state, not the IRS.

| Group set | Declared exempt |
|---|---|
| Fenner's 420 groups | 419 (99.8%) |
| 527 East Park Ave | 275 of 275 |
| Watkins | 92.7% |
| All 527s | 62.0% |

**Hit means:** The "shell network" angle needs the money. The IRS doesn't have it for these groups by design, so the story would have to run through Florida Division of Elections filings. Those aren't in the warehouse; I found no Florida campaign table in the catalog.

**Miss means:** Ranking who sits on the most 527s just ranks compliance treasurers.

**Boring explanation:** Treasurer-for-hire firms in Tallahassee and Sacramento sign as officer for hundreds of state PACs. **Ruled in** by the titles and the 99.8% exempt flag.

---

## 5. Texas lobby entertainment: **dead**

**Checked**
- 2,836 outings, 2005-2026, from 325 lobbyists. A recipient is named on 99.5%. 368 rows are exact ($84,995); the rest are ranges. Totals: $456K at the range lows, $605K at the highs.
- **Top by range high:**
  - A blank last name tops it: 40 items, $19.8K-$21.6K, prefix MRS.
  - John Whitmire: 35 items, $6.6K-$8.4K, 2005-2021.
  - Larry Taylor: 42 items, $5.9K-$7.9K.
  - Carol Alvarado: $4.9K-$6.0K.
  - Ken Paxton: 22 items, $3.8K-$4.8K, 2005-2024.
- Venues: stadiums, UT golf, a few resorts, the same AGC conference circuit as the trips.
- **Coverage, years lined up (2005-2026):** itemized high $605K against $8.83M on the cover sheets. **That's 6.9%.**

**Hit means:** Nothing at a story size. The top official averages about $500 a year.

**Miss means:** The real entertainment money ($8.8M) isn't itemized per official, so the "who got the most" question can't be answered from here.

**Boring explanation:** Texas requires itemizing only above a per-person threshold; most outings are $150-$200 tickets. **Ruled in.**

---

## Traps (new)

- **TX_LOBBY_FOOD_BEVERAGE:** the max row ($78,701) is the Austin ZIP 78701 typed into the amount. Report 604419, 2014-01-26; ten other guests that day show $35. Drop it before any sum.
- **TX_LOBBY_TRANSPORTATION has no money column.** Dollars exist only per report on the cover (`TOTAL_EXPEND_TRANSPORTATION`), so a per-official trip cost can't be computed. `LODGINGSTREETCOUNTRYCD` says USA for Jerusalem, Tel Aviv and Banff.
- **The Texas itemized tables are slivers.** 2005-2026, food detail is 3.5% of cover food dollars and entertainment detail is 6.9%. "Who got the most" ranks what got itemized.
- **Texas client lines are per report, not per line.** They land on 31-45% of detail reports and don't exist before 2000.
- **IRS 527 Schedule B repeats payments across filings.**
  - 220,991 payments (same EIN, date, recipient and amount) appear on 2 or more filings, which fits amended 8872s re-listing their lines. That's **$2.02B of the $13.32B raw total (15%).**
  - Deduped, the total is $10.87B.
  - Separately, 739,734 keys repeat inside one filing ($0.37B). Those may be real repeat payments; not resolved.
- **IRS 527 officer groups mostly never file money reports.** 62% of all 527s, and 99.8% of the Florida treasurer-service groups, set `EXEMPT_8872_IND`. A Schedule B miss is by design, not a loading gap.
- **facts.tsv mislabels TX_LOBBY_COVER.** It says REPORT_INFO_IDENT "10250 1.0K," but the column is unique.

## Open, not chased (budget)

- The #1 Texas transport report ever: Christian Bionat, March 2024, $156,254 transport and $26,814 food. It has no itemized lines and no client line. A typo or an unitemized trip.
- Brad Gilbert's, Lulu Llano's and Stacey Peot's employers. That decides whether the hedge-fund meals are a pension story.

Housekeeping: the scratchpad is shared across agents. By mistake I overwrote the root-level `scratchpad/q.py` and `scratchpad/b1.sql` from an earlier agent before moving my work into `scratchpad/deep15/`. Nothing in the repo was touched except these two deep-15 files.
