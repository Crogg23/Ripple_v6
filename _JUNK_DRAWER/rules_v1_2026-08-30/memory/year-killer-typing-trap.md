---
name: year-killer-typing-trap
description: "2026-08-22: the typing-rulings rollout mis-ruled 61 year columns as ambiguous_date; the guarded date cast NULLs pure-digit values, so 29 built marts had 100% NULL year columns (Treasury, Open Payments, PBGC, OSHA ITA, foreign aid) — fixed same night; the trap class and how to spot it"
metadata: 
  node_type: memory
  type: project
  originSessionId: d10c26ca-89ea-4453-a057-a3762df38910
  modified: 2026-08-23T00:27:52.172Z
---

The clock-style typing rollout (reports/typing_index/typing_rulings.csv +
scripts/typing/apply_rulings.py) rules a column `ambiguous_date` when its values
parse BOTH as number and date ("both_parse") — but a bare year like `2024`
"parses as a date" only in the trivial sense, and the guarded cast in
macros/ripple_typing.sql deliberately NULLs any pure-digit value that isn't
8-digit YYYYMMDD. Net effect 2026-08-22: **61 year-named columns ruled as dates;
the 29 already applied into mart models produced 100% NULL year columns in the
built marts** — Treasury fiscal/calendar years, all three Open Payments program
years, PBGC data years, all six OSHA ITA years, foreign-aid fiscal year, NHTSA
model years, CDC NNDSS's MMWR year (whose loss masqueraded as 659k "duplicate
keys"), plus two cumulative case-COUNT columns that merely had YEAR in their
names.

**Why:** the ruling heuristic treats "both_parse" as date-leaning; for year
columns the correct ruling is `ambiguous_number` (→ numeric cast). The failure
is silent — the mart builds fine, tests only catch it where a not_null or grain
test happens to touch the column.

**How to apply:**
- Never rule a *_YEAR/_YR-named (or year-semantic) column as any date type;
  rule it ambiguous_number. All 61 CSV rows corrected 2026-08-22; the 29 model
  applications switched to ripple_num and rebuilt green.
- When a uniqueness test "fails with massive duplicates," FIRST check whether a
  key column is 100% NULL — a destroyed grain dimension reads as duplication
  (the NNDSS case). And when a not_null fails at exactly the row count, suspect
  a cast, not the data (the PBGC case).
- Same-night sibling traps confirmed for the completeness ledger: VARIANT chunk
  tables measured by rows not records (see [[completeness-check-traps]]), and
  raw CSV line counts inflated by wrapped quoted fields (ransomware list "37%
  short" was exactly complete). Never compare a mart's deduped business grain
  to a publisher's raw record count (FDA establishment reg).
