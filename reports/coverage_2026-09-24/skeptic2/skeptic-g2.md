# Skeptic round 2, group g2, 2026-09-24

Python door, tag `skeptic-r2-2026-09-24`. 15 statements (6 + 4 + 5), all SELECT/WITH, in `skeptic-g2.sql`.
Every person, company or building named here is a data match, not verified against primary records.

## Verdicts up front

| Lead | Verdict | Grade | One line |
|---|---|---|---|
| Section 8 / White Birch | **CONFIRMED** | B | Every number holds. It's a bigger outlier in Milwaukee than nationally. The $10.5M assumes 100% occupancy |
| NTSB destroyed, FAA still valid | **NARROWED** | B | 420 / 344 / 663 are exact. But "valid for years" is mostly the FAA's own 2023 extension sweep. 175 records were touched **after** the crash |
| ARCOS / Food City #674 | **NARROWED** | B | #1 holds, but only if you count long-acting 40-80mg. The chain peer group mixes in an unrelated Arizona chain. It's a Knoxville **cluster** of Food City stores, not one store |

---

## HOUSING__FED_HUD_MF_SECTION8_CONTRACTS: CONFIRMED

**Claim as written:** White Birch Apartments, Milwaukee. HUD pays $2,574/unit/month vs a national median of $859. That's 3.0x, at 223% of local FMR.
Also: 766 contracts over 150%, 7.5% of matched spending, $1.30B a year.

**What I checked**
- L1-1 contract row: one Active contract, WI39L000025, LMSA, 339 units, ratio **223.25**. 1BR FMR $1,119. Started 2023-12-01, 240 months. Matches.
- Bedroom math: FMR-weighted rent for its mix (207 1BR, 60 2BR, 65 3BR, 7 4BR) is $1,273. HUD $2,574 + tenant $240 = $2,814. That's 2.21x. **The two files agree with each other.**
- L1-2 Picture of Subsidized Households (Dec 2025): $2,574 spending, $240 tenant rent, 339 units. Matches.
  - ⚠ Only **292 occupied (86%)**. $2,574 x 339 x 12 = $10.47M. $2,574 x 292 x 12 = **$9.02M**. The report's $10.5M assumes every unit is full.
  - Tenants: 97% Black non-Hispanic, 91% under 30% of area median income, 7% age 62+. So it's not an elderly-services building.
- L1-3 owners file: one row. Aspen Crossing LIHTC LLC, Chicago, profit-motivated. Evergreen Real Estate Services manages it. **Ownership effective 2024-05-10**, five months after the new contract.
- L1-4 peer medians, same quarter, 15,574 project-based buildings:
  - National $859.5. Wisconsin **$598.5** (468). Milwaukee metro **$731** (118).
  - White Birch is #1 in Milwaukee and in Wisconsin.
  - Nationally, **434 buildings** sit at or above $2,574, and 1,700 are over 2x the national median. **It's not a national outlier.**
- L1-5 Milwaukee top 10: White Birch $2,574. The next is Clare Central at **$1,304**. That's a 2.0x gap to #2.
- L1-6 report totals: 766 over-150% contracts. 7.5% of matched spending, $1.30B. Matches.
  - Units share is 4.6%, not 4.3%. Minor.
  - At occupied units instead of total, it's $1.24B.
  - Ratio vs real spending correlates at only **0.30**. Over-150% buildings have a median of $1,020, the rest $852. **The FMR ratio is a weak proxy for dollars.** The report already said the lead is about 20 buildings, not 766.

**What a hit means / what a miss means**
- Hit: two HUD files agree on the building, the units and the dollars, and it sits 3.5x its own metro's median. The number is real.
- Miss would have been: a bedroom-mix artifact, or a PSH match to the wrong building. Neither happened.
- **Not ruled out, and it's the hinge:** new 20-year contract Dec 2023, then new tax-credit owner May 2024. That fits a legal recapitalization rent reset. A reset like that would make this a "HUD policy" story, not a waste story.
- Is it famous? Not known to me. North Milwaukee press may have covered the sale.

