# Deep pass 9: five tables, 35 statements

2026-09-24. Door: Python. Tag `coverage-b-2026-09-24`. Read-only.
SQL: `reports/coverage_2026-09-24/deep/deep-9.sql` (numbers in brackets below point to it).
Every person or company named here is a **data match, not verified against primary records**.

## The menu

| Table | Verdict | One line |
|---|---|---|
| OSHA 300A 2025 | **live** | SpaceX, Ford and Bath Iron Works still run 2.5-3x their industry peers in 2025. The deaths angle is dead. |
| FAA aircraft registry | probed | Sanctions join is empty. One lead: Aircraft Guaranty's trustee arm still holds 364 valid tails and added 38 since 2024. |
| DOJ Epstein Wayback | probed | 94% of "edits" are 50-byte page churn. One real edit: 11 court-record pages renamed to drop plaintiff names, Feb 22-25, 2026. |
| NIH RePORTER | probed | Overhead-by-school numbers hold up, but the cap fight already published them. |
| Member PAC money | probed | Numbers check against FEC within 4%. The top of the list is the 2024 Senate battlegrounds, which everyone has already published. |

---

## 1. OSHA 300A 2025 — **live** (as a year-on update, not a new find)

**Size.** 383,283 sites, 778 deaths [1]. 2024: 398,620 sites, 812 deaths.
- ⚠️ The trap note says "2025 file is half-loaded". It isn't: it holds **96%** of 2024's rows. The 2025 filings stop at 2026-03-15. The 2024 table runs to 2025-12-31, so only the late filers are missing.

### The year-on table [14]

Rate = recordable cases (days away + job transfer + other) per 200,000 hours worked, which is per 100 full-time workers.
Peer = every other site in the same 6-digit NAICS that year, with the company taken out. It falls back to 4-digit when peers log under 5M hours.
Only sites logging 500-4,500 hours per worker count.

| Company | 2024 rate / peer / ratio | 2025 rate / peer / ratio | Sites 24 → 25 |
|---|---|---|---|
| SpaceX (name tag) | 1.86 / 0.57 / **3.27x** | 1.91 / 0.61 / **3.12x** | 16 → 31 |
| Ford Motor | 8.68 / 4.05 / **2.14x** | 6.66 / 2.70 / **2.47x** | 52 → 80 |
| Bath Iron Works | 12.70 / 4.21 / **3.01x** | 11.82 / 4.42 / **2.67x** | 1 → 1 |
| Electric Boat | 4.09 / 4.86 / 0.84x | 4.08 / 5.04 / 0.81x | 10 → 3 |
| Ingalls / HII | 4.78 / 4.66 / 1.03x | 5.19 / 4.70 / 1.10x | 2 → 2 |

- **Bath is clean**: one site, 6,638 workers, 662 cases, 11.82 against 4.42 at other shipyards (336611) [34].
- ⚠️ **The SpaceX tag pulls in contractors** [34]: ABM janitorial, PCAM valet, Performance Contractors and Austin Commercial at SpaceX sites. They add 39 of the 478 cases and about 5.1M of the 50M hours.
  - SpaceX's own 10 sites (EIN 010627671): **439 cases on about 44.9M hours = 1.96**. Starbase alone is 3.01, Hawthorne 1.47.
  - Own-site peer ratio not rerun (out of budget). F-035 found own sites alone run *higher* (about 4.7x in 336414).
- ⚠️ **Ford's 2025 filing adds offices** (541330 engineering, 561110 admin). The 80 sites mix plants with desks. The ratio is still per-industry, but it needs a plants-only rerun (3361xx/3363xx) to compare like with like.

**Checked:** the SpaceX, Ford, Bath, Electric Boat and Ingalls sites matched by name in both years, each benchmarked against its own 6-digit industry with the company removed.
**Hit means:** the F-035 to F-037 pattern held a third year. "Still 3x after the Reuters exposé" is a real update line.
**Miss would have meant:** the gap closed, and the 2023-24 story was a blip.
**Boring:** SpaceX sites are thin 6-digit pools (481212 falls back to 4-digit), so the benchmark is fragile. Contractors and offices blur the tags. Neither is ruled out until the EIN-only and plants-only reruns.

