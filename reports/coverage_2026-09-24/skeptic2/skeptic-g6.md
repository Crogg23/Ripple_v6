# Skeptic g6, round 2, 2026-09-24

Door: Python. Read-only. **15 statements** (1 metadata, L1 2, L2 3, L3 3, L4 6; one failed with a Snowflake internal error and was re-run). SQL: `skeptic-g6.sql`.
Every facility, mine or utility named is a **data match, not verified against primary records**.

| Lead | Verdict | Grade |
|---|---|---|
| RCRA_EVALUATIONS | **CONFIRMED** (sharpened) | B |
| NPDES_QNCR_HISTORY | **NARROWED** | B |
| SDWA_SITE_VISITS | **NARROWED** | B |
| SDWA_EVENTS_MILESTONES | **NARROWED** hard | C |

**Bad news up front**
- L4: the "only 276 of 1,029 have a notice row" contrast is mostly noise. 143 of the 1,029 had results reported *before* the rule. 393 are in states that never log the notice row. Clean contrast: **93 systems**, and 44 of those are too fresh to judge.
- L3: 63 of the 117 are purchased-water systems, and 58 last had a survey in 2020 to mid-2021, the COVID slip. The hard core is smaller: **59 systems, 5.9M people, last surveyed 2019 or earlier.**

---

## RCRA_EVALUATIONS: CONFIRMED

**Claim as written:** at sites where EPA found hazardous-waste violations, a state inspection of the same site within 2 years found violations 15.5% of the time in IL (41 sites), 28.5% NJ, 34.5% PA.

**What I checked**
- Reran deep's pairing (1-730 days, deduped CEIs). **It reproduces:** IL 15.5% of 41, NJ 28.5% of 87, PA 34.5% of 78.
- **"41 sites" is really 41 EPA inspections** at 38 distinct sites (NJ 87 at 80, PA 78 at 78). Max 2-4 inspections on one site. No single site drives it.
- **Joint inspections:** deep dropped same-day pairs. There are 965 same-day state CEIs at EPA-found inspections, and the state logs Y on **85.7%** of them. Almost all are in KY (100) and NC (114). IL has 0, NJ 3, PA 13. **So joint logging does not touch IL/NJ/PA.**
- **"It got fixed in between":** split by which visit came first.

| State | State inspected BEFORE EPA: pairs, % Y | State inspected 31-730 days AFTER: pairs, % Y |
|---|---|---|
| IL | 25, **12.0%** | 33, 21.2% |
| NJ | 65, **20.0%** | 64, 21.9% |
| PA | 83, 36.1% | 64, 26.6% |
| WI | 28, 82.1% | 48, 79.2% |
| All states | 1,434, 39.5% | 1,142, 42.4% |

  The state inspecting first finds *fewer* violations in IL and NJ, so fixes between visits can't explain it.
- **Is EPA's finding real?** Did EPA open a formal enforcement action (RCRA type code 200+) within a year of the finding? IL **87.8%**, NJ 72.4%, PA 39.7%. The IL and NJ findings weren't paperwork noise.
- **Control, the part that changes the framing:** the same states' hit rate at sites where EPA found nothing, and their overall CEI rate:

| State | State % Y where EPA found | where EPA clean | state's own CEI baseline |
|---|---|---|---|
| IL | 15.5 | 9.4 | 15.3 |
| NJ | 28.5 | 11.2 | 17.6 |
| PA | 34.5 | 20.0 | 23.9 |
| WI | 80.8 | 68.8 | 83.6 |

**What a hit means / what a miss means**
- Hit, which is what came back: IL inspectors find violations at a site EPA just wrote up, and EPA then took formal action, at the **same ~15% rate they find them anywhere**. The same-site test holds up, but what it shows is each state's write-up habit, not a missed site.
- A miss would have been state rates near EPA's at the paired sites. They weren't, in either time order.
- Not tested:
  - Whether EPA cites federal-only rules the state isn't authorized for. The next check is violation citations by type.
  - IL, NJ and PA's own State Review Framework reports. EPA's SRF grades exactly this ("accurate identification of violations"), so the pattern may already be on record there.

**Corrected headline:** Where EPA inspectors found hazardous-waste violations and went on to formal enforcement (88% of the time in Illinois), Illinois state inspectors visiting the same sites within two years found violations only 15.5% of the time (41 EPA inspections, 38 sites), the same rate Illinois finds anywhere. It's 28.5% in NJ (87) and 34.5% in PA (78), against 80.8% in Wisconsin (55).

**Portfolio grade:** B. The counts are small (25-87 pairs per state), and it needs the state's SRF report as an outside check.

**Next join that would make it a story:** `RCRA_VIOLATIONS` on `ID_NUMBER` + date, EPA-found violation types at the IL/NJ pairs vs the state's citations. Then `RCRA_ENFORCEMENTS` penalty amounts (PMP/FMP) on the same sites.

---

## NPDES_QNCR_HISTORY: NARROWED

**Claim as written:** 553 permits broke effluent limits in 36+ of 40 quarters 2016-2025; 152 got no formal action; WV chronic mines got formal action 26% vs 58% for other chronic.

