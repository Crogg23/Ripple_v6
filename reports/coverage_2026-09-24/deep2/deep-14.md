# deep-14: hand queries, group 14

2026-09-24. Five tables: one pension, four politics. Python door only.
34 statements: 28 SELECTs plus 6 session statements, one under the 35 budget. The SQL is in `deep-14.sql`, numbered [1] to [28].

Every person, company, PAC or county named below is **a data match, not verified against primary records.**

## The call

| Table | Verdict | One line |
|---|---|---|
| POLITICS__FEC_COMMITTEE | **probed** | 92 PACs took in $580M from individuals in 2024 and passed under 10% of their spending on to candidates, committees, outside ads or affiliates. The busiest treasurers' big PACs do this about twice as often as everyone else's: 30% vs 14.6%. Can't say where the money went: the FEC operating-expense table isn't in the warehouse. |
| POLITICS__IRS527_8872_REPORTS | **probed** | Amended reports stack on top of the originals. That's $2.13B of double-counted receipts (15.7%). The biggest gaps are famous groups. The one odd case is DeSantis's $82.5M transfer, already widely reported. |
| POLITICS__FED_EAC_EAVS | **probed** | This is the full 2022 survey, not a partial load. The top "rejecting" counties are mostly an artifact: Orange and LA counties counted 114K undeliverable ballots as rejected. The real outliers left are Texas and Philadelphia, and the press has both. |
| LABOR__FED_PBGC_TRUSTEED_PLANS | **probed** | The contracts join timed out, so the main angle is unresolved. Repeat dumpers are 33 EINs, mostly well-known double bankruptcies like LTV Steel. |
| POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS | **dead** | The $8.5M line is a lump of small gifts. Donors over the legal cap are 99% duplicated lines. Quarterly returns repeat the annual returns, and that's about $1B of the $3.0B total. |

**None of the five is live.** Two of them (FEC, 527) have a real number but are blocked or already reported. The three others turned up data traps, not stories.

---

## 1. POLITICS__FEC_COMMITTEE: probed

**Headline:** In 2024, 92 non-joint-fundraising PACs raised $1M+ each from individuals, $580M in all. Each sent **under 10%** of its spending to candidates, other committees, independent expenditures (outside ads) or affiliated committees.

Among PACs with $250K+ from individuals:
- The 12 busiest treasurers: **29 of 96 PACs (30%)** are that low.
- Everyone else: **188 of 1,289 (14.6%)**.

**Size:** 20,938 committees in 2024 and 20,007 in 2026, one row per committee per cycle. 14,131 treasurer names in 2024; 957 rows have no treasurer.

**Checked**
- [3] Counted committees and treasurers by cycle, and pulled a sample [4].
- [13] Joined 2024 PAC-type committees (types N, Q, O, V, W) to the FEC PAC summary on CMTE_ID. 2024 cycle only; I took the latest summary line with an end date from 2023-01 to 2025-01. **Land rate: 9,207 of 10,271 (89.6%).**
- [13] then [14] used "political share" = (contributions to other committees + independent expenditures) / total spending.
  - **That metric was wrong:** every joint fundraising committee read 0%, for example Harris Victory Fund at $1.29B. They move money as transfers to affiliates.
- [24] and [25] fixed it: added transfers to affiliates and dropped joint fundraising committees.
- [25] Second-field check: summed the Schedule E table (FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES, cycle 2024) for each flagged PAC.
  - **0 of 30** show Schedule E spending above 10% of what they spent.
  - So the outside-ad column is not hiding their spending.

| Treasurer (2024, non-JFC) | PACs | $250K+ from people | Under 10% to politics | Rate |
|---|---|---|---|---|
| Datwyler, Thomas | 189 | 9 | 4 ($6.7M) | 44% |
| Kilgore, Paul | 99 | 16 | 4 | 25% |
| Hobbs, Cabell | 66 | 15 | 7 | 47% |
| Stanger, Howie | 55 | 4 | 2 ($23.2M) | 50% |
| All other treasurers | 8,242 | 1,289 | 188 ($566M) | 14.6% |

Biggest low-share PACs [25], all data matches:

