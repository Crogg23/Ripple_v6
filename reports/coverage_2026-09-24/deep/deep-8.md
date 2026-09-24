# Deep-8: five tables, second look

2026-09-24 · Python door · read-only · **30 of 35 statements** (two were failed compiles, rerun) · SQL: `deep-8.sql`

**Bottom line: nothing here is live.** All five come back **probed**. Each has a real number, but each is small, already known, or rests on a weak denominator.
The more useful output is **11 new data traps**, listed at the bottom. Three of them break the triage angles as written.

Every person and company named below is a data match, not verified against primary records.

---

## The menu

| Table | Verdict | The one number | Why it isn't bigger |
|---|---|---|---|
| COURTLISTENER_DISCLOSURE_REIMBURSEMENTS | probed | Outside groups of bankruptcy lawyers and advisers paid for **41.0%** of bankruptcy judges' trips, against **0.7%** for other federal judges (2011-19) | Permitted and routine. No sponsor is tied to a case. There are no dollar amounts. |
| FJC_IDB_BANKRUPTCY | probed (the dollar angle is dead) | Delaware holds **46 of 80** Chapter 11 case families with $1B+ assets filed since 2015, but only **3.2%** of all families | "Debt discharged" isn't discharge. Houston's assets are blank. Venue shopping is a known story. |
| OPENSANCTIONS_DEFAULT | probed (small) | **0** FAA hits. **$7.5M** in federal contracts to 6 firms that were sanctioned later. Only **$20,647** moved on or after a listing date. | Almost all the money went out before the listing, and every sponsor-type hit is a name collision |
| FORM5500_SCHEDULE_SB | probed | **631** plans report **$426.7M** in unpaid minimum contributions | The big-name plans are 79-94% funded. The unpaid money sits mostly in plans with about 8 people. The data covers one year only. |
| MSHA_ACCIDENTS | probed | ACNR mines: **11.10** recordable injuries per 100 current workers a year, against **2.24-8.81** at other coal owners (Foresight is higher at 12.33) | The denominator is today's headcount, not hours. ACNR's serious-injury rate is middling. It overlaps finding F-010. |

---

## 1. CourtListener judge reimbursements: probed

**Headline:** outside groups of bankruptcy lawyers and advisers paid for 41.0% of bankruptcy judges' reported trips in 2011-19 (2,525 of 6,166 trips). For district judges it was 0.7%, and for appeals judges also 0.7%. Delaware bankruptcy judge Kevin Carey reported 200 trips, 7x his peers' yearly rate.

**Checked**
- Stmt 1-2. There are 33,472 rows. 30,029 of them (89.7%) join through FINANCIAL_DISCLOSURES to a judge.
  - **Disclosure years run 2003-2020, not 2021-23.** Triage read DATE_CREATED, which is the day CourtListener entered the row into its database.
- Stmt 2. Rows paid by bankruptcy groups run 2-8 a year through 2010, then jump to 315-428 a year from 2011. So bankruptcy judges enter the collection in 2011, and every comparison uses 2011-19.
- Stmt 3. Top judges by trip count, 2011-19:
  - Douglas Ginsburg: 223 trips, 30 of them paid by the GMU Scalia law school
  - Harry Edwards: 212 trips, 144 of them paid by NYU under three spellings
  - Kevin Carey (Del. bankr.): 200 trips
- Stmt 4. Who paid, by type of judge:

  | Judges | Judges counted | Trips | Bankruptcy-group share | Law firm or company share |
  |---|---|---|---|---|
  | Bankruptcy | 395 | 6,166 | 41.0% | 0.3% |
  | District, magistrate, other | 854 | 8,798 | 0.7% | 2.8% |
  | Appeals and Supreme Court | 345 | 6,574 | 0.7% | 1.1% |

  - Bankruptcy groups here means ABI, the Turnaround Management Association (TMA), INSOL, restructuring groups and bankruptcy bar groups. The bankruptcy judges' own association (NCBJ) is counted separately: 499 trips.
- Stmt 5. Law firms and companies that paid judges directly:
  - Robert Vogel Law Office paid Judge Alice Senechal (D.N.D.) for 75 trips in 2011-15, labeled "Litigation activity."
  - "Jack and Sheryl Morris through JSM at Falcon LLC" paid for 12 personal-vacation trips by Judge Freda Wolfson (D.N.J.), 2009-2020.
