# deep-11: coverage round 2, five tables queried by hand

2026-09-24. Door: Python (`connect/db.py`). Read-only. Query tag `coverage-r2-2026-09-24`.
**32 of 35 statements used.** 3 of them failed (1 timeout, 2 typos) and are noted in `deep-11.sql`.
Every person or company named here is a **data match, not verified against primary records**.

---

## The menu

| Table | Verdict | The number that decided it |
|---|---|---|
| INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING | **probed** | The "Download all files (.zip)" link was on 11 data-set pages. All 11 lost it between Jan 30 and Feb 9, 2026, and none got it back by early June. 12 court-case links were renamed to "[redacted] v. ..." between Feb 21 and Feb 24. |
| JUSTICE__COUNTY_DOUBLE_BURDEN | **probed** | Compared with counties of the same size, the 54 flagged counties got **$45 of SAMHSA money per person** in FY19-25, against **$92** for counties with the same overdose ranking. They are no less likely to have a methadone clinic (14.8% vs 15.2%). |
| JUSTICE__FED_CONSOLIDATED_SCREENING_LIST | **probed** | One clean hit. NAI Logistics B.V. (Rahmani network, Global Magnitsky list) kept getting paid for DLA fuel: 32 actions and $148K in 2023, then 13 actions and $20.6K after its own SAM exclusion date. The exclusion record carries a **different UEI** from the one the vendor was paid under. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS | **dead** | I tested 1,572 judge-gift pairs against 3.59M dockets. That found **4 hits and 1 real one**: a single 2005 case against the Fort Worth Club. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_POSITIONS | **dead** | I tested 11,937 to 14,051 judge-position pairs against 9.9M to 12.3M dockets. That found **1 clean director-of-a-party hit**: a single 2003 case. |

---

## 1. DOJ Epstein pages in the Wayback Machine: **probed**

**Rows:** 24,897 links, from 13 archived pages: the main disclosures page plus data sets 1-12. The captures run from 2025-12-19 to 2026-06-03, and the main page was captured 77 times.

### What I checked
- For every page and every link, I found the first and last capture the link appeared in. A link counts as vanished if it is missing from that page's newest capture [7].
- I sorted the vanished links by kind, then checked two things: is the same link text still on the page, and does the link turn up on any later page [8]-[10].
- I listed every link on the main page's newest capture, 2026-05-26 [11].

### What vanished, and why

| Kind | Vanished | What happened |
|---|---|---|
| EFTA PDF links | 627 | **516 were URL rewrites.** The same file name is still on the page under a new address (`DataSet%201` became `DataSet 1`). Data set 1 lost 50 more in 3 hours on release day: one page of the listing, so paging, not deletion. |
| **"Download all files (.zip)"** | 23 links on 11 data-set pages + the main page | **Gone from all 11 data-set pages.** Last seen between Jan 30 and Feb 3, 2026, and gone by Feb 9. Data sets 10 and 11 had a zip link for only a few hours on Jan 30. It is never seen again through the last capture (May 26 - Jun 3). |
| BOP jail video, one link per hour of Aug 9-10, 2019 | 32 | **Moved, not removed.** From Feb 21 the main page links to a `/bop-video-footage` page instead. |
| Flight log, contact book, masseuse list, evidence list, OIG memo 23-085, OPR report, Bondi letter | 16 PDFs | Last seen Feb 1-2, 2026. From Feb 21 the main page links to "First Phase of Declassified Epstein Files" and "Memoranda and Correspondence" pages. **They probably moved there**, but this table never captured those pages, so that is not verified. |
| Court-case names | ~14 links | **Renamed to hide the plaintiffs.** On Feb 21 the links still read Farmer v. Indyke, Bryant v. Indyke, Davies v. Indyke, Edwards v. Maxwell, C.L. v. Epstein and Epstein v. Edwards. By Feb 24, **12 links** read "[redacted] v. Indyke", "[redacted] v. Maxwell", "Epstein v. [redacted]" and so on. |

