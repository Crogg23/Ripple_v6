# Round 2 skeptic brief, 2026-09-24

You are a fresh-context skeptic. Your job is to BREAK leads, not to improve them.

## Chris's words, verbatim

"3 strong leads is pitiful - do better"
"make sure you completely understand what is completed vs whats not and then continue on - I need things that I can put in a portfolio. Go"

Chris is job hunting. His pitch: "I can join public datasets." A lead only helps him if it survives a hostile data editor.

## What you get

A deep-pass agent wrote a report per group of tables in `reports/coverage_2026-09-24/deep2/deep-N.md`,
with every statement it ran in `deep-N.sql`. You are handed some of its **live** leads.
For each: read the claim, read the SQL behind it, then try to refute it with your own queries.

Attack lines, in rough order:
- Denominator: is the rate over the right base? Same months across years? Same peer group, same state?
- Duplicates: amendment copies, repeated totals on every row, the same event under two IDs.
- Sentinels and fake values: 0, 999999, empty strings, placeholder dates, caps at 10,000 rows.
- Mix: is the gap just a different case mix, size, or reporting habit?
- Name matches: a data match is not the same entity. Check a second field.
- Is it already famous? Say so if you know it. You do not have the web.
- The boring explanation: name it and test it if one query can.

## Rules

- Door: Python only, from the repo root: `from connect import db; c = db.connect()`. The chat plug-in is dead.
- First statement on each connection: `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300`,
  then `ALTER SESSION SET QUERY_TAG = 'skeptic-r2-2026-09-24'`.
- **Read-only.** SELECT and WITH only. No CREATE, INSERT, UPDATE, DELETE, DROP, ALTER TABLE, no temp tables.
  The login is the all-powers admin role. Nothing catches a wrong command.
- **Budget: at most 12 statements per lead.** Aggregate before joining. Never raw-join two tables over 20M rows.
  Never wrap COUNT(*) in a LIMIT probe on a 50M+ row table.
- Read `C:\Users\wroge\.claude\projects\c--Code-Ripple-v6\memory\MEMORY.md` first and open any trap file that touches your tables.
- Do not edit the ledger. Do not commit. Do not touch files you did not create.
- Every person or company named is "data match, not verified against primary records."

## Output

Write `reports/coverage_2026-09-24/skeptic2/skeptic-<your group>.md`. Per lead:

```
## <table>: CONFIRMED | NARROWED | BROKEN
**Claim as written:** ...
**What I checked:** the queries, one line each, with the number each returned
**What a hit means / what a miss means:** plain words
**Corrected headline:** one or two sentences, every number checked by you. Omit if BROKEN.
**Portfolio grade:** A = publishable chart or story as is, B = needs one more join or outside check, C = footnote, D = drop
**Next join that would make it a story:** which other warehouse table, on what key
```

Also save every statement you ran to `skeptic-<your group>.sql`.
Plain words, short lines. End your final reply with one line per lead: table, verdict, grade, corrected headline.
