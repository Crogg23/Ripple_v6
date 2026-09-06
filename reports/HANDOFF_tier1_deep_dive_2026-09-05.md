# Handoff: Tier 1 investigations, deep dive plus Plotly visuals

Written 2026-09-05 for a new session. Ripple is Chris's solo data-warehouse
investigative project — a Snowflake warehouse of ~2,900 public-records tables
government filings, court records, Medicare/CMS data, campaign finance,
environmental enforcement — built to surface real patterns of fraud, neglect,
and abuse of power. This is not a startup. It's an ambitious solo build, and
Chris treats every claim like a journalist would: nothing is "done" until it's
been run and checked twice.

## The job

Take the 21 hunches below. Each already has a confirmed first number from an
earlier pass — a real query already ran, a real result came back. Your job:

1. **Deepen each one.** Re-run the core query for real, then push past the
   first number — more years, more geography, the obvious follow-up question
   a skeptical editor would ask next.
2. **Verify hard.** Before writing anything as fact, rebuild the number
   independently, the way a fact-checker would, not the way the first analyst
   did. If it doesn't reproduce, say so and say why.
3. **Build one Plotly visual story per hunch.** Not a chart dump — a small
   sequence of 2 to 4 charts that walks a reader with zero context from "here's
   the setup" to "here's the finding" to "here's why it's real." Python,
   `plotly`, saved as standalone HTML so they open with no server.
4. **Write the story in plain English next to the chart.** Chris is going to
   show these to non-technical people. Assume the reader has never heard of a
   CCN, an NPI, or a HOLC grade — explain it once, in one sentence, then never
   again.

## How Chris works, in five rules

- **BAR SPEAK.** Explain it like you're telling a sharp friend at a bar. Plain
  words, short lines. Compress by word choice, never by cutting facts.
- **Every finding walks its chain.** What was checked. What a hit means. What
  a miss means. A label like "vintage drift" is not a finding — the mechanism
  is the finding.
- **Never say "done" without proof.** Run the thing that could disprove your
  own number before you write it down. If you can't verify something, say
  "looks real, not verified yet" — not "confirmed."
- **Money and warehouse changes need a price and a yes first.** Before any
  real spend or hard-to-undo warehouse action, say what it is and what it
  costs, then wait. Read-only SELECT queries for investigation are fine
  without asking.
- **The spine is dead.** Don't call anything you build a "spine." That word is
  retired in this project, permanently.

## Warehouse access

Two doors, and they fail separately — always say which one broke:

- **Python door:** `connect/db.py`, reuses `library-onboarding/snow.py` for
  the actual connection. PAT-as-password, loaded from a gitignored `.env`.
  This is the door that works.
- **Chat plug-in door:** returning 401 as of 2026-09-05. Don't rely on it.

The scripts log in as the all-powers admin role. There is no safety net under
a wrong command — read `.claude/traps.md` before writing anything that isn't a
plain `SELECT`.

## Before you query anything, read these two files

- `.claude/traps.md` — every known data trap in this warehouse: columns that
  look like IDs and aren't, sentinel values, censored fields, epoch-time bugs,
  mart-vs-landing row-count mismatches. Assume any trap in there applies to
  your table until you've personally ruled it out.
- `reports/hunch_master_spreadsheet_2026-09-05.csv` — the full 150-hunch
  spreadsheet this handoff was cut from. Your 21 rows are a subset; the other
  129 have their own tables and traps if you want to cross-reference.

Two traps that will bite immediately on this list:
- A bare table name and its "mart" version can be completely different files
  with wildly different row counts. Check both before trusting a gap.
- Everything in `LIBRARY_RAW.LANDING` is `TEXT`. Dollars, dates, counts — all
  strings. Cast before you compare, every time.

## What "beautiful" means here

Load the `dataviz` skill before writing any chart code. It has the palette,
the accessibility rules, and the interaction patterns Chris wants — don't
freelance a color scheme. The bar is: someone could screenshot one chart and
post it with zero caption and the story still lands.

## Output format

For each hunch, a folder: `reports/tier1_deep_dive_2026-09-05/<id>_<slug>/`
holding:
- `story.html` — the Plotly charts, standalone, opens in a browser
- `findings.md` — the chain: what was checked, what the number is, what a
  skeptic would attack, and the answer to that attack