| PAC | From individuals | Share passed on | Likely reason |
|---|---|---|---|
| Never Surrender | $68.6M | 0% | leadership PAC, legal bills |
| Turnout for America | $42.4M | 6.7% | |
| RON PAC | $33.1M | 1.5% | |
| Democratic Action | $26.6M | 0.2% | |
| Heartland Patriots | $22.7M | 0% | |
| Citizens for Free Enterprise | $14.9M | 0.1% | |
| MoveOn | $44.7M | 6.1% | voter contact |
| EMILY's List | $33.8M | 2.3% | conduit, earmarks go direct |

- **Hit means:** a PAC takes in millions and passes almost nothing on. That's the scam-PAC shape, and it clusters a bit at serial treasurers.
- **Miss means:** if the busiest treasurers matched the 14.6% baseline, the treasurer angle would be dead. They don't match it, but the count is only 96 PACs.
- **Boring explanation, not ruled out:** canvassing, digital ads that aren't reported as outside ads, conduits, training groups (NDTC) and legal bills all look "low share" without being scams. Scam PACs have been in the press since 2019.
- **What would move it:** land the FEC operating expenditures (Schedule B vendor payments). Then split each low-share PAC's spending into fundraising vendors vs. voter contact.

---

## 2. POLITICS__IRS527_8872_REPORTS: probed

**Headline:** 527 groups file amended 8872s, and both the originals and the amendments sit in the table.
- If you keep only the latest report per EIN and period, receipts drop from **$13.58B to $11.45B**, minus $2.13B (15.7%).
- Spending drops from **$13.31B to $11.16B**, minus $2.15B (16.1%).
- The Republican Governors Association alone goes from $2.21B to $1.31B.

**Size:** 55,579 reports, 4,150 EINs, 4,644 flagged as amended. Periods run 2000 to 2026-07.

**Checked**
- [9] Counted reports and distinct EIN+period pairs. There are 52,034 pairs for 55,579 reports.
- [20] Kept the latest filing per EIN + period start + period end, then compared totals cycle by cycle.
  - After that, 2,256 reports still overlap another period. They hold $84M of receipts, so that leftover is small.
- [21] Per EIN per cycle, deduped: receipts minus spending.
  - 281 EIN-cycles swing $1M+ (141 up, 140 down).
  - 157 EINs are $5M+ ahead over their whole life.
- [28] Checked 6 EINs against the Schedule A and B line tables.
  - **The line sums equal the raw, un-deduped 8872 totals to the dollar, for all 6.**
  - So the line tables stack amendments too.

**The top gaps are all household names:** RGA, DGA, ActBlue, AFSCME. The two odd ones:
- **Empower Parents PAC**
  - $325,860 in, $83.1M out.
  - One Schedule B line is $82.5M to Never Back Down, Inc. on 2023-05-31, marked "contribution."
  - It matches the widely reported 2023 move of DeSantis's Florida committee money into his super PAC. Not verified here.
- **American Technology Excellence Project**
  - One Schedule A line of $45M in the 2026 cycle, $6.8M spent.
  - The press has already reported it as a new tech-industry political group. Not verified here.

- **Hit means:** a 527 that takes money in and doesn't itemize spending of it. That would be a sitting-on-cash or pass-through story.
- **Miss means:** once deduped, the gaps are carryover at big famous groups. That's what happened.
- **Boring explanation, ruled in:** amendments double count, and famous groups dominate. Schedule A and B also hold only itemized lines, so the gap between them isn't cash on hand.

---

## 3. POLITICS__FED_EAC_EAVS: probed

**Headline:** This is the full 2022 EAVS: 6,460 jurisdictions and 112.05M voters.
- The Wisconsin skew isn't a partial load. Wisconsin reports by town (1,851 rows).
- Nationally, 549,776 of 36.06M returned mail ballots were rejected: **1.52%**.
- **But 115,617 of those "rejections" (21%) are undeliverable mail, booked as rejected by three counties.**

**Checked**
- [5] Totals, sentinel values and year hints.
  - F1A (people who voted) = 112.05M, which fits the 2022 midterm.
  - 411 comments mention 2022; none mention 2024.
  - Returned = counted + rejected (C1B = C8A + C9A) on 6,014 rows.
- [15] Rejected / returned for each jurisdiction with 1,000+ returned. Each is compared to **its own state's rate**, ranked by excess rejections.
  - 1,747 jurisdictions qualify.
  - 24 reject at 3x their state rate or more, with 50+ rejections.
