# Deep pass 16: SBIR awards, Retraction Watch, NTSB aircraft, NTSB events

2026-09-24. Python door, tag `coverage-r2-2026-09-24`. **33 of 35 statements**, all logged in `deep-16.sql`. S10 failed to compile and still counts. Each of the 8 connections also ran the two ALTER SESSION lines. Those 16 aren't counted.
This group held **4 tables, not 5**.
Every person, company or aircraft named here is a data match. None is checked against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT | **live** | 420 planes the NTSB rated destroyed still hold a valid FAA registration issued before the crash. 344 of those crashes were fatal (663 dead) | Nearly all are recent: 0.9% of 2008-15 wrecks, 82.5% of 2024-26 wrecks. Lag is the boring half. The open half is how long "valid" lasts now |
| TRANSPORT__FED_NTSB_AVIATION_EVENTS | probed | Air-ambulance accidents: 59 of 184 fatal (32.1%). The rest of Part 135: 122 of 680 (17.9%) | Known story, and the gap closed: 38.7% fatal in 2008-13, 22.2% in 2020-26. LNA airport is a real statistical outlier with no common thread |
| SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE | probed | 31 US authors with 3+ misconduct retractions got $67.1M in NIH awards dated after their last one. The 14 whose institution agrees hold $39.1M | Same wall as F-008: the data doesn't say which author cheated. The top name is a co-author on a known lab scandal |
| SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | probed | Top 20 firms take 8.1% of $41.04B (2015-25). The 38 firms with 100+ awards take 11.5% | Mills exist, but money isn't concentrated. "Never sells a product" can't be tested: there's no sales column |

---

## 1. NTSB aircraft + FAA registry: **live**

**The triage angle first: dead.** It asked about repeat operators and repeat tails.
- US Part 121 (airlines): 741 events, 7 fatal, 159 operator names. Southwest tops with 78 events and 1 fatal. That's fleet size.
- US Part 135 (charter, cargo, air ambulance): 893 events, 161 fatal, 550 operator names.
  - Air Methods tops under three spellings: 34 events, 9 fatal, 27 dead.
  - It runs the biggest air-ambulance fleet, so that's fleet size too.
- Tails with 2+ US Part 121/135 events: 63 of 1,578. 48 are on the FAA registry, and 43 have a matching serial. Mostly airliners with minor events. Nothing there.

**Checked: the join that made it**
- Every US aircraft the NTSB rated DEST (destroyed) that has an N-number and a serial: 2,123.
- Joined to the FAA registry on N-number. The registry is an August 2026 snapshot with 315,447 rows. Second field: the serial number has to match.
- 632 of those tails are still on the registry. 470 have the same serial.
- The other 162 have a different serial. Most are N-numbers reissued to other planes: N207DR was a Cessna 208B, serial 208B0859, destroyed in 2011, and now sits on a different serial. Some may be serial-format mismatches.
- **420 of the 470 are status V (valid), with a certificate issued before the crash, not expired.** 344 of those crashes were fatal, with 663 dead.
- Owner check: when the NTSB names an owner, the first six letters match the FAA registrant 185 times out of 192.

By crash year:

| Crashed | Destroyed | Still valid | Share |
|---|---|---|---|
| 2008-15 | 756 | 7 | 0.9% |
| 2016-20 | 762 | 31 | 4.1% |
| 2021-23 | 365 | 184 | 50.4% |
| 2024-26 | 240 | 198 | 82.5% |

Worst examples:
- **N321BA**, Bering Air Cessna 208B, Nome AK, 2025-02-06, 10 dead. Still V to Bering Air Inc, expires 2028-03-31.
- **N221BN**, Pacific Aerospace 750XL, Butler MO, 2026-06-14, 12 dead. V to SkyHi Aero LLC, expires 2030-01-31.
- **N93012**, the B-17, Windsor Locks CT, 2019-10-02, 7 dead. V, certificate from 2007, expires 2029-11-30.

On the registry side:
- 309,255 of the 315,447 rows are V.
- 206,217 valid rows (67%) were last touched in 2023. The top day, 2023-01-22, holds 12,107.
- That fits the FAA moving registrations to seven-year terms in early 2023. **Not checked against the rule text.**

**Hit means:** the registry's "valid" flag doesn't show whether a plane still exists. Since about 2021, a plane destroyed in a fatal crash can stay "valid" for years. The owner is supposed to send the certificate back after a total loss. This says most owners don't, and expiry was doing the cleanup.

**Miss means:** it's paperwork lag with no story if either of these turns up:
- the 2021-23 planes are rebuilt wrecks, or
- the FAA's deregistered file shows them cancelled while the master file lags.

