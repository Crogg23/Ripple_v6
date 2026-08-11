# Entity spine + cross-source connection audit — 2026-08-11

The question: **when Ripple says two records are the same real-world entity, or
joins table A to table B, is that TRUE — and how often?** Measured, not asserted.
Companion to the same day's `warehouse_verification_2026-08-11.md` (single-table
truth) and `warehouse_repair_2026-08-11.md` (the fixes).

## Headline

1. **One real wrong merge, found and fixed.** Placeholder tax ID `999999999`
   fused CVS Pharmacy, SK Telecom, Kingsway Financial, Enstar Group and a literal
   "TEST Company" into ONE entity (`ENT_ce752d70…`, canonical name "TEST COMPANY
   INC1 TESTS") spanning 16 source tables / ~156 source rows. The normalizer
   nulled all-zeros but not all-nines or keyboard walks. Fixed in
   `connect/keys.py` + its `serve/serve_queries.py` mirror; guards red-first.
2. **The connection layer was reading pre-repair copies of two sources.** The
   spine and the flagship debarment lens still pointed at the 9,000-row capped
   SAM exclusions sample (2,940 UEIs) three weeks after — and 4 hours after the
   repair session landed — the full 167,928-row list (38,425 UEIs). Measured
   cost: **53 debarred firms with federal contract awards visible before, 102
   after.** The dbt lead queue had already been repointed; the connection engine
   had not.
3. **A dead source was still wired into the spine.** `FED_NCUA_CALL_REPORTS`
   (NCUA's account dictionary, not call reports — triage A3) contributed an
   EIN key that is 100% empty. Its replacement tables carry no hard ID at all,
   so credit unions are now out of the spine rather than in it on a fake key.
4. **Where joins do fire, they are honest.** Two measured precisions below.
5. **The spine itself is stale and must be rebuilt** for fixes 1–3 to reach the
   warehouse. Priced decision, on Chris.

## 1–2. Precision of identity and of joins (measured)

| join surface | pairs | corroborated | measured precision |
|---|---|---|---|
| debarred firm (SAM, full list) ↔ federal contract recipient, on UEI | 102 | 99 name-match (8-char prefix), 82 exact after punctuation | **97%** |
| OIG-excluded provider ↔ pharma/device payment recipient, on NPI | 350 | 336 exact surname | **96% exact; the other 14 are all hyphen/space variants of the same surname → effectively 100%** |

The 3 UEI non-corroborations are sole-proprietor shape, not wrong merges:
`Badoni Construction Co., LLC` ↔ `WILLIAM BADONI`, `Florence Metals` ↔
`MURAR FLORENCE`, `I-Tek` ↔ `IRIS KIM, INC.` — same UEI, company name on one
side and the owner's name on the other.

Identity precision is structurally protected: the spine clusters on hard
registry IDs only (`GROUP BY key_type, key_value`), never fuses different ID
types, and fuzzy matching stays gated at REVIEW (measured 0.876 precision /
0.46 recall on its best rung — never auto-merged). The failure mode that
remains is not fuzzy matching; it is **a garbage value inside a hard ID**,
which is exactly what finding 1 was.

## 5. Collision hunt

Fan-out is bounded: max source count per entity is 18 of 128 spec'd tables, and
the top of that list is real shared-EIN corporate structure. A sentinel sweep of
repeated-digit and sequential values across `CONNECT_NODES` found:

| key | value | source tables merged |
|---|---|---|
| EIN | 999999999 | **16** |
| COMPANY_NO | 11111111 | 2 |
| CCN | 111111 | 2 |
| EIN | 111111111 / 123456789 / 987654321 / 000000001 | 1 each |
| NPI | 1234567890 | 1 |
| ICPSR | 1,2,3,9,11,22,99,111,… | 1 each (small legislator IDs — real, not fillers) |

Blast radius is small (~156 source rows) but the class is the dangerous one: a
false merge accuses the wrong company. All now normalize to NULL.

## 6. Sentinel keys in joins

The known masked-ID traps do not silently enter the spine — pad-mode
normalization already rejects text sentinels (`<UNAVAIL>` → dropped) and now
rejects numeric fillers too. Three spec tables still nominate columns the
triage file marks dead (FCC licensing EIN, NSF awards EIN, and the retired
credit-union EIN): they contribute no keys rather than bad ones, and the
credit-union one is now removed outright.

## 3. Recall — what SHOULD connect and doesn't

Measured on the flagship "banned but still operating" shape (debarred firms
holding federal contracts), same join, three different copies of the inputs:

| inputs | debarred firms with federal awards |
|---|---|
| capped exclusions sample × spec'd contracts table | **53** (the state before today) |
| full exclusions list × spec'd contracts table | **102** (the state after today's repoint) |
| full exclusions list × the fuller 20M contracts table | **343** |

The 20M contracts table is itself loader-capped at a suspiciously round
20,000,000 rows, so 343 is a floor, not the truth. It carries 420,990 distinct
recipient UEIs against 92,833 in the table the spine reads. **Nothing was wired
to the fuller copy today** — repointing to a knowingly truncated table trades one
wrong number for another; the honest fix is an uncapped re-pull first. Same
shape, unresolved: the 200-row IRS 990 table the spine reads has a 5.5M-row
sibling with EINs.

Overall key coverage of spine inputs: **93.9%** of 806M spine-input rows carry a
usable hard key after normalization (`outputs/_spine_key_health_2026-08-11.json`,
all 146 table-key pairs measured live). The sparse ones are honest publisher
reality, not loss: ship tracks without IMO, assistance awards without UEI,
excluded individuals without a UEI (28% of exclusions rows), OIG exclusions
predating NPI (10%).

## 4 & 7. Key-tier honesty and bridge grain

Nothing downstream treats a weak tier as strong. The spine clusters on hard IDs
only; the fuzzy resolver writes to a separate REVIEW table and never touches the
spine; lens jobs are refused at runtime unless they declare they are running
targeted SQL rather than the fan-out bridge engine. No one-to-many bridge is
consumed as one-to-one in the lens layer.

## 8. Staleness — the layer is behind, on purpose until Chris says go

| artifact | last built | behind by |
|---|---|---|
| who's-who tables (32M entities), golden records, per-source index | **2026-08-08** | 3 days, and now behind today's code fixes too |
| connection edges | 2026-08-09 / 08-10 (incremental) | " |
| connection graph + fingerprint files on disk | 2026-08-09 | " |

Every fix in this report is code-side. **None of it is in the warehouse until
the who's-who build re-runs**, and the placeholder-ID fix invalidates every
existing key value, so an incremental catch-up will not do it — that is the
priced decision handed to Chris.

## 9. Guards added (each verified red on the bad state first)

| defect class | guard |
|---|---|
| placeholder ID merges distinct companies | `tests/test_keys_normalize.py` — offline SQL shape + live: 8 placeholder values must normalize to NULL, 3 real IDs must survive |
| the spine reads a stale/capped copy of a source | `tests/test_spine_inputs_live.py::test_no_spec_table_is_shadowed_by_an_unacknowledged_newer_sibling` |
| a dead key is wired into the spine | `tests/test_spine_inputs_live.py::test_every_spine_key_column_carries_real_values` (146 parametrized cases) |
| serve-layer copy drifts from the engine's normalizer | already existed; it caught this session's one-sided edit immediately |

## Not done / open

- The uncapped USASpending contracts re-pull and the IRS 990 e-file index wiring
  (both are recall gaps with a measured size, both need a pull, not a code edit).
- Publisher-side spot-verification of joined pairs (this audit corroborated both
  sides internally by name; no external fetch).
- The spine's own rebuild (see the price tag in STATUS).

## Addendum — a third and fourth copy of the normalizer, both drifted

The serve-layer drift guard caught one one-sided edit immediately, which
prompted a sweep for every other embedded copy. There were 54 more:

- `cohort_queue.sql` carries a character-for-character copy (guarded since audit
  F6); it was regenerated.
- **53 staging models embed a GENERATED copy** inside their `spine_entity_id`
  expression, so a mart can join the who's-who without calling Python. Those
  copies predated the 2026-07-28 digits-only guard — a text sentinel such as
  NPPES's `<UNAVAIL>` padded into a plausible 9-character value and hashed to an
  entity id **the spine had correctly refused to create**. Those rows carried a
  spine id that joins to nothing, silently, and no test compared them.

All 54 regenerated from the single source of truth, and one new parity test now
covers every embedded copy at once (`tests/test_staging_spine_id_parity.py`),
verified red on all 53 before the fix. This is the same lesson the platform has
now learned three times: **a hand-maintained copy of the key normalizer always
drifts; only a generated-and-guarded copy stays true.**

## Found in passing (not connection-layer)

The roll-call vote metadata is modeled into two marts that disagree — 113,512
rows in one, the pre-re-pull 3,364 in the other. The code was repointed during
the 2026-08-11 repair session but the second table was never rebuilt. It cannot
be rebuilt with dbt: a standing policy guard refuses, because that table is a
mirror of a Python-built canonical table and a dbt rebuild would overwrite
reconciled numbers. The offline suite has been failing on this since the repair
session; the fix is to re-run the Python builder, and it is left for whoever
owns that lane rather than forced past the guard.

## Post-rebuild verification (same evening, Chris said go)

The who's-who was rebuilt on the fixed rules and re-measured:

| check | result |
|---|---|
| placeholder EIN `999999999` entity | **gone** (0 rows) |
| any other repeated-digit / sequential key entity | 1 — UK company number `11111111`, a genuinely registered company appearing in the register and the PSC file (both the same publisher), not a filler |
| debarment source feeding the spine | the full list: **38,424 debarred entities**, up from 2,940 |
| the three dead sources (FCC, NSF, retired credit-union file) | contribute 0 nodes, as intended |
| entities total | 31,887,492 (was 31,852,154) |
| entities appearing in 2+ sources | 15,477,855 |
| debarred entities also present in the contracts source | 102 — matches the pre-rebuild measurement exactly |
| max fan-out | 18 source tables, on a real shared corporate EIN |

Runtime was ~25 minutes, not the ~4.5 hours estimated from the 2026-08-08
precedent, so the actual spend was a small fraction of the $10–15 price tag.

## Addendum 2 — EVERY connection measured, not two

The first pass hand-checked two join surfaces. This closes the gap: because the
spine is hard-ID-only, every connection the platform can make between two
sources is an entity present in both, so a self-join of the per-source entity
index enumerates all of them exactly once. **847 connections**, measured on name
agreement (identical after normalisation, prefix containment, or shared 4+
character token — order-insensitive).

| | |
|---|---|
| connections measured | **847** |
| name-checkable (both sides carry a name) | 661 |
| not name-checkable (one side has no name column) | 186 — reported honestly, not counted as good |
| overall name agreement | **99.4%** (90,507,854 of 91,064,041 compared pairs) |
| connections below 50% agreement | 17, of which 3 were real defects and the rest are naming conventions |

### The three real defects this found

1. **430,916 of 434,040 public water systems were named after one of their own
   wells.** A child table listing wells, tanks and intakes had a stronger
   survivorship rank than the water-system register, so systems came out called
   "WELL #1" or "LA1055063#01". Compounding it, the register itself was pointed
   at a contact-person column, which also put private individuals' names into the
   map ("ALLEN, FRITZ" for the system "ARTISAN CENTER OF CORRALES"). Fixed: the
   register names the system from its own name column; the child table keeps its
   membership but may no longer name its parent.
2. **3,883 political committees were named after a donor.** Every column on a
   contribution row describes the giver, not the committee the ID identifies.
   Fixed: that source contributes membership only, no name or address.
3. **Dialysis clinics fused with doctors.** 69,437 rows of the dialysis facility
   file carry an individual's provider ID (NPPES entity type 1) instead of the
   clinic's — the medical director, most likely — so "DCI ROCKCASTLE" became the
   same entity as the prescriber "Rahman, Khalil". Fixed: that ID dropped as an
   identity key; the facility ID already identifies these clinics.

### The false alarms (joins are correct, publishers just name things differently)

- Person-name order: "Josh Gottheimer" vs "Gottheimer, Josh" — five congressional
  joins flagged only because the first comparator was order-sensitive. Fixed in
  the comparator, not in the data.
- Facility trade name vs owning legal entity ("Oakland Manor Nursing and
  Rehabilitation" vs "OAKLAND MANOR NURSING & REHAB CENTER LLC").
- Clinic vs operating hospital ("MCBAIN PRIMARY CARE" vs "MUNSON HEALTHCARE
  CADILLAC") — same facility ID, one publisher lists the operator.
- Committee vs the candidate it supports — a real relationship, deliberately not
  an identity claim.

Each is listed with its reason in the guard test, so it stays a claim a human
made rather than a silent exception.

### Bridges (the explicit crosswalk table)

Nine bridge types, all built 2026-07-30, all carrying an explicit relation and a
measured fan-out — no one-to-many bridge is presented as one-to-one:

| bridge | rows | relation | fan-out |
|---|---|---|---|
| facility ↔ provider | 2,249,953 | affiliation | up to 6,962 |
| candidate ↔ committee | 218,584 | affiliation | up to 821 |
| facility ↔ company (EPA crosswalk) | 73,948 | same row | 1 |
| facility ↔ provider (same row) | 52,031 | same row | 1 |
| filer ↔ tax ID | 40,440 | same row | 1 |
| legislator IDs | 12,655 / 12,298 | affiliation / same row | 3 / 1 |
| ship IDs | 6,684 | affiliation | up to 21 |

The affiliation bridges are relationships, not identities, and the spine
deliberately does not fuse across them.

### Guard

`tests/test_connection_agreement_live.py` re-measures all 847 connections and
fails on any NEW pair that drops below 50% agreement, plus a map-wide floor of
97%. The legitimate naming-convention pairs are listed with reasons.

### Post-fix re-measure (map rebuilt on the corrected specs)

| | before | after |
|---|---|---|
| connections measured | 847 | 829 (the wrong clinic-to-doctor links are gone) |
| overall name agreement | 99.4% | **99.6%** (90,492,645 of 90,814,433) |
| connections below 50% agreement | 17 | **0** |
| water systems named after a well | 430,916 | **0** |
| committees named after a donor | 3,883 | **0** |
| not name-checkable (one side unnamed) | 186 | 191 - the honest remaining gap |

The guard test passes against the rebuilt map, and would have failed against the
old one: the water-system pair, both donor-name pairs and the clinic-to-doctor
pairs were all below the floor and none of them is on the acknowledged list.
Findings were re-run afterwards on the corrected map; the counts are unchanged
(343 debarred firms with federal awards, 773 banned-from-Medicare with drug-money
records, 236 in billing data), which is the expected result - these fixes changed
what entities are CALLED and one bad identity link, not who is connected to whom
on those surfaces.