**What I checked**
- Reran it. **553 / 152 reproduce exactly.** WV: 22 of 85 chronic mines (25.9%) vs 110 of 191 chronic sewer plants (57.6%). Both reproduce.
- **"No action at all" is partly states that don't upload.** 69 of the 553 have neither formal nor informal action. **29 of those 69** sit in states that log about 0% informal actions to ICIS on *any* long-reporting permit: WV 15, MA 5, MD 5, PR/VT/NV/MP 1 each.
- **No formal action, by state habit:** 44 of the 152 are in states where only 6-16% of all long-reporting permits get any formal action: MO 19, AK 10, CO 6, MD 5, WA 4. That's thin enforcement *or* thin upload, and this table can't tell which.
- **WV, same agency code:** mine and sewer formal actions are both coded "State" (EPA did 0 of the 22 mine actions). So it isn't a state-vs-EPA split.
  - 60 of the 85 chronic mines have **never** had a formal action in ICIS. For sewer plants it's 40 of 191.
  - Only 1 mine's last action falls in 2010-2015, so pre-2016 consent decrees don't explain it (as logged in ICIS).
- **Still going:** 83 of the 85 chronic WV mines had effluent-violation quarters in 2024-25. Mines average 7.3 violations per bad quarter vs 5.1 for sewer plants.
- **Is the state the permittee?** No chronic-mine name looks like a forfeited or state-held reclamation site (0 hits on RECLAMATION / FORFEIT / WVDEP).

**What a hit means / what a miss means**
- Hit: within one state and one reporting agency, chronic coal-mine permits almost never show a formal action. For sewer plants it's the reverse.
- The boring version that can't be killed from here: WV mining NPDES permits are enforced by the DEP's mining division under the state mining law (NOVs, cessation orders). Those may never reach ICIS. There's **no SMCRA/OSMRE or WV DEP enforcement table in the warehouse** (metadata check found none).
- The national "152 / 69" should not be sold as "no enforcement." It's "no enforcement in EPA's federal database."

**Corrected headline:** In West Virginia, 60 of 85 coal-mine water permits that broke effluent limits in 20+ of 40 quarters (2016-2025) have never had a formal enforcement action in EPA's national database, against 40 of 191 chronic sewer plants in the same state. 83 of the 85 were still violating in 2024-25. Nationally, 152 of the 553 worst permits show no formal action since 2016 in that database.

**Portfolio grade:** B. It needs WV DEP's own enforcement list for about 5 named mines (Sugartree, Westridge, Rush Creek, Peach Orchard No. 5, Berry Branch) before "no enforcement" can be said.

**Next join that would make it a story:** there's no in-warehouse fix. Operator names would come from `ENVIRONMENT__FED_EPA_ECHO` (FRS) by name + city, which is fuzzy. The real join is outside: WV DEP enforcement records on permit number.

---

## SDWA_SITE_VISITS: NARROWED

**Claim as written:** 117 big water systems, 8.7M people, have no sanitary survey on file in 5 years; the legal limit is 3.

**What I checked**
- **117 / 8,725,950 reproduces.** The system table has 1 row per PWSID, so there's no double count. All 117 are in the 2026Q2 roster, and 107 reported lead results since 2023, so they're alive.
- **Purchased water:** **63 of 117 (3.51M people)** buy their water (SWP/GWP). They're still under the survey rule, but they're distribution-only systems.
- **Reporting lag:** median visit-to-upload lag for big-system surveys is 92-165 days by state. p90 is 285 days in CA and about **1,450 days in WA**. The 9 WA systems (514K people) could be upload backlog.
- **States do upload.** Big systems surveyed per year are steady 2016-2025 (CA 101-177, NJ 31-98). The gap is specific systems, not a state that stopped reporting.
- **When they were last surveyed:**

| Last survey | Systems | People |
|---|---|---|
| 2010-2018 | 39 | 2.52M |
| 2019 | 20 | 3.38M |
| 2020 | 23 | 0.95M |
| 2021 H1 | 35 | 1.88M |

  58 systems (2.82M) last surveyed in 2020 to mid-2021: that's the COVID slip. They're still 2+ years past the 3-year clock.
- **By state:**
  - **NJ:** 26 systems, 2.28M people. **21 of them last surveyed 2014-2016.** Only 1 has had no visit of any kind. They get records, investigation and Level 1/2 assessment visits (RSCH, INVG, LV1A, LV2A), just not surveys.
  - **CA:** 41 systems, 4.25M people. 35 of them have **no visit of any kind** logged since 2021-07.

**What a hit means / what a miss means**
- Hit: big systems with no survey on file for 7-16 years, while their state keeps surveying its other big systems on a roughly 3-year cycle.
- A miss would have been the gap disappearing once you allow for lag, purchased water or partial codes. It shrinks but doesn't go away.
- Not ruled out: CA and NJ surveys recorded under another PWSID (for example, a wholesaler parent), or kept only in state files.

