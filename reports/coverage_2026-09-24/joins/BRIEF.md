# Join pass brief, 2026-09-24

You are building one **portfolio dossier**: one lead, followed across as many warehouse datasets as it honestly reaches.

## Chris's words, verbatim

"3 strong leads is pitiful - do better"
"make sure you completely understand what is completed vs whats not and then continue on - I need things that I can put in a portfolio. Go"

Chris is job hunting. His pitch: **"I can join public datasets."**
A dossier proves that pitch when one entity or place shows up in 3+ unrelated federal datasets, every join is checked, and the result says something a reader cares about.

## Where things are

- The lead you own and its checked numbers are in your assignment. Earlier reports: `reports/coverage_2026-09-24/` (menu.md, deep/, deep2/, skeptic2/), `ledger/findings.tsv`, `reports/actor_pilot_2026-09-24/`.
- `outputs/catalog/plain.json` explains every table and column in plain English. `outputs/catalog/er.json` lists tables and join keys. Search these first to find join targets.
- Read `C:\Users\wroge\.claude\projects\c--Code-Ripple-v6\memory\MEMORY.md` first, and open every trap file touching your tables. Many columns look real and are not.

## Rules

- Door: Python only, from the repo root: `from connect import db; c = db.connect()`. The chat plug-in is dead; don't try it.
- First statements on each connection: `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300`, then `ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'`.
- **Read-only.** SELECT and WITH only. No CREATE, INSERT, UPDATE, DELETE, DROP, ALTER TABLE, no temp tables. The login is the all-powers admin role. Nothing catches a wrong command.
- **Budget: at most 45 statements.** Aggregate before joining. Never raw-join two tables over 20M rows. Start any new table with a LIMIT 5 and a filtered count.
- **Scratch files go only in your own folder** `reports/coverage_2026-09-24/joins/<your id>/`. Never use the shared scratchpad; other agents overwrite it.
- Do not edit the ledger. Do not commit. Do not touch files you did not create.
- Every person or company named is "data match, not verified against primary records."

## How to join honestly

- Prefer real IDs: NPI, CCN, EIN, UEI, FRS/registry ID, CIK. Say which key each join used.
- Name joins need a second field agreeing, such as state, city or address. Single-word name matches are 8% real.
- For every join, report: rows on each side, rows that matched, and a 5-row sample you eyeballed.
- A miss is a result. Say what was checked and what the miss means.
- Compare to a peer group, never only to the nation.
- Money after a date: check each award's first action date.

## Output

Write `reports/coverage_2026-09-24/joins/<your id>.md` and `<your id>.sql` with every statement.

```
# <lead name>
**The one-line story:** plain words, every number checked by you
**Datasets it reaches:** a table: dataset, join key, rows matched, what it adds
**Chain:** for each join, what was checked, what a hit means, what a miss means
**The chart:** one chart that would carry this in a portfolio: type, x, y, the rows to plot (inline, max 30 rows)
**Weak points a hostile editor would hit**
**Outside checks still needed:** news search, court records, the agency's own page
```

End your final reply with: the one-line story, the dataset count, and a grade: A = publishable as is, B = one outside check away, C = not a portfolio piece.
