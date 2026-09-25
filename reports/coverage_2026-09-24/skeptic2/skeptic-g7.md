# Skeptic g7, round 2, 2026-09-24

Python door, read-only, tag `skeptic-r2-2026-09-24`. SQL in `skeptic-g7.sql`.
Statements: PHMSA 8, NOAA 7, VA 7. Three failed at compile and were rerun (noted in the .sql).
Every company named is a data match, not verified against primary records.

| Lead | Verdict | Grade |
|---|---|---|
| PHMSA flagged incidents | **NARROWED** (hard) | B |
| NOAA storm events | **CONFIRMED** as a recording story, one line overstated | B |
| VA suicide by state | **NARROWED** | C |

---

## ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS: NARROWED

**Claim as written:** 2025 is the worst year in 16 for gas lost from transmission lines, 5.21M units vs 1.4-3.0M. 63% is one Energy Transfer offshore line, Sea Robin.

**What I checked:**
- Landing columns (P2): the landing table has `GAS_COST_IN_MCF`, `EST_COST_UNINTENTIONAL_RELEASE`, `GAS_FLOW_IN_PIPE_IN_MCF`, `NARRATIVE`, `PIPE_FACILITY_TYPE`, `SYSTEM_PART_INVOLVED`.
- Sea Robin 2024+ rows and narratives (P3, P4): 11 rows, all final reports, all internal-corrosion pinholes offshore.
- Unit check (P5): cost / (volume x $ per MCF) = **1.000 median, 112 of 112 rows in 2025**. The Jan narratives also spell out "1,587,069 MCF". **Unit is MCF (thousand cubic feet). Settled.** (The cost is computed from the volume, so this confirms the unit, not the volume.)
- Years (P5): 2025 = 5,207,153 MCF. Sea Robin 3,286,741 (63.1%). Next year 2022 = 2,981,778.
- Top reports (P6): the 2022 number-two row (Equitrans, 1.29M) is **underground storage**, not a line.

**The break: the May report is a copy.**
- Reports 20250058 and 20250059 (Jan 13) each say: *"the unintentional volume was split between two incidents ... total volume for both incidents was 1,587,069 MCF."* So 793,534 x 2 is one January total, split on purpose.
- Report 20250066 (May 17) is a **different** leak. Confirmed 14:30, line isolated 14:37, clamped May 24. It claims **1,587,069 MCF**, the January total to the unit. Its narrative never mentions a volume.
- A one-week leak on an isolated line matching a four-month leak's total to the unit is a copy, not a measurement.
- Same pattern on the intentional side: 527,853 MCF sits on three reports (Jul 22, Aug 2 twice). All three narratives end "back in service 10-20-2025". One blowdown, three reports.

**Second doubt, not proven:** the January total may be too big too.
- `GAS_FLOW_IN_PIPE_IN_MCF` = 3,000 on the Sea Robin rows. If that is per day, full flow for the 121-day outage (Jan 13 to May 14) is about 363,000 MCF.
- The filing claims 1,587,069, **4.4x** that, from a line the narrative says was isolated at 13:30 on day one. An isolated line can only leak what is packed inside it.
- Not provable here: no line diameter, length or pressure in the warehouse, and the flow field's time unit is unconfirmed.

**Numbers after the fix:**

| 2025 version | MCF | vs 2022 (2.98M) |
|---|---|---|
| As filed | 5,207,153 | top |
| May copy removed | 3,620,084 | still top |
| Sea Robin removed | 1,920,412 | ordinary year |

**What a hit means / what a miss means:**
- Hit: the "worst year" rests entirely on one operator's self-estimates, one of them provably copied. That is a data-editing story: a federal filing carrying a number from another incident.
- Miss (PHMSA says the May figure is real): Sea Robin had the two biggest leak events in the table's history, four months apart. Still a story, a different one.
- Also: the table is **transmission + gathering + storage**, not "transmission lines". 2026 has 26 of 55 reports not final.

**Corrected headline:** Energy Transfer's Sea Robin line filed 3.29M MCF of 2025 gas loss, 63% of the national total. But its May report repeats, to the unit, the 1,587,069 MCF it gave as the two-leak total for January. Take out the copy and 2025 falls to 3.62M, still above 2022's 2.98M. Take out Sea Robin and 2025 is an ordinary year (1.92M).

**Portfolio grade:** B. Needs PHMSA's current record for report 20250066 (supplements can change it) or a question to Energy Transfer.

**Next join that would make it a story:** nothing in the warehouse. It needs PHMSA annual-report mileage (not landed) or BSEE offshore segment data, joined on `PHMSA_OPERATOR_ID` + segment, to check line pack against the claimed volume.

---

## ENVIRONMENT__FED_NOAA_STORM_EVENTS: CONFIRMED (one line overstated)

**Claim as written:** Phoenix office logged 1,345 of 2,145 US heat deaths (63%) 2018-2023, copied from Maricopa County. No heat events after June 2024.