- [26] Read the "other" labels and comments for the top outliers.
- [16] Same test for provisional ballots.
  - 694,771 cast, 148,929 rejected (21.4%).
  - Only 3 of 243 jurisdictions (500+ cast) are at 3x their state rate. Small.

| County | Rejected / returned | Own state | What the "other" column says |
|---|---|---|---|
| Orange CA | 64,278 / 892,738 (7.2%) | 2.44% | 48,628 in "UNDELIVERABLE/VOID/FINAL NOT COUNTED". Void (9) and final (436) are listed separately, so the rest is undeliverable. |
| Los Angeles CA | 92,427 / 2.05M (4.5%) | 2.44% | 65,822 labeled "UNDELIVERABLE" |
| Hernando FL | 1,422 / 31,774 (4.5%) | 0.80% | 1,167 "UNDELIVERABLE/TEMP AWAY" |
| Kings CA | 3,903 / 28,455 (13.7%) | 2.44% | 3,628 in C9P. No label, no comment. **Open.** |
| Bexar TX | 3,037 / 35,601 (8.5%) | 3.40% | 2,428 in C9M. Harris TX has 2,617 of 2,665 in C9M. |
| Philadelphia PA | 5,763 / 133,969 (4.3%) | 1.88% | C9C 2,264, C9H 1,820 |
| Kings NY (Brooklyn) | 2,056 / 33,210 (6.2%) | 1.85% | spread over many reasons |

- Take out the undeliverable mail and Orange County falls to about 1.9%, Los Angeles to about 1.3%.
- Those three counties hold 60% of the excess rejections over state rates (86K of 142,618).
- **Hit means:** a county rejecting voters' ballots at several times its state's rate, under the same law. That's a local-practice story.
- **Miss means:** the outliers are reporting artifacts, or state law that everyone already knows. That's mostly what happened.
- **Boring explanation, partly ruled in:**
  - The two biggest outliers are bookkeeping.
  - Texas's C9M spike is most likely the 2022 SB1 ID-number rule. The codebook isn't in the warehouse, so the letter-to-reason map isn't verified.
  - Philadelphia's is most likely the undated-envelope fight.
  - Both are well covered. Kings County CA is the one unexplained outlier.

---

## 4. LABOR__FED_PBGC_TRUSTEED_PLANS: probed

**Headline:** The key join, dumpers that went on to win federal contracts, **did not finish.**
- [12] failed: ACTION_DATE is text.
- The fixed rerun [22] hit the 300-second timeout.
- The other two angles are small or already known.

**Size:** 5,176 plans, 4,431 EINs, 2.53M people at termination. Terminations run 1972 to 2026-04; takeovers up to 2026-06. 531 EINs lost a leading zero; padded here.

**Checked**
- [11] Repeat dumpers: EINs whose plans ended 3+ years apart.
  - **33 EINs, 160,139 participants.** 7 are 10+ years apart.
  - Top of the list: LTV Steel (1986 and 2002, 85,650 people), Kaiser Aluminum, Allis-Chalmers, Penn Traffic, Oneida (2006 as Ltd, 2022 as LLC), Aloha Airlines.
  - One union local's EIN (Local 1139 UE) holds 8 plans from 1985 to 2011, 451 people.
- [23] PBGC EIN matched to the sponsor EIN in Form 5500, using plan year 2025.
  - **14 of 4,431 EINs land.** 12 pass a first-word name check.
  - 7 of those were taken over in 2008 or later: Times Publishing (2022), True Value (2025), Mohawk Fine Papers (2024), Isola USA, Niagara Falls Memorial, United Way SE Michigan, Abbott House.
  - **The Form 5500 table holds only 29,069 sponsor EINs.** It's a thin slice, so a low land rate means nothing.
- [22] Normalized PBGC sponsor name matched to USAspending contract recipient name (R2, 93M rows).
  - Scanning distinct names with a regex was too slow.
  - **Unresolved.**

- **Hit means:** a company hands its pension to PBGC, then keeps drawing federal contract money, checked by state and by date.
- **Miss means:** no contracts after the takeover. That would kill the angle.
- **Boring explanation:** a repeat EIN is one company, several plans, usually one bankruptcy wave or a second bankruptcy. Ruled in for the top 10.
- **What would move it:** a cheaper name join. Pre-filter R2 on the first word of the sponsor name, or use a small recipient table (UEI + name) instead of the 93M transaction rows. The sponsor names also need the junk values dropped (see traps).