- Stmt 6. The Gilstrap-style docket test on the Wolfson sponsor. 15 D.N.J. dockets name JSM or Edgewood Properties entities (3 "Ledgewood" hits dropped). **Wolfson is the assigned judge on none of them.**
- Stmt 29. Judges at the mega-case courts (Delaware, S.D.N.Y., S.D. Tex., N.J.) are not more industry-funded as a group:
  - Isgur (Houston): 18.4%. Jones (Houston): 21.2%. Other bankruptcy judges: 40.5%.
  - Carey is the outlier on volume: 22.2 trips per year against 3.16 for his peers. 90 of his trips were industry-paid, and 25 were paid by TMA, out of at least 118 TMA trips to bankruptcy judges.

**Hit means:** the people who bill in bankruptcy cases (lawyers, turnaround advisers, restructuring firms) help pay for the travel of the judges who approve their fees. One Delaware judge took 200 such trips in nine years.

**Miss means:**
- No bar group appears as a party, so the "sponsor later appeared before them" test can't run on 97% of trips.
- The one personal sponsor tested (Wolfson's) came back clean.
- A docket shows only the last assigned judge. A recusal looks the same as never being assigned.

**Boring, not ruled out:** teaching and speaking at ABI or TMA is allowed and common. The disclosures carry no dollar amounts. Senechal's 75 trips are likely wind-down work from her former firm. Not checked.

**Next pass, if picked:** Carey's full list of sponsors, set against the professionals who billed fees in his biggest cases. That needs a fee-application source the warehouse doesn't have.

---

## 2. FJC bankruptcy cases: probed (the dollar angle is dead)

**Headline:** Delaware got 46 of the 80 Chapter 11 case families with $1B+ in assets filed since 2015 (57.5%), while holding 3.2% of all business Chapter 11 families. But "debt discharged" doesn't mean discharged, and Houston's mega-cases carry blank asset figures. So "venue shopping measured in dollars" can't be built from this table.

**Checked**
- Stmt 7. The table has 7.0M rows. 126,751 of them are Chapter 11 rows across the six snapshots.
  - The sample showed a business case converted to Chapter 7 with DEBT_DISCHARGED equal to TOTAL_DEBT to the cent. Companies don't get a discharge in Chapter 7.
- Stmt 8 and 10. Deduped to one row per case (latest snapshot), business Chapter 11 filings from 2015 on:
  - **4,257 cases still pending, with no disposition, carry $196.8B "discharged."** 4,002 of them equal TOTAL_DEBT exactly.
  - Closed cases: 7,114 of the 7,498 with a positive value (95%) equal TOTAL_DEBT.
  - The column is filled on only about a quarter of business Chapter 11 cases.
- Stmt 9. Case families: affiliate cases grouped under their joint-administration lead, taking the largest asset figure in each family, not the sum.

  | District | Families with $1B+ assets | Share of $1B+ families | Share of all families |
  |---|---|---|---|
  | Delaware | 46 | 57.5% | 3.2% |
  | S.D.N.Y. | 12 | 15.0% | 4.7% |
  | S.D. Tex. (Houston) | 2 | 2.5% | 5.1% |

- Stmt 10. Families with 20+ affiliate cases, a size measure that doesn't depend on asset dollars:
  - S.D. Tex. 58, Delaware 56, S.D.N.Y. 26, N.D. Tex. 13, N.J. 12, everywhere else 34.
  - **52 of Houston's 58 carry under $1M in assets on file.**
- Stmt 10. By filing era, families with 20+ affiliates in Delaware / S.D.N.Y. / Houston:
  - filed 2015-18: 3 / 3 / 2
  - filed 2019-22: 27 / 17 / 23

**Hit means:** the mega-case concentration is real and measurable by family count. Delaware, Houston and S.D.N.Y. together hold 140 of the 199 families with 20+ affiliate cases.

**Miss means:**
- Dollar totals can't rank venues, because Houston's asset figures are missing.
- "Debt wiped out" can't be measured at all.
- The table has no debtor names, so the "which big debtors" question needs a join to dockets.

**Boring, not ruled out:** venue shopping by Delaware, Houston and New Jersey is a well-covered story.
- The six-snapshot double count was handled by keeping the latest snapshot per case.
- The 2.0T and 3.0T maxima weren't chased, because the dollar columns failed first.

---

## 3. OpenSanctions: probed (small)

**Headline:** once the list is cut to real sanctions programs (OFAC, EU, UK, UN, Canada, Australia, Swiss, Japan):
- **0** FAA aircraft owners match.
- **13** federal contract recipients match by name. On 6 of them the country agrees too.
- Those 6 got **$7.5M**, almost all before they were listed. The exception: NAI Logistics B.V. got 13 Defense Department contract actions, net **$20,647**, dated on or up to 3 days after its 2023-12-11 Global Magnitsky listing.

**Checked**
- Stmt 11. 63,068 company-type rows carry a non-empty SANCTIONS string.
- Stmt 13. The first match against FAA registrants and USAspending (R2) returned junk:
  - China's countermeasure list aimed at US drone makers (Shield AI, Insitu, AeroVironment)
  - OFAC settlements (PACCAR, Humana) and OCC bank orders
  - state Medicaid exclusions, with people's names typed as LegalEntity
- Stmt 15. Rerun on real sanctions programs only: companies with 2+ word names, and people only with 3+ word names. Suffixes stripped, word order ignored.
  - FAA: 0 hits.
  - R2: 13 hits. The country agrees on 6: NAI Logistics (NL), Gateway Ventures FZC (UAE), Fidelis Logistic and Supply Services (AF), Eiger Shipping (CH), Idronaut (IT), Phnom Penh Hotel (KH).
  - The rest are collisions, like the sanctioned Russian "LLC Phoenix" against a US "PHOENIX LLC."
- Stmt 16. Listing date (FIRST_SEEN) against contract action dates:

  | Firm | Paid | Listed | After listing |
  |---|---|---|---|
  | NAI Logistics | $3.28M over 436 DoD actions | 2023-12-11 (Global Magnitsky) | 13 actions, net $20,647 |
  | Fidelis Logistic | $1.39M (Sept 2022) | same day, same program | nothing |
  | Eiger Shipping | $1.30M | 2025-05-20 (Ukraine) | one −$8,438 pull-back of money; Ukraine's list doesn't bind US agencies |
  | Idronaut | $31.6K | 2024-08-23 | nothing |
  | Phnom Penh Hotel | $12.2K | 2024-09-12 | nothing |

  - Geotech Engineering, Chinese-listed, had contracts in Zambia in 2013-14, well before its 2025 listing.
  - Gateway Ventures missed this date check because a Cyrillic prefix broke the name match. Its contracts end in 2019, and its listing is in 2025.
- Stmt 28. PPP borrowers: 7 name hits. 6 are plain collisions: a Russian, Indian or Australian listing against a US small business. Sun Properties LLC (OFAC Venezuela program) against a Kentucky borrower at $157,400 is a generic name. Unresolved.

**Hit means:** the Defense Department kept paying NAI Logistics for 3 days after its sanctions listing, and paid it and Fidelis $4.67M before they were listed.

**Miss means:**
- No sanctioned company or 3+ word sanctioned person owns a US-registered aircraft under its own name.
- Nominee trusts would hide that, and this test can't see through them.

**Boring, not ruled out:** actions in the 3 days after a listing are likely close-out paperwork. The press releases for both Global Magnitsky listings may cite the US contracts themselves. Not checked.
- Politically exposed people were left out on purpose.
- The SEC side wasn't run, because ECONOMICS__FED_SEC_EDGAR holds only 200 rows (see traps).

---

## 4. Form 5500 Schedule SB (single-employer pensions): probed

**Headline:** 2024 single-employer pensions hold 108.9% of what they owe in aggregate.
- Of the 1,583 plans owing $100M+, 77 are under 80% funded and 4 under 60%. The underfunded plans are short $67.1B combined.
- 631 plans report $426.7M in unpaid minimum contributions. The plans truly behind across several years (the 248 in arrears) have a median of 8 participants.

**Checked**
- Stmt 17-18. There are 41,802 rows, but 40,443 deduped plans are **plan year 2024**. The rest are a few hundred stragglers. It is not 17 years.
  - 895 plans were filed twice (original plus amendment). The State Farm-EIN plan appears twice at $35.2B.
  - Deduped by EIN + plan number + year, keeping the latest ACK_ID.
  - Triage's formula used SB_RTD_FNDNG_TGT_AMT, which is the retirees' slice only. Used SB_TOT_FNDNG_TGT_AMT instead.
- Stmt 19. Top shortfall: EIN 521893632, $4.70B short, 78.8% funded, 84,564 people. It paid $990M against a $568.7M minimum.
  - The rest of the top 25 are 79-94% funded. The median plan owing $1B+ is 104.6% funded.
  - The sponsor-name join failed: 0 of 25 matched the main Form 5500 on ACK_ID, and only 4 matched on EIN (EIDP, FCA US, Dow, Unisys).
- Stmt 20. Plans with unpaid minimum contributions, named via IRS BMF, the main Form 5500 and the PBGC plan list:
  - National Telecommunications Cooperative Association, plan 333 (16,274 people, 74.6% funded): unpaid $131.2M, exactly equal to its $131.2M minimum, while it reported $167.1M contributed. That points to timing, not arrears.
  - EIN 822871833 (no name found; 2,475 people): **25.8% funded, $95.4M unpaid** against a $4.8M minimum this year.
  - Transit Management of Southeast Louisiana (1,617 people, 87.2% funded): $79.5M unpaid against a $3.6M minimum.
- Stmt 27. How the unpaid money splits (this cut filtered before deduping, so it counts 643 plans and runs about $1.4M high):
  - arrears (unpaid is above this year's minimum): 248 plans, $237.5M, median 8 people, 58 of them under 60% funded
  - timing (unpaid equals this year's minimum): 201 plans, $160.9M
  - part paid: 194 plans, $29.7M

**Hit means:** two mid-size plans, EIN 822871833 and the New Orleans transit plan, carry $175M in unpaid contributions spanning several years. Both are worth a name lookup and a PBGC check.

**Miss means:**
- There's one year of data, so "kept paying minimums while the gap grew" can't be tested.
- The big-name shortfalls are ordinary: plans 79-94% funded whose sponsors paid in.
- The stock-buyback and CEO-pay angle wasn't reachable.

**Boring, largely confirmed:** big shortfalls sit at big old-industry plans that are already watched. Plans whose unpaid amount exactly equals this year's minimum likely filed before the contribution deadline.

---

## 5. MSHA mine accidents: probed

**Headline:** ACNR Holdings' underground coal mines logged 11.10 recordable injuries per 100 current workers a year in 2018-24. Other big coal owners ran 2.24-8.81, and Foresight ran 12.33.
- Marshall County Mine (WV) climbed from 80 lost-time injuries in 2018 to 131 in 2024 and 150 in 2025.
- But ACNR's fracture and amputation rate is middle of the pack. Its lead is sprains and strains booked as days away from work.

**Checked**
- Stmt 21-22. There are 273,623 rows, 2000 to July 2026.
  - Injury code 01 lines up exactly with IS_FATALITY: 335 deaths in 2015-25, at 297 mines.
  - One injury carries 3,616 lost days, so every injury was capped at 365 days. At the top mines the cap barely moves anything (Marshall County: 54,741 days capped, 57,241 raw).
- **Denominator:** there's no MSHA hours or employment file in the warehouse. Every rate uses MSHA_MINES.NO_EMPLOYEES, which is **today's headcount**, over 7 years.
- Stmt 23. Mines with 100+ workers, 2018-24:
  - Marshall County Mine: 12.0 lost-time injuries per 100 workers a year. The median of its 61 underground-coal peers is 2.7.
  - ACNR holds 4 of the top 10 by days lost per worker.
- Stmt 24. Owners with 1,000+ workers:
  - ACNR: 10.83 lost-time injuries per 100 workers a year. The median owner: 0.69.
  - Deaths per 1,000 current workers, 2015-25: Alpha Metallurgical 3.45 (11 deaths), Alliance 3.36 (10), ACNR 2.62 (6). The median is 1.40.
- Stmt 25. The pattern holds across owners:
  - Murray-era years (2015-20): 149-274 lost-time injuries a year
  - ACNR-era years (2021-25): 231-266 a year
- Stmt 26. Underground coal owners with 500+ workers, per 100 workers a year:

  | Owner | Fractures and amputations | Sprains and strains | Fracture share of lost-time injuries |
  |---|---|---|---|
  | ACNR | 1.33 | 4.65 | 13.7% |
  | Foresight | 2.75 | | |
  | Alliance | 1.70 | | |
  | Peabody | 1.35 | | |
  | the other nine owners | 0.79-1.58 | 0.44-4.61 | 30-80% at most |

- Stmt 30. Counting all recordable injuries (days away, light duty only, no lost time):
  - ACNR 11.10, Foresight 12.33, Iron Senergy 8.81, Alliance 7.12, Alpha 4.06, Core 3.73.
  - ACNR books 87.8% of its injuries as days away. The other owners book 38.6-80.8%.

**Hit means:** ACNR and Foresight miners get hurt, or at least get recorded as hurt, at 1.5-3x the rate of other big coal owners. The rate is steady under two owners, and it's rising at Marshall County.

**Miss means:**
- On serious injuries ACNR is ordinary. Part of its lead on days-away injuries is how it classifies them.
- Deaths are too few (6-11 per owner) to rank.

**Boring, not ruled out:**
- Today's headcount understates 2018-20 staffing at the post-bankruptcy owners (Murray to ACNR, Foresight), which inflates their rates.
- More complete reporting looks like more harm.
- ACNR and Foresight already sit in finding F-010 (B10) for violations.
- The fix is MSHA's quarterly employment and hours file, which isn't loaded.

---

## New data traps (11)

1. **CourtListener reimbursements:** DATE_CREATED (2021-23) is the day CourtListener entered the row. The real disclosure year is FINANCIAL_DISCLOSURES.YEAR_COL, 2003-2020. Bankruptcy judges only enter in 2011.
2. **FJC bankruptcy DEBT_DISCHARGED is not debt discharged.** It equals TOTAL_DEBT to the cent on 95% of filled closed cases, and shows $196.8B on 4,257 still-pending cases with no disposition. Treat it as scheduled debt.
3. **FJC bankruptcy TOTAL_ASSETS is under $1M on 52 of 58 Houston (S.D. Tex.) case families with 20+ affiliates.** Any dollar ranking of venues drops Houston.
4. **FJC snapshots start in FY2021**, so pre-2020 filings that closed early are likely missing. Families with 20+ affiliates filed 2015-18 number 2-3 per big district, against 17-27 for 2019-22. This is inferred, not proven.
5. **OpenSanctions: a non-empty SANCTIONS string does not mean sanctioned.** It also covers China's list aimed at US defense firms, OFAC and OCC settlements, and Medicaid and SAM exclusions, and LegalEntity rows hold people's names. Filter on DATASETS by sanctions program.
6. **Schedule SB is one plan year (2024), not 17.** 895 plans were filed twice as amendments: dedupe by EIN + plan number + year. SB_RTD_FNDNG_TGT_AMT is retirees only. Use SB_TOT_FNDNG_TGT_AMT.
7. **Schedule SB doesn't join the main Form 5500 on ACK_ID:** 0 of the top 25 matched. They are different sets of filings.
8. **ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS is not a list of failed plans.** It holds live insured mega-plans (EIN 910425694 at 298K participants). An EIN match there means nothing.
9. **ECONOMICS__FED_SEC_EDGAR is 200 rows, 20 companies (CIKs).** It is useless as an EIN or company directory.
10. **Schedule SB "unpaid minimum" equals this year's minimum on 201 plans:** the filing came before the contribution deadline, not arrears. Test unpaid above the minimum for real arrears.
11. **MSHA has no hours file, and owners classify injuries differently.** ACNR books 87.8% of its recordable injuries as days away; the other owners book 38.6-80.8%. Compare total recordable injuries, not days away alone.

**Housekeeping:** the session scratchpad is shared across parallel agents. Another agent's runner overwrote a shared `q.py` mid-run, so this agent moved to `scratchpad/deep8/`. Nothing in the repo was touched besides the two files named above.
