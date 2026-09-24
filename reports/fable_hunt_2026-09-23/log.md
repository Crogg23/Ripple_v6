# Fable hunt log — 2026-09-23

Door: Python scripts, `connect/db.py`, role ACCOUNTADMIN, warehouse COMPUTE_WH.
Read-only. Every statement is SELECT/WITH. Session timeout set to 300 s.
Prior hunts already pulled out: pharma-money vs brand %, LEIE excluded-but-paid, nursing-home chains vs fines,
and the FINDINGS schema views (contractor EPA violators, PAC funds both sides, revoked-but-deductible, opioid prescriber paid high rx).
Those are off the table unless a new angle appears.

## Wave 1 — wide probes

Probed so far, one query each unless noted:
- HEALTH: Open Payments 2022 x Part D drug 2022, maker-vs-rival test. LIVE, strong.
- ENVIRONMENT: ECHO x corporate crosswalk x contracts. Crosswalk covers 8% of facilities; ECHO TOTAL_PENALTIES double-counts shared cases (UPS $503M). Parked.
- FINANCE/POLITICS: SEC insiders x FEC donors. First run 0 rows, name-parse bug found (leading space after comma). Rerun pending.
- JUSTICE: judge disclosures x investments x dockets. Link is real: 1.89M holdings, 3,290 judges, 8.1M assigned dockets 2015-25. First pattern run timed out at 300s; pre-filtered rerun works in 47s. Bank names hit deposit accounts, "cisco" hits "Francisco". Refining.
- FINANCE: FDIC enforcement orders x branch deposits. Banks under orders grew deposits 51.7% vs 49.1%. DEAD.
- CONSUMER: CFPB complaints x FDIC orders by bank name. 2 of 30 names match. DEAD as a name join.
- LABOR: MSHA controllers, S&S per 1k employees. Sev.en Global, Foresight, Coronado, Warrior Met at 1,500-1,960. Single-domain so far.
- IMMIGRATION: ICE stints 2022-2026, 2.57M stints, 37 deaths. Facility table joins clean.
- PROCUREMENT: SAM exclusions x contracts (UEI). 33 firms got new awards while excluded. LIVE.
- POLITICS: Senate trades 2012-2020 x committee membership x SIC sector. 41% of health trades by HELP/Finance members. Needs base rate.
- SCIENCE: Retraction Watch authors x NIH PIs. Name join hits 1,101 names; common-name collisions. Refining with PI profile ids.
- HEALTH: hospital officer pay x HCRIS via CCN-EIN crosswalk. 37% of 920 nonprofit hospitals pay top officer more than charity care. LIVE.
- HEALTH: ARCOS 2006-12 pills per capita x CDC overdose 2019-24. Decile 1 to 10: OD rate 13.7 to 23.4. LIVE.
- LOBBYING: LDA clients x contract recipients by name. 995 names match; no angle yet.

Heartbeat 1, 21:35: ~100 statements from this hunt, 278 queries on COMPUTE_WH by this user in the last 2 hours, 12.2 min elapsed, 0.014 cloud-services credits.

## Wave 2 — deepening
- Judges: tightened to stock-looking holdings and ' v. ' case names with company-specific strings. 331 judges, 1,700 cases, 116 companies. Gilstrap E.D. Tex leads.
- SAM x contracts: split mods from new awards. 33 firms with new awards while excluded, $2.10M on the first pass; $0.80M after the skeptic. ATI's $6.8M was all mods on old contracts.
- Hospital pay: restricted to officers and key employees, pay from the org itself. 27% top officer > charity care; 45% all officers > charity care.
- Insiders x FEC: name-parse fixed. 5,362 insiders, 36,301 gifts, $555.5M deduped, $183.5M to super PACs. Bridge from MSHA controllers to executives to FEC works: Alliance Resource CEO Craft $8.2M.
- Retraction Watch x NIH: ORI-investigated papers, unique PI profile ids. 131 co-authors matched, 76 got NIH money after, $187M.
- Senate: base rate run. Banking committee members are 19% of trading senators but make 34% of bank-stock trades. Health and energy are at or below base rate.
- ICE deaths per 100k stints by facility type: Federal/USMS 3.3, Dedicated 1.9, Hold 0.5. 37 deaths total 2022-26.
- PPP x SAM by exact name+state: only EPA facility listings match, which do not bar PPP. Clean miss.
- MSHA controller names x FEC employer strings: 1 hit. Dead as a name join; the insider bridge does the job instead.
- Skeptic 1 (opioids) came back BROKEN on the suppression filter: COUNT_SUP is the count, null = suppressed. Fixed and rerun: 18.7 vs 51.1 per 100k ranked by dose; the skeptic's own rerun ranked by tablets got 20.0 vs 53.0. Saved as a memory trap.

## Wave 3 — skeptics and closing probes
- Five skeptics ran in parallel on the A/B candidates. Verdicts recorded in findings.md, both sides kept.
  - Opioids: BROKEN on the suppression filter, fixed, now stronger. Saved as a trap memory.
  - Pharma money: correlation holds, "moves" does not. Half the gap predates the money.
  - Hospitals: confirmed with caveats; Ochsner and two physician-topped hospitals dropped; the state pattern is hospital size.
  - Debarred firms: facility listings and old-contract orders inflated it; $800K of delivery orders survives, 18 standalone micro-orders.
  - Judges: Gilstrap holds; funds, sold stock and an inherited MDL inflated the rest. Three fixes applied; 331/1,700 became 249/1,180.
- Closing probes: HMDA 2017 denial gaps by lender (B7, names resolved after rebuilding the ARID key), GHGRP emitters vs ECHO (dead, CO2E nulls), ICE deaths per 100k stints (thin), PPP vs SAM (clean miss), Senate base rate (banking over base, health and energy at or under).

Final heartbeat, 22:33: 210 statements ran through this hunt's runner, 13.2 min of runner-measured query time; the five skeptics ran their own queries outside this log.
Warehouse, all queries by this user on COMPUTE_WH in the last 4 hours, skeptics included: 591 queries, 19.4 min elapsed, 16.3 min execution, 421 GB scanned.
Eight runner statements errored, all syntax or 300 s timeouts, none touched data. Nothing written to the warehouse. Nothing committed: the report folder is untracked.

## Closing skeptic
Verdict DONE WITH GAPS. Ten gaps, all fixed or noted in findings.md: two headlines rewritten from their own tables (B6, B10); a dead regex in the judge SQL, single backslashes, fixed and rerun, 249/1,180 became 240/1,157; the narrowed debarment query added as sql/04c and rerun, $0.80M reproduced; line 5 of findings.md restated; the made-up heartbeat time replaced; B8 and B9 carry the skeptic's demotion note and stay B for Chris to decide; the "data match" mark now sits on every A and B section; C-file names mapped.