### Deaths angle — dead [11][12][26]
- Top of the death list = **known disasters + typos**:
  - Accurate Energetic Systems, McEwen TN, **16 deaths**. Matches the October 2025 explosives-plant blast.
  - UPS airline, Louisville, 3. Matches the November 2025 UPS crash. U.S. Steel Clairton, 2. Matches the August 2025 blast.
  - Rosen Inn, Orlando: **10 deaths, 0 recordable cases** at a hotel. Capriati Construction: 6 deaths, 0 cases. Both look typed.
  - A **column-shifted row** ("Grand Prairie", company "332321", state "1") carries a fake 16 deaths.
- **193 shifted rows** (state not two letters, or company name all digits) carry **18 deaths** [26].
- Only 8 of 691 death sites also had a death in 2024 (412 matched a 2024 row with the same ZIP).
- National rate on clean rows: 0.95 deaths per 100M hours.

### Top injury-rate angle — dead as a quick story [26]
- 4,368 sites with 500+ workers and 30+ cases. **276 (6.3%) run 3x+ their peers.**
- The top of that list is wrong industry codes and typos:
  - Cleveland Clinic Beachwood: 2,192 cases on 541 workers.
  - Sunrise Hospital filed as 524114 (insurance).
  - A Wegmans store filed as 551114 (company HQ).
- A ranking needs every NAICS checked by hand first.

---

## 2. FAA aircraft registry — probed

**Size.** 315,447 tails, one row each [9]. There's no "trust" owner code. Trustees file as corporation (3), LLC (7) or co-owner (4).

| Count | Number |
|---|---|
| Tails with TRUSTEE in the owner name | **13,037** (4.1%) |
| Jets (turbojet/turbofan) held by trustees | **4,319 of 29,000** (14.9%) |
| Non-citizen corporations (code 8) | 2,097. Top: Cirrus 427, Piper 165 — plane makers, boring |

Biggest trustees [23]: Bank of Utah 1,844 (1,314 jets). TVPX 1,419 (c/o NetJets, fractional). Wilmington Trust 623. International Air Services 602. UMB Bank 574. Southern Aircraft Consultancy 514. Aircraft Guaranty 359 + 5.

### Sanctions angle — dead [24][25][30][35]
- **Tail-number join: 0 hits.** One OFAC SDN record names an N-tail (166 name any tail), and 344 OpenSanctions airplane records exist. None is on today's US registry.
- **Exact company-name join: 0 confirmed.**
  - OFAC: 0 hits.
  - SAM exclusions: 3 hits. Every one has a different city (Twisted Distribution, Burleson TX vs Parkland FL; Medicine Shoppe, Covington TN vs Chillicothe MO; Twin Power, Wilmington DE vs Grimes IA).
  - OpenSanctions "sanctioned" hits are US bank enforcement orders and export settlements (FedEx, Lockheed, Honeywell, First National Bank). They aren't sanctions.
- ⚠️ Name-matching can't see through a trust anyway. The trustee *is* the name on file.

### The one lead: Aircraft Guaranty Corp Trustee [30][33]
- All at 928 SW 107th St, Oklahoma City: **364 tails, all valid, all unexpired.**
- New certificates by year: 2021: 1, 2022: 0, 2023: 1, then **2024: 6, 2025: 18, 2026: 14**.
- Press reports (outside the warehouse, **not verified here**) tie Aircraft Guaranty to its owner's 2023 federal conviction in a cartel aircraft-registration case.
- ⚠️ No warehouse list names the company or its owner: 0 hits in OpenSanctions, SAM or OFAC [35].

**Checked:** trustee names ranked by tails, registration status and certificate years; tails and names joined to OFAC, OpenSanctions and SAM.
**Hit means:** a trust company tied to a drug-plane conviction took on 38 new US registrations after the verdict.
**Miss would mean:** the trust changed hands or the FAA already reviewed it. The data can't tell.
**Boring (not ruled out):** trustee registration is legal and common. The Boston Globe covered this corner in 2019. A new owner may run Aircraft Guaranty now.
Southern Aircraft Consultancy re-issued 511 of 514 certificates in 2026 at a shared Casper, WY registered-agent address. That looks like an address move.

---

## 3. DOJ Epstein Wayback — probed