- the query scripts used, so the numbers can be rebuilt from scratch

One `INDEX.md` at the top of that folder linking all 21, headline number
first, one line each.

## The 21 hunches

### 2. Which nursing home owners get fined the most per home, and does it repeat?

- **Why it matters:** Shows which owners treat fines as a cost of doing business
- **Where we left it:** Confirmed — one chain gets fined 5x more per home than a comparable one
- **Time window:** deficiencies 2017-26, penalties 2023-06 on
- **Watch out for:** penalties file starts 2023-06-17, deficiencies go back to 2017 — don't mix the two windows in one chart.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES`

### 5. Do people get worse loan terms right after a hurricane or flood?

- **Why it matters:** Would show lenders profiting off disaster victims
- **Where we left it:** Confirmed the setup works — 47 disasters checked, more digging needed
- **Time window:** 2015-2017
- **Watch out for:** the small HMDA and LAR tables are samples, 28k and 17k rows — use HISTORIC only, the 45M-row full file.
- **Tables:**
  - `LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS`
  - `LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC`

### 15. Are banned companies still getting paid on disaster relief contracts?

- **Why it matters:** Would be straightforward government fraud
- **Where we left it:** Confirmed — 26 banned companies, $169 million in contracts
- **Time window:** untimed
- **Watch out for:** exclusion effective-date vs contract-award date was never checked in the first pass — do that before calling it timed.
- **Tables:**
  - `LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS`
  - `LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2`

### 22. Do those same neighborhoods have more toxic factories today?

- **Why it matters:** Would prove 90-year-old racist housing policy still poisons people today
- **Where we left it:** CONFIRMED — worst-graded areas have 18x more toxic sites than the best
- **Time window:** current
- **Watch out for:** facility coordinates are stored two different ways in the same table, DDMMSS text vs decimal — convert before mapping, and HOLC_GRADE has 814 blank rows.
- **Tables:**
  - `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY`
  - `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023`
  - `LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY`

### 23. How much money did banned suppliers still collect?

- **Why it matters:** Straightforward fraud, easy to state in dollars
- **Where we left it:** Confirmed — $1.4 billion, one company alone took $860 million
- **Time window:** ingested 2026-07
- **Watch out for:** the supplier file carries no year column at all — state the ingest date, 2026-07-26, before publishing any number as current.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL`

### 27. Are any of them already banned for past fraud?

- **Why it matters:** Would catch fraud before it even starts
- **Where we left it:** Confirmed — 9 found, small but real
- **Time window:** 2026-07 snapshot
- **Watch out for:** the pending-applicant list has 17 duplicate NPIs — dedupe first or a city's real count doubles.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION`

### 30. Do new owners appear right after a home gets penalized, like a shell game?

- **Why it matters:** Would show owners dodging penalties by 'selling' to themselves
- **Where we left it:** Confirmed — 39 homes did exactly this
- **Time window:** penalties 2023-06 on
- **Watch out for:** two 'different' enrollment tables are byte-for-byte the same file — don't join it to itself by accident, and the ownership-change flag is 'N' on every single row, so it can't be used as a filter.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES`

### 31. Do hospital-owned home health agencies perform worse but cost more?

- **Why it matters:** Would show hospitals steering patients to their own worse service
- **Where we left it:** Confirmed pattern, but it cuts both ways — mixed result
- **Time window:** snapshot
- **Watch out for:** star ratings are missing for 37% of independent HHAs vs 5% of hospital-owned ones — the comparison is biased toward the owned group looking better than it is.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH`

### E38. Are drug and device companies still paying them anyway?

- **Why it matters:** Opting out doesn't mean stepping away from industry money
- **Where we left it:** Confirmed — $70.8 million paid to opted-out doctors
- **Time window:** PY2023
- **Watch out for:** opt-out counts rise each year mostly because the opt-out roster itself is growing, not because more doctors are re-entering — fix the cohort to isolate a real trend.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`

### E39. Do the paid ones prescribe way more opioids than unpaid ones?

- **Why it matters:** Would show money buying opioid prescriptions directly
- **Where we left it:** Confirmed — paid ones prescribe opioids at a much higher rate
- **Time window:** two years
- **Watch out for:** this only shows targeting, paid doctors already prescribed more opioids before the money arrived — it does not show the money caused the prescribing.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS`