**Corrected headline:** 59 active water systems serving 10,000+ people (5.9M people) have no sanitary survey on file with EPA since 2019 or earlier, against a 3-year federal clock. New Jersey stands out: 21 of its big systems were last surveyed in 2014-2016, even though NJ inspectors logged other visits there through 2025.

**Portfolio grade:** B. It needs NJDEP and CA DDW to confirm survey dates for about 5 named systems.

**Next join that would make it a story:** `SDWA_VIOLATIONS_ENFORCEMENT` on PWSID, health-based violations 2021+ at these 59 vs big systems that were surveyed. That tests "unsurveyed and also violating."

---

## SDWA_EVENTS_MILESTONES: NARROWED

**Claim as written:** 1,029 systems over the lead action level since the new notice rule; 3.27M people; only 276 have a notice row.

**What I checked**
- **Units:** all PB90 rows are mg/L, 58,433 rows, no mixing. 2 systems read over 1 mg/L, which are likely typos.
- **1,029 / 3,271,425 people reproduces.** The system table has no duplicate rows.
- **Timing, the big hole.** Deep kept any sampling period *ending* after 2024-10-16. Many periods are 3 years long (median 1,095 days) and run to 2028-2033.

| When | Systems | With LALE | People |
|---|---|---|---|
| A: period starts after the rule | 402 | 163 | 2.23M |
| B: 3-year period started before, reported after | 484 | 108 | 0.87M |
| C: result reported **before** the rule | 143 | 5 | 0.18M |

  C can't owe a notice under the rule. For B the sample date is unknown.
- **Is the row supposed to exist in this file? Yes.** LALE rows carry reason code T1PN. Comments record the notice itself ("Posted on 10/10 ... Meets the 24 hrs", "hand delivered to all residents"). It's a state-entered record that the notice was given.
- **But ~20 states never enter it:** PA (62 post-rule systems over the limit, 0 rows), FL 12, CA 12, MD 7, MN, MA, OH, CO. Same pattern as the LSLI gap deep already found. States that do enter it are near-complete: IL 29/34, WI 18/19, OR 15/17, GA 9/9, MI 11/12, VA 5/5.
- **Clean contrast** (period starts after the rule, state logs LALE): 256 systems, 163 with a notice row (64%), **93 without** (301K people).
  - 44 of the 93 had their result reported since 2026-03. LALE rows upload a median 58 days late (p90 167). **Too fresh to call.**
  - 16 have a public-notice violation (code 75) logged since the rule. The state itself recorded a notice failure. Examples: Morton Grove IL, Marseilles IL, Burnham IL, Grand Portage. Code 75 isn't tied to lead in my query, so this is an upper bound.
  - **42 have an older result and no PN violation.** That's the real unexplained gap.
  - Gaps bunch up in NY (17 over, 0 rows while NY logs 2 elsewhere), TX (12 of 28), VT (2 of 11) and ME (1 of 7).

**What a hit means / what a miss means**
- Hit: in states that record lead notices, about a third of post-rule exceedances have no notice record. After lag, it's about 42 systems with no trace, plus 16 where the state logged a notice violation.
- The "1,029 vs 276" framing is a miss as written. Most of the gap is states that don't upload, three-year periods, and pre-rule results.

**Corrected headline:** Since the October 2024 lead-notice rule, 402 water systems (2.2M people) tested over the lead action level in a monitoring period that started after the rule. In the states that record these notices, 163 of 256 have one on file. Of the 93 that don't, 16 were cited for a notice violation and 42 have no trace of either. The biggest are Mundelein IL (31,500), Garden City (V) NY (23,272) and Amsterdam NY (20,700).

**Portfolio grade:** C. It's a footnote until NY/TX notice status is checked. The 1,029 number is not usable.

**Next join that would make it a story:** `SDWA_VIOLATIONS_ENFORCEMENT` on PWSID, restricted to code 75 with a lead-linked rule. Tie each PN violation to its ALE by date. Then `SDWA_PUB_WATER_SYSTEMS` for owner type (NY villages vs investor-owned).

---

## One line per lead

- RCRA_EVALUATIONS | CONFIRMED | B | Where EPA found violations and followed with formal enforcement (88% in IL), IL state inspectors found violations at the same sites within 2 years 15.5% of the time (41 inspections, 38 sites), their normal rate anywhere; NJ 28.5%, PA 34.5%, WI 80.8%.
- NPDES_QNCR_HISTORY | NARROWED | B | 60 of 85 chronic WV coal-mine permits have never had a formal action in EPA's database, vs 40 of 191 chronic WV sewer plants; 83 of 85 still violating in 2024-25. "No action" means none in ICIS, not none at all.
- SDWA_SITE_VISITS | NARROWED | B | 59 big water systems (5.9M people) have no sanitary survey on file since 2019 or earlier, against a 3-year clock; 21 NJ systems last surveyed 2014-2016.
- SDWA_EVENTS_MILESTONES | NARROWED | C | 402 systems over the lead limit in post-rule periods; in states that log notices, 163 of 256 have one, 16 were cited for a notice violation, 42 have no trace.