**Corrected headline:** White Birch Apartments (Milwaukee) costs HUD $2,574 per unit per month. That's 3.5x the Milwaukee metro median of $731 and 2x the next-costliest Section 8 building in the metro. At its reported 86% occupancy, that's about $9.0M a year. It began on a new 20-year contract in Dec 2023, and a tax-credit LLC took ownership in May 2024.

**Portfolio grade:** B. The chart is real. It needs one outside check: HUD's rent-setting basis for the 2023 renewal (market-rent study vs budget-based).

**Next join that would make it a story:** `HOUSING__FED_HUD_MF_FIRM_COMMITMENTS` on property name plus Milwaukee address, to find the 2023-24 recap loan. A rehab loan would explain the rent. No loan means the rent reset has no visible cost behind it.

---

## TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT: NARROWED

**Claim as written:** 420 planes the NTSB rated destroyed still hold a valid FAA registration issued before the crash. 344 of those crashes were fatal, 663 dead. Lag is the boring half. The open half is how long "valid" lasts now.

**What I checked**
- L2-1 registry rows: N321BA (Bering Air) cert 2021-03-05, last action 2023-04-28, expires 2028-03-31. That's a 7-year term.
  - The B-17 N93012: cert 2007, but **last action 2023-09-15**, four years after the 2019 crash. Expires 2029-11-30.
- L2-2 recount: **420 rows = 420 events = 420 tails.** 344 fatal, 663 dead.
  - Summed per distinct event: still 344 and 663. **Zero multi-aircraft events**, so no midair double count.
  - N-number is unique in the registry: 315,447 rows, 315,447 tails.
  - All 420 are unexpired. **0 have an airworthiness date after the crash**, so there's no sign of rebuilds.
  - ⚠ **177 of the 420 had an FAA action dated after the crash.**
- L2-3 by time since crash (destroyed / still V with pre-crash cert / of those, touched after crash):

| Since crash | Destroyed | Still V | Touched after crash |
|---|---|---|---|
| under 2 yrs | 170 | 141 (83%) | 1 |
| 2-4 yrs | 212 | 150 (71%) | 47 |
| 4-7 yrs | 424 | 109 (26%) | **109 (all)** |
| 7+ yrs | 1,317 | 20 (1.5%) | **20 (all)** |

- L2-4 the 177 touched records: **175 were touched in 2023.** 30 on 2023-01-22, the rest spread over 36 days in 2023. None expires 7 years after its touch date, so these don't look like owner renewals. 146 were fatal crashes.

**What a hit means / what a miss means**
- Every still-valid wreck older than about 4 years was **touched by the FAA in 2023**. That fits the 2023 move to 7-year registration terms being stamped onto records the NTSB had already rated destroyed. I did not read the rule text.
- The ones under 2 years old are plain paperwork lag.
- So "valid" is two things: recent lag, plus a 2023 bulk extension that ran with no destroyed-aircraft check. It is not owners renewing wrecks. The B-17 is the exception worth a look.
- Is it famous? Registry inaccuracy is a known issue (FAA re-registration drive around 2010). The 2023-extension angle is not known to me.
- Blind spot: `LAST_ACTION_DATE` says **something** happened, not what. Only the FAA deregistered/history file can say "extended."

**Corrected headline:** 420 aircraft the NTSB rated destroyed, from 344 fatal crashes (663 dead), still show a valid FAA registration. 175 of those records were updated by the FAA in 2023, after the crash, when registrations moved to longer terms. Every still-valid wreck more than 4 years old is one of them.

**Portfolio grade:** B. It needs the 2023 rule text and the deregistered file to name the action. Without them it's a good data-quality footnote.

**Next join that would make it a story:** the FAA deregistered-aircraft file on N-number plus serial. **It is not in the warehouse** (no match in the ledger). In-warehouse there's no partner that says what the 2023 action was.

---

## HEALTH__FED_DEA_ARCOS: NARROWED

**Claim as written:** Food City Pharmacy #674, Knoxville TN: 13.8M oxycodone pills of 30mg+, 2006-12. That's 64% of its pills vs a TN pharmacy average of 8%. #1 of 84,334 US pharmacies. Its own chain runs 4.7% at the median store, across 96 Food City pharmacies.