---

## 5. POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS: dead

**Headline:** Every triage lead is an artifact.
- The **$8.5M line** is the Conservatives' 2008 annual lump, "Contributions of $200 or less." The top 5 lines are all that lump.
- **Over the cap:**
  - 93,969 of 1,303,067 donor-party-years (7.2%) look more than 10% over the yearly per-party cap.
  - **93,259 of them (99.2%) contain identical repeated lines:** same donor, party, date and amount.
  - Top rows show exactly 2x the lines, for example 28 lines but 14 unique.
  - Only 949 are over 2x the cap.
- **Two-party donors:** 5,438 of 1,399,991 donor-years (0.39%) gave $200+ to two or more parties. 628 of them gave to both the Conservatives and the Liberals. Small.

**Checked**
- [7] Rows and dollars by kind of recipient, kind of donor and kind of return.
- [8] Top 5 lines plus 5 random lines.
- [17] Quarterly party lines matched to annual lines on recipient, name, postal code, date and amount.
- [18] Yearly per-party cap test on annual returns, all parts, lump lines dropped.
  - Donor key = name + postal code.
  - Caps: $5,400 used as a ceiling for 2004-06 (the real cap was about $5,000, indexed), $1,100 for 2007-11, $1,200 for 2012-14, then $1,500 plus $25 a year.
- [27] Same test, Part 2a lines only.
- [19] Donors who gave to two or more parties in the same year.

- **Hit means:** a donor clearly over the cap to one party in one year, on distinct lines.
- **Miss means:** the overage goes away once lines are deduped. That's what happened.
- **Boring explanation, ruled in:** duplicated lines, lump lines, and quarterly returns repeating annual ones. Also not a US story.
- **Still open, small:** 79 estate donor-years are over the cap by $2.94M in total. The NDP got $1.12M from one estate in 2014. Check Canada's bequest rule before calling any of it a breach.

---

## New data traps

1. **The IRS 527 tables stack amended reports.**
   - The 8872 reports, the Schedule A lines and the Schedule B lines all keep both the original and the amendment.
   - That overstates receipts by $2.13B (15.7%) and spending by $2.15B (16.1%).
   - RGA's line tables overstate it by 69%.
   - Fix: keep the latest FORM_ID per EIN + PERIOD_BEGIN_DATE + PERIOD_END_DATE, and carry that onto the line tables through FORM_ID_NUMBER.
2. **Canada's quarterly party returns repeat the annual ones.**
   - 1.83M quarterly lines ($981M); 80% match an annual line exactly.
   - From 2005 to 2019, each year's quarterly dollars are within about 3% of that year's annual dollars.
   - So the $3.0B total in the facts line double counts about $1B.
   - Use annual returns only.
3. **Canada annual returns repeat lines, and Part 2b isn't ordinary giving.**
   - Identical lines (same donor, party, date, amount) sit behind 99% of over-cap donor-years. The catalog's "identical repeat lines are real" needs rechecking.
   - Part 2b lines spike in leadership-race years: 2006, 2012, 2013, 2017, 2020, 2022, 2025.
   - In 2020 and 2022, Part 2b holds flat $50,000 lines under names that match Conservative leadership candidates (MacKay, Lewis, Sloan, Charest). Data match, not verified.
4. **EAVS counts undeliverable mail as rejected ballots.**
   - Orange CA (48,628), Los Angeles CA (65,822) and Hernando FL (1,167) put undeliverable mail in the "other" rejection buckets.
   - That's 21% of the national total.
   - Read C9R, C9S and C9T and their `_OTHER` labels before ranking.
5. **FEC PAC summary: joint fundraising committees read 0% "spent on politics."**
   - Their money moves as TRANSFERS_TO_AFFILIATES.
   - Any share-passed-on metric has to include transfers or drop designation J.
6. **PBGC SPONSOR_NAME holds filler.**
   - "UPDATE SPONSOR NAME" sits on an Allis-Chalmers EIN, and "C/O SLEVIN & HART PC" on another.
   - Drop these before any name join.

## Statement count

28 SELECT/WITH statements (one compile error, one timeout) + 6 session statements = **34 of 35**.
