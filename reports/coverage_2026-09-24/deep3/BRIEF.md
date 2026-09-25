# Deep pass 3 brief, 2026-09-24

You own 5 warehouse tables that so far got only a 3-query glance: row count, the biggest number, the top names.
Your job: look at each one **properly**, the way a data reporter would, and find what the glance can't.

## Chris's words, verbatim
"3 strong leads is pitiful - do better"
"I need things that I can put in a portfolio."
Asked whether the whole warehouse had been checked, he learned most tables got only a glance, and said: "Yes. Go."

His pitch: "I can join public datasets." A lead only helps if it survives a hostile data editor.

## Your tables
`reports/coverage_2026-09-24/deep3/chunks/<your group>.json` holds each table's plain-English summary, suggested angles (`look_for`), useful columns (`where`), join keys, known traps, and the glance's numbers (`found`, `battery_facts`).
`outputs/catalog/plain.json` explains every column in plain English. `outputs/catalog/er.json` lists join keys across tables.

## What "properly" means: the checks a glance can't do
For each table, pick the 2-3 that fit:
1. **Peer comparison.** Rank actors, places or facilities against their own peer group (same state, same industry, same size), never only the nation.
2. **Time.** Same months across years. Look for breaks, spikes, a series that stops.
3. **Concentration with a denominator.** Who holds an outsized share per patient, per bed, per worker, per person.
4. **One join.** If the table has a real key (NPI, CCN, EIN, UEI, FRS ID, CIK, FIPS, docket), join to one other table that adds harm, money or enforcement. Check the land rate and eyeball 5 rows.
5. **Data trap check.** Constant columns, sentinels, repeated totals, duplicate loads. A trap is a finding for the ledger, not a story.

Reference or lookup tables (code lists, crosswalks, tiny dimension tables): one query to confirm it's a lookup, verdict `skip`, move on. Spend the budget where there's something to find.

## Lessons from today's skeptics (every one of these broke a lead)
- Picking a group for its extreme value, then showing that group is extreme, is circular. Test inside the group.
- Check whether 3-4 units carry the whole effect. Report the median unit too.
- Self-reported or self-coded fields (acuity, "fundraising" labels) can't carry the claim alone.
- Dedupe amendments, original+correction pairs, repeated bulk rows, conduit mirrors.
- Text dates sort wrong. Parse them. Suppressed counts are not always small.
- Name matches need a second field agreeing: city, ZIP, address.
- A miss only means something if the table is complete enough to hit.
- "Missing from a registry" usually tracks age or bans, not wrongdoing.
- Say what the dull explanation is, and test it with one query if you can.

## Rules
- Door: Python only, repo root: `from connect import db; c = db.connect()`. The chat plug-in is dead; don't try it.
- First statements per connection: `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300`, then `ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'`.
- **Read-only: SELECT and WITH only.** No CREATE, INSERT, UPDATE, DELETE, DROP, ALTER TABLE, temp tables. The login is the all-powers admin role; nothing catches a wrong command.
- **Budget: at most 35 statements for all 5 tables.** Aggregate before joining. Never raw-join two tables over 20M rows. Never wrap COUNT(*) in a LIMIT probe on a 50M+ row table.
- Read `C:\Users\wroge\.claude\projects\c--Code-Ripple-v6\memory\MEMORY.md` first and open trap files touching your tables.
- Scratch files only in `reports/coverage_2026-09-24/deep3/<your group>/`. Never the shared scratchpad.
- Do not edit the ledger. Do not commit. Do not touch files you didn't create.
- Every person or company named is "data match, not verified against primary records."

## Output
Write `reports/coverage_2026-09-24/deep3/<your group>.md` (plain words, short lines) and `<your group>.sql` with every statement.
Then return the structured result: one entry per table.

Verdicts:
- `live`: a specific, checked number that could lead a story, with the peer or time comparison done
- `probed`: looked properly, nothing story-grade, but the table is usable
- `dead`: looked properly, nothing there, or the table is broken for this purpose
- `skip`: reference or lookup table