### Walking the chain
- **Hit means:** DOJ took a public feature away (the bulk zip download) or changed what the public page says (it blacked out plaintiff names that are already in public court records).
- **Miss means:** most of the churn is URL rewrites, paging and one redesign around Feb 2-4. On that date the navigation links changed on all 13 pages at once.
- **Boring explanation, mostly stands:**
  - One redesign moved the video and probably the older documents to their own pages.
  - The zip removal and the name redactions fit a victim-privacy cleanup after the Jan 30 release.
  - The Epstein files are among the most covered stories of the year. I did not check any of this against news reports.
- **What is left:** two dated facts, zip removal Feb 3-9 and names redacted Feb 21-24. They are only worth something if nobody has reported them yet.

---

## 2. County double burden: **probed**

**Rows:** 3,029 counties. 54 are flagged as worst tenth on both overdose and jail rate.

### Traps in the table itself [12], [13]
- **The jail years don't line up.** 1,405 counties use 2024, 562 use 2023, 549 use 2019 and 78 are older than 2015. Counties from different years are ranked against each other.
- **One regional jail shows up as seven counties.** Dickenson, Wise, Russell, Norton, Buchanan, Lee and Tazewell VA all read exactly **1,068**. That is one shared jail rate copied to seven counties.
- **Some jails hold state prisoners.** 13 of the 54 are in Kentucky, where county jails hold state prisoners. Beaver County UT reads 7,939 per 100K, and Grayson KY reads 4,404.
- **The overdose number is a band, and the top band has no ceiling.** ">30" is the highest band, so 31 and 90 look the same.
- **JAIL_POPULATION can be fractional.** Bristol city VA reads 0.06 inmates.
- **The implied population is small.** Jail population divided by jail rate gives 885 to 35K people per flagged county. That fits a population count of ages 15-64.

### The join that would make it a story
**A. Opioid treatment clinics** [14]
- I matched Medicare-enrolled clinics to counties by ZIP code. All 1,340 of 1,340 clinic NPIs landed on a county.

**B. SAMHSA grant money, FY2019-2025** [30], [31]
- I summed SAMHSA dollars by the county where the grant is carried out ("place of performance").
- $50.5B in all. $39.2B carries a county code, and $37.1B lands on a county in this table (73% of all dollars).

Size-matched: only counties with a base population of 800 to 40,000 [31]. Denominator: the implied base population.

| Group | Counties | Any SAMHSA $ | SAMHSA $ per person | Has a methadone clinic |
|---|---|---|---|---|
| **Double burden** | 54 | 22.2% | **$45** | 14.8% |
| Overdose worst tenth only | 164 | 34.1% | $92 | 15.2% |
| Jail worst tenth only | 223 | 21.5% | $97 | 9.4% |
| Rest | 1,727 | 25.3% | $93 | 10.7% |

Without the size match, the gap looks bigger: $45 vs $151 for the overdose group. That extra gap is only because the flagged counties are small.

### Walking the chain
- **Hit means:** the counties jailing people while they die of overdoses get half the federal treatment money per person of same-size counties with the same overdose ranking.
- **Miss means:** there is no clinic gap. Counties this small rarely have a methadone clinic in any group.
- **Boring explanation, not ruled out:**
  - Most SAMHSA money is block grants to state agencies. Those count where the state agency sits, not where the money is spent.
  - The money arrives in lumps. The median county in every group got $0, so one big grant in one peer county moves the average.
  - Kentucky, Tennessee and Virginia make up 28 of the 54. How each state routes its money could explain the whole gap.
- **Deeper pass:** compare each flagged county with same-size counties **in its own state**, and follow the state's subgrants.

---

## 3. Consolidated Screening List: **probed**

**Rows:** 25,988 entries. SDN entities 9,871, SDN individuals 7,502, Entity List 3,419, Denied Persons 1,596, SDN vessels 1,534, ITAR debarred 787 [15].
**Trap:** SDN rows have **no START_DATE**, 0 of 19,249. So "paid after listing" can't be worked out from this table for SDN. The listing date has to come from SAM's ACTIVATION_DATE or from Treasury.

### What I checked
1. **Name match to contracts** [17]
   - Primary name plus alt names, cleaned up, 2+ words, matched exactly against all 93M contract actions in the R2 table.
   - 147 pairs matched, mostly collisions, like Myanmar's Ministry of Defence and a "MINISTRY OF DEFENSE" contract recipient.
