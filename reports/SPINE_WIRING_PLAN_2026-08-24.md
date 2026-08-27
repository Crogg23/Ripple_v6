# Spine Wiring Plan — closing the 178-vs-real gap

**Dated 2026-08-24.** Answers one question: how do we register every table that
carries a real entity ID into the spine, at the same trust level as the 178
tables already done, without guessing.

**Real number, verified this session (not the 670 headline estimate):**
**596 tables**, after removing duplicates and dead weight — down from a raw
769-898 depending on how you slice the audit file, because that raw count
still included:
- `THE_LIBRARY` (the dead, zero-row database)
- the frozen pre-dbt backup database
- `_RESTORE_*` scratch schemas
- `TIMELINE` schema mirrors (same table, materialized twice by dbt)

**596 is the real, deduplicated worklist.** Nothing gets built off the 670
estimate again.

---

## 1. Why this can't be batch-generated

Every existing entry in the spine's registry was hand-verified: which column
is a person's name vs. a company's name, which columns are address, and a
trust rank for when two sources disagree on the same entity's name. Guessing
any of those from column names alone is the exact trap that already burned
this project twice (a column that looks 100% populated and is actually
sentinel-masked junk). **The ID column is free — today's audit already found
it for all 596. The name/address/trust judgment is not free.** That's the
actual work.

## 2. The worklist, broken into batches that make sense to ship separately

Ranked by real key type, biggest first (post-cleanup counts):

| Batch | Key type | Tables | Why this grouping |
|---|---:|---:|---|
| 1 | `NPI` (medical providers) | 116 | One national authority (NPPES), high name-quality, mirrors an already-wired pattern (11 CMS tables already done) |
| 2 | `EIN` (employer tax ID) | 103 | One national authority (IRS), spans many agencies — highest cross-domain payoff |
| 3 | `CCN` (Medicare facility) | 100 | One authority (CMS), same domain as batch 1 |
| 4 | `CIK` + `LEI` + `DUNS` + `UEI` (corporate/financial IDs) | 112 | Same "single company, many federal filings" shape — SEC, GLEIF, SAM |
| 5 | `FRS_ID` + `NPDES_ID` + `PWSID` (EPA facility IDs) | 63 | One domain (environmental), one agency family |
| 6 | `PATENT` + `FEC_CAND_ID` + `FEC_CMTE_ID` + `BIOGUIDE` (misc named-entity IDs) | 66 | Smaller, well-defined, high name-quality |
| 7 | Everything else not yet counted above | ~ remainder | Long tail, one-off key types |
| **Parked** | `DOCKET` | 187 | **Not wired this pass.** Today's audit already found the DOCKET label is mostly noise (city portals mis-tagged as agencies, coincidental number collisions) except a 45-pair federal-courts cluster. That cluster gets its own dedicated "federal case" entity treatment, not folded into this sweep. |

Batches 1-6 = **409 tables** of real, high-confidence work. Batch 7 (the long
tail) gets sized once 1-6 are done and we know real per-table pace.

## 3. The per-table process (same rigor as the 178 that exist today)

For every table, in order, no skipping steps:

1. **Pull live `INFORMATION_SCHEMA` columns** for the table — not the audit
   CSV's cached list, the actual current schema (tables drift; the MSHA view
   bug from today's audit was exactly this kind of drift).
2. **Pull 10 live sample rows.** Identify candidate name column(s) and
   address column(s) by eye, not by column-name pattern-matching.
3. **Run the trap check**: `COUNT(*)` vs `COUNT(DISTINCT normalized_value)`
   vs a 5-value sample, on both the ID column and any candidate name column —
   per the constitution's standing rule. Reject anything that's sentinel-
   masked or fake-populated.
4. **Decide person vs. organization vs. facility** — this determines which
   `DISPLAY_SPECS` shape to use (`person: [last, first]` vs `org: single
   column`).