**What I checked:**
- 2018-2023 totals (N3): US 2,145, Phoenix (PSR) 1,345. **Exact match.**
- Maricopa sourcing (N3): 1,338 of PSR's 1,345 deaths sit on rows whose narrative names Maricopa County. 17 zones carry deaths. Only 248 sit on 6 rows with 20+ deaths, so it is not one lump.
- Duplicates (N2): event IDs = rows in every year 2010-2025. No repeated events.
- **When it started** (N2): PSR logged 0-6 heat deaths a year 2010-2017 (20 total), then 157 in 2018. The Maricopa feed starts in 2018.
- Cutoff (N5): PSR heat rows in 2024: Apr 3, May 6, **Jun 122 (68 deaths)**, then **0 from July 2024 on**. July 2024 has 82 PSR rows of other types. 2025 has one heat row (a May hiker).
- Arizona outside PSR (N2): 2024 AZ heat deaths 147 vs PSR 73, so other AZ offices logged 74. 2025: AZ 50, PSR 1. **Only Phoenix went quiet.**
- Late filing (N6b + repo): landing has no file-version column. `scripts/noaa_storm_events_backfill.py` pulled 1996-2024 around 2026-06/07 (git dates, not a load log). So the 2024 file was at least 18 months past year end. A lag is unlikely, not ruled out: NCEI revises these files.

**What a hit means / what a miss means:**
- Hit: from 2018 on, federal Storm Data heat deaths measure one office's paperwork. When it stopped, the national count fell with it.
- Miss: none found. Rows are unique, the sourcing is in the text, the other Arizona offices kept filing.

**Overstated line:** "the 2024-25 drop is fake" goes too far.
- 557 to 99 is a fall of 458. Phoenix explains 351 of it (77%).
- Without Phoenix it is still 205, 177, 98: **down 52%**. Texas went 56, 3, 0. That part is unexplained, not fake.

**Corrected headline:** From 2018 to 2023 one Weather Service office, Phoenix, supplied 1,345 of the 2,145 heat deaths (63%) in the federal storm record, nearly all copied from Maricopa County reports. Before 2018 it logged 20 heat deaths in eight years. Its last heat event is June 2024. Without its entries the national 2023-2025 drop is 52%, not 82%.

**Already known?** Heat researchers know Storm Data undercounts heat and that NWS Phoenix uses Maricopa's reports. I know of no coverage of the mid-2024 stop. No web here, so unconfirmed.

**Portfolio grade:** B. Needs Maricopa County's own annual heat-death reports beside PSR's rows (from memory, not verified: about 645 in 2023, about 600 in 2024) and one email to NWS Phoenix asking why filing stopped.

**Next join:** no death-certificate table in the warehouse. `HEALTH__FED_CDC_LEADING_CAUSES_STATE` ends 2017; the CDC county injury file has no heat intent. The join is to Maricopa County's public report, on year.

---

## HEALTH__FED_VA_SUICIDE_STATE: NARROWED

**Claim as written:** Oklahoma veteran suicides 228 to 287 (2019-20 vs 2022-23), rate 37.9 to 50.7, general-population rate flat 20.4 to 20.3.

**What I checked:**
- Year rows (V4): OK 2015-2023 = 134, 115, 98, 127, 114, 114, 131, 126, **161**. Published rate = deaths / population exactly. Veteran population is rounded to thousands and reads 283,000 in both 2022 and 2023.
- General-population columns in the VA table (V2): **0 of 1,196 filled.**
- **Is OK an outlier? Empirical null** (V3): every state, every window pair (y, y+1) vs (y+3, y+4), 945 pairs:
  - SD of the Poisson z is **1.68**, not 1. State veteran counts wobble more than Poisson.
  - **17 of 945 pairs (1.8%) reach z of 4.9 or more.** About **0.9 states per window** by chance.
  - In the 2019 window OK is **first of 48 at z = 4.96**. Then Texas 4.19, Indiana 4.00, Kansas 3.79. Six states reach 3+.
  - So OK tops its window, at about the level the top state reaches in a typical window. Not a proven outlier.
- **Kansas** (V3): z = 3.79; 82 of 945 pairs (8.7%) reach 3+. **Noise level. Drop "Kansas shows the same shape."**
- Baseline (V4): 2019-20 (114, 114) is a low base. Against 2015-18 (average 118.5) the 2022-23 average (143.5) is **+21%**, not +26%. Without 2023, 2022 alone is +10.5%.
- **General-population line, same years** (V7): yes, 2019-20 vs 2022-23 on both sides. Panel rate 19.4, 21.3, 20.1, 20.5. Flat. **Confirmed.** But:
  - Only 26-31 of 77 OK counties have a count each year. The panel is **15 counties**, 516-573 deaths a year against 646-713 counted.
  - The last full-state count in the warehouse is 2017 (V6: 756; `CDC_LEADING_CAUSES_STATE` ends 2017). By that yardstick the panel holds about two-thirds of state suicides and misses rural Oklahoma, where veterans skew.
  - The "general" line **includes the veterans**. That makes the contrast slightly stronger, not weaker.

**What a hit means / what a miss means:**
- Hit: OK's 2023 repeats in 2024, and the gap to non-veterans holds statewide.
- Miss: 2023 (161) is a one-year spike. The table says about one state per window hits this level by chance.

**Corrected headline:** Oklahoma had the biggest rise in veteran suicides of any state from 2019-20 to 2022-23 (228 to 287), while suicides in its 15 largest-count counties held flat. Most of the jump is one year, 2023 (161), and a rise that size shows up in about one state per period by chance.

**Portfolio grade:** C. Footnote until VA's 2024 state data lands.

**Next join that would make it a story:** VA 2024 state sheet (not in the warehouse yet). Inside it: CDC `FA_Suicide` in the same county file on `GEOID`, same 15-county panel, for the firearm share. A full-state 2019-2023 general-population count is not landed.