2. **Parties with US addresses, inside their listing window** [18]
   - Three Denied Persons List firms had matching city and state and got paid while their export denial ran. **That is about $3.3M:**
     - Data Physics Corp, San Jose: $2.45M, 62 actions, denial ran 2006-2011
     - Omega Engineering, Stamford: $623K, 130 actions, denial ran 2003-2008
     - Universal Industries Limited, Boynton Beach: $219K, 8 DoD actions, denial ran 2012-2014
   - **Boring, and it stands:** a denial order bans exports, not federal contracts.
3. **Exact foreign matches, checked by country** [19]-[24]
   - Only the Rahmani network matched on country. NAI Logistics B.V. (Amsterdam) and Fidelis Logistic and Supply Services (Kabul) are both "Linked To: RAHMANI, Ajmal" on the Global Magnitsky list.
4. **Scale check** [32]
   - I name-matched 19,736 OFAC entities on the SAM exclusion list to contract recipients.
   - 57 pairs matched. **Only NAI Logistics matches on country and was paid after its SAM exclusion date.**
   - Possible second lead: Skyline Aviation B.V. (Netherlands) got $5.05M after the listed Skyline Aviation Ltd (San Marino, Crimea program) was excluded on 2022-06-02. The countries differ, so it may be two different firms.

### NAI Logistics B.V., the one lead [21], [23], [24]

| When | Actions | Net $ | What |
|---|---|---|---|
| 2015-2022 (last one 2022-12-08) | 404 | $3.13M | DLA Energy, fuel oil and diesel |
| 2023 | 32 | $148K | same |
| On or after 2023-12-11, its SAM exclusion date | 13 | $20.6K | last one 2023-12-14 |

- The SAM exclusion (OFAC, "Reciprocal") went in on **2023-12-11**. It lists UEI **P8ATG76DP1Y3**.
- The vendor was paid under UEI **SLVJF3DR8MN5**. A check by UEI would not connect the two.
- The OFAC designation date for the Rahmani network is **not in this table**. From memory it is Dec 9, 2022, one day after the last 2022 action. **Check that against the Treasury press release.**

### Walking the chain
- **Hit means:** a sanctioned firm was paid by DLA for about a year after it was listed. It was still paid 3 days after its own SAM exclusion, which sits under an ID the payment system would not match.
- **Miss means:** almost every other name match is a collision. It is a US firm sharing a name with a foreign one (Seventh Sense, Crystal Group, Costar).
- **Boring explanation:**
  - The Rahmani network was sanctioned **because of** DoD fuel contracts, so the contracts themselves are known.
  - The money after listing is small, and the last actions may be closeout adjustments. Several are negative.

---

## 4. Judges' disclosure gifts: **dead**

**Rows:** 2,025 gifts from 536 judges. **301 rows (15%) have no judge**: their disclosure ID is missing from the disclosures table.
**Trap:** the disclosure years run 2002-2022. The "2021-23" in triage is CourtListener's own record date.

### Traps [25]
- **VALUE_COL is garbled scanned text.** The parsed sum is $5.01B, and one row alone parses to **$5,000,625,000**. Don't sum it.
- **The table holds rows from other sections.** One "gift" is "Mortgage - Investment Real Property" from Wells Fargo.

| Giver type | Gifts | Judges | Median $ |
|---|---|---|---|
| Other | 1,175 | 340 | $900 |
| Bar, law school, judicial group, university | 400 | 155 | $600 |
| Club membership | 205 | 55 | $840 |
| Law-firm-like, mostly swearing-in receptions | 146 | 72 | $4,000 |
| Blank, exempt or none | 99 | 46 | $2,000 |

### What I checked [26]
- I took every giver name of 2+ words.
- I searched the same judge's docket case names from one year before the gift to two years after.
- That is 1,572 pairs, 489 judges and 3.59M dockets.

| Hit | Real? |
|---|---|
| John Houston, Wells Fargo, 7 foreclosure cases | No. The "gift" is a mortgage line filed in the wrong table, which is the deep-7 debts story. |
| Catherine McEwen (bankruptcy court), The Florida Bar | No. The Bar is a creditor, and the gift is an $825 fee waiver. |
| Gustavo Gelpi, Bankers Club | Doubtful. The name is a fragment inside a hotel-association case. |
| **Terry Means, The Fort Worth Club** | **Yes, one case.** He got an honorary membership (2005) and was assigned *Linders v. Fort Worth Club*, an employment case filed in 2005. Whether he stepped aside is unknown. |