5. **Set the authority rank** — where does this source rank against others
   that might describe the same entity? Default to "unranked / lowest
   priority" unless there's a clear reason to rank it higher (e.g. it's the
   issuing authority for that ID, like NPPES is for NPI).
6. **Write the entry** into the registry, with a one-line comment recording
   what was checked and when — matching the existing entries' documentation
   style, so the next session can trust it without re-verifying.
7. **Spot-check**: after each batch of ~10-20 tables, run the actual spine
   build against just those tables and confirm no crash, no `<UNAVAIL>` names
   leaking through, row counts sane.

**Anything that fails step 3 or can't get a confident answer at step 4 does
NOT get force-wired.** It gets logged as "known gap, documented reason" —
exactly like the LEIE table already is in the registry today (10.4% joinable,
explicitly accepted rather than papered over).

## 4. What gets automated vs. what stays manual

**Automated (safe to script):**
- Pulling live schema + samples for all 596 tables up front, in bulk — this
  is read-only, cheap, and removes the single biggest slowdown (waiting on
  individual queries).
- The trap check (`COUNT` / `COUNT DISTINCT` / sample) — mechanical, same
  logic already proven in today's audit.
- Drafting a **candidate** name/address column guess per table, to speed up
  the human/AI judgment step — but every candidate is a draft, not an entry,
  until step 4-6 above are done by a person or a session doing real review.

**Stays manual, one table at a time:**
- The actual person/org/facility call.
- The authority rank.
- The final entry + comment.

This mirrors path C from the earlier options list, but scoped correctly:
automation speeds up steps 1-3, never replaces steps 4-6.

## 5. Sizing, honestly

Going by how the 178 existing entries read (short ones are a few lines, hard
ones like NPPES or LEIE carry paragraphs of hand-verified reasoning), a
realistic per-table pace once the bulk schema/sample pull is automated:
**roughly 5-15 minutes of real judgment per table**, faster for
same-authority batches (1, 3, 5) where the pattern repeats, slower for the
mixed-authority batch (4) and the long tail (7).

- Batches 1-6 (409 tables) ≈ **35-100 hours of actual review work**, spread
  across sessions — not a number to round down.
- Batch 7 (the long tail, size TBD after 1-6) — priced once we know real pace.

**This is why "670 properly" was never a one-session ask.** The plan is
sized to be run as a standing backlog: a fixed number of tables wired and
verified per session, batch by batch, checked into the registry as real,
tested work — not a single sprint to declare done.

## 6. Rollout sequence

1. Build the read-only bulk schema+sample+trap-check tool (automatable part,
   §4) — one script, runs once against all 596, produces a per-table draft
   packet (candidate columns + trap-check verdict + red flags).
2. Batch 1 (NPI, 116 tables) as the pilot — smallest-risk, most repetitive
   pattern, existing NPPES entries to model against. Wire + verify + spot-
   check the spine build.
3. Batches 2-6 in the order above, each closed out with a spot-check before
   moving to the next.
4. Re-run this session's audit's overlap pass (the exact technique from
   `key_overlap_edges_new.csv`) after each batch closes, to measure the real
   new-connection yield — this turns "we wired N tables" into "we found N
   new real connections," which is the actual mission metric.
5. Batch 7 (long tail) sized and scoped once 1-6 are done.
6. DOCKET (parked) gets its own separate decision: build the federal-courts
   entity type, or leave the rest alone — that's a scope call for a later
   session, not folded into this backlog.

## 7. Definition of done, per table (so nothing gets marked wired that isn't)

A table only counts as "wired" when all of:
- [ ] Entry exists in the registry with live-verified column names
- [ ] Trap check passed (real distinct values, not masked/sentinel)
- [ ] Person/org/facility call made and stated
- [ ] Authority rank set
- [ ] Spine build re-run including this table, no crash
- [ ] Spot-checked against 3-5 real sample rows that the resolved name/address
      looks right, not garbage

No partial credit. A table that fails any box is a documented gap (like LEIE),
not a silent partial wire.

---

