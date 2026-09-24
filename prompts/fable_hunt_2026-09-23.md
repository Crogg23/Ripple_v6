# The hunt

You're going on a long, open-ended hunt through Ripple's data warehouse.
The job is to find patterns, trends and outliers that nobody has pulled out yet.
Cast a wide net. Every finding has to join at least two tables, and three or more is better.
The best finding crosses domains: health money meets campaign money,
or an EPA violation meets a federal contract.

Chris owns this project. He's a solo builder and an investigative data person.
He'll read what you produce and choose which threads become stories.
Your job is to widen what he can see, not to pick his story for him.

## What you're working with

- **The warehouse:** Snowflake. Around 650 mart tables in `LIBRARY_MARTS`, one schema per domain:
  HEALTH, FINANCE, ENVIRONMENT, JUSTICE, POLITICS, HOUSING, ECONOMICS, CORPORATE_REGISTRY,
  IMMIGRATION, LABOR, PROCUREMENT, EDUCATION, ENERGY, TRANSPORT and more.
  Raw landing tables live in `LIBRARY_RAW.LANDING`. Stay in the marts unless a mart is missing something.
- **The door:** Python only. `from connect import db; c = db.connect()`, run from the repo root.
  The Snowflake chat plug-in is dead. Don't try it, and don't report on it.
- **The map:**
  - `outputs/catalog/er.json` lists every mart table and its columns, with a join-key label on each column.
    Keys, and how many tables carry each: NPI 42, CCN 32, EIN 50, CIK 24, FRS_ID 20, FEC_CMTE_ID 16,
    UEI 12, DUNS 9, LEI 9, BIOGUIDE 19, COUNTY_FIPS 35, NAICS 24, PECOS_PAC_ID 8, EIA_PLANT_ID 10, NPDES_ID 10.
  - `outputs/catalog/plain.json` explains every table and column in plain English.
  - A label is a hint, not proof. Labels have fired on a single word before:
    DRUG_NAME was tagged as a company. Check the values before you join on a column.
- **The traps:** your memory index lists roughly 40 known data traps. Each is a file in the memory folder.
  Read the index before your first query. Open the full file whenever you touch a table it names.
  They're cheap to read and expensive to relearn.

## Hard rules

- **Read only.** The scripts log in as the all-powers admin role, and nothing catches a wrong command.
  Run SELECT and nothing else: no CREATE, INSERT, UPDATE, DELETE, DROP, ALTER TABLE or temp tables.
  CTEs are fine. Pull results down to local files if you need to hold them.
  One exception: `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300` at the start of each connection.
- **Mind the giants.** FEC individual contributions has 284M rows, ARCOS 179M, Part D drug 26M.
  Aggregate or filter them down before you join. Never join two giants raw.
  Start a new table with `LIMIT` and a `COUNT(*)`.
- **Publish nothing.** Don't send email, post anywhere, commit to git or share outside the repo.
  Files under `reports/` and your scratchpad are fine.
- **Never wipe or overwrite a file you didn't create.**

## How a finding earns its place

These are the checks that tripped the last hunt. Treat them as the price of admission.

1. **Check the column is real.** Count its distinct values and look at a sample.
   Watch for suppression markers standing in for numbers: `#`, `*`, blank, `-999`, `'nan'`.
   A suppressed count is hidden, not zero. Drop those rows or model them, and say which you did.
2. **Check the join is real.** After you join on an ID, check that a second field agrees,
   like name or state, and report the agreement rate.
   A name-only join needs at least two words: single-word matches have been 8% real.
3. **Line up the years.** Check each table's year, because different files cover different years.
   Part D drug-level data is 2022, the Part D summary is 2024, and Open Payments has separate 2022, 2023 and 2024 tables.
4. **Read every flag column before you filter on it.** A waiver flag turned a "zero" into a one last time.
   A "reinstated" flag turned out to be False on every row, so filtering on it did nothing.
5. **Build on what's present.** Missing data is a gap in what got loaded, not a finding.
   Never build a finding on absence.
6. **Name the boring explanation.** For every correlation, write down the dull reason it could happen.
   Say whether you ruled it out and how.
7. **Walk the chain.** Each finding records what you checked, what a hit means and what a miss means.
   A label like "anomaly" or "drift" isn't a finding. Name the physical thing:
   "193 doctors banned by OIG took drug-company money in 2024."
8. **Get a skeptic.** Before any finding goes in the top tier, send it to a fresh-context skeptic subagent.
   Give it the claim, the SQL and the numbers. Record both verdicts. If they disagree, keep both.

## Where to start, not where to stop

These are open doors. The table names come from the catalog, so confirm they hold what they claim.
Go past this list. The best thing you find probably isn't on it.

- **Health money:**
  - Do the doctors a drug maker pays prescribe that maker's drugs? Join Open Payments 2022 to Part D drug 2022.
  - Opioid shipments from ARCOS against county overdose deaths from CDC.
  - Nursing-home chains against deficiencies, fines, staffing and Provider Relief Fund dollars.
  - Hospital officer pay against HCRIS cost reports.
- **Politics money:**
  - Corporate insiders from SEC Form 4 who also give to campaigns in FEC data.
  - Senate stock trades against the committees those senators sit on and the bills they back.
  - Lobbying filings against federal contracts and grants.
- **Courts:**
  - Judges' financial disclosures, their investments, against the parties in their own cases.
  - Federal civil case data against corporate registries.
- **Environment:**
  - Facilities with EPA violations and enforcement cases, linked by FRS ID to their corporate parents.
  - Those parents' PAC money and federal contracts.
  - Toxic releases from TRI and drinking-water violations against county health outcomes.
  - FracFocus wells against USGS orphaned wells.
- **Banks and finance:**
  - FDIC enforcement orders against bank branch deposits.
  - HMDA lending against branch deposits, to look for redlining shapes.
  - 13F holdings against insider trades.
  - OpenSanctions and OFAC entities against corporate registries and FATCA.
- **Everything else:** labor and mine safety by MSHA controller, ATF gun dealers against NICS checks,
  immigration detention facilities, police violence against incarceration trends by county, CFPB complaints by company.

Go wide before you go deep. Put at least one real probe into eight or more domains
before you spend long on any single thread. Then go deep on the strongest five.
Cross-domain chains of three or more tables are the prize.

## What to hand back

Put everything in `reports/fable_hunt_2026-09-23/`:

- `log.md`: a running log.
  - After roughly every 20 queries, add a heartbeat line: which domains you've probed, what's live and what's dead.
  - Include your warehouse time so far, from `information_schema.query_history_by_session()`.
- `sql/`: one file per finding, holding the exact queries that produce its numbers.
- `findings.md`: the deliverable. Put a ranked summary at the top, in this shape:
  - one-line headline stated as a fact
  - a fenced block of aligned numbers
  - three to five short bullets: what was checked, what a hit means, what a miss means
  - the tables joined, the join-agreement rate and the skeptic verdict

  Rank the findings in tiers:
  - **A:** survived the skeptic and could anchor a story.
  - **B:** real, but needs outside reporting.
  - **C:** dead ends. Keep them, because a clean miss saves the next person a day.
- For Chris, write short lines and plain words, with tables for things that compare.
  Put numbers in fenced blocks.
  Don't use jargon unless the plain word sits beside it.

Name real people and companies when the data names them.
Mark each one "data match, not verified against primary records."

Stop when the ranked list has at least ten A-tier or B-tier findings, or when new probes stop turning up anything new.
Then write a final heartbeat with your total warehouse time.