- **Hit means:** a judge heard a case against someone who gave him a gift.
- **Miss means:**
  - The givers are bar groups and clubs, which are rarely sued.
  - Law firms show up as counsel, not in case names. The deep-7 opinions check covers counsel.
- **Boring explanation, it stands:** these are small gifts from people who don't end up in court.

---

## 5. Judges' outside positions: **dead**

**Rows:** 37,050 positions, 2,502 judges. **4,533 rows (12%) have no judge.** The disclosure years run 1990-2022 [27].

| Organization type | Rows | Judges |
|---|---|---|
| Other nonprofit or civic | 15,897 | 1,933 |
| University or school | 7,194 | 881 |
| Bar or judicial | 5,063 | 634 |
| Company-like | 4,250 | 627 |
| Family trust or estate | 3,048 | 477 |
| Hospital or health | 619 | 89 |
| Religious | 208 | 60 |

### What I checked
Under 28 USC 455(b)(5)(i), a judge who is an officer, director or trustee of a party must step aside. So I searched each judge's own dockets for the organizations he or she is a director, trustee or officer of, from one year before to one year after.

**Strict run** [28]: the full organization name had to appear in the case name. That is 14,051 pairs and 12.3M dockets.
- 2 hits, and neither is a director role:
  - Irene Keeley, a member of a WVU "President's House" group, had 6 West Virginia University cases.
  - Edward Davila, on Santa Clara University's law advisory board, had 1 case.

**Loose run** [29]: I split lists of organizations apart, stripped "Board of Trustees of", and dropped advisory and honorary roles. That is 11,937 pairs and 9.9M dockets.
- 18 hits, most of them place names (LOS ANGELES, SAN FRANCISCO).
- **One clean hit:** Gerald Rosen was on the Focus:HOPE board of directors (2004 disclosure) and was assigned *Abner v. Focus Hope*, filed in 2003.
- The rest are related bodies, not the party itself. Richard Stearns is a trustee of a Mass General foundation and heard a case against the hospital system. Michael McShane sits on a University of Oregon center's board and had 2 cases against the university.

### Walking the chain
- **Hit means:** a judge was a director of a party in his or her own case. Recusal would be mandatory.
- **Miss means:** almost none show up. Possible reasons:
  - Judges step aside before the docket records them.
  - Most roles are with charities, schools and bar groups, which are rarely sued.
  - Exact-name matching misses variants like "Board of Trustees, X University" against "Doe v. X Univ."
- **Boring explanation, it stands:** with 1 hit in about 12,000 pairs, even a matcher 10 times more sensitive would not make this a pattern.

---

## New data traps

| Table or column | Trap |
|---|---|
| CourtListener gifts VALUE_COL | Garbled scanned text. It parses to $5.0B, one row reads $5,000,625,000, and mortgage lines sit in the gifts table. |
| CourtListener gifts, positions | DATE_CREATED 2021-23 is CourtListener's date. The real disclosure years are 1990/2002 to 2022. 12-15% of rows link to no judge. |
| COUNTY_DOUBLE_BURDEN | Jail years mixed (2019-2024 plus 78 counties before 2015). Seven SW Virginia counties share one regional-jail rate of 1,068. Overdose is a band with ">30" as the top. |
| CONSOLIDATED_SCREENING_LIST | SDN rows have no START_DATE (0 of 19,249). |
| SAM_EXCLUSIONS, OFAC "Reciprocal" rows | They carry their own UEI, not the vendor's registered UEI. For NAI Logistics: P8ATG76DP1Y3 against SLVJF3DR8MN5. |
| CONTRACTS_FULL_R2 ACTION_DATE | Stored as text. YEAR() fails, so use LEFT(ACTION_DATE, 4). |
| Wayback DOJ listing | 516 of 627 "vanished" PDF links are URL-encoding rewrites. Diff on link text, not HREF. |

Statements: **32** (budget 35). SQL is in `reports/coverage_2026-09-24/deep2/deep-11.sql`.