**Next action, pending your go:** build the bulk schema+sample+trap-check
tool (§4, step 1) and run it read-only against all 596 tables. That's prep
work, touches nothing live, and turns this plan into an actual worklist with
real per-table data instead of estimates.

---

## 8. Reconciliation (evening 2026-08-24) — the 596 is not 596 tables of work

Cross-checking every draft packet against the registry the spine actually reads
(it reads `LIBRARY_RAW.LANDING` only, by bare table name) collapsed the list:

| Bucket | Tables | Work? |
|---|---:|---|
| Mart mirror (`LIBRARY_MARTS.*__X`) of a landing table already wired | 156 | none — same data, already in |
| Landing table already wired (audit flagged it unwired by mistake) | 37 | none |
| Derived / meta / retired (FINDINGS, CONNECT outputs, RETIRED schema) | 14 | none — outputs, not sources |
| Mart-only tables with no landing twin (politics marts etc.) | ~20 | parked — spine reads landing only; wiring marts is a design change |
| `DOCKET` landing tables | 135 | parked (audit §6b) |
| **City/state portal crawls** (`PORTAL_*`) | **153** | **scope call for Chris** — 143 of 153 are ≤2,000-row capped crawl samples, 56 have every key column empty |
| **Federal landing tables, unwired** | **30** | **this session** |

Real per-key-type counts on the 30 federal: LEI 2, CCN 1, CL_COURT_ID 1,
NPDES_ID 2, FRS_ID 3, CIK 3, UEI/DUNS 4, ICE_FACILITY 1, EIN 10, NPI 3 (all
three junk), plus 1 crosswalk. The plan's batch sizes in §2 (116 NPI, 103 EIN,
...) counted mirrors and portal crawls; they are superseded by this table.

**Outcome of the 30:** 11 wired (verified live, spot-checked with the spine's
own SELECT), 19 documented gaps (empty/junk scrapes, no recognized key axis,
superseded duplicates, stale test loads, one derived crosswalk). Detail and
reasons live in the registry itself, in the 2026-08-24 batch block.

**New key axes seen while reviewing (parking lot, vote count 1 each):** FCC FRN
(1.69M licence rows), FDIC CERT / Fed RSSD (27,836 banks), CFPB ARID-2017.

**Portal question, framed for Chris:** wiring the 97 portal tables with a real
key means adding ≤2,000-row *samples* of state Medicaid claims, licensing
lists, etc. to the spine — the IDs are real, but each table is a slice, not the
dataset. Options: (a) don't wire samples, re-land the full datasets first;
(b) wire them as-is at lowest authority, labelled sample; (c) wire only the
10 that are >2,000 rows.

---

## 9. Portal ruling and batch 2 (late 2026-08-24)

**Chris's ruling: wire the portal crawls as-is, marked "sample."**

- 153 portal landing tables reviewed. **79 wired** (registry block
  `SPINE_WIRING_PORTAL_SAMPLES_2026_08_24_DISPLAY_SPECS`), each with
  `"sample": True`, authority 9 (below every federal source), and a comment
  carrying dataset title, portal, rows-at-source vs rows-landed, and live
  key/name counts. Every chosen column verified to exist live; every key
  re-counted; every declared name column confirmed non-empty.
- **74 not wired**, reasons in the same block: 56 where every tagged ID
  column is empty in the crawl; 12 Utah trust-lands tables whose "patent
  number" is a land patent, not a US patent; 2 real-patent tables (no
  patent entity type exists — parked); 1 Texas insurance table whose "EIN" is
  the agent's producer number; 1 Washington audit table whose "EIN" is a UBI;
  1 Texas water-utility table whose "CCN" is a PUC certificate; 1 Delaware
  COVID supplier form with free-text DUNS.
- Standing caveat: any finding that leans on a sample-flagged table shows
  who appears in the crawl, not who is in the dataset. Re-landing the full
  datasets (portal_loader.py cap) is the parked follow-up that lifts the flag.