### E40. Are brand-new doctors billing Medicare for millions in expensive wound-care products?

- **Why it matters:** Would be a fast-growing, hard-to-catch fraud scheme
- **Where we left it:** Confirmed — $1.35 billion in billing, concentrated fast
- **Time window:** DY2024
- **Watch out for:** of the $1.35B total, only about $444M can be tied to a specific confirmed skin-substitute product — say which number you're using.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI`

### E41. Can hospitals still legally order tests and equipment through them?

- **Why it matters:** Would show a loophole letting banned doctors keep working
- **Where we left it:** Confirmed — 7 doctors doing exactly this
- **Time window:** snapshot
- **Watch out for:** 26 of the excluded orderers were excluded before the ordering data was even loaded — check exclusion date against data date, not just against today.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING`

### E42. Is drug industry money still being sent to them?

- **Why it matters:** Would show sloppy or fraudulent payment records
- **Where we left it:** Confirmed — $4.2 million, mostly to just 10 people
- **Time window:** PY2024
- **Watch out for:** 94% of the flagged dollars go to just 10 people — this is a handful of records, not a systemic pattern, until proven otherwise.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`

### E43. Were they already losing money before the sale?

- **Why it matters:** Would show a pattern of dumping failing hospitals
- **Where we left it:** Confirmed — 60% of sold hospitals were losing money first
- **Time window:** FY2022-24
- **Watch out for:** confirm the sale date used is the actual transaction date, not the CHOW filing date — those can be months apart.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER`

### E44. Did its safety violations get worse right before the fines hit?

- **Why it matters:** Adds a timeline to an already-known bad actor
- **Where we left it:** Confirmed with a clear timeline
- **Time window:** 2023-2025
- **Watch out for:** the deficiency data is a rolling three-year window and 2023 is a partial year for half the homes — compare rates, never raw counts.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES`

### E47. Were they already in financial trouble before converting?

- **Why it matters:** Would show the conversion program catching hospitals as they fail
- **Where we left it:** Confirmed — 84% were losing money first
- **Time window:** last full year
- **Watch out for:** small universe, 25 hospitals total — a strong percentage on a small base still needs the raw numbers shown alongside it.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER`

### E48. Were their financial reports already bad beforehand?

- **Why it matters:** Would let regulators predict closures before they happen
- **Where we left it:** Confirmed — 68% were already losing money
- **Time window:** 2024-26
- **Watch out for:** some hospitals that look 'terminated' actually sold and closed, only 3.4% — separate closures from sales before framing this as failure.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER`

### E49. Did they win government contracts specifically during their ban?

- **Why it matters:** A tighter, dated version of #15
- **Where we left it:** Confirmed, but the dollar amount is small
- **Time window:** timed
- **Watch out for:** most of the dollar total is small, 17 of the awards are worth only $43k combined — don't let one big contract carry the whole story.
- **Tables:**
  - `LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS`
  - `LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2`

### E57. Are they also the ones industry pays the most?

- **Why it matters:** Volume and money moving together is a red flag
- **Where we left it:** Confirmed — a real, meaningful overlap
- **Time window:** DY2024
- **Watch out for:** 79% of the overlap dollars are royalty payments, not general payments — say what kind of money it is, not just how much.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`

### E62. Are they still getting cited for missing sprinkler systems?

- **Why it matters:** Would show a safety checkbox that lies
- **Where we left it:** Confirmed as a real data quality problem
- **Time window:** snapshot
- **Watch out for:** the 'sprinklers installed' flag has no 'No' value in the source file, so a blank isn't proof of absence — 64 citations were still open at the snapshot date.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411`
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES`

### E68. Do they give very little free care to the poor despite huge profits?

- **Why it matters:** Would expose 'nonprofit' hospitals not acting like one
- **Where we left it:** Confirmed — 37 hospitals over $50 million profit, under 1% charity care
- **Time window:** FY2023
- **Watch out for:** this is one cost-report year against one BMF snapshot — there's no before/after here, so don't imply a trend, only a point-in-time gap.
- **Tables:**
  - `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS`

## When you're done

Run one skeptic pass per hunch before calling it finished — a fresh-context
review of the claim against the actual data, not against your own memory of
running the query. Report back tier 1 status per hunch: confirmed as
written, confirmed but reframed, or dead — the matrix file it came from
used exactly this language, keep using it.