**Boring**
- **Paperwork lag: half ruled in.** Older wrecks are clean (0.9%). The open question is how long the lag runs now. The 2021-23 wrecks are 3 to 5 years old, and half are still valid.
- **Rebuilds: not ruled out.** NTSB "destroyed" means too costly to fix, not scrapped, and some come back. Fatal wrecks come back less often, and 344 of the 420 were fatal.
- **Time since the crash muddies any before/after-2023 read.** One snapshot can't tell "longer terms" apart from "less time to clean up."

**Next pass:**
- Pull the FAA deregistered file.
- Read the 2023 seven-year rule.
- Use an AIRWORTHINESS_DATE after the crash as a sign of a rebuild.

---

## 2. NTSB events: probed

**Checked**
- 30,968 events, 2008-01-01 to 2026-07-29. 25,161 are in the USA.
- **Deaths (INJ_TOT_F) sum to 16,688, but US events hold only 7,166.** The other 9,522 died in foreign crashes the NTSB assisted on. The facts line's "Manas 35" is one of them.
- Fatal share by type of flight:
  - The denominator is US accidents in that group, counting the first aircraft in each event.
  - The warehouse has no flight hours, so these aren't true accident rates.

| Group | Accidents | Fatal | Fatal % | Deaths |
|---|---|---|---|---|
| 91 other private | 14,603 | 2,665 | 18.2 | 4,610 |
| 91 homebuilt | 3,310 | 742 | 22.4 | 952 |
| 91 instruction | 3,365 | 301 | 8.9 | 507 |
| 137 crop dusting | 1,187 | 144 | 12.1 | 146 |
| 135 charter/cargo, not tour or medical | 612 | 108 | 17.6 | 280 |
| 135 air medical | 126 | 34 | 27.0 | 103 |
| 91 air medical (legs with no patient) | 51 | 21 | 41.2 | 60 |
| 135 air tour | 68 | 14 | 20.6 | 62 |
| 91 air tour | 206 | 28 | 13.6 | 98 |
| 133 external load | 124 | 29 | 23.4 | 41 |
| 91 skydiving | 114 | 19 | 16.7 | 50 |
| 121 airline | 470 | 7 | 1.5 | 126 |

Air medical (AIR_MEDICAL = Y, any FAR part) against the rest of Part 135, by period:

| Period | Air-med accidents | Air-med fatal % | Air-med deaths | Other 135 fatal % |
|---|---|---|---|---|
| 2008-13 | 62 | 38.7 | 79 | 19.3 |
| 2014-19 | 59 | 35.6 | 57 | 16.8 |
| 2020-26 | 63 | 22.2 | 44 | 17.3 |

- Named operators with 3+ fatal US events: 16.
  - Air Methods (two spellings): 11 fatal, 33 dead.
  - Air Evac EMS: 5 fatal, 15 dead.
  - Dean International, a Florida flight school: 4 fatal in 14 events.
  - Guardian Flight: 3 fatal, 11 dead.
  - Paklook Air: 3 fatal, 10 dead.
- Airports:
  - **LNA, Palm Beach County Park, Lantana FL:** 10 of 22 accidents fatal, 45.5%. All US accidents tied to an airport run 13.9%.
  - z = 4.29. It's the only one of 110 airports with 15+ accidents at z of 3 or more. The binomial tail is 0.00035, so chance is unlikely even across 110 airports.
  - The 10 share nothing:
    - All Part 91, 2009-2023.
    - Ten different planes and operators.
    - 8 in daylight, all in good weather.
    - 6 off the airport.

**Hit means:** air ambulances crash deadlier than other charter flights.

**Miss means:** the gap has mostly closed. Air ambulances were 2x the rest of Part 135 in 2008-13 and are 1.3x now. No operator stands out today.

**Boring**
- **Air ambulance: known, not ruled out.** Helicopter air-ambulance deaths were an NTSB priority, and the FAA's 2014 air-ambulance rule went after them. Air Methods tops the list because it has the biggest fleet.
- **LNA: a lead, not a story.** No common operator, aircraft or weather. It's a busy training field near the coast.

---

## 3. Retraction Watch: probed

**Checked**
- 71,388 rows, 71,388 record IDs, retraction dates 1756 to 2026-07-17.
- The FED_RETRACTION_WATCH copy has 71,591 rows, 71,377 IDs and the same last date. **Two copies of one source.**
- US misconduct retractions, 2010-2026, retractions only: 1,532 papers, 6,423 author names.
  - Misconduct means one of these reasons: fabrication or falsification, image manipulation, paper mill, misconduct by author, official misconduct finding, ORI, plagiarism, fake peer review.
- Only 156 US papers cite a paper mill. The paper-mill angle is really Chinese hospitals plus the Hindawi mass retractions. Not chased.
- The top US names are the known repeat offenders Retraction Watch already ranks. Retraction counts:
  - Fazlul Sarkar 41
  - James Hunton 35
  - Stanley Rapoport 22
  - Piero Anversa 18
  - Bharat Aggarwal 16
