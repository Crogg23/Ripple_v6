# Grow the Wiring — scout + first edge batch (2026-08-21)

Chris said "grow the wiring." This session scouted the 81% dark zone from the
wire-confirm pass and shipped the first edge batch as a preview→apply script.

## The dark zone is three different problems, not one

Top-25 dark tables (they carry 828 of the stuck pair-slots):

| Class | Pair-slots | What it means |
|---|---|---|
| Entity-wireable now | 194 (23%) | Real ID columns exist; edges can be built |
| Geography-only | 147 (18%) | State-level aggregates; wireable only at GEO tier |
| **No entity at all** | **487 (59%)** | National aggregate time series (Treasury daily cash, CDC survey rates, CFTC positions, missile tests…). **These can NEVER be entity-wired.** Their co-movements are macro/climate questions, not connection questions — the honest fix is to label them so in the queue, not to chase wiring that cannot exist. |

Fake-key guard fired once: the FTC datasets table has an `EIN` column with
exactly ONE distinct value — the third sentinel-key catch on this platform
(after NPPES EIN and AIS imo_number).

## The first edge batch (preview verified, awaiting apply)

`scripts/ripples/grow_wiring_pass.py` — preview run 2026-08-21:

| Edge | Key | Tier | Match |
|---|---|---|---|
| BILLS ↔ MEMBER_SPINE | BIOGUIDE | STEEL | 632/632 (100%) |
| BILL_COSPONSORS ↔ MEMBER_SPINE | BIOGUIDE | STEEL | 635/635 (100%) |
| MEMBER_CROSSWALK ↔ MEMBER_SPINE | BIOGUIDE | STEEL | 12,781/12,781 (100%) |
| MEMBER_FEC_ID ↔ MEMBER_SPINE | BIOGUIDE | STEEL | 1,530/1,530 (100%) |
| **MEMBER_FEC_ID ↔ FED_FEC_CANDIDATES** | FEC_CAND_ID | STEEL | 1,132/1,715 (66%) |

The last row is the headline: **the first verified hard link between the
politics cluster and everything else** (landmine 3 said politics had zero).
It lands politics one hop from the whole FEC money graph, which is already
spine-wired. The 34% misses are mostly members predating FEC bulk coverage.

Apply: `python3 scripts/ripples/grow_wiring_pass.py --apply` under a
write-capable role (edge table is ACCOUNTADMIN-owned; the reader PAT fails by
design). Script refuses any edge whose live-measured match rate is below 50%.

## Next wiring moves, ranked by unlocked pair-slots

1. **Queue triage flag** — mark the 59% entity-less pairs "macro, unwireable"
   so the wire-confirm pass stops counting them as fixable debt. (Cheap, big
   honesty win; changes the real wiring gap from 81% to roughly the low 40s.)
2. **GEO-tier edges for state-keyed tables** (CDC anxiety/insurance etc.) —
   147 slots; low trust tier, clearly labeled.
3. **ARCOS distributor names → corporate crosswalk** — 87 distinct company
   names; small but ARCOS is named graph dark matter in the landmine list.
   Name-match tier (CORROBORATED at best), needs manual review of 87 names.
4. Lobby registers (TX/CA) share DOCKET/ZIP shapes — needs a docket-format
   check before proposing anything.

Receipts: `reports/wiring_scout_2026-08-21.json` (full per-table key audit),
`scripts/ripples/grow_wiring_scout.py` (rerunnable, read-only).