**What I checked** (ARCOS scanned only filtered or grouped by buyer, never joined raw)
- L3-1/L3-2 store BF7000526: 5,705 rows, all code S, all tablets, 2006-01-03 to 2012-12-31. One name.
  - **21,555,400** pills, **13,819,900** at 30mg+ (64.1%). Matches.
  - **Zero duplicate shipments** (same reporter, date, product, quantity, transaction id). All row keys end in -1.
- L3-3 product mix of the 13.8M:
  - Immediate-release 30mg: about **9.1M (66%)**.
  - Long-acting 40/60/80mg (OxyContin and generic ER): about **4.7M (34%)**.
  - The report cited only OxyContin 80 (1.6M) and understated the long-acting share.
- L3-4 national ranking, 84,334 pharmacies (VA mail-order excluded): Food City #674 is **#1 on 30mg+**. Next are J & H Stores 13.02M and Generic Depot #2 10.61M. Matches.
  - ⚠ On **immediate-release 30mg alone it's #3**: J & H 10.92M, Generic Depot 9.12M, Food City 9.10M.
  - TN 8.0% is the **pooled** share. The **median** TN pharmacy runs **3.5%**. The report's "average" label undersells the gap.
  - ZIP 37919: 19 pharmacies, 17.67M strong pills. Food City #674 and #694 hold 16.89M of it (96%).
- L3-5 chain peers:
  - ⚠ **Name trap.** "FOOD CITY" matches 93 buyers, including **16 in Arizona**. As far as I know, those are a separate grocery chain (Bashas'-owned), not the Tennessee/Virginia/Kentucky Food City. The report's chain median of 4.7% mixes the two.
  - Real footprint medians: TN **12.0%** (56 stores), VA 1.3% (14), KY 0.8% (7).
  - ⚠ **It's a cluster, not one store:**

| Store | City | Strong share |
|---|---|---|
| #616 | Knoxville | 68.2% |
| #674 | Knoxville | 64.1% |
| #694 | Knoxville | 59.5% |
| #644 | Seymour | 50.0% |
| #682 | Knoxville | 40.2% |
| #632 | Loudon | 39.9% |

**What a hit means / what a miss means**
- Hit: the volume and the #1 rank are real, with no duplicate rows and no sentinel units.
- But the frame changes. Six Knoxville-area Food City stores run 40-68% strong oxycodone, and the median TN Food City runs 12%. That points at a local prescriber source or a regional chain practice, not one rogue counter.
- Miss would have been: duplicate rows, non-tablet units, or a mail-order/LTC buyer. None of those.
- Is it famous? The ARCOS pharmacy lookups have been public since 2019, and East Tennessee pill mills were heavily prosecuted. This store's own coverage is not known to me. **Check the press before calling it new.**

**Corrected headline:** From 2006 to 2012, Food City Pharmacy #674 in Knoxville bought 13.8M oxycodone pills of 30mg or more, 64% of its opioid pills. That's more than any other US pharmacy, and 9.1M of them were immediate-release 30mg. It wasn't alone: five other Knoxville-area Food City stores ran 40-68%, against 3.5% at the median Tennessee pharmacy.

**Portfolio grade:** B. It needs a press, DEA and TN Board of Pharmacy check. The cluster version is the stronger chart.

**Next join that would make it a story:** ARCOS has no prescriber, and the warehouse has nothing prescriber-level for 2006-12. The nearest is CMS Part D prescriber-by-drug (2013+) for oxycodone prescribers in Knox County ZIPs, joined on ZIP / county FIPS 47093. It's lagged a year past ARCOS, so it only finds the tail of the clinics.

---

## Blind spots of my checks
- PSH `SPENDING_PER_MONTH`: I did not confirm whether HUD divides by total or occupied units. So the dollar figure is shown both ways.
- FAA: `LAST_ACTION_DATE` does not say what the action was.
- ARCOS: the IR/ER split uses product-name text (CONTIN / CR / ER). A generic ER line without those words would count as IR.
- The Arizona Food City ownership is from my memory, not from data.