- **The join:** authors with 3+ misconduct retractions, 2010-2025, matched to NIH RePORTER by first and last name. A match only counts when the name maps to one NIH profile.
  - 433 repeat authors. 418 have a usable name. **95 land (22%).**
  - 31 got NIH awards dated after their *last* misconduct retraction: **$67.1M**.
  - Second field, institution, on those 31:
    - 14 agree between the retraction and the NIH grant. They hold $39.1M.
    - 4 are clearly the wrong person, $7.97M. Example: an author at an Iranian university matched to Nova Southeastern.
    - 13 are plausible job moves, not checked.
  - Top four (data match):
    - Joseph Loscalzo: $9.75M after 2018-12-12, 4 retractions, Brigham. He's a co-author on the Anversa-lab papers.
    - Craig Elmets: $6.61M.
    - Jeffrey Elmendorf: $5.83M.
    - Roger Colbran: $4.64M.
  - The famous names got **$0** after their last retraction: Sarkar, Rapoport, Jasti Rao, Paul Dent.

**Hit means:** repeat co-authors of misconduct papers kept winning NIH money.

**Miss means:** the people most tied to misconduct got nothing after. That's the system working.

**Boring**
- Retraction Watch lists every author, not the one who cheated. Senior co-authors and department heads keep getting grants either way.
- **Not ruled out.** It's the same wall F-008 hit, graded C. The respondent names in ORI findings would break it, and that table isn't in the warehouse.
- The $67.1M undercounts second-listed PIs. See trap 4.

---

## 4. SBIR: probed

**Checked**
- 219,503 awards, $82.16B, 1983-2026. 66,703 have no UEI ($15.20B).
- 2015-2025: 68,081 awards, $41.04B, 15,710 firms after name clean-up.
- How concentrated the money is, 2015-25:
  - Top firm, Physical Sciences Inc: 687 awards, $411.6M, 1.0% of dollars.
  - Top 20 firms: 8.1% of dollars, 9.6% of awards.
  - The 157 firms with the most awards (top 1%): 21.3% of dollars.
  - 38 firms with 100+ awards: 11.5%. 107 firms with 50+: 18.0%.
  - 6,597 firms won exactly one award.
- Phase II awards per Phase I award:
  - 0.60 for firms with 100+ awards.
  - 0.68 for firms with 10-99.
  - 0.53 for firms with under 10.
  - Mills move to Phase II about as often as their peers.
- Duplicate-title screen: same firm, same title, same phase, titles 25+ characters. 1,015 groups, $2.61B.
  - Nearly all sit in one agency, or a pair of DoD branches sharing a topic code. That's a sequential or transferred Phase II, which is allowed.
  - Across two departments: 14 groups, $20.7M. Example: Kalyra Pharmaceuticals, same non-opioid painkiller title, NIH 2015 $2.47M and DoD 2017 $1.0M. A lead list, not a finding.

**Hit means:** a few dozen firms live on SBIR money. That's known and legal.

**Miss means:** the top firm holds 1%. No one firm dominates.

**Boring**
- **Ruled in.** SBIR mills are known, reported and legal, and Congress added performance benchmarks for firms that win a lot.
- F-022 already mined the Newington address.
- "Never commercialize" needs a sales or Phase III column. There isn't one.

---

## Traps found

1. **57% of deaths in NTSB events are foreign.** INJ_TOT_F sums to 16,688, and US events hold 7,166. Filter on EV_COUNTRY = 'USA'.
2. **NTSB OPER_NAME "On File" is a placeholder.** It ranks #1 among operators with 3+ fatal events (29 events, 8 fatal). Drop it along with "Pilot".
3. **NTSB highest injury FATL with zero deaths:** 20 US events. The reverse never happens: every event with deaths has the flag.
4. **NIH PI_PROFILE_IDS uses commas, but PI_NAMES uses semicolons.** That's on 192,270 of 192,333 multi-PI rows, FY2010-26.
   - F-008 and S17 split both columns on ';'. The first PI gets the whole ID list and every other PI's row drops out.
   - So F-008's one-profile check and its dollar totals are off for multi-PI grants.
5. **SBIR NUMBER_EMPLOYEES is one value per firm, copied onto every award.** 99.8% of the 3,965 firms with 10+ awards have one value or none. It isn't headcount at award time.
6. **SBIR contract numbers aren't unique.** 1,342 extra rows share a contract number and amount with another row: $435.3M, 0.53% of dollars. The worst, NAS961, sits on 138 rows (old NASA numbers, cut short).
7. **Retraction Watch is loaded twice:** XC_RETRACTION_WATCH_DATABASE (71,388 rows) and FED_RETRACTION_WATCH (71,591 rows, 214 repeat IDs).
8. **A V on the FAA registry doesn't mean the plane exists.** 420 destroyed planes show V. 82.5% of those destroyed in 2024-26 still do.

## Statement count

33 of 35. All are in `reports/coverage_2026-09-24/deep2/deep-16.sql`, labeled S01 to S33.