**Size.** 1,537,348 snapshots of 28,196 URLs, Dec 19 2025 – Jun 9 2026, with 201,548 distinct fingerprints [3].
- **0 PDFs. Every row is an HTML listing page.** Data sets 9, 10 and 11 alone hold 27,407 URLs and 96% of the snapshots (`?page=N` file lists) [15].
- Snapshots jump from hundreds a week to 85K-157K a week from March. That's a bulk crawl starting, not DOJ doing anything [16].

### "Quiet edits" — mostly churn [16][18]
| Fingerprint changes (status-200 snapshots) | Count |
|---|---|
| All changes | 173,284 |
| Size moved 50 bytes or less | **163,012 (94.1%)** |
| Size moved over 500 bytes | 945 (0.5%) |

- The big changes land on the **same days across every page** (2026-01-17, 01-30, 03-04, 03-18/19, 05-09/10). That's a site-wide template change or a release day, not a targeted edit.
- 401/403 answers are crawler blocks. They come back to 200 on almost every URL [17].
- 404s (67 rows) are mostly junk URLs (`%0A`, `%5C`) and guessed data sets 24-39 that never existed [27].

### The one real edit: plaintiff names stripped from court-record addresses [31]
- **11 cases, 15 named addresses** all answered **404 on 2026-03-05**:
  - Giuffre v. Maxwell; Farmer v. Indyke (x2); Bryant, Helm and Davies v. Indyke; Edwards v. Maxwell.
  - L.M., M.J. and C.L. v. Epstein; V.E. v. Nine East 71st Street.
- Every one has a **name-free twin** with the same case number ("court-records-v-indyke-no-119-cv-10479...", "court-records-v-maxwell-no-115-cv-07433..."). The twins were first saved 2026-02-25 and still answered 200 in June.
- Two named addresses were saved live first: Bryant v. Indyke and Edwards v. Maxwell, both **200 on 2026-02-22**. So the rename landed **between Feb 22 and Feb 25, 2026**.

**Checked:** each URL's snapshots in time order, with fingerprint and size changes, every non-200 answer, and every court-records address.
**Hit means:** DOJ edited on a specific date, and only the pages carrying a survivor's or party's name.
**Miss means:** everything else is page churn. This table can't see document pulls; it holds no documents.
**Boring (likely):** a privacy scrub, and small. 9 of the 11 cases' named addresses were only ever caught as 403 or 404, so we only know they existed because the crawler found links to them.

---

## 4. NIH RePORTER — probed

