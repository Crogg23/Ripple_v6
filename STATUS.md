# RIPPLE STATUS — 2026-08-17 (session 4) — The full spine batch is staged; one rebuild lights it all

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new.** Standing: roll-call vote mart still disagrees with its
Python-built twin. Suite re-run after the batch: 3,034 passed, 2 skipped, that
one pre-existing failure only.

---

## THE HEADLINE: "no bits and pieces" is done — everything rides one rebuild

Chris asked what else should ride the rebuild so it isn't done piecemeal. A
full column sweep over all 2,216 live raw tables found every un-wired
candidate; 41 were measured live against the entity map; every passer is now
staged behind ONE flag (`connect/keys.py: ENABLE_SPINE_BATCH_2026_08`).

**Staged — 48 spec tables total (9 court + 39 batch) + 5 new key families:**
- Charity/tax: IRS exempt-org master file (1.98M charities, 99.95% overlap —
  becomes the golden charity name source), the 527 dark-money family (4
  tables), both failed-pension tables, pension actuarial filings, judges'
  schools.
- Providers/facilities: Medicare enrollment (2.5M, 100%), pharma-payment
  recipient profiles (1.7M), equipment suppliers/referrers, health-center
  sites, hospital price books.
- Money: NIH grants + small-business awards (the spine's FIRST DUNS entities,
  each row carrying UEI too → free old↔new federal-ID crosswalk), auditor
  issuer IDs, fund registries, ticker map, exchange LEIs, UK-sanctioned hulls.
- Environment: the EPA facility registry itself (3.28M, 100%), air program,
  greenhouse gas, toxics 2023, plus the new water-permit family (7 event
  tables, 100.0% referential vs 1.21M permitted facilities).
- New families: courts + judges, water permits, credit unions (incl. the
  merger ledger), ICE detention facilities (2.6M stints, 100.0%).

**Rejected on evidence, documented in code so nobody re-tries them:** FCC EIN
(fully masked), FDIC bank LEI (empty), one dead toxics FRS column, a
25-company SEC feed posing as a registry, three retired-schema tables, one
twin load, and the in-house EPA corporate crosswalk (98.6% unmatched/fuzzy —
stays an overlay; the spine is zero-false-merge). **Parked:** legislator
FEC-IDs (JSON list per row — needs a tiny flatten build; still the cheapest
politics unlock), banking certificate/RSSD family. Fixed in passing: the UK
company-number key's missing collision-math entry.

Flag verified both ways: off = config fingerprint unchanged (incremental
updater unaffected today); on = 173 spine tables / 196 table-key pairs.

## THE DECISION ON CHRIS'S DESK (§8.7)

**The full spine rebuild: ~$10–15, ~4.5h** (may run somewhat longer with the
new 71.7M-docket and water-permit scans — call it $12–20 ceiling). One "go"
buys: judge dossiers + court caseload ledgers, the failed-pension EIN legs,
the charity golden names, 527s, water-permit enforcement chains, credit
unions, detention-by-operator, first DUNS entities — all in one pass, then
incremental re-pins and normal operation resumes.

## Live/open items

- **Rebuild go/no-go (above).** Next session on "go": flip the flag, run
  `connect spine`, re-seed incremental, re-measure the graph (expect ~5 new
  key families and a much bigger EIN/FRS world), update the graph JSON.
- Data-trap repairs ranked by the fill (FAERS 76% dup, contracts epoch dates,
  NEISS future dates, SEC year-zero, foreign-assistance EIN, 2 broken staging
  views).
- FEC-IDs flatten build (small; flips money→votes to hard-ID).
- Source-registry reconciliation (staging→raw leg done; onboarding-log leg
  open).
- Roll-call mart rebuild via Python builder (standing).
- CourtListener citation-network load retry (standing).

**YOUR MOVE:** one word — "go" on the rebuild (price above), or hold.

**NEXT SESSION:**
1. Boot trust check vs this file and git log.
2. On go: flag on → full rebuild → re-seed incremental → re-measure every new
   connection → brief with the new graph numbers.
3. Otherwise: FEC-IDs flatten build or top data-trap repairs.

**Tests:** suite run twice today after changes — 3,034 passed, 2 skipped,
1 pre-existing failure (roll-call mart twin). Nothing new broken.

**COST:** session 4 ~$1-2 — the 41-candidate verification (mostly small
aggregates; a few over 2-8M-row tables) + two local test runs. Whole day
all-in: ~$5.