**Size.** 2,122,611 rows, FY2000-2026, one per application-year [7].
FY2024, NIH, parent rows only: $26.90B direct and $9.68B overhead = **36.0 cents per direct dollar** [21].
- 11,010 subproject rows ($4.43B) are left out, because they repeat parent money (per RePORTER's docs; not checked row by row).
- 4,489 parent rows ($7.60B) carry no overhead split.

Peer group: the 69 organizations with $100M+ direct. **Their median is 38.0 cents** [22].

| By overhead $ (FY2024) | Overhead | Rate | Loss at a 15% cap |
|---|---|---|---|
| Johns Hopkins | $239.8M | 36.3¢ | $140.7M |
| UCSF | $219.5M | 35.5¢ | $126.7M |
| Penn | $208.9M | 41.9¢ | $134.2M |
| Yale | $208.2M | 43.1¢ | $135.7M |
| Michigan | $206.2M | 36.6¢ | $121.8M |

- Highest rates vs the 38¢ peer median: Sloan-Kettering **57.6¢**, Scripps 49.4¢, Boston Children's 48.4¢, Dana-Farber 46.0¢, MD Anderson 46.0¢. Independent institutes and hospitals — the known pattern.
- The cap math applies 15% to total direct cost. The real cap used a smaller base, so treat these as rough. Across NIH: $9.68B − 0.15 × $26.90B = **$5.65B**.
- **Parked thread** [29][32]: the overhead share went 36.0% (FY24) → **37.6% (FY25)** → 40.0% (FY26, partial through Aug 8).
  - Inside research grants alone: 42.2% → 43.2% → 45.0%.
  - Research grants fell 8% in count (45,399 → 41,764) while direct dollars rose.
  - Likely mix plus multi-year funding. Not chased.

**Checked:** overhead ÷ direct by organization for FY2024 NIH parent rows, ranked by dollars and by rate within the $100M+ peer group, plus the trend by year and by mechanism.
**Hit means:** the list of who loses most under a cap.
**Miss means:** nothing new. The same list ran nationally in February 2025.
**Boring (confirmed):** negotiated rates are public and the cap fight was covered. F-008 already mined this table.

---

## 5. Member PAC money — probed

**Size.** 1,258 rows: 664 for 2024 and 594 for 2026, one per member per cycle, plus one blank-BIOGUIDE row per cycle [5].

2024 outside money (for + against) [19]:

| Member | Outside total | PAC |
|---|---|---|
| Bernie Moreno (OH) | $154.8M | $3.1M |
| Sherrod Brown (OH)* | $139.7M | $5.5M |
| Bob Casey (PA)* | $124.8M | $5.7M |
| David McCormick (PA) | $107.5M | $5.0M |
| Tim Sheehy (MT) | $82.1M | $1.7M |

\*Brown, Casey and Tester are named from their BIOGUIDE IDs. The name join covers sitting members only (146 rows in 2024 have no name).

- **Cross-check vs FEC independent-expenditure lines [28]:**
  - Moreno: $66.5M for / $85.6M against (mart: $69.1M / $85.6M).
  - Brown: $24.7M / $115.1M (mart: $24.6M / $115.1M).
  - Both agree within 4%.
- **The blank-BIOGUIDE 2024 row** holds $29.3M of PAC money from "2 donors", $237.6M for and $156.8M against. No single FEC candidate matches: Trump's lines are $134.8M / $142.2M. It's an unmatched rollup, not a person. Unresolved.
- 2026 so far: Cornyn $6.2M for (the Texas primary). **Massie $5.66M against vs $90.7K PAC from 28 PACs** (the push to unseat him, widely covered). The rest are special elections.
- PAC leaders are chairs and leadership (Guthrie $2.81M, Johnson $2.71M, Jason Smith $2.48M in 2026). Expected.

**Checked:** each cycle's members ranked by outside money and by PAC money, names from the money-raised table, and totals cross-checked against the raw FEC independent-expenditure file.
**Hit means:** a member whose outside help dwarfs their own PAC take.
**Miss means:** every top row is a Senate battleground.
**Boring (confirmed):** battleground Senate races draw outside money, and OpenSecrets publishes this exact ranking.

---

## New traps (not saved — the lead decides)

1. **OSHA 2025 shifted rows:** 193 rows have a non-state STATE or an all-digit COMPANY_NAME. They carry 18 deaths, including a fake 16-death row.
2. **OSHA deaths with zero cases:** hotel 10, construction firm 6. Read TOTAL_DEATHS next to the case counts before ranking.
3. **OSHA NAICS miscodes** dominate any "worst rate" list: hospitals filed as insurance, stores filed as HQ.
4. **The "half-loaded 2025" trap is stale:** the file holds 96% of 2024's rows; only the filings after the 2026-03-15 cutoff are missing.
5. **Company name tags catch contractors:** "SPACEX" matches ABM janitorial and PCAM valet sites. Tag by EIN.
6. **FEC IE `IS_SUPERSEDED` is 'True'/'False' with capitals.** `EXP_AMO` has billion-dollar typos: $18.8B and $18.5B on one 2024 presidential filer, $6.3B on an Oklahoma Senate filer, $17B against a 2026 Florida filer. Cap per-line amounts before summing.
7. **OpenSanctions "has sanctions" includes US bank enforcement orders and export settlements.** A US company name match is usually one of those.
8. **The Epstein Wayback table has no documents.** It's listing pages only, and 94% of fingerprint changes are 50-byte churn.
9. **FAA has no trust owner code.** Search the name for TRUSTEE.

## Housekeeping
- 35 statements, plus two `ALTER SESSION` per connection (5 connections). One compile error ([13], rerun as [26]). One empty result from the capital-letter flag ([20], rerun as [28]).
- ⚠️ I overwrote another agent's scratch runner (`scratchpad/q.py`, deep-5's) by mistake. I rebuilt it with the same behavior, pointed at `deep-5.sql` and `count.txt`. deep-5 should check its log if anything looks off.
